"""
Craig Fouts (cfouts@nygenome.org)
Sarah Rodwin (srodwin@nygenome.org)
"""

import numpy as np
import os
import pickle
import torch
from scipy import stats
from scipy.cluster.vq import kmeans, vq
from scipy.spatial.distance import cdist
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm
from .nets import VAE
from .util import set_seed

def load_SLDA(name='slda'):
    """TODO
    
    Parameters
    ----------
    TODO

    Returns
    -------
    TODO
    """
    
    with open(name + '.pkl', 'rb') as f:
        attributes = pickle.load(f)

    model = SLDA(1)
    model.__dict__ = attributes

    return model

def load_sceLDA(name='scelda'):
    """TODO
    
    Parameters
    ----------
    TODO

    Returns
    -------
    TODO
    """
    
    with open(name + '.pkl', 'rb') as f:
        attributes = pickle.load(f)

    model = sceLDA(1)
    model.__dict__ = attributes

    return model

class SLDA(BaseEstimator, TransformerMixin):
    """TODO
    
    Parameters
    ----------
    TODO

    Attributes
    ----------
    TODO
    """
    
    def __init__(self, n_topics, n_docs=900, vocab_size=25, n_replicates=5, sigma=1.5, alpha=None, beta=None, batch_size=None, type_stack=False, time_stack=False, img_stack=False, seed=None):
        super().__init__()

        if seed is not None:
            set_seed(seed)

        self.n_topics = n_topics
        self.n_docs = n_docs
        self.vocab_size = vocab_size
        self.n_replicates = n_replicates
        self.sigma = sigma
        self.alpha = 1/n_docs if alpha is None else alpha
        self.beta = 1/n_topics if beta is None else beta
        self.batch_size = batch_size
        self.type_stack = type_stack
        self.time_stack = time_stack
        self.img_stack = img_stack
        self.seed = seed

        self.corpus = None
        self.doc_locs = None
        self.doc_topic_counts = None
        self.topic_word_counts = None
        self.topic_log = []
        self.likelihood_log = []

    def shuffle(self, words):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        docs = np.random.choice(self.n_docs, (words.shape[0], 1))
        topics = np.random.choice(self.n_topics, (words.shape[0], 1))
        doc_range, topic_range = np.arange(self.n_docs), np.arange(self.n_topics)
        self.doc_topic_counts = (docs == doc_range).T@np.eye(self.n_topics)[topics.T[0]]
        self.topic_word_counts = (topics == topic_range).T@np.eye(self.vocab_size)[words]

        return docs, topics
    
    def build(self, data, n_steps, burn_in, vocab_steps=10):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        if not self.img_stack:
            data = np.hstack([np.zeros((data.shape[0], 1)), data])
        
        locs, markers = data[:, :3], data[:, 3:]
        self.n_docs = np.unique(locs[:, 0]).shape[0]*self.n_docs
        doc_idx = np.random.permutation(data.shape[0])[:self.n_docs]
        self.doc_locs = np.hstack([locs[doc_idx, :1], np.random.normal(locs[doc_idx, 1:], 1e-1)])
        codebook, _ = kmeans(markers, self.vocab_size, vocab_steps)
        words = np.concatenate((vq(markers, codebook)[0],)*self.n_replicates)
        docs, topics = self.shuffle(words)
        self.corpus = np.hstack([np.vstack((locs,)*self.n_replicates), words[None].T, docs, topics])
        self.topic_log = np.zeros((self.corpus.shape[0], n_steps - burn_in))

        if self.batch_size is None:
            self.batch_size = self.corpus.shape[0]

        return self
    
    def save(self, name='slda'):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(self.__dict__, f)

    def sample_doc(self, loc, topic, return_likelihood=False):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        mask = (self.doc_locs[:, 0] == loc[0]).astype(np.int32)
        sqdiff = ((loc[1:] - self.doc_locs[:, 1:])**2).sum(-1)
        doc_probs = np.exp(-sqdiff/self.sigma**2)
        topic_probs = self.doc_topic_counts[:, topic] + self.alpha
        topic_probs /= (self.doc_topic_counts + self.alpha).sum(-1)
        probs = mask*doc_probs*topic_probs
        probs /= probs.sum()
        doc = np.random.choice(self.n_docs, p=probs)
        
        if return_likelihood:
            return doc, probs[doc]
        
        return doc
    
    def sample_topic(self, word, doc, return_likelihood=False, maximize=False):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        topic_probs = self.doc_topic_counts[doc] + self.alpha
        topic_probs /= (self.doc_topic_counts[doc] + self.alpha).sum()
        word_probs = self.topic_word_counts[:, word] + self.beta
        word_probs /= (self.topic_word_counts + self.beta).sum(-1)
        probs = topic_probs*word_probs/(topic_probs*word_probs).sum()
        topic = np.argmax(probs) if maximize else np.random.choice(self.n_topics, p=probs)

        if return_likelihood:
            return topic, probs[topic]
        
        return topic
    
    def sample(self, loc, word, old_doc, old_topic, return_likelihood=False, maximize=False):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        new_doc, doc_likelihood = self.sample_doc(loc, old_topic, return_likelihood)
        new_topic, topic_likelihood = self.sample_topic(word, old_doc, return_likelihood, maximize)
        
        if return_likelihood:
            return new_doc, new_topic, doc_likelihood + topic_likelihood

        return new_doc, new_topic
    
    def decrement(self, word, doc, topic):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        self.doc_topic_counts[doc, topic] -= 1
        self.topic_word_counts[topic, word] -= 1

        return self.doc_topic_counts, self.topic_word_counts
    
    def increment(self, word, doc, topic):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        self.doc_topic_counts[doc, topic] += 1
        self.topic_word_counts[topic, word] += 1

        return self.doc_topic_counts, self.topic_word_counts
    
    def step(self, step, maximize=False):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        likelihood_sum = 0

        for i in range(self.corpus.shape[0]):
            loc, (word, old_doc, old_topic) = self.corpus[i, :3], self.corpus[i, 3:].astype(np.int32)
            self.decrement(word, old_doc, old_topic)
            new_doc, new_topic, likelihood = self.sample(loc, word, old_doc, old_topic, return_likelihood=True, maximize=maximize)
            self.increment(word, new_doc, new_topic)
            self.corpus[i, -2:] = new_doc, new_topic
            self.topic_log[i, step] = new_topic
            likelihood_sum += likelihood

        return likelihood_sum
    
    def fit(self, X, n_steps=500, burn_in=400, desc='SLDA', verbosity=1):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        self.build(X, n_steps, burn_in)

        for i in tqdm(range(n_steps), desc=desc) if verbosity == 1 else range(n_steps):
            likelihood = self.step((i - burn_in)%(n_steps - burn_in))
            self.likelihood_log.append(likelihood)

        return self
    
    def transform(self, _=None):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        TODO
        """
        
        topic_log = []
        n_samples = self.corpus.shape[0]//self.n_replicates

        for i in range(self.n_replicates):
            topic_log.append(self.topic_log[i*n_samples:(i+1)*n_samples])

        topic_log = np.hstack(topic_log)
        topics = stats.mode(topic_log, -1)[0]

        return topics

class sceLDA(BaseEstimator, TransformerMixin):
    """TODO
    
    Parameters
    ----------
    TODO

    Attributes
    ----------
    vae : VAE
        TODO
    slda : SLDA
        TODO
    """

    def __init__(self, n_topics, layers=(20,), n_docs=900, vocab_size=25, n_replicates=5, sigma=1.5, alpha=None, beta=None, img_stack=False, seed=None):
        super().__init__()

        self.seed = seed

        self.vae = VAE(*layers, seed=seed)
        self.slda = SLDA(n_topics, n_docs, vocab_size, n_replicates, sigma, alpha, beta, img_stack=img_stack, seed=seed)

    def save(self, name='scelda'):
        """TODO
        
        Parameters
        ----------
        TODO

        Returns
        -------
        None
        """
        
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(self.__dict__, f)

    def fit(self, X, n_vae_steps=500, n_slda_steps=500, learning_rate=1e-2, batch_size=32, test_size=0., burn_in=100, verbosity=1):  # , info_rate=5):
        """TODO
        
        Parameters
        ----------
        X : array-like of shape=(n_samples, n_features)
            TODO
        n_vae_steps : int, default=1000
            TODO
        learning_rate : float, default=1e-2
            TODO
        n_slda_steps : int, default=500
            TODO
        burn_in : int, default=100
            TODO
        vae_patience : int, default=10
            TODO
        vae_window : int, default=10
            TODO
        slda_patience : int, default=5
            TODO
        slda_window : int, default=5
            TODO
        verbosity : int, default=1
            TODO
            Supports 0, 1, or 2.
        info_rate : int, default=5
            TODO

        Returns
        -------
        self
            I return therefore I am.
        """

        if not torch.is_tensor(X):
            X = torch.tensor(X, dtype=torch.float32)

        locs, features = X[:, :3], X[:, 3:]
        self.vae.fit(features, n_vae_steps, learning_rate, batch_size, test_size, verbosity=verbosity)  # , info_rate=info_rate)
        Z = torch.hstack([locs, self.vae.transform(features)]).detach().numpy()
        self.slda.fit(Z, n_slda_steps, burn_in, verbosity=verbosity)  # , info_rate=info_rate)

        return self
    
    def transform(self, X):
        """TODO
        
        Parameters
        ----------
        X : array-like of shape=(n_samples, n_features)
            TODO

        Returns
        -------
        ndarray of shape=(n_samples,)
            TODO
        """

        topics = self.slda.transform(X)

        return topics
