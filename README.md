# Classifying Fecundity Data UI

This UI is meant to help with classifying split images. Each image is a 75x75 "tile" of the original image. We use tile to refer to the image displayed on the site.
![Screenshot 2025-01-06 162822](https://github.com/user-attachments/assets/f069d3cd-0d1e-430b-a7d1-c0fb29bfb627)

## UI Rules

You will be assigned two folders to look through and assign labels to. The UI contains the following buttons: One, two, three, unsure, custom count, and undo. With this program, you will be classifying the number of eggs in the tile provided.



#### One, Two, Three, and Four through Nine
Select these options if there are one, two, or three eggs in the image. You can use the keyboard to type these numbers and they will automatically classify them.

#### Unsure
If you are unsure about the number of eggs in an image, click this, or type u. These will later be reviewed by Ken and classified accordingly.

#### Custom Count
If there are more than three eggs in the image, use the **arrows** to go the number of the number of eggs in the tile. Then, click submit.

#### Undo
If you make a mistake, click Undo, ctrl+z, or z. This allows you to reclassify the image.

#### Important: Partial Egg Counting
There is no partial egg button! If you see more than 70% of an egg in the image or you didn't _really_ have to think about if this is an egg or not, count is as an egg. If there's very little of the egg in the image (e.g. less than 20% of the egg), do not count it as an egg. If you are unsure, click "Unsure."

## Getting Started

### Dependencies

* Python >3.9.6
* Flask
* numpy
* cv2

### Installing & Executing the Program

#### 1. Downloading Python
* I used Python 3.12.5, so I recommend that but if your existing Python version is 3.9.6 and up, you don't need to update your Python.
* If you don't have Python, click [here](https://www.python.org/downloads/) and install it. Follow the directions that it states.

#### 2. Getting the Repository
1. Click the Green Code button in the right side and press "Download Zip," this should download the Classifier-Site repository onto your computer
2. Find which folder this has been downloaded, it is most likely in your Downloads folder

##### macOS/Linux

3. Right click on the Classifier-Site folder and press Get Info. There should be an option called "Where" containing information as to the folders the Classifier-Site directory is in.

<img width="263" alt="Screenshot 2024-12-14 at 5 56 31 PM" src="https://github.com/user-attachments/assets/98640e07-6f7c-4ef6-85b4-25cc0d3725cd" />

You should have something similar, this means that the Classifier-Site path is **/Users/shreyanakum/Downloads/Classifier-Site**

4. Open Terminal and cd into the Classifier-Site directory:
```
$ cd [your-path-to-the-Classifier-Site-directory]
```
EX) In my case, I would type **cd /Users/shreyanakum/Downloads/Classifier-Site**
5. Now, we will double check that you have all necessary files/sub-directories:
```
$ ls
additions.txt		custom_arg.py		static
backend.py		preprocessing_files		image_shredder.py
```
If your output is missing one of these files, please contact us and do not proceed.

##### Windows

3. Right click on the Classifier-Site folder and press Properties. There should be "Location" field containing  the Classifier-Site directory's path. Copy it. If "Copy as Path" appears when you right-click, click that button instead. That should copy the path as well. Ensure that you're using the absolute path.

4. Open Command Prompt and cd into the Classifier-Site directory:
```
> cd [your-path-to-the-Classifier-Site-directory]
```
5. Now, we will double check that you have all necessary files/sub-directories:
```
> dir
additions.txt
custom_arg.py
static
backend.py
preprocessing_files
image_shredder.py
```
If your output is missing one of these, please contact us and do not proceed.

#### 3. Pip
* If you downloaded Python from python.org (the link provided in the previous step), you should already have pip.
* If you have an older version if pip and are using **macOS or Linux**, please update it now by running (the $ is just to indicate shell, do not copy it when you run the command):
```
$ pip install --upgrade pip
```
If you are a **Windows** user try:
```
> py -m pip install --upgrade pip
```
If neither of these worked, Google your error. If you are still having issues, contact me (Shreya). 

#### 4. Virtual Environment & Flask
* The backend of this program was written using [Flask](https://flask.palletsprojects.com/en/stable/installation/), a Python package that is a web framework with tools and libraries for building web applications (like this one)!
* Before you install Flask, you need to make a virtual environment.
  
##### macOS/Linux
```
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install Flask
$ pip install numpy
$ pip install opencv-python
```
##### Windows
```
> py -3 -m venv .venv
> .venv\Scripts\activate
> pip install Flask
> pip install numpy
> pip install opencv-python
```

#### 5. Execution
* You should have been emailed a two folders containing the images that you will classify. Choose one.
* The folder's structure should be:
```
.
├── FolderName
```

* Do what you did when finding the path to the Classifier-Site directory to find the path of the folder you just chose again.
* **IMPORTANT NOTE:** If this is the SECOND time you're running the program, make sure that your path ends with "-sliced" otherwise the program will reshred the images.
EX) ./MONTH DAY/FolderName

Run the following command:
```
$ python3 backend.py [path-to-image-folder]
```

## Help

If you need help, email or text me, I can help with debugging your issues. Please include a screenshot of what the issue is and tell me what OS you're using.

## Authors

Shreya Nakum

[snakum@uci.edu](snakum@uci.edu)

Alden Black

## Version History
* 0.4
    * Added hot-keys for 4-9
    * Added ctrl+z and z for undo and u for unsure
    * Integrated image shredder into the backend
* 0.3
    * Added Undo button
    * Fixed issues with sys.argv
* 0.2
    * Added hot-keys
    * Added progress bar
    * Switched to number buttons
* 0.1
    * Initial Release
