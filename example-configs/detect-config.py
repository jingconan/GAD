ROOT = ''

#################################
##   Parameters For Detector  ###
#################################

ANO_ANA_DATA_FILE = './Share/AnoAna.txt'
DETECTOR_DESC = dict(
        interval=100,
        win_size=200,
        win_type='time', # 'time'|'flow'
        fr_win_size=100, # window size for estimation of flow rate
        false_alarm_rate = 0.001,
        fea_option = {'flow_size':(4, [0, 50000])},
        ano_ana_data_file = ANO_ANA_DATA_FILE,
        normal_rg = None,
        detector_type = 'mfmb',
        max_detect_num = None,
        data_type = 'fs',
        pic_show = True,
        pic_name = './res.eps',
        export_flows = None,
        csv = None,
        )