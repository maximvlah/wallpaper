'''
    Download wallpapers in the desired resolution from the wallpaperscraft.com
'''

import os
from selenium import webdriver

def scrape(category,resolution):

    #get url
    url = f'https://wallpaperscraft.com/catalog/{category}/{resolution}'

    # wallpapers__link
    pass


def main():
    category = 'nature'
    resolution = '1920x1080'



driver = webdriver.Firefox()
print('hey')