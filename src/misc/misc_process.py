#!/usr/bin/env python

"""
Set of definition to process and/or import data.
"""

import os, time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.ndimage.filters import gaussian_filter1d

__author__ = "Marek Grzelczak"
__copyright__ = "Copyright 2021, Centro de Fisica de Materiales CSIC-UPV/EHU"
__credits__ = ["Marek Grzelczak"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Marek Grzelczak"
__email__ = "grzelczak.marek@gmail.com"
__status__ = "Production"

def normalize_max(data):
    # normalize each dataframe by the maximum value
    data_norm = data.apply(lambda x: x/x.max(), axis=0)
    return data_norm

def normalize_400(data):
    # normalize each dataframe by the maximum value
    data_norm = data.apply(lambda x: x/x.iloc[400,], axis=0)
    return data_norm

def import_files (path, filter = '', experiment_number = ''):  
    ''' import, append and concat files into a dataframe and extract data
    at given wavelength Abs340 and finally plot full spectra and Abs at 340
    over time.'''
    all_files = glob.glob(os.path.join(path, filter + "*.txt")) 
    data_frame = []
    name = []
    full_spectra = pd.DataFrame()
    for file in sorted(all_files):
        creation_time = os.stat(file).st_birthtime
        readible_date = datetime.fromtimestamp(creation_time)
        df = pd.read_csv(file, index_col=0, header=None, sep='\t', skiprows=0)
        df.rename(columns={1: readible_date}, inplace=True)
        data_frame.append(df)
        full_spectra = pd.concat(data_frame, 
                                 axis=1).round(decimals = 3).truncate(before = 300, 
                                                                      after = 1100, 
                                                                      axis = 0)
    for column in full_spectra.columns:
        time_step = column - full_spectra.columns[0]
        minutes = round(time_step.total_seconds() / 60) # convert time difference from hour to minute
        name.append(minutes)  
    full_spectra.columns = name
#     full_spectra.to_csv('{}_UV_Vis.csv'.format(experiment_number),  header = True)
    return full_spectra

def fit_norm_mu(data, column_name = ""):
    ''' This function get the histogram for a given colum in a dataframe. 
    Use df and column name as input
    '''
    mu, std = norm.fit(data[column_name])
    return mu, std

def get_maxima_LSPR(df):
    # slice the spectra around the abs maximum of plasmon band
    truncated_data = df.loc[700:900,:]
    df1 = truncated_data.max().to_frame()

   # df1.set_index(pd.Index(list(range(31)))
   # df1.index.name = 'Time'
   # df1.columns = ['LSPR@abs']
    
    # set the index of sliced df by copying column names and rename column :  
    df1.set_index(df.columns, inplace=True)
    df1.index.name = 'Time'
    df1.columns = ['LSPR@abs']
        
    # add column with wavelenght at the maximum absorption
    df1['LSPR@max'] = truncated_data.idxmax()
#     df1.to_csv(path + df + ".csv",  header = True)
    return df1

def get_maxima_NADH(df):
    # slice the spectra around the abs maximum of plasmon band
    truncated_data = df.loc[320:360,:]
    df1 = truncated_data.max().to_frame()

   # df1.set_index(pd.Index(list(range(31)))
   # df1.index.name = 'Time'
   # df1.columns = ['LSPR@abs']
    
    # set the index of sliced df by copying column names and rename column :  
    df1.set_index(df.columns, inplace=True)
    df1.index.name = 'Time'
    df1.columns = ['NADH@abs']
        
    # add column with wavelenght at the maximum absorption
    df1['NADH@max'] = truncated_data.idxmax()
#     df1.to_csv(path + df + ".csv",  header = True)
    return df1

def cleaning(df):
    df.index.rename('Wavelength', inplace=True)
    df1 = df.reset_index()
    df2 = df1.round({'Wavelength':0})
    df3 = df2.drop_duplicates( 'Wavelength', keep='first').set_index('Wavelength')
    df4 = df3.loc[0:1500, :]
    #df5 = df4.iloc[:, 0:len(fiveC)]
    roundcol = [round(x, 1) for x in df4.columns]
    df4.columns = roundcol
    return(df4)


def smoothing(cleaned, i):
    smoothed = []
    for column in cleaned:
        col = cleaned.loc[:, column]
        smoothing = gaussian_filter1d(col, sigma=i, axis = 0)
        liste = list(smoothing)
        smoothed.append(liste)  
    df = pd.DataFrame(index = range(300, 1096))
    for i, x in zip(cleaned, range(len(cleaned.columns)+1)):
        df[i] = smoothed[x]
    return(df)

def normalize_max(data):
    # normalize each dataframe by the maximum value
    data_norm = data.apply(lambda x: x/x.max(), axis=0)
    return data_norm

def R_get(data):
        R = data.iloc[650,] / data.max()
        return R

def add_comma(file):
    filename_with_extension = os.path.basename(file)
    filename_witout_extension = os.path.splitext(filename_with_extension)[0]
    pathway = os.path.dirname(file)
    new_filename = pathway +  "/" + filename_witout_extension +  "copy" + ".csv"
    outfile=open(new_filename,"w+")
    with open(file,"r") as infile:
        lines=infile.readlines()
        for n, l in enumerate(lines,1):
            if "Name,," in l:
                outfile.write(l)
            elif "Name," in l:
                l1= l.replace("Name","Name,")
                outfile.write(l1)  
            else:
                outfile.write(l)
        return(new_filename)    
        
def import_kinetics(file, skip):
    df = pd.read_csv(file,
                     sep = ",", engine = "python", skiprows = skip, skip_blank_lines = True, keep_default_na = True)  
    return(df)

"""Tidy Dataframe from Cary csv KINETICS file. Returns a list of dataframes for each sample"""

def cleaning_kinetics(df, samples):
    df1 = df.iloc[:, 1::2].iloc[:, ::len(samples)]
    df1.dropna(axis = 1, how = "all", inplace = True)
    df1.dropna(axis = 0, how = "all", inplace = True)
    timestamps = pd.to_datetime(df1.iloc[0], format = "%Y-%m-%d %H:%M:%S (%z)")
    Wavelength = df1.iloc[7:, 1].astype("int64")
    
    minutes = []
    for i in timestamps:
        time_step = i - timestamps[0]
        minute = round(float(time_step.total_seconds())/60, 1)
        minutes.append(minute)
        
    dfs = []
    names = samples

    for i in names:
        experiment = df.filter(like = i).iloc[7:]
        for x in experiment:
            experiment[x] = pd.to_numeric(experiment[x])
        experiment.dropna(axis = 1, how = "all", inplace = True)
        experiment.dropna(axis = 0, how = "all", inplace = True)
        experiment.index = Wavelength
        experiment.index.rename("Wavelength (nm)", inplace =True)
        experiment.columns = minutes
        experiment = experiment.iloc[::-1]
        dfs.append(experiment)
    if len(dfs) == 1:
        return(dfs[0])
    else:
        return(dfs)

def C2K(C): 
    '''
    Function to convert temperature from degree Celsius to Kelvin. 
    '''
    return (C + 273.15) 


def func(x, y0, A1, t1):
    '''
    Exponential decay function
    '''
    y = A1*np.exp(-x/t1) + y0
    return(y)

