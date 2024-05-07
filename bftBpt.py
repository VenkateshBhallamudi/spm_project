import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import argrelextrema
import spmEntry as se
import spmParsers as sp
from math import isnan

def filter_speed_values(values_list=[]):
    prevIndex = float('-inf')
    prevSpeed = float('-inf')
    indexList = []
    value_ret_list = []
    for i, value in enumerate(values_list):
        if(not isnan(value)):
            #if(prevIndex == float('-inf') or (i-prevIndex > 10)):
                indexList.append(i)
                value_ret_list.append(value)
                #prevIndex = i
                #prevSpeed = value

    return (indexList, value_ret_list)

def filter_bft_value(maxima_index_list=[], maxima_value_list=[], minima_index_list=[], minima_value_list=[]):
    filtered_maxima_list = []
    filtered_maxima_indices_list = []
    filtered_minima_list = []
    filtered_minima_indices_list = []

    for i, maxima_value in enumerate(maxima_value_list):
        if(maxima_value >= 7 and maxima_value <= 20):
            filtered_maxima_indices_list.append(maxima_index_list[i])
            filtered_maxima_list.append(maxima_value_list[i])

    for i, minima_value in enumerate(minima_value_list):
        if(minima_value >= 0 and minima_value <= 10):
            filtered_minima_indices_list.append(minima_index_list[i])
            filtered_minima_list.append(minima_value_list[i])

    return (filtered_maxima_indices_list, filtered_maxima_list, filtered_minima_indices_list, filtered_minima_list)

def filter_bpt_value(maxima_index_list=[], maxima_value_list=[], minima_index_list=[], minima_value_list=[], service='GOODS'):
    filtered_maxima_list = []
    filtered_maxima_indices_list = []
    filtered_minima_list = []
    filtered_minima_indices_list = []

    if service == 'GOODS':
        for i, maxima_value in enumerate(maxima_value_list):
            if(maxima_value >= 30 and maxima_value <= 60):
                filtered_maxima_indices_list.append(maxima_index_list[i])
                filtered_maxima_list.append(maxima_value_list[i])

        for i, minima_value in enumerate(minima_value_list):
            if(minima_value >= 0 and minima_value <= 35):
                filtered_minima_indices_list.append(minima_index_list[i])
                filtered_minima_list.append(minima_value_list[i])
    else:
        for i, maxima_value in enumerate(maxima_value_list):
            if(maxima_value >= 45 and maxima_value <= 75):
                filtered_maxima_indices_list.append(maxima_index_list[i])
                filtered_maxima_list.append(maxima_value_list[i])

        for i, minima_value in enumerate(minima_value_list):
            if(minima_value >= 0 and minima_value <= 38):
                filtered_minima_indices_list.append(minima_index_list[i])
                filtered_minima_list.append(minima_value_list[i])

    return (filtered_maxima_indices_list, filtered_maxima_list, filtered_minima_indices_list, filtered_minima_list)

def find_bft_bpt(filtered_maxima_indices_list, filtered_maxima_list, filtered_minima_indices_list, filtered_minima_list, cum_distance_vals):
    for i, filtered_maxima_index in enumerate(filtered_maxima_indices_list):
        for j, filtered_minima_index in enumerate(filtered_minima_indices_list):
            if(filtered_minima_index > filtered_maxima_index):
                if(filtered_minima_list[j] < filtered_maxima_list[i]*0.7 and (cum_distance_vals[filtered_minima_index] - cum_distance_vals[filtered_maxima_index]) < 1500):
                    print(f'{cum_distance_vals[filtered_minima_index]}, {cum_distance_vals[filtered_maxima_index]}')
                    return (filtered_maxima_index, filtered_maxima_list[i], filtered_minima_index, filtered_minima_list[j])
    
    return (-1,-1,-1,-1)

