# !/usr/bin/python3
# coding: utf-8

# Copyright 2015-2018
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#TODO use pytesseract wrapper for future flexibility

import os
import sys
import cv2

from PIL import Image
from send2trash import send2trash

from parser.parser import read_config

config = read_config()



BASE_PATH = os.getcwd()
IMAGES_PATH = config.get('images_path', "data/img")
RECEIPTS_PATH = config.get('receipts_path', "data/txt")
INPUT_FOLDER = os.path.join(BASE_PATH, IMAGES_PATH)
TMP_FOLDER = os.path.join(BASE_PATH, "data/tmp")

OUTPUT_FOLDER = os.path.join(BASE_PATH, RECEIPTS_PATH)
LANGUAGE = config.get("language", "deu")

print(IMAGES_PATH)
print(RECEIPTS_PATH)

def prepare_folders():
    """
    :return: void
        Creates necessary folders
    """

    for folder in [
        INPUT_FOLDER, TMP_FOLDER, OUTPUT_FOLDER
    ]:
        if not os.path.exists(folder):
            os.makedirs(folder)


def find_images(folder):
    """
    :param folder: str
        Path to folder to search
    :return: generator of str
        List of images in folder
    """

    for file in os.listdir(folder):
        full_path = os.path.join(folder, file)
        if os.path.isfile(full_path):
            try:
                _ = Image.open(full_path)  # if constructor succeeds
                yield file
            except:
                pass


def rotate_image(input_file, output_file, angle=90):
    """
    :param input_file: str
        Path to image to rotate
    :param output_file: str
        Path to output image
    :param angle: float
        Angle to rotate
    :return: void
        Rotates image and saves result
    """

    cmd = "convert -rotate " + "' " + str(angle) + "' "
    cmd += "'" + input_file + "' '" + output_file + "'"
    print("Running", cmd)
    os.system(cmd)  # sharpen

    return output_file

def convert_b_w(input_file, output_file):
    print('Converting Image to Black and White + Removing Noise')
    # load the example image and convert it to grayscale
    image = cv2.imread(input_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Apply threshold
    gray = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    #Apply Blur
    gray = cv2.medianBlur(gray, 3)

    # Write image to output
    cv2.imwrite(output_file, gray)

    return output_file

def sharpen_image(input_file, output_file):
    """
    :param input_file: str
        Path to image to prettify
    :param output_file: str
        Path to output image
    :return: void
        Prettifies image and saves result
    """
    
    cmd = "convert -auto-level -sharpen 0x4.0 -contrast "
    cmd += "'" + input_file + "' '" + output_file + "'"
    print("Running", cmd)
    os.system(cmd)  # sharpen

    return output_file

def deskew_image(input_file, output_file):

    cmd = "convert -deskew 80% "
    cmd += "'" + input_file + "' '" + output_file + "'"
    print("Running", cmd)
    os.system(cmd)  # sharpen

    return output_file


def run_tesseract(input_file, output_file):
    """
    :param input_file: str
        Path to image to OCR
    :param output_file: str
        Path to output file
    :return: void
        Runs tesseract on image and saves result
    """

    cmd = f"tesseract -l {LANGUAGE} "
    cmd += "'" + input_file + "' '" + output_file + "'"
    print("Running", cmd)
    os.system(cmd)


def main(params):
    prepare_folders()
    images = list(find_images(INPUT_FOLDER))
    print("Found the following images in", INPUT_FOLDER)
    print(images)

    for image in images:
        input_path = os.path.join(
            INPUT_FOLDER,
            image
        )
        tmp_path = os.path.join(
            TMP_FOLDER,
            image
        )
        out_path = os.path.join(
            OUTPUT_FOLDER,
            image + ".out.txt"
        )
        # Controll OCR via parameters
        # Optimized getting parameter values using a generator

        print(f"Input is {input_path}")

        for p in (x for x in params):
            if 'rotate' in p:
                angle = int(p.replace('rotate-', ''))# Parse the command i.e rotate-90
                input_path = rotate_image(input_path, tmp_path, angle)  # rotate
                # We break so if there are unlimited parameters we stop looping
                # since we are only expecting the rotate params for now
                break
            
        input_path = sharpen_image(input_path, tmp_path)   # sharpen images
        input_path = convert_b_w(input_path, tmp_path)
        input_path = deskew_image(input_path, tmp_path)   # deskew image
        run_tesseract(tmp_path, out_path)

    print("Removing tmp folder")
    # send2trash(TMP_FOLDER)


if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)
