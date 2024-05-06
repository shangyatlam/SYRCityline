#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 22:54:47 2024

@author: lamshangyat
"""

import pandas as pd

# Read the data file

request = pd.read_csv("SYRCityline_requests_(2021-Present).csv", index_col="Id")
print(request.head())

# Drop the duplicated columns "Lat" and "Lng"

request = request.drop(columns=["Lat", "Lng"])

# Create new columns for relevant analysis

request[["Created_Date", "Created_Time"]] = request["Created_at_local"].str.split(" - ", expand=True)
request["Created_Date"] = pd.to_datetime(request["Created_Date"])
request = request.drop(columns="Created_at_local")

request["Year"] = request["Created_Date"].dt.year.astype(str)
request["Month"] = request["Created_Date"].dt.strftime("%Y-%m")

# Rename the "Agency_Name" column 

request = request.rename(columns={"Agency_Name":"Agency"})

# Write out a csv file with the new columns

request.to_csv("request_cleaned.csv")
