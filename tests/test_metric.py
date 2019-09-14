from src.index import lambda_handler, DroneMetric
import pytest
from unittest.mock import Mock,patch

@pytest.fixture
def dmo():
    return DroneMetric()

def test_metric_send(monkeypatch):
    monkeypatch.setenv('SSM_KEY', '/drone/production/cloudwatch')
    monkeypatch.setenv('DRONE_SERVER', 'https://drone.kloudcover.com')
    lambda_handler({}, {})

def test_convert_metric(dmo):
    assert dmo.convert_metric('boston_shoey') == 'BostonShoey'
