ROOT = ''

import numpy as np
#################################
##   Parameters For Detector  ###
#################################
DETECTOR_DESC = dict(
        method = 'robust',
        # method = 'mfmb',
        # data = './Simulator/n0_flow.txt',
        ref_scheck = 'dump',
        interval=100,
        win_size=100,
        win_type='time', # 'time'|'flow'
        fr_win_size=100, # window size for estimation of flow rate
        false_alarm_rate = 0.001,
        unified_nominal_pdf = False, # used in sensitivities analysis
        fea_option = {'flow_size':(2, [0, 10000]), 'duration':(3, [0, 10])},
        # fea_option = {'flow_size':(2, [0, 10000]), 'duration':(3, [0, 10]),
        #               'cluster': (3, [0, 2])},
        dump_folder = ROOT + 'res/',
        normal_rg = None,
        ref_data = ROOT + 'test-data/n0_flow.txt',
        # normal_rg = None,
        detector_type = 'mfmb',
        max_detect_num = None,
        data_type = 'fs',
        pic_show = True,
        pic_name = './res2.eps',
        # data_handler = 'fs_deprec',

        export_flows = None,
        csv = None,

        ####### Only for Robust approach #####
        register_info = {
            'FBAnoDetector' : {
                'type' : 'static',
                'para' : {
                    'normal_rg' : None,
                    },
                'para_type' : 'product',
                },
            'PeriodStaticDetector' : {
                'type' : 'static',
                'para' :  {
                    'period':[10, 100, 1000],
                    'start': [30],
                    'delta_t':[1000],
                    },
                'para_type' : 'product',
                },
            'SlowDriftStaticDetector' : {
                'type' : 'static',
                'para' : {
                    # 'start':np.arange(1, 168, 6) * 3600,
                    'start':np.linspace(1, 3000, 3),
                    'delta_t':[100, 300]
                    },
                'para_type' : 'product',
                },
            },

        #### only for SVM approach #####
        # gamma = 0.01,

        #### only for Generalized Emperical Measure #####
        small_win_size = 1,
        # small_win_size = 1000,
        g_quan_N = 3,
        )
