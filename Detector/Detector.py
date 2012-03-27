#!/usr/bin/env python
### -- Created at [2012-03-01 14:55:21]
### -- [2012-03-01 17:13:27] support multi feature
### -- [2012-03-01 22:05:29] GetFlowRate, test with flowSize, dur, flowRate

from OldDetector import *

from matplotlib.pyplot import *
def Compare(fName, dataName= ''):
    '''This is just a wrap-up of Detecotor function. Load some parameters and detect.

    - fName is the name of the flow file generated by fs-simulator.
    - if data Name is not empty, the output data(*time, model-free indicator and model based indicator*)
    will be stored in data file, otherwise the result will be plotted.

    '''
    IF2, IB2, t2, threshold = Detect(fName,
            settings.DISCRETE_LEVEL + [settings.CLUSTER_NUMBER],
            settings.DETECTOR_WINDOW_SIZE)

    if dataName != '':
        import cPickle as pickle
        # data = t2, IF2, IB2 #FIXME ATTENTION the order
        data = t2, IF2, IB2, threshold
        pickle.dump( data, open(dataName, 'w') )
    else:
        figure()
        subplot(211)
        plot(t2, IF2)
        subplot(212)
        plot(t2, IB2)
        savefig(settings.ROOT + '/res/entropy.eps')
        # show()

import operator
def FHash(digit, level):
    '''This is just a hash function. to map a sequence to a unique number.
    The implemetation is: return digit[0] + digit[1] * level[0] + digit[2] * level[1] * level[0] ...
    '''
    # return digit[0] + digit[1] * level[0] + digit[2] * level[1] * level[0]
    value = digit[0]
    for i in xrange(len(digit)-1):
        value += digit[i+1] * reduce(operator.mul, level[0:i+1])
    return value

def GetFeatureHashList(F, Q):
    '''For each list of feature and corresponding quantized level.
    Get the hash value correspondingly'''
    return [ FHash(f, Q) for f in zip(*F) ]

def ModelBased(qFeaVec, feaQN):
    '''estimate the transition probability. It has same input parameter with ModelFree.

    - qFeaVec :qFeaVec is a list of list containing all the quantized feature in a window. len(qFeaVec)
               equals to the number of feature types. len(qFeaVec[0]) equals to the number of flows in this
               window.
    - feaQN : this is a list storing the quantized number for each feature.
    '''
    QLevelNum = reduce(operator.mul, feaQN)
    P = np.zeros( (QLevelNum, QLevelNum) )
    fl = len(qFeaVec[0])
    mp = np.zeros((QLevelNum, ))
    m_list = GetFeatureHashList(qFeaVec, feaQN)

    for i in xrange(fl-1):
        mp[m_list[i]] += 1
        P[m_list[i], m_list[i+1]] += 1
    mp[m_list[fl-1]] += 1

    P = P * 1.0 / (fl-1)
    mp = mp / fl
    return P, mp

def ModelFree(qFeaVec, feaQN):
    '''estimate the probability distribution for model free case. It has same input parameters with ModelBased

    - qFeaVec :qFeaVec is a list of list containing all the quantized feature in a window. len(qFeaVec)
               equals to the number of feature types. len(qFeaVec[0]) equals to the number of flows in this
               window.
    - feaQN : this is a list storing the quantized number for each feature.
    '''
    QLevelNum = reduce(operator.mul, feaQN)
    P = np.zeros( (QLevelNum, ) )
    fl = len(qFeaVec[0])
    m_list = GetFeatureHashList(qFeaVec, feaQN)

    for i in range(fl):
        idx = m_list[i]
        try:
            P[idx] += 1
        except:
            import pdb; pdb.set_trace()
    P = P * 1.0 / fl
    assert(abs( np.sum(np.sum(P, 0)) - 1.0) < 0.01)
    return P


