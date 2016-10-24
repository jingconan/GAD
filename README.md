Introduction
============
**GAD** is the acronym of General Anomaly Detector. It was
once part of **[SADIT](https://github.com/hbhzwj/SADIT)**. We can now use the two packages either jointly or separately. Here are their main differences:

1. **SADIT** focuses on providing  an integrated interface for generating
test data and evaluating algorithms.

2. **GAD** focuses on providing a collection of anomaly
detection algorithms.

If you are interested in our recent publications (see below) on network anomaly detection and want to use them as references, please cite the repository [SADIT](https://github.com/hbhzwj/SADIT)/[GAD](https://github.com/hbhzwj/GAD) together with:


Jing Wang and I. Ch. Paschalidis, "***Statistical Traffic Anomaly Detection in Time-Varying Communication Networks***", IEEE Transactions on Control of Network Systems, in print.

Jing Wang and I. Ch. Paschalidis,  "***Robust Anomaly Detection in Dynamic Networks***", Proceedings of the 22nd Mediterranean Conference on Control and Automation
  (MED 14), pages 428-433, June 16--19, 2014, Palermo, Italy. 

Also, recently we have obtained a result accurately approximating the threshold needed by the generalized Hoeffding test (with Markovian assumption corresponding to the model-based method in the package). 
You are welcome to test the 'mb', 'mfmb', or 'robust' method; any feedback is highly appreciated. The complete theoretical result will come out soon. You are also welcome to test our algorithm by using the 
repo [TAHTMA](https://github.com/jingzbu/TAHTMA). By the way, the i.i.d. case has been solved recently by other researchers 
(cf. [J. Unnikrishnan and D. Huang](http://lcav.epfl.ch/files/content/sites/lcav/files/people/jayakrishnan.unnikrishnan/TIT13submitted.pdf)), and we also provide a repo [TAHTIID](https://github.com/jingzbu/TAHTIID)
for interested readers to test the performance of their method.  

Especially, you are welcome to visit the page [log-normal-sample](https://www.dropbox.com/sh/ce12g4epj5qf250/AABLoBx8KfQJvijQz_R2kEAea?dl=0) to test 'robust' method with our threshold approximation. If you have
any question, please feel free to contact us.

Installation
============

GAD can be installed on Linux, Mac OS X and Windows (through cygwin) with python 2.7. However, we strongly recommend the debian-based OS, e.g., Ubuntu 12.04, 14.04, or 16.04, for which we have prepared a one-command installation script. We recommend using Anaconda2 as the Python environment; conda has a good ability to manage external packages.

To be specific, if you are working on Ubuntu, do the following sequentially:

1. Change the working directory to where you want to install GAD, create a new folder `gad`, and then type:

 `$ git clone https://github.com/hbhzwj/GAD.git gad/`

2. Change the working directory to `gad`, and then type:

 `gad$ git clone https://github.com/hbhzwj/gad-ui.git gad-ui/`

3. Change the working directory to be `gad/install`, and then type:

 `gad/install$ sudo sh debian.sh` 

4. Make sure `socket.io` and `socketIO-client` be installed as well.

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
Please type `$ ./cmdgad -h`
 to get general help message (see the following).

```
usage: cmdgad [--profile PROFILE] [-h] [experiment]

gad

positional arguments:
  experiment         type ./cmdgad <exper> -h for help of an experiment;
                     available experiments are [detect | detectbatch |
                     detectcompare | detectrealtime | eval |
                     multisrvexperiment]

optional arguments:
  --profile PROFILE  profile the program
  -h, --help         print help message and exit
```

Each **experiment** provides a subcommand that has certain functionality.

We give some sample commands (experiments) as follows:

detect
------
detect the data directly and plot the result.

Examples:

    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mfmb --pic_show --lw 5
    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mf --pic_show --lw 3
    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mfmb --pic_show --enable_sanov
    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mf --pic_show --enable_sanov
    $ ./cmdgad detect -c ./example-configs/robust-detect.py -d ./test-data/n0_flow_ref.txt -m robust -r='dump test-data/sc.pk'
    $ ./cmdgad detect -c ./example-configs/robust-detect.py -d ./test-data/n0_flow.txt -m robust -r='load test-data/sc.pk' --pic_show


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
Boston University (advised by Professor [Yannis Paschalidis](http://ionia.bu.edu/)).  His main interest is 
Mathematical Modeling, i.e., constructing mathematical models for the real world and 
trying to solve practical problems.

Email: `wangjing@bu.edu`

Personal Webpage: https://wangjingpage.wordpress.com/


Jing Zhang

Jing Zhang currently is a PhD student in Division of Systems Engineering, Boston University 
(advised by Professor [Yannis Paschalidis](http://ionia.bu.edu/)). 

Email: `jzh@bu.edu`

Personal Webpage: http://people.bu.edu/jzh/


*Last updated on 10/23/2016 (By Jing Z.)*
