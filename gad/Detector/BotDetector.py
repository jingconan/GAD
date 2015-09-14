#!/usr/bin/env python
""" Community Detection Related Functions
"""
from __future__ import print_function, division, absolute_import
from subprocess import check_call
import logging
import numpy as np
import scipy as sp
import sys

from .Correlation import TrafficCorrelationAnalyzer


# def com_det(A, r_vec, w, lamb, out):
#     """ Community Detection using Revised Modularity Maximization Method

#     Is defined as:
#         (0.5 / m) A - (0.5 / m^2) deg * deg' + w * r_rec r_rec' - lamb * I

#     **deg** is the degree sequence of each node.
#     **m** is the edge number of the graph

#     Parameters
#     ---------------
#     A : symmetric matrix.
#         Adjcant matrix of correlation graph
#     r_vec : list
#         interaction of each node with pivot nodes

#     Returns
#     --------------
#     None
#     """
#     n = A.shape[0]
#     deg = np.sum(A, axis=1).reshape(-1)
#     mc = 0.5 * np.sum(deg)
#     M = A / (2.0 * mc) - np.outer(deg, deg) / ((2.0 * mc) ** 2)
#     M += w * np.outer(r_vec, r_vec) - lamb * np.eye(n)
#     return max_cut(M, out)


def com_det_reg(A, r_vec, w1, w2, lamb, out):
    """ Modularity-based community detection with regularizatoin term

    The problem is defined as:
        M = (0.5 / m) A - (0.5 / m^2) deg * deg'
        max s' (M - lamb I ) s + (w1 r - w2 / 2)' s
        s.t.
            s_i^2 = 1

    **deg** is the degree sequence of each node.
    **m** is the edge number of the graph

    Parameters
    ---------------
    A : symmetric matrix.
        Adjcant matrix of correlation graph
    r_vec : list
        interaction of each node with pivot nodes

    Returns
    --------------
    P0 : M - lamb I
    q0 : w1 r - 0.5 w2 1
    W :
        | P0,     0.5 q0 |
        | 0.5 q0, 0      |
    """
    n = A.shape[0]
    deg = np.sum(A, axis=1).reshape(-1)
    mc = 0.5 * np.sum(deg)
    M = A / (2.0 * mc) - np.outer(deg, deg) / ((2.0 * mc) ** 2)
    # M = A / (2.0 * mc)
    P0 = M - lamb * np.eye(n)
    q0 = w1 * r_vec - 0.5 * w2 * np.ones((n,))
    qv = q0.reshape(-1, 1)
    zerov = np.array([[0]])
    W = np.vstack([np.hstack([P0, 0.5 * qv]),
                  np.hstack([0.5 * qv.T, zerov])])
    export_max_cut(W, out)
    return P0, q0, W


def export_max_cut(W, out):
    """  Export the max_cut problem to **out**

    The max cut problem is:

        max Tr(XW)
        s.t.
            X >= 0
            X_{ii} = 1

    Parameters
    ---------------
    W : nxn matrix
        Weight matrix

    out : str or file handler
        specify the output file

    Returns
    --------------
    None

    """
    n = W.shape[0]
    F = [W]
    for i in xrange(n):
        dv = np.zeros((n,))
        dv[i] = 1
        F.append(np.diag(dv))
    c = np.ones((n,))
    if isinstance(out, str):
        with open(out, 'w') as fid:
            SDPA_writer(c, F, fid)
    else:
        SDPA_writer(c, F, out)


def SDPA_writer(c, F, out=sys.stdout):
    """ Write Problem to SDPA format. Can also be used by CSDP

    See Also
    --------------
    We work with a semidefinite programming problem that has been written

    (D)    max tr(F0*Y)
           st  tr(Fi*Y)=ci           i=1,2,...,m
                     Y >= 0

    http://plato.asu.edu/ftp/sdpa_format.txt
    """
    m = len(F) - 1
    n = F[0].shape[0]
    print('%d =mdim' % (m), file=out)
    print('%d =nblocks' % (1), file=out)
    print('%d %d' % (n, n), file=out)
    print(' '.join([str(cv)for cv in c]), file=out)
    for k, f_mat in enumerate(F):
        I, J = np.triu(f_mat).nonzero()
        for i, j in zip(I, J):
            print('%d %d %d %d %f' % (k, 1, i+1, j+1, f_mat[i, j]), file=out)


def parse_CSDP_sol(f_name, n):
    """  parse CSDP solution

    Parameters
    ---------------
    f_name : str
        path of the csdp output
    n : int
        number of nodes

    Returns
    --------------
    Z :
    X : FIXME
    """
    data = np.loadtxt(f_name, skiprows=1)
    assert(np.max(data[:, 1]) == 1)
    zr, = np.where(data[:, 0] == 1)
    Z = sp.sparse.coo_matrix((data[zr, 4], (data[zr, 2]-1, data[zr, 3]-1)),
                             shape=(n, n))

    xr, = np.where(data[:, 0] == 2)
    X = sp.sparse.coo_matrix((data[xr, 4], (data[xr, 2]-1, data[xr, 3]-1)),
                             shape=(n, n))
    return Z, X


