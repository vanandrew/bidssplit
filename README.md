# neurosplitter

#### Installation

`git clone` the repo, then install the dependencies in `requirements.txt`. Will probably work on a `pip`
package in the near future...

#### Usage:

```
usage: neurosplitter [-h] [-i BIDS_DIRECTORY] [-o OUTPUT_DIRECTORY]
                     [--input_image INPUT_IMAGE]
                     [--output_prefix OUTPUT_PREFIX] [-r {T,S,C}] [-s SUFFIX]
                     [-e EXCLUDE] [-c COMPOSE] [--scale SCALE]

Splits volumes in a dataset to 2D. Useful for Deep Learning Applications.

optional arguments:
  -h, --help            show this help message and exit
  -i BIDS_DIRECTORY, --bids_directory BIDS_DIRECTORY
                        BIDS mode. Path to BIDS directory to process.
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Path to dump image outputs. Used with bids_directory
                        flag.
  --input_image INPUT_IMAGE
                        Single image mode. Use this if you want to process a
                        single image, or non-BIDS data.
  --output_prefix OUTPUT_PREFIX
                        Output prefix of single image. Used with input_image
                        flag.
  -r {T,S,C}, --orientation {T,S,C}
                        Orientation of output images (Volume is forced to RAS+
                        orientation on load). Can be T (Transverse), S
                        (Sagittal), or C (Coronal). Default is T.
  -s SUFFIX, --suffix SUFFIX
                        BIDS mode. BIDS file suffix to process.
  -e EXCLUDE, --exclude EXCLUDE
                        Text file with list of subjects to exclude. Just the
                        subject id (no sub-). BIDS mode only
  -c COMPOSE, --compose COMPOSE
                        Composes nifti volume from slice directory.
  --scale SCALE         Data scale for write. Default is 4095.
```

#### Examples:

```
  # Generates slices at path/to/output
  neurosplitter --input_image /path/to/example.nii.gz --output_prefix path/to/output/example --scale 100
```

```
  # Composes nifti volume from slices
  neurosplitter -c /path/to/slices -r T # Make sure orientation is set to the same as the slice decomposition!
```