#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# logging.warning
import logging
# zip file support
import zipfile
from os.path import basename, splitext
# string => StringIO => pandas.Dataframe
import pandas as pd #, numpy as np
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class IGRA2Parser(object):
    ''' primary object for parsing igra2 derived files, this class
    is primarily responsible for opening a file, splitting it and
    handing off each line to ish_report, which process the specific
    igra2 report '''

    DATA_COLUMNS = (
        'PRESS' , 'REPGPH' , 'CALCGPH', 'TEMP', 'TEMPGRAD',
        'PTEMP', 'PTEMPGRAD', 'VTEMP', 'VPTEMP', 'VAPPRESS',
        'SATVAP', 'REPRH', 'CALCRH', 'RHGRAD', 'UWND',
        'UWDGRAD', 'VWND', 'VWNDGRAD', 'N',
    )

    HEADER_COLUMNS = (
        'ID', 'YEAR', 'MONTH', 'DAY', 'HOUR',
        'RELTIME', 'NUMLEV', 'PW', 'INVPRESS', 'INVHGT',
        'INVTEMPDIF', 'MIXPRESS', 'MIXHGT', 'FRZPRESS', 'FRZHGT',
        'LCLPRESS', 'LCLHGT', 'LFCPRESS', 'LFCHGT', 'LNBPRESS',
        'LNBHGT', 'LI', 'SI', 'KI', 'TTI',
        'CAPE', 'CIN',
    )

    def __init__(self):
        self._header = pd.DataFrame(columns=self.HEADER_COLUMNS)
        self._data = []
        self.length = 0
        return

    def __len__(self):
        return self.length

    def get_header(self, i):
        return self._header.loc[i, :]

    def get_data(self, i):
        if np.isnan(i): return None
        if instance(i, float): i = int(i)
        return self._data[i]

    def load(self, file_path):
        ''' load function
        load data from zip/txt file and parse them towards reports
        '''

        # file info
        file_ext = splitext(file_path)[1]
        # compressed zip or not?
        if file_ext == '.zip':
            print('loading zip file: {}'.format(basename(file_path)))
            file_name = basename(splitext(file_path)[0])
            with zipfile.ZipFile(file_path, 'r') as archive:
                contents = bytes.decode(archive.read(file_name))
            archive.close()
        else:
            print('loading plain file: {}'.format(basename(file_path)))
            with open(file_path, 'r') as fp:
              contents = fp.read()
            fp.close()

        # split it to daily parts
        records = contents.split('#')
        print('parsing records to pandas.DataFrame')
        # parsing to dataframes
        for i in range(1, len(records)):
            # print progress
            if not(i % 300): print('parsing the {}-th record'.format(i))
            # parse NaN
            record = records[i].replace('-99999', '    NA')
            # retreive header & data
            [header, data] = record.split('\n', 1)
            header = pd.read_csv(StringIO(header), header=None, index_col=None, delim_whitespace=True)
            header.columns = self.HEADER_COLUMNS
            data = pd.read_csv(StringIO(data), header=None, index_col=None, delim_whitespace=True)
            data.columns = self.DATA_COLUMNS
            data.index = data.PRESS
            self._header = self._header.append(header)
            self._data.append(data)

        # set header index
        #self._header.index = pd.to_datetime(self._header[['YEAR','MONTH','DAY','HOUR']])
        self.length = len(self._header)
        self._header.index = range(self.length)
        # logging
        if len(self._header) == len(self._data):
            print('all {} records parsed'.format(len(records)-1))
        else:
            logging.error('The length of headers is NOT equal to the length of data!')

        return
