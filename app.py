from flask import Flask
from flask_cors import CORS
from controllers import container, image
from controllers.web import container as web_container, index

app = Flask(__name__)
CORS(app)

# CONTAINER ENDPOINTS
app.register_blueprint(container.api)

# IMAGE ENDPOINTS
app.register_blueprint(image.api)

# CONTAINER PAGES
app.register_blueprint(index.web)
app.register_blueprint(web_container.web)
if __name__ == '__main__':
    app.run(debug=True)
