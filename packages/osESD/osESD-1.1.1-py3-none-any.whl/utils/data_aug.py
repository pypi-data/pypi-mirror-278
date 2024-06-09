


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from scipy.stats import norm
from datetime import datetime
warnings.filterwarnings(action='ignore')

def bernoulli():
    return np.random.choice([-1, 1], 10000, p=[0.5, 0.5])

def uniform():
    return np.random.uniform(-1, 1, 10000)

def linear():
    L = 10000
    x = np.arange(1, L + 1)
    probs = np.linspace(0, 1, L)
    probs = probs / np.sum(probs)
    samples = np.random.choice(x / L, size=L, replace=True, p=probs)
    signs = bernoulli()
    return samples * signs

def quadratic():
    L = 10000
    x = np.arange(1, L + 1)
    probs = np.linspace(0, 1, L)
    probs = (probs ** 2) / np.sum(probs ** 2)
    samples = np.random.choice(x / L, size=L, replace=True, p=probs)
    signs = bernoulli()
    return samples * signs

# def add_timestamp(dataframe):
#     try:
#         dataframe = dataframe[['timestamps','value','anomaly']]
#     except:
#         dataframe = dataframe[['value','anomaly']]
#         dataframe['timestamps']=[i for i in range(1,len(dataframe)+1)]
#     return dataframe

def add_timestamp(dataframe):
    if 'timestamps' not in dataframe.columns:
        dataframe['timestamps'] = [i for i in range(1, len(dataframe) + 1)]
    return dataframe

def change_to_timestamp(df,column,format):
    df['timestamps'] = df[column].apply(lambda x:datetime.timestamp(datetime.strptime(x,format)))
    return df

def change_to_index(values, length):
    temp = [0 for _ in range(length)]
    for i in values:
        temp[i] = 1
    return temp

# def change_to_value(indices, length):
#     temp

def math_round(x):
    M = x//1
    return M if x-M<0.5 else M+1

def contaminate(ts, alpha, anom_percent, func):

    def update(List, old_mean, old_sd, new_val):
        # print(new_val, old_mean)
        Len = len(List)
        new_std = np.sqrt(((Len - 1) / Len) * old_sd ** 2 + (1 / (Len + 1)) * (new_val - old_mean) ** 2)
        new_mean = old_mean * (Len) / (Len + 1) + new_val / (Len + 1)
        List.append(new_val)
        return {'mean': new_mean, 'sd': new_std, 'List': List}

    L = len(ts)

    X_t = [ts[0]]
    X_t_mean = ts[0]
    X_t_sd = 0

    anomal_index = []
    randoms = np.random.uniform(0, 1, L)

    if func.lower() in ['bernoulli', 'ber']:
        samples = bernoulli()
    elif func.lower() in ['uniform', 'uni']:
        samples = uniform()
    elif func.lower() in ['linear', 'lin']:
        samples = linear()
    elif func.lower() in ['quadratic', 'quad']:
        samples = quadratic()
    else:
        raise ValueError("Anomaly generating function must be 'Bernoulli', 'Uniform', 'Linear', or 'Quadratic'.")

    for i in range(1, L):
        new_vals = update(X_t, X_t_mean, X_t_sd, ts[i])
        X_t_mean = new_vals['mean']
        X_t_sd = new_vals['sd']
        X_t = new_vals['List']
        if randoms[i] < anom_percent:
            multiplier = np.random.choice(samples, 1)
            anomal_index.append(i)
            ts[i] = ts[i] + (multiplier * norm.ppf(1 - alpha / 2, loc=0, scale=X_t_sd))

    anomal_val = np.zeros(len(ts))
    anomal_val[anomal_index] = 1
    anomal_val = pd.Series(anomal_val, dtype='category')
    return {'value': ts, 'anomaly': anomal_val}


if __name__ == "__main__":
    plt.hist(bernoulli(), bins=100)
    plt.savefig(fname='..//results//plots//bernoulli_distribution.png')
    plt.show()

    plt.hist(uniform(), bins=100)
    plt.savefig(fname='..//results//plots//uniform_distribution.png')
    plt.show()

    plt.hist(linear(), bins=100)
    plt.savefig(fname='..//results//plots//linear_distribution.png')
    plt.show()

    plt.hist(quadratic(), bins=100)
    plt.savefig(fname='..//results//plots//quadratic_distribution.png')
    plt.show()





