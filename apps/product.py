import uuid
from flask import Flask
from flask import jsonify
from flexiv_consul_service.conf import settings
from flexiv_consul_service.src.base_service import ConsulBaseService

app = Flask(__name__)


@app.route('/product_detail')
def product_detail():
    return jsonify({
        "code": 200,
        "msg": "get product detail",
        "data": {
            "name": "iphone 13",
            "price": 6990
        }
    })


@app.route('/health')
def health_check():
    return 'service is health'


if __name__ == '__main__':
    host = '172.16.18.218'
    port = 5000
    service_name = 'product'
    service_id = str(uuid.uuid4())
    tags = ["v1", "product"]
    
    # service register
    consul_client = ConsulBaseService(consul_ip=settings.CONSUL_IP, consul_port=settings.CONSUL_PORT)
    consul_client.register(name=service_name,
                           service_id=service_id,
                           address=host,
                           port=port,
                           tags=tags)
    app.run(host=host, port=port)
