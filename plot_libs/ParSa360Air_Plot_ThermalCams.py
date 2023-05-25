import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy import ndimage
import os

class ThermalCameraPlotter:
    def __init__(self, thermal_cam_files, output_folder):
        self.thermal_cam_files = thermal_cam_files
        self.output_folder = output_folder

    def read_thermal_cam_scene(self, thermal_cam_cap_scene_path):
        therm_cam_scene = pd.read_csv(thermal_cam_cap_scene_path, delimiter="\t")
        return therm_cam_scene

    def plot_thermal_cam_scene(self):
        mlx_shape = (24, 32)
        mlx_interp_val = 20  # Interpolation factor on each dimension
        mlx_interp_shape = (mlx_shape[0] * mlx_interp_val, mlx_shape[1] * mlx_interp_val)  # New shape after interpolation

        therm_cam_scenes = []

        for thermal_cam_x_cap_scene in self.thermal_cam_files:
            therm_cam_x_cap = self.read_thermal_cam_scene(thermal_cam_x_cap_scene)
            therm_cam_x_scenes = []

            for i in range(len(therm_cam_x_cap)):
                therm_cam_x_scene_data = therm_cam_x_cap.values[i, 7:776]
                data_reshaped = np.reshape(therm_cam_x_scene_data, mlx_shape)  # Reshape data
                therm_cam_scene = np.flipud(np.rot90(data_reshaped, 3))  # Flip and rotate data

                # Apply interpolation
                therm_cam_scene = ndimage.zoom(therm_cam_scene, mlx_interp_val)

                therm_cam_x_scenes.append(therm_cam_scene)

            therm_cam_scenes.append(therm_cam_x_scenes)

        nrows = 2
        ncols = 6
        fig_width = 12
        fig_height = 7
        vmax = 30
        vmin = 18
        dpi = 300
        axes_list = []

        fig = plt.figure(figsize=(fig_width, fig_height))
        grid_spec = fig.add_gridspec(nrows=nrows, ncols=ncols, left=0, right=1, wspace=0.1, hspace=0.1)

        ax11 = fig.add_subplot(grid_spec[1, 0])
        ax12 = fig.add_subplot(grid_spec[1, 1])
        ax13 = fig.add_subplot(grid_spec[1, 2])
        ax14 = fig.add_subplot(grid_spec[1, 3])
        ax15 = fig.add_subplot(grid_spec[1, 4])
        ax16 = fig.add_subplot(grid_spec[1, 5])
        ax17 = fig.add_subplot(grid_spec[0, 2])
        ax18 = fig.add_subplot(grid_spec[0, 3])

        axes_list.extend([ax11, ax12, ax13, ax14, ax15, ax16, ax17, ax18])

        cmap = cm.get_cmap('jet')
        fcm_list = []
        interpolation = 'none'

        for ax, therm_cam_x_cap in zip(axes_list, therm_cam_scenes):
            scene = therm_cam_x_cap[0]  # Select the first scene for plotting
            fcm = ax.imshow(scene, interpolation=interpolation, cmap=cmap, vmin=vmin, vmax=vmax)
            fcm_list.append(fcm)

        all_axes = axes_list

        for ax in all_axes:
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            ax.set_aspect(aspect='equal')

        ax11.set_title('Thermal Cam 1')
        ax12.set_title('Thermal Cam 2')
        ax13.set_title('Thermal Cam 3')
        ax14.set_title('Thermal Cam 4')
        ax15.set_title('Thermal Cam 5')
        ax16.set_title('Thermal Cam 6')
        ax17.set_title('Thermal Cam 7')
        ax18.set_title('Thermal Cam 8')

        output_file_path = os.path.join(self.output_folder, 'ThermCamViews.jpg')
        fig.savefig(output_file_path, dpi=dpi, bbox_inches='tight', transparent=True)
        plt.close(fig)  # Close the figure to release memory

        return output_file_path
