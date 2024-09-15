# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 09:20:33 2024

@author: Harshit
"""

import pandas as pd
import numpy as np

# Number of instances and features
num_instances = 550
num_features = 786

# Generate roll numbers
roll_numbers = [f"2401{str(i).zfill(4)}" for i in range(num_instances)]

# Generate random feature vectors
feature_vectors = np.random.rand(num_instances, num_features)

# Create DataFrame
data = pd.DataFrame(feature_vectors, index=roll_numbers)

# Reset index and rename columns
data.reset_index(inplace=True)
data.rename(columns={'index': 'Roll_No'}, inplace=True)

# Save to CSV
file_path = 'student_data.csv'
data.to_csv(file_path, index=False)

file_path
