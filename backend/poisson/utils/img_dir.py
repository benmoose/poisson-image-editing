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


def save_image(image, name='out'):
    uid = str(uuid.uuid4())[:5]
    out_name = '{name}-{uid}.png'.format(name=name, uid=uid)
    out_dir = 'static/out/t1'
    save_to = os.path.join(out_dir, out_name)
    image.save(save_to)
    return save_to
