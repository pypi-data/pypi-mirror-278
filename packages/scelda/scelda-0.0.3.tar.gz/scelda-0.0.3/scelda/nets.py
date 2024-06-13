"""
Craig Fouts (cfouts@nygenome.org)
Sarah Rodwin (srodwin@nygenome.org)
"""

import pyro
import pyro.distributions as dist
import pyro.optim as po
import torch
import torch.nn as nn
import torch.optim as to
from contextlib import nullcontext
from pyro.infer import SVI, Trace_ELBO
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from tqdm import tqdm
from .util import set_seed

def activation(act='relu', **kwargs):
    """Instantiates and returns the specified torch.nn activation object.
    
    Parameters
    ----------
    act : str, default='relu'
        Activation to instantiate.
        Supports 'relu', 'sigmoid', 'softplus', or 'softmax'.
    **kwargs : dict
        Additional arguments needed for the specified activation.

    Returns
    -------
    ReLU, Sigmoid, Softplus, or Softmax
        Instantiated object corresponding to the specified activation.

    Raises
    ------
    NotImplementedError
        If the specified activation is not supported.
    """

    if act == 'relu':
        return nn.ReLU(**kwargs)
    elif act == 'sigmoid':
        return nn.Sigmoid(**kwargs)
    elif act == 'tanh':
        return nn.Tanh(**kwargs)
    elif act == 'softplus':
        return nn.Softplus(**kwargs)
    elif act == 'softmax':
        return nn.Softmax(dim=-1)
    
    raise NotImplementedError(f'Activation function"{act}" not supported.')

def mlp(layers, bias=True, act='relu', final_act=None, batch_norm=True, affine=True, dropout=0.):
    """Generates linear neural network layers with activation, dropout, and 
    optional batch normalization.
    
    Parameters
    ----------
    layers : tuple or list of shape=(n_layers,)
        Sequence of integer values specifying the size of each layer.
    bias : bool, default=True
        Whether or not to learn an additive bias at each layer.
    act : str, default='relu'
        Hidden activation function.
        Supports 'relu', 'sigmoid', 'softplus', or 'softmax'.
    final_act : str, default=None
        Final activation function.
        Supports 'relu' | 'sigmoid' | 'softplus' | 'softmax'.
    batch_norm : bool, default=True
        Whether or not to perform final batch normalization.
    affine : bool, default=True
        Whether or not to allow for learnable affine parameters.
    dropout : float, default=0.0
        Probability of random node omission during training.

    Yields
    -------
    Linear, ReLU, Sigmoid, Softplus, Softmax, BatchNorm1d, or Dropout
        TODO
    """
    
    n_layers = len(layers) - 1

    for i in range(1, n_layers + 1):
        yield nn.Linear(layers[i - 1], layers[i], bias=bias)
        if i < n_layers - 1:
            yield activation(act)
        else:
            if batch_norm:
                yield nn.BatchNorm1d(layers[i], affine=affine)
            if final_act:
                yield activation(final_act)
            yield nn.Dropout(dropout)

class MLP(nn.Module):
    """TODO

    Parameters
    ----------
    layers : tuple or list of shape=(n_layers,)
        Sequence of integer values specifying the size of each layer.
    bias : bool, default=True
        Whether or not to learn an additive bias at each layer.
    act : str, default='relu'
        Hidden activation function.
        Supports 'relu', 'sigmoid', 'softplus', or 'softmax'.
    final_act : str, default=None
        Final activation function.
        Supports 'relu', 'sigmoid', 'softplus', or 'softmax'.
    batch_norm : bool, default=False
        Whether or not to perform final batch normalization.
    affine : bool, default=True
        Whether or not to allow for learnable affine parameters.
    dropout : float, default=0.0
        Probability of random node omission during training.
        
    Attributes
    ----------
    net : Sequential
        TODO
    """

    def __init__(self, layers, bias=True, act='relu', final_act=None, batch_norm=False, affine=True, dropout=0.):
        super().__init__()

        self.net = nn.Sequential(*list(mlp(layers, bias, act, final_act, batch_norm, affine, dropout)))
    
    def forward(self, x):
        """TODO

        Parameters
        ----------
        x : tensor of shape=(n_samples, input_dim)
            TODO

        Returns
        -------
        tensor of shape=(n_samples, output_dim)
            TODO
        """

        return self.net(x)
    
