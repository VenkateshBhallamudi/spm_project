import pandas as pd
import spmDataClasses as dc
import matplotlib.pyplot as plt
import gradParsers as gp

#Function to output CSV File from list of Chainage Records
def output_chainage_csv(listChainageRecords, fileName):
    #Open the passed Filename
    out_file = open(fileName, 'w')

    #Define CSV header and data initialization
    csv_header = 'Mast_Km,Km_Chainage,Item,Item Code\n'
    out_lines = []
    out_lines.append(csv_header)

    #Iterate through the list of Chainage Entry Records
    for chainageEntryRecord in listChainageRecords:
        #Format the Chainage Entry Record as a CSV record and append to list of output lines
        out_line = chainageEntryRecord.mast_km + ',' + str(chainageEntryRecord.km_chainage) + ',' + chainageEntryRecord.item + ',' + chainageEntryRecord.item_code  + '\n'
        out_lines.append(out_line)
    
    #Write Output to file and close
    out_file.writelines(out_lines)
    out_file.close()

#Function to output CSV File from list of SR Records
def output_sr_csv(listSrRecords, fileName):
    #Open the passed Filename
    out_file = open(fileName, 'w')

    #Define CSV header and data initialization
    csv_header = 'From_SR,To_SR,From_SR_Chainage,To_SR_Chainage,SR_Speed,SR_Type\n'
    out_lines = []
    out_lines.append(csv_header)

    #Iterate through the list of SR Entry Records
    for srEntryRecord in listSrRecords:
        #Format the SR Entry Record as a CSV record and append to list of output lines
        out_line = srEntryRecord.from_sr + ',' + srEntryRecord.to_sr + ',' + str(srEntryRecord.from_sr_chainage) + ',' + str(srEntryRecord.to_sr_chainage) + ',' + str(srEntryRecord.sr_speed) + ',' + srEntryRecord.sr_type + '\n'
        out_lines.append(out_line)
    
    #Write Output to file and close
    out_file.writelines(out_lines)
    out_file.close()

#Filter Chainage Records based on Starting Mast/KM, Direction and Total Distance of SPM
def filter_chainage_records(listChainageRecords, start_mast_km, direction, cum_distance):
    chainage_km, isFound = find_chainage_km(listChainageRecords, start_mast_km)
    filteredChainageRecords = []
    if(isFound):
        for chainageRecord in listChainageRecords:
            difference_km = chainageRecord.km_chainage - chainage_km
            if(abs(round(difference_km*1000,2)) <= round(cum_distance*1000,2)):
                if((direction == 'DOWN' and difference_km >= 0) or (direction == 'UP' and difference_km <= 0)):
                    filteredChainageRecord = dc.Chainage(mast_km=chainageRecord.mast_km, km_chainage=abs(difference_km), item=chainageRecord.item, item_code=chainageRecord.item_code, item_disp=chainageRecord.item_disp, item_type=chainageRecord.item_type)
                    filteredChainageRecords.append(filteredChainageRecord)
    
    return sorted(filteredChainageRecords)

def find_chainage_km(listChainageRecords, start_mast_km):
    if('/' in start_mast_km):
        for i, chainageRecord in enumerate(listChainageRecords):
            if(start_mast_km == chainageRecord.mast_km):
                return (chainageRecord.km_chainage, True)
    elif(start_mast_km != None and start_mast_km.strip() != ''):
        return (float(start_mast_km), True)
    
    return (0, False)

def filter_mast_locs(listChainageRecords):
    mastChainageRecords = []
    for chainageRecord in listChainageRecords:
        if '/' in chainageRecord.mast_km:
            mastChainageRecords.append(chainageRecord)
    
    return mastChainageRecords

def filter_item_locs(listChainageRecords):
    itemChainageRecords = []
    for chainageRecord in listChainageRecords:
        if(not (chainageRecord.item == None or chainageRecord.item.strip() == '')):
            itemChainageRecords.append(chainageRecord)
    
    return itemChainageRecords

