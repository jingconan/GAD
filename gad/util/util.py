# from random import randint
from __future__ import print_function, division, absolute_import

### -- [2012-03-26 14:01:02] add docstring for each function.

def IN(*val_list):
    """Generate a string command that import object variables
    to locals() in the class methods"""
    return ";".join(['%s=self.%s'%(v, v) for v in val_list])

def OUT(*val_list):
    """Generate a string command that export object variables
    to locals() in the class methods"""
    return ";".join(['self.%s=%s'%(v, v) for v in val_list])


import types
def Load(var):
    '''Load is useful when the some elements in var is specified as random value.
    for example, if the var is ['rand(1)', 1], var[0] will be different random
    value at each time.'''
    t = type(var)
    if t == types.TupleType or t == types.ListType:
        return [Load(x) for x in var]
    elif t == types.DictType:
        res = dict()
        for k, v in var.iteritems():
            # If cannot properly loaded, use origianl value
            try:
                res[k] = Load(v)
            except Exception:
                res[k] = v
        return res
    elif t == types.StringType:
        return eval(var)
    elif t == types.FloatType or t == types.IntType:
        return var
    else:
        raise TypeError('unknown type of var')

def Dump2Txt(var, fname, op):
    """Dump2Txt will dump the variable to text file for use of other programs like Matlab.

    - *fname* : is the name for output file
    - *op* : is a option flag, ::

        if op[0:2] == '1d':
            m = len(var)
            for i in xrange(m): fid.write("%f "%(var[i]))
            fid.write('\\n')
        elif op[0:2] == '2d':
            if op[2:] == 'np': m, n = var.shape
            elif op[2:] == 'list':
                m = len(val)
                m = len(val[0])
            else:
                raise ValueError('unknown op')

            for i in xrange(m):
                for j in xrange(n):
                    fid.write("%s "%(var[i,j]))
                fid.write("\\n")


    """
    fid = open(fname, 'w')
    if op[0:2] == '1d':
        m = len(var)
        for i in xrange(m): fid.write("%f "%(var[i]))
        fid.write('\n')
    elif op[0:2] == '2d':
        if op[2:] == 'np': m, n = var.shape
        elif op[2:] == 'list':
            m = len(var)
            m = len(var[0])
        else:
            raise ValueError('unknown op')

        for i in xrange(m):
            for j in xrange(n):
                fid.write("%s "%(var[i,j]))
            fid.write("\n")
    else:
        raise ValueError('unknow op')

    fid.close()


try:
    import numpy as np
    from numpy import arange, pi, linspace
except ImportError:
    print('no numpy')

import inspect
def PrintVar(namespace, outputFile = ''):
    '''Print all variances in the namespace into .py file'''
    fid = -1
    if outputFile != '':
        fid = open(outputFile, 'w')
    for k, v in namespace.iteritems():
        if k.startswith("__")==0 and k not in imports:
            # print 'type(v), ', type(v)
            if type(v) == types.StringType:
                expr ='%s = \'%s\'\n' %(k, str(v))
            elif type(v) == types.FunctionType:
                expr = inspect.getsource(v) + '\n'
                # removing the leading blankspace
                leadingSpace = expr.rfind('def')
                if leadingSpace != 0 and leadingSpace != -1:
                    srcLine = inspect.getsourcelines(v)
                    expr = ''
                    for line in srcLine[0]:
                        expr = expr + line[leadingSpace:]
                if leadingSpace != -1:
                    GetFuncName = lambda s: s[s.find('def')+4:s.find('(')]
                    funcName = GetFuncName(expr)
                    if funcName != k: expr += '\n%s = %s\n' %(k, funcName)

            elif type(v) == types.BuiltinFunctionType:
                module =inspect.getmodule(v)
                expr = 'from %s import %s\n' %(module.__name__,  v.__name__)
            elif type(v) == types.ModuleType:
                expr = 'import %s as %s\n' %(v.__name__, k)
            elif type(v) == np.ndarray:
                expr = k + ' = ' + str(v.tolist()) + '\n'
            else:
                expr = '%s = %s\n' %(k, str(v))
            if fid == -1:
                print(expr,)
                continue
            fid.write( expr )
    if fid != -1:
        fid.close()


def PrintModelFree(mfIndi, mbIndi):
    '''Print the ModelFree Derivative which is not nan value'''
    # mfIndi = ModelFreeDetectAnoType()
    # mbIndi = ModelBaseDetectAnoType()
    for i in xrange(len(mfIndi)):
        if not np.isnan( mfIndi[i]):
            print('[%d]\t%f'%(i, mfIndi[i]))
    print('\n')


def PrintModelBase(mbIndi):
    '''print the model based derivative which is not nan value.'''
    m, n = mbIndi.shape
    for i in xrange(m):
        for j in xrange(n):
            if not np.isnan(mbIndi[i,j]):
                print('[%d, %d]\t%f' %(i, j, mbIndi[i,j]))
    print('\n')


def abstract_method():
    """ This should be called when an abstract method is called that should have been
    implemented by a subclass. It should not be called in situations where no implementation
    (i.e. a 'pass' behavior) is acceptable. """
    raise NotImplementedError('Method not implemented!')

def FROM_CLS(*val_list):
    return ";".join(['%s=self.%s'%(v, v) for v in val_list])

def TO_CLS(*val_list):
    return ";".join(['self.%s=%s'%(v, v) for v in val_list])


class DataEndException(Exception):
    pass

class FetchNoDataException(Exception):
    pass



QUAN = 1
NOT_QUAN = 0

# The Distance Function
DF = lambda x,y:abs(x[0]-y[0]) * (256**3) + abs(x[1]-y[1]) * (256 **2) + abs(x[2]-y[2]) * 256 + abs(x[3]-y[3])

