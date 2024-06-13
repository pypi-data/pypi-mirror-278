import numpy as np
import os
import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scelda.sim import CHBLOCKS, GGBLOCKS, designate, interpret, make_blocks, make_data, make_dataset, make_datasets, parameterize, partition, sample, transfigure

def test_partition(n_samples=4, n_partitions=5):
    parts = partition(n_samples, n_partitions)
    assert len(parts) == n_partitions
    assert sum(parts) == n_samples

def test_parameterize(n_components=10, n_features=15):
    means, variances = parameterize(n_components, n_features)
    assert means.shape == (n_components, n_features)
    assert variances.shape[0] == n_features

def test_designate(n_samples=1000, n_components=10, n_features=15):
    sample_counts, means, variances = designate(n_samples, n_components, n_features)
    assert len(sample_counts) == n_components
    assert sum(sample_counts) == n_samples
    assert means.shape == (n_components, n_features)
    assert variances.shape[0] == n_features

def test_sample(n_samples=1000, n_components=10, n_features=15, component=1):
    means, variances = parameterize(n_components, n_features)
    data, labels = sample(n_samples, n_components, n_features, means, variances, component)
    assert data.shape == (n_samples, n_features)
    assert labels.shape[0] == n_samples

def test_transfigure():
    blocks = transfigure('ggblocks')
    assert blocks.shape == GGBLOCKS.shape

def test_interpret():
    blocks, n_components = interpret(['chblocks', 'ggblocks'], share_components=False)
    assert len(blocks) == 2
    assert n_components == 7

def test_interpret_shared():
    blocks, n_components = interpret(['chblocks', 'ggblocks'], share_components=True)
    assert len(blocks) == 2
    assert n_components == 5

def test_make_data(n_samples=1000, n_components=10, n_features=15):
    data, labels = make_data(n_samples, n_components, n_features)
    assert data.shape == (n_samples, n_features)
    assert labels.shape[0] == n_samples
    assert np.unique(labels).shape[0] == n_components

def test_make_blocks(n_features=15, block_size=5):
    data, labels = make_blocks(GGBLOCKS, n_features, block_size=block_size)
    n_samples = GGBLOCKS.shape[0]*GGBLOCKS.shape[1]*block_size**2
    assert data.shape == (n_samples, n_features + 2)
    assert labels.shape[0] == n_samples
    assert np.unique(labels).shape[0] == 5

def test_make_dataset(n_features=15, block_size=5):
    data, labels = make_dataset(GGBLOCKS, n_features)
    n_samples = GGBLOCKS.shape[0]*GGBLOCKS.shape[1]*block_size**2
    assert data.shape == (n_samples, n_features + 2)
    assert labels.shape[0] == n_samples
    assert np.unique(labels).shape[0] == 5

def test_make_datasets(n_features=15, block_size=5):
    data, labels = make_datasets([CHBLOCKS, GGBLOCKS], n_features)
    n_samples = (CHBLOCKS.shape[0]*CHBLOCKS.shape[1] + GGBLOCKS.shape[0]*GGBLOCKS.shape[1])*block_size**2
    assert data.shape == (n_samples, n_features + 3)
    assert labels.shape[0] == n_samples
    assert np.unique(labels).shape[0] == 5
