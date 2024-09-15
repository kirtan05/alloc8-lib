# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 17:16:10 2024

@author: Harshit
"""

from spherecluster import SphericalKMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import csv

'''
def getroomie(feature_vec_csv, batch_strength=552, floors=7, roomsperfloor=28, sharing_factor=3, cluster_size=3,num_features=2454):
    
    # help:
    # feature_vec_csv (.csv): student IDs and their feature vectors across all parameters
    # batch_strength (int): number of students to allocate in a hostel
    # floors (int): no of floors in the hostel 
    # roomsperfloor (int): no of rooms in each floor 
    # sharing_factor (int): no of roomies
    # cluster_size (int): size of one cluster (roomwise/floorwise allocation)
    
    # Find K clusters from data matrix X (n_examples x n_features)

    # spherical k-means
    
    # Normalize the numbers so that their sum equals 
    inertia = []
    ks = []
    for k in range(6,260,10):
        normalized_list = [1/num_features]*num_features
        normalized_array = np.array(normalized_list)
        feature_df = pd.read_csv(feature_vec_csv) 
        X = feature_df.to_numpy()
        X = X[:,1:]
        
        x_squared_norms = np.zeros(len(feature_df))
        for i in range(len(x_squared_norms)):
            x_squared_norms[i] = np.sum(X[i,:]) 
        
        #skm = SphericalKMeans(n_clusters=int(batch_strength/cluster_size))
        skm = SphericalKMeans(n_clusters=k)
        skm.fit(X,sample_weight = normalized_array)
        #print(skm.cluster_centers_)
        #print(skm.labels_)
        print(skm.inertia_)
        inertia.append(skm.inertia_)
        ks.append(k)
    
    plt.plot(ks,inertia)
    plt.show()
    plt.savefig("init_res.png")

'''

def getroomie(feature_vec_csv, batch_strength=552, floors=7, roomsperfloor=28, sharing_factor=3, cluster_size=3,num_features=2454):
    
    # help:
    # feature_vec_csv (.csv): student IDs and their feature vectors across all parameters
    # batch_strength (int): number of students to allocate in a hostel
    # floors (int): no of floors in the hostel 
    # roomsperfloor (int): no of rooms in each floor 
    # sharing_factor (int): no of roomies
    # cluster_size (int): size of one cluster (roomwise/floorwise allocation)
    
    # Find K clusters from data matrix X (n_examples x n_features)

    # spherical k-means
    
    # Normalize the numbers so that their sum equals 
    normalized_list = [1/num_features]*num_features
    normalized_array = np.array(normalized_list)
    feature_df = pd.read_csv(feature_vec_csv) 
    X = feature_df.to_numpy()
    ids = X[:,0]
    X = X[:,1:]
    
    x_squared_norms = np.zeros(len(feature_df))
    for i in range(len(x_squared_norms)):
        x_squared_norms[i] = np.sum(X[i,:]) 
    
    #skm = SphericalKMeans(n_clusters=int(batch_strength/cluster_size))
    skm = SphericalKMeans(n_clusters=3)
    skm.fit(X,sample_weight = normalized_array)
    #print(skm.cluster_centers_)
    print(skm.labels_)
    print(skm.inertia_)
    
    #label_types = {0:[],1:[],2:[],3:[],4:[],5:[]}
    label_types = {0:[],1:[],2:[]}
    for i in range(len(skm.labels_)):
        label_types[skm.labels_[i]].append(ids[i])
    print(ids)
    print(label_types)
    
    # Path to your CSV file
    csv_file_path = 'floorwise_allocation_femme.csv'
    
    # Write the dictionary to a CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header (keys)
        writer.writerow(label_types.keys())
        # Write the values
        writer.writerow(label_types.values())
    
    print(f'The dictionary has been saved to {csv_file_path}')
        
        
        
    
    
def getnumcolumns(csv_file_path):
    df = pd.read_csv(csv_file_path)
    num_columns = df.shape[1]
    print(f'The number of columns in the CSV file is: {num_columns}')

if __name__ == "__main__":
    getnumcolumns("women_stud_data.csv")
    getroomie("women_stud_data.csv")
    
    