def find_bft_bpt_tuples(listSpmEntryRecords=[], service='GOODS'):
    xs = []
    cum_distance_vals = []
    for spmEntryRecord in listSpmEntryRecords:
        xs.append(spmEntryRecord.entrySpeed)
        cum_distance_vals.append(spmEntryRecord.entryCumDist)

    df = pd.DataFrame(xs, columns=['speed'])

    n = 30
    df['min'] = df.iloc[argrelextrema(df.speed.values, np.less_equal,
                        order=n)[0]]['speed']
    df['max'] = df.iloc[argrelextrema(df.speed.values, np.greater_equal,
                        order=n)[0]]['speed']
    
    maxima_values = df['max'].tolist()
    minima_values = df['min'].tolist()
    maxima_indices_list, maxima_speed_list = filter_speed_values(maxima_values)
    minima_indices_list, minima_speed_list = filter_speed_values(minima_values)

    bft_max_indices, bft_max_values, bft_min_indices, bft_min_values = filter_bft_value(maxima_indices_list, maxima_speed_list, minima_indices_list, minima_speed_list)
    bpt_max_indices, bpt_max_values, bpt_min_indices, bpt_min_values = filter_bpt_value(maxima_indices_list, maxima_speed_list, minima_indices_list, minima_speed_list, service)

    bft_start_index, bft_start_speed, bft_end_index, bft_end_speed = find_bft_bpt(bft_max_indices, bft_max_values, bft_min_indices, bft_min_values, cum_distance_vals)
    bpt_start_index, bpt_start_speed, bpt_end_index, bpt_end_speed = find_bft_bpt(bpt_max_indices, bpt_max_values, bpt_min_indices, bpt_min_values, cum_distance_vals)

    return [(bft_start_index, bft_end_index), (bpt_start_index, bpt_end_index)]

if __name__ == '__main__':
    spmEntryRecords = sp.medhaParser('D:/Pydir/SPM_RAW/medha.txt')
    date_time_vals = []
    speed_vals = []
    inst_dist_vals = []
    cum_dist_vals = []
    index_list = []
    for i, spmEntryRecord in enumerate(spmEntryRecords):
        date_time_vals.append(spmEntryRecord.entryDate)
        speed_vals.append(spmEntryRecord.entrySpeed)
        inst_dist_vals.append(spmEntryRecord.entryInstDist)
        cum_dist_vals.append(spmEntryRecord.entryCumDist)
        index_list.append(i)

    bft_bpt_list = find_bft_bpt_tuples(spmEntryRecords, 'COACHING')
    bft_tuple = bft_bpt_list[0]
    bpt_tuple = bft_bpt_list[1]

    spm_start_time = date_time_vals[0]
    spm_start_distance = cum_dist_vals[0]

    bft_start_index = bft_tuple[0]
    bft_end_index = bft_tuple[1]
    
    bft_start_distance = cum_dist_vals[bft_start_index]
    bft_end_distance = cum_dist_vals[bft_end_index]

    bft_start_time = date_time_vals[bft_start_index]
    bft_end_time = date_time_vals[bft_end_index]

    bpt_start_index = bpt_tuple[0]
    bpt_end_index = bpt_tuple[1]
    
    bpt_start_distance = cum_dist_vals[bpt_start_index]
    bpt_end_distance = cum_dist_vals[bpt_end_index]

    bpt_start_time = date_time_vals[bpt_start_index]
    bpt_end_time = date_time_vals[bpt_end_index]

    #if(bft_start_distance - spm_start_distance < 5000 and bft_end_distance - bft_start_distance < 500):
    plt.scatter(bft_start_index, speed_vals[bft_start_index], c='r')
    plt.scatter(bft_end_index, speed_vals[bft_end_index], c='b')
    
    #if(bpt_start_distance - spm_start_distance < 10000 and bpt_end_distance - bpt_start_distance < 1000):
    plt.scatter(bpt_start_index, speed_vals[bpt_start_index], c='y')
    plt.scatter(bpt_end_index, speed_vals[bpt_end_index], c='g')

    plt.plot(index_list, speed_vals)
    plt.grid()
    plt.show()