def build_item_recs(listChainageRecords, direction):
    itemRecords = []
    i = 0
    for chainageRecord in listChainageRecords:
        if(not (chainageRecord.item == None or chainageRecord.item.strip() == '')):
            item_str = chainageRecord.item.strip()
            itemCode_str = chainageRecord.item_code.strip()
            itemDisp_str = chainageRecord.item_disp.strip()
            itemType_str = chainageRecord.item_type.strip()
            
            itemsList = item_str.split('/')
            itemCodeList = itemCode_str.split('/')
            itemsTypeList = itemType_str.split('/')

            itemRecord = dc.ItemRecord(mast_km=chainageRecord.mast_km, km_chainage=chainageRecord.km_chainage, 
                                       item=item_str, item_code=itemCode_str, item_disp=itemDisp_str, item_type=itemType_str)
            itemPresent = False
            for index, item_val in enumerate(itemsList):
                itemComponents = item_val.strip().split(':')

                item_direction = itemComponents[0].strip()
                item_name = itemComponents[1].strip()
                item_location = itemComponents[2].strip()
                item_code = itemCodeList[index].strip() if index < len(itemCodeList) else ''

                item_type = itemsTypeList[index].strip() if index < len(itemsTypeList) else 'SIG'
                item_type = item_type if (item_type == 'SIG' or item_type == 'NS' or item_type == 'STN') else 'SIG'
                
                if((direction == 'UP' and item_direction == 'UP') or (direction == 'DOWN' and item_direction == 'DN')):
                    if(item_type == 'SIG'):
                        signalRecord = dc.SignalRecord(signal_name=item_name, signal_location=item_location, signal_direction=item_direction, signal_code=item_code)
                        itemRecord.add_signalRecord(signalRecord)
                        itemPresent = True

                    if(item_type == 'NS'):
                        nsRecord = dc.NeutralSectionRecord(ns_location=item_location, ns_direction=item_direction)
                        itemRecord.add_nsRecord(nsRecord)
                        itemPresent = True

                    if(item_type == 'STN'):
                        stationRecord = dc.StationRecord(station_name=item_location, station_direction=item_direction)
                        itemRecord.add_stationRecord(stationRecord)
                        itemPresent = True

            if(itemPresent):
                i += 1
                itemRecord.itemNo = i
                print(str(itemRecord))
                print(itemRecord.itemString() + '\n')
                itemRecords.append(itemRecord)
    
    return itemRecords

def build_sr_records(listChainageRecords, fileName):
    #Read CSV File
    dtype = {'SR From': str, 'SR To': str, 'SR Speed': str, 'SR Type': str}
    data = pd.read_csv(fileName, keep_default_na=False, dtype=dtype)
    
    #Create the lists from corresponding CSV headers
    from_sr_list_csv = data['SR From'].tolist()
    to_sr_list_csv = data['SR To'].tolist()
    sr_list_csv = data['SR Speed'].tolist()
    sr_type_list_csv = data['SR Type'].tolist()

    #Data Initialization
    line_num = 0
    skipped_records = 0
    srRecords = []
    file_records_len = len(from_sr_list_csv)

    for i in range(len(from_sr_list_csv)):
        try:
            print(f'From sr chainage {from_sr_list_csv[i]}')
            from_sr_chainage, isFromFound = find_chainage_km(listChainageRecords, from_sr_list_csv[i].strip())
            to_sr_chainage, isToFound = find_chainage_km(listChainageRecords, to_sr_list_csv[i].strip())
            
            if(isFromFound or isToFound):
                srEntryRecord = None
                if(from_sr_chainage < to_sr_chainage):
                    srEntryRecord = dc.SpeedRestriction(from_sr=from_sr_list_csv[i].strip(), to_sr=to_sr_list_csv[i].strip(), from_sr_chainage=from_sr_chainage, 
                                                        to_sr_chainage=to_sr_chainage, sr_speed=float(sr_list_csv[i].strip()), sr_type=sr_type_list_csv[i].strip())
                else:
                    srEntryRecord = dc.SpeedRestriction(from_sr=to_sr_list_csv[i].strip(), to_sr=from_sr_list_csv[i].strip(), from_sr_chainage=to_sr_chainage, 
                                                        to_sr_chainage=from_sr_chainage, sr_speed=float(sr_list_csv[i].strip()), sr_type=sr_type_list_csv[i].strip())
                srRecords.append(srEntryRecord)
                line_num += 1
            else:
                #print(f'Skipping the row with data {from_sr_list_csv[i]}, {to_sr_list_csv[i]}, {sr_list_csv[i]}, {sr_type_list_csv[i]}')
                skipped_records += 1
        except ValueError:
            #print(f'Skipping the row with data {from_sr_list_csv[i]}, {to_sr_list_csv[i]}, {sr_list_csv[i]}, {sr_type_list_csv[i]}')
            skipped_records += 1
            pass  # Ignore rows with invalid format
    
    #print(f'Total {file_records_len} in file, {line_num} records processed, {skipped_records} records skipped')
    #Return SR Records List
    return sorted(srRecords)
    

