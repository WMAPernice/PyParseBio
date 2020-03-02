![PPB icon](https://github.com/WMAPernice/PyParseBio/blob/master/PPB_Logo_v1.0.png)

# PyParseBio
Simple and fast pure-python scripts to extract and process images from multipoint microscopy-files in a parallelized fashion. Extracts and converts images from e.g. ND2 multipoint files to tiffs through various preprocessing steps, e.g. to prepare machine-learning projects. PPB consistently runs at up to 20x the speed of FIJI and 3-4x the speed of parallelized CellProfiler in headless mode. Point it at a folder of multipoint files and have PPB blaze through them :rocket: 

Intergrated features:  
- data-type conversions
- resizing
- z-projections
- channel extraction and re-ordering
- metadata extraction and derivation

Note: currently only works with Nikon Elements ND2 files with .tiff stacks as outputs.

## Example & Benchmark: 
You can download an example ND2 (Nikon Elements) file here: https://nd2tiff.s3-us-west-2.amazonaws.com/2019-9-5_11-Multi-point-test-image_001.zip

The file contains 11 image-stacks (collected at different XYZ coordinates of a multiwell plate), each consisting of 7-z slices and 5-channels. Run the following to extract the 11 multipoints as individual max-projected images, containing only 4/5 channels in a custom order, resized to 512x512 and converted from 12- to 8-bit tiff-files, parallelizing the work over 6 cores:
```
python -W ignore [PATH/TO/PACKAGE/]PPB.py [input/path/] [output/path/] -c 1 2 0 3 -z max_project -s 512 512 -d uint8 -w 6
```
The following benchmark results of PyParseBio (PPB) against CellProfiler were created using the exact 11-multipoint ND2 file provided in the download link above, as well as another 43-multipoint ND2 file with the same dimensions. 

![PPB Benchmark vs CP](https://github.com/WMAPernice/PyParseBio/blob/master/PPB_Benchmark_v1.0.png)

To recapitulate these results yourself, you can find the relevant CellProfiler pipeline and scripts for running CP in headless mode in the PPB_benchmarks folder of this repo. 

## Installation: 

### PIP:
```
pip install PyParseBio
```
### Anaconda:
TODO
### Dev installation:
Clone this repo 

## Usage:

```
usage:    PPB.py [-h] [-c [CHANNELS [CHANNELS ...]]] [-z ZPROJECT]
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
## Acknowledgments: 
- Broad Institute of MIT/Harvard (Carpenter lab)
- Columbia University (Hirano lab)
