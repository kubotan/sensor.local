#!/usr/bin/python3
# -*- coding:utf-8 -*-

import csv
import datetime
import os
import sys
import serial
from serial.tools import list_ports
import time
import traceback

def getSerial(ser):

  port = '/dev/ttyACM0'
  devices = list_ports.comports()
  for device in devices:
    if device.usb_description().startswith('ttyACM0'):
      port = device[0]

  if ser is None or ser.isOpen() is False:
    return serial.Serial(
      port = port,
      baudrate = 9600,
      parity = serial.PARITY_NONE,
      bytesize = serial.EIGHTBITS,
      stopbits = serial.STOPBITS_ONE,
      timeout = 1,
      xonxoff = 0,
      rtscts = 0,
    )
  elif ser is not None or ser.isOpen() is True:
    return ser

def validateCols(cols):
    for col in cols[1:len(cols)]:
      try:
        float(col)
      except:
        return False
    return True

if __name__ == '__main__':

  numberOfCommaInCsv = 8   # with datetime columns.
  latestFile= '/var/www/html/data/latest'
  tmpFile= latestFile + '.tmp'
  ser = None
  isError=False

  while True:
    time.sleep(2)
    try:
      ser=getSerial(ser)
      serLine=ser.readline().decode('utf-8')
      csvRow = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ',' + serLine
    except serial.serialutil.SerialException as e:
      print(traceback.format_exc())
      csvRow = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ',0,0,0,0,0,0,0,0'
      ser=None
    cols = csvRow.strip().split(',') 
    if validateCols(cols) == True and len(cols) == numberOfCommaInCsv:
      with open(tmpFile, 'w') as f:
        f.write(csvRow)
      os.rename(tmpFile, latestFile)
      os.chmod(latestFile, 0o777)
sys.exit()
