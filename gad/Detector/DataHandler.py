#!/usr/bin/env python
""" Handler Class for Data Files
"""
from __future__ import print_function, division, absolute_import
__author__ = "Jing Conan Wang"
__email__ = "wangjing@bu.edu"

import collections

from ..util import DF, NOT_QUAN, QUAN
from ..util import abstract_method, FetchNoDataException, DataEndException
from ..util.ClusterAlg import KMedians
from .DetectorLib import vector_quantize_states, model_based, model_free
# from scipy.cluster.vq import whiten
import numpy as np

# TODO(hbhzwj) Right now the usage of processor is to covert other types of
# data to numerical data, which faciliate the quantization process. Note that
# quantization of numerical values are not handled by processors, but
# implemented in function quantize_fea().
# Should unify them without sacrifice performance.
class FeatureProcessor(object):
    """FeatureProcessor defines interface a transformation of a feature.
    """
    def __init__(self, fea_id, option):
        self.fea_id = fea_id
        self.option = option

    def init_handler_state(self, handler):
        abstract_method()

    def process_feature(self, input):
        abstract_method()

class NumericalFeatureProcessor(FeatureProcessor):
    def init_handler_state(self, handler):
        option = self.option
        handler.fea_QN[self.fea_id] = option['quantized_number']
        handler.global_fea_range[self.fea_id, 0] = option['range'][0]
        handler.global_fea_range[self.fea_id, 1] = option['range'][1]

    def process_feature(self, input):
        return input

class CategoricalFeatureProcessor(FeatureProcessor):
    """Processor that transforms categorical symbols to numerical values.
    """
    def init_handler_state(self, handler):
        symbol_index = self.option['symbol_index']
        min_index = min(symbol_index.values())
        max_index = max(symbol_index.values())
        handler.fea_QN[self.fea_id] = max_index - min_index + 1
        handler.global_fea_range[self.fea_id, 0] = min_index
        handler.global_fea_range[self.fea_id, 1] = max_index

    def process_feature(self, input):
        option = self.option
        symbol_index = option['symbol_index']
        mapped_val = symbol_index.get(input)
        if mapped_val is None:
            mapped_val = symbol_index.get('DEFAULT', None)
            #  print('[warning] default value is used for symbol: ' +
            #        input)
        if mapped_val is None:
            raise Exception('[error] cannot find symbol %s in '
                            'symbol_index of detector config! Pls '
                            'verify your config file.'
                            % (input))
        return mapped_val

class IPv4AddressFeatureProcessor(CategoricalFeatureProcessor):
    """Processor that transforms IPv4Address to numerical values.

    This processors cluster all IPs using KMedians clustering algorithm and
    map each IP to its cluster id.
    """

    def _generate_symbol_index(self, handler):
        from ..util.ClusterAlg import KMedians
        from ..util import DF

        ip_cluster_num = self.option['ip_cluster_num']
        #  distance_quantize_num = self.option['distance_quantize_num']
        if 'ip_columns' in self.option:
            ip_feature_columns = self.option['ip_columns']
        else:
            ip_feature_columns = self.option['feature_name']

        all_ips = handler.data.get_rows(ip_feature_columns)
        unique_str_ip = set(all_ips.flatten())

        unique_ip = []
        for ip in unique_str_ip:
            tokens = ip.split('.')
            if len(tokens) != 4:
                continue
            unique_ip.append(tuple(int(t) for t in tokens))

        unique_src_cluster, center_pt = KMedians(unique_ip,
                                                 ip_cluster_num,
                                                 DF)

        # self.center_map = dict(zip(unique_src_IP_vec_set, center_pt))
        #  dist_to_center = [DF( unique_ip[i], center_pt[ unique_src_cluster[i] ]) for i in xrange(len(unique_ip))]
        #  dist_rg = [min(dist_to_center), max(dist_to_center)]
        # quantize distance to _center
        #  symbol_length = (dist_rg[1] - dist_rg[0]) * 1.0 / distance_quantize_num
        #  dtc = np.array(dist_to_center)
        #  quantized_dtc = (dtc - dist_rg[0]) / symbol_length

        symbol_index = dict()
        for i, ip in enumerate(unique_ip):
            ip_str = '%i.%i.%i.%i' % ip
            symbol_index[ip_str] = unique_src_cluster[i]
            #  symbol_index[ip_str] = \
            #      distance_quantize_num * unique_src_cluster[i] + \
            #      quantized_dtc[i]

        symbol_index['DEFAULT'] = self.option['DEFAULT']
        return symbol_index

    def init_handler_state(self, handler):
        if not self.option.get('symbol_index'):
            self.option['symbol_index'] = self._generate_symbol_index(handler)

        # save the symbol_index to save the clustering step.
        if self.option.get('save_symbol_index_path'):
            import json
            with open(self.option['save_symbol_index_path'], 'w') as fid:
                json.dump(self.option['symbol_index'], fid)

        CategoricalFeatureProcessor.init_handler_state(self, handler)

