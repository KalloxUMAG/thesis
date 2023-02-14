def drop_first_line(file_path):
    with open(file_path, 'r+') as fp:
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()

        fp.writelines(lines[1:])