def VectorQuantizeState(feaVec , feaQN, feaRange, quanFlag=None):
    '''Quantize a vector of numbers.

    - feaVec : is a list of list containing all the features in a window. len(feaVec)
               equals to the number of feature types. len(feaVec[0]) equals to the number of flows in this
               window.
    - feaQN : quantized number for each feature. len(feaQn) equals to the number of feature types.
    - feaRange : a list of two-digit tupe containing the range for each user. the
                 length for first diemension equals to the number of feature types.
                 the length of the second dimension is two.

    '''
    if not quanFlag: quanFlag = len(data) * [1]
    QS = lambda a, b, c, flag: QuantizeState(a, b, c)[1] if flag else a
    return [ QS(a, b, c, flag) for a, b, c, flag in zip(feaVec , feaQN, feaRange, quanFlag) ]

def GetAllPMF(feaVec, feaQN, feaRange,  quanFlag=None):
    '''This Function Support Multiple Features, get probability mass function

    - feaVec : is a list of list containing all the features in a window. len(feaVec)
               equals to the number of feature types. len(feaVec[0]) equals to the number of flows in this
               window.
    - feaQN : quantized number for each feature. len(feaQn) equals to the number of feature types.
    - feaRange : a list of two-digit tupe containing the range for each user. the
                 length for first diemension equals to the number of feature types.
                 the length of the second dimension is two.

    '''
    qFeaVec = VectorQuantizeState(feaVec, feaQN, feaRange, quanFlag)
    pmf = ModelFree(qFeaVec, feaQN)
    Pmb, mpmb = ModelBased(qFeaVec, feaQN)
    return pmf, Pmb, mpmb

def GetFlowRate(t, cluster):
    '''Get Estimation of Flow Rate For Each User input:

    - **t** : arrival time
    - **cluster** : cluster labels flows

    output is Estimated flow arrival rate for each time
    '''
    win = settings.FLOW_RATE_ESTIMATE_WINDOW
    fr = []
    for i in xrange(len(t)):
        idx = Find(t, t[i] - win)
        if idx == -1: idx = 0
        c = cluster[i]
        fr.append( cluster[idx:i].count(c) )

    return fr


def GetFeature(fName, clusterNum, cutHead=True):
    '''Get feature by parsing the data file.

    - fName : is the name for the flow file generated by fs-simulator
    - clusterNum : the number of cluster in K-means clustering.
    - cutHead : if we use estimated value of flow rate. The beginning part of
                the estimation will be not accurate. cutHead flag indicates
                whether we need to delete beginning part of the data or not.

    '''
    flow = ParseData(fName);
    srcIPVec, flowSize, t, dur = TransData(flow)

    cluster, centerPt = KMeans(srcIPVec, clusterNum, DF)
    distToCenter = GetDistToCenter(srcIPVec, cluster, centerPt, DF)
    flowRate = GetFlowRate(t, cluster)

    if cutHead:
        ns = Find(t, min(t) + settings.FLOW_RATE_ESTIMATE_WINDOW)
        srcIPVec = srcIPVec[ns:]
        flowSize = flowSize[ns:]
        t = t[ns:]
        dur = dur[ns:]
        flowRate = flowRate[ns:]

    exec settings.LOAD_FEATURE

    quanFlag = ( len(feaVec) - 1 ) * [1] + [0]
    feaRange = GetRange(feaVec)
    return feaVec, feaRange, quanFlag, t, centerPt

# def GenNominalPDF(fName, clusterNum, ND, NF, dumpFlag =False):
def GenNominalPDF(fName, feaQN, dumpFlag =False):
    '''This function is to generate the nominal probability densition function for
    both model free and model free case.

    - fName : is the name for the flow file generated by fs-simulator
    - feaQN : quantized number for each feature. len(feaQn) equals to the number of feature types.
    - dumpFlag : indicate whether dump the generated nominal pdf to a data file.

    '''

    '''Generate the nominal probability mass function'''
    feaVec, feaRange, quanFlag, t, centerPt = GetFeature(fName, feaQN[-1])

    # ns = 0 # normal start
    ns = Find(t, min(t) + settings.FLOW_RATE_ESTIMATE_WINDOW)
    ne = Find(t, min(t) + settings.ANOMALY_TIME[0] - 10) + 1
    n_feaVec = SL(feaVec, ns, ne)

    pmf, Pmb, mpmb = GetAllPMF(n_feaVec, feaQN, feaRange,  quanFlag)

    data = pmf, Pmb, mpmb, feaRange
    if dumpFlag:
        pickle.dump( data, open(NominalPDFFile, 'w') )
    return pmf, Pmb, mpmb, feaVec, feaQN, feaRange,  quanFlag, t, centerPt

