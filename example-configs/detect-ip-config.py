ROOT = ''

#################################
##   Parameters For Detector  ###
#################################
# ANO_ANA_DATA_FILE = ROOT + '/Share/AnoAna.txt'
ANO_ANA_DATA_FILE = './Share/AnoAna.txt'
DETECTOR_DESC = dict(
        # method = 'mfmb',
        # data = './Simulator/n0_flow.txt',
        # file_type = 'SQL',
        # interval=30,
        # interval=50,
        # win_size = 50,
        # interval=20,
        # interval=4,
        # interval=10,
        interval=30,
        # interval=100,
        # interval=2000,
        # win_size = 10,
        # win_size=100,
        win_size=100,
        # win_size=2000,
        # win_size=20000,
        # win_size=200,
        win_type='time', # 'time'|'flow'
        # win_type='flow', # 'time'|'flow'
        # win_type='flow', # 'time'|'flow'
        fr_win_size=100, # window size for estimation of flow rate
        false_alarm_rate = 0.001,
        unified_nominal_pdf = False, # used in sensitivities analysis
        # discrete_level = DISCRETE_LEVEL,
        # cluster_number = CLUSTER_NUMBER,
        fea_option = {'flow_size': (2, [0, 10000]),
                      'duration':(3, [0, 10]),
                      'cluster': (3, [0, 2]),
                      'dist_to_center': (3, [0, 100000])},
        ano_ana_data_file = ANO_ANA_DATA_FILE,
        # normal_rg = [0, 1000],
        # normal_rg = [0, 1000],
        normal_rg = None,
        # normal_rg = [0, 300],
        # normal_rg = [0, 4000],
        # normal_rg = [0, float('inf')],
        detector_type = 'mfmb',
        max_detect_num = None,
        # max_detect_num = 10,
        # max_detect_num = 20,
        # max_detect_num = 100,
        # data_handler = 'fs',
        data_type = 'fs',
        pic_show = True,
        pic_name = './res2.eps',
        # data_handler = 'fs_deprec',

        export_flows = None,
        csv = None,

        #### only for SVM approach #####
        # gamma = 0.01,

        #### only for Generalized Emperical Measure #####
        small_win_size = 1,
        # small_win_size = 1000,
        g_quan_N = 3,
        )
