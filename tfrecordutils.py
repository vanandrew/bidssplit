#!/usr/bin/env python3

import os
import argparse
import nibabel as nib
import tensorflow as tf

# Define tf Example serializer for brain data
def serialize_brain_data(t1,t2,mask,shape):
    """
        Saves data as tf.Example format
    """
    # create a dict of features to pass into tf Features 
    feature_dict = {
        't1': tf.train.Feature(bytes_list=tf.train.BytesList(value=[t1])),
        't2': tf.train.Feature(bytes_list=tf.train.BytesList(value=[t2])),
        'mask': tf.train.Feature(bytes_list=tf.train.BytesList(value=[mask])),
        'shape': tf.train.Feature(int64_list=tf.train.Int64List(value=shape))
    }
    # create example from features
    example = tf.train.Example(features=tf.train.Features(feature=feature_dict))
    return example.SerializeToString()

# write tfrecord
def write_tfrecord(outputfile, T1list, T2list, masklist):
    with tf.io.TFRecordWriter(outputfile,"ZLIB") as writer:
        for t1,t2,mask in zip(T1list,T2list,masklist):
            print(t1)
            print(t2)
            print(mask)
            # load t1,t2 and mask
            t1data = nib.load(t1)
            t2data = nib.load(t2)
            maskdata = nib.load(mask)

            # serialize subject to write to tfrecord
            subject_example = serialize_brain_data(
                t1data.get_data().ravel().tobytes(), # saves as float32 bytes
                t2data.get_data().ravel().tobytes(), # saves as float32 bytes
                maskdata.get_data().ravel().tobytes(), # saves as float32 bytes
                t1data.shape # saves as int64
            )

            # write to tfrecord
            writer.write(subject_example)

# define the parsing function for tfrecord
def parse_img_function(example):
    return tf.io.parse_single_example(example, {
        't1': tf.io.FixedLenFeature([], tf.string),
        't2': tf.io.FixedLenFeature([], tf.string),
        'mask': tf.io.FixedLenFeature([], tf.string),
        'shape': tf.io.FixedLenFeature([3], tf.int64)
    })

# read tfrecord
def read_tfrecord(tfrecord_file):
    raw_tfrecord = tf.data.TFRecordDataset(tfrecord_file, "ZLIB")
    parsed_image_dataset = raw_tfrecord.map(parse_img_function,4)
    return parsed_image_dataset
