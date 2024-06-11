import numpy as np
import pandas as pd
import os
import time
import argparse


def _read_hdf(filename):
    df = pd.read_hdf(filename, 'df')

    new_cols_order = ['datetime', 'year', 'month', 'day', 'hour', 'Kp', 'kp_bin_no', 'MLT', 'mlt_bin_no', 'MLAT', 'mlat_bin_no']
    df = df[new_cols_order]

    return df


def _create_dirs():
    if not os.path.isdir('dir'):
        os.mkdir('dir')
    os.chdir('dir')

    for i in range(27):
        new_kp = 'kp_' + str(i)
        if not os.path.isdir(new_kp):
            os.mkdir(new_kp)

    for folder in os.listdir():
        os.chdir(folder)
        for i in range(96):
            new_mlt = 'mlt_' + str(i)
            if not os.path.isdir(new_mlt):
                os.mkdir(new_mlt)
            os.chdir(new_mlt)
            for j in range(90):
                new_mlat = 'mlat_' + str(j)
                if not os.path.isdir(new_mlat):
                    os.mkdir(new_mlat)
            os.chdir('..')
        os.chdir('..')
    os.chdir('..')


def _sep2bins(filename):
    df = _read_hdf(filename)

    _create_dirs()
    os.chdir('dir')

    pd.set_option('display.max_columns', None)

    kp_bin_no = np.arange(27, dtype=np.int32)
    mlt_bin_no = np.arange(96, dtype=np.int32)
    mlat_bin_no = np.arange(90, dtype=np.int64)

    cnt = 0
    lst_x = []
    lst_y = []
    for kp in kp_bin_no:
        for mlt in mlt_bin_no:
            for mlat in mlat_bin_no:
                res = df.loc[(df['kp_bin_no'] == kp) & (df['mlt_bin_no'] == mlt) & (df['mlat_bin_no'] == mlat)]
                if not res.empty:
                    os.chdir('kp_' + str(kp))
                    os.chdir('mlt_' + str(mlt))
                    os.chdir('mlat_' + str(mlat))

                    date = ((str(res['year'].loc[res.index[0]]) + '-'
                            + str(res['month'].loc[res.index[0]]) + '-'
                            + str(res['day'].loc[res.index[0]])) + '-'
                            + str(res['hour'].loc[res.index[0]]))
                    new_filename = (date + '-kp' + str(kp) + '-mlt'
                                    + str(mlt) + '-mlat' + str(mlat) + str('.hdf'))

                    res.to_hdf(new_filename, key='df', mode='w')

                    cnt += 1
                    os.chdir('..')
                    os.chdir('..')
                    os.chdir('..')

    print('Создано ' + str(cnt) + ' hdf-файлов')
    return lst_x, lst_y


def sep2bins():
    parser = argparse.ArgumentParser(
        description='Splitting of one HDF file by bin based on kp, MLT, mlat parameter values.')
    parser.add_argument('input_filename', type=str, help='The name of the merged HDF file')
    args = parser.parse_args()
    
    filename = args.input_filename

    start = time.time()
    x, y = _sep2bins(filename)
    end = time.time()
    print((end - start)/60, 'min')
