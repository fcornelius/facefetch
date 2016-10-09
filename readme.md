# facefetch

Batch downloads a set of images matching specified criteria off Bing Images and organizes each set in subfolders.
Although this was originally used to gather training data for a face recognizer it can be utilized to accumulate any kind of image clusters.


#### Dependencies
facefetch is written in Python3 and requires [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) for html parsing

```bash
pip install beautifulsoup4
```

#### Sample usage

```bash
git clone https://github.com/phoelix/facefetch.git
cd facefetch
mkdir 'Bud Spencer' && mkdir 'Terrence Hill'
./ffetch -n 10 --size large --face closeup --ftypes jpg --rename {dir}_{:02d}
```

This would fill each folder with 10 jpgs of large face closeups, with file naming format budspencer_01.jpg, budspencer_02.jpg ...

##### Options

As ffetch takes the names of all subdirectories as search query input, the only required option is the number of images to download (`-n`) into each folder.

Positional Arguments:

```
path                  absolute path to directory with image folders.
                      defaults to working directory
```

Optional Arguments:

```bash
  -h, --help            show help message
  -n                    number of images to download in each directory
  --size, -s            minimum image size. Values: all, small,
                        medium, large, xlarge. defaults to medium
  --type, -t            image type. Values: photo, clipart,
                        lineart, anim
  --face, -f            images with faces. Values: closeup,portrait
  --ftypes, -T [[...]]  limit to image file types. Combination of: jpg,
                        png, gif, tiff, bmp, svg
  --rename, -F          specify format to rename image files.
                        Accepts python3 string formats, use {:d} for a running
                        number and {dir} for the subfolder name

```
#### Notes

+ ffetch will skip folders containing >= the specified amount of images to download, allowing it to resume batch downloading after abort
+ you will notice (in verbose mode) that some downloads fail due to HTTP 403/404/502... Errors. ffetch will collect an extra image for each failed download to make sure it always results in exactly n images in each subfolder.
