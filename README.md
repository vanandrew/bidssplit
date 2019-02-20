# bidssplit
A simple script for converting 3D volumes into 2D slices. It expects that the data is stored as a BIDS dataset.

```
usage: bidssplit.py [-h] [-o {T,S,C}] [-e EXCLUDE]
                    bids_directory output_directory

Splits T1w volumes in a BIDS dataset to 2D. Useful for Deep Learning
Applications.

positional arguments:
  bids_directory        Path to BIDS directory to process
  output_directory      Path to dump image outputs

optional arguments:
  -h, --help            show this help message and exit
  -o {T,S,C}, --orientation {T,S,C}
                        Orientation of output images. Can be T (Transverse), S
                        (Sagittal), or C (Coronal). Default is T.
  -e EXCLUDE, --exclude EXCLUDE
                        Text file with list of subjects to exclude
```
