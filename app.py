from flask import Flask
from flasgger import Swagger
from routes.recommend import recommend_bp

app = Flask(__name__)
swagger = Swagger(app)

# Register blueprint
app.register_blueprint(recommend_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
