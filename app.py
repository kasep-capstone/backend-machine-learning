from flask import Flask
from flasgger import Swagger
from routes.recommend import recommend_bp
import logging
# from flask_cors import CORS

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
swagger = Swagger(app)
# CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprint
app.register_blueprint(recommend_bp, url_prefix='/api')

@app.route('/')
def index():
    return 'OK', 200

@app.route('/health')
def health_check():
    app.logger.debug("Health check called")
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
