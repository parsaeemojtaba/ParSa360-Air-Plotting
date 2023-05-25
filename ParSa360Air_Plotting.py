#%% This script enables plotting all imagery-multi-sensory data captured by ParSa 360+Air
#!/usr/local/bin/python3

import sys
# Define the path to the directory including plotting libraries
plot_LibPath=r'C:\Users\parsa\Desktop\RaspberryPi\MultiSensoryScripts\plot_libs'
sys.path.insert(1, plot_LibPath)
from ParSa360Air_Plot_ReadCapturedData import CapturedDataReader
from ParSa360Air_Plot_ThermalCams import ThermalCameraPlotter
from ParSa360Air_Plot_MultisensoryData import MultiDataPlotter
from ParSa360Air_Plot_PhotobiologicalMetrics import PhotoBiologicalPlotter

# Define the path to the ExifTool executable
exe = r'C:\Program Files\ExifTool\exiftool.exe'

# Define the main directory where the captured data is stored
data_logger_main_dir = r'C:\Users\parsa\Desktop\RaspberryPi\MultiSensoryScripts\DataLogger'

# Create an instance of CapturedDataReader
captured_data_reader = CapturedDataReader(data_logger_main_dir)

# Get the output folder path
output_folderpath = captured_data_reader.get_output_folder()

# Access the captured data
camera_capture_lists, cam_1_capture_folder_list, cam_2_capture_folder_list = captured_data_reader.get_camera_capture_lists()
therm_cam_cap_scenes_files = captured_data_reader.get_therm_cam_scenes_files()
therm_cam_cap_stats_files = captured_data_reader.get_therm_cam_stats_files()
sound_level_captures = captured_data_reader.sound_level_captures
lux_level_captures = captured_data_reader.lux_level_captures
sd_captures = captured_data_reader.sd_captures
tem_hum_captures = captured_data_reader.tem_hum_captures
co2_captures = captured_data_reader.co2_captures

# Plot multi-sensory data
PMair_Captures = co2_captures
plotter = MultiDataPlotter()
pointINtime = 240
plotter.plot_MultiData(pointINtime, lux_level_captures, sound_level_captures, sd_captures, tem_hum_captures, co2_captures, PMair_Captures, output_folderpath)

# Create an instance of ThermalCameraPlotter
plotter = ThermalCameraPlotter(therm_cam_cap_scenes_files, output_folderpath)

# Call the plot method to generate the thermal camera plot and save it
plot_file = plotter.plot_thermal_cam_scene()


# Generate photo-biological metrics plot
plotter = PhotoBiologicalPlotter()
cam_1_capture = cam_1_capture_folder_list[0]
cam_2_capture = cam_2_capture_folder_list[0]
plotter.generate_plot(cam_1_capture, cam_2_capture, output_folderpath)

# %%
