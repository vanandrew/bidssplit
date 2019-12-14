# neurosplitter

#### Installation

`git clone` the repo, then install the dependencies in `requirements.txt`. Will probably work on a `pip`
package in the near future...

#### Usage:

```
usage: neurosplitter [-h] {bids,single,compose} ...

Splits volumes in a dataset to 2D. Useful for Deep Learning Applications.

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {bids,single,compose}
                        Use the -h/--help flag on each subcommand for more help.
    bids                Splits an entire BIDS Dataset.
    single              Splits a Single Image.
    compose             Composes a volume from a folder of split images.
```

```
usage: neurosplitter bids [-h] [-s SUFFIX] [-n INCLUDE] [-e EXCLUDE] [--flat] [-r {T,S,C}] [-p WIDTH HEIGHT] [--scale SCALE] bids_directory output_directory

positional arguments:
  bids_directory        Path to BIDS directory to process.
  output_directory      Path to dump image outputs.

optional arguments:
  -h, --help            show this help message and exit
  -s SUFFIX, --suffix SUFFIX
                        BIDS file suffix to process.
  -n INCLUDE, --include INCLUDE
                        Text file with list of subjects to include. Just the subject id (no sub-).
  -e EXCLUDE, --exclude EXCLUDE
                        Text file with list of subjects to exclude. Just the subject id (no sub-).
  --flat                If used, write all images to the output directory directly without subfolders.
  -r {T,S,C}, --orientation {T,S,C}
                        Orientation of output images (Volume is forced to RAS+ orientation on load). Can be T (Transverse), S (Sagittal), or C (Coronal). Default is T.
  -p WIDTH HEIGHT, --pad_crop WIDTH HEIGHT
                        Specifies Width x Height to make each image. Will either center crop/pad image to reach desired dimensions.
  --scale SCALE         Data scale for write. Default is 4095.
```

```
usage: neurosplitter single [-h] [-r {T,S,C}] [-p WIDTH HEIGHT] [--scale SCALE] input_image output_prefix

positional arguments:
  input_image           Path to input image.
  output_prefix         Output prefix of split images.

optional arguments:
  -h, --help            show this help message and exit
  -r {T,S,C}, --orientation {T,S,C}
                        Orientation of output images (Volume is forced to RAS+ orientation on load). Can be T (Transverse), S (Sagittal), or C (Coronal). Default is T.
  -p WIDTH HEIGHT, --pad_crop WIDTH HEIGHT
                        Specifies Width x Height to make each image. Will either center crop/pad image to reach desired dimensions.
  --scale SCALE         Data scale for write. Default is 4095.
```

```
usage: neurosplitter compose [-h] [-a AFFINE] [-r {T,S,C}] [-p WIDTH HEIGHT] input_dir

positional arguments:
  input_dir             Composes nifti volume from slice directory.

optional arguments:
  -h, --help            show this help message and exit
  -a AFFINE, --affine AFFINE
                        Use affine information from specified nifti file. Uses eye(4) otherwise.
  -r {T,S,C}, --orientation {T,S,C}
                        Orientation of output images (Volume is forced to RAS+ orientation on load). Can be T (Transverse), S (Sagittal), or C (Coronal). Default is T.
  -p WIDTH HEIGHT, --pad_crop WIDTH HEIGHT
                        Specifies Width x Height to make each image. Will either center crop/pad image to reach desired dimensions.
```

#### Examples:

```
  # Generates slices at path/to/output
  neurosplitter single /path/to/example.nii.gz path/to/output/example --scale 100
```

```
  # Composes nifti volume from slices
  neurosplitter compose /path/to/slices -r T # Make sure orientation is set to the same as the slice decomposition!
```