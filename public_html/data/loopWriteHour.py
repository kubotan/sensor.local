#!/usr/bin/python3
# -*- coding:utf-8 -*-

import csv
import json
import os
import time
import re
import sys
import serial
import pandas as pd
import numpy as np

def validateCols(cols):
    for col in cols[1:len(cols)]:
      try:
        float(col)
      except:
        return False
    return True

if __name__ == '__main__':

  jsonFile = '/var/www/html/data/hour.json'
  tmpFile = jsonFile + '.tmp'
  numberOfCommaInCsv = 8   # with datetime columns.
  last = 100
  float64Cols = ['TEMPERATURE', 'HUMIDITY','PRESSURE','CO2','LUX','CPM','USV']
  interval = 40

  while True:
    time.sleep(interval)
    df = pd.read_json(jsonFile)
    df.columns = ['DATETIME', 'TEMPERATURE', 'HUMIDITY','PRESSURE','CO2','LUX','CPM','USV'] 
    df[float64Cols] = df[float64Cols].astype(np.float64)
    df = df.tail(last - 1)

    with open('/var/www/html/data/latest') as ser:
      csvRow = ser.readline()
      cols = csvRow.strip().split(',') 
      if validateCols(cols) == True and len(cols) == numberOfCommaInCsv:
        dLine = pd.DataFrame([cols], columns=df.columns.tolist(), dtype=np.float64)
        df = df.append(dLine, ignore_index=True)
        df = df.round(3)
        with open(tmpFile, 'w') as f:
          json.dump(df.values.tolist(), f, ensure_ascii=True)
        os.rename(tmpFile, jsonFile)
        os.chmod(jsonFile, 0o777)
sys.exit()