#Parser to parse a Mast, Signal Chainage parser
def chainageParser(fileName):
    #Read CSV File
    dtype = {'Km': str, 'Chainage': str, 'Item': str, 'Item Code': str}
    data = pd.read_csv(fileName, keep_default_na=False, dtype=dtype)
    
    #Create the lists from corresponding CSV headers
    km_list_csv = data['Km'].tolist()
    chainage_list_csv = data['Chainage'].tolist()
    item_list_csv = data['Item'].tolist()
    item_code_list_csv = data['Item Code'].tolist()
    item_disp_list_csv = data['Item Disp'].tolist()
    item_type_list_csv = data['Item Type'].tolist()

    #print(item_list_csv)
    #Data Initialization
    line_num = 0
    chainageRecords = []

    file_records_len = len(km_list_csv)
    skipped_records = 0

    # Iterate through each CSV Record
    for i in range(len(km_list_csv)):
        try:
            #Try to parse the first two columns which are expected to be in date and time formats
            km_mast_val = km_list_csv[i].strip()
            km_str = km_mast_val.split('/')[0].strip()
            chainage_str = chainage_list_csv[i].strip()
            item_val = item_list_csv[i].strip()
            item_code_val = item_code_list_csv[i].strip()
            item_disp_val = item_disp_list_csv[i].strip()
            item_type_val = item_type_list_csv[i].strip()

            #Check if KM or Chainage strings are not empty
            if(not(km_str == '' or chainage_str == '')):
                #Km and chainage calculation
                km_val = float(km_str)
                chainage_val = float(chainage_str)
                km_chainage_val = km_val + (chainage_val/1000)
                
                #Create Chainage Entry Record and add to list of records
                chainageEntryRecord = dc.Chainage(mast_km=km_mast_val, km_chainage=km_chainage_val, item=item_val, item_code=item_code_val, item_disp=item_disp_val, item_type=item_type_val)
                chainageRecords.append(chainageEntryRecord)

                #Increment Line Number after successful processing
                line_num += 1

                #Print
                print(str(line_num) + '::' + str(chainageEntryRecord))
            else:
                #print(f'Skipping the row with data {km_list_csv[i]}, {chainage_list_csv[i]}, {item_list_csv[i]}, {item_code_list_csv[i]}')
                skipped_records += 1
        except ValueError:
            #print(f'Skipping the row with data {km_list_csv[i]}, {chainage_list_csv[i]}, {item_list_csv[i]}, {item_code_list_csv[i]}')
            skipped_records += 1
            pass  # Ignore rows with invalid format
    
    #print(f'Total {file_records_len} in file, {line_num} records processed, {skipped_records} records skipped')
    #Return Spm Entries List
    return chainageRecords

