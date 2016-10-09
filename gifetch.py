#!/user/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import argparse
import urllib
from bs4 import BeautifulSoup


def main():

    sizes  = ['all', 'small', 'medium', 'large', 'xlarge']
    types  = ['photo', 'clipart', 'lineart', 'anim']
    face   = ['closeup', 'portrait']
    ftypes = ['jpg', 'png', 'gif', 'tiff', 'bmp', 'svg']

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
    p.add_argument('--ftypes', '-T',
                   choices=ftypes,
                   default=ftypes,
                   nargs='*',
                   metavar='',
                   help='(optional) limit to image file types. Values: ' + ', '.join(ftypes))

    args = p.parse_args()
    if not os.path.isdir(args.path):
        sys.exit('Invalid Path.')
    dirs = [d for d in next(os.walk(args.path))[1] if not d.startswith('.')]
    if not dirs:
        sys.exit('No subfolders. Add one subfolder for each image query')


    fetcher = ImageFetcher(args)
    for query in dirs:
        urls = fetcher.collect_urls(query)
        fetcher.store_images(urls,query)



def progress(count, total):
     bar_w = 40
     filled = round(bar_w * float(count) / total)
     bar = '█' * filled + '-' * (bar_w-filled)
     sys.stdout.write('\r▏{} ▏ {}/{} '.format(bar,count,total))
     if count == total: sys.stdout.write('\n')
     sys.stdout.flush()

def file_from_url(url):
    return urllib.parse.urlparse(url)[2].rpartition('/')[2]

def ftype_from_url(url):
    return file_from_url(url).rpartition('.')[2]


class ImageFetcher:
    def __init__(self, args):
        self.args = self.set_query_params(args)

    def collect_urls(self, query):
        urls = []
        print('Collecting img urls...')
        query_string = 'https://www.bing.com/images/search?&q={}&qft={}{}{}'
        query_string = query_string.format(query.replace(' ','+'), self.args.size, self.args.type, self.args.face)

        first = 1
        count = 28
        query_string += '&first={}&count=' + str(count)

        while len(urls) < self.args.n + 10:
            query_url = query_string.format(first)

            req = urllib.request.Request(query_url, headers={'User-Agent' : "gifetch"})
            res = urllib.request.urlopen(req)
            html = res.read()
            soup = BeautifulSoup(html, 'lxml')
            imgs = soup.select('a[class=thumb]')

            for i in imgs:
                url = i['href']
                if not url in urls and \
                    ftype_from_url(url) in self.args.ftypes:
                    urls.append(i['href'])

            first += count
        # urls = urls[0:self.args.n]
        return urls

    def store_images(self, urls, dir):
        print('Downloading images for ' + dir)
        i = 1
        n = self.args.n
        for url in urls:
            filename = file_from_url(url)
            filename = self.args.path + '/' + dir + '/' + filename
            # print(url)
            try:
                req = urllib.request.Request(url, headers={'User-Agent': "gifetch"})
                res = urllib.request.urlopen(req)
            except urllib.error.HTTPError as err:
                print(err)
            except:
                print("Error storing image")
            else:
                while os.path.isfile(filename):
                    parts = filename.rpartition('.')
                    filename = parts[0] + '_' + ''.join(parts[1:])

                out = open(filename, 'wb')
                out.write(res.read())
                out.close()
                i += 1
                print(filename)

            if i > n: break
            # progress(i, n)


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




