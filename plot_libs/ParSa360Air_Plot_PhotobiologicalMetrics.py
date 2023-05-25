import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors, cm
from matplotlib.ticker import LogFormatter, ScalarFormatter
import matplotlib.image as mpimg

class PhotoBiologicalPlotter:
    def callanHDRI(self, CaptureFolderPath):
        HDRImagePath = os.path.join(CaptureFolderPath, 'hdrDebevec.hdr')
        TonemapImagePath = os.path.join(CaptureFolderPath, 'hdrDebevec_Reinhard.png')
        imageDataHDR = cv2.imread(HDRImagePath, cv2.IMREAD_ANYDEPTH)
        imageDataLDR = mpimg.imread(TonemapImagePath)
        return imageDataHDR, imageDataLDR

    def PhotoBio_params(self, image, coeff=None):
        if coeff is not None:
            b_coef, g_coef, r_coef, x_coef, y_coef, z_coef = coeff
        else:
            NoCoeff = 1
            b_coef = NoCoeff
            g_coef = NoCoeff
            r_coef = NoCoeff
            x_coef = NoCoeff
            y_coef = NoCoeff
            z_coef = NoCoeff

        b = image[:, :, 0] * b_coef
        g = image[:, :, 1] * g_coef
        r = image[:, :, 2] * r_coef

        x = (0.412453 * r + 0.357580 * g + 0.180423 * b) * x_coef
        y = (0.212671 * r + 0.715160 * g + 0.072169 * b) * y_coef
        z = (0.019334 * r + 0.119193 * g + 0.950227 * b) * z_coef

        sum_xyz = x + y + z
        cord_x = np.divide(x, sum_xyz)
        cord_y = np.divide(y, sum_xyz)
        n = np.divide((cord_x - 0.3320), (0.1858 - cord_y))
        CCT = (437 * n ** 3) + (3601 * n ** 2) + (6861 * n) + 5514.31

        r_new = (3.240479 * x) + (-1.53715 * y) + (-0.498535 * z)
        g_new = (-0.969256 * x) + (1.875991 * y) + (0.041556 * z)
        b_new = (0.055648 * x) + (-0.204043 * y) + (1.057311 * z)

        photopic = (0.212671 * r_new + 0.715160 * g_new + 0.072169 * b_new)
        melanopic = 0.0013 * r_new + 0.3812 * g_new + 0.6175 * b_new
        ratio = np.divide(melanopic, photopic)

        photopic_inv = photopic[::-1]
        melanopic_inv = melanopic[::-1]
        ratio_inv = ratio[::-1]
        CCT_inv = CCT[::-1]

        return photopic_inv, melanopic_inv, ratio_inv, CCT_inv

    def PhotoBio_falsecolor(self, PhotoBio_params, axes, cmaps):
        fcm1 = axes[1].pcolormesh(PhotoBio_params[0], norm=colors.LogNorm(vmin=10, vmax=3000, clip=True),
                                  cmap=cmaps[0], alpha=1)
        fcm2 = axes[2].pcolormesh(PhotoBio_params[1], norm=colors.LogNorm(vmin=10, vmax=3000, clip=True),
                                  cmap=cmaps[1], alpha=1)
        fcm3 = axes[3].pcolormesh(PhotoBio_params[2], norm=colors.Normalize(vmin=0.35, vmax=1.65, clip=True),
                                  cmap=cmaps[2], alpha=1)
        fcm4 = axes[4].pcolormesh(PhotoBio_params[3], norm=colors.Normalize(vmin=2000, vmax=10000, clip=True),
                                  cmap=cmaps[3], alpha=1)
        return fcm1, fcm2, fcm3, fcm4

    def generate_plot(self, cam_1_capture, cam_2_capture, output_folderpath):
        Cam_1_imageDataHDR, Cam_1_imageDataLDR = self.callanHDRI(cam_1_capture)
        Cam_2_imageDataHDR, Cam_2_imageDataLDR = self.callanHDRI(cam_2_capture)

        Cam_1_PhotoBio_params = self.PhotoBio_params(Cam_1_imageDataHDR)
        Cam_2_PhotoBio_params = self.PhotoBio_params(Cam_2_imageDataHDR)

        # set the dpi of the input images
        dpi_img = 72
        # set the output image dpi
        dpi_plt = 72

        nrows = 1
        ncols = 3
        ww = 5
        hh = 10
        w1 = (Cam_1_imageDataHDR.shape[1])
        h1 = (Cam_1_imageDataHDR.shape[0])
        print(w1, h1)

        fig, axs = plt.subplots(figsize=(ww, hh), nrows=5, ncols=2, constrained_layout=True)
        axes_list_1 = []
        ax11 = axs[0, 0]
        ax12 = axs[1, 0]
        ax13 = axs[2, 0]
        ax14 = axs[3, 0]
        ax15 = axs[4, 0]
        axes_list_1.append(ax11)
        axes_list_1.append(ax12)
        axes_list_1.append(ax13)
        axes_list_1.append(ax14)
        axes_list_1.append(ax15)

        axes_list_2 = []
        ax21 = axs[0, 1]
        ax22 = axs[1, 1]
        ax23 = axs[2, 1]
        ax24 = axs[3, 1]
        ax25 = axs[4, 1]
        axes_list_2.append(ax21)
        axes_list_2.append(ax22)
        axes_list_2.append(ax23)
        axes_list_2.append(ax24)
        axes_list_2.append(ax25)

        axes_list_1[0].imshow(Cam_1_imageDataLDR)
        axes_list_2[0].imshow(Cam_2_imageDataLDR)

        cmaps = []
        cmap1 = cm.get_cmap('nipy_spectral')
        cmaps.append(cmap1)
        cmap2 = cm.get_cmap('nipy_spectral')
        cmaps.append(cmap2)
        cmap3 = cm.get_cmap('RdBu')
        cmaps.append(cmap3)
        cmapx = cm.get_cmap('jet')
        cmap4 = cmapx.reversed()
        cmaps.append(cmap4)

        Cam_1_fcm1, Cam_1_fcm2, Cam_1_fcm3, Cam_1_fcm4 = self.PhotoBio_falsecolor(Cam_1_PhotoBio_params, axes_list_1, cmaps)
        Cam_2_fcm1, Cam_2_fcm2, Cam_2_fcm3, Cam_2_fcm4 = self.PhotoBio_falsecolor(Cam_2_PhotoBio_params, axes_list_2, cmaps)

        formatter = LogFormatter(10, labelOnlyBase=False)

        cb_aspect = 10
        cb_pad = 0.1
        cb_shrink = .9

        bounds = [1.04, 0.0, 0.07, 1]
        cax1 = ax22.inset_axes(bounds, transform=ax22.transAxes)
        cax2 = ax23.inset_axes(bounds, transform=ax23.transAxes)
        cax3 = ax24.inset_axes(bounds, transform=ax24.transAxes)
        cax4 = ax25.inset_axes(bounds, transform=ax25.transAxes)

        formatter = ScalarFormatter()
        cb1 = plt.colorbar(Cam_2_fcm1, ax=ax22, cax=cax1, format=formatter, drawedges=False, extend='both')
        cb2 = plt.colorbar(Cam_2_fcm2, ax=ax23, cax=cax2, format=formatter, drawedges=False, extend='both')
        cb3 = plt.colorbar(Cam_2_fcm3, ax=ax24, cax=cax3, format=formatter, drawedges=False, extend='both')
        cb4 = plt.colorbar(Cam_2_fcm4, ax=ax25, cax=cax4, format=formatter, drawedges=False, extend='both')

        rotation = 270
        labelpad = 10
        cb1.ax.set_ylabel('cd/m2', labelpad=labelpad, rotation=rotation)
        cb2.ax.set_ylabel('EMcd/m2', labelpad=labelpad, rotation=rotation)
        cb3.ax.set_ylabel('M/P ratio', labelpad=labelpad, rotation=rotation)
        cb4.ax.set_ylabel('K', labelpad=labelpad, rotation=rotation)

        ax11.set_title('View 1')
        ax21.set_title('View 2')

        ax12.set_title('Photopic')
        ax22.set_title('Photopic')

        ax13.set_title('Melanopic')
        ax23.set_title('Melanopic')

        ax14.set_title('M/P Ratio')
        ax24.set_title('M/P Ratio')

        ax15.set_title('CCT')
        ax25.set_title('CCT')

        allaxes = axes_list_1 + axes_list_2

        for ax in allaxes:
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            ax.set_aspect(aspect='equal')

        fig.set_constrained_layout_pads(w_pad=4 / 72, h_pad=4 / 72, hspace=0.05, wspace=0.05)

        OutputFileLDR = os.path.join(output_folderpath, 'CamViews.jpg')
        fig.savefig(OutputFileLDR, dpi=dpi_plt, bbox_inches='tight', transparent=True)



