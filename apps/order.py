import uuid
from flask import Flask
from flask import jsonify
from flexiv_consul_service.conf import settings
from flexiv_consul_service.src.base_service import ConsulBaseService
from flexiv_consul_service.src.base_service import request

app = Flask(__name__)


@app.route('/product_detail')
def get_product_detail():
    response = request(url='http://product/product_detail', data={})
    name = response["data"].get("name")
    price = response["data"].get("price")
    return jsonify({
        "code": 200,
        "msg": "get product detail from product service",
        "data": {
            "name": name,
            "price": price
        }
    })


@app.route('/health')
def health_check():
    return 'service is health'


if __name__ == '__main__':
    host = '172.16.18.218'
    port = 5001
    
    # service register
    consul_client = ConsulBaseService(consul_ip=settings.CONSUL_IP, consul_port=settings.CONSUL_PORT)
    consul_client.register(name='order',
                           service_id=str(uuid.uuid4()),
                           address=host,
                           port=port,
                           tags=["v1", "order"])
    app.run(host=host, port=port)
