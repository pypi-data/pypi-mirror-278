"""
Craig Fouts (cfouts@nygenome.org)
Sarah Rodwin (srodwin@nygenome.org)
"""

import numpy as np
import torch
from sklearn.datasets import make_classification
from .util import itemize

HSBLOCKS = np.array([[0, 0],
                     [1, 1]], dtype=np.int32)

VSBLOCKS = np.array([[0, 1],
                     [0, 1]], dtype=np.int32)

CHBLOCKS = np.array([[0, 1, 0],
                     [1, 0, 1],
                     [0, 1, 0]], dtype=np.int32)

GGBLOCKS = np.array([[0, 1, 0, 2, 2, 2],
                     [1, 1, 1, 2, 0, 2],
                     [0, 1, 0, 2, 2, 2],
                     [3, 0, 0, 4, 4, 4],
                     [3, 3, 0, 0, 4, 0],
                     [3, 3, 3, 0, 4, 0]], dtype=np.int32)

def partition(n_samples, n_partitions):
    """TODO
    
    Parameters
    ----------
    n_samples : int
        TODO
    n_partitions : int
        TODO

    Returns
    -------
    list of shape=(n_partitions,)
        TODO
    """

    parts = [n_samples // n_partitions]

    for i in range(1, n_partitions):
        parts.append((n_samples - sum(parts))//(n_partitions - i))
        
    return parts

def parameterize(n_components, n_features, n_equivocal=0, n_redundant=0, mean_scale=1., variance_scale=1.):
    """TODO
    
    Parameters
    ----------
    n_components : int
        TODO
    n_features : int
        TODO
    n_equivocal : int, default=0
        TODO
    n_redundant : int, default=0
        TODO
    mean_scale : float, default=1.0
        TODO
    variance_scale : float, default=1.0
        TODO

    Returns
    -------
    ndarray of shape=(n_components, n_features)
        TODO means
    ndarray of shape=(n_features,)
        TODO variances
    """
    
    n_informative = n_features - n_equivocal - n_redundant
    means, _ = make_classification(n_samples=n_components, n_features=n_features, n_informative=n_informative, n_redundant=n_redundant, n_classes=n_components, n_clusters_per_class=1, scale=mean_scale)
    variances = variance_scale*np.random.rand(n_features)

    return means, variances

def designate(n_samples, n_components, n_features, n_equivocal=0, n_redundant=0, sample_counts=None, means=None, variances=None, mean_scale=1., variance_scale=1.):
    """TODO
    
    Parameters
    ----------
    n_samples : int
        TODO
    n_components : int
        TODO
    n_features : int
        TODO
    n_equivocal : int, default=0
        TODO
    n_redundant : int, default=0
        TODO
    sample_counts : tuple or list of shape=(n_components,), default=None
        TODO
    means : array-like of shape=(n_components, n_features), default=None
        TODO
    variances : array-like of shape=(n_features,), default=None
        TODO
    mean_scale : float, default=1.0
        TODO
    variance_scale : float, default=1.0
        TODO

    Returns
    -------
    list of shape=(n_components,)
        TODO sample_counts
    ndarray of shape=(n_components, n_features)
        TODO means
    ndarray of shape=(n_features,)
        TODO variances
    """
    
    if sample_counts is None:
        sample_counts = partition(n_samples, n_components)
    if means is None:
        means, _ = parameterize(n_components, n_features, n_equivocal, n_redundant, mean_scale, variance_scale)
    if variances is None:
        _, variances = parameterize(n_components, n_features, n_equivocal, n_redundant, mean_scale, variance_scale)

    return sample_counts, means, variances

def sample(n_samples, n_components, n_features, means, variances, component, n_mix=0):
    """TODO
    
    Parameters
    ----------
    n_samples : int
        TODO
    n_components : int
        TODO
    n_features : int
        TODO
    means : array-like of shape=(n_components, n_features)
        TODO
    variances : array-like of shape=(n_features,)
        TODO
    component : int
        TODO
    n_mix : int, default=0
        TODO

    Returns
    -------
    ndarray of shape=(n_samples, n_features)
        TODO data
    ndarray of shape=(n_samples,)
        TODO labels
    """
    
    labels = component*np.ones(n_samples, dtype=np.int32)
    data = np.random.normal(means[component], variances, (n_samples, n_features))
    
    mix_idx = np.random.randint(0, n_samples, n_mix)
    labels[mix_idx] = np.random.randint(0, n_components, n_mix)
    data[mix_idx] = np.random.normal(means[labels[mix_idx]], variances, (n_mix, n_features))
    
    return data, labels

def transfigure(blocks):
    """TODO
    
    Parameters
    ----------
    blocks : str
        TODO
        Supports 'hsblocks', 'vsblocks', 'chblocks', or 'ggblocks'.

    Returns
    -------
    ndarray of shape=(y_dim, x_dim)
        TODO
    """

    if isinstance(blocks, str):
        if blocks == 'hsblocks':
            return HSBLOCKS
        if blocks == 'vsblocks':
            return VSBLOCKS
        if blocks == 'chblocks':
            return CHBLOCKS
        if blocks == 'ggblocks':
            return GGBLOCKS
    
        raise NotImplementedError(f'Block palette "{blocks}" not supported.')
    
    return blocks

def interpret(blocks, share_components=False):  
    """TODO
    
    Parameters
    ----------
    blocks : tuple or list of shape=(n_blocks,)
        TODO
    share_components : bool, default=False
        TODO

    Returns
    -------
    list of shape=(n_blocks,)
        TODO blocks
    int
        TODO n_samples
    int
        TODO n_components
    """

    n_components = []

    for idx, b in enumerate(blocks):
        blocks[idx] = b = transfigure(b)
        n_components.append(np.unique(b).shape[0])

    n_components = max(n_components) if share_components else sum(n_components)

    return blocks, n_components

def make_data(n_samples, n_components, n_features, n_equivocal=0, n_redundant=0, sample_counts=None, means=None, variances=None, mean_scale=1., variance_scale=1., mix=0.):
    """TODO
    
    Parameters
    ----------
    n_samples : int
        TODO
    n_components : int
        TODO
    n_features : int
        TODO
    n_equivocal : int, default=0
        TODO
    n_redundant : int, default=0
        TODO
    sample_counts : tuple or list of shape=(n_components), default=None
        TODO
    means : array-like of shape=(n_components, n_features), default=None
        TODO
    variances : array-like of shape=(n_features,), default=None
        TODO
    mean_scale : float, default=1.0
        TODO
    variance_scale : float, default=1.0
        TODO
    mix : float, default=0.0
        TODO

    Returns
    -------
    ndarray of shape=(n_samples, n_features)
        TODO data
    ndarray of shape=(n_samples,)
        TODO labels
    """
    
    n_mix = partition(int(mix*n_samples), n_components)
    sample_counts, means, variances = designate(n_samples, n_components, n_features, n_equivocal, n_redundant, sample_counts, means, variances, mean_scale, variance_scale)
    data = np.zeros((n_samples, n_features), dtype=np.float32)
    labels = np.zeros(n_samples, dtype=np.int32)
    j = 0

    for i in range(n_components):
        k = j + sample_counts[i]
        data[j:k], labels[j:k] = sample(sample_counts[i], n_components, n_features, means, variances, i, n_mix[i])
        j += sample_counts[i]

    return data, labels

def make_blocks(blocks, n_features, n_equivocal=0, n_redundant=0, means=None, variances=None, mean_scale=1., variance_scale=1., block_size=5, wiggle=0., mix=0.):
    """TODO
    
    Parameters
    ----------
    blocks : array-like of shape=(y_dim, x_dim)
        TODO
    n_features : int
        TODO
    n_equivocal : int, default=0
        TODO
    n_redundant : int, default=0
        TODO
    means : array-like of shape=(n_components, n_features), default=None
        TODO
    variances : array-like of shape=(n_features,), default=None
        TODO
    mean_scale : float, default=1.0
        TODO
    variance_scale : float, default=1.0
        TODO
    block_size : int, default=5
        TODO
    wiggle : float, default=0.0
        TODO
    mix : float, default=0.0
        TODO

    Returns
    -------
    ndarray of shape=(n_samples, n_features)
        TODO data
    ndarray of shape=(n_samples,)
        TODO labels
    """
    
    grid = np.repeat(np.repeat(blocks, block_size, 0), block_size, 1)
    n_samples = grid.shape[0]*grid.shape[1]
    _, sample_counts = np.unique(grid, return_counts=True)
    n_components = sample_counts.shape[0]
    data, labels = make_data(n_samples, n_components, n_features, n_equivocal, n_redundant, sample_counts, means, variances, mean_scale, variance_scale, mix)
    data = np.hstack([np.zeros((data.shape[0], 2)), data])
    j = 0

    for i in range(n_components):
        locs = np.stack(np.where(grid.T == i)).T
        locs[:, -1] = -locs[:, -1] + grid.shape[0]
        data[j:j + locs.shape[0], :2] = locs
        j += locs.shape[0]

    data[:, :2] += 2*wiggle*np.random.rand(*data[:, :2].shape) - wiggle
    
    return data, labels

def make_dataset(blocks, n_features, n_equivocal=0, n_redundant=0, means=None, variances=None, mean_scale=1., variance_scale=1., block_size=5, wiggle=0., mix=0., img=None, offset=0, return_tensor=False):
    """TODO
    
    Parameters
    ----------
        blocks : array-like of shape=(y_dim, x_dim)
            TODO
        n_features : int
            TODO
        n_equivocal : int, default=0
            TODO
        n_redundant : int, default=0
            TODO
        means : array-like of shape=(n_components, n_features), default=None
            TODO
        variances : array-like of shape=(n_features,), default=None
            TODO
        mean_scale : float, default=1.0
            TODO
        variance_scale : float, default=1.0
            TODO
        block_size : int, default=5
            TODO
        wiggle : float, default=0.0
            TODO
        mix : float, default=0.0
            TODO
        img : int, default=None
            TODO
        offset : int, default=0
            TODO
        return_tensor : bool, default=False
            TODO

    Returns
    -------
    ndarray or tensor of shape=(n_samples, n_features)
        TODO
    ndarray or tensor of shape=(n_samples,)
        TODO
    """

    if means is not None:
        means = means[offset:]
    
    blocks = transfigure(blocks)
    data, labels = make_blocks(blocks, n_features, n_equivocal, n_redundant, means, variances, mean_scale, variance_scale, block_size, wiggle, mix)
    labels += offset

    if img is not None:
        data = np.hstack([img*np.ones((data.shape[0], 1)), data])

    if return_tensor:
        return torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.int32)
    
    return data, labels

def make_datasets(blocks, n_features, n_equivocal=0, n_redundant=0, means=None, variances=None, mean_scale=1., variance_scale=1., block_size=5, wiggle=0., mix=0., share_components=True, return_tensor=False):
    """TODO
    
    Parameters
    ----------
        blocks : list or array-like of shape=(n_datasets,) or (y_dim, x_dim)
            TODO
        n_features : int
            TODO
        n_equivocal : int, default=0
            TODO
        n_redundant : int, default=0
            TODO
        means : array-like of shape=(n_components, n_features), default=None
            TODO
        variances : array-like of shape=(n_features,), default=None
            TODO
        mean_scale : float, default=1.0
            TODO
        variance_scale : float, default=1.0
            TODO
        block_size : int or list of shape=(n_datasets,), default=5
            TODO
        wiggle : float or list of shape=(n_datasets,), default=0.0
            TODO
        mix : float or list of shape=(n_datasets,), default=0.0
            TODO
        share_components : bool, default=True
            TODO
        return_tensor : bool, default=False
            TODO

    Returns
    -------
        ndarray or tensor of shape=(n_samples, n_features)
            TODO data
        ndarray or tensor of shape=(n_samples,)
            TODO labels
    """
    
    n_datasets = len(blocks) if isinstance(blocks, list) else 1
    blocks, block_size, wiggle, mix = itemize(n_datasets, blocks, block_size, wiggle, mix)
    blocks, n_components = interpret(blocks, share_components)
    _, means, variances = designate(1, n_components, n_features, n_equivocal, n_redundant, 1, means, variances, mean_scale, variance_scale)
    datasets = []

    for idx, (b, s, w, m) in enumerate(zip(blocks, block_size, wiggle, mix)):
        offset = 0 if share_components or len(datasets) == 0 else max(datasets[-1][1]) + 1
        datasets.append(make_dataset(b, n_features, n_equivocal, n_redundant, means, variances, mean_scale, variance_scale, s, w, m, idx, offset))

    data, labels = zip(*datasets)
    data = np.concatenate(data)
    labels = np.concatenate(labels)

    if return_tensor:
        return torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.int32)
    
    return data, labels
