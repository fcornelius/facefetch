#!/user/bin/env python3
# -*- coding: utf-8 -*-

import argparse


def main():

    sizes = ['l', 'm', 'i', 'qsvga', 'vga', 'svga', 'xga', '2mp', '4mp', '8mp', '10mp']
    types = ['face', 'photo', 'clip', 'line', 'anim']

    p = argparse.ArgumentParser(description='Batch downloads a set amount of images in seperate subfolders matching the Google Image search query of each folder name.')
    p.add_argument('path',
                   default='',
                   help='path to directory with image folders')
    p.add_argument('-n',
                   default=10,
                   type=int,
                   help='number of images to download in each directory')
    p.add_argument('--size', '-s',
                   choices=sizes,
                   default='m',
                   help='minimum image size. Values: ' + ', '.join(sizes),
                   metavar='')
    p.add_argument('--type', '-t',
                   choices=types,
                   default='',
                   help='image type. Values: ' + ', '.join(sizes),
                   metavar='')
    args = p.parse_args()
    print(args)



def print_usage():
    print("")

if __name__ == '__main__':
    main()




