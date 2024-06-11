import os, sys
import numpy as np
from agi_med_utils.config.config import ConfigSingleton
from agi_med_utils.llm.yandex_access import YandexGPTEntryPoint
from agi_med_utils.llm.giga_access import GigaChatEntryPoint, GigaPlusEntryPoint

config = ConfigSingleton('/config').get()

giga = GigaChatEntryPoint(**config['gigachat_creds'])   
giga_plus = GigaPlusEntryPoint(**config['gigachat_creds'])    
ya_gpt = YandexGPTEntryPoint(**config['yandex_creds'])

warmup_sent = 'Привет! Давай общаться!'

def cos_dist(emb, other_emb):
    return np.dot(emb, other_emb)/(np.linalg.norm(emb)*np.linalg.norm(other_emb))

def test_config():
    assert isinstance(config, dict)
    assert len(config)

def test_giga_text():  
    out = giga.get_response(warmup_sent)
    assert isinstance(out, str)
    assert len(out)

def test_giga_emb():  
    emb1 = giga.get_embedding(warmup_sent)
    emb2 = giga.get_embedding(warmup_sent)
    embs = giga.get_embeddings([warmup_sent for _ in range(100)])
    more_embs = giga.get_more_embeddings([warmup_sent for _ in range(2*1024)])
    assert isinstance(emb1, list)
    assert isinstance(embs, list)
    assert isinstance(more_embs, list)
    assert len(emb1) == giga.DIM
    assert len(embs) == 100
    assert len(more_embs) == 2*1024
    assert cos_dist(emb1, emb2) > 0.999
    assert cos_dist(embs[0], embs[-1]) > 0.999
    assert cos_dist(embs[0], emb2) > 0.999
    assert cos_dist(embs[0], more_embs[0]) > 0.999

def test_giga_plus_text():  
    out = giga_plus.get_response(warmup_sent)
    assert isinstance(out, str)
    assert len(out)

def test_giga_plus_emb():  
    emb1 = giga_plus.get_embedding(warmup_sent)
    emb2 = giga_plus.get_embedding(warmup_sent)
    embs = giga.get_embeddings([warmup_sent for _ in range(100)])
    more_embs = giga_plus.get_more_embeddings([warmup_sent for _ in range(2*1024)])
    assert isinstance(emb1, list)
    assert isinstance(embs, list)
    assert isinstance(more_embs, list)
    assert len(emb1) == giga.DIM
    assert len(embs) == 100
    assert len(more_embs) == 2*1024
    assert cos_dist(emb1, emb2) > 0.999
    assert cos_dist(embs[0], embs[-1]) > 0.999
    assert cos_dist(embs[0], emb2) > 0.999
    assert cos_dist(embs[0], more_embs[0]) > 0.999

def test_gigas_consistency():
    giga_emb = giga.get_embedding(warmup_sent)
    plus_emb = giga_plus.get_embedding(warmup_sent)
    assert cos_dist(plus_emb, giga_emb) > 0.999

def test_ya_gpt():
    out = ya_gpt.get_response('Привет!')
    assert isinstance(out, str)
    assert len(out)