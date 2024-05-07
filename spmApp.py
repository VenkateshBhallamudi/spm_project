import tkinter as tk
import os
import datetime
from spmDataClasses import SpmInputData
from spmInputFrame import SpmInputFrame
from spmDataClasses import ItemRecord
from spmInfoFrame import SpmInfoFrame
import selectionFrame as sf
import matplotlib.pyplot as plt
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import mapFileParsers as mp
import gradParsers as gp
import numpy as np
from matplotlib.widgets import RectangleSelector
from matplotlib.widgets import TextBox
import matplotlib
matplotlib.use('TkAgg')
from spmParsers import outputCsv
import pdfDataClasses as pd
import pdfGenerator as pg
from spmEntry import SpmEntryRecord
from bftBpt import find_bft_bpt_tuples
from tkinter import ttk

class App(tk.Tk):
    def _on_mouse_wheel(self, event):
        self.my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
                           
    def __init__(self):
        super().__init__()
        cwd = os.getcwd()
        self.title('SC Universal SPM App')
        self.iconbitmap((str(os.getcwd()) + '\\railwaylogo.ico').replace('\\', '/'))
        
        self.spmEntryRecords = []
        self.chainRecords = []
        self.itemRecords = []
        self.gradientRecords = []
        self.date_time_vals = []
        self.speed_vals = []
        self.inst_dist_vals = []
        self.cum_dist_vals = []
        self.bft_start_index = -1
        self.bft_end_index = -1
        self.bpt_start_index = -1
        self.bpt_end_index = -1

        opts = {'padx':7, 'pady':7}
        
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=1)

        self.my_canvas = tk.Canvas(main_frame)
        self.my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        my_scrollbar_x = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.my_canvas.xview)
        my_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.my_canvas.yview)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.my_canvas.configure(yscrollcommand=my_scrollbar.set, xscrollcommand=my_scrollbar_x.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox('all')))
        self.my_canvas.bind_all('<MouseWheel>', self._on_mouse_wheel)
        second_frame = tk.Frame(self.my_canvas)
        self.my_canvas.create_window((0,0), window=second_frame, anchor='nw')

        self.stoppageList = tk.Listbox(second_frame)
        self.processFrame = tk.LabelFrame(second_frame, text='Process')

        self.process_btn = tk.Button(self.processFrame, text='Process SPM', command=self.spm_process)
        self.process_btn.grid(row=0, column=0, sticky='nwe', **opts)
        self.process_map_file = tk.Button(self.processFrame, text='Process Mapping', command=self.map_file_process)
        self.process_map_file.grid(row=0, column=1, sticky='nwe', **opts)
        self.process_item = tk.Button(self.processFrame, text='Process Items', command=self.item_process)
        self.process_item.grid(row=0, column=2, sticky='nwe', **opts)
        self.process_sr_file = tk.Button(self.processFrame, text='Process SR File', command=self.sr_file_process)
        self.process_sr_file.grid(row=1, column=0, sticky='nwe', **opts)
        self.process_grad_file = tk.Button(self.processFrame, text='Process Gradient File', command=self.grad_file_process)
        self.process_grad_file.grid(row=1, column=1, sticky='nwe', **opts)
        
        #Output Label Frame
        self.outputFrame = tk.LabelFrame(second_frame, text="Output")
        tk.Button(self.outputFrame, text='Plot Speed vs Distance', command=self.plot_dist_speed).grid(row=0, column=0, sticky='nwe', **opts)
        tk.Button(self.outputFrame, text='Plot Speed vs Time', command=self.plot_speed_time).grid(row=0, column=1, sticky='nwe', **opts)
        tk.Button(self.outputFrame, text='Plot Stoppage', command=self.plot_current_stoppage).grid(row=0, column=2, sticky='nwe', **opts)
        tk.Button(self.outputFrame, text='Plot Current & Voltage', command=self.plot_current_voltage).grid(row=1, column=0, sticky='nwe', **opts)
        tk.Button(self.outputFrame, text='Plot Energy', command=self.plot_energy).grid(row=1, column=1, sticky='nwe', **opts)
        tk.Button(self.outputFrame, text='Generate Report', command=self.generate_report).grid(row=1, column=2, sticky='nwe', **opts)
        tk.Button(self.outputFrame, text='Output CSV', command=self.write_csv).grid(row=2, column=0, sticky='nwe', **opts)
        tk.Button(self.outputFrame, text='Save Plots', command=self.save_plots).grid(row=2, column=1, sticky='nwe', **opts)
        
        #tk.Button(self.outputFrame, text='Plot Energy', command=self.plot_energy).grid(row=1, column=2, sticky='nwe', **opts)

        #Plot Config Frame
        self.plotConfigFrame = tk.LabelFrame(second_frame, text="Plot Config")
        
        self.showGrid = tk.IntVar()
        self.showGrid_btn = tk.Checkbutton(self.plotConfigFrame, text="Show Grid", variable=self.showGrid)
        self.showGrid_btn.grid(row=0, column=0, sticky='nw', **opts)
        
        self.showTicks = tk.IntVar()
        self.showTicks_btn = tk.Checkbutton(self.plotConfigFrame, text="Show Station Sections", variable=self.showTicks)
        self.showTicks_btn.grid(row=0, column=1, sticky='nw', **opts)

        self.showMps = tk.IntVar()
        self.showMps_btn = tk.Checkbutton(self.plotConfigFrame, text="Show MPS/From/To", variable=self.showMps)
        self.showMps_btn.grid(row=1, column=0, sticky='nw', **opts)

        self.showIntersect = tk.IntVar()
        self.showIntersect_btn = tk.Checkbutton(self.plotConfigFrame, text="Show Intersections/Zeroes", variable=self.showIntersect)
        self.showIntersect_btn.grid(row=1, column=1, sticky='nw', **opts)

        self.showSpmAnnot = tk.IntVar()
        self.showSpmAnnot_btn = tk.Checkbutton(self.plotConfigFrame, text="Show SPM Annotations", variable=self.showSpmAnnot)
        self.showSpmAnnot_btn.grid(row=2, column=0, sticky='nw', **opts)

        self.showItem = tk.IntVar()
        self.showItem_btn = tk.Checkbutton(self.plotConfigFrame, text="Show Signals/NS", variable=self.showItem)
        self.showItem_btn.grid(row=2, column=1, sticky='nw', **opts)

        self.showSr = tk.IntVar()
        self.showSr_btn = tk.Checkbutton(self.plotConfigFrame, text="Show SRs", variable=self.showSr)
        self.showSr_btn.grid(row=3, column=0, sticky='nw', **opts)
        
        self.showGrad = tk.IntVar()
        self.showGrad_btn = tk.Checkbutton(self.plotConfigFrame, text="Show Gradient", variable=self.showGrad)
        self.showGrad_btn.grid(row=3, column=1, sticky='nw', **opts)

        self.showGradAnnot = tk.IntVar()
        self.showGradAnnot_btn = tk.Checkbutton(self.plotConfigFrame, text="Show Grad Annotations", variable=self.showGradAnnot)
        self.showGradAnnot_btn.grid(row=4, column=0, sticky='nw', **opts)

        self.showBft = tk.IntVar()
        self.showBft_btn = tk.Checkbutton(self.plotConfigFrame, text="Show BFT", variable=self.showBft)
        self.showBft_btn.grid(row=4, column=1, sticky='nw', **opts)

        self.showBpt = tk.IntVar()
        self.showBpt_btn = tk.Checkbutton(self.plotConfigFrame, text="Show BPT", variable=self.showBpt)
        self.showBpt_btn.grid(row=5, column=0, sticky='nw', **opts)

        #Initialize SPM Info and Input Frames
        self.itemFrame = sf.SelectionFrame(master=second_frame, padx=15, pady=10, text='Items')
        self.srFrame = sf.SelectionFrame(master=second_frame, padx=15, pady=10, text='Speed Restrictions')
        self.spmInfoFrame = SpmInfoFrame(second_frame, padx=15, pady=10, text='SPM Info Data')
        self.spmInputFrame = SpmInputFrame(master=second_frame, change_callback=self.input_frame_change_callback, padx=15, pady=10, text='SPM Input')

        #Place all on the App
        self.spmInfoFrame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nwe', **opts)
        self.spmInputFrame.grid(row=0, column=2, rowspan=1, sticky='nwe', **opts)
        self.stoppageList.grid(row=2, column=2, sticky='nwe', **opts)
        self.processFrame.grid(row=2, column=0, sticky='nwe', **opts)
        self.outputFrame.grid(row=2, column=1, sticky='nwe', **opts)
        self.itemFrame.grid(row=3, column=0, rowspan=3, sticky='nwe', **opts)
        self.srFrame.grid(row=3, column=1,rowspan=3, sticky='nwe', **opts)
        self.plotConfigFrame.grid(row=3, column=2, sticky='nwe', **opts)

        spmMenu = tk.Menu(self)
        reportMenu = tk.Menu(spmMenu, tearoff=0)
        self.archive_var = tk.BooleanVar()
        self.overControl_var = tk.BooleanVar()
        self.speedCompile_var = tk.BooleanVar()

        reportMenu.add_checkbutton(label="Archive Report", onvalue=True, offvalue=False, variable=self.archive_var)
        reportMenu.add_checkbutton(label="Over Controlling", onvalue=True, offvalue=False, variable=self.overControl_var)
        reportMenu.add_checkbutton(label="Speed Compilation Before Stop", onvalue=True, offvalue=False, variable=self.speedCompile_var)

        spmMenu.add_cascade(label='Reports', menu=reportMenu)
        spmMenu.add_command(label='About', command=self.show_about)
        spmMenu.add_command(label='Quit', command=self.destroy)
        self.archive_var.set(True)
        self.config(menu=spmMenu)

        self.process_btn.config(state=tk.DISABLED)
        self.process_item.config(state=tk.DISABLED)
        self.process_map_file.config(state=tk.DISABLED)
        self.process_sr_file.config(state=tk.DISABLED)
        self.process_grad_file.config(state=tk.DISABLED)
        self.disable_frames([self.plotConfigFrame,self.outputFrame])
        self.srRecords = None
        self.itemRecords = None
        #self.resizable(False, False)
        
    def input_frame_change_callback(self, itemChanged):
        if(itemChanged == 'SPM' or itemChanged == 'MAP'):
            self.process_btn.config(state=tk.NORMAL)
            self.process_item.config(state=tk.DISABLED)
            self.process_map_file.config(state=tk.DISABLED)
            self.process_sr_file.config(state=tk.DISABLED)
            self.process_grad_file.config(state=tk.DISABLED)
            self.stoppageList.delete(first=0, last=tk.END)
            self.stoppageList.config(state=tk.DISABLED)
            self.itemFrame.clear_selection_frame()
            self.srFrame.clear_selection_frame()
            self.spmInfoFrame.state_reset()
            self.spmInfoFrame.spm_state_reset()
            self.disable_frames([self.plotConfigFrame,self.outputFrame])

        if(itemChanged == 'GRAD'):
            self.showGrad_btn.config(state=tk.DISABLED)
            self.showGradAnnot_btn.config(state=tk.DISABLED)

        if(itemChanged == 'SR'):
            self.showSr_btn.config(state=tk.DISABLED)
        """
        if(itemChanged == 'MAP'):
            self.process_map_file.config(state=tk.NORMAL)
            self.process_item.config(state=tk.DISABLED)
            self.process_sr_file.config(state=tk.DISABLED)
            self.showItem_btn.config(state=tk.DISABLED)
            self.showTicks_btn.config(state=tk.DISABLED)
            self.showGrad_btn.config(state=tk.DISABLED)
            self.showGradAnnot_btn.config(state=tk.DISABLED)
            self.showSr_btn.config(state=tk.DISABLED)
        """
    def disable_frames(self, frames):
        for frame in frames:
            for child in frame.winfo_children():
                child.configure(state=tk.DISABLED)

    def enable_frames(self, frames):
        for frame in frames:
            for child in frame.winfo_children():
                child.configure(state=tk.NORMAL)

    def plot_dist_speed(self, save=False, directory='', report=False):
        spmInfoData = self.spmInfoFrame.getSpmInfoData()
        startLoc = spmInfoData.startLoc.strip()
        cum_distance = self.cum_dist_vals[-1]/1000
        direction = spmInfoData.direction
        showItem = (self.showItem_btn.cget('state') == tk.NORMAL and self.showItem.get() == 1)
        showIntersect = (self.showIntersect_btn.cget('state') == tk.NORMAL and self.showIntersect.get() == 1)
        showGrad = (self.showGrad_btn.cget('state') == tk.NORMAL and self.showGrad.get() == 1)
        showSr = (self.showSr_btn.cget('state') == tk.NORMAL and self.showSr.get() == 1)
        self.plotGrad = False
        plotItem = False

        fig, ax1 = plt.subplots()
        color = 'tab:blue'
        ax1.set_title('Speed vs Distance Plot', weight='bold')
        ax1.set_xlabel('Distance (km)', color='tab:purple', weight='bold')
        ax1.set_ylabel('Speed (kmph)', color=color, weight='bold')

        isXticks = False
        if(self.showTicks_btn.cget('state') == tk.NORMAL and self.showTicks.get() == 1):
            station_labels = []
            xticks = []
            for itemRecord in self.itemRecords:
                stationRecords = itemRecord.stationRecords
                if(len(stationRecords) > 0):
                    stationName = stationRecords[0].station_name
                    
                    km_chainage = itemRecord.km_chainage
                    diff_list = [cum_dist_value - km_chainage*1000 for cum_dist_value in self.cum_dist_vals]
                    index = np.argmin(np.abs(diff_list))
                    nearest_x = self.cum_dist_vals[index]
                    
                    xticks.append(nearest_x)
                    station_labels.append(stationName)

            if(len(station_labels) > 0):
                ax1.set_xlabel('Stations', color='tab:purple', weight='bold')
                ax1.tick_params(axis='x', labelcolor='tab:purple', labelsize='medium', width=3)
                ax1.set_xticks(xticks, labels=station_labels, rotation=90)
                isXticks = True
            else:
                mb.showwarning('Warning', 'No Station Records Found in Mapping. Plotting without station ticks')

            mps_attained = max(self.speed_vals)
            yticks = np.arange(0, mps_attained, 5)
            if mps_attained not in yticks:
                yticks = np.append(yticks, mps_attained)

            ax1.tick_params(axis='y', labelcolor='tab:blue', labelsize='small', width=2)
            ax1.set_yticks(yticks)

            for tick in ax1.get_xticklabels():
                tick.set_fontweight('bold')
            for tick in ax1.get_yticklabels():
                tick.set_fontweight('bold')

        if(self.showGrid_btn.cget('state') == tk.NORMAL and self.showGrid.get() == 1):
            if(isXticks):
                ax1.grid(axis='x', color = 'tab:purple', linestyle = '-.', linewidth = 1)
                ax1.grid(axis='y', linestyle = '-', linewidth = 0.5)
            else:
                ax1.grid()

        ax2 = None

        if(showItem or showGrad or showSr):
            if(startLoc == ''):
                mb.showwarning('Warning', 'To show Items/Gradient/Speed Restrictions, startLoc must be specified.\nPlotting without showing Items/Gradient/Speed Restrictions.')
            elif(len(self.chainRecords) == 0):
                mb.showwarning('Warning', 'To show Items/Gradient/Speed Restrictions chainage data must be present.\nPlotting without showing Items/Gradient/Speed Restrictions.')
            else:
                startKm, islocfound = mp.find_chainage_km(self.chainRecords,startLoc)
                if(islocfound):
                    if(self.showSr_btn.cget('state') == tk.NORMAL and showSr == 1):
                        srList = self.srFrame.get_rframe_items()
                        plot_sr_records = []
                        trainLength = 0
                        spmInfoData = self.spmInfoFrame.getSpmInfoData()
                        try:
                            trainLength = 0 if spmInfoData.trainLength is None or spmInfoData.trainLength.strip() == '' else int(spmInfoData.trainLength)
                        except BaseException as error:
                            trainLength = 0

                        for sr in srList:
                            serialNo = sr[:sr.find('.')]
                            srString = sr[sr.find('.')+1:]
                            #print('SR String: ' + srString + '\n')
                            for storedSrRecord in self.srRecords:
                                #print('Stored SR String' + ':::' + storedSrRecord.srString() + '\n')
                                if storedSrRecord.isSpeedRestriction(srString):
                                    plotSrTuple = (serialNo, storedSrRecord)
                                    plot_sr_records.append(plotSrTuple)
                        
                        #mb.showinfo('SR Items', f'Items in Plot SR tuple {len(plot_sr_records)}')
                        mp.plot_sr_records(axis=ax1, plotSrRecords=plot_sr_records, multiplier=1000, trainLength=trainLength)

                    if(self.showGrad_btn.cget('state') == tk.NORMAL and showGrad == 1):
                        if(self.gradientRecords != None and len(self.gradientRecords) != 0):
                            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
                            color = 'tab:olive'
                            ax2.set_ylabel('Gradient (m)', color=color)
                            (self.grad_xvals, self.grad_yvals) = gp.plot_gradient(axis=ax2, plotColor=color, multiplier=1000, gradientRecords=self.gradientRecords)
                            self.plotGrad = True
                        else:
                            mb.showwarning('Warning', 'To show Gradient, Gradient File must be specified.\nPlotting without showing Gradient.')

                    if(self.showItem_btn.cget('state') == tk.NORMAL and showItem == 1):
                        itemList = self.itemFrame.get_rframe_items()
                        plot_item_records = []
                        
                        for item in itemList:
                            serialNo = item[:item.find('.')]
                            itemString = item[item.find('.')+1:]
                            itemRecord = ItemRecord.buildItemRecord(itemString)
                            for storedItemRecord in self.itemRecords:
                                if storedItemRecord == itemRecord:
                                    plotTuple = (serialNo, storedItemRecord)
                                    plot_item_records.append(plotTuple)

                        mp.plot_item_records(axis=ax1, plotItemRecords=plot_item_records, multiplier=1000, y_location=max(self.speed_vals))
                        plotItem = True
                else:
                    mb.showwarning('Warning', 'Valid starting location not found in given mapping file.\nPlotting without showing Items/Gradient/Speed Restrictions.')

        color='tab:blue'
        ax1.plot(self.cum_dist_vals, self.speed_vals, color=color)
        
        plotBft = self.showBft_btn.cget('state') == tk.NORMAL and self.showBft.get() == 1
        plotBpt = self.showBpt_btn.cget('state') == tk.NORMAL and self.showBpt.get() == 1

        if(plotBft):
            if(self.bft_start_index != -1 and self.bft_end_index != -1):
                color='tab:orange'
                bft_speeds = self.speed_vals[self.bft_start_index:self.bft_end_index+1]
                bft_cum_dist = self.cum_dist_vals[self.bft_start_index:self.bft_end_index+1]
                bft_x_vals = [bft_cum_dist[0], bft_cum_dist[-1]]
                bft_y_vals = [bft_speeds[0], bft_speeds[-1]]
                ax1.plot(bft_cum_dist, bft_speeds, color=color, label="BFT")
                ax1.plot(bft_x_vals, bft_y_vals, 'go')
        
        if(plotBpt):
            if(self.bpt_start_index != -1 and self.bpt_end_index != -1):
                color='tab:brown'
                bpt_speeds = self.speed_vals[self.bpt_start_index:self.bpt_end_index+1]
                bpt_cum_dist = self.cum_dist_vals[self.bpt_start_index:self.bpt_end_index+1]
                bpt_x_vals = [bpt_cum_dist[0], bpt_cum_dist[-1]]
                bpt_y_vals = [bpt_speeds[0], bpt_speeds[-1]]
                ax1.plot(bpt_cum_dist, bpt_speeds, color=color, label="BPT")
                ax1.plot(bpt_x_vals, bpt_y_vals, 'ro')
        
        if(plotBft or plotBpt):
            ax1.legend(loc="upper left")
        
        if(self.showMps_btn.cget('state') == tk.NORMAL and self.showMps.get() == 1):
            try:
                mps = float(self.spmInfoFrame.getSpmInfoData().mps.strip())
                x_vals = [0, cum_distance*1000]
                y_vals = [mps, mps]
                ax1.plot(x_vals, y_vals, color='magenta')
                mpsFromStr = self.spmInfoFrame.getSpmInfoData().speedFrom.strip()
                if(mpsFromStr != ''):
                    mpsFrom = float(mpsFromStr)
                    x_vals = [0, cum_distance*1000]
                    y_vals = [mpsFrom, mpsFrom]
                    ax1.plot(x_vals, y_vals, color='yellow')
                    
                mpsToStr = self.spmInfoFrame.getSpmInfoData().speedTo.strip()
                if(mpsToStr != ''):
                    mpsTo = float(mpsToStr)
                    x_vals = [0, cum_distance*1000]
                    y_vals = [mpsTo, mpsTo]
                    ax1.plot(x_vals, y_vals, color='yellow')
            except BaseException as error:
                mb.showerror('Error', 'Invalid MPS or Speed From/To values entered. Plotting without MPS/Speed From/To lines.\nError occured: {}'.format(error))

        if(self.showIntersect_btn.cget('state') == tk.NORMAL and showIntersect == 1):
            if(plotItem):
                intersect_x_vals = []
                intersect_y_vals = []
                for sNo, itemRecord in plot_item_records:
                    km_chainage = itemRecord.km_chainage
                    diff_list = [cum_dist_val - km_chainage*1000 for cum_dist_val in self.cum_dist_vals]
                    index = np.argmin(np.abs(diff_list))
                    nearest_x = self.cum_dist_vals[index]
                    nearest_y = self.speed_vals[index]
                    intersect_x_vals.append(nearest_x)
                    intersect_y_vals.append(nearest_y)

                ax1.plot(intersect_x_vals, intersect_y_vals, 'mo')
                
            zero_x_vals = [tup[-1] for tup in self.zeroClusters]
            ax1.plot(zero_x_vals, [0.0]*len(self.zeroClusters), 'mo')
        
        if(save and directory.strip() != ''):
            if not os.path.exists(directory):
                os.mkdir(directory)
            savePath = os.path.join(directory,  'SpeedDistancePlot.png')
            if(not report):
                fig.tight_layout()
                fig.set_size_inches(32,18)

            fig.savefig(savePath, bbox_inches='tight')
            print('Speed Distance Plot Saved in ' + savePath)
            plt.close()
            return savePath
        else:
            fig.tight_layout()
            self.km_chainage_list = [chainRec.km_chainage for chainRec in self.filteredChainRecs]
            self.mast_km_list = [chainRec.mast_km for chainRec in self.filteredChainRecs]
            
            #print(self.km_chainage_list[-1])
            #print(self.mast_km_list[-1])
            #print(self.cum_dist_vals[-1])

            fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
            self.ax1 = ax1
            if(self.plotGrad):
                self.ax2 = ax2
            
            plt.show()

    def save_plots(self):
        directory = fd.askdirectory(title="Open directory", initialdir="/")
        if directory:
            self.plot_speed_time(save=True, directory=directory, report=False)
            self.plot_dist_speed(save=True, directory=directory, report=False)
            self.save_stoppages(directory)
            self.plot_current_voltage(save=True, directory=directory)
            self.plot_energy(save=True, directory=directory)
            mb.showinfo('Information', f'Plots saved in {directory}')

    def plot_current_stoppage(self):
        index = self.stoppageList.curselection()
        if index:
            self.plot_stoppage(index, save=False)

    def save_stoppages(self, directory=''):
        for index in range(self.stoppageList.index(tk.END)):
            self.plot_stoppage(index, save=True, directory=directory)

    def plot_stoppage(self, index, save=False, directory=''):
        plot_x_vals = []
        plot_y_vals = []
        stop_date_time_vals = []

        list_value = float(self.stoppageList.get(index))
        cumDistIndex, zeroCumDist = (float('-inf'),float('-inf'))
        for zeroCluster in self.zeroClusters:
            i, zeroCumDist = zeroCluster
            if(list_value == round(zeroCumDist,2)):
                cumDistIndex = i
                zeroCumDist = list_value

        if(cumDistIndex == float('-inf') or zeroCumDist == float('-inf')):
            mb.showwarning('Warning', 'The zero not found in Zero clusters')
        else:
            #print(f'Speed at zero cluster {list_value} is {self.speed_vals[cumDistIndex]} at index {cumDistIndex}')
            cumDistIndex2 = cumDistIndex
            for cum_dist_value in self.cum_dist_vals[cumDistIndex:0:-1]:
                if((list_value - cum_dist_value) <= 1500):
                    plot_cum_dist_value = cum_dist_value - list_value
                    plot_speed = self.speed_vals[cumDistIndex]
                    stop_date_time = self.date_time_vals[cumDistIndex]
                    plot_x_vals.append(plot_cum_dist_value)
                    plot_y_vals.append(plot_speed)
                    stop_date_time_vals.append(stop_date_time)
                    cumDistIndex -= 1
            if(len(plot_x_vals) > 0):
                xticks1 = np.arange(0, plot_x_vals[-1], -100)
                xticks1 = np.append(xticks1, plot_x_vals[-1])   
            else:
                xticks1 = np.arange(0, -100)
                
            plot_x_vals.reverse()
            plot_y_vals.reverse()
            stop_date_time_vals.reverse()
            xticks1 = np.flip(xticks1)

            for cum_dist_value in self.cum_dist_vals[cumDistIndex2:]:
                if((cum_dist_value - list_value) <= 1500):
                    plot_cum_dist_value = cum_dist_value - list_value
                    plot_speed = self.speed_vals[cumDistIndex2]
                    stop_date_time = self.date_time_vals[cumDistIndex2]
                    plot_x_vals.append(plot_cum_dist_value)
                    plot_y_vals.append(plot_speed)
                    stop_date_time_vals.append(stop_date_time)
                    cumDistIndex2 += 1
            if(len(plot_x_vals) > 0):
                xticks2 = np.arange(0, plot_x_vals[-1], 100)
                xticks2 = np.append(xticks2, plot_x_vals[-1])    
            else:
                xticks2 = np.arange(0, 100)

            xticks = np.append(xticks1, xticks2)

            fig, self.stopaxis = plt.subplots()
            fig.subplots_adjust(bottom=0.15)
            color = 'tab:red'
            self.stopaxis.set_xlabel('Distance (m)')
            self.stopaxis.set_ylabel('Speed (kmph)', color=color)
            color='tab:red'                
            self.stopaxis.plot(plot_x_vals, plot_y_vals, color=color, lw=2)
            self.stop_x_vals = plot_x_vals
            self.stop_y_vals = plot_y_vals
            self.stop_datetime_vals = stop_date_time_vals
            self.stopaxis.grid()
            self.stopaxis.set_title(f'Stoppage Plot for ~1500m at stoppage {list_value}m')
            #xticks = np.arange(plot_x_vals[0], plot_x_vals[-1], 100)
            self.stopaxis.set_xticks(xticks)

            if(save and directory.strip() != ''):
                if not os.path.exists(directory):
                    os.mkdir(directory)
                savePath = os.path.join(directory,  f'StoppagePlot_{index+1}.png')
                fig.tight_layout()
                fig.set_size_inches(32,18)
                fig.savefig(savePath, bbox_inches='tight')
                print(f'Stoppage Plot {index+1} saved in ' + savePath)
                plt.close()
            else:
                axbox = fig.add_axes([0.1, 0.05, 0.8, 0.040])
                display_value = 'Speed Diff: 0.0 kmph (0.0 m/s); Distance Diff: 0.0 m (0.0 km); Time Diff: 0 s; Avg Acc/Dcc: 0 m/s2'
                self.stop_text_box = TextBox(axbox, "Selection Info:", textalignment="center")
                self.stop_text_box.set_val(display_value) 
                #annotation = ax.annotate(text=annotate_text, xy=(0,0))

                self.rect_selector = RectangleSelector(self.stopaxis, self.onselect_function, button=[1])

                #fig.tight_layout()
                fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_stop)

                plt.show()
    
    def on_mouse_move_stop(self, event):
        if event.xdata is not None and event.ydata is not None:
            if(event.xdata > self.stop_x_vals[0] and event.xdata < self.stop_x_vals[-1]):
                index = np.argmin(np.abs(self.stop_x_vals - event.xdata))
                nearest_x = self.stop_x_vals[index]
                nearest_date_time = self.stop_datetime_vals[index].strftime('%d-%m-%y %H:%M:%S')
                nearest_y = self.stop_y_vals[index]

                for artist in self.stopaxis.texts:
                    artist.remove()
                
                for collection in self.stopaxis.collections:
                    collection.remove()

                self.stopaxis.annotate(f'({nearest_x:.2f}, {nearest_y:.2f})\n({nearest_date_time})',
                            xy=(event.xdata, event.ydata),
                            xytext=(-20, 20),
                            textcoords='offset points',
                            ha='right')
                self.stopaxis.scatter(nearest_x, nearest_y, s=30, color='green', alpha=0.5)
                plt.draw()

    def onselect_function(self, eclick, erelease):
        extent = self.rect_selector.extents
        yextent = round(extent[3]-extent[2],2)
        speeddiff = round((extent[3]-extent[2])*(5/18),2)
        xextent = round(extent[1]-extent[0],2)
        distdiff = round(xextent/1000, 2)
        diff_list = [stop_x_val - extent[1] for stop_x_val in self.stop_x_vals]
        index1 = np.argmin(np.abs(diff_list))
        diff_list = [stop_x_val - extent[0] for stop_x_val in self.stop_x_vals]
        index2 = np.argmin(np.abs(diff_list))
        nearest_date_time1 = self.date_time_vals[index1]
        nearest_date_time2 = self.date_time_vals[index2]
        a_timedelta = nearest_date_time1 - nearest_date_time2
        timeDiffSec = abs(a_timedelta.total_seconds())
        avg_acc = round(speeddiff/timeDiffSec,2)

        display_value = f'Speed Diff: {yextent} kmph ({speeddiff} m/s); Distance Diff: {xextent} m ({distdiff} km); Time Diff: {timeDiffSec} s; Avg Acc/Dcc: {avg_acc} m/s2'
        self.stop_text_box.set_val(display_value)
        #annotation.set(position=(extent[1], extent[3]), horizontalalignment='center', verticalalignment='bottom')
        #annotation.set_text(display_value)

    def plot_current_voltage(self, save=False, directory=''):
        plot_x_vals = []
        fig, self.currentaxis = plt.subplots()
                  
        self.currentaxis.set_xlabel('Distance (km)', color='tab:purple', weight='bold')
        plot_x_vals = self.cum_dist_vals

        color = 'tab:blue' 
        self.currentaxis.set_ylabel('Current (A)', color=color, weight='bold')
        self.currentaxis.set_title('Current, Voltage vs Distance Plot')
        plot_y_current_vals = self.current_vals
        self.currentaxis.plot(plot_x_vals, plot_y_current_vals, color=color)

        self.voltageaxis = self.currentaxis.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:olive'
        self.voltageaxis.set_ylabel('Voltage (kV)', color=color, weight='bold')
        plot_y_voltage_vals = self.voltage_vals
        self.voltageaxis.plot(plot_x_vals, plot_y_voltage_vals, color=color)
        
        if(self.showGrid_btn.cget('state') == tk.NORMAL and self.showGrid.get() == 1):
            self.currentaxis.grid()
        
        if(save and directory.strip() != ''):
            if not os.path.exists(directory):
                os.mkdir(directory)
            savePath = os.path.join(directory,  'CurrentVoltagePlot.png')
            fig.tight_layout()
            fig.set_size_inches(32,18)
            fig.savefig(savePath, bbox_inches='tight')
            print('Current Voltage Plot Saved in ' + savePath)
            plt.close()
            return savePath
        else:
            fig.tight_layout()
            fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_current_voltage)

            plt.show()

    def on_mouse_move_current_voltage(self, event):
        if event.xdata is not None and event.ydata is not None:
            if(event.xdata > 0 and event.xdata < self.cum_dist_vals[-1]):
                index = np.argmin(np.abs(self.cum_dist_vals - event.xdata))
                
                nearest_x = self.cum_dist_vals[index]
                nearest_current = self.current_vals[index]
                nearest_voltage = self.voltage_vals[index]

                for artist in self.currentaxis.texts:
                    artist.remove()
                
                for collection in self.currentaxis.collections:
                    collection.remove()

                for artist in self.voltageaxis.texts:
                    artist.remove()
                
                for collection in self.voltageaxis.collections:
                    collection.remove()

                self.voltageaxis.annotate(f'({round(nearest_x,2)} m, {nearest_current} A, {nearest_voltage} kV)',
                            xy=(event.xdata, event.ydata),
                            xytext=(-20, 20),
                            textcoords='offset points',
                            ha='right')
                
                self.voltageaxis.scatter(nearest_x, nearest_voltage, s=30, color='red', alpha=0.5)
                self.currentaxis.scatter(nearest_x, nearest_current, s=30, color='green', alpha=0.5)
                
                plt.draw()

    def plot_energy(self,save=False,directory=''):
        plot_x_vals = []
        fig, self.energyaxis = plt.subplots()
                  
        self.energyaxis.set_xlabel('Distance (km)', color='tab:purple', weight='bold')
        plot_x_vals = self.cum_dist_vals
 
        self.energyaxis.set_ylabel('Energy (kWh)', color='tab:blue', weight='bold')
        self.energyaxis.set_title('Energy vs Distance Plot')
        plot_y_henergy_vals = self.haltEnergy_vals
        plot_y_renergy_vals = self.runEnergy_vals
        plot_y_tenergy_vals = self.totalEnergy_vals
        
        self.energyaxis.plot(plot_x_vals, plot_y_henergy_vals, color='tab:olive', label='Halt Energy')
        self.energyaxis.plot(plot_x_vals, plot_y_renergy_vals, color='tab:brown', label='Run Energy')
        self.energyaxis.plot(plot_x_vals, plot_y_tenergy_vals, color='tab:blue', label='Total Energy')
        self.energyaxis.legend(loc="upper left")
        
        if(self.showGrid_btn.cget('state') == tk.NORMAL and self.showGrid.get() == 1):
            self.energyaxis.grid()
        
        if(save and directory.strip() != ''):            
            if not os.path.exists(directory):
                os.mkdir(directory)
            savePath = os.path.join(directory,  'EnergyPlot.png')
            fig.tight_layout()
            fig.set_size_inches(32,18)
            fig.savefig(savePath, bbox_inches='tight')
            print('Energy Plot Plot Saved in ' + savePath)
            plt.close()
            return savePath
        else:
            fig.tight_layout()
            fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_energy)

            plt.show()

    def on_mouse_move_energy(self, event):
        if event.xdata is not None and event.ydata is not None:
            if(event.xdata > 0 and event.xdata < self.cum_dist_vals[-1]):
                index = np.argmin(np.abs(self.cum_dist_vals - event.xdata))
                
                nearest_x = self.cum_dist_vals[index]
                nearest_henergy = self.haltEnergy_vals[index]
                nearest_renergy = self.runEnergy_vals[index]                
                nearest_tenergy = self.totalEnergy_vals[index]

                for artist in self.energyaxis.texts:
                    artist.remove()
                
                for collection in self.energyaxis.collections:
                    collection.remove()

                self.energyaxis.annotate(f'({round(nearest_x,2)} m, \nHalt Energy: {nearest_henergy} kWh, \nRun Energy: {nearest_renergy} kWh, \nTotal Energy: {nearest_tenergy} kWh)',
                            xy=(event.xdata, event.ydata),
                            xytext=(-20, 20),
                            textcoords='offset points',
                            ha='right')
                
                self.energyaxis.scatter(nearest_x, nearest_henergy, s=30, color='blue', alpha=0.5)
                self.energyaxis.scatter(nearest_x, nearest_renergy, s=30, color='green', alpha=0.5)
                self.energyaxis.scatter(nearest_x, nearest_tenergy, s=30, color='red', alpha=0.5)
                
                plt.draw()

    def plot_speed_time(self, save=False, directory='', report=False):
        plot_x_vals = []
        plot_y_vals = []
        self.date_time_vals
        fig, self.speedaxis = plt.subplots()

        color = 'tab:green'        
        self.speedaxis.set_xlabel('Time')
        self.speedaxis.set_ylabel('Speed (kmph)', color=color)                
        
        plot_x_vals = np.arange(0, len(self.date_time_vals))
        plot_y_vals = self.speed_vals

        self.speedaxis.plot(plot_x_vals, plot_y_vals, color=color)
    
        self.speedaxis.set_title('Speed vs Time Plot')
        total_points = len(self.date_time_vals)
        skip_ticks = int(total_points/50)

        xticks = np.arange(0, plot_x_vals[-1], skip_ticks)
        xlabels = [self.date_time_vals[index].strftime('%H:%M:%S') for index in xticks]
        self.speedaxis.set_xticks(xticks, labels=xlabels, rotation=90)

        if(self.showGrid_btn.cget('state') == tk.NORMAL and self.showGrid.get() == 1):
            self.speedaxis.grid()
        
        if(self.showMps_btn.cget('state') == tk.NORMAL and self.showMps.get() == 1):
            try:
                mps = float(self.spmInfoFrame.getSpmInfoData().mps.strip())
                x_vals = [0, len(plot_x_vals)]
                y_vals = [mps, mps]
                self.speedaxis.plot(x_vals, y_vals, color='magenta')
                mpsFromStr = self.spmInfoFrame.getSpmInfoData().speedFrom.strip()
                if(mpsFromStr != ''):
                    mpsFrom = float(mpsFromStr)
                    x_vals = [0, len(plot_x_vals)]
                    y_vals = [mpsFrom, mpsFrom]
                    self.speedaxis.plot(x_vals, y_vals, color='yellow')
                
                mpsToStr = self.spmInfoFrame.getSpmInfoData().speedTo.strip()
                if(mpsToStr != ''):
                    mpsTo = float(mpsToStr)
                    x_vals = [0, len(plot_x_vals)]
                    y_vals = [mpsTo, mpsTo]
                    self.speedaxis.plot(x_vals, y_vals, color='yellow')
            except BaseException as error:
                mb.showerror('Error', 'Invalid MPS or Speed From/To values entered. Plotting without MPS/Speed From/To lines.\nError occured: {}'.format(error))

        plotBft = self.showBft_btn.cget('state') == tk.NORMAL and self.showBft.get() == 1
        plotBpt = self.showBpt_btn.cget('state') == tk.NORMAL and self.showBpt.get() == 1

        if(plotBft):
            if(self.bft_start_index != -1 and self.bft_end_index != -1):
                color='tab:orange'
                bft_speeds = self.speed_vals[self.bft_start_index:self.bft_end_index+1]
                bft_time = np.arange(self.bft_start_index, self.bft_end_index+1)
                bft_x_vals = [bft_time[0], bft_time[-1]]
                bft_y_vals = [bft_speeds[0], bft_speeds[-1]]
                self.speedaxis.plot(bft_time, bft_speeds, color=color, label="BFT")
                self.speedaxis.plot(bft_x_vals, bft_y_vals, 'go')
        
        if(plotBpt):
            if(self.bpt_start_index != -1 and self.bpt_end_index != -1):
                color='tab:brown'
                bpt_speeds = self.speed_vals[self.bpt_start_index:self.bpt_end_index+1]
                bpt_time = np.arange(self.bpt_start_index, self.bpt_end_index+1)
                bpt_x_vals = [bpt_time[0], bpt_time[-1]]
                bpt_y_vals = [bpt_speeds[0], bpt_speeds[-1]]
                self.speedaxis.plot(bpt_time, bpt_speeds, color=color, label="BPT")
                self.speedaxis.plot(bpt_x_vals, bpt_y_vals, 'ro')

        if(plotBft or plotBpt):
            self.speedaxis.legend(loc="upper left")

        if(save and directory.strip() != ''):
            if not os.path.exists(directory):
                os.mkdir(directory)
            savePath = os.path.join(directory,  'SpeedTimePlot.png')
            if(not report):
                fig.tight_layout()
                fig.set_size_inches(32,18)

            fig.savefig(savePath, bbox_inches='tight')
            print('Speed Time Plot Saved in ' + savePath)
            plt.close()
            return savePath
        else:
            fig.tight_layout()
            if(self.showSpmAnnot.get() == 1):
                fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_speed)

            plt.show()
    
    def on_mouse_move_speed(self, event):
        if event.xdata is not None and event.ydata is not None:
            if(event.xdata > 0 and event.xdata < len(self.date_time_vals)):
                x_vals = np.arange(0, len(self.date_time_vals))
                index = np.argmin(np.abs(x_vals - event.xdata))
                
                nearest_x = x_vals[index]
                nearest_date = self.date_time_vals[index].strftime('%d-%m-%Y')
                nearest_time = self.date_time_vals[index].strftime('%H:%M:%S')
                nearest_y = self.speed_vals[index]

                for artist in self.speedaxis.texts:
                    artist.remove()
                
                for collection in self.speedaxis.collections:
                    collection.remove()

                self.speedaxis.annotate(f'({nearest_time}, {nearest_y})',
                            xy=(event.xdata, event.ydata),
                            xytext=(-20, 20),
                            textcoords='offset points',
                            ha='right')
                self.speedaxis.scatter(nearest_x, nearest_y, s=30, color='blue', alpha=0.5)
                plt.draw()



    def on_mouse_move(self,event):
        if event.xdata is not None and event.ydata is not None:
            spmannot = False
            gradannot = False
            
            if(self.showSpmAnnot.get() == 1):
                if(event.xdata > 0 and event.xdata < self.cum_dist_vals[-1]):
                    index = np.argmin(np.abs(self.cum_dist_vals - event.xdata))
                    nearest_x = self.cum_dist_vals[index]
                    nearest_date_time = self.date_time_vals[index].strftime('%d-%m-%y %H:%M:%S')
                    nearest_y = self.speed_vals[index]
                    nearest_mast = ''
                    #if(len(self.km_chainage_list) > 0):

                    if(len(self.km_chainage_list) > 0 and nearest_x/1000 <= self.km_chainage_list[-1]):
                        km_diff_list = [km_chainage - nearest_x/1000 for km_chainage in self.km_chainage_list]
                        nearest_km_index = np.argmin(np.abs(km_diff_list))
                        nearest_mast = self.mast_km_list[nearest_km_index]

                    for artist in self.ax1.texts:
                        artist.remove()
                    
                    for collection in self.ax1.collections:
                        collection.remove()
                    
                    spmannot = True


            if(self.showGradAnnot.get() == 1 and self.plotGrad):
                if(event.xdata > 0 and event.xdata < self.cum_dist_vals[-1]):
                    diff_vals = [grad_xval-event.xdata for grad_xval in self.grad_xvals]
                    max_negative_value, max_negative_index, min_positive_value, min_positive_index = self.find_extremes(diff_vals)

                    grad_indices = [max_negative_index, min_positive_index]
                    if((grad_indices[0] >= 0 and grad_indices[0] < len(self.grad_xvals)) and (grad_indices[0] >= 0 and grad_indices[0] < len(self.grad_xvals))): 
                        nearest_grad_x1 = self.grad_xvals[grad_indices[0]]
                        nearest_grad_y1 = self.grad_yvals[grad_indices[0]]

                        nearest_grad_x2 = self.grad_xvals[grad_indices[1]]
                        nearest_grad_y2 = self.grad_yvals[grad_indices[1]]

                        diff_x = nearest_grad_x2-nearest_grad_x1
                        diff_y = nearest_grad_y2-nearest_grad_y1
                        grad_slope = float('inf')
                        if diff_x != 0:
                            grad_slope = diff_y/diff_x

                        bubble_location_x = event.xdata
                        bubble_location_y = nearest_grad_y1 + grad_slope*(bubble_location_x - nearest_grad_x1)

                        for artist in self.ax2.texts:
                            artist.remove()

                        for collection in self.ax2.collections:
                            collection.remove()
                    
                        gradient_text = ''
                        if(diff_x == 0):
                            gradient_text = 'VERTICAL'
                        elif(grad_slope == 0.0):
                            gradient_text = 'LEVEL'
                        else:
                            gradient_text = str(round(1/grad_slope,0))
                        
                        gradannot = True
                    
            if(spmannot and gradannot):
                annotate_text = f'({nearest_x:.2f}, {nearest_y:.2f}, {nearest_mast})\n({nearest_date_time})\n(Slope: {gradient_text})' if nearest_mast != '' else f'({nearest_x:.2f}, {nearest_y:.2f})\n({nearest_date_time})\n(Slope: {gradient_text})'
                self.ax2.annotate(annotate_text,
                                xy=(event.xdata, event.ydata),
                                xytext=(-20, 20),
                                textcoords='offset points',
                                ha='right')
                self.ax2.scatter(bubble_location_x, bubble_location_y, s=30, color='green', alpha=0.5)
                self.ax1.scatter(nearest_x, nearest_y, s=30, color='red', alpha=0.5)
                
            elif(spmannot):
                annotate_text = f'({nearest_x:.2f}, {nearest_y:.2f}, {nearest_mast})\n({nearest_date_time})' if nearest_mast != '' else f'({nearest_x:.2f}, {nearest_y:.2f})\n({nearest_date_time})'
                self.ax1.annotate(annotate_text,
                                xy=(nearest_x, nearest_y),
                                xytext=(-20, 20),
                                textcoords='offset points',
                                ha='right')
                self.ax1.scatter(nearest_x, nearest_y, s=30, color='red', alpha=0.5)
            elif(gradannot):
                self.ax2.annotate(f'(Slope: {gradient_text})',
                                xy=(event.xdata, event.ydata),
                                xytext=(-20, 20),
                                textcoords='offset points',
                                ha='right')
                self.ax2.scatter(bubble_location_x, bubble_location_y, s=30, color='green', alpha=0.5)
            
            if(spmannot or gradannot):
                plt.draw()
    
    def find_extremes(self, lst):
        max_negative_value = float('-inf')
        max_negative_index = -1
        min_positive_value = float('inf')
        min_positive_index = -1

        for i, num in enumerate(lst):
            if num < 0 and num > max_negative_value:
                max_negative_value = num
                max_negative_index = i
            elif num > 0 and num < min_positive_value:
                min_positive_value = num
                min_positive_index = i

        return max_negative_value, max_negative_index, min_positive_value, min_positive_index

    def item_process(self):
        success = False
        #try:
        self.itemRecords = []
        spmInfoData = self.spmInfoFrame.getSpmInfoData()
        cum_distance = self.cum_dist_vals[-1]/1000
        direction = spmInfoData.direction
        
        self.itemRecords = mp.build_item_recs(self.filteredChainRecs, direction)
        items = [itemRecord.itemString() for itemRecord in self.itemRecords]   
        self.itemFrame.clear_selection_frame()      
        self.itemFrame.add_lframe(items)
        itemRecords_len = len(self.itemRecords)
        if(itemRecords_len == 0):
            mb.showwarning('Warning', 'No Item Records found in the mapping file/format for given location.\nPlease change location/mapping file and try.')
            success = False
        else:
            mb.showinfo('Information', f'{itemRecords_len} Item Records found in given SPM duration of distance {cum_distance*1000} m')
            success = True
        #except BaseException as error:
        #    mb.showerror('Error', 'An exception occurred: {}'.format(error))
        #    success = False

        if(success):
            self.showItem_btn.config(state=tk.NORMAL)
            self.showTicks_btn.config(state=tk.NORMAL)
        else:
            self.showItem_btn.config(state=tk.DISABLED)
            self.showTicks_btn.config(state=tk.DISABLED)
            self.itemRecords = []
    
    def sr_file_process(self):
        success = False
        #try:
        self.srRecords = []
        spmInfoData = self.spmInfoFrame.getSpmInfoData()
        cum_distance = self.cum_dist_vals[-1]/1000
        direction = spmInfoData.direction
        startLoc = spmInfoData.startLoc.strip()
        
        if(startLoc == ''):
            mb.showinfo('Information', 'Starting location to be specified to process Speed Restrictions')
            success = False
        else:
            srFileLoc = self.spmInputFrame.getSpmInputData().srFileLoc.strip()
            if(srFileLoc != ''):
                filteredChainRecs = mp.filter_chainage_records(listChainageRecords=self.chainRecords, start_mast_km=startLoc, direction=direction, cum_distance=cum_distance)  
                self.srRecords = mp.build_sr_records(filteredChainRecs, srFileLoc)
                items = [srRecord.srString() for srRecord in self.srRecords]
                self.srFrame.clear_selection_frame()      
                self.srFrame.add_lframe(items)
                srRecords_len = len(self.srRecords)
                if(srRecords_len == 0):
                    mb.showwarning('Warning', 'No SR records found for the given file and format.\nPlease change file and try again.')
                    success = False
                else:
                    mb.showinfo('Information', f'{srRecords_len} SR Records found in given SPM duration of distance {cum_distance*1000} m')
                    success = True
            else:
                mb.showwarning('Warning', 'To process Speed Restrictions SR File must be specified.')
                success = False
        #except BaseException as error:
        #    mb.showerror('Error', 'An exception occurred: {}'.format(error))
        #    success = False

        if(success):
            self.showSr_btn.config(state=tk.NORMAL)
        else:
            self.showSr_btn.config(state=tk.DISABLED)
            self.srRecords = []

    def grad_file_process(self):
        success = False
        try:
            self.gradientRecords = []
            spmInfoData = self.spmInfoFrame.getSpmInfoData()
            cum_distance = self.cum_dist_vals[-1]/1000
            direction = spmInfoData.direction
            startLoc = spmInfoData.startLoc.strip()
            
            if(startLoc == ''):
                mb.showinfo('Information', 'Starting location to be specified to process Speed Restrictions')
                success = False
            else:
                gradFileLoc = self.spmInputFrame.getSpmInputData().gradientFileLoc.strip()
                startKm, islocfound = mp.find_chainage_km(self.chainRecords,startLoc)
                if(islocfound):
                    if(gradFileLoc != ''):
                        self.gradientRecords = gp.gradientParser(gradFileLoc, startKm, cum_distance, direction)
                        gradient_records_len = len(self.gradientRecords)
                        if(gradient_records_len == 0):
                            mb.showwarning('Warning', 'No Gradient records found for the given file and format.\nPlease change file and try again.')
                            success = False
                        else:
                            mb.showinfo('Information', f'{gradient_records_len} Gradient Records found in given SPM duration of distance {cum_distance*1000} m')
                            gp.output_gradient_csv('D:/Pydir/Map Files/GradientFiltered.csv',self.gradientRecords)
                            success = True
                    else:
                        mb.showwarning('Warning', 'To process gradients, Gradient File must be specified.')
                        success = False
                else:
                    mb.showwarning('Warning', 'Starting location not found in mapping file.\nNot processing gradients.')
                    success = False
        except BaseException as error:
            mb.showerror('Error', 'An exception occurred: {}'.format(error))
            success = False

        if(success):
            self.showGrad_btn.config(state=tk.NORMAL)
            self.showGradAnnot_btn.config(state=tk.NORMAL)
        else:
            self.showGrad_btn.config(state=tk.DISABLED)
            self.showGradAnnot_btn.config(state=tk.DISABLED)
            self.gradientRecords = []

    def map_file_process(self):
        success = False
        spmInfoData = self.spmInfoFrame.getSpmInfoData()
        startLoc = spmInfoData.startLoc.strip()
        endLoc = spmInfoData.endLoc.strip()
        spmDist = (self.cum_dist_vals[-1] - self.cum_dist_vals[0])/1000

        #try:
        self.chainRecords = []
        self.filteredChainRecs = []

        mapFileLoc = self.spmInputFrame.getSpmInputData().mapFileLoc.strip()
        if(mapFileLoc != ''):
            self.chainRecords = mp.chainageParser(fileName=mapFileLoc)
            map_records_len = len(self.chainRecords)
            if(map_records_len == 0):
                mb.showwarning('Warning', 'No Map Chainage records found for the given format.\nPlease change file and try again.')
                success = False
            else:
                start_chainage_km, startIsFound = mp.find_chainage_km(self.chainRecords, startLoc)
                end_chainage_km, endIsFound = mp.find_chainage_km(self.chainRecords, endLoc)
                if(startIsFound):
                    message_user = ''
                    if(endIsFound):
                        message_user = f'Mapping file processed successfully... {map_records_len} records processed.\n{startLoc} found in given file with {start_chainage_km} chainage km.\n{endLoc} found in given file with {end_chainage_km} chainage km.'
                    else:
                        message_user = f'Mapping file processed successfully... {map_records_len} records processed.\n{startLoc} found in given file with {start_chainage_km} chainage km.\n{endLoc} not found in mapping file.'
                    mb.showinfo('Information', message_user)
                    success = True
                else:
                    mb.showinfo('Information', f'{startLoc} not found in mapping file. Please try by changing mapping file or mapping location')
                    success = False     
                
                if(startIsFound and endIsFound):
                    start_end_chainage_distance = abs(end_chainage_km - start_chainage_km)
                    chainage_spm_percent = round((start_end_chainage_distance/spmDist)*100,2)
                    user_answer = mb.askyesno('Readjust', f'{endLoc} found in given file with {end_chainage_km} chainage km.\nSPM total distance is {round(spmDist,2)} km\nStart-End Chainage distance is {round(start_end_chainage_distance,2)}\nChainage-SPM Distance Ratio (%) is {chainage_spm_percent}\n\nDo you want to readjust SPM data?')
                    if(user_answer):
                        ratio = start_end_chainage_distance/spmDist
                        self.inst_dist_vals = [inst_dist_val * ratio for inst_dist_val in self.inst_dist_vals]
                        self.cum_dist_vals = [cum_dist_val * ratio for cum_dist_val in self.cum_dist_vals]

                        self.spmEntryRecords = []
                        
                        for i, inst_dist_val in enumerate(self.inst_dist_vals):
                            spmEntry = SpmEntryRecord(self.date_time_vals[i], self.speed_vals[i], inst_dist_val, self.cum_dist_vals[i], self.runEnergy_vals[i], self.haltEnergy_vals[i], self.totalEnergy_vals[i], self.voltage_vals[i], self.current_vals[i], self.pf_vals[i])
                            self.spmEntryRecords.append(spmEntry)

                        self.zeroClusters = self.get_zero_clusters(self.spmEntryRecords)

                        self.stoppageList.delete(first=0, last=tk.END)
                        stoppageListItems = []
                        for i, zeroCluster in self.zeroClusters:
                                stoppageListItems.append(round(zeroCluster,2))

                        self.stoppageList.insert(0, *stoppageListItems)
                        mb.showinfo('Informaton', f'Original SPM resized by Chainage/SPM ratio {round(ratio,2)}')
                    else:
                        mb.showinfo('Informaton', 'Original SPM not resized.')
        else:
            mb.showwarning('Warning', 'Map file location not entered.')
            success = False
        #except BaseException as error:
        #    mb.showerror('Error', 'An exception occurred: {}'.format(error))
        #    success = False

        if(success):
            self.process_map_file.config(state=tk.DISABLED)
            self.process_item.config(state=tk.NORMAL)
            self.process_sr_file.config(state=tk.NORMAL)
            self.process_grad_file.config(state=tk.NORMAL)
            
            cum_distance = self.cum_dist_vals[-1]/1000
            direction = spmInfoData.direction
            self.filteredChainRecs = mp.filter_chainage_records(listChainageRecords=self.chainRecords, start_mast_km=startLoc, direction=direction, cum_distance=cum_distance)
        else:
            self.process_map_file.config(state=tk.NORMAL)
            self.process_item.config(state=tk.DISABLED)
            self.process_sr_file.config(state=tk.DISABLED)
            self.process_grad_file.config(state=tk.DISABLED)
            self.showItem_btn.config(state=tk.DISABLED)
            self.showTicks_btn.config(state=tk.DISABLED)
            self.showGrad_btn.config(state=tk.DISABLED)
            self.showGradAnnot_btn.config(state=tk.DISABLED)
            self.showSr_btn.config(state=tk.DISABLED)
            self.chainRecords = []
            self.filteredChainRecs = []

            self.spmInfoFrame.map_file_process(success=success)

    def spmFromToCalculate(self, spmAnalysisFrom, spmAnalysisTo):
        fromIndex = 0
        toIndex = -1
        fromDate = None
        toDate = None

        try:
            fromDate = datetime.datetime.strptime(str(spmAnalysisFrom).strip(), '%d-%m-%y %H:%M:%S')
        except ValueError:
            fromIndex = 0
            fromDate = None

        try:
            toDate = datetime.datetime.strptime(str(spmAnalysisTo).strip(), '%d-%m-%y %H:%M:%S')
        except ValueError:
            toIndex = -1
            toDate = None
        
        print(f'{fromDate}, {toDate}')
        if(fromDate is not None):
            for i, spmEntryRecord in enumerate(self.spmEntryRecords):
                if(spmEntryRecord.entryDate >= fromDate):
                    fromIndex = i
                    break
        else:
            fromDate = self.spmEntryRecords[0].entryDate
        
        if(toDate is not None):
            for j, spmEntryRecord in enumerate(self.spmEntryRecords):
                if(spmEntryRecord.entryDate >= toDate):
                    toIndex = j
                    break
        else:
            toDate = self.spmEntryRecords[-1].entryDate

        print(f'{fromIndex}, {toIndex}')
        if(fromIndex == toIndex or fromDate >= toDate):
            fromIndex = 0
            toIndex = -1

        return (fromIndex, toIndex)

    def spm_process(self):
        success = False
        #try:
        self.spmEntryRecords = []
        self.date_time_vals = []
        self.speed_vals = []
        self.current_vals = []
        self.voltage_vals = []
        self.haltEnergy_vals = []
        self.runEnergy_vals = []
        self.pf_vals = []
        self.totalEnergy_vals = []
        self.inst_dist_vals = []
        self.cum_dist_vals = []

        self.srRecords = []
        self.gradientRecords = []
        self.itemRecords = []
        self.chainRecords = []
        self.filteredChainRecs = []
        
        self.spmTimeDiff = 0
        self.bft_start_index = -1
        self.bft_end_index = -1
        self.bpt_start_index = -1
        self.bpt_end_index = -1
        
        spmException = False
        try:
            self.spmEntryRecords = self.spmInputFrame.getSpmInputData().spmFileParse()
            spmException = False
        except BaseException as error:
            mb.showwarning('Warning', f'Error in processing the SPM file {error}\n Try changing SPM Type/SPM file')
            spmException = True
            success = False

        records_length = len(self.spmEntryRecords)

        if(not spmException and records_length == 0):
                mb.showwarning('Warning', 'No SPM records found in the given SPM file for the given format.\n Try changing SPM Type/File')
                success = False

        if(not spmException and records_length != 0):
            spmAnalysisFrom = self.spmInputFrame.getSpmInputData().anaFrom
            spmAnalysisTo = self.spmInputFrame.getSpmInputData().anaTo
            
            spmTimeDiffSec = 0
            spmInfoData = self.spmInfoFrame.getSpmInfoData()
            if(spmInfoData.spmTimeDiff is not None and spmInfoData.spmTimeDiff.strip() != ''):
                try:
                    spmTimeDiff_str = spmInfoData.spmTimeDiff.strip()
                    isNegative = spmTimeDiff_str.startswith('-')
                    date_time_str = spmTimeDiff_str[1:]
                    date_time = datetime.datetime.strptime(date_time_str, '%H:%M:%S')
                    a_timedelta = date_time - datetime.datetime(1900, 1, 1)
                    spmTimeDiffSec = -1 * a_timedelta.total_seconds() if isNegative else a_timedelta.total_seconds()
                except BaseException as error:
                    spmTimeDiffSec = 0
            else:
                spmTimeDiffSec = 0
            
            self.spmTimeDiff = spmTimeDiffSec
            for spmEntryRecord in self.spmEntryRecords:
                spmEntryRecord.entryDate = spmEntryRecord.entryDate + datetime.timedelta(seconds=spmTimeDiffSec)

            fromIndex, toIndex = self.spmFromToCalculate(spmAnalysisFrom, spmAnalysisTo)
            self.spmEntryRecords = self.spmEntryRecords[fromIndex:] if toIndex == -1 else self.spmEntryRecords[fromIndex:toIndex]
            cum_dist = 0
            self.total_energy = 0.0
            for spmEntryRecord in self.spmEntryRecords:
                spmEntryRecord.entryCumDist = cum_dist + spmEntryRecord.entryInstDist
                cum_dist += spmEntryRecord.entryInstDist
                self.date_time_vals.append(spmEntryRecord.entryDate)
                self.speed_vals.append(spmEntryRecord.entrySpeed)
                self.current_vals.append(spmEntryRecord.current)
                self.voltage_vals.append(spmEntryRecord.voltage)
                self.haltEnergy_vals.append(spmEntryRecord.haltEnergy)
                self.runEnergy_vals.append(spmEntryRecord.runEnergy)
                self.totalEnergy_vals.append(spmEntryRecord.totalEnergy)
                self.pf_vals.append(spmEntryRecord.pf)
                self.inst_dist_vals.append(spmEntryRecord.entryInstDist)
                self.cum_dist_vals.append(spmEntryRecord.entryCumDist)
                self.total_energy += spmEntryRecord.totalEnergy

            records_len = len(self.spmEntryRecords)
            self.zeroClusters = self.get_zero_clusters(self.spmEntryRecords)
            
            service = self.spmInfoFrame.getSpmInfoData().service
            bft_bpt_list = find_bft_bpt_tuples(self.spmEntryRecords, service)
            bft_tuple = bft_bpt_list[0]
            bpt_tuple = bft_bpt_list[1]

            self.bft_start_index = bft_tuple[0]
            self.bft_end_index = bft_tuple[1]
            self.bpt_start_index = bpt_tuple[0]
            self.bpt_end_index = bpt_tuple[1]

            if(self.bft_start_index != -1 and self.bft_end_index != -1):
                bft_start_distance = self.cum_dist_vals[self.bft_start_index]
                bft_end_distance = self.cum_dist_vals[self.bft_end_index]
                bft_distance = bft_start_distance - bft_end_distance
                if(bft_start_distance > 10000 or bft_end_distance > 10000 or bft_start_distance == self.cum_dist_vals[-1] or bft_distance > 500):
                    self.bft_start_index = -1
                    self.bft_end_index = -1
            else:
                self.bft_start_index = -1
                self.bft_end_index = -1
            
            if(self.bpt_start_index != -1 and self.bpt_end_index != -1):
                bpt_start_distance = self.cum_dist_vals[self.bpt_start_index]
                bpt_end_distance = self.cum_dist_vals[self.bpt_end_index]
                bpt_distance = bpt_start_distance - bpt_end_distance
                if(bpt_start_distance > 15000 or bpt_end_distance > 15000 or bpt_start_distance == self.cum_dist_vals[-1] or bpt_distance > 700):
                    self.bpt_start_index = -1
                    self.bpt_end_index = -1
            else:
                self.bpt_start_index = -1
                self.bpt_end_index = -1

            if(records_len == 0):
                mb.showwarning('Warning', 'No SPM final records found. \nPlease try changing SPM input settings.')
                success = False
            else:
                mb.showinfo('Information', f'SPM file processed successfully... {records_len} records processed.\n SPM time adjusted by {spmTimeDiffSec} seconds')
                success = True
            #except BaseException as error:
            #    mb.showerror('Error', 'An exception occurred: {}'.format(error))
            #    success = False
        
        if(success):
            self.process_btn.config(state=tk.DISABLED)
            self.process_map_file.config(state=tk.NORMAL)
            self.process_item.config(state=tk.DISABLED)
            self.process_sr_file.config(state=tk.DISABLED)
            self.process_grad_file.config(state=tk.DISABLED)
            self.enable_frames([self.plotConfigFrame, self.outputFrame])
            self.showItem_btn.config(state=tk.DISABLED)
            self.showTicks_btn.config(state=tk.DISABLED)
            self.showGrad_btn.config(state=tk.DISABLED)
            self.showGradAnnot_btn.config(state=tk.DISABLED)
            self.showSr_btn.config(state=tk.DISABLED)
            self.stoppageList.config(state=tk.NORMAL)          
            stoppageListItems = []
            for i, zeroCluster in self.zeroClusters:
                    stoppageListItems.append(round(zeroCluster,2))

            self.stoppageList.insert(0, *stoppageListItems)
        else:
            self.process_btn.config(state=tk.NORMAL)
            self.process_map_file.config(state=tk.DISABLED)
            self.process_item.config(state=tk.DISABLED)
            self.process_sr_file.config(state=tk.DISABLED)
            self.process_grad_file.config(state=tk.DISABLED)
            self.stoppageList.delete(first=0, last=tk.END)
            self.stoppageList.config(state=tk.DISABLED)
            self.disable_frames([self.plotConfigFrame, self.outputFrame])
            self.spmEntryRecords = []
            self.date_time_vals = []
            self.speed_vals = []
            self.current_vals = []
            self.voltage_vals = []
            self.haltEnergy_vals = []
            self.runEnergy_vals = []
            self.pf_vals = []
            self.totalEnergy_vals = []
            self.inst_dist_vals = []
            self.cum_dist_vals = []

        self.spmInfoFrame.spm_file_process(success=success)

    def get_zero_clusters(self, spmEntryRecords=[], distance_threshold=10):
        prevCumDist = float('-inf')
        zero_clusters = []
        for i, spmEntryRecord in enumerate(spmEntryRecords):
            speed = spmEntryRecord.entrySpeed
            if speed == 0.0:
                cumDist = spmEntryRecord.entryCumDist
                if((prevCumDist == float('-inf')) or ((cumDist - prevCumDist) > distance_threshold)):
                    cumDistTuple = (i, cumDist)
                    zero_clusters.append(cumDistTuple)
                    prevCumDist = cumDist

        return zero_clusters            

    def write_csv(self):
        try:
            filetypes = (('CSV Files', '*.csv'), ('All Files', '*'))
            filename = fd.asksaveasfilename(title='Output SPM CSV', defaultextension=".csv", initialdir=os.getcwd(), filetypes=filetypes)
            if filename:
                outputCsv(self.spmEntryRecords, filename)
                mb.showinfo('Information', f'CSV File Written Successfully.\nFile output: {filename}')
            else:
                mb.showinfo('Information', 'Operation cancelled!!!')
        except BaseException as error:
            mb.showerror('Error', f'An exception occurred: {error}')

    def generate_report(self):
        #try:
            filetypes = (('PDF Files', '*.pdf'), ('All Files', '*'))
            filename = fd.asksaveasfilename(title='Generate PDF Report', defaultextension=".pdf", initialdir=os.getcwd(), filetypes=filetypes)
            if filename:
                if(self.outputReport(filename)):
                    mb.showinfo('Information', f'PDF Report Generated Successfully.\nFile output: {filename}')
            else:
                mb.showinfo('Information', 'Operation cancelled!!!')
        #except BaseException as error:
        #    mb.showerror('Error', f'An exception occurred: {error}')

    def outputReport(self, filename):
        spmInfoData = self.spmInfoFrame.getSpmInfoData()

        if(spmInfoData.lpPfNo == None or spmInfoData.lpPfNo.strip() == ''):
            mb.showwarning('Warning', 'LP PF No cannot be empty for generating report.\nNot generating report.')
            return False
        else:
            headerTitle = 'SPM Analysis Report'
            if (self.spmInfoFrame.getSpmInfoData().train != None and self.spmInfoFrame.getSpmInfoData().train.strip() != ''):
                headerTitle = headerTitle + ' of ' + self.spmInfoFrame.getSpmInfoData().train
                if(self.spmInfoFrame.getSpmInfoData().tripDate != None and self.spmInfoFrame.getSpmInfoData().tripDate.strip() != ''):
                    headerTitle = headerTitle + ' on ' + self.spmInfoFrame.getSpmInfoData().tripDate

            headerStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=15, align='C',textColor=(220, 50, 50), fillColor=(230, 230, 0), drawColor=(0,80,180),border=True,height=9)
            customPdf = pd.CustomPDF(headerImage=(str(os.getcwd()) + '\\railwaylogo.ico').replace('\\', '/'), headerTitle=headerTitle, headerStyle=headerStyle)

            customPdf.add_customPage(pg.generateSpmSummaryReport(self.spmInfoFrame.getSpmInfoData(), self.spmInputFrame.getSpmInputData()))

            if(self.date_time_vals != None and len(self.date_time_vals) > 0):
                #Add Summary Analysis Summary Report Page
                toShowBft = True if self.showBft_btn.cget('state') == tk.NORMAL and self.showBft.get() == 1 else False
                toShowBpt = True if self.showBpt_btn.cget('state') == tk.NORMAL and self.showBpt.get() == 1 else False
                customPdf.add_customPage(pg.generateAnalysisSummaryReport(spmInfoData=self.spmInfoFrame.getSpmInfoData(), date_time_vals=self.date_time_vals, speed_vals=self.speed_vals, inst_dist_vals=self.inst_dist_vals, cum_dist_vals=self.cum_dist_vals, bftBptList=[self.bft_start_index, self.bft_end_index, self.bpt_start_index, self.bpt_end_index], zeroClusters=self.zeroClusters, current_vals=self.current_vals, voltage_vals=self.voltage_vals, haltEnergy_vals=self.haltEnergy_vals, runEnergy_vals=self.runEnergy_vals, totalEnergy_vals=self.totalEnergy_vals, toShowBft=toShowBft, toShowBpt=toShowBpt, showOverControl=self.overControl_var.get(), showSpeedCompile=self.speedCompile_var.get()))
                
                #Add Speed Groups Report Page
                customPdf.add_customPage(pg.generateSpeedGroupsReport(self.spmInfoFrame.getSpmInfoData(), date_time_vals=self.date_time_vals, speed_vals=self.speed_vals, inst_dist_vals=self.inst_dist_vals, cum_dist_vals=self.cum_dist_vals))

                #Add Stoppage Distance Report
                customPdf.add_customPage(pg.generateStoppageDistanceReport(self.zeroClusters, self.date_time_vals, self.speed_vals, self.cum_dist_vals, spmInfoData=self.spmInfoFrame.getSpmInfoData(), showOverControl=self.overControl_var.get(), showSpeedCompile=self.speedCompile_var.get()))
                
                #Add Stoppage Item Report
                if(self.itemRecords != None and len(self.itemRecords) != 0):
                    customPdf.add_customPage(pg.generateStoppageItemReport(self.zeroClusters, self.itemRecords, self.date_time_vals, self.speed_vals, self.cum_dist_vals, spmInfoData = self.spmInfoFrame.getSpmInfoData()))

                #Add SR Records Page
                if(self.srRecords != None and len(self.srRecords) > 0):
                    customPdf.add_customPage(pg.generateSrReport(self.spmInfoFrame.getSpmInfoData(), self.srRecords, speed_vals=self.speed_vals, cum_dist_vals=self.cum_dist_vals, inst_dist_vals=self.inst_dist_vals, date_time_vals=self.date_time_vals))
                
                #Add Station to station running report
                if(self.itemRecords != None and len(self.itemRecords) > 0):
                    customPdf.add_customPage(pg.generateStationToStationReport(self.itemRecords, self.date_time_vals, self.cum_dist_vals, self.speed_vals))
                
                #Add Gradient Report
                if(self.gradientRecords != None and len(self.gradientRecords) > 0):
                    attackSpeed_str = self.spmInfoFrame.getSpmInfoData().attackSpeed
                    attackSpeed = 0
                    try:
                        attackSpeed = 0 if attackSpeed_str == None or attackSpeed_str.strip() == '' else float(attackSpeed_str)
                    except BaseException as error:
                        attackSpeed = 0
                    customPdf.add_customPage(pg.generateGradientReport(gradientRecords=self.gradientRecords, attackSpeed=attackSpeed, date_time_vals=self.date_time_vals, speed_vals=self.speed_vals, cum_dist_vals=self.cum_dist_vals))

                #Add Item Records Page
                if(self.itemRecords != None and len(self.itemRecords) > 0):
                    customPdf.add_customPage(pg.generateItemReport(self.itemRecords, date_time_vals=self.date_time_vals, speed_vals=self.speed_vals, cum_dist_vals=self.cum_dist_vals))
            #gradientRecords = gp.gradientParser(gradFileLoc, startKm, cum_distance, direction)
            customPdf.process_pages()

            #Add Plots
            saveDir = os.path.join(os.getcwd(), 'Plots')
            customPdf.includeHeader = False
            customPdf.add_page(orientation='L',)
            speed_time_report_plot = self.plot_speed_time(save=True, directory=saveDir, report=True)
            customPdf.image(speed_time_report_plot, x=10, y=10, h=190, w=270)
            customPdf.add_page(orientation='L',)
            speed_distance_report_plot = self.plot_dist_speed(save=True, directory=saveDir, report=True)
            customPdf.image(speed_distance_report_plot, x=10, y=10, h=190, w=270)
            customPdf.output(filename)
            print('User report generated in ' + filename)
            
            #Cleanup the directory
            os.remove(speed_time_report_plot)
            os.remove(speed_distance_report_plot)
            if len(os.listdir(saveDir)) == 0: 
                os.rmdir(saveDir)
            
            if(self.archive_var.get() == True):
                lpArchivePath = os.path.join(os.getcwd(), 'LpDump')
                if not os.path.exists(lpArchivePath):
                    os.mkdir(lpArchivePath)
                lpPath = os.path.join(lpArchivePath, spmInfoData.lpPfNo)
                if not os.path.exists(lpPath):
                    os.mkdir(lpPath)
                #archiveReportPath = os.path.join(lpPath, spmInfoData.tripDate.strip() + '#' + spmInfoData.train.strip() + '#' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
                lpArchiveReportPath = os.path.join(lpPath, spmInfoData.tripDate.strip() + '#' + spmInfoData.train.strip() + '#' + datetime.datetime.now().strftime('%d.%m.%Y') + '.pdf')
                customPdf.output(lpArchiveReportPath)
                print('LP Archive Report generated in ' + lpArchiveReportPath)

                cliArchivePath = os.path.join(os.getcwd(), 'CliDump')
                if not os.path.exists(cliArchivePath):
                    os.mkdir(cliArchivePath)
                cliPath = os.path.join(cliArchivePath, spmInfoData.cliPfNo)
                if not os.path.exists(cliPath):
                    os.mkdir(cliPath)
                #archiveReportPath = os.path.join(lpPath, spmInfoData.tripDate.strip() + '#' + spmInfoData.train.strip() + '#' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
                cliArchiveReportPath = os.path.join(cliPath, spmInfoData.tripDate.strip() + '#' + spmInfoData.train.strip() + '#' + datetime.datetime.now().strftime('%d.%m.%Y') + '.pdf')
                customPdf.output(cliArchiveReportPath)
                print('CLI Archive Report generated in ' + cliArchiveReportPath)

                anaByArchivePath = os.path.join(os.getcwd(), 'AnalysisByDump')
                if not os.path.exists(anaByArchivePath):
                    os.mkdir(anaByArchivePath)
                anaByPath = os.path.join(anaByArchivePath, spmInfoData.analysisBy)
                if not os.path.exists(anaByPath):
                    os.mkdir(anaByPath)
                #archiveReportPath = os.path.join(lpPath, spmInfoData.tripDate.strip() + '#' + spmInfoData.train.strip() + '#' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
                anaByArchiveReportPath = os.path.join(anaByPath, spmInfoData.tripDate.strip() + '#' + spmInfoData.train.strip() + '#' + datetime.datetime.now().strftime('%d.%m.%Y') + '.pdf')
                customPdf.output(anaByArchiveReportPath)
                print('Analysis By Archive Report generated in ' + anaByArchiveReportPath)
            return True
        
    def show_about(self):
        about_text = '''SC Universal SPM App Version 1.0:

SC Division-South Central Railway

Design, Development and Programming:
B.Venkatesh DEE/OP/SC

Acknowledgements:

Leadership and Inspiration:
Shri P.D.Mishra PCEE/SCR
Shri Bhartesh Kumar Jain DRM/SC
Shri Vishnu Kant CEE/Plg & Op/SCR
Shri Rajeev Gangele ADRM/O/SC
Shri M.Gopal ADRM/I/SC

Guidance and Support:
Shri Kosuru Chaitanya Sr.DEE/TRSO/SC
Shri M.Sambasiva Rao ADEE/TRSO/SC

Testing and Feedback:
Shri R.Ramakrisha CLI/SNF
Shri S.Nagaraju Sr.ALP/SNF
Shri B.Santosh Kumar Sr.ALP/KZJ

        '''
        mb.showinfo('About', about_text)

if __name__ == '__main__':
    app = App()
    #width, height = app.winfo_screenwidth(), app.winfo_screenheight()
    #app.geometry('%dx%d+0+0' % (width,height))
    #app.geometry('500x500')
    app.state('zoomed')
    app.mainloop()