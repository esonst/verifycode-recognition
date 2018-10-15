from keras.models import load_model
import numpy as np
def load_models(name):
    return load_model(name)
def pre_process(model,image):
    x_set=[]
    x_set.append(image[:,2:18,:])
    x_set.append(image[:,17:33,:])
    x_set.append(image[:,31:47,:])
    x_set.append(image[:,40:56,:])
    X_=np.asarray(x_set)/255
    Y_=model.predict_classes(X_)
    return "".join([chr(i+48) if i<10 else chr(i+56) for i in Y_])
