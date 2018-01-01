from flask import Flask, json, url_for
from flask_cors import CORS
from PIL import Image

from poisson.model import PoissonImageEditor
from poisson.utils.img_dir import get_images
from poisson.utils.api import data_url


app = Flask(__name__)
# allow CORS requests
CORS(app)


@app.route('/images')
def images():
    files = get_images('./static')
    return json.jsonify(
       list(map(lambda f: {'name': f, 'url': url_for('static', filename=f)},
                files)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
