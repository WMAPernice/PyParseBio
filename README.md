# MultiParseND2
Pure python scripts to extract and process images from multipoint ND2-files in a parallelized fashion.

## Installation: 

To install, clone this repo - PIP upload remains on TODO. 

## Usage:

```
usage: ND2tif.py [-h] [-c [CHANNELS [CHANNELS ...]]] [-z ZPROJECT]
                 [-s [SIZE [SIZE ...]]] [-i ITPL] [-d DTYPE] [-wd WISHDICT]
                 [-t TAG] [-r [RANGE [RANGE ...]]] [-w WORKERS]
                 ND2file outdir
```
```
positional arguments:
  ND2file               Specify path to multipoint .nd2 file
  outdir                Specify path output directory

optional arguments:
  -h, --help            show this help message and exit
  -c [CHANNELS [CHANNELS ...]], --channels [CHANNELS [CHANNELS ...]]
                        provide list to specify channels to be extracted
                        and/or reorder them, e.g. [1,2,0,3]
  -z ZPROJECT, --zproject ZPROJECT
                        provide string to specify mode of z-projection, e.g.
                        max_project
  -s [SIZE [SIZE ...]], --size [SIZE [SIZE ...]]
                        provide tuple of target dimensions for output images,
                        e.g. (512,512)
  -i ITPL, --itpl ITPL  provide int [0-5] to specify mode of interpolation to
                        be used in resize (default: 3 -> bicubic)
  -d DTYPE, --dtype DTYPE
                        provide string specifying the desired dtype of output
                        images (default: uint8)
  -wd WISHDICT, --wishdict WISHDICT
                        provide key1:value1,key2:value2,... to try to extract
                        metadata items from the image according to values.
  -t TAG, --tag TAG     specify additional string to be added to output
                        filenames (default: None)
  -r [RANGE [RANGE ...]], --range [RANGE [RANGE ...]]
                        provide list [L1,L2] to limit which multipoints to
                        process (default: None)
  -w WORKERS, --workers WORKERS
                        specify number of workers (default: 1)
```
