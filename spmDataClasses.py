import spmParsers as ps

class SpmEntryRecord:
    def __init__(self, entryDate, entrySpeed, entryInstDist, entryCumDist=0):
        self.entryDate = entryDate
        self.entrySpeed = entrySpeed
        self.entryInstDist = entryInstDist
        self.entryCumDist = entryCumDist
    
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
        return 'Date, Time, Speed, Inst Dist, Cum Dist=> {}, {}, {}, {}, {}'.format(self.entryDate.strftime('%d-%m-%y'), self.entryDate.strftime('%H:%M:%S'), str(self.entrySpeed), str(round(self.entryInstDist,2)), str(round(self.entryCumDist,2)))
    
class SpmInputData:
    SPM_TYPES = {'Laxven':ps.laxvenParser, 'Medha':ps.medhaParser, 'AAL':ps.aalParser, 'Laxven LT':ps.laxvenLTParser, 'Medha SS':ps.medhaSSParser, 'AAL CSV':ps.aalCsvParser, 'DSL DEMU':ps.dslDemuParser, 'Remlot':ps.remlotParser, 'RTIS':ps.rtisParser, 'CSV Custom':ps.csvParser}
    def __init__(self, spmType='Laxven', spmFileLoc='', mapFileLoc='', gradientFileLoc='', srFileLoc='', anaFrom='', anaTo=''):
        self.spmType = spmType
        self.spmFileLoc = spmFileLoc
        self.mapFileLoc = mapFileLoc
        self.gradientFileLoc = gradientFileLoc
        self.srFileLoc = srFileLoc
        self.anaFrom = anaFrom
        self.anaTo = anaTo
    
    def spmFileParse(self):
        parser = SpmInputData.SPM_TYPES.get(self.spmType)
        return parser(self.spmFileLoc)

    def __str__(self):
        return 'SPM Input Data=> \n SPM Type: {}\n SPM Input File Location: {}\n SPM Mapping File Location: {}\n SPM Gradient File Location: {}\n SPM SR File Location: {}'.format(self.spmType, self.spmFileLoc, self.mapFileLoc, self.gradientFileLoc, self.srFileLoc)

class SpmInfoData:
     #self.fields = ['LP Name', 'LP Designation', 'LP HQ', 'LP PF No', 'LP CMS ID', 'ALP Name', 'ALP HQ', 'ALP PF No', 'ALP CMS ID', 'LP CLI', 'ALP CLI', 'SPM Analysis CLI', 
         #                'From Stn', 'Start Loc', 'To Stn', 'End Loc', 'Section', 'Train', 'Train Length (m)', 'No of Coaches/Wagons', 'Load', 'Loco No', 'Loco Type', 'Loco Base', 
         #                'Trip Date', 'MPS', 'MPS Range From', 'MPS Range To', 'Attacking Speed', 'SPM GPS Time Difference','Remarks']
    def __init__(self, lpName='', lpDesg='', lpHq='', lpPfNo='', lpCmsId='', alpName='', alpHq='', coachWagonType='', alpCmsId='', lpCli='', 
                 alpCli='', cliPfNo='', fromStn='', startLoc='', toStn='', endLoc='', section='', train='', trainLength='', noCw='', load='', 
                 locoNo='', locoType='', locoBase='', locoDueDate='', locoScheduleDue='', tripDate='', mps='',speedFrom='', speedTo='', attackSpeed='', spmTimeDiff='', remarks='', service='', 
                 loadedEmpty='', direction=''):
        self.lpName = lpName
        self.lpDesg = lpDesg
        self.lpHq = lpHq
        self.lpPfNo = lpPfNo
        self.lpCmsId = lpCmsId
        self.alpName = alpName
        self.alpHq = alpHq
        self.coachWagonType = coachWagonType
        self.alpCmsId = alpCmsId
        self.lpCli = lpCli
        self.analysisBy = alpCli
        self.cliPfNo = cliPfNo
        self.fromStn = fromStn
        self.startLoc = startLoc
        self.toStn = toStn
        self.endLoc = endLoc
        self.section = section
        self.train = train
        self.trainLength = trainLength
        self.noCw = noCw
        self.load = load
        self.locoNo = locoNo
        self.locoType = locoType
        self.locoBase = locoBase
        self.locoDueDate = locoDueDate
        self.locoScheduleDue = locoScheduleDue
        self.tripDate = tripDate
        self.mps = mps
        self.speedFrom = speedFrom
        self.speedTo = speedTo
        self.attackSpeed = attackSpeed
        self.spmTimeDiff = spmTimeDiff
        self.remarks = remarks
        self.service = service
        self.loadedEmpty = loadedEmpty
        self.direction = direction

    def __str__(self):
        return f'''SPM Info Data=>LP Name: {self.lpName}, LP Designation: {self.lpDesg}, LP HQ: {self.lpHq}, LP PF No: {self.lpPfNo}, LP CMS ID: {self.lpCmsId},
        ALP Name: {self.alpName}, ALP HQ: {self.alpHq}, Coach/Wagon Type: {self.coachWagonType}, ALP CMS ID: {self.alpCmsId}, LP CLI: {self.lpCli}, ALP CLI: {self.alpCli},
        CLI PF No: {self.cliPfNo}, From Station: {self.fromStn}, Starting Location: {self.startLoc}, To Station: {self.toStn}, Ending Location: {self.endLoc},
        Section: {self.section}, Train: {self.train}, Train Length(m): {self.trainLength}, No of Coaches/Wagons: {self.noCw}, Load: {self.load}, Loco No: {self.locoNo}, 
        Loco Type: {self.locoType}, Loco Base: {self.locoBase}, Trip Date: {self.tripDate}, MPS: {self.mps}, MPS Speed From: {self.speedFrom}, MPS Speed To: {self.speedTo},
        Attacking Speed: {self.attackSpeed}, SPM GPS Time Difference: {self.spmTimeDiff}, Service: {self.service}, Loaded/Empty: {self.loadedEmpty}, Direction: {self.direction},
        Remarks: {self.remarks}'''
    
