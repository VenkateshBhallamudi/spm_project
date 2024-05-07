class SpmEntryRecord:
    def __init__(self, entryDate, entrySpeed, entryInstDist, entryCumDist=0, runEnergy=0.0, haltEnergy=0.0, totalEnergy=0.0, voltage=0.0, current=0.0, pf=0.0):
        self.entryDate = entryDate
        self.entrySpeed = entrySpeed
        self.entryInstDist = entryInstDist
        self.entryCumDist = entryCumDist
        self.runEnergy = runEnergy
        self.haltEnergy = haltEnergy
        self.totalEnergy = totalEnergy
        self.voltage = voltage
        self.current = current
        self.pf = pf
    
    def __lt__(self, obj): 
        return ((self.entryDate) < (obj.entryDate)) 
  
    def __gt__(self, obj): 
        return ((self.entryDate) > (obj.entryDate)) 
  
    def __le__(self, obj): 
        return ((self.entryDate) <= (obj.entryDate)) 
  
    def __ge__(self, obj): 
        return ((self.entryDate) >= (obj.entryDate)) 
  
    def __eq__(self, obj): 
        return (self.entryDate == obj.entryDate) 
    
    def __str__(self):
        return 'Date, Time, Speed, Inst Dist, Cum Dist, Run Energy, Halt Energy, Total Energy, Voltage, Current, PF => {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(self.entryDate.strftime('%d-%m-%y'), self.entryDate.strftime('%H:%M:%S'), str(self.entrySpeed), str(round(self.entryInstDist,2)), str(round(self.entryCumDist,2)), str(round(self.runEnergy,2)), str(round(self.haltEnergy,2)), str(round(self.totalEnergy,2)), str(round(self.voltage, 2)), str(round(self.current, 2)), str(round(self.pf, 2)))