class Codebook(nn.Module):
    """TODO
    
    Parameters
    ----------
    n_words : int, default=10
        TODO
    min_efficacy : float, default=1e-2
        TODO

    Attributes
    ----------
    codebook : tensor of shape=(n_words, word_dim)
        TODO
    """
    
    def __init__(self, n_words=10, min_efficacy=1e-2):
        super().__init__()

        self.n_words = n_words
        self.min_efficacy = min_efficacy

        self.codebook = None

    @torch.no_grad()
    def refresh(self, z, words, source):
        """TODO
        
        Parameters
        ----------
        z : tensor of shape=(n_samples, sample_dim)
            TODO
        words : tensor of shape=(n_samples,)
            TODO
        source : tensor of shape=(>=n_words, word_dim)
            TODO

        Returns
        -------
        tensor of shape=(n_words, word_dim)
            TODO
        """
        
        idx, counts = words.unique(return_counts=True)
        bincount = torch.bincount(idx, counts, minlength=self.n_words)
        sink = bincount/idx.shape[0] < self.min_efficacy
        self.codebook[sink] = z.detach()[source[:sink.sum()]]

        return self.codebook

    def forward(self, z=None):
        """TODO
        
        Parameters
        ----------
        z : tensor of shape=(n_samples, sample_dim)
            TODO

        Returns
        -------
        tensor of shape=(n_words, word_dim)
            TODO
        """
        
        if self.codebook is None and z is not None:
            idx = torch.randperm(z.shape[0])[:self.n_words]
            self.codebook = nn.Parameter(z.detach()[idx], requires_grad=True)

        return self.codebook
    
class QEncoder(nn.Module):
    """TODO

    Parameters
    ----------
    TODO

    Attributes
    ----------
    TODO
    """
    
    def __init__(self, *layers, n_words=10, min_efficacy=1e-2):
        super().__init__()

        self.e_net = MLP(layers)
        self.codebook = Codebook(n_words, min_efficacy)
    
    def quantize(self, z, refresh=False, z_grad=False, c_grad=False, return_words=False):
        """TODO
        
        Parameters
        ----------
        TODO
    
        RETURNS
        -------
        TODO
        """
        
        z = z if z_grad else z.detach()
        codebook = self.codebook(z) if c_grad else self.codebook(z).detach()
        distances = (z[:, None] - codebook[None, :]).square().sum(-1)
        words = distances.argmin(-1)
        loss = distances[torch.arange(words.shape[0]), words].sum()

        if refresh:
            source = distances.max(-1)[0].argsort(descending=True)
            self.codebook.refresh(z, words, source)

        return words if return_words else self.codebook()[words], loss
    
    def forward(self, x, quantize=False, refresh=False, grad=False, return_words=False):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        with nullcontext() if grad else torch.no_grad():
            z = self.e_net(x)

        if quantize or return_words:
            words, z_loss = self.quantize(z, z_grad=grad, return_words=return_words)
            _, c_loss = self.quantize(z, refresh=refresh, c_grad=grad)

            return words, z_loss + c_loss
        return z, 0
    
class VEncoder(nn.Module):
    """TODO
    
    Parameters
    ----------
    TODO

    Attributes
    ----------
    TODO
    """
    
    def __init__(self, *layers):
        super().__init__()

        self.e_net = MLP(layers[:-1], final_act='softplus', dropout=.2)
        self.m_net = MLP(layers[-2:], batch_norm=True)
        self.v_net = MLP(layers[-2:], batch_norm=True)

    def forward(self, x, grad=False):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        with nullcontext() if grad else torch.no_grad():
            z = self.e_net(x)
            m, v = self.m_net(z), self.v_net(z).exp()
            z = m + v*torch.randn_like(v)
            kl_loss = (m.square() + v.square() - v.log() - .5).sum()

        return z, kl_loss
    
class Decoder(nn.Module):
    """TODO
    
    Parameters
    ----------
    TODO

    Attributes
    ----------
    TODO
    """
    
    def __init__(self, *layers, batch_norm=False, dropout=0.):
        super().__init__()

        self.d_net = MLP(layers, batch_norm=batch_norm, dropout=dropout)

    def forward(self, z, grad=False):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        with nullcontext() if grad else torch.no_grad():
            y = self.d_net(z)

            return y
    
