
# Automated Online Sequential ESD (Python)

This package includes Python codes for online sequential ESD(osESD), a variation of GESD tests.
It is a accurate and efficient way to detect anomalies in an univariate time series dataset.


We provide the basic function `osESD` and an automated grid search method `auto-osESD`.
`auto-osESD` can be used to find the best parameters for a specific dataset,  
using basic parameters or parameters provided explicitly by the user.  


## Installation

### 1. Download library.
Download osESD library using pip.
```
pip install osESD
```


### 2. Import function.
Import function in python code.
`osESD` is for a single online sequential ESD test, and will return indices of the anomalies.
Also, it will produce a text file with these anomalies in the designated output file (default 'osESD_results').
`auto_osESD` is for convenient tuning of `osESD`, and will run with default parameters if not specified otherwise.

```
from osESD import osESD, auto_osESD
```


### 3. Run on dataset.
Read data and run it using `osESD`.
The model is designed to run on univarites time series dataset in a csv. fashion.
Imported csv. dataset and custom name of the dataset should be entered. Also, the name of the column with values should be entered to 'value_name' and the name of the column with anomaly values should be entered as 'anomaly_name'.

```
import os
import pandas as pd

from osESD import osESD, auto_osESD

os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv("ARIMA1_ber_1.csv")
anoms_1 = osESD(df,"A2_benchmark", value_name='value',anomaly_name='anomaly')
print(anoms_1)

anoms_2 = osESD(df,"A2_benchmark", value_name='value',anomaly_name='anomaly',size=100, dwin=5, rwin=5, maxr=6, alpha=0.01)
print(anoms_2)

auto_anoms_1 = auto_osESD(df,"A2_benchmark_auto")
print(auto_anoms_1)

auto_anoms_2 = auto_osESD(df,"A2_benchmark_auto", size=[20,50,100,150],conditions=[True,False],alphas=[0.001,0.01],weights=[0,0,1,0],learning_length=0.3)
print(auto_anoms_2)

```

## Versions
```
Python = 3.8.16    
argparse = 1.1  
numpy = 1.24.3  
pandas = 1.5.3  
torch = 1.13.1  
matplotlib = 3.7.0  
scikit-learn = 1.2.1  
scipy = 1.10.1  
rrcf = 0.4.4  
```

## License
```
License :: OSI Approved :: MIT License
Operating System :: OS Independent
```

## Acknowledgements
```
This work was supported by the Ministry of Education of the Republic of Korea 
and the National Research Foundation of Korea (NRF-2018R1A5A7059549). 
This work was also supported by `Human Resources Program in Energy Technology' 
of the Korea Institute of Energy, Technology Evaluation and Planning (KETEP), 
and was granted financial resources from the Ministry of Trade, 
Industry $\&$ Energy, Republic of Korea (No. 20204010600090).

Related research and tests were mainly done in 
Intelligent Data Systems Laboratory in Hanyang University, Seoul, South Korea.
```

## References
Paper (currently under revision).

