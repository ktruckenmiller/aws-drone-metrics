import os
import requests
import boto3
import logging
import datetime
import dateutil
from pprint import pprint
from prometheus_client.parser import text_string_to_metric_families

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    secret = ssm.get_parameter(
        Name=os.environ.get('SSM_KEY'),
        WithDecryption=True
    )
    endpoint = f'{os.environ.get("DRONE_SERVER")}/metrics'
    headers = {"Authorization": f"Bearer {secret['Parameter']['Value']}"}
    res = str(requests.get(endpoint, headers=headers).content)

    dm = DroneMetric()
    dm.load_metrics(res)
    dm.send_metrics()


class DroneMetric():
    def __init__(self):
        self.cw = boto3.client('cloudwatch')
        self.payload = []
        self.post_metrics = [
            'drone_build_count',
            'drone_pending_builds',
            'drone_pending_jobs',
            'drone_repo_count',
            'drone_running_builds',
            'drone_running_jobs',
            'drone_user_count'
        ]

    @staticmethod
    def convert_metric(metric):
        return ''.join(word.title() for word in metric.split('_'))

    def load_metrics(self, metrics):
        for line in metrics.split('\\n'):
            if '#' not in line:
                metric = line.split(' ')
                if metric[0] in self.post_metrics:
                    self.payload.append({
                        "MetricName": self.convert_metric(metric[0]),
                        "Dimensions": [{
                            "Name": "DroneServer",
                            "Value": "kloudcover"
                        }],
                        "Timestamp": datetime.datetime.now(dateutil.tz.tzlocal()),
                        "Value": int(metric[1])
                    })

    def send_metrics(self):
        r = self.cw.put_metric_data(
            Namespace='Drone',
            MetricData=self.payload
        )
        logger.info('Cloudwatch cluster metric sent')
