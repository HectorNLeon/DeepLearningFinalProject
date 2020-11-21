
########################## first part: prepare data ###########################
from random import shuffle
import glob
import numpy as np


shuffle_data = True  # shuffle the addresses

hdf5_path = 'D:/SimpsonsHDF5/simpsonsData.h5'  # file path for the created .hdf5 file

simpsons_train_path = 'D:/simpsons_dataset/*.jpg' # the original data path

# get all the image paths 
addrs = glob.glob(simpsons_train_path)

# label the data as 0=cat, 1=dog
labels = [0 if 'homer' in addr else 1 for addr in addrs] 
classes = np.array(["Homer Simpson", "Not Homer"])

# shuffle data
if shuffle_data:
    c = list(zip(addrs, labels)) # use zip() to bind the images and labels together
    shuffle(c)
 
    (addrs, labels) = zip(*c)  # *c is used to separate all the tuples in the list c,  
                               # "addrs" then contains all the shuffled paths and 
                               # "labels" contains all the shuffled labels.
                               
# Divide the data into 80% for train and 20% for test
train_addrs = addrs[0:int(0.8*len(addrs))]
train_labels = labels[0:int(0.8*len(labels))]

test_addrs = addrs[int(0.8*len(addrs)):int(0.9*len(addrs))]
test_labels = labels[int(0.8*len(labels)):int(0.9*len(addrs))]

dev_addrs = addrs[int(0.9*len(addrs)):]
dev_labels = labels[int(0.9*len(addrs)):]

##################### second part: create the h5py object #####################
import h5py

train_shape = (len(train_addrs), 64, 64, 3)
test_shape = (len(test_addrs), 64, 64, 3)
dev_shape = (len(dev_addrs), 64, 64, 3)


# open a hdf5 file and create earrays 
f = h5py.File(hdf5_path, mode='w')

# PIL.Image: the pixels range is 0-255,dtype is uint.
# matplotlib: the pixels range is 0-1,dtype is float.
f.create_dataset("train_img", train_shape, np.uint8)
f.create_dataset("dev_img", dev_shape, np.uint8)
f.create_dataset("test_img", test_shape, np.uint8)  

dt = h5py.special_dtype(vlen=str)
f.create_dataset("list_classes", (len(classes),),dtype=dt)
f["list_classes"][...] = classes


# the ".create_dataset" object is like a dictionary, the "train_labels" is the key. 
f.create_dataset("train_labels", (len(train_addrs),), np.uint8)
f["train_labels"][...] = train_labels

f.create_dataset("dev_labels", (len(dev_addrs),), np.uint8)
f["dev_labels"][...] = dev_labels

f.create_dataset("test_labels", (len(test_addrs),), np.uint8)
f["test_labels"][...] = test_labels

######################## third part: write the images #########################
import cv2

# loop over train paths
for i in range(len(train_addrs)):
  
    if i % 1000 == 0 and i > 1:
        print ('Train data: {}/{}'.format(i, len(train_addrs)) )

    addr = train_addrs[i]
    img = cv2.imread(addr)
    img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)# resize to (128,128)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # cv2 load images as BGR, convert it to RGB
    f["train_img"][i, ...] = img[None] 

# loop over dev paths
for i in range(len(dev_addrs)):
  
    if i % 1000 == 0 and i > 1:
        print ('Dev data: {}/{}'.format(i, len(dev_addrs)) )

    addr = dev_addrs[i]
    img = cv2.imread(addr)
    img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)# resize to (128,128)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # cv2 load images as BGR, convert it to RGB
    f["dev_img"][i, ...] = img[None] 

# loop over test paths
for i in range(len(test_addrs)):

    if i % 1000 == 0 and i > 1:
        print ('Test data: {}/{}'.format(i, len(test_addrs)) )

    addr = test_addrs[i]
    img = cv2.imread(addr)
    img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    f["test_img"][i, ...] = img[None]

f.close()
