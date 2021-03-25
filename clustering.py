'''
    Code borrowed from: https://towardsdatascience.com/how-to-cluster-images-based-on-visual-similarity-cd6e7209fe34
'''

# for loading/processing the images  
from keras.preprocessing.image import load_img 
from keras.preprocessing.image import img_to_array 
from keras.applications.vgg16 import preprocess_input 

# models 
from keras.applications.vgg16 import VGG16 
from keras.models import Model

# clustering and dimension reduction
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# for everything else
import os
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import pandas as pd
import pickle
from tqdm import tqdm


def get_filepaths_by_extension(path, ext):
    '''
        Get list of all filepaths with a specific extension within the given directory and all its subdirectories
    '''
    paths = []

    for root, dirs, files in os.walk(path):
        for file in files:
            #append the file name to the list
            new_path = os.path.join(root,file)
            if new_path[-len(ext):].lower() == ext:
                paths.append(new_path)

    paths = [path.replace('\\','/') for path in paths]

    return paths

path = 'photos'

#get photos paths
photos = get_filepaths_by_extension(path,'.jpg')
            
model = VGG16()
model = Model(inputs = model.inputs, outputs = model.layers[-2].output)

def extract_features(file, model):
    # load the image as a 224x224 array
    img = load_img(file, target_size=(224,224))
    # convert from 'PIL.Image.Image' to numpy array
    img = np.array(img) 
    # reshape the data for the model reshape(num_of_samples, dim 1, dim 2, channels)
    reshaped_img = img.reshape(1,224,224,3) 
    # prepare image for model
    imgx = preprocess_input(reshaped_img)
    # get the feature vector
    features = model.predict(imgx, use_multiprocessing=True)
    return features
   
data = {}
p = 'data'

# lop through each image in the dataset
for photo in tqdm(photos):
    # try to extract the features and update the dictionary
    try:
        feat = extract_features(photo,model)
        data[photo] = feat
    except:
        pass
 
# get a list of the filenames
filenames = np.array(list(data.keys()))

# get a list of just the features
feat = np.array(list(data.values()))

# reshape so that there are 210 samples of 4096 vectors
feat = feat.reshape(-1,4096)

# reduce the amount of dimensions in the feature vector
pca = PCA(n_components=100, random_state=42)
pca.fit(feat)
x = pca.transform(feat)

# cluster feature vectors
kmeans = KMeans(n_clusters=5,n_jobs=-1, random_state=42)
kmeans.fit(x)

# holds the cluster id and the images { id: [images] }
groups = {}
for file, cluster in zip(filenames,kmeans.labels_):
    if cluster not in groups.keys():
        groups[cluster] = []
        groups[cluster].append(file)
    else:
        groups[cluster].append(file)
#save groups
with open('data/clusters.pkl','wb') as f:
    pickle.dump(groups,f) 
