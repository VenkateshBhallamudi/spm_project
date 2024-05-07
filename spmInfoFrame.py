import tkinter as tk
from spmDataClasses import SpmInfoData

class SpmInfoFrame(tk.LabelFrame):
    def __init__(self, master, **args):
        super().__init__(master, **args)
        self.fields = ['LP Name', 'LP Designation', 'LP HQ', 'LP PF No', 'LP CMS ID', 'ALP Name', 'ALP HQ', 'ALP CMS ID', 'LP CLI', 'CLI PF No', 'SPM Analysis By', 
                         'From Stn', 'Start Loc (km)', 'To Stn', 'End Loc (km)', 'Section', 'Train', 'Train Length (m)', 'No of Coaches/Wagons', 'Coach/Wagon Type','Total Load (incl Loco) (T)', 'Loco No', 'Loco Type', 'Loco Base', 
                         'Loco Due Date', 'Schedule Due', 'Trip Date', 'MPS (kmph)', 'MPS Range From (kmph)', 'MPS Range To (kmph)', 'Attacking Speed (kmph)', 'SPM GPS Time Difference\n+/-hh:mm:ss','Remarks']
        self.positions = [(0,0), (0,2), (0,4), (1,0), (1,2), (1,4), (2,0), (2,2), (2,4), (3,0), (3,2), (3,4), (4,0), (4,2), (4,4), (5,0), (5,2), (5,4), (6,0), (6,2), (6,4),
                          (7,0), (7,2), (7,4), (8,0), (8,2), (8,4), (9,0), (9,2), (9,4), (10,0), (10,2), (10,4), (11,0)]
        
        self.spmInfoData = SpmInfoData()
        self.labels = [tk.Label(self, text=f) for f in self.fields]
        self.entries = [tk.Entry(self) for _ in self.fields]
        self.labelsMap = dict(zip(self.fields, self.labels))
        self.entriesMap = dict(zip(self.fields, self.entries))
        opts = {'padx':7, 'pady':7, 'sticky':'nw'}

        for i, field in enumerate(self.fields):
            label = self.labelsMap.get(field)
            entry = self.entriesMap.get(field)
            row, column = self.positions[i]
            label.grid(row=row, column=column, **opts)
            entry.grid(row=row, column=column+1, **opts)
        
        #Direction, Goods/Coaching, Loaded/Empty in Option Menu
        i += 1
        row, column = self.positions[i]
        tk.Label(self, text='Goods/Coaching').grid(row=row, column=column, sticky='w', padx=7, pady=7)
        column += 1
        self.serviceOption = tk.StringVar()
        self.serviceOption.set('COACHING')
        self.serviceMenu = tk.OptionMenu(self, self.serviceOption, *('GOODS', 'COACHING'))
        self.serviceMenu.grid(row=row, column=column,  sticky='nwe', padx=7, pady=7)
        column += 1
        
        column = 0 if column == 6 else column
        row = row + 1 if column == 0 else row
        tk.Label(self, text='Loaded/Empty').grid(row=row, column=column, sticky='w', padx=7, pady=7)
        column += 1
        self.loadedEmpty = tk.StringVar()
        self.loadedEmpty.set('EMPTY')
        self.loadedEmptyMenu = tk.OptionMenu(self, self.loadedEmpty, *('LOADED', 'EMPTY'))
        self.loadedEmptyMenu.grid(row=row, column=column,  sticky='nwe', padx=7, pady=7)
        column += 1

        column = 0 if column == 6 else column
        row = row + 1 if column == 0 else row
        tk.Label(self, text='Direction \nDecreasing Km:UP\nIncreasing Km:DOWN').grid(row=row, column=column, sticky='w', padx=7, pady=7)
        self.directionOption = tk.StringVar()
        self.directionOption.set('UP')
        self.directionMenu = tk.OptionMenu(self, self.directionOption, *('UP', 'DOWN'))
        self.directionMenu.grid(row=row, column=column+1,  sticky='nwe', padx=7, pady=7)

        self.initValues_test()

    def initValues_test(self):
        self.entriesMap.get('LP Name').insert(0, 'MUTHYAM POCHAIAH')
        self.entriesMap.get('LP Designation').insert(0, 'LPG')
        self.entriesMap.get('LP HQ').insert(0, 'KZJ')
        self.entriesMap.get('LP PF No').insert(0, '24211515521')
        self.entriesMap.get('LP CMS ID').insert(0, 'KZJ1651')
        self.entriesMap.get('ALP Name').insert(0, 'ALLU KUMAR SWAMY')
        self.entriesMap.get('ALP HQ').insert(0, 'KZJ')
        self.entriesMap.get('Coach/Wagon Type').insert(0, 'BOXNHL')
        self.entriesMap.get('ALP CMS ID').insert(0, 'KZJ3149')
        self.entriesMap.get('LP CLI').insert(0, 'M RAJENDER')
        self.entriesMap.get('SPM Analysis By').insert(0, ' P.SAMPATH KUMAR')
        self.entriesMap.get('CLI PF No').insert(0, '24211501820')
        self.entriesMap.get('From Stn').insert(0, 'PQL')
        self.entriesMap.get('Start Loc (km)').insert(0, '316/27')
        self.entriesMap.get('To Stn').insert(0, 'ZN')
        self.entriesMap.get('End Loc (km)').insert(0, '276/33')
        self.entriesMap.get('Section').insert(0, 'KZJ-SNF')
        self.entriesMap.get('Train').insert(0, '17660')
        self.entriesMap.get('Train Length (m)').insert(0, '533')
        self.entriesMap.get('No of Coaches/Wagons').insert(0, '22')
        self.entriesMap.get('Total Load (incl Loco) (T)').insert(0, '1271')
        self.entriesMap.get('Loco No').insert(0, '32722')
        self.entriesMap.get('Loco Type').insert(0, 'WAG9')
        self.entriesMap.get('Loco Base').insert(0, 'LGD')
        self.entriesMap.get('Loco Due Date').insert(0, '09.07.2024')
        self.entriesMap.get('Schedule Due').insert(0, 'IC')
        self.entriesMap.get('Trip Date').insert(0, '15.04.2024')
        self.entriesMap.get('MPS (kmph)').insert(0, '90')
        self.entriesMap.get('MPS Range From (kmph)').insert(0, '85')
        self.entriesMap.get('MPS Range To (kmph)').insert(0, '95')
        self.entriesMap.get('Attacking Speed (kmph)').insert(0, '60')
        self.entriesMap.get('SPM GPS Time Difference\n+/-hh:mm:ss').insert(0, '+00:00:00')
        self.entriesMap.get('Remarks').insert(0, 'NO REMARKS')

    def initValues(self):
        self.entriesMap.get('SPM GPS Time Difference\n+/-hh:mm:ss').insert(0, '+00:00:00')

    def getSpmInfoData(self):
        self.spmInfoData.lpName = self.entriesMap.get('LP Name').get().strip()
        self.spmInfoData.lpDesg = self.entriesMap.get('LP Designation').get().strip()
        self.spmInfoData.lpHq = self.entriesMap.get('LP HQ').get().strip()
        self.spmInfoData.lpPfNo = self.entriesMap.get('LP PF No').get().strip()
        self.spmInfoData.lpCmsId = self.entriesMap.get('LP CMS ID').get().strip()
        self.spmInfoData.alpName = self.entriesMap.get('ALP Name').get().strip()
        self.spmInfoData.alpHq = self.entriesMap.get('ALP HQ').get().strip()
        self.spmInfoData.coachWagonType = self.entriesMap.get('Coach/Wagon Type').get().strip()
        self.spmInfoData.alpCmsId = self.entriesMap.get('ALP CMS ID').get().strip()
        self.spmInfoData.lpCli = self.entriesMap.get('LP CLI').get().strip()
        self.spmInfoData.analysisBy = self.entriesMap.get('SPM Analysis By').get().strip()
        self.spmInfoData.cliPfNo = self.entriesMap.get('CLI PF No').get().strip()
        self.spmInfoData.fromStn = self.entriesMap.get('From Stn').get().strip()
        self.spmInfoData.startLoc = self.entriesMap.get('Start Loc (km)').get().strip()
        self.spmInfoData.toStn = self.entriesMap.get('To Stn').get().strip()
        self.spmInfoData.endLoc = self.entriesMap.get('End Loc (km)').get().strip()
        self.spmInfoData.section = self.entriesMap.get('Section').get().strip()
        self.spmInfoData.train = self.entriesMap.get('Train').get().strip()
        self.spmInfoData.trainLength = self.entriesMap.get('Train Length (m)').get().strip()
        self.spmInfoData.noCw = self.entriesMap.get('No of Coaches/Wagons').get().strip()
        self.spmInfoData.load = self.entriesMap.get('Total Load (incl Loco) (T)').get().strip()
        self.spmInfoData.locoNo = self.entriesMap.get('Loco No').get().strip()
        self.spmInfoData.locoType = self.entriesMap.get('Loco Type').get().strip()
        self.spmInfoData.locoBase = self.entriesMap.get('Loco Base').get().strip()
        self.spmInfoData.locoDueDate = self.entriesMap.get('Loco Due Date').get().strip()
        self.spmInfoData.locoScheduleDue = self.entriesMap.get('Schedule Due').get().strip()
        self.spmInfoData.tripDate = self.entriesMap.get('Trip Date').get().strip()
        self.spmInfoData.mps = self.entriesMap.get('MPS (kmph)').get().strip()
        self.spmInfoData.speedFrom = self.entriesMap.get('MPS Range From (kmph)').get().strip()
        self.spmInfoData.speedTo = self.entriesMap.get('MPS Range To (kmph)').get().strip()
        self.spmInfoData.attackSpeed = self.entriesMap.get('Attacking Speed (kmph)').get().strip()
        self.spmInfoData.spmTimeDiff = self.entriesMap.get('SPM GPS Time Difference\n+/-hh:mm:ss').get().strip()
        self.spmInfoData.remarks = self.entriesMap.get('Remarks').get().strip()
        self.spmInfoData.service = self.serviceOption.get().strip()
        self.spmInfoData.loadedEmpty = self.loadedEmpty.get().strip()
        self.spmInfoData.direction = self.directionOption.get().strip()

        return self.spmInfoData

    def spm_file_process(self, success=False):
        if(success):
            self.entriesMap.get('SPM GPS Time Difference\n+/-hh:mm:ss').config(state=tk.DISABLED)            
            self.serviceMenu.config(state=tk.DISABLED)
            self.loadedEmptyMenu.config(state=tk.DISABLED)
        else:
            self.spm_state_reset()
    
    def spm_state_reset(self):
        self.entriesMap.get('SPM GPS Time Difference\n+/-hh:mm:ss').config(state=tk.NORMAL)
        self.serviceMenu.config(state=tk.NORMAL)
        self.loadedEmptyMenu.config(state=tk.NORMAL)

    def map_file_process(self, success=False):
        if(success):
            self.entriesMap.get('Start Loc (km)').config(state=tk.DISABLED)
            self.entriesMap.get('End Loc (km)').config(state=tk.DISABLED)
            self.directionMenu.config(state=tk.DISABLED)
        else:
            self.state_reset()
    
    def state_reset(self):
        self.entriesMap.get('Start Loc (km)').config(state=tk.NORMAL)
        self.entriesMap.get('End Loc (km)').config(state=tk.NORMAL)
        self.directionMenu.config(state=tk.NORMAL)