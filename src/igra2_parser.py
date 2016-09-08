#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# logging.warning
import logging
# zip file support
import zipfile
from os.path import basename, splitext
# string => StringIO => pandas.Dataframe
import pandas, numpy
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
        self._header = pandas.DataFrame(columns=self.HEADER_COLUMNS)
        self._data = []

        return

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
            if not(i % 100): logging.info('parsing the {}-th record'.format(i))
            # parse NaN
            record = records[i].replace('-99999', '    NA')
            # retreive header & data
            [header, data] = record.split('\n', 1)
            header = pandas.read_csv(StringIO(header), header=None, index_col=None, delim_whitespace=True)
            header.columns = self.HEADER_COLUMNS
            data = pandas.read_csv(StringIO(data), header=None, index_col=None, delim_whitespace=True)
            data.columns = self.DATA_COLUMNS
            data.index = data.PRESS
            self._header = self._header.append(header)
            self._data.append(data)

        # set header index
        #self._header.index = pandas.to_datetime(parser._header[['YEAR','MONTH','DAY','HOUR']])
        self._header.index = numpy.arange(len(self._header))
        # logging
        if len(self._header) == len(self._data):
            logging.info('all {} records parsed'.format(len(records)-1))
        else:
            logging.error('The length of headers is NOT equal to the length of data!')

        return