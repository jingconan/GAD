ROOT = ''

#################################
##   Parameters For Detector  ###
#################################

#ANO_ANA_DATA_FILE = './Share/AnoAna.txt'
DETECTOR_DESC = dict(
        interval=100,
        win_size=100,
        win_type='time', # 'time'|'flow'
        fr_win_size=100, # window size for estimation of flow rate
        hoeff_far = 0.001,
        fea_option = {'flow_size':(8, [0, 10000])},
        #ano_ana_data_file = ANO_ANA_DATA_FILE,
        normal_rg = None,
	norm_win_ratio = 10,
	#period = 24 * 3600,
        max_detect_num = None,
        data_type = 'fs',
        pic_show = True,
        pic_name = './res2.eps',
        export_flows = None,
        csv = None,
        )


