import sys
import os
import random
from flask import Flask, jsonify, request, send_from_directory
from collections import deque

import logging
logging.basicConfig(level=logging.DEBUG)

from preprocessing_files.pruning import classify_white_spaces
from custom_arg import ArgumentError

import image_shredder
import cv2

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

n = len(sys.argv)
if (n < 2):
    raise ArgumentError("Missing directory argument.")
backend = sys.argv[0]
IMAGE_FOLDER = sys.argv[1]

if (n > 2):
    IMAGE_FOLDER = ' '.join(sys.argv[1:])
if not os.path.isdir(IMAGE_FOLDER):
    raise ArgumentError('Image bank path must lead to a directory.')

# classify_white_spaces(IMAGE_FOLDER) # this takes about 1-2 minutes to run, dw about it, it's removing all white space squares

# check if the first image is 75 x 75, if it is not, then run the shredder on the folder
first_image_path = os.path.join(IMAGE_FOLDER, os.listdir(IMAGE_FOLDER)[0])
print(f'first image path: {first_image_path}')
first_image = cv2.imread(first_image_path)
print(first_image)
height, width = first_image.shape[:2]
if (height != 75 or width != 75):
    image_shredder.main(IMAGE_FOLDER)
    IMAGE_FOLDER+="-sliced"
    classify_white_spaces(IMAGE_FOLDER)

categorization_history = deque(maxlen=10) # use a single history stack for the local instance which holds the most recent 10 images changed

@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), filename)

def get_next_image():
    images = [f for f in os.listdir(IMAGE_FOLDER) if ((f.endswith('.jpg') or f.endswith('.png')) and not (f.startswith('eggs') or f.startswith('unsure')))]
    return random.choice(images) if images else None

