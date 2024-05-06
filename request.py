#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 22:56:03 2024

@author: lamshangyat
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["figure.dpi"] = 300
sns.set_style("darkgrid")

# Read the data file with the new columns

request = pd.read_csv("request_cleaned.csv", index_col="Id")
print(request.head())

#%%

# Countplot: Category of requests by year

fig, ax = plt.subplots()
sns.countplot(data=request, x="Year", hue="Agency", ax=ax)

ax.set_ylabel("Count")
fig.suptitle("Types of City Department to which Requests were Assigned by Year")

legend = ax.legend()
for text in legend.texts:
    text.set_fontsize(4.5)

fig.tight_layout()
fig.savefig("assigned_dept_year.png")

#%%

## Countplot: Report sources by year

fig, ax = plt.subplots()
sns.countplot(data=request, x="Year", hue="Report_Source", ax=ax)

ax.set_xlabel("Year")
ax.set_ylabel("Count")
fig.suptitle("Report Sources by Year")
fig.savefig("source.png")

#%%

## Lineplot: Trend of requests by Month

# Calculate the number of requests handled by different agencies by month

by_Month = request.groupby("Month")["Agency"].value_counts().reset_index(name="Count")
print(by_Month.head())

# Create a figure

g = sns.relplot(data=by_Month, x="Month", y="Count", hue="Agency", marker="o", kind="line")
ax = g.ax

n_ticks = 5
tick_positions = ax.get_xticks()
selected_tick_positions = tick_positions[::len(tick_positions)//n_ticks]
ax.set_xticks(selected_tick_positions)
plt.xticks(rotation=45)

ax.set_ylabel("Count")
g.fig.suptitle("Types of City Department to which Requests were Sent by Month")

g.tight_layout()
g.fig.savefig("assigned_dept_month.png")

#%%

## Lineplot: Requests under the category "Weekly Trash Pickup" and "Illegal setouts" in each Month

# Subset requests that fall under the two categories

by_trash = request[(request["Category"]=="Weekly Trash Pickup") | 
                     (request["Category"]=="Illegal Setouts")]
by_trash_group = by_trash.groupby("Month")["Category"].value_counts().unstack().fillna(0)
by_trash_group["total"] = by_trash_group.sum(axis=1)
print(by_trash_group.head())

# Create a figure

fig, ax = plt.subplots()
sns.lineplot(data=by_trash_group, x="Month", y="total", marker="o", ax=ax)

plt.axvline(x="2023-06", color='r', linestyle='--')
plt.axvline(x="2023-09", color='g', linestyle='--')

ax.set_ylabel("Number")
plt.xticks(rotation=90)
fig.suptitle("Number of 'Weekly Trash Pickup' and 'Illegal Setouts' Requests in Each Month")

fig.tight_layout()
fig.savefig("trash_related.png")

#%%

## Barplot: Average processing time of each agency

# Calculate the average processing time (in days) of each agency

time_by_agency = request.groupby("Agency")["Minutes_to_closed"].sum()
no_by_agency = request.groupby("Agency").size()
average_days = (time_by_agency/no_by_agency/1440).sort_values(ascending=True)

# Create a figure

fig, ax = plt.subplots()
average_days.plot(kind="bar", ax=ax)

ax.set_xlabel("Agency")
ax.set_ylabel("Average Processing Days")
plt.xticks(fontsize=5)
plt.xticks(rotation=30)
fig.suptitle("Average Processing Time of Different Types of City Department")

fig.tight_layout()
fig.savefig("time.png")
