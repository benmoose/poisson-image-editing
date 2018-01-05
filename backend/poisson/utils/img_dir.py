import os
import uuid


def get_images(img_dir='img'):
    # returns a triple: root, dirs, files
    walk = os.walk(img_dir)
    # unpack walk results
    root, dirs, files = list(walk)[0]
    # acceptable image extensions
    img_exts = ['png', 'jpg', 'jpeg', 'gif']
    # return list of all img files in `img_dir`
    img_files = []
    for file in [f for f in files if f.lower().split('.')[-1] in img_exts]:
        img_files.append(file)
    return img_files


def save_image(image, task, name='out', use_hash=True):
    if not task:
        raise ValueError('Must specify a task directory')
    uid = '-{}'.format(str(uuid.uuid4())[:5]) if use_hash else ''
    out_name = '{name}{uid}.png'.format(name=name, uid=uid)
    out_dir = 'static/out/{}'.format(task)
    save_to = os.path.join(out_dir, out_name)
    image.save(save_to)
    return save_to


def clean_img_dir(task_dir):
    if not task_dir:
        raise ValueError('Must specify a task directory')
    files = os.listdir(os.path.join('static', 'out', task_dir))
    for file in files:
        os.remove(os.path.join('static', 'out', task_dir, file))
