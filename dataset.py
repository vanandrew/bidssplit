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
            subdata.get_fdata().ravel().tobytes(),
            np.array(subdata.shape).tobytes()
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
slist = [np.frombuffer(i['feature_img'].numpy()).reshape(np.frombuffer(i['shape'].numpy(),dtype=np.int)) for i in parsed_image_dataset]
# # save to TFrecord
# t1_dataset = tf.data.Dataset.from_tensor_slices(T1s)
# serialized_t1_dataset = tf.io.serialize_tensor(t1_dataset)
# print(t1_dataset)
# print(serializer_t1_dataset)
# # t2_dataset = tf.data.Dataset.from_tensor_slices(T2s)
# # mask_dataset = tf.data.Dataset.from_tensor_slices(masks)
# writer = tf.data.experimental.TFRecordWriter("./t1_dataset.01.tfrecords")
# writer.write(t1_dataset)