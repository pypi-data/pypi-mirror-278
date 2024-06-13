# -*- coding: utf-8 -*-
from alibabacloud_computenestsupplier20210521.client import Client as ComputeNestSupplier20210521Client
from computenestcli.client.base import BaseClient

AP_SOUTHEST_1 = 'ap-southeast-1'


class ComputeNestClient(BaseClient):

    def __init__(self, context):
        super().__init__(context.region_id,
                         context.credentials.access_key_id,
                         context.credentials.access_key_secret)

    def create_client_compute_nest(self):
        if self.region_id == AP_SOUTHEST_1:
            self.config.endpoint = f'computenestsupplier.ap-southeast-1.aliyuncs.com'
        else:
            self.config.endpoint = f'computenestsupplier.cn-hangzhou.aliyuncs.com'

        return ComputeNestSupplier20210521Client(self.config)