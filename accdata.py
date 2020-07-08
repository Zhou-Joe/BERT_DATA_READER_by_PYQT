import pandas as pd
import re
import math
from sci_calculation import *
import numpy as np
import os
class AccData:
    def __init__(self, rawdata, path=None, is_raw=False, *args, **kwargs):
        if is_raw:
            self.rawdata=rawdata
            self.data=rawdata
            self.filename=path
            self.filtered_data = pd.DataFrame()
            self.std_data = pd.DataFrame()

        else:
            self.rawdata = pd.read_csv(rawdata, header=None, index_col=False, sep='\t', low_memory=False)
            self.filename = os.path.basename(rawdata)
            self.filtered_data = pd.DataFrame()
            self.std_data = pd.DataFrame()
            # self.start_idx=0
            # self.col_idx=0
            self.get_core_idx()
            self.init_angle()
            self.get_angle()
            self.get_colID()
            self.parsie_cols()
            self.get_offset()
            self.filter_data(cutoff=5)
    def init_angle(self):
        self.pitch_angle = 0
        self.yaw_angle = 0
        self.roll_angle = 0
        self.seatback_angle = 0

    def get_angle(self):
        for i in range(10):
            try:
                if "Initial Pitch Angle: " in str(self.rawdata.iloc[i, 0]):
                    self.pitch_angle = int(re.sub(r"Initial Pitch Angle: ", '', self.rawdata.iloc[i, 0]))
                elif "Seatback Angle: " in str(self.rawdata.iloc[i, 0]):
                    self.seatback_angle = int(re.sub(r"Seatback Angle: ", '', self.rawdata.iloc[i, 0]))

                elif "Initial Roll Angle: " in str(self.rawdata.iloc[i, 0]):
                    self.roll_angle = int(re.sub(r"Initial Roll Angle: ", '', self.rawdata.iloc[i, 0]))
                elif "Initial Yaw Angle: " in str(self.rawdata.iloc[i, 0]):
                    self.yaw_angle = int(re.sub(r"Initial Yaw Angle: ", '', self.rawdata.iloc[i, 0]))
            except:
                pass

    def get_offset(self):
        [self.zero_x, self.zero_y, self.zero_z] = coordTransform(self.pitch_angle, self.seatback_angle, self.roll_angle, self.yaw_angle)

        # first 500 data point average:
        self.x_avg = self.data.iloc[:499, 1].mean()
        self.y_avg = self.data.iloc[:499, 2].mean()
        self.z_avg = self.data.iloc[:499, 3].mean()
        # get deviate value:
        self.offset_x = self.x_avg - self.zero_x
        self.offset_y = self.y_avg - self.zero_y
        self.offset_z = self.z_avg - self.zero_z

    def get_core_idx(self):
        for i in range(20):
            try:
                if "SARCcolumnIDs" in str(self.rawdata.iloc[i, 0]):
                    self.col_idx = i
            except:
                pass

            try:
                m1 = round(float(self.rawdata.iloc[i, 0]), 3)
                m2 = round(float(self.rawdata.iloc[i + 1, 0]), 3)
            except:
                m1 = 0
                m2 = 0
            if m1 == 0 and m2 == 0.002:
                self.start_idx = i

        try:
            re.sub(r'time', 'Time', self.rawdata.iloc[self.col_idx, 0])
        except:
            pass

    def get_colID(self, column_str=None):
        try:
            self.column_row_content = re.sub(r'SARCcolumnIDs: ', "", self.rawdata.iloc[self.col_idx, 0])
            self.columns = re.sub(r'SARCcolumnIDs: ', '', self.rawdata.iloc[self.col_idx, 0]).split(' ')
        except:
            pass

    def set_colID(self, column_str):
        self.column_row_content = column_str
        self.columns = self.column_row_content.split(' ')
        self.data.columns = self.columns

    def parsie_cols(self):
        self.data = pd.DataFrame()
        for i in range(len(self.columns)):
            self.data[self.columns[i]] = self.rawdata.iloc[self.start_idx:, i]
        self.data.reset_index(drop=True, inplace=True)
        if "Time" in self.columns:
            self.data['Time'] = pd.to_numeric(self.data['Time'], errors='ignore').round(decimals=4)
        self.data = self.data.round(decimals=4)

    def filter_data(self, cutoff=500):
        self.filtered_data['Time'] = self.data['Time']
        self.std_data['Time'] = self.data['Time']
        cutoff = cutoff
        i = 0
        zero_list = [self.x_avg, self.y_avg, self.z_avg]
        offset_list=[self.offset_x, self.offset_y, self.offset_z]
        for cols in list(self.data.columns):
            if not "Time" in cols:
                self.std_data[cols] = butter_lowpass_filter(self.data[cols], cutoff, fs=500, order=4,
                                                                 zeropoint=zero_list[i])-offset_list[i]
                self.filtered_data[cols] = butter_lowpass_filter(self.data[cols], cutoff, fs=500, order=4,
                                                                 zeropoint=zero_list[i])
                i += 1
        self.filtered_data = self.filtered_data.round(decimals=4)
        self.std_data = self.std_data.round(decimals=4)
    def set_angle(self, pitch_angle, seatback_angle, roll_angle, yaw_angle):
        self.pitch_angle = pitch_angle
        self.seatback_angle = seatback_angle
        self.roll_angle = roll_angle
        self.yaw_angle = yaw_angle
        self.get_offset()

    def reformat(self, overwrite=False, setting_angle=False, pitch_angle=0, seatback_angle=0, roll_angle=0, yaw_angle=0):
        if setting_angle:
            self.set_angle(pitch_angle, seatback_angle, roll_angle, yaw_angle)
        self.new_data = pd.DataFrame()
        for i in self.columns:
            self.new_data[i] = self.data[i]
        self.new_data.loc[-6, 'Time'] = 'Initial Pitch Angle: {}'.format(self.pitch_angle)
        self.new_data.loc[-5, 'Time'] = 'Seatback Angle: {}'.format(self.seatback_angle)
        self.new_data.loc[-4, 'Time'] = 'Initial Roll Angle: {}'.format(self.roll_angle)
        self.new_data.loc[-3, 'Time'] = 'Initial Yaw Angle: {}'.format(self.yaw_angle)
        self.new_data.loc[-2, 'Time'] = 'SARCcolumnIDs: {}'.format(self.column_row_content)
        self.new_data.loc[-1, 'Time'] = np.nan
        self.new_data.sort_index(inplace=True)
        self.new_data.reset_index(drop=True, inplace=True) #only for export if not overwrite
        if overwrite is True:
            self.rawdata = self.new_data
            self.get_core_idx()
            self.get_colID()
            self.parsie_cols()
            self.get_offset()
            self.filter_data(cutoff=5)

    def edit_data(self, method, value_array):
        self.raw_data=pd.DataFrame()
        for i in self.columns:
            self.raw_data[i] = self.data[i]
        self.raw_data.loc[-6, 'Time'] = 'Initial Pitch Angle: {}'.format(self.pitch_angle)
        self.raw_data.loc[-5, 'Time'] = 'Seatback Angle: {}'.format(self.seatback_angle)
        self.raw_data.loc[-4, 'Time'] = 'Initial Roll Angle: {}'.format(self.roll_angle)
        self.raw_data.loc[-3, 'Time'] = 'Initial Yaw Angle: {}'.format(self.yaw_angle)
        self.raw_data.loc[-2, 'Time'] = 'SARCcolumnIDs: {}'.format(self.column_row_content)
        self.raw_data.loc[-1, 'Time'] = np.nan
        self.raw_data.sort_index(inplace=True)
        self.raw_data.reset_index(drop=True, inplace=True)  # only for export if not overwrite
        self.rawdata=self.raw_data
        if method is 'add':
            for i in range(3):
                self.rawdata.iloc[:,i+1] = self.rawdata.iloc[:,i+1].values + value_array[i]
        if method is 'multiply':
            for i in range(3):
                self.rawdata.iloc[:, i + 1] = self.rawdata.iloc[:, i + 1].values * value_array[i]


        self.rawdata=self.rawdata.round(decimals=4)

        self.get_core_idx()
        self.get_colID()
        self.parsie_cols()
        self.get_offset()
        self.filter_data(cutoff=5)



    def truncate_data(self, starttime, endtime):
        start_row = int(starttime) * 500
        end_row = int(endtime) * 500
        self.new_data=pd.DataFrame()
        for i in self.columns:
            self.new_data[i] = self.data[i][start_row:end_row]
        self.new_data['Time']=self.new_data['Time'].values-starttime
        self.new_data.loc[-6, 'Time'] = 'Initial Pitch Angle: {}'.format(self.pitch_angle)
        self.new_data.loc[-5, 'Time'] = 'Seatback Angle: {}'.format(self.seatback_angle)
        self.new_data.loc[-4, 'Time'] = 'Initial Roll Angle: {}'.format(self.roll_angle)
        self.new_data.loc[-3, 'Time'] = 'Initial Yaw Angle: {}'.format(self.yaw_angle)
        self.new_data.loc[-2, 'Time'] = 'SARCcolumnIDs: {}'.format(self.column_row_content)
        self.new_data.loc[-1, 'Time'] = np.nan
        self.new_data.sort_index(inplace=True)
        self.new_data.reset_index(drop=True, inplace=True) #only for export if not overwrite
        self.rawdata = self.new_data
        self.get_core_idx()
        self.get_colID()
        self.parsie_cols()
        self.get_offset()
        self.filtered_data=pd.DataFrame()
        self.std_data=pd.DataFrame()
        self.filter_data(cutoff=5)
    def reset_data(self):
        self.parsie_cols()
    def get_data_stats(self, data):  # output dataframe value
        minmax = [[data.iloc[:, 1].idxmax() / 500, data.iloc[:, 1].max(), data.iloc[:, 1].idxmin() / 500,
                   data.iloc[:, 1].min(), self.zero_x],
                  [data.iloc[:, 2].idxmax() / 500, data.iloc[:, 2].max(), data.iloc[:, 2].idxmin() / 500,
                   data.iloc[:, 2].min(), self.zero_y],
                  [data.iloc[:, 3].idxmax() / 500, data.iloc[:, 3].max(), data.iloc[:, 3].idxmin() / 500,
                   data.iloc[:, 3].min(), self.zero_z]]
        return pd.DataFrame(minmax, index=['X', 'Y', 'Z'], columns=['t (Max)', 'Max', 't (Min)', 'Min', 'Zero Pos'])

    def get_angle_info(self):  # output string value
        str_info = ("Dataset: {}\nPitch Angle: {}°\tSeatback Angle: {}°\nRoll Angle: {}°\tYaw Angle: {}°\n".format
                    (self.filename, self.pitch_angle, self.seatback_angle, self.roll_angle,
                     self.yaw_angle))
        return str_info

    def export_to_file(self, path):
        try:
            self.reformat(overwrite=True, setting_angle=False)
            self.rawdata.to_csv(path, sep='\t', header=False, index=False)
        except:
            pass