def parse_SDPA_sol(f_name, n):
    pass
    # return Y


# def randomization_old(S, W):
#     n = S.shape[0]
#     sn = 5000
#     sample = np.random.multivariate_normal(np.zeros((n,)), S.todense(),
#     (sn,))
#     val = np.zeros((sn,))
#     for i in xrange(sn):
#         fea_sol = np.sign(sample[i, :])
#         val[i] = np.dot(np.dot(fea_sol.T, W), fea_sol)
#     best_one = np.argmax(val)
#     print('the best sampled solution is :', val[best_one])
#     return np.sign(sample[best_one, :])


def randomization(S, P0, q0, sn=5000):
    """ Randomization and search a good feasible solution

    Parameters
    ---------------
    S : (n+1)x(n+1) matrix
        solution of the following relaxed problem:

        max Tr(X P0) + q0' s
        s.t
            [ X,   x]  >= 0
            [ x',  1]
            X_ii = 1

        S = [ X,   sx ]
            [ sx', 1 ]

    P0:
        M - lamb I
    q0:
        w1 r - 0.5 * w2 1


    Returns
    --------------
    sol : n-dimentional vector
        feasible solution
    """
    S = np.array(S.todense())
    X = S[:-1, :-1]
    sx = S[-1, :-1]
    covar = X - np.outer(sx, sx)
    n = X.shape[0]
    # sample = np.random.multivariate_normal(np.zeros((n,)), covar, (sn,))
    sample = np.random.multivariate_normal(sx, covar, (sn,))
    val = np.zeros((sn,))
    for i in xrange(sn):
        fea_sol = np.sign(sample[i, :])
        val[i] = np.dot(np.dot(fea_sol.T, P0), fea_sol) + np.dot(q0, fea_sol)
    best_one = np.argmax(val)
    print('the best sampled solution is :', val[best_one])
    return np.sign(sample[best_one, :])


from .Base import BaseDetector

class BotDetector(BaseDetector):
    def __init__(self, desc):
        self.desc = desc
        self.anomaly_detector = desc['anomaly_detector']

    def init_parser(self, parser):
        super(BotDetector, self).init_parser(parser)
        self.anomaly_detector.init_parser(parser)
        pass

    def detect(self, data_file, anomaly_detect=True):
        threshold = self.desc['threshold']
        if anomaly_detect:
            self.data_file = data_file
            self.anomaly_detector.desc.update(self.desc)
            self.anomaly_detector.detect(data_file)

        self.data_file = self.anomaly_detector.data_file
        divs = self.anomaly_detector.record_data['entropy']
        if len(divs) == 0:
            logging.warning('There is less than one window!')
            return
        divs = np.array(divs, dtype=float) / np.max(divs)
        detect_result = divs > threshold
        winT = self.anomaly_detector.record_data['winT']
        return self.get_ips(winT, detect_result)

    def get_ips(self, window_times, detect_result):
        pass

class SoBotDet(BotDetector):
    def get_ips(self, window_times, detect_result):
        import pandas
        ip_col_names = self.desc['ip_col_names']
        win_size = self.desc['win_size']
        win_type = self.desc['win_type']
        config = self.desc['botnet_detection_config']
        pivot_node_threshold = config['pivot_node_threshold']
        correlation_graph_threshold = config['correlation_graph_threshold']
        w1 = config['w1']
        w2 = config['w2']
        lamb = config['lambda']
        sdpb_filepath = config.get('sdpb_filepath', './prob.sdpb')
        solution_filepath = config.get('solution_filepath', './botnet.sol')
        csdp_binary = config.get('csdp_binary', 'csdp')


        start_times = [w for w, d in zip(window_times, detect_result) if d]
        end_times = [t + win_size for t in start_times]
        abnormal_windows = pandas.DataFrame({
            'start_time': start_times,
            'end_time': end_times,
        })

        data = self.anomaly_detector.data_file.data
        analyzer = TrafficCorrelationAnalyzer(data,
                                              ip_col_names[0],
                                              ip_col_names[1],
                                              abnormal_windows)
        features = analyzer.create_features(pivot_node_threshold)
        all_ips = list(analyzer.node_set)

        total_interact_measure = features.sum(axis=0)
        graph = analyzer.generate_correlation_graph(features,
                                                    correlation_graph_threshold)
        P0, q0, W = com_det_reg(graph, total_interact_measure, w1, w2, lamb,
                                out=sdpb_filepath)
        check_call([csdp_binary, sdpb_filepath, solution_filepath])

        node_num = len(total_interact_measure)
        Z, X = parse_CSDP_sol(solution_filepath, node_num + 1)
        solution = randomization(X, P0, q0)
        inta_diff = np.dot(total_interact_measure, solution)
        print('inta_diff', inta_diff)

        #  botnet, = np.nonzero(solution > 0)
        bot_ips = [n for n, d in zip(all_ips, solution) if d > 0]
        return {
            'detected_bot_ips': bot_ips,
            'all_ips': all_ips,
            'interact_measure_diff': inta_diff,
            'correlation_graph': graph,
        }
