from agi_med_utils.dig_ass.db import make_session_id
from agi_med_utils.config.config import ConfigSingleton
from agi_med_utils.dig_ass.dataset import DigitalAssistantDataset

config = ConfigSingleton('/config').get()

dataset = DigitalAssistantDataset(**config['dataset'])

def test_session_id():
    out = make_session_id()
    assert isinstance(out, str)
    assert len(out) == 12

def test_dataset():
    assert isinstance(dataset.make_table(), dict)