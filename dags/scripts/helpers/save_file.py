def save_file(name, content, extension, path):
    file = open(path+name+'.'+extension, 'wb')
    file.write(content)
    file.close()
    print(f'{name}.{extension} saved.')