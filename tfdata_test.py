#!/usr/bin/env python3

import os
import numpy as np
import nibabel as nib
import tensorflow as tf

# get list of T1s/T2s/masks
path = "/mnt/Daenerys/HBCD/organized_data/"
files = os.listdir(path)
T1list = sorted([i for i in files if "T1w.nii.gz" in i])
T2list = sorted([i for i in files if "T2w.nii.gz" in i])
masklist = sorted([i for i in files if "brainmask.nii.gz" in i])

# Define tf Example serializer for brain data
def serialize_brain_data(t1,t2,mask,shape):
    """
        Saves data as tf.Example format
    """
    # create a dict of features to pass into tf Features 
    feature_dict = {
        't1': tf.train.Feature( # makes a single feature
            bytes_list=tf.train.BytesList( # converts to tf Example bytes list
                value=[t1] # pass in the numpy bytes to the list
            )
        ),
        't2': tf.train.Feature(
            bytes_list=tf.train.BytesList(
                value=[t2]
            )
        ),
        'mask': tf.train.Feature(
            bytes_list=tf.train.BytesList(
                value=[mask]
            )
        ),
        'shape': tf.train.Feature(
            int64_list=tf.train.Int64List(
                value=shape
            )
        )
    }
    # create example from features
    example = tf.train.Example(features=tf.train.Features(feature=feature_dict))
    return example.SerializeToString()

# load files
T1s = list()
T2s = list()
masks = list()
tfrecords_path = "/mnt/Daenerys/HBCD/tfrecords/"
# write data to tfrecord
with tf.io.TFRecordWriter(tfrecords_path+"hbcd.tfrecords","ZLIB") as writer:
    for t1,t2,mask in zip(T1list,T2list,masklist):
        # load t1, t2, and mask
        print(t1)
        t1data = nib.load(path+t1)
        print(t2)
        t2data = nib.load(path+t2)
        print(mask)
        maskdata = nib.load(path+mask)

        # serialize subject to write to tfrecord
        subject = serialize_brain_data(
            t1data.get_data().ravel().tobytes(), # saves as float32 bytes
            t2data.get_data().ravel().tobytes(), # saves as float32 bytes
            maskdata.get_data().ravel().tobytes(), # saves as float32 bytes
            t1data.shape # saves as int64
        )

        # write to tf record
        writer.write(subject)

# # read tfrecord
# feature_description = {
#     't1': tf.io.FixedLenFeature([], tf.string),
#     't2': tf.io.FixedLenFeature([], tf.string),
#     'mask': tf.io.FixedLenFeature([], tf.string),
#     'shape': tf.io.FixedLenFeature([], tf.string)
# }
# def parse_img_function(example):
#     return tf.io.parse_single_example(example, feature_description)
# raw_tfrecord = tf.data.TFRecordDataset(tfrecords_path+'hbcd.tfrecords',"ZLIB")
# parsed_image_dataset = raw_tfrecord.map(parse_img_function)

# # decode data into tensor
# import simplebrainviewer as sbv
# for i in parsed_image_dataset:
#     # decode the shape data
#     shaped = tf.io.decode_raw(i['shape'],'int64')
#     # decode image data
#     image_data = tf.io.decode_raw(i['t1'],'float')
#     a = tf.reshape(image_data, shaped)
#     sbv.plot_brain(a.numpy())
#     # decode image data
#     image_data = tf.io.decode_raw(i['t2'],'float')
#     a = tf.reshape(image_data, shaped)
#     sbv.plot_brain(a.numpy())
#     # decode image data
#     image_data = tf.io.decode_raw(i['mask'],'float')
#     a = tf.reshape(image_data, shaped)
#     sbv.plot_brain(a.numpy())