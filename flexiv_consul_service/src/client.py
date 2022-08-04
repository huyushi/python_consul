# -*- coding: utf-8 -*-

import requests
import json

from flexiv_consul_service.src.base_service import ConsulBaseService


def register_service(ip, port, service_list, consul_ip=None, consul_port=None):
    if not isinstance(service_list, list):
        raise TypeError("service list must be list params")
    if not service_list:
        raise Exception("service_list not allow empty")

    consul_client = ConsulBaseService(consul_ip, consul_port)
    for service in service_list:
        service_id = service + ip + ':' + str(port)
        consul_client.register(service, service_id=service_id, address=ip, port=port, tags=['master'])


def get_service_info(service_name: str, token: str, method="get", data={}, consul_ip=None, consul_port=None):
    if not service_name:
        raise Exception("not allow service empty")
    if not token:
        raise Exception("not allow token empty")

    consul_client = ConsulBaseService(consul_ip, consul_port)
    ip, port = consul_client.get_service(service_name)

    if not hasattr(requests, method):
        raise AttributeError(f'requests has no attribute {method} ')
    func = getattr(requests, method)

    if method == "get":
        headers = {"Authorization": f"jwt {token}", 'content-type': "text/plain"}
        service_res = func(f"http://{ip}:{port}/{service_name}",
                           params=data,
                           headers=headers,
                           verify=False, timeout=2.0)
    else:
        headers = {"Authorization": f"jwt {token}", 'content-type': "application/json"}
        service_res = func(f"http://{ip}:{port}/{service_name}",
                           data=json.dumps(data),
                           headers=headers,
                           verify=False, timeout=2.0)

    service_res_content = service_res.json()

    return service_res_content













