"""
Craig Fouts (cfouts@nygenome.org)
Sarah Rodwin (srodwin@nygenome.org)
"""

import matplotlib.pyplot as plt
import muon as mu
import numpy as np
import os
import pyro
import random
import torch
from itertools import product
from matplotlib import cm, colormaps, colors
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm

def set_seed(seed=9):
    """Initializes uniform random number generators.

    Parameters
    ----------
    seed : int, default=9
        Value to be used for all random number generation.

    Returns
    -------
    None
    """

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True
    pyro.set_rng_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

def sample_grid(parameter_grid, threshold=.05):
    """TODO
    
    Parameters
    ----------
    parameter_grid : dict
        TODO
    threshold : float, default=0.05
        TODO

    Returns
    -------
    list of shape=(n_parameter_sets, n_parameters)
        TODO
    """
    
    ranges = [range(0, len(list(parameter_grid.values())[i])) for i in range(len(parameter_grid))]
    parameters = []
    
    for range_ in product(*ranges):
        if np.random.rand() < threshold:
            parameters.append({})

            for idx, value in enumerate(range_):
                parameters[-1][list(parameter_grid.keys())[idx]] = list(parameter_grid.values())[idx][value]

    return parameters

def autotune(model, parameter_grid, data, threshold=.1, recall=10, log_id='loss_log', maximize=False, verbosity=1, **kwargs):
    """TODO
    
    Parameters
    ----------
    subject : TODO
        TODO
    parameter_grid : dict
        TODO
    data : ndarray or tensor of shape=(n_samples, n_features)
        TODO
    threshold : float, default=0.05
        TODO
    recall : int, default=10
        TODO
    log_ids : str, default='loss_log'
        TODO
    maximize : bool, default=False
        TODO
    verbosity : int, default=1
        TODO
    kwargs : dict
        TODO

    Returns
    -------
    list of shape=(n_parameters,)
        TODO
    """
    
    parameters = sample_grid(parameter_grid, threshold)

    for parameter_set in tqdm(parameters) if verbosity == 1 else parameters:
        subject = model(**parameter_set)
        subject.fit_transform(data, verbosity=0, **kwargs)
        log = sum(getattr(subject, log_id)[-recall:])/recall

    parameter_idx = np.argmax(log) if maximize else np.argmin(log)
    parameter_set = parameters[parameter_idx]

    return parameter_set
    
def map_labels(X_labels, Y_labels):
    """Maps predicted clustering labels to the given ground truth using linear
    sum assignment.
    
    Parameters
    ----------
    X_labels : array-like of shape=(n_samples,)
        Ground truth cluster labels.
    Y_labels : array-like of shape=(n_samples,)
        Predicted cluster labels.

    Returns
    -------
    ndarray of shape=(n_samples,)
        TODO
    """

    scores = confusion_matrix(Y_labels, X_labels)
    row, col = linear_sum_assignment(scores, maximize=True)
    labels = np.zeros_like(X_labels)

    for i in row:
        labels[Y_labels == i] = col[i]

    return labels

def get_spatial(mdata, spatial_key='spatial', modality_key='morphological'):
    """TODO
    
    Parameters
    ----------
    mdata : MuData or AnnData
        TODO
    spatial_key : str, default='spatial'
        TODO
    modality_key : str, default='physical'
        TODO
    
    Returns
    -------
    ndarray of shape=(n_samples,)
        TODO
    ndarray of shape=(n_samples,)
        TODO
    """

    try:
        return mdata[modality_key].obsm[spatial_key].T
    except KeyError:
        return mdata.obsm[spatial_key].T
    
def get_features(mdata, feature_key='protein', imagenet_key='imagenet'):
    """TODO

    Parameters
    ----------
    MuData or AnnData
        TODO
    feature_key : str, default='protein'
        TODO
    imagenet_key : str, default='imagenet'
        TODO
    
    Returns
    -------
    ndarray of shape=(n_samples, n_features)
        TODO
    """

    try:
        features = mdata[feature_key].X
    except KeyError:
        features = mdata.X

    if imagenet_key:
        imagenet = mdata[imagenet_key].X
        features = np.hstack([features, imagenet])

    return features
    