class QAE(nn.Module, BaseEstimator, TransformerMixin):
    """TODO
    
    Parameters
    ----------
    TODO

    Attributes
    ----------
    TODO
    """
    
    def __init__(self, *layers, n_words=10, min_efficacy=1e-2, seed=None):
        super().__init__()

        if seed is not None:
            set_seed(seed)

        self.layers = layers
        self.n_words = n_words
        self.min_efficacy = min_efficacy
        self.seed = seed

        self.encoder = None
        self.decoder = None
        self.optimizer = None
        self.loss_log = []

    def build(self, X, learning_rate=1e-2):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        if self.layers[0] != X.shape[-1]:
            self.layers = (X.shape[-1], *self.layers)

        self.encoder = QEncoder(*self.layers, n_words=self.n_words, min_efficacy=self.min_efficacy)
        self.decoder = Decoder(*self.layers[::-1])
        self.optimizer = torch.optim.Adam(self.parameters(), learning_rate)

        return self

    def forward(self, x, quantize=False, refresh=False, grad=False):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        z, q_loss = self.encoder(x, quantize, refresh, grad)
        y = self.decoder(z, grad)
        loss = (y - x).square().sum() + q_loss

        return loss
    
    def step(self, x_train, x_test=None, quantize=False, refresh=False):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        assert self.optimizer is not None

        self.optimizer.zero_grad()
        loss = self(x_train, quantize, refresh, grad=True)
        loss.backward()
        self.optimizer.step()

        if x_test is not None:
            loss = self(x_test, quantize)

        return loss.item()
    
    def fit(self, X, n_ae_steps=100, n_vq_steps=100, learning_rate=1e-2, test_size=0., refresh_rate=1, verbosity=1):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        self.build(X, learning_rate)
        X_train, X_test = train_test_split(X, test_size=test_size) if test_size > 0. else (X, None)
        n_steps = n_ae_steps + n_vq_steps

        for i in tqdm(range(n_steps)) if verbosity == 1 else range(n_steps):
            quantize = i >= n_ae_steps
            refresh = i%refresh_rate == 0
            loss = self.step(X_train, X_test, quantize, refresh)
            self.loss_log.append(loss)

        return self
    
    def transform(self, X):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        quantize = self.encoder.codebook.codebook is not None
        Z, _ = self.encoder(X, return_words=quantize)

        return Z
    
class VAE(nn.Module, BaseEstimator, TransformerMixin):
    """TODO
    
    Parameters
    ----------
    TODO

    Returns
    -------
    TODO
    """
    
    def __init__(self, *layers, seed=None):
        super().__init__()

        if seed is not None:
            set_seed(seed)

        self.layers = layers
        self.seed = seed

        self.encoder = None
        self.decoder = None
        self.optimizer = None
        self.loss_log = []

    def build(self, X, learning_rate=1e-2):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        if self.layers[0] != X.shape[-1]:
            self.layers = (X.shape[-1], *self.layers)

        self.encoder = VEncoder(*self.layers)
        self.decoder = Decoder(*self.layers[::-1])
        self.optimizer = torch.optim.Adam(self.parameters(), learning_rate)

        return self
    
    def forward(self, x, grad=False):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        z, kl_loss = self.encoder(x, grad)
        y = self.decoder(z, grad)
        loss = (y - x).square().sum() + kl_loss

        return loss
    
    def step(self, x_loader, x_test=None):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        assert self.optimizer is not None

        for x in x_loader:
            self.optimizer.zero_grad()
            loss = self(x, grad=True)
            loss.backward()
            self.optimizer.step()

        if x_test is not None:
            loss = self(x_test)

        return loss.item()
    
    def fit(self, X, n_steps=500, learning_rate=1e-2, batch_size=32, test_size=0., desc='VAE', verbosity=1):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        self.build(X, learning_rate)
        X_train, X_test = train_test_split(X, test_size=test_size) if test_size > 0. else (X, None)
        X_loader = DataLoader(X_train, batch_size=batch_size)

        for _ in tqdm(range(n_steps), desc=desc) if verbosity == 1 else range(n_steps):
            loss = self.step(X_loader, X_test)
            self.loss_log.append(loss)

        return self

    def transform(self, X):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        Z, _ = self.encoder(X)

        return Z
