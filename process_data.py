import matplotlib.image as mpimg
import numpy as np
import h5py
import os
def process_data():
    X=[]
    a=os.listdir("./dataset")
    y=np.array([i[0:4] for i in a])
    for i in a:
        I= mpimg.imread('./dataset/'+i)
        X.append(I[:,:,0:3])
    s=np.array(X)
    dt = h5py.special_dtype(vlen=str)
    with h5py.File("dataset.h5","w") as f:
        f["X"]=s
        ds = f.create_dataset('Y', y.shape , dtype=dt)
        ds[:]=y
def get_data():
    with h5py.File("dataset.h5","r") as f:
        X=f["X"].value
        Y=f["Y"].value
    return X,Y
