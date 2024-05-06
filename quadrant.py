#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:36:58 2024

@author: lamshangyat
"""

import pandas as pd

# Read the cleaned data file

request = pd.read_csv("request_cleaned.csv", index_col="Id")

# Rename and clean the "Export_tagged_places" column

request = request.rename(columns={"Export_tagged_places":"Quadrant"})
print(request["Quadrant"].unique())

request["Quadrant"] = request["Quadrant"].str.split(",").str[0]

# Quadrant

print(request["Quadrant"].unique())

quad = ["Northwest Quadrant", "Northeast Quadrant", "Southwest Quadrant", 
             "Southeast Quadrant"]

good_quad = request[request["Quadrant"].isin(quad)]
request_by_quad = good_quad.groupby("Quadrant").size().reset_index(name='Count')
total_request = len(good_quad)

request_by_quad["percentage"] = (request_by_quad["Count"] / total_request).round(3)
print(request_by_quad)

# Rename the quadrants

rename_dict = {'Northeast Quadrant': 'Northeast',
               'Northwest Quadrant': 'Northwest',
               'Southeast Quadrant': 'Southeast',
               'Southwest Quadrant': 'Southwest'}

request_by_quad['Quadrant'] = request_by_quad['Quadrant'].replace(rename_dict).str.upper()

print(request_by_quad)

# Write out a csv file

request_by_quad.to_csv("percentage_by_quad.csv")
