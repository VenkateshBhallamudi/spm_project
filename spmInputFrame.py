import tkinter as tk
from spmDataClasses import SpmInputData
import tkinter.filedialog as fd

class SpmInputFrame(tk.LabelFrame):
    def __init__(self, master, change_callback, **args):
        super().__init__(master, **args)
        self.spmInputData = SpmInputData()
        self.change_callback = change_callback
        i,j=(0,0)
        opts = {'padx':7, 'pady':7}

        tk.Label(self, text='SPM Type', anchor=tk.W).grid(row=i, column=j, columnspan=3, sticky='nw', **opts)

        #Define Tkinter Variables
        self.spmTypeVar = tk.StringVar()
        self.spmTypeVar.trace_add(mode='write', callback=self.variable_trace_spm)
        self.spmFileLocVar = tk.StringVar()
        self.spmFileLocVar.trace_add(mode='write', callback=self.variable_trace_spm)
        self.spmMapLocVar = tk.StringVar()
        self.spmMapLocVar.trace_add(mode='write', callback=self.variable_trace_map)
        self.spmGradientLocVar = tk.StringVar()
        self.spmGradientLocVar.trace_add(mode='write', callback=self.variable_trace_grad)
        self.spmSrLocVar = tk.StringVar()
        self.spmSrLocVar.trace_add(mode='write', callback=self.variable_trace_sr)
        
        self.spmAnalysisFrom = tk.StringVar()
        self.spmAnalysisFrom.trace_add(mode='write', callback=self.variable_trace_ana_from)
        self.spmAnalysisTo = tk.StringVar()
        self.spmAnalysisTo.trace_add(mode='write', callback=self.variable_trace_ana_to)

        self.fileMethodMaps = {'SPM File':self.choose_spm_file, 'Map File':self.choose_mapping_file, 'Grad File':self.choose_gradient_file, 'SR File': self.choose_sr_file}
        self.fileVariableMaps = {'SPM File':self.spmFileLocVar, 'Map File':self.spmMapLocVar, 'Grad File':self.spmGradientLocVar, 'SR File': self.spmSrLocVar}

        #Construct SPM Type Buttons
        
        self.spmTypeVar.set('Laxven')
        self.initValues_testL()
        
        self.spmTypeButtons = [self.create_radio(c) for c in SpmInputData.SPM_TYPES.keys()]
        i,j=(1,0)
        for button in self.spmTypeButtons:
            button.grid(row=i, column=j, sticky='nw', **opts)
            if(j==2):
                i, j = (i+1, 0)
            else:
                j=j+1
        i, j = (i+1, 0)
        tk.Label(self, text='Input Files', anchor=tk.W).grid(row=i, column=j, columnspan=3, sticky='nw', **opts)
        #Construct Opn File Buttons and corresponding entry boxes
        for fileType in self.fileMethodMaps.keys():
            i, j= (i+1, 0)
            tk.Button(self, text='Open '+fileType, command=self.fileMethodMaps.get(fileType)).grid(row=i, column=j, sticky='nsw', **opts)
            j=j+1
            tk.Entry(self, textvariable=self.fileVariableMaps.get(fileType)).grid(row=i, column=j, columnspan=3, sticky='nsew', **opts)
        
        i, j = (i+1, 0)
        tk.Label(self, text='SPM Analysis From\n(dd-mm-yy HH:MM:SS)', anchor=tk.W).grid(row=i, column=j, sticky='nw', **opts)
        j=j+1
        tk.Entry(self, textvariable=self.spmAnalysisFrom).grid(row=i, column=j, columnspan=3, sticky='nsew', **opts)

        i, j = (i+1, 0)
        tk.Label(self, text='SPM Analysis To\n(dd-mm-yy HH:MM:SS)', anchor=tk.W).grid(row=i, column=j, sticky='nw', **opts)
        j=j+1
        tk.Entry(self, textvariable=self.spmAnalysisTo).grid(row=i, column=j, columnspan=3, sticky='nsew', **opts)

    def initValues_test(self):
        self.spmFileLocVar.set('C:/Users/VENKATESH/OneDrive/Desktop/Action Plan/Trial 03.06.2024/17660 03.06.2024.txt')
        self.spmMapLocVar.set('C:/Users/VENKATESH/OneDrive/Desktop/Action Plan/Trial 03.06.2024/Mast Signal Chainage KZJ-SC_Signals_Final MMTS_Updated.csv')
        self.spmGradientLocVar.set('C:/Users/VENKATESH/OneDrive/Desktop/Action Plan/Trial 03.06.2024/Gradient_KZJ-SC.csv')
        self.spmSrLocVar.set('C:/Users/VENKATESH/OneDrive/Desktop/Action Plan/Trial 03.06.2024/SR Map File KZJ-SC.csv')
        self.spmAnalysisFrom.set('')
        self.spmAnalysisTo.set('03-06-24 12:50:04')
    
    def initValues_testL(self):
        self.spmFileLocVar.set('C:/Users/bvenk/OneDrive/Desktop/Action Plan/Trial 03.06.2024/17660 03.06.2024.txt')
        self.spmMapLocVar.set('C:/Users/bvenk/OneDrive/Desktop/Action Plan/Trial 03.06.2024/Mast Signal Chainage KZJ-SC_Signals_Final MMTS_Updated.csv')
        self.spmGradientLocVar.set('C:/Users/bvenk/OneDrive/Desktop/Action Plan/Trial 03.06.2024/Gradient_KZJ-SC.csv')
        self.spmSrLocVar.set('C:/Users/bvenk/OneDrive/Desktop/Action Plan/Trial 03.06.2024/SR Map File KZJ-SC.csv')
        self.spmAnalysisFrom.set('')
        self.spmAnalysisTo.set('03-06-24 12:50:04')
    
    def getSpmInputData(self):
        return self.spmInputData
    
    def updateSpmInputData(self):
        self.spmInputData.spmType = self.spmTypeVar.get()
        self.spmInputData.spmFileLoc = self.spmFileLocVar.get()
        self.spmInputData.mapFileLoc = self.spmMapLocVar.get()
        self.spmInputData.gradientFileLoc = self.spmGradientLocVar.get()
        self.spmInputData.srFileLoc = self.spmSrLocVar.get()
        self.spmInputData.anaFrom = self.spmAnalysisFrom.get()
        self.spmInputData.anaTo = self.spmAnalysisTo.get()
        #print(self.spmInputData)
        

    def variable_trace_spm(self, var, index, mode):
        self.updateSpmInputData()
        self.change_callback('SPM')
        #print('Updated variable: {}'.format(var))

    def variable_trace_map(self, var, index, mode):
        self.updateSpmInputData()
        self.change_callback('MAP')
        #print('Updated variable: {}'.format(var))

    def variable_trace_grad(self, var, index, mode):
        self.updateSpmInputData()
        self.change_callback('GRAD')
        #print('Updated variable: {}'.format(var))

    def variable_trace_sr(self, var, index, mode):
        self.updateSpmInputData()
        self.change_callback('SR')
        #print('Updated variable: {}'.format(var))

    def variable_trace_ana_from(self, var, index, mode):
        self.updateSpmInputData()
        self.change_callback('SPM')
        #print('Updated variable: {}'.format(var))

    def variable_trace_ana_to(self, var, index, mode):
        self.updateSpmInputData()
        self.change_callback('SPM')
        #print('Updated variable: {}'.format(var))

    def create_radio(self, spmType):
        return tk.Radiobutton(self, text=spmType, value=spmType, variable=self.spmTypeVar)
    
    def choose_spm_file(self):
        filename=self.choose_file('Open SPM Input File')
        if filename:
            self.spmFileLocVar.set(filename)
            print('SPM Input File Selected: {}'.format(filename))
    
    def choose_mapping_file(self):
        filename=self.choose_file('Open Mapping File')
        if filename:
            self.spmMapLocVar.set(filename)
            print('SPM Mapping File Selected: {}'.format(filename))

    def choose_gradient_file(self):
        filename=self.choose_file('Open Gradient File')
        if filename:
            self.spmGradientLocVar.set(filename)
            print('SPM Gradient File Selected: {}'.format(filename))

    def choose_sr_file(self):
        filename=self.choose_file('Open SR File')
        if filename:
            self.spmSrLocVar.set(filename)
            print('SPM SR File Selected: {}'.format(filename))

    def choose_file(self, title='Open File', initialdir='D:/Pydir/Map Files'):
        filetypes = (('Plain Text Files', '*.txt'), ('Excel Files', '*.xlsx'), ('All Files', '*'), ('CSV Files', '*.csv'))
        filename = fd.askopenfilename(title=title, initialdir=initialdir, filetypes=filetypes)
        return filename
