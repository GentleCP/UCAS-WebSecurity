#coding:utf-8
from captcha.image import ImageCaptcha
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
import string
#from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import os
characters = string.digits #+ string.ascii_uppercase

width, height, n_len, n_class = 100, 50, 4, len(characters)

def create_captcha(random_str):
    generator = ImageCaptcha(width=width, height=height)
    img = generator.generate_image(random_str)
    #print(type(img))
    return img

def create_captcha_set():
    for n in range(1):
        random_str = ''.join([random.choice(characters) for j in range(4)])
        #random_str = [random.choice(characters) for j in range(4)]
        img = create_captcha(random_str)
        title = ''
        for i in random_str:
            title = title + i
        #title = title[1:]
        #plt.axis('off')
        #print(title)
        #plt.imshow(img)
        #plt.savefig("./img/"+str(title)+".png")
        dirname = 'static/images'
        img.save("./"+dirname+"/"+'captcha'+".png")
    return img,str(title)