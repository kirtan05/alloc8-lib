# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 12:22:43 2024

@author: Harshit
"""

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
import ast
from collections import defaultdict

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

def getroomie(feature_vec_csv, floorwise_allocation, batch_strength=552, floors=7, roomsperfloor=28, sharing_factor=3, cluster_size=3,num_features=2454):
    
    # help:
    # feature_vec_csv (.csv): student IDs and their feature vectors across all parameters
    # floorwise_allocation (.csv): floor number and student IDs of students matched to the floor 
    # batch_strength (int): number of students to allocate in a hostel
    # floors (int): no of floors in the hostel 
    # roomsperfloor (int): no of rooms in each floor 
    # sharing_factor (int): no of roomies
    # cluster_size (int): size of one cluster (roomwise/floorwise allocation)
    
    # Find K clusters from data matrix X (n_examples x n_features)

    # spherical k-means
    rooms=[None]*700

    floor_df = pd.read_csv(floorwise_allocation)
    for i in range(3):
        floor_ids = floor_df[f'{i}'].iloc[0]
        floor_ids = ast.literal_eval(floor_ids)
        floor_ids = np.array(floor_ids, dtype=np.float64)
        normalized_list = [1/num_features]*num_features
        normalized_array = np.array(normalized_list)
        feature_df = pd.read_csv(feature_vec_csv) 
        X = feature_df.to_numpy()
        ids = X[:,0]
        X = X[:,1:]
        #print(ids, floor_ids)
        mask = np.isin(ids,floor_ids)
        #print(mask)
        ids=ids[mask]
        X=X[mask]
        #print(X)
        #print(filtered_ids)
        #skm = SphericalKMeans(n_clusters=int(batch_strength/cluster_size))
        skm = SphericalKMeans(n_clusters=len(floor_ids)//2)
        skm.fit(X,sample_weight = normalized_array)
        #print(skm.cluster_centers_)
        #print(skm.labels_)
        #print(skm.inertia_)
        for j in range(len(skm.labels_)):
            room_id = skm.labels_[j]+i*100
            #print(room_id)
            if rooms[room_id] is None:
                rooms[room_id]=[]
            rooms[room_id].append(ids[j])
        
        #label_types = {0:[],1:[],2:[],3:[],4:[],5:[]}
        
        #for i in range(len(skm.labels_)):
        #    label_types[skm.labels_[i]].append(ids[i])
        #print(ids)
        #print(label_types)
        
        # Path to your CSV file
        #csv_file_path = 'roomwise_allocation.csv'
        
        # Write the dictionary to a CSV file
        #with open(csv_file_path, mode='w', newline='') as file:
        #    writer = csv.writer(file)
            # Write the header (keys)
        #    writer.writerow(label_types.keys())
            # Write the values
        #    writer.writerow(label_types.values())
        
        #print(f'The dictionary has been saved to {csv_file_path}')
        
    print(rooms)
    csv_file_path = 'rooms_femme.csv'
    total=0
    # Prepare the data for CSV
    data_for_csv = []
    for room_id, students in enumerate(rooms):
        if students is not None:
            row = [room_id] + students
            total+=len(row)
            data_for_csv.append(row)
    
    # Write the data to a CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_for_csv)
    print(f"total number of students {total}")
    print(f"Data saved to {csv_file_path}")
    
    # Function to get floor from room ID
    def get_floor(room_id):
        return room_id % 100
    
    # Process rooms into floors and students
    floors = defaultdict(list)
    for room_id, student_ids in enumerate(rooms):
        if student_ids:  # Skip if the room has no students
            floor = get_floor(room_id)
            floors[floor].append((room_id, student_ids))
    
    # Group students into trios
    trios = []
    leftovers_by_floor = defaultdict(list)
    
    # Group students in the same room first
    for floor, rooms_on_floor in floors.items():
        for room_id, students in rooms_on_floor:
            while len(students) >= 3:
                trios.append((floor, room_id, students[:3]))
                students = students[3:]
            if students:
                leftovers_by_floor[floor].extend(students)
    
    # Group leftover students by floor
    for floor, leftovers in leftovers_by_floor.items():
        while len(leftovers) >= 3:
            trios.append((floor, 'leftovers', leftovers[:3]))
            leftovers = leftovers[3:]
        if leftovers:
            floors[floor] = leftovers
        else:
            floors[floor] = []
    
    # Handle any remaining students that couldn't be grouped into trios
    remaining_students = []
    for leftovers in floors.values():
        remaining_students.extend(leftovers)
    
    # Form trios with remaining students
    for i in range(0, len(remaining_students), 3):
        trios.append(('remaining', 'remaining', remaining_students[i:i+3]))
    
    # Save the trios to a CSV file
    output_csv_path = 'trios_floorwise.csv'
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Floor', 'Room', 'Student_1', 'Student_2', 'Student_3'])
        for trio in trios:
            floor, room, students = trio
            writer.writerow([floor, room] + students + [''] * (3 - len(students)))
    
    print(f"Trios saved to {output_csv_path}")

        
    
    
def getnumcolumns(csv_file_path):
    df = pd.read_csv(csv_file_path)
    num_columns = df.shape[1]
    print(f'The number of columns in the CSV file is: {num_columns}')

if __name__ == "__main__":
    #getnumcolumns("male_stud_data.csv")
    getroomie("women_stud_data.csv","floorwise_allocation_femme.csv")
    
    


