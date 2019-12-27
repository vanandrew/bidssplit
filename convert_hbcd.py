#!/usr/bin/env python

import os
from tfrecordutils import write_tfrecord

if __name__ == '__main__':
    # get files
    path = "/home/vanandrew/Data/nii_data"
    files = os.listdir(path)
    T1list = sorted([os.path.join(path,i) for i in files if "T1w.nii.gz" in i])
    T2list = sorted([os.path.join(path,i) for i in files if "T2w.nii.gz" in i])
    masklist = sorted([os.path.join(path,i) for i in files if "brainmask.nii.gz" in i])
    
    # filter list
    with open('/home/vanandrew/Data/lists/train_set.txt','r') as filter_list:
        filt = filter_list.readlines()
        filt = [i.rstrip() for i in filt]
        T1list = [i for i in T1list if os.path.basename(i).split("_")[0].split("sub-")[1] in filt]
        T2list = [i for i in T2list if os.path.basename(i).split("_")[0].split("sub-")[1] in filt]
        masklist = [i for i in masklist if os.path.basename(i).split("_")[0].split("sub-")[1] in filt]

    # write data to tfrecord
    write_tfrecord("/home/vanandrew/Data/hbcd_train.tfrecords", T1list, T2list, masklist)