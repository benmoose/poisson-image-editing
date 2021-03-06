from flask import Flask, jsonify, url_for, request, abort
from flask_cors import CORS

from poisson.utils.img_dir import get_images
from poisson.utils.api import APIError, saved_image_json
from poisson.utils.task_setup import load_image_or_error, parse_region
from poisson.tasks import task1, task2, task3, task5


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
    return saved_image_json(saved_to)


# TASK 2 ROUTE
@app.route('/poisson/t2/<source_name>/<dest_name>')
def task2_route(source_name, dest_name):
    # Load images
    source_im = load_image_or_error(source_name)
    dest_im = load_image_or_error(dest_name)
    # Get region corner coords (tl, tr, bl, br)
    region = request.args.get('region')
    region_arr = parse_region(region, source_im.size)
    # Get method type
    import_gradients_query = request.args.get('import_gradients') or ''
    import_gradients = import_gradients_query.lower() == 'true'
    # Run the task
    print('ig', import_gradients)
    saved_to = task2.task2(
        source_im, dest_im, region_arr, import_gradients=import_gradients)
    return saved_image_json(saved_to)


# TASK 3 ROUTE
@app.route('/poisson/t3/<source_name>/<dest_name>')
def task3_route(source_name, dest_name):
    # Load images
    source_im = load_image_or_error(source_name)
    dest_im = load_image_or_error(dest_name)
    # Get region corner coords (tl, tr, bl, br)
    region = request.args.get('region')
    region_arr = parse_region(region, source_im.size)
    saved_to = task3.task3(source_im, dest_im, region_arr)
    return saved_image_json(saved_to)


# TASK 4 ROUTE
@app.route('/poisson/t4')
def task4_route():
    # Load images
    img_dir = '/static/out/t4'
    return jsonify([
        {
            'final': '{}/final-e1642.png'.format(img_dir),
            'mask': '{}/mask-7b18d.png'.format(img_dir),
            'red_channel': '{}/ch-0-c8ad1.png'.format(img_dir),
            'green_channel': '{}/ch-1-2ef65.png'.format(img_dir),
            'blue_channel': '{}/ch-2-e8edd.png'.format(img_dir),
        },
        {
            'final': '{}/final-5747d.png'.format(img_dir),
            'mask': '{}/mask-e108b.png'.format(img_dir),
            'red_channel': '{}/ch-0-e43e3.png'.format(img_dir),
            'green_channel': '{}/ch-1-dcd2d.png'.format(img_dir),
            'blue_channel': '{}/ch-2-3bbe6.png'.format(img_dir),
        },
        {
            'final': '{}/final-d7b9b.png'.format(img_dir),
            'mask': '{}/mask-b8d6d.png'.format(img_dir),
            'red_channel': '{}/ch-0-587ad.png'.format(img_dir),
            'green_channel': '{}/ch-1-f111d.png'.format(img_dir),
            'blue_channel': '{}/ch-2-905b1.png'.format(img_dir),
        },
    ])


# TASK 5 ROUTE
@app.route('/poisson/t5/<image_name>')
def task5_route(image_name):
    # Load image
    im = load_image_or_error(image_name)
    # Get region corner coords (tl, tr, bl, br)
    region = request.args.get('region')
    region_arr = parse_region(region, im.size)
    # Run the task
    saved_to = task5.task5(im, region_arr)
    return saved_image_json(saved_to)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
