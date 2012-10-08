"""
This file defines useful APIs for other modules or program to use
"""
from __future__ import print_function, division
#######################################################
###        Import Detectors                        ####
#######################################################
from StoDetector import ModelFreeAnoDetector, ModelBaseAnoDetector, FBAnoDetector
from SVMDetector import SVMFlowByFlowDetector, SVMTemporalDetector
from ART.ART import ARTDetector

# detector_map defines correspondence between detector
# options with detector name
detector_map = {
        'mf': ModelFreeAnoDetector,
        'mb': ModelBaseAnoDetector,
        'mfmb': FBAnoDetector,
        'svm_fbf': SVMFlowByFlowDetector,
        'svm_temp': SVMTemporalDetector,
        'art': ARTDetector,
        }

# usually one detector corresponds to one handler
# handlers do some data preprocessing for detector.
from DataHandler import *
data_handler_handle_map = {
        'mf': QuantizeDataHandler,
        'mb': QuantizeDataHandler,
        'mfmb': QuantizeDataHandler,
        'svm_temp': SVMTemporalHandler,
        'svm_fbf':QuantizeDataHandler,
        'art': FakeDataHandler,
        }

from Data import *
data_map = {
        'fs': PreloadHardDiskFile,
        'pcap2netflow': PreloadHardDiskFile_pcap2netflow,
        'xflow': PreloadHardDiskFile_xflow,
        'SQLFile_SperottoIPOM2009': SQLFile_SperottoIPOM2009,
        'flow_exporter': PreloadHardDiskFile_FlowExporter,
        }

def print_detector_help(type_):
    """print help message of detector with type_
    """
    detector = detector_map[ type_ ]({})
    detector.set_args(['-h'])

def detect(f_name, desc, res_args=[]):
    """An function for convenience
    - *f_name* the name or a list of name for the flow file.
    - *desc* is a parameter dictionary
    """
    win_size = desc['win_size']
    fea_option = desc['fea_option']
    data_file = data_map[ desc['data_type'] ](f_name)
    data_handler = data_handler_handle_map[desc['detector_type']](data_file, win_size, fea_option)
    detector = detector_map[ desc['detector_type'] ](desc)
    detector.set_args(res_args)
    detector.detect(data_handler)
    return detector

def detector_plot_dump(data_name, type_, desc, *args, **kwargs):
    """don't actually detect, only plot precalculated data
    """
    detector = detector_map[type_](desc)
    detector.set_args([])
    detector.plot_dump(data_name, *args, **kwargs)

def test_detect():
    ANO_ANA_DATA_FILE = './test_AnoAna.txt'
    DETECTOR_DESC = dict(
            interval=20,
            win_size=400,
            win_type='time', # 'time'|'flow'
            fr_win_size=100, # window size for estimation of flow rate
            false_alarm_rate = 0.001,
            unified_nominal_pdf = False, # used in sensitivities analysis
            fea_option = {'dist_to_center':2, 'flow_size':2, 'cluster':2},
            ano_ana_data_file = ANO_ANA_DATA_FILE,
            detector_type = 'mfmb',
            data_handler = 'fs',
            )
    desc = DETECTOR_DESC
    detector = detect('../Simulator/n0_flow.txt', desc)
    detector.plot_entropy()

if __name__ == "__main__":
    test_detect()
