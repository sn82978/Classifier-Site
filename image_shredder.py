import numpy as np
import cv2 as cv
import math
import os
import sys

def split_image(outpath, imgpath, imgid):
    img = cv.imread(imgpath, 1)
    height, width, _ = img.shape
    index = 1
    print(f"SPLITTING {imgid}")
    imgname = imgid[0:imgid.find(".")]
    # Since not all image resolutions are evenly divisible by 75, center w/ indent:
    y_indent = int(height%75/2)
    x_indent = int(width%75/2)
    y_splits = height//75
    x_splits = width//75
    for c in range(x_splits): # the number of columns = x
        for r in range(y_splits): # the number of rows = y
            y1 = r*75 + y_indent
            y2 = (r+1)*75 + y_indent
            x1 = c*75 + x_indent
            x2 = (c+1)*75 + x_indent
            crop_img = img[y1:y2, x1:x2] 
            # cv.imwrite(r'{}/{} pt{}.jpg'.format(outpath,imgname,index),crop_img) 
            cv.imwrite(os.path.join(outpath, f'{imgname} pt{index}.jpg'), crop_img)
            # outputs jpg
            index += 1

def main(path): # changed argv into path
    # path = ""
    # path = argv
    # for i in range(1, len(sys.argv)):
        # path += sys.argv[i] + " "
    # path = path[0:len(path)-1]
    for x in os.listdir(path): 
        # imgpath = f'{path}/{x}'
        imgpath = os.path.join(path, x)
        print(imgpath)
        if  x.endswith(".jpg") or x.endswith(".png"):
            outpath = r'{}-sliced'.format(path)
            if not os.path.exists(outpath):
                os.mkdir(outpath)
            split_image(outpath, imgpath, x)
    print("Finished!")

# main(0) # to run, type: > python3 image_shredder.py [folder-path]


# import numpy as np
# import cv2 as cv
# import math
# import os
# import sys

# def split_image(outpath, imgpath, imgid):
#     img = cv.imread(imgpath, 1)
#     height, width, _ = img.shape
#     index = 1
#     print(f"SPLITTING {imgid}")
#     imgname = imgid[0:imgid.find(".")]
#     # Since not all image resolutions are evenly divisible by 75, center w/ indent:
#     y_indent = int(height%75/2)
#     x_indent = int(width%75/2)
#     y_splits = height//75
#     x_splits = width//75
#     for c in range(x_splits): # the number of columns = x
#         for r in range(y_splits): # the number of rows = y
#             y1 = r*75 + y_indent
#             y2 = (r+1)*75 + y_indent
#             x1 = c*75 + x_indent
#             x2 = (c+1)*75 + x_indent
#             crop_img = img[y1:y2, x1:x2] 
#             cv.imwrite(r'{}/{} pt{}.jpg'.format(outpath,imgname,index),crop_img) # outputs jpg
#             index += 1

# def main(path): # changed argv into path
#     # path = ""
#     # path = argv
#     # for i in range(1, len(sys.argv)):
#         # path += sys.argv[i] + " "
#     # path = path[0:len(path)-1]
#     for x in os.listdir(path): 
#         imgpath = f'{path}/{x}'
#         print(imgpath)
#         if  x.endswith(".jpg") or x.endswith(".png"):
#             outpath = r'{}-sliced'.format(path)
#             if not os.path.exists(outpath):
#                 os.mkdir(outpath)
#             split_image(outpath, imgpath, x)
#     print("Finished!")

# # main(0) # to run, type: > python3 image_shredder.py [folder-path]

