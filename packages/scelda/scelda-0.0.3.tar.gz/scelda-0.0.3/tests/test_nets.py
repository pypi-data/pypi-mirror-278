import os
import pytest
import sys
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scelda.nets import activation, mlp, Codebook, Decoder, MLP, QAE, QEncoder, VAE, VEncoder

def test_activation(act='test'):
    with pytest.raises(NotImplementedError):
        activation(act)

def test_mlp(layers=(15, 10, 5), n_samples=1000, n_features=15):
    model = nn.Sequential(*list(mlp(layers)))
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    output = model(input)
    assert output.shape == (n_samples, layers[-1])

def test_MLP_forward(layers=(15, 10, 5), n_samples=1000, n_features=15):
    model = MLP(layers)
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    output = model(input)
    assert output.shape == (n_samples, layers[-1])

def test_Codebook_refresh(n_samples=1000, n_features=15, n_words=10, min_efficacy=.5):
    z = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    words = torch.hstack([torch.arange(n_words).repeat(n_samples//n_words), torch.arange(n_samples%n_words)])
    source = torch.arange(n_words)
    model = Codebook(n_words, min_efficacy)
    model.forward(z)
    model.refresh(z, words, source)
    assert model.codebook.shape == (n_words, n_features)

def test_Codebook_forward(n_samples=1000, n_features=15, n_words=10):
    z = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model = Codebook(n_words)
    model.forward(z)
    assert model.codebook.shape == (n_words, n_features)

def test_QEncoder_quantize(layers=(15, 10, 5), n_samples=1000, n_features=15, n_words=10):
    z = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model = QEncoder(*layers, n_words=n_words)
    words, loss = model.quantize(z, c_grad=True)
    assert words.shape == (n_samples, n_features)
    assert loss > 0

def test_QEncoder_forward(layers=(15, 10, 5), n_samples=1000, n_features=15, n_words=10):
    model = QEncoder(*layers, n_words=n_words)
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    output, loss = model(input)
    assert output.shape == (n_samples, layers[-1])
    assert loss == 0

def test_VEncoder_forward(layers=(15, 10, 5), n_samples=1000, n_features=15):
    model = VEncoder(*layers)
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    output, loss = model(input)
    assert output.shape == (n_samples, layers[-1])
    assert loss > 0

def test_Decoder_forward(layers=(5, 10, 15), n_samples=1000, n_features=5):
    model = Decoder(*layers)
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    output = model(input)
    assert output.shape == (n_samples, layers[-1])

def test_QAE_build(layers=(15, 10, 5), n_samples=1000, n_features=15):
    model = QAE(*layers)
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model.build(input)
    assert model.layers[0] == input.shape[-1]
    assert model.encoder is not None
    assert model.decoder is not None
    assert model.optimizer is not None

def test_QAE_forward(layers=(15, 10, 5), n_samples=1000, n_features=15):
    model = QAE(*layers)
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model.build(input)
    loss = model(input)
    assert loss >= 0

def test_QAE_step(layers=(15, 10, 5), n_samples=1000, n_features=15):
    model = QAE(*layers)
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model.build(input)
    loss = model.step(input)
    assert loss >= 0

def test_QAE_fit(layers=(15, 10, 5), n_samples=1000, n_features=15, n_steps=10):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model = QAE(*layers).fit(input, n_steps, n_steps)
    assert len(model.loss_log) == 2*n_steps

def test_QAE_transform(layers=(15, 10, 5), n_samples=1000, n_features=15, n_steps=10):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model = QAE(*layers).fit(input, n_steps, n_steps)
    Z = model.transform(input)
    assert Z.shape[0] == n_samples

def test_VAE_build(layers=(15, 10, 5), n_samples=1000, n_features=15):
    model = VAE(*layers)
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model.build(input)
    assert model.layers[0] == input.shape[-1]
    assert model.encoder is not None
    assert model.decoder is not None
    assert model.optimizer is not None

def test_VAE_forward(layers=(15, 10, 5), n_samples=1000, n_features=15):
    model = VAE(*layers)
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model.build(input)
    loss = model(input)
    assert loss >= 0

def test_VAE_step(layers=(15, 10, 5), n_samples=1000, n_features=15, batch_size=32):
    model = VAE(*layers)
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model.build(input)
    loader = DataLoader(input, batch_size=batch_size)
    loss = model.step(loader)
    assert loss >= 0

def test_VAE_fit(layers=(15, 10, 5), n_samples=1000, n_features=15, n_steps=10):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model = VAE(*layers).fit(input, n_steps)
    assert len(model.loss_log) == n_steps

def test_VAE_transform(layers=(15, 10, 5), n_samples=1000, n_features=15, n_steps=10):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)
    model = VAE(*layers).fit(input, n_steps)
    Z = model.transform(input)
    assert Z.shape[0] == n_samples