@app.route('/undo', methods=['POST'])
def undo():
    if not categorization_history:
        return jsonify({'success': False, 'error': 'No actions to undo'}), 400

    last_action = categorization_history.pop()
    old_name, new_name = last_action['new_name'], last_action['old_name']

    old_path = os.path.join(IMAGE_FOLDER, old_name)
    new_path = os.path.join(IMAGE_FOLDER, new_name)

    try:
        os.rename(old_path, new_path)
        return jsonify({'success': True, 'imagePath': f'/images/{new_name}'})
    except Exception as e:
        logging.error(f"Error in undo: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# @app.route('/categorize', methods=['POST'])
# import os

@app.route('/categorize', methods=['POST'])
def categorize():
    data = request.json
    old_name = data['imageName'].replace("%20", " ")
    category = data['category']
    new_name = f"{category}{old_name}"

    old_path = os.path.join(IMAGE_FOLDER, old_name)
    new_path = os.path.join(IMAGE_FOLDER, new_name)
   
    try:
        # Check if the new file name already exists
        if os.path.exists(new_path):
            # If it exists, generate a unique name by appending a number
            base, extension = os.path.splitext(new_name)
            counter = 1
            while os.path.exists(new_path):
                new_name = f"{base}_{counter}{extension}"
                new_path = os.path.join(IMAGE_FOLDER, new_name)
                counter += 1

        os.rename(old_path, new_path)
       
        # store the action in the history with both the old and new name it gets later on
        categorization_history.append({'old_name': old_name, 'new_name': new_name})
       
        return jsonify({'success': True, 'newName': new_name})
    except Exception as e:
        logging.error(f"Error in categ:  {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# def categorize():
#     data = request.json
#     old_name = data['imageName'].replace("%20", " ")
#     category = data['category']
#     new_name = f"{category}{old_name}"

#     old_path = os.path.join(IMAGE_FOLDER, old_name)
#     new_path = os.path.join(IMAGE_FOLDER, new_name)
   
#     try:
#         os.rename(old_path, new_path)
       
#         # store the action in the history with both the old and new name it gets later on
#         categorization_history.append({'old_name': old_name, 'new_name': new_name})
       
#         return jsonify({'success': True})
#     except Exception as e:
#         logging.error(f"Error in categ:  {str(e)}")
#         return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/next-image', methods=['GET'])
def next_image():
    image = get_next_image()
    if image:
        return jsonify({'imagePath': f'/images/{image}'})
    return jsonify({'error': 'No more images available'}), 404

# @app.route('/categorize', methods=['POST'])
# def categorize():
#     data = request.json
#     old_name = data['imageName'].replace("%20", " ")
#     category = data['category']
#     new_name = f"{category}{old_name}"



#     old_path = os.path.join(IMAGE_FOLDER, old_name)
#     new_path = os.path.join(IMAGE_FOLDER, new_name)
   
#     try:
#         os.rename(old_path, new_path)
#         return jsonify({'success': True})
#     except Exception as e:
#         logging.error(f"Error in categ:  {str(e)}")
#         return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/total-images', methods=['GET'])
def total_images():
    images = [f for f in os.listdir(IMAGE_FOLDER) if (f.endswith('.jpg') and not (f.startswith('eggs') or f.startswith('unsure')))]
    return jsonify({'totalImages': len(images)})


if __name__ == '__main__':
    app.run(debug=True)


# import sys
# import os
# import random
# from flask import Flask, jsonify, request, send_from_directory
# from collections import deque

# import logging
# logging.basicConfig(level=logging.DEBUG)

# from preprocessing_files.pruning import classify_white_spaces
# from custom_arg import ArgumentError

# import image_shredder
# import cv2

# app = Flask(__name__)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# n = len(sys.argv)
# if (n < 2):
#     raise ArgumentError("Missing directory argument.")
# backend = sys.argv[0]
# IMAGE_FOLDER = sys.argv[1]

# if (n > 2):
#     IMAGE_FOLDER = ' '.join(sys.argv[1:])
# if not os.path.isdir(IMAGE_FOLDER):
#     raise ArgumentError('Image bank path must lead to a directory.')

# # classify_white_spaces(IMAGE_FOLDER) # this takes about 1-2 minutes to run, dw about it, it's removing all white space squares

# # check if the first image is 75 x 75, if it is not, then run the shredder on the folder
# first_image_path = os.path.join(IMAGE_FOLDER, os.listdir(IMAGE_FOLDER)[0])
# print(f'first image path: {first_image_path}')
# first_image = cv2.imread(first_image_path)

# height, width = first_image.shape[:2]
# if (height != 75 or width != 75):
#     image_shredder.main(IMAGE_FOLDER)
#     IMAGE_FOLDER+="-sliced"
#     classify_white_spaces(IMAGE_FOLDER)

# categorization_history = deque(maxlen=10) # use a single history stack for the local instance which holds the most recent 10 images changed

# @app.route('/')
# def index():
#     return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), 'index.html')

# @app.route('/static/<path:filename>')
# def static_files(filename):
#     return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), filename)

# def get_next_image():
#     images = [f for f in os.listdir(IMAGE_FOLDER) if ((f.endswith('.jpg') or f.endswith('.png')) and not (f.startswith('eggs') or f.startswith('unsure')))]
#     return random.choice(images) if images else None

# @app.route('/undo', methods=['POST'])
# def undo():
#     if not categorization_history:
#         return jsonify({'success': False, 'error': 'No actions to undo'}), 400

#     last_action = categorization_history.pop()
#     old_name, new_name = last_action['new_name'], last_action['old_name']

#     old_path = os.path.join(IMAGE_FOLDER, old_name)
#     new_path = os.path.join(IMAGE_FOLDER, new_name)

#     try:
#         os.rename(old_path, new_path)
#         return jsonify({'success': True, 'imagePath': f'/images/{new_name}'})
#     except Exception as e:
#         logging.error(f"Error in undo: {str(e)}")
#         return jsonify({'success': False, 'error': str(e)}), 500

# @app.route('/categorize', methods=['POST'])
# def categorize():
#     data = request.json
#     old_name = data['imageName'].replace("%20", " ")
#     category = data['category']
#     new_name = f"{category}{old_name}"

#     old_path = os.path.join(IMAGE_FOLDER, old_name)
#     new_path = os.path.join(IMAGE_FOLDER, new_name)
   
#     try:
#         os.rename(old_path, new_path)
       
#         # store the action in the history with both the old and new name it gets later on
#         categorization_history.append({'old_name': old_name, 'new_name': new_name})
       
#         return jsonify({'success': True})
#     except Exception as e:
#         logging.error(f"Error in categ:  {str(e)}")
#         return jsonify({'success': False, 'error': str(e)}), 500
    
# @app.route('/next-image', methods=['GET'])
# def next_image():
#     image = get_next_image()
#     if image:
#         return jsonify({'imagePath': f'/images/{image}'})
#     return jsonify({'error': 'No more images available'}), 404

# # @app.route('/categorize', methods=['POST'])
# # def categorize():
# #     data = request.json
# #     old_name = data['imageName'].replace("%20", " ")
# #     category = data['category']
# #     new_name = f"{category}{old_name}"



# #     old_path = os.path.join(IMAGE_FOLDER, old_name)
# #     new_path = os.path.join(IMAGE_FOLDER, new_name)
   
# #     try:
# #         os.rename(old_path, new_path)
# #         return jsonify({'success': True})
# #     except Exception as e:
# #         logging.error(f"Error in categ:  {str(e)}")
# #         return jsonify({'success': False, 'error': str(e)}), 500

# @app.route('/images/<path:filename>')
# def serve_image(filename):
#     return send_from_directory(IMAGE_FOLDER, filename)

# @app.route('/total-images', methods=['GET'])
# def total_images():
#     images = [f for f in os.listdir(IMAGE_FOLDER) if (f.endswith('.jpg') and not (f.startswith('eggs') or f.startswith('unsure')))]
#     return jsonify({'totalImages': len(images)})


# if __name__ == '__main__':
#     app.run(debug=True)
