#!/usr/bin/python3
# -*- coding:utf-8 -*-

import csv
import json
import os
import re
import sys
import serial
import pandas as pd
import numpy as np
import time
import requests
from pathlib import Path

def validateCols(cols):
    for col in cols[1:len(cols)]:
      try:
        float(col)
      except:
        return False
    return True

if __name__ == '__main__':

  args = sys.argv
  if len(args) != 2:
    sys.stderr.write('Invalid argument.\n')
    sys.exit()
  jsonFile = args[1]
  tmpFile = jsonFile + '.tmp'
  limitRetry = 5
  numberOfCommaInCsv = 8   # with datetime columns.
  last = 100
  float64Cols = ['TEMPERATURE', 'HUMIDITY','PRESSURE','CO2','LUX','CPM','USV']

  df = pd.read_json(jsonFile)
  df.columns = ['DATETIME', 'TEMPERATURE', 'HUMIDITY','PRESSURE','CO2','LUX','CPM','USV'] 
  df[float64Cols] = df[float64Cols].astype(np.float64)
  last=last - 1   # offset new line
  df = df.tail(last)

  with open('/var/www/html/data/latest') as ser:

    countRetry = 0
    while countRetry <= limitRetry:
      csvRow = ser.readline()
      cols = csvRow.strip().split(',') 
      if validateCols(cols) == True and len(cols) == numberOfCommaInCsv:
        dLine = pd.DataFrame([cols], columns=df.columns.tolist(), dtype=np.float64)
        df = df.append(dLine, ignore_index=True)
        df = df.round(3)
        with open(tmpFile, 'w') as f:
          json.dump(df.values.tolist(), f, ensure_ascii=False, indent=2, sort_keys=True)
        os.rename(tmpFile, jsonFile)
        os.chmod(jsonFile, 0o777)
        break
      else:
        countRetry += 1
sys.exit()
