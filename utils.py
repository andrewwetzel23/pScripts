

def adjust_label_number(label_path, number):
    files = get_texts_from_dir(label_path)
    for file_name in files:
        f = open(join(label_path, file_name), 'r')
        lines = f.read().splitlines()
        f.close()

        f = open(join(label_path, file_name), 'w')
        for line in lines:
            line = str(number) + line[1:]
            f.write(f'{line}\n')
        f.close()

def move_source_data(model):
    jpgs = get_imgs_from_dir(model.data)
    mp4s = get_videos_from_dir(model.data)

    for jpg in jpgs:
        shutil.move(join(model.data, jpg), join(model.path, 'jpg', 'unsorted'))

    for mp4 in mp4s:
        shutil.move(join(model.data, mp4), join(model.path, 'mp4', 'new'))