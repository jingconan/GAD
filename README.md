Introduction
============
**GAD** is the acronym of **G**eneral **A**nomaly **D**etector. It was
once part of **SADIT**. They are splitted into two packages to solve
different issues:

1. **SADIT** focuses on providing  an integrated interface for generating
test data and evaluating algorithms.

2. **GAD** focuses on providing an collection of anomaly
detection algorithms.

Usage
=====
Please type 
    $./cmdgad -h
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
Avaliable subcommnd (experiments) are as follows:

detect
------
detect the data directly and plot the result as figure.

Examples:

    $ ./cmdgad detect -c ./example-configs/detect-config.py -d ./test-data/n0_flow.txt -m mfmb --pic_show
    $ ./cmdgad detect -c ./example-configs/robust-detect.py -d ./test-data/n0_flow.txt -m robust -r='dump test-data/sc.pk' --lamb=0.2
    $ ./cmdgad detect -c ./example-configs/robust-detect.py -d ./test-data/n0_flow.txt -m robust -r='load test-data/sc.pk' --lamb=0.2 --pic_show


detectcompare
-------------
run several methods on a dataset and save the results for furture
comparison.

Examples:

    $ ./cmdgad detect -c ./example-configs/robust-detect.py -d ./test-data/n0_flow.txt -m robust -r='dump test-data/sc.pk' --lamb=0.2
    $ ./cmdgad detectcompare -c ./example-configs/compare-detect.py -d ./test-data/n0_flow.txt -p mfmb,robust 
    $ ./cmdgad detectcompare -c ./example-configs/compare-detect.py -d ./test-data/n0_flow.txt -p mfmb,robust --plot_dump --pic_show


Installation
============

GAD can be installed in Linux, Mac OS X and Windows(through cygwin)
with python 2.7

### Debain (Ubuntu, Mint, etc)

If you are using debain based system like Ubuntu, Mint, you are lucky.
There is an installation script prepared for debain based system, just
type :

    sh debain.sh

### Mac OS X

For mac user, just type :

    sudo python setup-dep.py

the **ipaddr**, **networkx**, **pydot**, **pyparsing** and **py-radix**
will be automatically downloaded and installed. If you just want to use
the **Detector** part, that is already enough If you want to use
**Configure** and **Simulator** part, then you also need to install
numpy and matplotlib. Please go to <http://www.scipy.org/NumPy> and
<http://matplotlib.sourceforge.net/faq/installing_faq.html> for
installation instruction.

### Windows
GAD should be able to be installed on windows machine with the help of cgywin. 


### Manually

If the automatical methods fail, you can try to install manually.
**SADIT** has been tested on python2.7.2. SADIT depends on all softwares
that fs-simulate depends on:

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

if you are in debain based system. you can simple use :

    sudo apt-get install python-dev
    sudo apt-get install python-numpy
    sudo apt-get install python-matplotlib

in other system, refer to corresponding website for installation of
**numpy** and **matplotlib**


Code Structure
============

All the detection algorithms locates
in the *ROOT/Detector* folder:

 -   **SVMDetector.py** contains two SVM based anomaly detection
     algorithmes: 1. SVM Temporal Detector and 2. SVM Flow by Flow Detector.
 -   **StoDetector.py** contains two anomaly detection algorithms based
     on Large Deviation Theory.
 -   **RobustDetect.py** contains a algorithm that works robustly under
     dynamic network environment.


Licensing
=============
Please see the file called LICENSE.

Authors
=============
Jing Conan Wang

    Jing Wang is a Ph.D. Student in Division of Systems Engineering, Boston
    University advised by Professor Yannis Paschalidis.  His main interests is
    Mathematica Modeling, i.e., contructing mathematical models for the real
    word and try to solve practical problems.

    **EMAIL:** wangjing AT bu.edu
    **Personal Webpage:** http://people.bu.edu/wangjing/