class Gradient:
    def __init__(self, from_km, to_km, direction, gradient):
        self.from_km = from_km
        self.to_km = to_km
        self.direction = direction
        self.gradient = gradient

    def __lt__(self, obj): 
        return ((self.from_km) < (obj.from_km)) 
  
    def __gt__(self, obj): 
        return ((self.from_km) > (obj.from_km)) 
  
    def __le__(self, obj): 
        return ((self.from_km) <= (obj.from_km)) 
  
    def __ge__(self, obj): 
        return ((self.from_km) >= (obj.from_km)) 
  
    def __eq__(self, obj): 
        return (self.from_km == obj.from_km) 
    
    def __str__(self):
        return f'From_Km, To_Km, Direction, Gradient => {self.from_km}, {self.to_km}, {self.direction}, {self.gradient}'
    
class Chainage:
    def __init__(self, mast_km='', km_chainage=0.0, item='', item_code='', item_disp='', item_type=''):
        self.mast_km = mast_km
        self.km_chainage = km_chainage
        self.item = item
        self.item_code = item_code
        self.item_disp = item_disp
        self.item_type = item_type

    def __lt__(self, obj): 
        return ((self.km_chainage) < (obj.km_chainage)) 
  
    def __gt__(self, obj): 
        return ((self.km_chainage) > (obj.km_chainage)) 
  
    def __le__(self, obj): 
        return ((self.km_chainage) <= (obj.km_chainage)) 
  
    def __ge__(self, obj): 
        return ((self.km_chainage) >= (obj.km_chainage)) 
  
    def __eq__(self, obj): 
        return (self.km_chainage == obj.km_chainage) 
    
    def __str__(self):
        return f'Mast, Km_Chainage, Item, Item Code, Item Disp, Item Type => {self.mast_km}, {self.km_chainage}, {self.item}, {self.item_code}, {self.item_disp}, {self.item_type}'
    
class SpeedRestriction:
    def __init__(self, from_sr='', to_sr='', from_sr_chainage=0.0, to_sr_chainage=0.0, sr_speed=0.0, sr_type=''):
        self.from_sr = from_sr
        self.to_sr = to_sr
        self.from_sr_chainage = from_sr_chainage
        self.to_sr_chainage = to_sr_chainage
        self.sr_speed = sr_speed
        self.sr_type = sr_type

    def srString(self):
        return f'{self.from_sr}-{self.to_sr}#{self.sr_speed}#{self.sr_type}'
    
    def isSpeedRestriction(self, inputSrString):
        return self.srString() == inputSrString

    def __lt__(self, obj): 
        return ((self.from_sr_chainage) < (obj.from_sr_chainage)) 
  
    def __gt__(self, obj): 
        return ((self.from_sr_chainage) > (obj.from_sr_chainage)) 
  
    def __le__(self, obj): 
        return ((self.from_sr_chainage) <= (obj.from_sr_chainage)) 
  
    def __ge__(self, obj): 
        return ((self.from_sr_chainage) >= (obj.from_sr_chainage)) 
  
    def __eq__(self, obj): 
        return (self.from_sr_chainage == obj.from_sr_chainage) 
    
    def __str__(self):
        return f'From SR, To SR, From SR Chainage, To SR Chainage, SR Speed, Chainage Type => {self.from_sr}, {self.to_sr}, {self.from_sr_chainage}, {self.to_sr_chainage}, {self.sr_speed}, {self.sr_type}'

