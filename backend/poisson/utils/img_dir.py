import os


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