def SL(data, st, ed):
    return [d[st:ed] for d in data]

def GetRange(data):
    return [ (min(x), max(x)) for x in data ]

def Detect(fName, feaQN, wSize):
    '''
    feaVec is a list contains all features, len(feaVec) equals to the number of features
    feaRange is a list, each element in the list is a tuple contains the range
    in current version, feature includes:
        1. cluster --> don't need to quantize
        2. distance to cluster center --> quantize
        3. flow size --> quantize
        4. estimate of flow rate --> quantize
    feaVec    |--> qFeaVec --> GenPDF
    feaRange  |
    '''
    ### Generate Nominal PDF ###
    if settings.UNIFIED_NOMINAL_PDF:
        pmf, Pmb, mpmb, feaRange = pickle.load(open(NominalPDFFile, 'r'))
        feaVec, feaRange, quanFlag, t, centerPt = GetFeature(fName)
    else:
        pmf, Pmb, mpmb, feaVec, feaQN, feaRange,  quanFlag, t, centerPt = GenNominalPDF(fName, feaQN)

    # print 'feaRange, ', feaRange
    # import pdb;pdb.set_trace()

    pickle.dump((feaRange, centerPt), open(settings.ANO_ANA_DATA_FILE, 'w'))
    # print 'nominal model free pmf, ', pmf
    # print 'nominal model based Pmb, ', Pmb
    # print 'nominal model based mpmb, ', mpmb


    IF, IB, winT = [], [], []
    threshold = []

    lp = 0 # last Position
    idx = 0 # current position
    ti = settings.DETECTOR_INTERVAL
    # time = 0
    minT = min(t)
    time = minT + settings.FLOW_RATE_ESTIMATE_WINDOW
    sIdx = Find(t, minT + settings.FLOW_RATE_ESTIMATE_WINDOW)
    detectNum = ( ( len(flow) - sIdx ) / dInter - 1 - sIdx ) if (settings.WINDOW_TYPE == 'FLOW') else int((max(t)-wSize - time )/ti)
    print 'detectNum, ', detectNum

    CleanGlobalDeri()
    for i in range(detectNum):
        # Find Data
        if settings.WINDOW_TYPE == 'FLOW':
            lp = idx + 1
            idx += wSize
            time = t[lp]
        elif settings.WINDOW_TYPE == 'TIME':
            time += ti
            lp = Find(t, time)
            idx = Find(t, time+wSize)
        else:
            raise ValueError('unknow window type')

        print 'time: %f' %(time - minT)
        d_feaVec = SL(feaVec, lp, idx+1)

        # Update Hoeffding test threshold
        threshold.append( idx-lp+1 ) #FIXME it is not real threshold

        d_pmf, d_Pmb, d_mpmb = GetAllPMF(d_feaVec, feaQN, feaRange,  quanFlag)


        mfEntro = I1(d_pmf, pmf)
        mbEntro = I2(d_Pmb, d_mpmb, Pmb, mpmb)
        IF.append(mfEntro)
        IB.append(mbEntro)
        winT.append(time)

        # Identify the Most significant state transition for model-base case
        modelFreeDeri= ModelFreeDerivative(d_pmf, pmf)
        modelBaseDeri = ModelBaseDerivative(d_Pmb, d_mpmb, Pmb, mpmb)
        # util.Dump2Txt(deri, './deri.res', '2dnp')

    DumpDerivative()
    if settings.PLOT_DERIVATIVE:
        PlotModelBase()
        PlotModelFree()

    return IF, IB, winT, threshold


if __name__ == "__main__":
    import sys,os
    os.system('cp ../settings_template.py ../settings.py')
    Compare(sys.argv[1], sys.argv[2])
