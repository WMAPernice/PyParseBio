import os
import time
import logging
import argparse
from tqdm import tqdm
from multiprocessing.pool import Pool
from nd2reader import ND2Reader
from PPB_utils import *

def ParseMultiPoint(pid, in_path, out_path, start, end, channels=None, zproject=None, size=None, itpl=3, to_dtype='uint8', in_range='image',
                       wishdict={}):

    with ND2Reader(in_path) as images:
        images.bundle_axes = 'zcyx'
        images.iter_axes = 'v'

        # compile additional metadata:     
        res = 1/images.metadata['pixel_microns']
        addMeta = get_addmeta(images, wishdict)

        # process series:
        try:
            for v, im in enumerate(tqdm(images[start:end], total = len(images[start:end]), unit='files', postfix=pid)):
                
                # Nikon Elements allows skipping frames during acquisition, e.g. by collecting every 2nd timepoint for one of multiple channels.
                # nd2reader handles these "gap" frames by filling an array of corresponding width and height with np.nan. Since any arithmetic 
                # with nan-type will convert data to nan, nan-values are converted to zeros aka. a black image. 
                if np.isnan(im).any(): 
                    im = np.nan_to_num(im)

                # Optional channel selection/re-ordering:
                if channels: 
                    im = selectch(im, channels)
                
                # Optional zproject:
                if zproject:
                    im = projectz(im, zproject)

                # Optional resize:
                if size[0]:
                    im = resize(im, size, itpl)
                    
                # Potential dtype conversion:
                # TODO: Internal min/max rescaling eliminates absolute intensity differences between images, yet non-linear effects (signal/noise) 
                # remain preserved. Rescaling with internal min/max also ensure max preservation of precision; instead, for low-contrast 
                # images, rescaling with e.g. uint16 dtype values followed by conversion to uint8 can lead to massive loss in precision!!
                if to_dtype != str(im.dtype):
                    if zproject:
                        im = dtype_conversion(im[None,...], to_dtype, in_range=in_range, forcecopy=False)
                        im = im[0]
                    else:
                        im = dtype_conversion(im[None,...], to_dtype, in_range=in_range, forcecopy=False)

                # Saving:
                fpath = f"{out_path}_{str(start + v).zfill(3)}.tiff"
                savetiff(im, fpath, res, addMeta)
        except: logging.exception('Exception occured: ')            

if __name__ == '__main__':

    # parameters:
    parser = argparse.ArgumentParser()

    class handledict(argparse.Action):
        def __call__(self, parser, namespace, instring, option_string=None):
            my_dict = {}
            for keyval in instring.split(","):
                print(keyval)
                key,val = keyval.split(":")
                my_dict[key] = val
            setattr(namespace, self.dest, my_dict)

    parser.add_argument('indir', type=str, help='Specify path to input directory')
    parser.add_argument('outdir', type=str, help='Specify path output directory')
    parser.add_argument('-c', '--channels', type=int, nargs='*', default=None, help='list channels to be extracted and their output order, e.g.: 1 2 0 3')
    parser.add_argument('-z', '--zproject', type=str, default=None, help='provide string to specify mode of z-projection, e.g. max_project') #TODO: add options
    parser.add_argument('-s', '--size', type=int, nargs='*', default=None, help='provide tuple of target dimensions for output images, e.g. (512,512)')
    parser.add_argument('-i', '--itpl', type=int, default=3, help='provide int [0-5] to specify mode of interpolation to be used in resize (default: 3 -> bicubic)')
    parser.add_argument('-d', '--dtype', type=str, default='uint8', help='provide string specifying the desired dtype of output images (default: uint8)')
    parser.add_argument('-scl','--scale', type=str, nargs='*', default='image', help='provide string specifying how min/max in skimage.exposure.rescale_intensity() are calculated (default: image). Can specify min/max values, e.g. for 12bit: 0 4096')
    parser.add_argument('-wd', '--wishdict', default={}, action=handledict, help='provide key1:value1,key2:value2,... to try to extract metadata items from the image according to values.')
    parser.add_argument('-t', '--tag', type=str, default=None, help='specify additional string to be added to output filenames (default: None)')
    parser.add_argument('-r', '--range', type=int, nargs='*', default=None, help='provide list [L1,L2] to limit which multipoints to process (default: None)')
    parser.add_argument('-w', '--workers', type=int, default=1, help='specify number of workers (default: 1)')
    params = parser.parse_args()

    if not os.path.exists(params.outdir): os.mkdir(params.outdir)

    flist = [params.indir + f for f in os.listdir(params.indir) if f.split('.')[-1] == 'nd2']
    for ND2file in flist:
        t00 = time.time()
        # setup list_len and naming:
        x = ND2Reader(ND2file)
        with ND2Reader(ND2file) as images:
            images.bundle_axes = 'zcyx'
            images.iter_axes = 'v'
            list_len = len(images)
            if params.range: 
                L1, L2 = params.range
                assert L1 < list_len and L2 <= list_len, f'Range out of bounds. Only {list_len} images in {ND2file}'
                list_len = L2 - L1
            else: L1 = 0
                
            # TODO: make this call a function:
            # fn = images.filename.split('/')[-1]
            fn = os.path.basename(images.filename)
            assert len(fn.split('_')) == 3, \
            'Please name your files according to: [yyyy-m-d_Plate-de-script-tion_Idx.nd2]'
            fn = fn.split('.')
            if len(fn)>2: fn = ".".join(fn[:-1])
            else: fn = fn[0]
            out_path = params.outdir + fn
            
        
        # Multiprocess setup. 
        # Will never use more cores than images to be extracted.
        process_num = np.min([params.workers, list_len])

        print('-------------------')
        print(f"Starting image extraction for: {ND2file}")
        print(f"Total images to be extracted {list_len}")
        print(f"Workers: {process_num}")
        print('Parent process %s.' % os.getpid())
        print(f"Output directory: {out_path}")
        print('-------------------')
        p = Pool(process_num)
        for i in range(process_num):
            start = int(L1 + (i * list_len / process_num))
            end = int(L1 + ((i + 1) * list_len / process_num))
            p.apply_async(
                ParseMultiPoint, args=(str(i), ND2file, out_path, start, end,
                params.channels, 
                params.zproject, 
                tuple(params.size),
                params.itpl,
                params.dtype,
                params.scale,
                params.wishdict
                )
            )

        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
        print('All subprocesses done.')
        print(f"Total execution time: {time.time() - t00}")
        print(f"Time-per-image: {(time.time() - t00)/list_len}")

