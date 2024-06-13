import numpy as np
import os
import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scelda.models import sceLDA, SLDA

def test_SLDA_shuffle(n_topics=10, n_samples=100, vocab_size=25):
    words = np.hstack([np.arange(vocab_size).repeat(n_samples//vocab_size), np.arange(n_samples%vocab_size)])
    docs, topics = SLDA(n_topics).shuffle(words)
    assert docs.shape == topics.shape == (n_samples, 1)

def test_SLDA_build(n_topics=10, n_samples=1000, n_markers=100, n_replicates=5, n_steps=10, burn_in=5):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    markers = np.arange(n_samples*n_markers).reshape(n_samples, n_markers)
    data = np.hstack([locs, markers])
    model = SLDA(n_topics, n_replicates=n_replicates).build(data, n_steps, burn_in)
    assert model.corpus.shape == (n_samples*n_replicates, 6)
    assert model.topic_log.shape == (n_samples*n_replicates, n_steps - burn_in)

def test_SLDA_sample_doc(n_topics=10, n_samples=1000, n_markers=100, n_steps=10, burn_in=5, loc=np.arange(3), topic=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    markers = np.arange(n_samples*n_markers).reshape(n_samples, n_markers)
    data = np.hstack([locs, markers])
    model = SLDA(n_topics).build(data, n_steps, burn_in)
    doc, likelihood = model.sample_doc(loc, topic, return_likelihood=True)
    assert type(doc) == int
    assert likelihood > 0

def test_SLDA_sample_topic(n_topics=10, n_samples=1000, n_markers=100, n_steps=10, burn_in=5, word=0, doc=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    markers = np.arange(n_samples*n_markers).reshape(n_samples, n_markers)
    data = np.hstack([locs, markers])
    model = SLDA(n_topics).build(data, n_steps, burn_in)
    topic, likelihood = model.sample_topic(word, doc, return_likelihood=True)
    assert type(topic) == int
    assert likelihood > 0

def test_SLDA_decrement(n_topics=10, n_samples=1000, n_markers=100, n_steps=10, burn_in=5, word=0, doc=0, topic=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    markers = np.arange(n_samples*n_markers).reshape(n_samples, n_markers)
    data = np.hstack([locs, markers])
    model = SLDA(n_topics).build(data, n_steps, burn_in)
    doc_topic_counts = model.doc_topic_counts.copy()
    topic_word_counts = model.topic_word_counts.copy()
    model.decrement(word, doc, topic)
    assert model.doc_topic_counts[doc, topic] == doc_topic_counts[doc, topic] - 1
    assert model.topic_word_counts[topic, word] == topic_word_counts[topic, word] - 1

def test_SLDA_increment(n_topics=10, n_samples=1000, n_markers=100, n_steps=10, burn_in=5, word=0, doc=0, topic=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    markers = np.arange(n_samples*n_markers).reshape(n_samples, n_markers)
    data = np.hstack([locs, markers])
    model = SLDA(n_topics).build(data, n_steps, burn_in)
    doc_topic_counts = model.doc_topic_counts.copy()
    topic_word_counts = model.topic_word_counts.copy()
    model.increment(word, doc, topic)
    assert model.doc_topic_counts[doc, topic] == doc_topic_counts[doc, topic] + 1
    assert model.topic_word_counts[topic, word] == topic_word_counts[topic, word] + 1

def test_SLDA_step(n_topics=10, n_samples=1000, n_markers=100, n_steps=10, burn_in=5, step=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    markers = np.arange(n_samples*n_markers).reshape(n_samples, n_markers)
    data = np.hstack([locs, markers])
    model = SLDA(n_topics).build(data, n_steps, burn_in)
    likelihood = model.step(step)
    assert (model.corpus[:, -1:].T[0] == model.topic_log[:, step]).all()
    assert likelihood > 0

def test_SLDA_fit(n_topics=10, n_samples=1000, n_markers=100, n_steps=10, burn_in=5):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    markers = np.arange(n_samples*n_markers).reshape(n_samples, n_markers)
    data = np.hstack([locs, markers])
    model = SLDA(n_topics).fit(data, n_steps, burn_in, verbosity=0)
    assert len(model.likelihood_log) == n_steps

def test_SLDA_transform(n_topics=10, n_samples=1000, n_markers=100, n_steps=10, burn_in=5):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    markers = np.arange(n_samples*n_markers).reshape(n_samples, n_markers)
    data = np.hstack([locs, markers])
    model = SLDA(n_topics).fit(data, n_steps, burn_in, verbosity=0)
    topics = model.transform(data)
    assert 0 <= topics.max() < n_topics
    assert topics.shape[0] == n_samples

def test_sceLDA_fit(n_topics=10, n_samples=1000, n_markers=100, n_vae_steps=10, n_slda_steps=10, burn_in=5):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    markers = np.arange(n_samples*n_markers).reshape(n_samples, n_markers)
    data = np.hstack([locs, markers])
    model = sceLDA(n_topics).fit(data, n_vae_steps, n_slda_steps, burn_in=burn_in)
    assert len(model.vae.loss_log) == n_vae_steps
    assert len(model.slda.likelihood_log) == n_slda_steps

def test_sceLDA_transform(n_topics=10, n_samples=1000, n_markers=100, n_vae_steps=10, n_slda_steps=10, burn_in=5):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    markers = np.arange(n_samples*n_markers).reshape(n_samples, n_markers)
    data = np.hstack([locs, markers])
    model = sceLDA(n_topics).fit(data, n_vae_steps, n_slda_steps, burn_in=burn_in)
    topics = model.transform(data)
    assert 0 <= topics.max() < n_topics
    assert topics.shape[0] == n_samples
