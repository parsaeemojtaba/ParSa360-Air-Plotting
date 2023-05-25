import os
import natsort
import pandas as pd

class CapturedDataReader:
    def __init__(self, data_logger_main_dir):
        self.data_logger_main_dir = data_logger_main_dir
        self.output_folder = os.path.join(data_logger_main_dir, '__MultiSensoryRenders')

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.sound_meter_folder_name = 'SoundMeters'
        self.sound_meter_dir = os.path.abspath(os.path.join(self.data_logger_main_dir, self.sound_meter_folder_name))
        self.sound_meter_cap_files = self.get_sorted_files(self.sound_meter_dir)

        self.lux_meter_folder_name = 'LuxMeters'
        self.lux_meter_dir = os.path.abspath(os.path.join(self.data_logger_main_dir, self.lux_meter_folder_name))
        self.lux_meter_cap_files = self.get_sorted_files(self.lux_meter_dir)

        self.sp_meter_folder_name = 'AsSpectrophotometers'
        self.sp_meter_dir = os.path.abspath(os.path.join(self.data_logger_main_dir, self.sp_meter_folder_name))
        self.sp_meter_cap_files = self.get_sorted_files(self.sp_meter_dir)

        self.tem_hum_folder_name = 'TempHumidityDht'
        self.tem_hum_dir = os.path.abspath(os.path.join(self.data_logger_main_dir, self.tem_hum_folder_name))
        self.tem_hum_cap_files = self.get_sorted_files(self.tem_hum_dir)

        self.co2_folder_name = 'CO2Level'
        self.co2_dir = os.path.abspath(os.path.join(self.data_logger_main_dir, self.co2_folder_name))
        self.co2_cap_file = self.get_sorted_files(self.co2_dir)[0]

        self.sound_level_captures = self.read_captures(self.sound_meter_cap_files, self.read_sound_level_capture)
        self.lux_level_captures = self.read_captures(self.lux_meter_cap_files, self.read_lux_level_capture)
        self.sd_captures = self.read_captures(self.sp_meter_cap_files, self.read_sd_capture)
        self.tem_hum_captures = self.read_captures(self.tem_hum_cap_files, self.read_tem_hum_capture)
        self.co2_captures = self.read_co2_capture(self.co2_cap_file)

    def get_sorted_files(self, folder_path):
        files = [os.path.abspath(os.path.join(folder_path, drx)) for drx in os.listdir(folder_path)]
        return natsort.natsorted(files, reverse=False)

    def read_captures(self, capture_files, read_function):
        captures = []
        for file in capture_files:
            capture = read_function(file)
            captures.append(capture)
        return captures

    def read_sound_level_capture(self, sound_meter_sen_x_cap_file):
        sound_level_cap = pd.read_csv(sound_meter_sen_x_cap_file, delimiter="\t")
        return sound_level_cap

    def read_lux_level_capture(self, lux_meter_sen_x_cap_file):
        lux_level_cap = pd.read_csv(lux_meter_sen_x_cap_file, delimiter="\t")
        return lux_level_cap

    def read_sd_capture(self, sp_sen_x_cap_file):
        sd_cap = pd.read_csv(sp_sen_x_cap_file, delimiter="\t")
        return sd_cap

    def read_tem_hum_capture(self, tem_hum_x_cap_file):
        tem_hum_cap = pd.read_csv(tem_hum_x_cap_file, delimiter="\t")
        return tem_hum_cap

    def read_co2_capture(self, co2_x_cap_file):
        co2_cap = pd.read_csv(co2_x_cap_file, delimiter="\t")
        return co2_cap

    def get_camera_capture_lists(self):
        cam_1_folder_name = 'Captures_Camera_1'
        cam_2_folder_name = 'Captures_Camera_2'
        cam_1_dir = os.path.join(self.data_logger_main_dir, cam_1_folder_name)
        cam_2_dir = os.path.join(self.data_logger_main_dir, cam_2_folder_name)

        cam_1_capture_folder_list = self.get_sorted_files(cam_1_dir)
        cam_2_capture_folder_list = self.get_sorted_files(cam_2_dir)

        camera_capture_lists = [cam_1_capture_folder_list, cam_2_capture_folder_list]

        return camera_capture_lists, cam_1_capture_folder_list, cam_2_capture_folder_list

    def get_therm_cam_scenes_files(self):
        therm_cam_folder_name = 'ThermalCamSens'
        therm_cam_dir = os.path.join(self.data_logger_main_dir, therm_cam_folder_name)

        therm_cam_cap_scenes_files = [
            os.path.join(therm_cam_dir, 'Scene_ThermalCam_1.txt'),
            os.path.join(therm_cam_dir, 'Scene_ThermalCam_2.txt'),
            os.path.join(therm_cam_dir, 'Scene_ThermalCam_3.txt'),
            os.path.join(therm_cam_dir, 'Scene_ThermalCam_4.txt'),
            os.path.join(therm_cam_dir, 'Scene_ThermalCam_5.txt'),
            os.path.join(therm_cam_dir, 'Scene_ThermalCam_6.txt'),
            os.path.join(therm_cam_dir, 'Scene_ThermalCam_7.txt'),
            os.path.join(therm_cam_dir, 'Scene_ThermalCam_8.txt')
        ]

        return therm_cam_cap_scenes_files

    def get_therm_cam_stats_files(self):
        therm_cam_folder_name = 'ThermalCamSens'
        therm_cam_dir = os.path.join(self.data_logger_main_dir, therm_cam_folder_name)

        therm_cam_cap_stats_files = [
            os.path.join(therm_cam_dir, 'Stats_ThermalCam_1.txt'),
            os.path.join(therm_cam_dir, 'Stats_ThermalCam_2.txt'),
            os.path.join(therm_cam_dir, 'Stats_ThermalCam_3.txt'),
            os.path.join(therm_cam_dir, 'Stats_ThermalCam_4.txt'),
            os.path.join(therm_cam_dir, 'Stats_ThermalCam_5.txt'),
            os.path.join(therm_cam_dir, 'Stats_ThermalCam_6.txt'),
            os.path.join(therm_cam_dir, 'Stats_ThermalCam_7.txt'),
            os.path.join(therm_cam_dir, 'Stats_ThermalCam_8.txt')
        ]

        return therm_cam_cap_stats_files

    def get_output_folder(self):
        return self.output_folder
