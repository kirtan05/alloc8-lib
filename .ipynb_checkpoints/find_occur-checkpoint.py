# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 14:29:18 2024

@author: Harshit
"""

import pandas as pd
import numpy as np
# Load the list.xlsx file
list_df = pd.read_excel('list.xlsx')

# Extract the JEE(Adv) Roll Numbers
jee_adv_roll_numbers = list_df[list_df['Gender'] == 'Male']['JEE(Adv) Roll No'].astype(str).tolist()
print(len(jee_adv_roll_numbers))
# Load the rooms.csv file
rooms_df = pd.read_csv('rooms_trio.csv', header=None)

# Flatten the rooms data to get a list of all roll numbers in rooms.csv
#rooms_roll_numbers = rooms_df.values.flatten()
#rooms_roll_numbers = [str(int(num)) for num in rooms_roll_numbers if pd.notna(num)]
#print(rooms_roll_numbers)
#duplicates = [item for item, count in pd.Series(rooms_roll_numbers).value_counts().items() if count > 1]

#print(duplicates)
# Find the roll numbers in list.xlsx that are not in rooms.csv
#missing_roll_numbers = [roll for roll in jee_adv_roll_numbers if roll not in rooms_roll_numbers]

final_trios = [[None]]*215
assigned = []
current_room=0


rooms_array = rooms_df.values
        
for i in rooms_array:
    for j in i:
        if j not in assigned:
            if final_trios[current_room] is None:
                final_trios[current_room]=[]
            if len(final_trios[current_room])==3:
                current_room+=1
            if final_trios[current_room] is None:
                final_trios[current_room]=[]
            final_trios[current_room].append(j)
            assigned.append(j)
print(type(jee_adv_roll_numbers[0]),type(rooms_array[0][0]))

for i in jee_adv_roll_numbers:
    i = np.int64(i)
    if i not in assigned:
            
            if final_trios[current_room] is None:
                final_trios[current_room]=[]
            if len(final_trios[current_room])==3:
                current_room+=1
            if final_trios[current_room] is None:
                final_trios[current_room]=[]
            final_trios[current_room].append(i)
            assigned.append(i)
print(len(final_trios))
finall=[]
cnt=0
temp=[]
for i in assigned:
    temp.append(i)
    cnt+=1
    if(cnt==3):
        finall.append(temp)
        cnt=0
        temp=[]
print(finall)
print(len(finall))
print(len(assigned))
print(assigned[-1])

# Load the list.xlsx file
list_df = pd.read_excel('list.xlsx')

# Extract relevant columns and convert roll numbers to strings
list_df['JEE(Adv) Roll No'] = list_df['JEE(Adv) Roll No'].astype(str)
list_df['Name'] = list_df['Name'].astype(str)

# Sample 'finall' list of lists (each sublist contains 3 roll numbers)
# This should be replaced with your actual 'finall' list
# Prepare data for the final DataFrame
final_data = []

for trio in finall:
    trio_data = []
    for roll_number in trio:
        student_info = list_df[list_df['JEE(Adv) Roll No'] == str(roll_number)]
        if not student_info.empty:
            name = student_info.iloc[0]['Name']
            trio_data.extend([roll_number, name])
        else:
            trio_data.extend([roll_number, "Name Not Found"])
    final_data.append(trio_data)

# Create the final DataFrame
final_df = pd.DataFrame(final_data, columns=['Roll1', 'Name1', 'Roll2', 'Name2', 'Roll3', 'Name3'])

# Save the final DataFrame to an Excel file
final_df.to_excel('final_trios.xlsx', index=False)

print("Final trios saved to final_trios.xlsx")

'''
# Output the missing roll numbers
print("Missing Roll Numbers:")
for roll in missing_roll_numbers:
    print(roll)
'''