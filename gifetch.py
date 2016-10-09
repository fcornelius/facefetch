#!/user/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import urllib.request
from bs4 import BeautifulSoup


def main():

    sizes = ['all', 'small', 'medium', 'large', 'xlarge']
    types = ['photo', 'clipart', 'lineart', 'anim']
    face  = ['closeup', 'portrait']

    p = argparse.ArgumentParser(description='Batch downloads a set amount of images in seperate subfolders matching the Bing Image search query of each folder name.')
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
                   default='medium',
                   nargs='?',
                   metavar='s',
                   help='(optional) minimum image size. Values: ' + ', '.join(sizes) + '. defaults to medium'
                   )
    p.add_argument('--type', '-t',
                   choices=types,
                   default='',
                   nargs='?',
                   metavar='t',
                   help='(optional) image type. Values: ' + ', '.join(types))
    p.add_argument('--face', '-f',
                   choices=face,
                   default='',
                   nargs='?',
                   metavar='f',
                   help='(optional) images with faces. Values: ' + ', '.join(face))

    args = p.parse_args()
    # print(args)
    if not os.path.isdir(args.path):
        sys.exit('Invalid Path.')
    dirs = [d for d in next(os.walk(args.path))[1] if not d.startswith('.')]
    if not dirs:
        sys.exit('No subfolders. Add one subfolder for each image query')

    # Size query params

    fetcher = ImageFetcher(args)
    for query in dirs:
        urls = fetcher.collect_urls(query)
        # print(urls)
        # fetcher.store_images(urls,query)





class ImageFetcher:
    def __init__(self, args):
        self.args = self.set_query_params(args)

    def collect_urls(self, query):
        urls = []
        query_string = 'https://www.bing.com/images/search?&q={}&qft={}{}{}'
        query_string = query_string.format(query.replace(' ','+'), self.args.size, self.args.type, self.args.face)

        req = urllib.request.Request(query_string, headers={'User-Agent' : "gifetch"})
        res = urllib.request.urlopen(req)
        html = res.read()
        soup = BeautifulSoup(html, 'lxml')
        imgs = soup.select('a[class=thumb]')

        for i in range(1, self.args.n):
            url = img[i]['href']



    def store_images(self, urls, dir):
        pass

    @staticmethod
    def set_query_params(args):
        if args.size == 'all':
            args.size = 'wallpaper'
        args.size = '+filterui:imagesize-' + args.size
        if args.size == 'all': args.size = ''

        if args.type == 'lineart':
            args.type = 'linedrawing'
        elif args.type == 'anim':
            args.type = 'animatedgif'
        if args.type:
            args.type = '+filterui:photo-' + args.type

        if args.face == 'closeup':
            args.face = 'face'
        if args.face:
            args.face = '+filterui:face-' + args.face

        return args


if __name__ == '__main__':
    main()




