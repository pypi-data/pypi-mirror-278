
### Code for running 'auto_osESD'.
### Results will appear in 'osESD_test_results' if not provided otherwise.

############################################################
############################################################
############################################################
############################################################


import os
import numpy as np
import pandas as pd

import time as t
from models import osESD_Detector, auto_osESD_Detector
from utils import data_aug
from utils import scores_module
from utils import plotting_modules

def osESD(dataset, data_name, plot=False, labeled=True, result_directory='osESD_results', value_name='value',
        timestamp_name='timestamps', anomaly_name='anomaly', size=100, condition=False, dwin=5,
        rwin=5,maxr=10, alpha=0.01):

    if value_name not in dataset.columns:
        raise ValueError("Value column can not be found. Please specify column name with time series values as \'value_name\'.")

    if anomaly_name not in dataset.columns:
        raise ValueError("Anomaly column can not be found. Please specify column name with time series values as \'anomaly_name\'.")
    

    df = dataset
    # data_name = dataset.split("//")[-1][:-4]

    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    ### Add timestamps to dataset if not labeled.
    if timestamp_name in df.columns:
        df['timestamps']=df[timestamp_name]
    else:
        df['timestamps']=[i for i in range(1,len(df)+1)]

    ### Deal with whether dataset is labeled or not. If labeled, then f1-scores will be returned as well.
    ### If not, then only index and a plot of predicted anomalies will be returned.
    if labeled:
        df[['value','anomaly']]=df[[value_name,anomaly_name]]
    else:
        df['value']=df[value_name]

    ### Run osESD with designated parameters. The indices of anomalies will be returned to 'predictions'.
    T1 = t.time()
    predictions = osESD_Detector.osESD(data=list(df['value']),
                                    time=list(df['timestamps']),
                                    train_size=size, condition=condition,
                                    dwins=dwin, rwins=rwin,
                                    alpha=alpha, maxr=maxr)
    T2 = t.time()

    ### Change the indices to a list of 0's and 1's of anomalies.
    pred_index = data_aug.change_to_index(predictions, len(df))
    pred_index = pred_index[size:]

    ### Export txt file.
    Results = ""
    if labeled:
        real_index = df['anomaly'][size:]
        results = scores_module.return_PRF_values(real_index, pred_index, T1, T2)
        Results = '\nPrecision : {:.4f}, Recall : {:.4f}, F1-score : {:.4f}, Time {:.4f} (sec)'.format(results[2],results[3],results[4],results[5])
        Results += "\n\nReal : [ "
        reals = np.where(df['anomaly'] == 1)
        Results += ', '.join([str(i) for i in reals[0]]) + " ]"
    Results += "\n\nAnomalies : [ "
    Results += ', '.join([str(i) for i in predictions]) + " ]"

    file_path = result_directory+"//"+data_name+"_osESD_result.txt"
    with open(file_path, "w") as file:
        file.write(Results)

    ### Export plot
    if plot:
        df['predictions'] = data_aug.change_to_index(predictions, len(df))
        plotting_modules.save_plot(data_path=data_name,column_name='predictions',
                                   df=df,save_path=result_directory+'//', model_name='osESD')

    print("Test successfully done.")
    print("Results can be seen in "+result_directory+" .")
    return predictions