def zeros(s):
    if len(s) == 1:
        return [0] * s[0]
    elif len(s) == 2:
        return [[0 for i in xrange(s[1])] for j in xrange(s[0])]
    else:
        raise Exception('unknown size in zeros')


# import inspect
def get_help_docs(dic):
    docs = []
    for k, v in dic.iteritems():
        doc  = inspect.getdoc(v)
        comp_doc = "%s %s"%(v.__name__, doc.rsplit('\n')[0]) \
                if doc else v.__name__
        docs.append("'%s': %s"%(k, comp_doc))

    return docs

def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)


def load_config(f_name, encap=None, allow_types=(list, str, dict, float, int),
        kwargs={}):
    """load configurations.

    Parameters:
    ----------------------
    f_name : str
        is the path of the configuration file
    allow_types : tuple
        specify the allowed types in parameter file.
    encap : function
        is the additional operation done to the data, for example,
        the default value encap=Namespace is to change parameters from dict
        to Namespace class.
    kwargs : dict
        contains some additional parameters
    """
    if f_name.endswith('.py'):
        config = kwargs
        execfile(f_name, config)
        if allow_types is not None:
            res = dict()
            for k, v in config.iteritems():
                for t_ in allow_types:
                    if isinstance(v, t_):
                        res[k] = v
                        break
            config = res
        del config['__builtins__']

    elif f_name.endswith('.json'):
        import json
        config = json.load(open(f_name, 'r'))
        config.update(kwargs)
        return config
    else:
        raise Exception('unknown type of config!')

    return config if encap is None else encap(config)

import csv
def save_csv(f_name, names, *args):
    with open(f_name, 'w') as f:
        w = csv.writer(f)
        valid_idx = [i for i in xrange(len(args)) if args[i] is not None]
        valid_names = [names[i] for i in valid_idx]
        valid_args = [args[i] for i in valid_idx]
        w.writerow(valid_names)
        w.writerows(zip(*valid_args))


import collections
def mkiter(e):
    """make e iteratable"""
    if not isinstance(e, collections.Iterable):
        return [e]
    else:
        return e

# import numpy as np
def meval(cmd):
    """to make arange, pi and linespace to be able to used directly in eval()"""
    return eval(cmd)

def del_none_key(dt):
    """delete key whose value is None"""
    res = dict()
    for k, v in dt.iteritems():
        if v is not None:
            res[k] = v
    return res


def update_not_none(d1, d2):
    for k, v in d2.iteritems():
        if v is not None:
            d1[k] = v

# class List(object):
#     """ List that support add with another List and division over a float or int.

#     Examples
#     -------------
#     >>> a = List([1, 2, 3])
#     >>> b = List([2, 3, 4])
#     >>> c = a + b
#     >>> d = a / 2
#     """
#     def __init__(self, d):
#         self.d = d
#         self.n = len(d)

#     def __add__(self, val):
#         if val is None:
#             return self

#         for i in xrange(self.n):
#             self.d[i] = self.d[i] + val[i]
#         return self

#     def __div__(self, val):
#         for i in xrange(self.n):
#             self.d[i] /= val
#         return self

#     def __str__(self):
#         return str(self.d)

#     def __getitem__(self, k):
        # return self.d[k]

##############################
# Data Storage and Load
###############################
try:
    import cPickle as pickle
except ImportError:
    import pickle
import gzip
proto = pickle.HIGHEST_PROTOCOL
def zdump(obj, f_name):
    f = gzip.open(f_name,'wb', proto)
    pickle.dump(obj,f)
    f.close()

def zload(f_name):
    f = gzip.open(f_name,'rb', proto)
    obj = pickle.load(f)
    f.close()
    return obj

import collections

class DataRecorder(object):
    def __init__(self):
        self._records = collections.defaultdict(list)
        pass

    def add(self, **kwargs):
        for k, v in kwargs.iteritems():
            self._records[k].append(v)

    def reset(self):
        self._records = collections.defaultdict(list)

    def to_pandas_dataframe(self):
        import pandas
        return pandas.DataFrame(self._records)

def get_detect_metric(A, B, W):
    """**A** is the referece, and **B** is the detected result, **W** is the whole set
    calculate the true positive, false negative, true negative and false positive
    """
    A = set(A)
    B = set(B)
    W = set(W)
    # no of true positive, no of elements that belongs to B and also belongs to A
    tp = len(set.intersection(A, B))

    # no of false negative no of elements that belongs to A but doesn't belong to B
    fn = len(A - B)

    # no of true negative, no of element that not belongs to A and not belong to B
    tn = len(W - set.union(A, B))
    # no of false positive, no of element that not belongs to A but belongs to B
    fp = len(B - A)

    # sensitivity is the probability of a alarm given that the this flow is anormalous
    sensitivity = tp * 1.0 / (tp + fn) if (tp + fn) > 0 else float('nan')
    # specificity is the probability of there isn't alarm given that the flow is normal
    specificity = tn * 1.0 / (tn + fp) if (tn + fp) > 0 else float('nan')

    return tp, fn, tn, fp, sensitivity, specificity


def generate_text_axis(length):
    """A function to generate text-base axis.
    """
    import itertools
    import math
    def get_text_with_sep(length, sep):
        length = int(length)
        c = itertools.cycle('0123456789')
        return sep.join(c.next() for _ in xrange(length))

    result = []
    l_str = str(length)
    sep = ' '
    l = length
    for _ in xrange(len(l_str)):
        line = get_text_with_sep(math.ceil(l), sep[:-1])
        result.append(line)
        sep *= 10
        l /= 10.0

    return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()

