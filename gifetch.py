#!/user/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import urllib
from bs4 import BeautifulSoup


def main():

    sizes = ['l', 'm', 'i', 'qsvga', 'vga', 'svga', 'xga', '2mp', '4mp', '8mp', '10mp']
    types = ['face', 'photo', 'clip', 'line', 'anim']

    p = argparse.ArgumentParser(description='Batch downloads a set amount of images in seperate subfolders matching the Google Image search query of each folder name.')
    p.add_argument('path',
                   default=os.getcwd(),
                   nargs='?',
                   help='absolute path to directory with image folders. defaults to working directory')
    p.add_argument('-n',
                   default=10,
                   type=int,
                   help='number of images to download in each directory')
    p.add_argument('--size', '-s',
                   choices=sizes,
                   default='m',
                   nargs='?',
                   metavar='s',
                   help='(optional) minimum image size. Values: ' + ', '.join(sizes) + '. defaults to m'
                   )
    p.add_argument('--type', '-t',
                   choices=types,
                   default='',
                   nargs='?',
                   metavar='t',
                   help='(optional) image type. Values: ' + ', '.join(types) + ' (optional)')

    args = p.parse_args()
    # print(args)
    if not os.path.isdir(args.path):
        sys.exit('Invalid Path.')
    dirs = [d for d in next(os.walk(args.path))[1] if not d.startswith('.')]
    if not dirs:
        sys.exit('No subfolders. Add one subfolder for each image query')

    fetcher = ImageFetcher(args)
    for query in dirs:
        urls = fetcher.collect_urls(query)
        # print(urls)
        # fetcher.store_images(urls,query)


class ImageFetcher:
    def __init__(self, args):
        self.args = args

    def collect_urls(self, query):
        urls = []
        query_string = 'https://www.google.de/search?q={}&tbm=isch&tbs=isz:{},itp:{}'
        query_string = query_string.format(query.replace(' ','+'), self.args.size, self.args.type)

        response = urllib.request.urlopen(query_string)
        return urls

    def store_images(self, urls, dir):
        pass



if __name__ == '__main__':
    main()




