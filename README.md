Introduction
============
**GAD** is the acronym of General Anomaly Detector. It was
once part of **[SADIT](https://github.com/hbhzwj/SADIT)**. We can now use the two packages either jointly or separately. Here are their main differences:

1. **SADIT** focuses on providing  an integrated interface for generating
test data and evaluating algorithms.

2. **GAD** focuses on providing a collection of anomaly
detection algorithms.

If you are interested in our recent publications (see below) on network anomaly detection and want to use them as references, please cite the repository [SADIT](https://github.com/hbhzwj/SADIT)/[GAD](https://github.com/hbhzwj/GAD) together with:

Wang, Jing, et al. "Network anomaly detection: A survey and comparative analysis of stochastic and deterministic methods." Decision and Control (CDC), 2013 IEEE 52nd Annual Conference on. IEEE, 2013.

Jing Wang and I. Ch. Paschalidis, "***Statistical Traffic Anomaly Detection in Time-Varying Communication Networks***", IEEE Transactions on Control of Network Systems, in print.

Jing Wang and I. Ch. Paschalidis,  "***Robust Anomaly Detection in Dynamic Networks***", Proceedings of the 22nd Mediterranean Conference on Control and Automation
  (MED 14), pages 428-433, June 16--19, 2014, Palermo, Italy. 

Jing Zhang and I. Ch. Paschalidis, "***An Improved Composite Hypothesis Test for Markov Models with Applications in Network Anomaly Detection***," Proceedings of the 54th IEEE Conference on Decision and Control, pp. 3810-3815, December 15-18, 2015, Osaka, Japan.

Jing Zhang and I. Ch. Paschalidis, "***Statistical Anomaly Detection via Composite Hypothesis Testing for Markov Models***," IEEE Transactions on Signal Processing, submitted, 2017. [arXiv:1702.08435](https://arxiv.org/abs/1702.08435)


Installation
============

GAD can be installed on Linux, Mac OS X and Windows (through cygwin) with python 2.7. However, we strongly recommend the debian-based OS, e.g., Ubuntu 12.04, 14.04, or 16.04, for which we have prepared a one-command installation script. We recommend using Anaconda2 as the Python environment; conda has a good ability to manage external packages.

To be specific, if you are working on Ubuntu, proceed as follows:

1. Change the working directory to where you want to install GAD, create a new folder `gad`, and then type:

 `$ git clone --recursive https://github.com/hbhzwj/GAD.git gad/`

2. Change the working directory to be `gad/install`, and then type:

 `gad/install$ sudo sh debian.sh` 

3. Make sure `socket.io` and `socketIO-client` be installed as well.

  You may use `$ npm install socket.io` and refer to https://pypi.python.org/pypi/socketIO-client to make `socketIO-client` work on your machine.


If you want to install GAD on other types of OS, you may refer to the following:


### Mac OS X

For mac users, after cloning the GAD package, change the working directory to be `ROOT/install`, and then just type :

    sudo python setup-dep.py

the **ipaddr**, **networkx**, **pydot**, **pyparsing** and **py-radix**
will be automatically downloaded and installed. If you just want to use
the **Detector** part (i.e., **GAD**), that is already enough. (For SADIT users) If you want to use
**Configure** and **Simulator** part, then you also need to install
numpy and matplotlib. Please go to <http://www.scipy.org/NumPy> and
<http://matplotlib.sourceforge.net/faq/installing_faq.html> for
installation instructions.

### Windows
GAD should be able to be installed on windows machine with the help of cgywin. 


### Manually

(For SADIT users) If the automatic methods fail, you can install SADIT manually.

**SADIT** has been tested on python 2.7.2. SADIT depends on all softwares
that [fs-simulator](http://cs-people.bu.edu/eriksson/papers/erikssonInfocom11Flow.pdf) depends on:

> -   ipaddr (2.1.1)
>     [Get](http://ipaddr-py.googlecode.com/files/ipaddr-2.1.1.tar.gz)
> -   networkx (1.0)
>     [Get](http://networkx.lanl.gov/download/networkx/networkx-1.0.1.tar.gz)
> -   pydot (1.0.2)
>     [Get](http://pydot.googlecode.com/files/pydot-1.0.2.tar.gz)
> -   pyparsing (1.5.2)
>     [Get](http://downloads.sourceforge.net/project/pyparsing/pyparsing/pyparsing-1.5.2/pyparsing-1.5.2.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fpyparsing%2Ffiles%2Fpyparsing%2Fpyparsing-1.5.2%2F&ts=1332828745&use_mirror=softlayer)
> -   py-radix (0.5)
>     [Get](http://py-radix.googlecode.com/files/py-radix-0.5.tar.gz)
> -   Cython (0.20)
>     [Get](http://cython.org/release/Cython-0.20.1.tar.gz)

besides: it requires:
:   -   numpy [Get](http://numpy.scipy.org/)
    -   matplotlib [Get](http://matplotlib.sourceforge.net/)
    -   profilehooks [Get](http://mg.pov.lt/profilehooks/)

If you are using debian based system, you can just type:

    sudo apt-get install python-dev
    sudo apt-get install python-numpy
    sudo apt-get install python-matplotlib

For other OS's, please refer to the corresponding website for installation of
**numpy** and **matplotlib**.


Usage
=====
Type `$ ./cmdgad <exper> -m <method> -h` to get help message (see the following).

```
usage: cmdgad [-h] [-c CONFIG] [--logging LOGGING] [-d DATA] [-m METHOD]
              [--help_method HELP_METHOD] [--data_type DATA_TYPE]
              [--feature_option FEATURE_OPTION] [--export_flows EXPORT_FLOWS]
              [--pic_name PIC_NAME] [--pic_show] [--csv CSV]

optional arguments:
  -h, --help            print help message
  -c CONFIG, --config CONFIG
                        config
  --logging LOGGING     logging level. See
                        https://docs.python.org/2/library/logging.html#levels
  -d DATA, --data DATA  --data [filename] will simply detect the flow file,
                        simulator will not run in this case
  -m METHOD, --method METHOD
                        --method [method] will specify the method to use.
                        Avaliable options are: ['gen_fb_mb': FBAnoDetector
                        model free and model based together, will be faster
                        then run model free | 'robust': RobustDetector Robust
                        Detector is designed for dynamic network environment |
                        '2w': TwoWindowAnoDetector Two Window Stochastic
                        Anomaly Detector. | 'speriod': PeriodStaticDetector
                        Reference Empirical Measure is calculated by
                        periodically selection. | 'mb': ModelBaseAnoDetector
                        Model based approach, use Markovian Assumption |
                        'gen_fb_mf': FBAnoDetector model free and model based
                        together, will be faster then run model free |
                        'two_win': TwoWindowAnoDetector Two Window Stochastic
                        Anomaly Detector. | 'mf': ModelFreeAnoDetector Model
                        Free approach, use I.I.D Assumption | 'mfmb':
                        FBAnoDetector model free and model based together,
                        will be faster then run model free | 'period':
                        PeriodStoDetector Stochastic Detector Designed to
                        Detect Anomaly when the]. If you want to compare the
                        results of several methods, simple use / as seperator,
                        for example [gen_fb_mb/robust/2w/speriod/mb/gen_fb_mf/
                        two_win/mf/mfmb/period]
  --help_method HELP_METHOD
                        print the detailed help message for a method.
                        Avaliable method [gen_fb_mb | robust | 2w | speriod |
                        mb | gen_fb_mf | two_win | mf | mfmb | period]
  --data_type DATA_TYPE
                        --specify the type of the data you use, the availiable
                        option are: ['fs': MEM_FS Data generated by `fs-
                        simulator | 'xflow': MEM_Xflow Data generated by xflow
                        tool. | 'pt': PT_Data Pytables format. (HDF5 format).
                        | 'pcap2netflow': MEM_Pcap2netflow Data generated
                        pcap2netflow, (the | 'Sperotto': SperottoIPOM Data
                        File wrapper for SperottoIPOM2009 format. | 'csv':
                        CSVFile | 'flow_exporter': MEM_FlowExporter Data
                        generated FlowExporter. It is a simple tool to convert
                        pcap to]
  --feature_option FEATURE_OPTION
                        specify the feature option. feature option is a
                        dictionary describing the quantization level for each
                        feature. You need at least specify 'cluster' and
                        'dist_to_center'. Note that, the value of 'cluster' is
                        the cluster number. The avaliability of other features
                        depend on the data handler.
  --export_flows EXPORT_FLOWS
                        specify the file name of exported abnormal flows.
                        Default is not export
  --pic_name PIC_NAME   picture name for the detection result
  --pic_show            whether to show the picture after finishing running
  --csv CSV             the path of the file to save plots a text output
----------------------------------------------------------------------
usage: cmdgad [-h] [--interval INTERVAL] [--win_size WIN_SIZE]
              [--win_type WIN_TYPE] [--max_detect_num MAX_DETECT_NUM]
              [--normal_rg NORMAL_RG] [--hoeff_far HOEFF_FAR]
              [--entropy_th ENTROPY_TH] [--enable_sanov] [--lw LW]
              [-r REF_SCHECK] [--days DAYS] [--alpha ALPHA] [--lamb LAMB]
              [--ref_data REF_DATA]

optional arguments:
  -h, --help            show this help message and exit
  --interval INTERVAL   interval between two consequent detection
  --win_size WIN_SIZE   window_size
  --win_type WIN_TYPE   window type 'flow'|'time'
  --max_detect_num MAX_DETECT_NUM
                        max detection number, useful for debug
  --normal_rg NORMAL_RG
                        normal range, when it is none, use the whole data as
                        the norminal data set
  --hoeff_far HOEFF_FAR
                        false alarm rate for hoeffding rule, if this parameter
                        is set while entropy_th parameter is not set, will
                        calculate threshold according to hoeffding rule.
                        Increase hoeff_far will decrease threshold
  --entropy_th ENTROPY_TH
                        entropy threshold to determine the anomaly, has higher
                        priority than hoeff_far
  --enable_sanov        whether or not to use Sanov's theorem to estimate the
                        threshold
  --lw LW               line width of the plot
  -r REF_SCHECK, --ref_scheck REF_SCHECK
                        ['dump <file>', 'load <file>']. whether to load the
                        precomputed reference self check data or calculate and
                        dump it. If <file> is not specfied, its default value
                        is "desc['dump_folder']/PLManager_scheck.pk"
  --days DAYS           number of days the simulated test data lasts;
                        default=7
  --alpha ALPHA         weight of minimum threshold determining the up-bound
                        of nominal cross-entropy; should be within (0, 1),
                        default=0.5
  --lamb LAMB           manual up-bound for nominal cross entropy; only when
                        lamb>0, use its value; has higher priority than alpha
  --ref_data REF_DATA   name for reference file
```

Each **experiment** provides a subcommand that has certain functionality.

We give some sample commands (experiments) as follows:

detect
------
detect the data directly and plot the result.

Examples:

    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mfmb --pic_show --lw 3
    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mb --pic_show --lw 3
    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mfmb --pic_show --hoeff_far 0.9999
    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mb --pic_show --hoeff_far 0.9999
    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mfmb --pic_show --hoeff_far 0.1
    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mfmb --pic_show --hoeff_far 0.001
    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mfmb --pic_show --enable_sanov
    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mf --pic_show --enable_sanov
    $ ./cmdgad detect -c ./example-configs/robust-detect.py -d ./test-data/n0_flow_ref.txt -m robust -r='dump test-data/sc.pk'
    $ ./cmdgad detect -c ./example-configs/robust-detect.py -d ./test-data/n0_flow.txt -m robust -r='load test-data/sc.pk' --pic_show --days 0.2


detectrealtime
--------------
detect the data and send data to web interface to visualize in
real-time. It requires support of `node js`; for `node js` installation, refer to http://nodejs.org/.


Examples:

First, cd to `gad-ui/` folder, run the following command: 

  `$ python -m SimpleHTTPServer` or `$ python3 -m http.server` (provided that you have installed python3)

Either will start a webserver. You will get responses similar to:

```
jzh@jzh:~/Research/Anomaly_Detection/gad/gad-ui$ python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
127.0.0.1 - - [22/Oct/2014 10:53:36] "GET /dashboard.html HTTP/1.1" 200 -
127.0.0.1 - - [22/Oct/2014 10:53:36] "GET /node_modules/socket.io/node_modules/socket.io-client/dist/socket.io.min.js HTTP/1.1" 200 -
127.0.0.1 - - [22/Oct/2014 10:53:36] "GET /frameworks/jquery-1.10.2.min.js HTTP/1.1" 200 -
127.0.0.1 - - [22/Oct/2014 10:53:36] "GET /frameworks/d3.v3.min.js HTTP/1.1" 200 -
127.0.0.1 - - [22/Oct/2014 10:53:36] "GET /js/dash.js HTTP/1.1" 200 -
127.0.0.1 - - [22/Oct/2014 10:53:39] "GET /dashboard.html HTTP/1.1" 200 -
......
```


Then, open a web browser, go to the following website:

         http://localhost:8000/dashboard.html


You will see a chart. 

Next, open another command window, cd to the `gad-ui/` folder, and run the following command: 

         node server.js 


You will get responses similar to:
```
jzh@jzh:~/Research/Anomaly_Detection/gad/gad-ui$ node server.js 
   info  - socket.io started
   debug - client authorized
   info  - handshake authorized TcnFyzPltVRfrAQCVUAK
   debug - setting request GET /socket.io/1/websocket/TcnFyzPltVRfrAQCVUAK
   debug - set heartbeat interval for client TcnFyzPltVRfrAQCVUAK
   debug - client authorized for 
   debug - websocket writing 1::
......
```


After finishing all these prerequisites, run the following command in `gad/` folder


         ./cmdgad detectrealtime -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mfmb --srv=127.0.0.1:3000


The realtime detection results will show up in the webpage above. 


detectcompare
-------------
run several methods on a dataset and save the results for future
 comparison.

Examples:

    $ ./cmdgad detect -c ./example-configs/robust-detect.py -d ./test-data/n0_flow.txt -m robust -r='dump test-data/sc.pk' --lamb=0.2
    $ ./cmdgad detectcompare -c ./example-configs/compare-detect.py -d ./test-data/n0_flow.txt -p mfmb,robust 


eval
----
calculate the ROC curve of a method.

Examples:

CD to `gad`, run the following two commands sequentially:

    $ ./cmdgad eval -c example-configs/eval-config.py --res_folder=res/ --ab_flows_data test-data/test_ab_flow.txt
    $ ./cmdgad eval -c example-configs/eval-config.py --res_folder=res/ --ab_flows_data test-data/test_ab_flow.txt --plot


Code Structure
============

All the detection algorithms locate
in the *ROOT/gad/Detector* folder:

 -   **SVMDetector.py** contains two SVM based anomaly detection
     algorithmes: 1. SVM Temporal Detector and 2. SVM Flow by Flow Detector.
 -   **StoDetector.py** contains two anomaly detection algorithms based
     on Large Deviation Theory.
 -   **RobustDetect.py** contains a algorithm that works robustly under
     dynamic network environment.

Want to Use Other Flow Records?
==============================


GAD does not only support the text output format of [fs-simulator](http://cs-people.bu.edu/eriksson/papers/erikssonInfocom11Flow.pdf) (see also https://github.com/hbhzwj/SADIT for details), but
also several other types of flow data. The data wrapper classes are defined in `ROOT.gad.Detector.Data` module and the handler classes locate in the `ROOT.gad.Detector.DataHandler` module.


In order to use data in a new format, you need to implement two new classes: 


First, a data class that satisfies Data interface (`Data.py`, Line 9). Namely, such a class has to at least provide the following three functions:
* `get_rows`: row slicing
* `get_where`: get range of rows that satisfies a criterion. 
* `get_min_max`: get min and max values of a certain feature at a certain range. 

The package has included several data classes, which all locates in `Data.py`. In some cases, you can re-use existing classes.

* `MEM_DiskFile`: base class for disk file data. 
* `MEM_FS`: disk file generated by [fs-simulator](http://cs-people.bu.edu/eriksson/papers/erikssonInfocom11Flow.pdf).
* `MEM_FlowExport`: disk file generated by FlowExport tool
* `MySQLDatabase`: base class for data in disk file. 


Second, a data handler class that implements data preprocessing, e.g., quantization.


* `QuantizeDataHandler`: will quantize the input data.
* `IPHanlder`: for logs with IP addresses. It will first cluster IPs and replace IPV4 with `(cluster label, dist to cluster center)` pair.


Then you just need to add your `data_handler` to
`data_handler_handle_map` defined in `ROOT/gad/Detector/API.py`



Licensing
=============
Please see the `LICENSE` file.

Authors
=============
Jing (Conan) Wang

Jing Wang obtained his Ph.D. degree in Fall 2014 from Division of Systems Engineering, 
Boston University (advised by Professor [Yannis Paschalidis](http://sites.bu.edu/paschalidis/)).  His main interest is 
Mathematical Modeling, i.e., constructing mathematical models for the real world and 
trying to solve practical problems.

Email: `wangjing@bu.edu`

Personal Webpage: https://wangjingpage.wordpress.com/


Jing Zhang

Jing Zhang currently is a PhD student in Division of Systems Engineering, Boston University 
(advised by Professor [Yannis Paschalidis](http://sites.bu.edu/paschalidis/)). 

Email: `jzh@bu.edu`

Personal Webpage: http://people.bu.edu/jzh/


*Last updated on 10/24/2016 (By Jing Z.)*