def get_labels(mdata, label_key='celltype', modality_key='protein'):
    """TODO
    
    Parameters
    ----------
    MuData or AnnData
        TODO
    label_key : str, default='celltype'
        TODO
    modality_key : str, default='protein'
        TODO

    Returns
    -------
    ndarray of shape=(n_samples,)
        TODO
    """
    
    try:
        labels = mdata[modality_key].obs[label_key]
    except KeyError:
        labels = mdata.obs[label_key]

    return labels

def remove_lonely(data, labels, n_neighbors=12, threshold=225.):
    """Filters out samples that are too far removed from the data of interest
    according to the given threshold.

    Parameters
    ----------
    data : array-like of shape=(n_samples, n_features)
        Collection of samples to be filtered.
    labels : array-like of shape=(n_samples,)
        Component labels for each sample.
    n_neighbors : int, default=12
        TODO
    threshold : float, default=225.0
        TODO

    Returns
    -------
    ndarray of shape=(n_samples, n_features)
        TODO
    ndarray of shape=(n_samples,)
        TODO
    """

    knn = NearestNeighbors(n_neighbors=n_neighbors).fit(data[:, :2])
    max_dist = knn.kneighbors()[0].max(-1)
    mask_idx, = np.where(max_dist > threshold)
    data = np.delete(data, mask_idx, axis=0)
    labels = np.delete(labels, mask_idx, axis=0)

    return data, labels

def read_anndata(filename, spatial_key='spatial', feature_key='protein', spatial_modality='morphological', imagenet_key='imagenet', label_key='celltype', label_modality='protein', n_neighbors=12, threshold=225., delineate=True, return_tensor=False):
    """Reads the specified annotated data object according to the format used by
    the NYGC Technology Innovation Laboratory.
    
    Parameters
    ----------
    filename : str
        TODO
    spatial_key : str, default='spatial'
        TODO
    spatial_modality : str, default='morphological'
        TODO
    feature_key : str, default='protein'
        TODO
    imagenet_key : str, default='imagenet'
        TODO
    label_key : str, default='celltype'
        TODO
    label_modality : str, default='protein'
        TODO
    n_neighbors : int, default=12
        TODO
    threshold : float, default=225.0
        TODO
    delineate : bool, default=True
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

    mdata = mu.read(filename)
    x, y = get_spatial(mdata, spatial_key, spatial_modality)
    features = get_features(mdata, feature_key, imagenet_key)
    data = np.hstack([x[None].T, y[None].T, features])
    labels = get_labels(mdata, label_key, label_modality)
    _, labels = np.unique(labels, return_inverse=True)

    if threshold is not None:
        data, labels = remove_lonely(data, labels, n_neighbors, threshold)

    if delineate:
        data = np.hstack([np.zeros((data.shape[0], 1)), data])

    if return_tensor:
        return torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.int32)
    
    return data, labels

def read_anndatas(filenames, spatial_key='spatial', spatial_modality='morphological', feature_key='protein', imagenet_key='imagenet', label_key='celltype', label_modality='protein', n_neighbors=12, threshold=225., return_tensor=False):
    """Reads the specified annotated data object according to the format used by
    the NYGC Technology Innovation Laboratory.
    
    Parameters
    ----------
    filenames : list
        TODO
    spatial_key : str, default='spatial'
        TODO
    spatial_modality : str, default='morphological'
        TODO
    feature_key : str, default='protein'
        TODO
    imagenet_key : str, default='imagenet'
        TODO
    label_key : str, default='celltype'
        TODO
    label_modality : str, default='protein'
        TODO
    n_neighbors : int, default=12
        TODO
    threshold : float, default=225.0
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

    data, labels = [], []

    for i, filename in enumerate(filenames):
        mdata = mu.read(filename)
        x, y = get_spatial(mdata, spatial_key, spatial_modality)
        features = get_features(mdata, feature_key, imagenet_key)
        data_i = np.hstack([x[None].T, y[None].T, features])
        labels_i = get_labels(mdata, label_key, label_modality)
        _, labels_i = np.unique(labels_i, return_inverse=True)

        if threshold is not None:
            data_i, labels_i = remove_lonely(data_i, labels_i, n_neighbors, threshold)

        data.append(np.hstack([i*np.ones((data_i.shape[0], 1)), data_i]))
        labels.append(labels_i)

    data, labels = np.vstack(data), np.hstack(labels)

    if return_tensor:
        return torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.int32)
    
    return data, labels

