from flask import Flask, jsonify, url_for, request, abort
from flask_cors import CORS

from poisson.utils.img_dir import get_images
from poisson.utils.api import APIError
from poisson.utils.task_setup import load_image_or_error, parse_region
from poisson.tasks import task1, task2


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
def task1_route(image_name):
    # Load image
    im = load_image_or_error(image_name)
    # Get region corner coords (tl, tr, bl, br)
    region = request.args.get('region')
    region_arr = parse_region(region, im.size)
    # Run the task
    saved_to = task1.task1(im, region_arr)
    return jsonify(result_url='/{}'.format(saved_to))


# TASK 2 ROUTE
@app.route('/poisson/t2/<source_name>/<dest_image>')
def task2_route(source_name, dest_image):
    # Load image
    source_im = load_image_or_error(source_name)
    dest_im = load_image_or_error(dest_image)
    # Get region corner coords (tl, tr, bl, br)
    region = request.args.get('region')
    region_arr = parse_region(region, source_im.size)
    # Run the task
    saved_to = task2.task2(source_im, dest_im, region_arr)
    return jsonify(result_url='/{}'.format(saved_to))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
