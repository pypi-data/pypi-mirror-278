import numpy as np
import os
import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scelda.models import SLDA
from scelda.util import autotune, map_labels, sample_grid, set_seed

def test_set_seed(seed=0):
    n1 = np.random.rand()
    set_seed(seed)
    n2 = np.random.rand()
    set_seed(seed)
    n3 = np.random.rand()
    assert n1 != n2 == n3

def test_sample_grid():
    parameter_grid = {
        'param1' : [0, 1, 2, 3],
        'param2' : [0, 1, 2, 3],
        'param3' : [0, 1, 2, 3],
        'param4' : [0, 1, 2, 3]
    }
    sample = sample_grid(parameter_grid)
    assert len(sample[0]) == 4

def test_autotune(n_samples=1000, n_markers=10, n_steps=10, burn_in=5):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    markers = np.arange(n_samples*n_markers).reshape(n_samples, n_markers)
    data = np.hstack([locs, markers])
    parameter_grid = {
        'n_topics' : [9, 10, 11],
    }
    parameters = autotune(SLDA, parameter_grid, data, threshold=1., log_id='likelihood_log', maximize=True, verbosity=0, n_steps=n_steps, burn_in=burn_in)
    assert len(parameters) == 1
    assert parameters['n_topics'] in [9, 10, 11]

def test_map_labels():
    X_labels = np.array([0, 1])
    Y_labels = np.array([1, 0])
    Z_labels = map_labels(X_labels, Y_labels)
    assert (Z_labels == X_labels).all()
