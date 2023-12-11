from flask import Flask, jsonify, request, redirect
from flask_caching import Cache
from circuitbreaker import circuit
from prometheus_flask_exporter import PrometheusMetrics
import requests
from load_balancer import get_healthy_cma_url, get_healthy_cr_url, cma_url_generator, cr_url_generator

app = Flask(__name__)
# initializing Flask Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://redis-master:6379/0'})

metrics = PrometheusMetrics(app)
# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

by_path_counter = metrics.counter(
    'by_path_counter', 'Request count by request paths',
    labels={'path': lambda: request.path}
)

# CMA_SERVICE_URL = "http://localhost:3000" 
# CR_SERVICE_URL = "http://localhost:4000" 
# Configuration for microservice endpoints
# CMA_SERVICE_URL = "http://cma" 
# CR_SERVICE_URL = "http://cr:4000" 

# load balancer implementation
CMA_SERVICE_URLS = ["http://cma:3010", "http://cma2:3011", "http://cma3:3012"]
CR_SERVICE_URLS = ["http://cr:4000", "http://cr2:4001", "http://cr3:4002"]


#health check endpoint 
@app.route('/health', methods=['GET'])
def get_health():
    return jsonify({"status": "ok"})


# routes for the cma service
@app.route('/cma/status', methods=['GET'])
def get_status_cma():
    try:
        cma_url = next(cma_url_generator)
        response = requests.get(f'{cma_url}/status')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/interactions/view', methods=['POST'])
# @circuit(failure_threshold=5, recovery_timeout=30)
def log_view_interaction():
    interaction_data = request.get_json()
    cma_url = next(cma_url_generator)
    response = requests.post(f"{cma_url}/interactions/view", json=interaction_data)
    return response.json(), response.status_code


@app.route('/interactions/like', methods=['POST'])
# @circuit(failure_threshold=5, recovery_timeout=30)
def log_like_interaction():
    interaction_data = request.get_json()
    cma_url = next(cma_url_generator)
    response = requests.post(f"{cma_url}/interactions/like", json=interaction_data)
    return response.json(), response.status_code

@app.route('/interactions/view/compensate', methods=['POST'])
def compensate_view_interaction_endpoint():
    try:
        interaction_data = request.get_json()
        cma_url = next(cma_url_generator)
        requests.post(f"{cma_url}/interactions/view/compensate", json=interaction_data)

        return jsonify({'message': 'Compensation for View Interaction completed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/interactions/comment', methods=['POST'])
def log_comment_interaction():
    interaction_data = request.get_json()
    cma_url = next(cma_url_generator)
    response = requests.post(f"{cma_url}/interactions/comment", json=interaction_data)
    return response.json(), response.status_code


@app.route('/interactions/comment/compensate', methods=['POST'])
def compensate_comment_interaction_endpoint():
    try:
        interaction_data = request.get_json()
        cma_url = next(cma_url_generator)
        requests.post(f"{cma_url}/interactions/comment/compensate", json=interaction_data)

        return jsonify({'message': 'Compensation for Comment Interaction completed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/interactions/add-to-favorites', methods=['POST'])
def log_add_to_favorites_interaction():
    interaction_data = request.get_json()
    cma_url = next(cma_url_generator)
    response = requests.post(f"{cma_url}/interactions/add-to-favorites", json=interaction_data)
    return response.json(), response.status_code


@by_path_counter
@app.route('/interactions', methods=['GET'])
@cache.cached(timeout = 60)
def get_all_interactions():
    cma_url = get_healthy_cma_url(cma_url_generator)
    response = requests.get(f"{cma_url}/interactions")
    return response.json(), response.status_code


# routes for the cr service
@app.route('/cr/status', methods=['GET'])
def get_status_cr():
    try:
        cr_url = next(cr_url_generator)
        response = requests.get(f'{cr_url}/status')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@by_path_counter
@app.route('/recommendations/<userId>', methods=['GET'])
@cache.cached(timeout = 60)
# @circuit(failure_threshold=5, recovery_timeout=30)
def get_recommendations(userId):
    cr_url = next(cr_url_generator)
    response = requests.get(f"{cr_url}/recommendations/{userId}")
    return response.json(), response.status_code
    

@by_path_counter
@app.route('/recommendations/<userId>/<contentId>', methods=['GET'])
@cache.cached(timeout = 60)
def get_content_from_recommendations(userId, contentId):
    cr_url = next(cr_url_generator)
    response = requests.get(f"{cr_url}/recommendations/{userId}/{contentId}")
    return response.json(), response.status_code


# routes for creating the content in the cr service
@app.route('/contents', methods=['POST'])
def create_content():
    content_data = request.get_json()
    cr_url = get_healthy_cr_url(cr_url_generator)
    response = requests.post(f"{cr_url}/contents", json=content_data)
    return response.json(), response.status_code


@app.route('/contents', methods=['GET'])
@cache.cached(timeout = 60)
def get_all_contents():
    cr_url = next(cr_url_generator)
    response = requests.get(f"{cr_url}/contents")
    return response.json(), response.status_code


@app.route('/contents/<contentId>', methods=['GET'])
@cache.cached(timeout = 60)
def get_content(contentId):
    cr_url = next(cr_url_generator)
    response = requests.get(f"{cr_url}/contents/{contentId}")
    return response.json(), response.status_code


@app.route('/contents/<contentId>', methods=['PUT'])
def update_content(contentId):
    content_data = request.get_json()
    cr_url = next(cr_url_generator)
    response = requests.put(f"{cr_url}/contents/{contentId}", json=content_data)
    return response.json(), response.status_code


@app.route('/contents/<contentId>', methods=['DELETE'])
def delete_content(contentId):
    cr_url = next(cr_url_generator)
    response = requests.delete(f"{cr_url}/contents/{contentId}")
    return response.json(), response.status_code


if __name__ == '__main__':
    app.run(debug=False, port=5050, host="0.0.0.0")