class PortFeatureProcessor(CategoricalFeatureProcessor):
    K_MAX_PORT_NUM = 65535
    K_INVALID_PORT = -1
    def init_handler_state(self, handler):
        handler.fea_QN[self.fea_id] = self.option['quantized_number']
        handler.global_fea_range[self.fea_id, 0] = 0
        handler.global_fea_range[self.fea_id, 1] = self.K_MAX_PORT_NUM

    def process_feature(self, input):
        try:
            output = int(input)
        except:
            output = self.K_INVALID_PORT
        return output


FEATURE_PROCESSOR_MAP = {
    'categorical': CategoricalFeatureProcessor,
    'numerical': NumericalFeatureProcessor,
    'ipv4_address': IPv4AddressFeatureProcessor,
    'port': PortFeatureProcessor,
}


##############################################################
####                  Interface Class                   ######
##############################################################
class DataHandler(object):
    """ virtual base class for Data Hanlder. Data Handler contains one or more
    Data class as the data source. And it generate the emperical measure based
    on the data class.
    """
    def __init__(self, data, desc):
        self.data = data
        self.desc = desc

    def get_em(self, rg=None, rg_type='time'):
        """get emperical measure within a range. emeprical measure is used to
        represent the data in this range. For example, it can the probability
        distribution of flow quantization state within and range(*for the model
        free case*), or the markovian trantion probability for the *model based*
        case"""
        abstract_method()

    def get_fea_slice(self, rg=None, rg_type=None):
        """Get feature slice within a range"""
        abstract_method()

    def get_fea_list(self):
        """Get feature list"""
        abstract_method()


from socket import inet_ntoa
from struct import pack
def long_to_dotted(ip):
    ip_addr = inet_ntoa(pack('!L', ip))
    return [int(val) for val in ip_addr.rsplit('.')]

from .DetectorLib import get_feature_hash_list
from ..util import izip

class QuantizeDataHandler(DataHandler):
    def __init__(self, data, desc):
        super(QuantizeDataHandler, self).__init__(data, desc)
        self._init_data(data)
        if desc.get('version', 0) == 0:
            self._parse_desc_v0(desc)
        else:
            self._parse_desc_v1(desc)

    def _parse_desc_v0(self, desc):
        fea_option = desc['fea_option']
        self.fea_option  = fea_option
        self.fea_list = fea_option.keys()
        self.fea_QN, self.global_fea_range = zip(*fea_option.values())
        self.global_fea_range = np.array(self.global_fea_range, dtype=np.float)

    def _parse_desc_v1(self, desc):
        self.fea_option = desc['fea_option']
        fea_num = len(self.fea_option)
        self.fea_list = []
        self.fea_QN = np.zeros((fea_num,))
        self.global_fea_range = np.zeros((fea_num, 2))

        # TODO I make processors to be dict. the key is feature idx, the value
        # is a list of processor, which will be applied sequentially.
        self.processors = collections.defaultdict(list)
        for idx, option in enumerate(self.fea_option):
            self.fea_list.append(option['feature_name'])
            processor = FEATURE_PROCESSOR_MAP[option['feature_type']](idx,
                                                                      option)
            processor.init_handler_state(self)
            self.processors[idx].append(processor)

        self.global_fea_range = np.array(self.global_fea_range)

    def get_quantized_levels(self):
        return self.fea_QN

    def _init_data(self, data):
        self.data = data

    def get_em(self, rg=None, rg_type='time'):
        abstract_method()

    def get_fea_list(self):
        return self.fea_list

    def _process_feature(self, row):
        fea_dim = len(row)
        for i in xrange(fea_dim):
            option = self.fea_option[i]
            if option['feature_type'] == 'numerical':
                continue
            for processor in self.processors[i]:
                row[i] = processor.process_feature(row[i])
        return row

    def get_fea_slice(self, rg=None, rg_type=None):
        data = self.data.get_rows(self.get_fea_list(), rg, rg_type)

        if self.desc.get('version', 0) >= 1:
            data = [self._process_feature(row)
                    for row in data]

        if not isinstance(data, (np.ndarray, np.generic) ):
            data = np.array(data, dtype=float)

        if data is None or len(data) == 0:
            raise FetchNoDataException("Didn't find any data in this range")
        return data

    def quantize_fea(self, rg=None, rg_type=None):
        """get quantized features for part of the flows"""
        fea_vec = self.get_fea_slice(rg, rg_type)
	fea_vec = np.array(fea_vec.tolist())
        fr = self.global_fea_range
        quan_len = (fr[:, 1] - fr[:, 0]) / self.fea_QN
        min_val = np.outer(np.ones(fea_vec.shape[0],), fr[:, 0])
        q_fea_vec = (fea_vec - min_val) / quan_len
        q_fea_vec = np.floor(q_fea_vec)
        q_fea_vec = np.clip(q_fea_vec, [0] * len(self.fea_QN),
                np.array(self.fea_QN) - 1)
        return q_fea_vec.T

    def hash_quantized_fea(self, rg, rg_type):
        q_fea_vec = self.quantize_fea(rg, rg_type)
        return get_feature_hash_list(q_fea_vec, self.fea_QN)


