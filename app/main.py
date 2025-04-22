from flask import Flask, jsonify, request
from .utils import is_prime, sum_digits
from .version import get_version

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, DevOps!"

@app.route('/version')
def version():
    return jsonify(version=get_version())

@app.route('/healthz')
def healthz():
    return jsonify(status="ok")

@app.route('/prime/<int:n>')
def route_is_prime(n):
    return jsonify(prime=is_prime(n))

@app.route('/sumdigits', methods=['POST'])
def route_sum_digits():
    try:
        data = request.get_json(force=True)
        n = int(data.get('number'))
        return jsonify(sum=sum_digits(n))
    except Exception as e:
        return jsonify(error=str(e)), 400

# Advanced: e.g., a “secret” endpoint to check for a workflow-set env variable (not used for flag, just for fun)
@app.route('/info')
def info():
    cicd_user = get_version()  # reusing get_version for demo
    return jsonify(message="Build info", version=get_version())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
