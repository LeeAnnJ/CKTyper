try:
    import cPickle as pickle
except ImportError:
    import pickle


def dumpObj(path, obj):
    with open(path, 'wb') as f:
    # f = file(path, 'wb')
        pickle.dump(obj, f)
    # f.close()


def load(path):
    with open(path, 'rb') as f:
    # f = file(path, 'rb')
        return pickle.load(f)