def auto_osESD(dataset, data_name, plot=True, labeled=True, result_directory='auto_osESD_results', value_name='value',
         timestamp_name='timestamps', anomaly_name='anomaly', sizes=[], conditions=[], dwins=[],
         rwins=[], maxrs=[], alphas=[], weights=[0,0,1,0.01], learning_length=0.2,
         min_max_switch=False):
    
    if value_name not in dataset.columns:
        raise ValueError("Value column can not be found. Please specify column name with time series values as \'value_name\'.")

    if anomaly_name not in dataset.columns:
        raise ValueError("Anomaly column can not be found. Please specify column name with time series values as \'anomaly_name\'.")



    ### Read dataset.
    df = dataset
    # data_name = dataset.split("//")[-1]
    # print(data_name)
    # adsaasd
    ### Add timestamps to dataset if not labeled.
    if timestamp_name in df.columns:
        df['timestamps'] = df[timestamp_name]
    else:
        df['timestamps'] = [i for i in range(1, len(df) + 1)]

    ### Deal with whether dataset is labeled or not. If labeled, then f1-scores will be returned as well.
    ### If not, then only index and a plot of predicted anomalies will be returned.
    if labeled:
        df[['value', 'anomaly']] = df[[value_name, anomaly_name]]
    else:
        df['value'] = df[value_name]

    ### If condition is not explicitly provided, use parameters set within 'auto_osESD' implementation.
    if sizes == [] and conditions == [] and dwins == [] and rwins == [] and maxrs == [] and alphas == [] :
        parameters = []
    else:

        if not sizes:
            sizes = [50, 100, 150, 200]

        if not conditions:
            conditions = [True, False]

        if not dwins:
            dwins = [2, 5, 10, 30]

        if not rwins:
            rwins = [4, 5, 10, 30]

        if not maxrs:
            maxrs = [3, 5, 7, 10]

        if not alphas:
            alphas = [0.001, 0.005, 0.01, 0.05]

        if min(sizes)<50:
            raise ValueError("Minimum value of windows should be above 50 for stable learning. Please adjust \"sizes\" as such.")

        if min(sizes)<min(max(rwins),max(dwins)) :
            raise ValueError("Minimum value of windows should be above maximum value of both R windows and D windows. Please adjust \"dwins\" and \"rwins\" as such.")


        if not os.path.exists(result_directory):
            os.makedirs(result_directory)

        sizes.sort()
        dwins.sort()
        rwins.sort()
        maxrs.sort()
        alphas.sort()

        

        # new_sizes = []
        # for i in sizes:
        #     if i>=50:
        #         new_sizes.append(i)
        # sizes = new_sizes

        parameters = [
            ["--WindowSizes", sizes],
            ["--AndOr", conditions],
            ["--MaxRs", maxrs],
            ["--Dwins", dwins],
            ["--Rwins", rwins],
            ["--Alphas", alphas]
        ]

    ### Run function 'osESD_Detector_auto' which will return [anomaly_list, anomaly_indices, best_parameters].
    ### Then use best_parameters (tuning_results[2]) to find final anomalies in full dataset.
    T1 = t.time()
    tuning_results = auto_osESD_Detector.osESD_Detector_auto(database=df, data_label=labeled,
                                                             weights=weights,
                                                             par_len=learning_length,
                                                             parameters=parameters, min_max_switch=min_max_switch)
    tuning_params = tuning_results[2]
    predictions = auto_osESD_Detector.run_osESD_modified(data=list(df['value']), time=list(df['timestamps']),
                                                        full_size=len(df), init_size=tuning_params[1],
                                                        params=tuning_params)
    T2 = t.time()

    pred_index = np.where(np.array(predictions)==1)

    Results = ""
    if labeled:
        real_index = df['anomaly'][tuning_params[1]:]
        results = scores_module.return_PRF_values(real_index, predictions[tuning_params[1]:], T1, T2)
        Results = '\nPrecision : {:.4f}, Recall : {:.4f}, F1-score : {:.4f}, Time {:.4f} (sec)'.format(results[2],results[3],results[4],results[5])
        Results += "\n\nReal : [ "
        reals = np.where(df['anomaly'] == 1)
        Results += ', '.join([str(i) for i in reals[0]]) + " ]"

    Results += "\n\nAnomalies : [ "
    Results += ', '.join([str(i) for i in list(pred_index[0])]) + " ]"

    file_path = result_directory+"//"+data_name[:-4]+"_auto_osESD_result.txt"
    with open(file_path, "w") as file:
        file.write(Results)

    if plot:
        df['predictions'] = predictions
        plotting_modules.save_plot(data_path=data_name,column_name='predictions',
                                   df=df,save_path=result_directory+'//', model_name='auto_osESD')

    print("Test successfully done.")
    print("Results can be seen in "+result_directory+" .")

    return pred_index