class ModelFreeQuantizeDataHandler(QuantizeDataHandler):
   def get_em(self, rg, rg_type):
       """get model-free empirical measure"""
       q_fea_vec = self.quantize_fea(rg, rg_type)
       return model_free( q_fea_vec, self.fea_QN)

class ModelBasedQuantizeDataHandler(QuantizeDataHandler):
   def get_em(self, rg, rg_type):
       """get model-based empirical measure"""
       q_fea_vec = self.quantize_fea(rg, rg_type )
       return model_based( q_fea_vec, self.fea_QN )

class FBQuantizeDataHandler(QuantizeDataHandler):
    def get_em(self, rg=None, rg_type=None):
        """get empirical measure"""
        q_fea_vec = self.quantize_fea(rg, rg_type )
        pmf = model_free( q_fea_vec, self.fea_QN )
        Pmb = model_based( q_fea_vec, self.fea_QN )
        return pmf, Pmb

class GeneralizedEMHandler(DataHandler):
    """ Generalized Emperical Measure Handler

    Can Treat the emperical measure caculated by normal data handler as
    feature and calcuale the generalized EM
    """
    def __init__(self, data, desc):
        super(GeneralizedEMHandler, self).__init__(data, desc)
        self.desc = desc
        self.small_win_size = desc['small_win_size']
        self.g_quan_N = desc['g_quan_N']
        self.handler = QuantizeDataHandler(data, desc)

    def quantize_fea(self, rg=None, rg_type=None):
        """get quantized features for part of the flows"""
        fea_vec = self.get_fea_slice(rg, rg_type)
        q_fea_vec = vector_quantize_states(izip(*fea_vec), self.fea_QN,
                izip(*self.global_fea_range), self.quan_flag)
        return q_fea_vec

    def cal_base_em_list(self, rg, rg_type):
        """calculate all the base emperical that will be used as feature"""
        if rg is None:
            rg = [0, float('inf')]

        pt = rg[0]
        em_list = CombinedEMList()

        while pt <= rg[1]:
            try:
                em = self.handler.get_em(
                        rg=[pt, pt+self.small_win_size],
                        rg_type=rg_type)
                # print('t: %i em: %s'%(pt, em))
                em_list.append( em )
                pt += self.small_win_size
            except FetchNoDataException:
                print('there is no data to detect in this window')
            except DataEndException:
                print('reach data end, break')
                if rg[1] != float('inf'):
                    raise
                break

        self.em_list = em_list
        # print('leng, ', len(self.em_list.data))

    def get_em(self, rg, rg_type):
        self.cal_base_em_list(rg, rg_type)
        self.em_list.regularize()
        self.em_list.quantize(self.g_quan_N)

        mf = self.get_mf_dist()
        mb = self.get_mb_dist()
        return mf, mb[0], mb[1]


class QuantizeGeneralizedEMHandler(GeneralizedEMHandler):
    def get_em(self, *args, **kwargs):
        """get generalized emperical measure
        """
        return self.handler.get_em(*args, **kwargs)



""" The following two handlers has the same output with QuantizeDataHandler,
which means it can work with any Detector that receive QuantizeDataHandler,
which includes:
    1. ModelFreeAnoDetector
    2. ModelBaseAnoDetector
    3. FBAnoDetector
    4. PeriodStoDetector
    5. TwoWindowAnoDetector
    6. AutoSelectStoDetector
"""

class ModelFreeFeaGeneralizedEMHandler(GeneralizedEMHandler):
    """ calculate the model free and model based emprical measure when the
    underline feature is model free emperical empeasure
    """
    def get_mf_dist(self):
        """ model free distribution of model free emperical measure
        """
        N = len(self.em_list[0].mf.flatten())
        # return model_free([flatten(em.mf) for em in self.em_list],
        #         [self.g_quan_N]*N)
        print('len self.em_list', len(self.em_list))
        mf = model_free([flatten(em.mf) for em in self.em_list],
                [self.g_quan_N]*N)
        print('mf ', mf )
        return mf

    def get_mb_dist(self):
        """ model free distribution of model free emperical measure
        """
        N = len(self.em_list[0].mf.flatten())
        return model_based([flatten(em.mf) for em in self.em_list],
                [self.g_quan_N]*N)

class ModelBasedFeaGeneralizedEMHandler(GeneralizedEMHandler):
    """ calculate the model free and model based emprical measure when the
    underline feature is model based emperical empeasure
    """
    def get_mf_dist(self):
        """ model free distribution of model based emperical measure
        """
        N = len(self.em_list[0].mb[0].flatten())
        return model_free([flatten(em.mb[0]) for em in self.em_list],
                [self.g_quan_N]*N)

    def get_mb_dist(self):
        """ model based distribution of model based emperical measure
        """
        N = len(self.em_list[0].mb[0].flatten())
        return model_based([flatten(em.mb[0]) for em in self.em_list],
                [self.g_quan_N]*N)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

