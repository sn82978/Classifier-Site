import os

def classify_white_spaces(dir):
    '''removes white squares from the split image folders by automatically classifying them as having 0 eggs'''
    files = os.listdir(dir)
    for filename in files:
        filepath = os.path.join(dir, filename)
        if os.path.isfile(filepath) and (filename[0] != "e"):
            file_size_kb = os.stat(filepath).st_size / 1024
            if file_size_kb <= 2.00:
                new_name = f"eggs0count{filename}"
                new_path = os.path.join(dir, new_name)
                os.rename(filepath, new_path)