def itemize(n, *items):
    """TODO
    
    Parameters
    ----------
    n : int
        TODO
    *items : any
        TODO
    
    Yields
    ------
    tuple or list of shape=(n,)
        TODO
    """

    for i in items:
        yield i if isinstance(i, (tuple, list)) else (i,)*n

def format_ax(ax, aspect='equal', show_ax=True):
    """TODO
    
    Parameters
    ----------
    ax : axis
        TODO
    aspect : str, default='equal'
        TODO
    show_ax : bool, default=True
        TODO

    Returns
    -------
    axis
        TODO
    """

    ax.set_aspect(aspect)
    
    if not show_ax:
        ax.axis('off')

    return ax

def show_dataset(locs, labels, size=15, figsize=5, show_ax=True, show_colorbar=False, colormap='Spectral', filename=None):
    """TODO
    
    Parameters
    ----------
    locs : array-like of shape=(n_samples, 2)
        TODO
    labels : array-like of shape=(n_samples,)
        TODO
    size : int, default=15
        TODO
    show_ax : bool, default=True
        TODO
    figsize : int, default=10
        TODO
    colormap : str, default='tab20'
        TODO
    filename : str, default=None
        TODO

    Returns
    -------
    None
    """

    cmap = colormaps.get_cmap(colormap)
    norm = colors.Normalize(labels.min(), labels.max())
    figsize, = itemize(2, figsize)
    fig, ax = plt.subplots(figsize=figsize)
    locs = locs[:, :2].T
    ax.scatter(*locs, s=size, c=cmap(norm(labels)))
    ax = format_ax(ax, aspect='equal', show_ax=show_ax)

    if show_colorbar:
        fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm))

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight', transparent=True)

def show_datasets(locs, labels, size=15, figsize=10, show_ax=True, show_colorbar=False, colormap='Spectral', filename=None):
    """TODO
    
    Parameters
    ----------
    locs : array-like of shape=(n_samples, 3)
        TODO
    labels : array-like of shape=(n_samples,)
        TODO
    size : int, default=15
        TODO
    figsize : int, default=10
        TODO
    show_ax : bool, default=True
        TODO
    colormap : str, default='tab20'
        TODO
    filename : str, default=None
        TODO

    Returns
    -------
    None
    """
    
    cmap = colormaps.get_cmap(colormap)
    norm = colors.Normalize(labels.min(), labels.max())
    n_datasets = np.unique(locs[:, 0]).shape[0]
    size, = itemize(n_datasets, size)
    figsize, = itemize(2, figsize)
    fig, ax = plt.subplots(1, n_datasets, figsize=figsize)
    axes = (ax,) if n_datasets == 1 else ax

    for i in range(n_datasets):
        idx = locs[:, 0].astype(np.int32) == i
        idx_locs = locs[idx, 1:3].T
        axes[i].scatter(*idx_locs, s=size[i], c=cmap(norm(labels[idx])))
        format_ax(axes[i], aspect='equal', show_ax=show_ax)

    if show_colorbar:
        fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm))

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight', transparent=True)

def show_logs(*logs, figsize=5, show_ax=True, filename=None):
    """TODO
    
    Parameters
    ----------
    *logs : tuple or list of shape=(n_logs,)
        TODO
    figsize : int, default=10
        TODO
    show_ax : bool, default=True
        TODO
    filename : str, default=None
        TODO

    Returns
    -------
    None
    """

    n_logs = len(logs)
    figsize, = itemize(2, figsize)
    fig, ax = plt.subplots(1, n_logs, figsize=figsize)
    axes = (ax,) if n_logs == 1 else ax

    for idx, log in enumerate(logs):
        if len(log) == 2:
            axes[idx].set_title(log[0])
            log = log[1]

        x = np.arange(len(log))
        axes[idx].plot(x, log)
        axes[idx].set_box_aspect(1)

        if not show_ax:
            axes[idx].tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight')
