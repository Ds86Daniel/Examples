# -*- coding: utf.
"""
Created on Wed Oct 25 21:19:59 2023

@author: Sanchez-Cisneros
"""

import cv2
import numpy as np
import requests
import os
import platform
import json
import random

#PIXABAY_API_KEY = "40280608-389a5d543efd52fde398d205d"


PIXABAY_API_KEY = '40280608-389a5d543efd52fde398d205d' # Replace with your Pixabay API key

def cartoonify_image(img_array):
    # Convert to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    
    # Apply median filter
    gray = cv2.medianBlur(gray, 5)

    # Detect edges using Laplacian and threshold
    edges = cv2.Laplacian(gray, cv2.CV_8U, ksize=5)
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)

    # Apply bilateral filter multiple times (cartoon effect)
    for _ in range(4):
        img_array = cv2.bilateralFilter(img_array, 9, 75, 75)

    # Convert back to color and bitwise the mask and image
    cartoon = cv2.bitwise_and(img_array, img_array, mask=mask)

    return cartoon

def fetch_and_cartoonify(output_path_prefix, num_images=7):
    query = "america+sunset"

    # Randomly select a page number between 1 and 37 (or any desired range)
    page_num = random.randint(1, 25)

    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page={num_images}&page={page_num}"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    if not data['hits']:
        print("No images found for the query.")
        return

    # Randomly select `num_images` distinct images from the fetched set
    selected_images = random.sample(data["hits"], num_images)

    for idx, random_image in enumerate(selected_images, 1):
        image_url = random_image["largeImageURL"]

        # Fetch the image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # Convert to numpy array for OpenCV
        img_array = np.asarray(bytearray(response.content), dtype="uint8")
        img_array = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Cartoonify the image
        cartoon = cartoonify_image(img_array)

        # Save the cartoon image with an index (like cartoonified_image_1.jpg, cartoonified_image_2.jpg, ...)
        output_path = f"{output_path_prefix}_{idx}.jpg"
        cv2.imwrite(output_path, cartoon)
        
        print("Image saved as", output_path)
        open_image(output_path)

def open_image(output_path):
    system_name = platform.system()
    if system_name == "Windows":
        os.system(f'start {output_path}')
    elif system_name == "Darwin":
        os.system(f'open {output_path}')
    elif system_name == "Linux":
        os.system(f'xdg-open {output_path}')
    else:
        print(f"Sorry, we don't support automatically opening files on {system_name}")

# Running the main function
fetch_and_cartoonify("cartoonified_image.jpg")


