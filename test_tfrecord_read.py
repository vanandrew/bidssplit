#!/usr/bin/env python3

from tfrecordutils import read_tfrecord

test = read_tfrecord("/home/vanandrew/Data/hbcd_test.tfrecords")
shape_data = test.map(lambda x: x['shape'])
batched = shape_data.batch(4)

for s in batched:
    print(s)
    