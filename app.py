from flask import Flask
from flask_cors import CORS
from controllers import container, image

app = Flask(__name__)
CORS(app)

# CONTAINER ENDPOINTS
app.register_blueprint(container.api)

# IMAGE ENDPOINTS
app.register_blueprint(image.api)

if __name__ == '__main__':
    app.run(debug=True)
