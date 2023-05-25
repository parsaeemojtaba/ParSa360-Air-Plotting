
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from matplotlib import pyplot as plt

class MultiDataPlotter:
    def __init__(self):
        self.nrows = 4
        self.ncols = 1
        self.ww = 14
        self.hh = 14
        self.linewidth = 1

        self.dpi_plt = 150
        self.fontdict_axislable = {'family':'Calibri','size':10, 'weight': 'normal', 'horizontalalignment':'center'}
        self.fontdict_title = {'family': 'Calibri', 'size': 12, 'weight': 'bold', 'horizontalalignment': 'center'}
        self.fontdict_gen = {'family': 'Calibri', 'size': 10}

        self.color = 'steelblue'
        self.color_2 = 'orange'
        self.color_3 = 'red'
        self.color_4 = 'green'
        self.color_5 = 'brown'
        self.color_6 = 'cyan'
        self.color_7 = 'darkcyan'
        self.fig = plt.figure(figsize=(self.ww, self.hh))
        self.wspace_3plt = 0.25
        self.wspace_4plt = 0.25
        self.wspace_6plt = 0.3
        self.gs00 = self.fig.add_gridspec(nrows=self.nrows, ncols=self.ncols, left=0, right=1, hspace=0.5)
        self.plts_lx = 6
        self.gs_lx = self.gs00[1].subgridspec(1, self.plts_lx, wspace=self.wspace_6plt)
        self.plts_sd = 4
        self.gs_sd = self.gs00[0].subgridspec(1, self.plts_sd, wspace=self.wspace_4plt)
        self.plts_sl = 4
        self.gs_sl = self.gs00[2].subgridspec(1, self.plts_sl, wspace=self.wspace_4plt)
        self.plts_air = 3
        self.gs_air = self.gs00[3].subgridspec(1, self.plts_air, wspace=self.wspace_3plt)

    def timeframe (self, dataframe, pointINtime):
        df = dataframe
        p = pointINtime
        delimiter_1 = '-'
        delimiter_2 = ':'
        delimiter_3 = '\n'

        timeframe_ymd = df['year'].astype(str) + delimiter_1 \
                        + df['month'].astype(str) + delimiter_1 \
                        + df['day'].astype(str)

        timeframe_hm = df['hour'].astype(str) + delimiter_2 + df['minute'].astype(str)
        timeframe_full = timeframe_ymd + delimiter_3 + timeframe_hm
        print(timeframe_full[0::10])
        timeframeP_ymd = timeframe_ymd[p]
        timeframeP_hm = timeframe_hm[p]
        timeframeP_full = timeframe_full[p]
        print(timeframeP_full)

        return timeframe_full, timeframe_ymd, timeframe_hm, timeframeP_full, timeframeP_ymd, timeframeP_hm

    def plot_MultiData(self, pointINtime, LuxLevel_Captures, SoundLevel_Captures, Sd_Captures, TemHum_Captures, CO2_Captures, PMair_Captures, Outputfolder):
        
        dataframe=SoundLevel_Captures[0]
        timeframe_full, timeframe_ymd, timeframe_hm, timeframeP_full, timeframeP_ymd, timeframeP_hm = self.timeframe(dataframe, pointINtime)
        ## Lux Meter
        lx_axs=[]
        for i in range (self.plts_lx):
            axlx_x=self.fig.add_subplot(self.gs_lx[i])
            lx_axs.append(axlx_x)

        ## spectrometer
        sd_axs=[]
        for i in range (self.plts_sd):
            sdax_x=self.fig.add_subplot(self.gs_sd[i])
            sd_axs.append(sdax_x)


        ## Sound level meter
        sl_axs=[]
        for i in range (self.plts_sl):
            slax_x=self.fig.add_subplot(self.gs_sl[i])
            sl_axs.append(slax_x)

        ## air condition
        air_axs=[]
        for i in range (self.plts_air):
            airax_x=self.fig.add_subplot(self.gs_air[i])
            air_axs.append(airax_x)

        ### X axis full time frame
        xloc = timeframe_full
        xlocLen=len(xloc)
        xtixk_st=0
        axtixk_it=120
        xticklabels = timeframe_full[xtixk_st::axtixk_it]
        xticksloc = timeframe_full[xtixk_st::axtixk_it]

        ### sound level meter plots
        ymin=20
        ymax=60
        ylim=(ymin, ymax)

        yminticklable=30
        ymaxticklabel=50
        ytick_it=10
        ytickloc=np.arange(yminticklable, ymaxticklabel+ytick_it, ytick_it)
        yticklabels=ytickloc

        sl_axisLabel = {'x':'Time (five-minute interval)', 'y':'dB'}
        sl_plottitles = [ 'Sound Level view 0-90', 'Sound Level view 90-180',
                        'Sound Level view 180-270', 'Sound Level view 270-360']

        ### lux meter plots
        lx_ymin=0
        lx_ymax=500
        lx_ylim=(lx_ymin, lx_ymax)

        lx_yminticklable = 0
        lx_ymaxticklabel = 500
        lx_ytick_it = 100
        lx_ytickloc = np.arange( lx_yminticklable, lx_ymaxticklabel+lx_ytick_it, lx_ytick_it)
        lx_yticklabels = lx_ytickloc

        lx_axisLabel = {'x':'Time (five-minute interval)', 'y':'lx'}
        lx_plottitles= [ 'Lux Level view 0-60', 'Lux Level view 60-120', 'Lux Level view 120-180',
                        'Lux Level view 180-240', 'Lux Level view 240-300', 'Lux Level view 300-360' ]

        ### Temperature and humidity plots
        tmp_ymin=20
        tmp_ymax=25
        tmp_ylim=(tmp_ymin, tmp_ymax)

        tmp_yminticklable =20
        tmp_ymaxticklabel = 25
        # tmp_ytick_it = 5
        # tmp_ytickloc = np.linspace(tmp_yminticklable, tmp_ymaxticklabel, tmp_ytick_it, endpoint=True)
        tmp_ytick_it = 1
        tmp_ytickloc = np.arange( tmp_yminticklable, tmp_ymaxticklabel + tmp_ytick_it, tmp_ytick_it)
        tmp_yticklabels = tmp_ytickloc

        tmp_axisLabel = {'x':'Time (five-minute interval)', 'y':'C'}

        hum_ymin=0
        hum_ymax=20
        hum_ylim=(hum_ymin, hum_ymax)

        hum_yminticklable = 0
        hum_ymaxticklabel = 20
        # hum_ytick_it = 4
        # hum_ytickloc = np.linspace(hum_yminticklable, hum_ymaxticklabel, hum_ytick_it, endpoint=True)
        hum_ytick_it = 4
        hum_ytickloc = np.arange( hum_yminticklable, hum_ymaxticklabel + hum_ytick_it, hum_ytick_it)

        hum_yticklabels = hum_ytickloc

        hum_axisLabel = {'x':'Time (five-minute interval)', 'y':'RH (%)'}

        tmpHum_plottitle= 'Temperature and Relative Humidity'

        ### CO2 plots
        co2_ymin=400
        co2_ymax=800
        co2_ylim=(co2_ymin, co2_ymax)

        co2_yminticklable = 400
        co2_ymaxticklabel = 800
        # tmp_ytick_it = 5
        # tmp_ytickloc = np.linspace(tmp_yminticklable, tmp_ymaxticklabel, tmp_ytick_it, endpoint=True)
        co2_ytick_it = 200
        co2_ytickloc = np.arange( co2_yminticklable, co2_ymaxticklabel + co2_ytick_it, co2_ytick_it )
        co2_yticklabels = co2_ytickloc

        co2_axisLabel = {'x':'Time (five-minute interval)', 'y':'ppm'}
        co2_plottitle= 'CO2 level'

        ### PM2.5 air quality plots
        pm25_ymin = 400
        pm25_ymax = 800
        pm25_ylim=(pm25_ymin, pm25_ymax)

        pm25_yminticklable = 400
        pm25_ymaxticklabel = 800
        # tmp_ytick_it = 5
        # tmp_ytickloc = np.linspace(tmp_yminticklable, tmp_ymaxticklabel, tmp_ytick_it, endpoint=True)
        pm25_ytick_it = 100
        pm25_ytickloc = np.arange( pm25_yminticklable, pm25_ymaxticklabel + pm25_ytick_it, pm25_ytick_it )
        pm25_yticklabels = pm25_ytickloc

        pm25_axisLabel = {'x':'Time (five-minute interval)', 'y':'PM 2.5'}
        pm25_plottitle= 'Air Quality Level (PM 2.5 particles)'


        ### spectral distribution plots
        sd_channels = [410, 435, 460, 485, 510, 535, 560, 585, 610, 645, 680, 705, 730, 760, 810, 860, 900, 940]

        sd_xmin=400
        sd_xmax=950
        sd_xlim=(sd_xmin, sd_xmax)

        sd_xminticklable = 400
        sd_xmaxticklabel = 950
        sd_xtick_it = 50
        sd_xticksloc = np.arange(sd_xminticklable, sd_xmaxticklabel + sd_xtick_it, sd_xtick_it)
        sd_xticklabels = sd_xticksloc

        sd_ymin=0
        sd_ymax=2.5
        sd_ylim=(sd_ymin, sd_ymax)

        sd_yminticklable = 0
        sd_ymaxticklabel = 2.5
        sd_ytick_it = .5
        sd_ytickloc = np.arange( sd_yminticklable, sd_ymaxticklabel + sd_ytick_it, sd_ytick_it)
        sd_yticklabels = sd_ytickloc

        sd_axisLabel = {'x':'wavelength', 'y':'count'}
        sd_plottitles= [ 'Spectral distribution view 0-90', 'Spectral distribution view 90-180',
                        'Spectral distribution view 180-270', 'Spectral distribution view 270-360']
        
        ###
        for sl_ax , SoundLevelCap , sl_plottitle in zip (sl_axs, SoundLevel_Captures, sl_plottitles):
            sl_ax.plot(xloc, SoundLevelCap['Sound level'], '-', linewidth=self.linewidth, color=self.color, alpha=1)
            sl_ax.fill_between(xloc, SoundLevelCap['Sound level'], alpha=0.2, color=self.color)
            sl_ax.set_xticks(xticksloc, xticklabels, **self.fontdict_axislable)
            sl_ax.set_ylim(ylim)
            sl_ax.set_yticks(ytickloc, yticklabels, **self.fontdict_axislable)
            
            sl_ax.set_xlabel(sl_axisLabel['x'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')
            sl_ax.set_ylabel(sl_axisLabel['y'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')
            sl_ax.set_title(sl_plottitle, loc='center', pad=5, fontdict=self.fontdict_title, color='black')

            sl_ax.xaxis.set_tick_params(which='major', direction='out', bottom=True, pad=5)
            sl_ax.yaxis.set_tick_params(which='major', direction='out', left=True, pad=10)

        for lx_ax , LuxLevelCap , lx_plottitle in zip (lx_axs, LuxLevel_Captures, lx_plottitles):
            lx_ax.plot(xloc, LuxLevelCap['lux level'], '-', linewidth=self.linewidth, color=self.color_2, alpha=1)
            lx_ax.fill_between(xloc, LuxLevelCap['lux level'], alpha=0.2, color=self.color_2)
            lx_ax.set_xticks(xticksloc, xticklabels, **self.fontdict_axislable)
            lx_ax.set_ylim(lx_ylim)
            lx_ax.set_yticks(lx_ytickloc, lx_yticklabels, **self.fontdict_axislable)
            
            lx_ax.set_xlabel(lx_axisLabel['x'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')
            lx_ax.set_ylabel(lx_axisLabel['y'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')
            lx_ax.set_title(lx_plottitle, loc='center', pad=5, fontdict=self.fontdict_title, color='black')

            lx_ax.xaxis.set_tick_params(which='major', direction='out', bottom=True, pad=5)
            lx_ax.yaxis.set_tick_params(which='major', direction='out', left=True, pad=10)
            
        for sd_ax , sdCap , sd_plottitle in zip (sd_axs, Sd_Captures, sd_plottitles):
            sd_ax.plot(sd_channels, sdCap.values[pointINtime][7:], '-', linewidth=self.linewidth, color=self.color_3, alpha=1)
            sd_ax.fill_between(sd_channels, sdCap.values[pointINtime][7:], alpha=0.2, color=self.color_3)
            sd_ax.set_xlim(sd_xlim)
            sd_ax.set_xticks(sd_xticksloc, sd_xticklabels, **self.fontdict_axislable)

            sd_ax.set_ylim(sd_ylim)
            sd_ax.set_yticks(sd_ytickloc, sd_yticklabels, **self.fontdict_axislable)
            
            sd_ax.set_xlabel(sd_axisLabel['x'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')
            sd_ax.set_ylabel(sd_axisLabel['y'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')

            sd_plottitle = sd_plottitle + '\n' +timeframeP_full
            sd_ax.set_title(sd_plottitle, loc='center', pad=5, fontdict=self.fontdict_title, color='black')

            sd_ax.xaxis.set_tick_params(which='major', direction='out', bottom=True, pad=5)
            sd_ax.yaxis.set_tick_params(which='major', direction='out', left=True, pad=10)


        ### plot air temperature and humidity
        TempHumCap = TemHum_Captures [0]
        tmp_ax = air_axs [0]

        tmp_ax.plot(xloc, TempHumCap['Temp'], '-', label='Temperature', linewidth=self.linewidth, color=self.color_4, alpha=1)

        tmp_ax.set_xticks(xticksloc, xticklabels, **self.fontdict_axislable)
        tmp_ax.set_xlabel(tmp_axisLabel['x'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')

        tmp_ax.set_ylim(tmp_ylim)
        tmp_ax.set_yticks(tmp_ytickloc, tmp_yticklabels, **self.fontdict_axislable)
        tmp_ax.set_ylabel(tmp_axisLabel['y'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')
        tmp_ax.yaxis.set_tick_params(which='major', direction='out', left=True, pad=10)
        ymajorformatter = ticker.FormatStrFormatter("%.1f")
        tmp_ax.yaxis.set_major_formatter(ymajorformatter)

        hum_ax = tmp_ax.twinx()
        hum_ax.plot(xloc, TempHumCap['Humidity'], '-', label='Humidity',
                            linewidth=self.linewidth, color=self.color_5, alpha=1)

        hum_ax.set_ylim(hum_ylim)
        hum_ax.set_yticks(hum_ytickloc, hum_yticklabels, **self.fontdict_axislable)
        hum_ax.set_ylabel(hum_axisLabel['y'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')
        hum_ax.yaxis.set_tick_params(which='major', direction='out', left=True, pad=10)
        ymajorformatter = ticker.FormatStrFormatter("%.0f")
        hum_ax.yaxis.set_major_formatter(ymajorformatter)

        tmp_ax.set_title(tmpHum_plottitle, loc='center', pad=5, fontdict=self.fontdict_title, color='black')

        tmp_ax.xaxis.set_tick_params(which='major', direction='out', bottom=True, pad=5)

        lines, labels = tmp_ax.get_legend_handles_labels()
        lines2, labels2 = hum_ax.get_legend_handles_labels()
        lns=lines+lines2
        legend_labs=labels+labels2
        legend = tmp_ax.legend(lns, legend_labs, prop=self.fontdict_gen,  loc="lower right")

        ### plot co2
        co2_ax = air_axs [1]
        co2_ax.plot(xloc, CO2_Captures['CO2'], '-', linewidth=self.linewidth, color=self.color_6, alpha=1)

        co2_ax.set_xticks(xticksloc, xticklabels, **self.fontdict_axislable)
        co2_ax.set_xlabel(co2_axisLabel['x'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')
        co2_ax.xaxis.set_tick_params(which='major', direction='out', bottom=True, pad=5)

        co2_ax.set_ylim(co2_ylim)
        co2_ax.set_yticks(co2_ytickloc, co2_yticklabels, **self.fontdict_axislable)
        co2_ax.set_ylabel(co2_axisLabel['y'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')
        co2_ax.yaxis.set_tick_params(which='major', direction='out', left=True, pad=10)
        ymajorformatter = ticker.FormatStrFormatter("%.0f")
        co2_ax.yaxis.set_major_formatter(ymajorformatter)

        co2_ax.set_title(co2_plottitle, loc='center', pad=5, fontdict=self.fontdict_title, color='black')

        ### plot air quality PM 2.5
        pm25_ax = air_axs [2]
        pm25_ax.plot(xloc, CO2_Captures['CO2'], '-', linewidth=self.linewidth, color=self.color_7, alpha=1)

        pm25_ax.set_xticks(xticksloc, xticklabels, **self.fontdict_axislable)
        pm25_ax.set_xlabel(co2_axisLabel['x'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')
        pm25_ax.xaxis.set_tick_params(which='major', direction='out', bottom=True, pad=5)

        pm25_ax.set_ylim(pm25_ylim)
        pm25_ax.set_yticks(pm25_ytickloc, pm25_yticklabels, **self.fontdict_axislable)
        pm25_ax.set_ylabel(pm25_axisLabel['y'], labelpad=5, fontdict=self.fontdict_axislable, loc='center')
        pm25_ax.yaxis.set_tick_params(which='major', direction='out', left=True, pad=10)
        ymajorformatter = ticker.FormatStrFormatter("%.0f")
        pm25_ax.yaxis.set_major_formatter(ymajorformatter)

        pm25_ax.set_title(pm25_plottitle, loc='center', pad=5, fontdict=self.fontdict_title, color='black')


        OutputFileName = 'MutliSens'
        OutputFileLDR = os.path.join(Outputfolder, OutputFileName+'.jpg')
        self.fig.savefig(OutputFileLDR, dpi=self.dpi_plt, bbox_inches = 'tight', transparent=True)