class ItemRecord:
    def __init__(self, itemNo=1, mast_km='', km_chainage=0.0, item='', item_code='', item_disp='', item_type=''):
        self.itemNo = itemNo
        self.mast_km = mast_km
        self.km_chainage = km_chainage
        self.item = item
        self.item_code = item_code
        self.item_disp = item_disp
        self.item_type = item_type
        self.signalRecords = []
        self.nsRecords = []
        self.stationRecords = []

    def add_signalRecord(self, signalRecord=None):
        if(signalRecord != None):
            self.signalRecords.append(signalRecord)

    def add_nsRecord(self, nsRecord=None):
        if(nsRecord != None):
            self.nsRecords.append(nsRecord)

    def add_stationRecord(self, stationRecord=None):
        if(stationRecord != None):
            self.stationRecords.append(stationRecord)

    def itemString(self):
        #return f'{self.item}#{self.item_code}#{self.itemNo}'
        delimiter = '#'
        item_string = ''
        for signalRecord in self.signalRecords:
            item_string = item_string + delimiter + signalRecord.buildSignalRecordStr() if item_string != '' else signalRecord.buildSignalRecordStr()
        
        for nsRecord in self.nsRecords:
            item_string = item_string + delimiter + nsRecord.buildNsRecordStr() if item_string != '' else nsRecord.buildNsRecordStr()
        
        for stationRecord in self.stationRecords:
            item_string = item_string + delimiter + stationRecord.buildStationRecordStr() if item_string != '' else stationRecord.buildStationRecordStr()

        item_string = item_string + delimiter + str(self.itemNo) if item_string != '' else str(self.itemNo)

        return item_string
    
    def buildItemRecord(itemString):
        itemRecord = None
        if(itemString != None and itemString != ''):
            listComponents = itemString.split('#')
            if(len(listComponents) != 0):
                itemNo = int(listComponents[-1])
                itemRecord = ItemRecord(itemNo=itemNo)
        
        return itemRecord
    
    def __lt__(self, obj): 
        return ((self.itemNo) < (obj.itemNo)) 
  
    def __gt__(self, obj): 
        return ((self.itemNo) > (obj.itemNo)) 
  
    def __le__(self, obj): 
        return ((self.itemNo) <= (obj.itemNo)) 
  
    def __ge__(self, obj): 
        return ((self.itemNo) >= (obj.itemNo)) 
  
    def __eq__(self, obj): 
        return (self.itemNo == obj.itemNo) 
    
    def __str__(self):
        return f'ItemNo, Mast, Km_Chainage, Item, Item Code, Item Disp, Item Type => {self.itemNo}, {self.mast_km}, {self.km_chainage}, {self.item}, {self.item_code}, {self.item_disp}, {self.item_type}'

class SignalRecord:
    def __init__(self, signal_name='', signal_location='', signal_direction='', signal_code=''):
        self.signal_name = signal_name
        self.signal_location = signal_location
        self.signal_direction = signal_direction
        self.signal_code = signal_code

    def __str__(self):
            return f'Signal Name, Signal Location, Signal Code, Signal Direction => {self.signal_name}, {self.signal_location}, {self.signal_code}, {self.signal_direction}'
    
    def buildSignalRecordStr(self):
            return f'{self.signal_name}:{self.signal_location}'

class NeutralSectionRecord:
    def __init__(self, ns_location='', ns_direction=''):
        self.ns_location = ns_location
        self.ns_direction = ns_direction

    def __str__(self):
            return f'NS Location, NS Direction => {self.ns_location}, {self.ns_direction}'
    
    def buildNsRecordStr(self):
        return f'NS:{self.ns_location}'

class StationRecord:
    def __init__(self, station_name='', station_direction=''):
        self.station_name = station_name
        self.station_direction = station_direction

    def __str__(self):
        return f'Station Name, Station Direction => {self.station_name}, {self.station_direction}'
    
    def buildStationRecordStr(self):
        return f'STN:{self.station_name}'