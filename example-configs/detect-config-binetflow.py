ROOT = ''
# VERSION is used to indicate the config versio. In version 1, fea_option is
# no longer a dict but a array of dict.
VERSION = 1

#################################
##   Parameters For Detector  ###
#################################

ANO_ANA_DATA_FILE = './Share/AnoAna.txt'
DETECTOR_DESC = {
    'version' : VERSION,
    'interval': 20,
    'win_size': 20,
    'win_type': 'time', # 'time'|'flow'
    'fr_win_size': 100, # window size for estimation of flow rate
    'false_alarm_rate': 0.001,
    'fea_option': [
        {
            'feature_name': 'TotBytes',
            'feature_type': 'numerical',
            'quantized_number': 4,
            'range': [0, 50000],
        },
        {
            'feature_name': 'SrcBytes',
            'feature_type': 'numerical',
            'quantized_number': 4,
            'range': [0, 50000],
        },
        {
            'feature_name': 'Proto',
            'feature_type': 'categorical',
            'symbol_index': {
                'tcp': 1,
                'udp': 2,
                'ipx/spx': 3,
                'arp': 4,
                'icmp': 5,
                'pim': 6,
                'rtcp': 7,
                'rtp': 8,
                'igmp': 9,
                'ipv6-icmp': 10,
                'esp': 11,
                'ipv6': 12,
                'DEFAULT': 0
            },
        },


    ],
    'ano_ana_data_file': ANO_ANA_DATA_FILE,
    'normal_rg': None,
    'detector_type': 'mfmb',
    'max_detect_num': 3000,
    'pic_show': True,
    'pic_name': './res.eps',
    'export_flows': None,
    'csv': None,
}
