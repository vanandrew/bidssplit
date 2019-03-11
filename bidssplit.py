#!/usr/bin/env python3
import os
import argparse
import numpy as np
import nibabel as nib
from bids import BIDSLayout
from imageio import imwrite

def main(args):
    # make the output directory path if it already does not exist
    try:
        print('Making output directory: {}'.format(args.output_directory))
        os.makedirs(args.output_directory)
    except OSError:
        print('Directory already exists. Continuing...')

    # Create the layout object
    print('Loading BIDS Directory...')
    layout = BIDSLayout(args.bids_directory)
    print(layout)

    # Get T1w images only
    files = layout.get(suffix='T1w')

    # Get list of subjects to exclude if set
    if 'exclude' in vars(args):
        # make exclude list
        exclude_list = []
        # read in exclude list
        with open(vars(args)['exclude'],'r') as f:
            for line in f:
                exclude_list.append(line.rstrip())

    # loop over each file
    for f in files:
        print('Processing {}...'.format(f.filename))

        # Force RAS+ orientation
        img = nib.as_closest_canonical(f.image) # Pybids already loads the nibabel image as the .image atribute

        # get subject and orientation to make images
        subject = f.entities['subject']
        run = f.entities['run']
        orient_code = {'S': 0, 'C': 1, 'T': 2}[args.orientation]

        # Check if subject in exclude list
        if subject in exclude_list:
            print('sub-{} is in exclude list. Skipping...'.format(subject))
            # skip if in exclude list
            continue

        # get volume data
        data = img.get_fdata()
        dims = data.shape

        # scale 12-bit data to fill 16-bit container
        data = np.round((data/4095)*65535)

        # write images to disk
        for n in range(dims[orient_code]):
            imwrite(
                os.path.join(args.output_directory, 'sub-{}_run-{}_slice-{}.tif'.format(subject, run, n)),
                np.pad( # pad to 512 x 512 (TODO: Dynamically set this value based on image)
                    np.flip(simple_slice(data,n,orient_code).T.astype('uint16'), axis=0), # Flip for proper orientation
                    ((96,96),(128,128)), # Images in HCP are 320 x 256. We pad to 512 x 512
                    'constant' # Pad with 0 values
                    )
                )

def simple_slice(arr, inds, axis):
    # this does the same as np.take() except only supports simple slicing, not
    # advanced indexing, and thus is much faster
    sl = [slice(None)] * arr.ndim
    sl[axis] = inds
    return arr[tuple(sl)]

if __name__ == '__main__':
    # Create command line parser
    parser = argparse.ArgumentParser(description='Splits T1w volumes in a BIDS dataset to 2D. \
        Useful for Deep Learning Applications.')
    parser.add_argument('bids_directory', help='Path to BIDS directory to process')
    parser.add_argument('output_directory', help='Path to dump image outputs')
    parser.add_argument('-o', '--orientation', choices=['T', 'S', 'C'], default='T',
        help='Orientation of output images. Can be T (Transverse), S (Sagittal), or C (Coronal). Default is T.')
    parser.add_argument('-e', '--exclude', help='Text file with list of subjects to exclude')

    # parse the arguments
    args = parser.parse_args()

    # Pass parameters to main
    main(args)
