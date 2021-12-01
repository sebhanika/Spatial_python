# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 10:54:07 2021

@author: hanik
"""
# this file is a first attempt of coding and working with Data in Python
# as an example I used Data from the 2020 Census in Delaware
# One major goal is to utilize the Geopandas package and make simple maps

#%%
# packages

import pandas as pd #used to manipulate data frames and read csv table
import geopandas #used to process Goedata and create maps
import matplotlib.pyplot as plt #used to modefy maps/plots

#%%
# import data from csv file
data_dl = pd.read_csv("Your path to census data")
data_dl.head

#import shapefile of county subdivisions
path_to_sub = "Your path to shapefile_County subdivisions"
shp_del_sub = geopandas.read_file(path_to_sub)

#import shapefile of census tracts
path_to_ct = "You path to shapefile_Census tracts"
shp_del_ct = geopandas.read_file(path_to_ct)

#%% Data for County sub divisions
# filter data for county subs
county_subs = data_dl[data_dl['SUMLEV'] == 60] #subsects data.frame to only county sub-divisons
county_subs2 = county_subs[["GEOCODE", "COUSUBNS", # select only relevant columns 
                            "COUSUB", "BASENAME", 
                            "P0010001", "P0010004",
                            "H0010001", "H0010002", 
                            "H0010003"]]

county_subs3 = county_subs2.rename(columns={"BASENAME": "NAME"}) #rename column for merging

# merge shapefile with county sub data
data_merge = shp_del_sub.merge(county_subs3, on='NAME') # merge shp and tbl with Name Attribute 
data_merge['AA_pop_rat'] = (data_merge.P0010004 / data_merge.P0010001)*100 # calculate Share of population
data_merge['Vacancies'] = (data_merge.H0010003 / data_merge.H0010001)*100

# plot of share of African American population
plot1 = data_merge.plot("AA_pop_rat", 
                legend = True, 
                cmap = 'OrRd', #defines color scheme/gradient
                edgecolor = "black", #defines color of lines
                legend_kwds = {'label': "African-American Population in %",
                               'orientation': "vertical"}) #formates Legend
plt.title('Share of African-American Population') #adds title to plot

# plot of housing vacancies
plot2 = data_merge.plot("Vacancies", 
                legend = True, 
                cmap = 'OrRd', #defines color scheme/gradient
                edgecolor = "black", #defines color of lines
                legend_kwds = {'label': "Vacant Housing in %",
                               'orientation': "vertical"}) #formates Legend
plt.title('Share of Vacant Housing') #adds title to plot

#%% Data for Census tracts
# similar process as above but for Census Tracks
# filter data for county subs

ct = data_dl[data_dl['SUMLEV'] == 140] #filter data to only census trackts (140)
ct2 = ct[["TRACT", "GEOCODE", "P0010001", "P0010004",
                    "H0010001", "H0010002", 
                    "H0010003"]]
ct3 = ct2.rename(columns={"GEOCODE": "GEOID"}) #rename column for merging

# merge shapefile with census track data
ct_merge = shp_del_ct.merge(ct3, on='GEOID') # merge shp and tbl with Name Attribute 
ct_merge['AA_pop_rat'] = (ct_merge.P0010004 / ct_merge.P0010001)*100 # calculate Share of population
ct_merge['Vacancies'] = (ct_merge.H0010003 / ct_merge.H0010001)*100 # calculate Share of vacant housing

# plot of share of African American population
plot1 = ct_merge.plot("AA_pop_rat", 
                legend = True, 
                cmap = 'OrRd', #defines color scheme/gradient
                edgecolor = "black", #defines color of lines
                linewidth = 0.2, #defines line width to make small CT more readable
                legend_kwds = {'label': "African-American Population in %",
                               'orientation': "vertical"}) #formates Legend
plt.title('Share of African-American Population') #adds title to plot

# plot of housing vacancies
plot2 = ct_merge.plot("Vacancies", 
                legend = True, 
                cmap = 'OrRd', #defines color scheme/gradient
                edgecolor = "black", #defines color of lines
                linewidth = 0.2,
                legend_kwds = {'label': "Vacant Housing in %",
                               'orientation': "vertical"}) #formates Legend
plt.title('Share of Vacant Housing') #adds title to plot
# plot2.set_axis_off() # removes axis 

#%% 