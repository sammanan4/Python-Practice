filepath_small = '/home/sammanan4/Downloads/companies1.csv'
piklepath = '/home/sammanan4/Downloads/companies1.pikle'
filepath = '/home/sammanan4/Desktop/data_generated.csv'

from ctypes import sizeof
from datetime import time
import timeit
from numpy import number
import pandas as pd
import pickle
import csv
import sys

def pikletiming():
    time1 = timeit.timeit('pd.read_csv(filepath)', number=1000, globals={'pd': pd, 'filepath': filepath_small})
    time2 = timeit.timeit('f=open(piklepath, "rb");pickle.load(f);f.close();', number=1000, globals={'pickle': pickle, 'piklepath': piklepath})

    print(f"pandas took {time1} seconds to read", f"\npickle took {time2} seconds to read")


def mem_eff():
    df = pd.read_csv(filepath)

    with open(filepath) as csv_file:    
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        # d = {'id': [], 'company_name': [], 'city': [], 'country': [], 'date_creation': [], 'yearly_revenue': [], 'number_of_employees': []}
        d = {"id": [], "dob": [], "fname": []}
        for row in csv_reader:
            for k,v in row.items():
                d[k].append(v)
    
    size = 0
    for i in d.items():
        size+=sys.getsizeof(i[1])
    
    
    print("dictionary takes ", size/(1024*1024), " MB space")
    print("dataframe takes ", sys.getsizeof(df)/(1024*1024), " MB space")


def time_eff():
    def df_time(pd, filepath):
        pd.read_csv(filepath)

    def dikt_time(csv, filepath): 
        with open(filepath) as csv_file:        
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            # d = {'id': [], 'company_name': [], 'city': [], 'country': [], 'date_creation': [], 'yearly_revenue': [], 'number_of_employees': []}
            d = {"id": [], "dob": [], "fname": []}
            for row in csv_reader:
                for k,v in row.items():
                    d[k].append(v)
    
    time1 = timeit.timeit('df_time(pd, filepath)', number=10, globals={'pd': pd, 'filepath': filepath, 'df_time': df_time})
    time2 = timeit.timeit('dikt_time(csv, filepath)', number=10, globals={'csv': csv, 'filepath': filepath, 'dikt_time': dikt_time})

    print(f"pandas takes {time1} seconds to read", f"\nDictReader takes {time2} seconds to read")

def time_to_create_dataset():
    def timer():
        l = []
        for i in range(0, 100000):
            l.append([k for k in range(5)])
        d = {"1": [], "2":[], "3":[], "4":[], "5": []}
        for row in l:
            d['1'].append(row[0])
            d['2'].append(row[1])
            d['3'].append(row[2])
            d['4'].append(row[3])
            d['5'].append(row[4])

    def timerdf(pd):
        l = []
        for i in range(0, 100000):
            l.append([k for k in range(5)])
        pd.DataFrame(l, columns=["1", "2", "3", "4", "5"])
        
    print(timeit.timeit('timer()', number=100, globals={"timer":timer}))
    print(timeit.timeit('timerdf(pd)', number=100, globals={"timerdf":timerdf, 'pd':pd}))


# pikletiming()
# mem_eff()
# time_eff()

# df = pd.read_csv('/home/sammanan4/Documents/Office/TDMS/CloudTDMS_V2/CloudTDMS/libraries/datafolder/cities.csv')#, dtype={"country": "category"})
# df_optimized = pd.read_csv('/home/sammanan4/Documents/Office/TDMS/CloudTDMS_V2/CloudTDMS/libraries/datafolder/cities.csv', dtype={"country": "category", "currency": "category", "lat": "float32", "lon": "float32"})
# print(sys.getsizeof(df_optimized)/(1024*1024))
# print(df_optimized.memory_usage(index=True, deep=True))
# print(df.dtypes)
files = [("~/Desktop/col1.csv", "name"), ("~/Desktop/col2.csv", "age"), ("~/Desktop/col3.csv", "lang")]
readers = []
chunksize = 4
number_of_rows = 9
for x in files:
    readers.append(pd.read_csv(x[0], chunksize=chunksize))
import math
iterations = math.ceil(number_of_rows/chunksize)
for i in range(iterations):

    newdf = pd.DataFrame()
    
    for col,col_name in zip(readers, files):
        newdf[col_name[1]] = list(next(col)[col_name[1]])
    
    print(newdf)


# reader = pd.read_csv(filepath_small, chunksize=10)
# print(sys.getsizeof(reader))
# print(next(reader))
# print(next(reader))
# print(reader)
# df_orig = pd.read_csv(filepath)
# print(sys.getsizeof(df))
# print(sys.getsizeof(df_orig))
# for reader in df:
#     print(type(reader))

# import pdfkit

# pdfkit.from_file("/home/sammanan4/Desktop/profile_report.html", "profile_report.pdf")