class RawData:
    def __init__(self, path, *args, **kwargs):
        self.filename = path
        self.rawdata = pd.read_csv(path, index_col=False, sep='\t')
        self.rawdata.dropna(inplace=True, axis=1)
        self.shape = self.rawdata.shape
        self.init_data()

    def init_data(self):
        ASTM_cols_str = "Time 13inch_accek-x 13inch_accel-y 13inch_accel-z"
        GB_cols_str = "Time 60cm_accel-x 60cm_accel-y 60cm_accel-z"
        ASTM_cols = ASTM_cols_str.split(' ')
        GB_cols = GB_cols_str.split(' ')
        col_time = pd.DataFrame(np.arange(0, self.shape[0] * 0.002, 0.002), columns=['Time'])
        ASTM_data = pd.DataFrame()
        ASTM_data['Time'] = col_time['Time']
        GB_data = pd.DataFrame()
        GB_data['Time'] = col_time['Time']
        for i in range(3):
            GB_data[GB_cols[i + 1]] = self.rawdata.iloc[:, i]
            ASTM_data[ASTM_cols[i + 1]] = self.rawdata.iloc[:, i + 3]
        self.GB_data = AccData(GB_data, is_raw=True, path="(GB)"+os.path.basename(self.filename))
        self.GB_data.set_colID(GB_cols_str)

        self.ASTM_data = AccData(ASTM_data,is_raw=True, path="(ASTM)"+os.path.basename(self.filename))
        self.ASTM_data.set_colID(ASTM_cols_str)
    def export_data(self):
        return self.GB_data, self.ASTM_data

