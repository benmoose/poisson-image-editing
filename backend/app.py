from flask import Flask, jsonify, url_for, request, abort
from flask_cors import CORS
from PIL import Image

from poisson.utils.img_dir import get_images
from poisson.utils.api import APIError
from poisson.tasks import task1


app = Flask(__name__)
# allow CORS requests
CORS(app)


@app.errorhandler(APIError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/images')
def images():
    files = get_images('./static')
    return jsonify(
       list(map(lambda f: {'name': f, 'url': url_for('static', filename=f)},
                files)))


# TASK 1 ROUTE
@app.route('/poisson/t1/<image_name>')
def poisson(image_name):
    # Get region corner coords (tl, tr, bl, br)
    region = request.args.get('region')
    if not region:
        raise APIError('region is a required parameter')
    # Convert region string to array
    region_arr = [int(p) for p in region.split(',')]
    # Validate length
    if len(region_arr) % 2 != 0:
        raise APIError('There must be an even number of region values')
    # Load the image and run the task
    try:
        im = Image.open('static/{}'.format(image_name))
        saved_to = task1.task1(im, region_arr)
        return jsonify(cropped_url='/{}'.format(saved_to))
    except FileNotFoundError:
        raise APIError('{} was not found'.format(image_name), status_code=404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