def plot_sr_records(axis, plotSrRecords=[], multiplier=1000, trainLength=0):
    srColor = 'tab:red'
    bubbleColor = 'ro'
    for serialNo, srRecord in plotSrRecords:
        to_chainage = srRecord.to_sr_chainage*multiplier + trainLength
        x_vals = [srRecord.from_sr_chainage*multiplier, to_chainage]
        y_vals = [srRecord.sr_speed, srRecord.sr_speed]
        bubble_sizes = [400, 400]

        if(srRecord.sr_type == 'TSR'):
            srColor = 'red'
            bubbleColor = 'red'
        elif(srRecord.sr_type == 'PSR'):
            srColor = 'darkorange'
            bubbleColor = 'darkorange'
        else:
            srColor = 'brown'
            bubbleColor = 'brown'

        axis.plot(x_vals, y_vals, color=srColor)
        axis.plot(x_vals, y_vals, bubbleColor)
        axis.plot(x_vals[0], y_vals[0], 'o', color=bubbleColor, alpha=1)
        axis.plot(x_vals[1], y_vals[1], 'o', color=bubbleColor, alpha=1)
        #axis.scatter()
        #axis.scatter(x_vals, y_vals, s=bubble_sizes, color=bubbleColor, alpha=0.5)
        axis.text(srRecord.from_sr_chainage*multiplier, srRecord.sr_speed, serialNo)

def plot_item_records(axis, plotItemRecords=[], multiplier=1000, y_location=0):
    itemColor = 'green'
    for serialNo, itemRecord in plotItemRecords:
        plt.axvline(itemRecord.km_chainage*multiplier, linestyle='dashed', color=itemColor)
        displayText = itemRecord.item_disp
        if(displayText != None and displayText.strip() != ''):
            axis.text(itemRecord.km_chainage*multiplier, y_location, serialNo + '.' + displayText, fontsize='small', rotation='vertical', color='maroon', fontweight='bold', alpha=0.8)

if __name__ == '__main__':
    chainRecords = chainageParser(fileName='D:/Pydir/Map Files/Mast Signal Chainage.csv')
    output_chainage_csv(chainRecords, fileName='D:/Pydir/Map Files/Mast Signal Chainage Output.csv')

    #323.7, 275.6, 0.0824, -0.0824
    startLoc = '275/22'
    startKm, islocfound = find_chainage_km(chainRecords,startLoc)
    direction = 'DOWN'
    cum_distance = 100

    if(islocfound):
        filteredChainRecs = filter_chainage_records(listChainageRecords=chainRecords, start_mast_km=startLoc, direction=direction, cum_distance=cum_distance)
        srRecords = build_sr_records(filteredChainRecs, 'D:/Pydir/Map Files/SR Map File.csv')
        output_chainage_csv(filteredChainRecs, fileName='D:/Pydir/Map Files/Mast Signal Chainage Filtered Output.csv')
        output_sr_csv(srRecords, fileName='D:/Pydir/Map Files/SR Records Output.csv')

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('Distance (m)')
        ax1.set_ylabel('Speed (kmph)', color=color)
        plot_sr_records(axis=ax1, srRecords=srRecords, multiplier=1000)
        ax1.tick_params(axis='y', labelcolor=color)

        
        gradientRecords = gp.gradientParser("D:/Pydir/Map Files/Gradient.csv", startKm, cum_distance, direction)
        gp.output_gradient_csv('D:/Pydir/Map Files/GradientFiltered.csv',gradientRecords)
        
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel('Gradient (m)', color=color)  # we already handled the x-label with ax1
        gp.plot_gradient(axis=ax2, plotColor=color, multiplier=1000, gradientRecords=gradientRecords)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()

        #output_chainage_csv(filter_mast_locs(chainRecords), fileName='D:/Pydir/Map Files/Mast Signal Chainage Mast Output.csv')
        #output_chainage_csv(filter_item_locs(chainRecords), fileName='D:/Pydir/Map Files/Mast Signal Chainage Item Output.csv')
    