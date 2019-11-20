#!/usr/bin/env python3

import os
import numpy as np
import nibabel as nib
import tensorflow as tf

# get list of T1s/T2s/masks
path = "/mnt/Daenerys/HBCD/organized_data/"
files = os.listdir(path)
T1list = sorted([i for i in files if "T1w.nii.gz" in i])[:2]
T2list = sorted([i for i in files if "T2w.nii.gz" in i])[:2]
masklist = sorted([i for i in files if "brainmask.nii.gz" in i])[:2]

# Define tf Example serializer for brain data
def serialize_brain_data(feature_img,shape):
    """
        Saves data as tf.Example format
    """
    # create a dict of features to pass into tf Features 
    feature_dict = {
        'feature_img': tf.train.Feature( # makes a single feature
            bytes_list=tf.train.BytesList( # converts to tf Example bytes list
                value=[feature_img] # pass in the numpy bytes to the list
            )
        ),
        'shape': tf.train.Feature(
            bytes_list=tf.train.BytesList(
                value=[shape]
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
with tf.io.TFRecordWriter(tfrecords_path+"hbcd_t1_data.00.tfrecords") as writer:
    for t1,t2,mask in zip(T1list,T2list,masklist):
        print(t1)
        # serialize subject to write to tfrecord
        subdata = nib.load(path+t1)

        subject = serialize_brain_data(
            subdata.get_data().ravel().tobytes(), # saves as float32 bytes
            np.array(subdata.shape).tobytes() # saves as int64 bytes
        )
        # write to tf record
        writer.write(subject)

# read tfrecord
feature_description = {
    'feature_img': tf.io.FixedLenFeature([], tf.string),
    'shape': tf.io.FixedLenFeature([], tf.string)
}
def parse_img_function(example):
    return tf.io.parse_single_example(example, feature_description)
raw_tfrecord = tf.data.TFRecordDataset(tfrecords_path+'hbcd_t1_data.00.tfrecords')
parsed_image_dataset = raw_tfrecord.map(parse_img_function)

# decode data into tensor
import simplebrainviewer as sbv
for i in parsed_image_dataset:
    # decode the shape data
    shaped = tf.io.decode_raw(i['shape'],'int64')
    # decode image data
    image_data = tf.io.decode_raw(i['feature_img'],'float')
    a = tf.reshape(image_data, shaped)
    print(a)
    sbv.plot_brain(a.numpy())