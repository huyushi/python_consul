# -*- coding: utf-8 -*-

import consul
import requests
import json
from random import randint
from flexiv_consul_service.conf import settings

from flexiv_consul_service.conf import settings as service_center_settings


class ConsulBaseService:
    _instance = None
    
    def __init__(self, consul_ip=None, consul_port=None):
        self.host = consul_ip if consul_ip else service_center_settings.CONSUL_IP
        self.port = consul_port if consul_port else service_center_settings.CONSUL_PORT
        self.token = service_center_settings.CONSUL_TOKEN
        self.consul = consul.Consul(host=self.host, port=self.port)
    
    def __call__(cls):
        if not cls._instance:
            cls._instance = ConsulBaseService()
        return cls._instance
    
    def register(self, name, service_id, address, port, tags):
        """
        Service register
        :param name: service name
        :param service_id: service id
        :param address: service ip
        :param port:
        :param tags:
        :return:
        """
        schema = 'http'
        check = consul.Check.http(f'{schema}://{address}:{port}/health', "5s", "5s", "5s")
        self.consul.agent.service.register(name,
                                           service_id=service_id,
                                           address=address,
                                           port=port,
                                           tags=tags,
                                           check=check)
    
    def get_service(self, name):
        """
        Service discovery
        :param name:
        :return:
        """
        # 获取相应服务下的 DataCenter
        url = 'http://' + self.host + ':' + str(self.port) + '/v1/catalog/service/' + name
        service_center_resp = requests.get(url)
        if service_center_resp.status_code != 200:
            raise Exception('can not connect to consul ')
        service_info_list = json.loads(service_center_resp.text)
        # 初始化 DataCenter
        temp_set = set()
        for service in service_info_list:
            temp_set.add(service.get('Datacenter'))
        # 服务列表初始化
        service_list = []
        for dc in temp_set:
            if self.token:
                url = f'http://{self.host}:{self.port}/v1/health/service/{name}?dc={dc}&token={self.token}'
            else:
                url = f'http://{self.host}:{self.port}/v1/health/service/{name}?dc={dc}&token='
            resp = requests.get(url)
            if resp.status_code != 200:
                raise Exception('can not connect to consul ')
            text = resp.text
            service_list_data = json.loads(text)
            
            for serv in service_list_data:
                status = serv.get('Checks')[1].get('Status')
                # 选取成功的节点
                if status == 'passing':
                    address = serv.get('Service').get('Address')
                    port = serv.get('Service').get('Port')
                    service_list.append({'port': port, 'address': address})
        if len(service_list) == 0:
            raise Exception('no service can be used')
        else:
            # 负载均衡随机获取一个服务节点
            service = service_list[randint(0, len(service_list) - 1)]
            return service['address'], int(service['port'])


def request(url: str, method="get", data={}):
    """
    request service
    :param url:
    :param method:
    :param data:
    :return:
    """
    service_name = url.split('/')[2]
    path = url.split('/')[3]
    consul_client = ConsulBaseService(settings.CONSUL_IP, settings.CONSUL_PORT)
    ip, port = consul_client.get_service(service_name)
    if not hasattr(requests, method):
        raise AttributeError(f'requests has no attribute {method} ')
    func = getattr(requests, method)
    
    if method == "get":
        service_res = func(f"http://{ip}:{port}/{path}",
                           params=data,
                           verify=False,
                           timeout=2.0)
    else:
        service_res = func(f"http://{ip}:{port}/{path}",
                           data=json.dumps(data),
                           verify=False,
                           timeout=2.0)
    
    service_res_content = service_res.json()
    
    return service_res_content
