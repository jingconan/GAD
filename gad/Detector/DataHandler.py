#!/usr/bin/env python
""" Handler Class for Data Files
"""
from __future__ import print_function, division, absolute_import
__author__ = "Jing Conan Wang"
__email__ = "wangjing@bu.edu"

from .ClusterAlg import KMedians
from .DetectorLib import vector_quantize_states, model_based, model_free
from ..util import DF, NOT_QUAN, QUAN
from ..util import abstract_method, FetchNoDataException, DataEndException
# from scipy.cluster.vq import whiten
import numpy as np

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
        self.cater_feature_option = []

        for idx, option in enumerate(self.fea_option):
            self.fea_list.append(option['feature_name'])
            if option['feature_type'] == 'categorical':
                symbol_index = option['symbol_index']
                min_index = min(symbol_index.values())
                max_index = max(symbol_index.values())
                self.fea_QN[idx] = max_index - min_index + 1
                self.global_fea_range[idx, 0] = min_index
                self.global_fea_range[idx, 1] = max_index

                self.cater_feature_option.append({
                    'feature_index': idx,
                    'symbol_index': symbol_index,
                })
            elif option['feature_type'] == 'numerical': # numerical
                self.fea_QN[idx] = option['quantized_number']
                self.global_fea_range[idx, 0] = option['range'][0]
                self.global_fea_range[idx, 1] = option['range'][1]
            else:
                raise Exception('unknown feature_type')

        self.global_fea_range = np.array(self.global_fea_range)

    def get_quantized_levels(self):
        return self.fea_QN

    def _init_data(self, data):
        self.data = data

    def get_em(self, rg=None, rg_type='time'):
        abstract_method()

    def get_fea_list(self):
        return self.fea_list

    def _map_categorical_feature(self, raw_data, feature_option):
        mapped_data = []
        for fea_vec in raw_data:
            for option in feature_option:
                index = option['feature_index']
                symbol_index = option['symbol_index']
                mapped_val = symbol_index.get(fea_vec[index], None)
                if mapped_val is None:
                    mapped_val = symbol_index.get('DEFAULT', None)
                    print('[warning] default value is used for symbol: ' +
                          fea_vec[index])
                if mapped_val is None:
                    raise Exception('[error] cannot find symbol %s in '
                                    'symbol_index of detector config! Pls '
                                    'verify your config file.'
                                    % (fea_vec[index]))

                fea_vec[index] = mapped_val
            mapped_data.append(fea_vec)
        return mapped_data

    def get_fea_slice(self, rg=None, rg_type=None):
        data = self.data.get_rows(self.get_fea_list(), rg, rg_type)

        if self.desc.get('version', 0) >= 1:
            data = self._map_categorical_feature(data,
                                                 self.cater_feature_option)

        if not isinstance(data, (np.ndarray, np.generic) ):
            data = np.array(data, dtype=float)

        if data is None or len(data) == 0:
            raise FetchNoDataException("Didn't find any data in this range")
        return data

    def quantize_fea(self, rg=None, rg_type=None):
        """get quantized features for part of the flows"""
        fea_vec = self.get_fea_slice(rg, rg_type)
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



class IPDataHandler(QuantizeDataHandler):
    """ Cluster and IP address and Quantize the feature in the Data

    Parameters
    ----------------
    fea_option : dict
        specified the quantized level for each feature


    Examples
    ---------------
    >>> from .Data import MEM_DiskFile
    >>> data = MEM_DiskFile('Test/n0_flow.txt')
    >>> fea_option = dict(cluster=2, dist_to_center=2, flow_size=2)
    >>> dh = QuantizeDataHandler(data, dict(fea_option=fea_option))
    finish get ip address
    start KMedians ...
    >>> flows = dh.quantize_fea([0, 100], 'flow')
    >>> print(len(flows))
    3
    >>> print(len(flows[0]))
    100
    """
    def __init__(self, data, desc):
        super(QuantizeDataHandler, self).__init__(data, desc)
        self._init_data(data)
        fea_option = desc['fea_option']
        self.fea_option  = fea_option
        self.direct_fea_list = [ k for k in fea_option.keys() if k not in ['cluster', 'dist_to_center']]
        self.fea_QN = [fea_option['cluster'], fea_option['dist_to_center']] + [fea_option[k] for k in self.direct_fea_list]

        self._cluster_src_ip(fea_option['cluster'])
        self._set_fea_range()

    def _cluster_src_ip(self, cluster_num):
        src_ip_int_vec_tmp = self.data.get_rows('src_ip')
        src_ip_vec = [tuple(x) for x in src_ip_int_vec_tmp]

        unique_ip = list( set( src_ip_vec ) )
        # unique_src_cluster, center_pt = KMeans(unique_src_IP_vec_set, cluster_num, DF)
        unique_src_cluster, center_pt = KMedians(unique_ip, cluster_num, DF)
        self.cluster_map = dict(zip(unique_ip, unique_src_cluster))
        # self.center_map = dict(zip(unique_src_IP_vec_set, center_pt))
        dist_to_center = [DF( unique_ip[i], center_pt[ unique_src_cluster[i] ]) for i in xrange(len(unique_ip))]
        self.dist_to_center_map = dict(zip(unique_ip, dist_to_center))


    def _set_fea_range(self):
        """set the global range for the feature list, used for quantization"""
        # set global fea range
        min_dist_to_center = min(self.dist_to_center_map.values())
        max_dist_to_center = max(self.dist_to_center_map.values())

        # min_vec = self.data.get_min(self.direct_fea_list)
        # max_vec = self.data.get_max(self.direct_fea_list)
        min_vec, max_vec = self.data.get_min_max(self.direct_fea_list)

        self.global_fea_range = [
                [0, min_dist_to_center] + min_vec,
                [self.fea_option['cluster']-1, max_dist_to_center] + max_vec,
                ]

    def get_fea_list(self):
        return ['cluster', 'dist_to_center'] + self.direct_fea_list

    def get_fea_slice(self, rg=None, rg_type=None):
        """get a slice of feature. it does some post-processing after get feature
        slice from Data. First it get *direct_fea_vec* from data, which is defined
        in **self.direct_fea_list**. then it cluster
        the source ip address, and insert the cluster label and distance to the
        cluster center to the feature list.
        """
        # get direct feature
        direct_fea_vec = self.data.get_rows(self.direct_fea_list, rg, rg_type)
        if direct_fea_vec is None:
            raise FetchNoDataException("Didn't find any data in this range")

        # calculate indirect feature
        src_ip = self.data.get_rows('src_ip', rg, rg_type)
        fea_vec = []
        for ip, direct_fea in izip(src_ip, direct_fea_vec):
            fea_vec.append( [self.cluster_map[tuple(ip)],
                self.dist_to_center_map[tuple(ip)]] + [float(x) for x in direct_fea])

        self.quan_flag = [QUAN] * len(self.fea_option.keys())
        self.quan_flag[0] = NOT_QUAN
        # return fea_vec, fea_range
        return fea_vec


class ModelFreeQuantizeDataHandler(QuantizeDataHandler):
   def get_em(self, rg, rg_type):
       """get model-free empirical measure"""
       q_fea_vec = self.quantize_fea(rg, rg_type )
       return model_free( q_fea_vec, self.fea_QN )

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

