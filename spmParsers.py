import re
import datetime
import pandas as pd
from spmEntry import SpmEntryRecord

def laxvenParser(spmFileName):
    #Static data
    spm_file = open(spmFileName)
    pattern = re.compile('\d\d\/\d\d\/\d\d')
    date_format = '%d/%m/%y %H:%M:%S'

    #Data Initialization
    spm_file_lines = spm_file.readlines()
    line_num = 0
    start_distance = 0
    prev_distance = 0
    spm_cumulative_distance = 0
    spmEntryRecords = []

    #Processing
    for spm_file_line in spm_file_lines:
        line_word_list = spm_file_line.split()
        if(pattern.match(line_word_list[0].strip()) is not None):
            line_num += 1
        
            #Date extraction
            date_string = line_word_list[0].strip() + ' ' + line_word_list[1].strip()
            spm_entry_date = datetime.datetime.strptime(date_string, date_format)
        
            #Distance extraction and calculation
            if(line_num == 1):
                start_distance = float(line_word_list[2])
                prev_distance = start_distance
            
            spm_current_entry_distance = float(line_word_list[2])
            spm_entry_inst_distance = (spm_current_entry_distance - prev_distance) * 1000
            spm_cumulative_distance = (spm_current_entry_distance - start_distance) * 1000
        
            #Speed extraction
            spm_entry_speed = float(line_word_list[3])



            if(len(line_word_list) >= 16):
                try:
                    spm_run_energy = float(line_word_list[9])
                    spm_halt_energy = float(line_word_list[10])
                    spm_total_energy = float(line_word_list[11])
                    spm_current = float(line_word_list[13])
                    spm_voltage = float(line_word_list[14])
                    spm_pf = float(line_word_list[15])
                    spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance, haltEnergy=spm_halt_energy, runEnergy=spm_run_energy, totalEnergy=spm_total_energy, voltage=spm_voltage, current=spm_current, pf=spm_pf)
                except ValueError:
                    spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
            else:
                spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
            
            spmEntryRecords.append(spmEntryRecord)
                
            #Next iteration initialization
            prev_distance = spm_current_entry_distance

            #Print
            #print(str(line_num) + '::' + str(spmEntryRecord))

    #Cleanup
    spm_file.close()
    return spmEntryRecords

def laxvenLTParser(spmFileName):
    #Static data
    spm_file = open(spmFileName)
    pattern = re.compile('\d\d\/\d\d\/\d\d')
    date_format = '%d/%m/%y %H:%M:%S'

    #Data Initialization
    spm_file_lines = spm_file.readlines()
    line_num = 0
    start_distance = 0
    prev_distance = 0
    spm_cumulative_distance = 0
    spmEntryRecords = []

    #Processing
    for spm_file_line in spm_file_lines:
        line_word_list = spm_file_line.split()
        if((len(line_word_list) != 0) and pattern.match(line_word_list[0].strip()) is not None):
            line_num += 1
        
            #Date extraction
            date_string = line_word_list[0].strip() + ' ' + line_word_list[1].strip()
            spm_entry_date = datetime.datetime.strptime(date_string, date_format)
        
            #Distance extraction and calculation
            if(line_num == 1):
                start_distance = float(line_word_list[2])
                prev_distance = start_distance
            
            spm_current_entry_distance = float(line_word_list[2])
            spm_entry_inst_distance = (spm_current_entry_distance - prev_distance) * 1000
            spm_cumulative_distance = (spm_current_entry_distance - start_distance) * 1000
        
            #Speed extraction
            spm_entry_speed = float(line_word_list[3])

            #Create SpmEntryRecord and add to list of records
            spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
            spmEntryRecords.append(spmEntryRecord)
                
            #Next iteration initialization
            prev_distance = spm_current_entry_distance

            #Print
            #print(str(line_num) + '::' + str(spmEntryRecord))

    #Cleanup
    spm_file.close()
    return spmEntryRecords

def rtisParser(fileName):
        # Read the Excel file
    df = pd.read_excel(fileName)

    #Data Initialization
    date_format = '%d-%m-%Y %H:%M:%S'
    line_num = 0
    start_distance = 0
    prev_distance = 0
    spm_cumulative_distance = 0
    spmEntryRecords = []

    # Iterate through each row
    for index, row in df.iterrows():
        # Check if the first column is in date format
        try:
            print(str(row[0]).strip() +',' + str(row[1]).strip() + ',' + str(row[3]).strip())
            spm_entry_date = datetime.datetime.strptime(str(row[0]).strip(), date_format)
            
            line_num += 1

            #Distance extraction and calculation
            if(line_num == 1):
                start_distance = float(str(row[3]).strip())
                prev_distance = start_distance
            
            spm_current_entry_distance = float(str(row[3]).strip())
            spm_entry_inst_distance = (spm_current_entry_distance - prev_distance) * 1000
            spm_cumulative_distance = (spm_current_entry_distance - start_distance) * 1000
        
            #Speed extraction
            spm_entry_speed = float(str(row[1]).strip())

            #Create SpmEntryRecord and add to list of records
            spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
            spmEntryRecords.append(spmEntryRecord)
                
            #Next iteration initialization
            prev_distance = spm_current_entry_distance

            #Print
            #print(str(line_num) + '::' + str(spmEntryRecord))
        except ValueError:
            pass  # Ignore rows with invalid date format

    #Return Spm Entries List
    return spmEntryRecords

def medhaParser(spmFileName):
    #Static data
    spm_file = open(spmFileName)
    pattern = re.compile('\d\d\/\d\d\/\d\d')
    date_format = '%d/%m/%y %H:%M:%S'

    #Data Initialization
    spm_file_lines = spm_file.readlines()
    line_num = 0
    spm_cumulative_distance = 0
    spmEntryRecords = []

    #Processing
    for spm_file_line in spm_file_lines:
        line_word_list = spm_file_line.split('|')
        if(pattern.match(line_word_list[0].strip()) is not None):
            line_num += 1
        
            #Date extraction
            date_string = line_word_list[0].strip() + ' ' + line_word_list[1].strip()
            spm_entry_date = datetime.datetime.strptime(date_string, date_format)
            
            #Speed extraction
            spm_entry_speed = float(line_word_list[2])
            
            #Distance extraction and calculation            
            spm_entry_inst_distance = float(line_word_list[3])
            spm_cumulative_distance += spm_entry_inst_distance
            #print(line_word_list)
            if(len(line_word_list) == 14):
                try:
                    #print(f'Line Word List: Voltage-{spm_voltage}, Current-{spm_current}, Pf-{spm_pf}, Run Energy-{spm_run_energy}, Halt Energy-{spm_halt_energy}, Total Energy-{spm_total_energy}')
                    spm_voltage = float(line_word_list[7].strip())
                    spm_current = float(line_word_list[8].strip())
                    spm_pf = float(line_word_list[9].strip())
                    spm_run_energy = float(line_word_list[10].strip())
                    spm_halt_energy = float(line_word_list[11].strip())
                    spm_total_energy = float(line_word_list[12].strip())
                    spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance, haltEnergy=spm_halt_energy, runEnergy=spm_run_energy, totalEnergy=spm_total_energy, voltage=spm_voltage, current=spm_current, pf=spm_pf)
                except ValueError:
                    print('Error in float conversion')
                    spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
            elif(len(line_word_list) == 13):
                try:
                    #print(f'Line Word List: Voltage-{spm_voltage}, Current-{spm_current}, Pf-{spm_pf}, Run Energy-{spm_run_energy}, Halt Energy-{spm_halt_energy}, Total Energy-{spm_total_energy}')
                    spm_voltage = float(line_word_list[7].strip())
                    spm_current = float(line_word_list[8].strip())
                    spm_run_energy = float(line_word_list[9].strip())
                    spm_halt_energy = float(line_word_list[10].strip())
                    spm_total_energy = float(line_word_list[11].strip())
                    spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance, haltEnergy=spm_halt_energy, runEnergy=spm_run_energy, totalEnergy=spm_total_energy, voltage=spm_voltage, current=spm_current)
                except ValueError:
                    print('Error in float conversion')
                    spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
            else:
                spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
            
            spmEntryRecords.append(spmEntryRecord)
            
            #Print
            #print(str(line_num) + '::' + str(spmEntryRecord))

    #Cleanup
    spm_file.close()

    #Return Spm Entries List
    return spmEntryRecords

def dslDemuParser(fileName):
    # Read the Excel file
    df = pd.read_excel(fileName)

    #Data Initialization
    date_format = '%d/%m/%y %H:%M:%S'
    line_num = 0
    spm_cumulative_distance = 0
    spmEntryRecords = []

    # Iterate through each row
    for index, row in df.iterrows():
        # Check if the first column is in date format
        try:
            date = datetime.datetime.strptime(str(row[0]).strip(), '%d/%m/%y')
            
            line_num += 1
        
            #Date extraction
            date_string = str(row[0]).strip() + ' ' + str(row[1]).strip()
            spm_entry_date = datetime.datetime.strptime(date_string, date_format)
            
            #Speed extraction
            spm_entry_speed = float(str(row[5]).strip())
            
            #Distance extraction and calculation            
            spm_entry_inst_distance = float(str(row[4]).strip())
            spm_cumulative_distance += spm_entry_inst_distance
            
            #Create SpmEntryRecord and add to list of records
            spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
            spmEntryRecords.append(spmEntryRecord)
            
            #Print
            #print(str(line_num) + '::' + str(spmEntryRecord))
        except ValueError:
            pass  # Ignore rows with invalid date format

    #Return Spm Entries List
    return spmEntryRecords

def aalParser(fileName):
    # Read the Excel file
    df = pd.read_excel(fileName)

    #Data Initialization
    date_format = '%d/%m/%Y %H:%M:%S'
    line_num = 0
    spm_cumulative_distance = 0
    spmEntryRecords = []

    # Iterate through each row
    for index, row in df.iterrows():
        # Check if the first column is in date format
        try:
            date = datetime.datetime.strptime(str(row[0]).strip(), '%d/%m/%Y')
            
            line_num += 1
        
            #Date extraction
            date_string = str(row[0]).strip() + ' ' + str(row[1]).strip()
            spm_entry_date = datetime.datetime.strptime(date_string, date_format)
            spm_entry_speed_text = str(row[3]).strip()
            spm_entry_inst_dist_text = str(row[2]).strip()

            if(not (spm_entry_speed_text=='' or spm_entry_speed_text=='nan' or spm_entry_inst_dist_text=='' or spm_entry_inst_dist_text=='nan')):
                #Speed extraction
                spm_entry_speed = float(spm_entry_speed_text)
                
                #Distance extraction and calculation            
                spm_entry_inst_distance = float(spm_entry_inst_dist_text)
                spm_cumulative_distance += spm_entry_inst_distance
                
                #Create SpmEntryRecord and add to list of records
                spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
                spmEntryRecords.append(spmEntryRecord)
                
                #Print
                #print(str(line_num) + '::' + str(spmEntryRecord))
        except ValueError:
            pass  # Ignore rows with invalid date format

    #Return Spm Entries List
    return spmEntryRecords

def aalCsvParser(spmFileName):
    #Static data
    spm_file = open(spmFileName)
    pattern = re.compile('\d\d\/\d\d\/\d\d\d\d')
    date_format = '%d/%m/%Y %H:%M:%S'

    #Data Initialization
    spm_file_lines = spm_file.readlines()
    line_num = 0
    spm_record_num = 0
    date_line_num = 0
    spm_cumulative_distance = 0
    spmEntryRecords = []

    is_date_read = False
    spm_entry_date = None
    
    for spm_file_line in spm_file_lines:
        line_word_list = spm_file_line.split(',')
        line_num += 1

        if(not is_date_read):
            if(pattern.match(line_word_list[0].strip()) is not None):
                date_string = line_word_list[0].strip() + ' ' + line_word_list[5].strip()
                spm_entry_date = datetime.datetime.strptime(date_string, date_format)
                spm_record_num += 1
                date_line_num = line_num
                is_date_read = True

        if(is_date_read):
            try:
                spm_entry_inst_distance = float(line_word_list[11].strip())
                spm_entry_speed = float(line_word_list[17].strip())            
                spm_cumulative_distance += spm_entry_inst_distance
                spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
                spmEntryRecords.append(spmEntryRecord)
            
                #print(str(spm_record_num) + '::' + str(spmEntryRecord))
                is_date_read = False
            except ValueError:
                if (line_num - date_line_num == 2):
                    #print(f'Record number {spm_record_num} default values assigned')
                    spm_entry_speed = 0.0          
                    spm_entry_inst_distance = 0.0
                    spm_cumulative_distance += spm_entry_inst_distance
                    spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
                    spmEntryRecords.append(spmEntryRecord)
                
                    #print(str(spm_record_num) + '::' + str(spmEntryRecord))
                    is_date_read = False
    
    #Cleanup
    spm_file.close()

    #Return Spm Entries List
    return spmEntryRecords

def remlotParser(fileName):
    # Read the Excel file
    df = pd.read_excel(fileName)

    #Data Initialization
    date_format = '%d/%m/%Y %H:%M:%S'
    line_num = 0
    spmEntryRecords = []

    # Iterate through each row
    for index, row in df.iterrows():
        # Check if the first column is in date format
        try:
            date = datetime.datetime.strptime(str(row[0]).strip(), date_format)
            
            line_num += 1
        
            #Data Extraction
            spm_entry_date = datetime.datetime.strptime(str(row[0]).strip(), date_format)
            spm_entry_speed_text = str(row[1]).strip()
            spm_entry_inst_dist_text = str(row[2]).strip()

            if(not (spm_entry_speed_text=='' or spm_entry_speed_text=='nan' or spm_entry_inst_dist_text=='' or spm_entry_inst_dist_text=='nan')):
                #Speed extraction
                spm_entry_speed = float(spm_entry_speed_text)
                
                #Distance extraction and calculation            
                spm_entry_inst_distance = float(spm_entry_inst_dist_text)
                
                #Create SpmEntryRecord and add to list of records
                spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance)
                spmEntryRecords.append(spmEntryRecord)
                
                #Print
                #print(str(line_num) + '::' + str(spmEntryRecord))
        except ValueError:
            pass  # Ignore rows with invalid date format

    #Return Spm Entries List
    spmEntryListSorted = sorted(spmEntryRecords)
    spm_cumulative_distance = 0
    for spmEntry in spmEntryListSorted:
        spm_cumulative_distance += spmEntry.entryInstDist
        spmEntry.entryCumDist = spm_cumulative_distance

    return spmEntryListSorted

def medhaSSParser(fileName):
    # Read the Excel file
    df = pd.read_excel(fileName)

    #Data Initialization
    date_format = '%d/%m/%y %H:%M:%S'
    line_num = 0
    spm_cumulative_distance = 0
    spmEntryRecords = []

    # Iterate through each row
    for index, row in df.iterrows():
        # Check if the first column is in date format
        try:
            date = datetime.datetime.strptime(str(row[0]).strip(), '%d/%m/%y')
            
            line_num += 1
        
            #Date extraction
            date_string = str(row[0]).strip() + ' ' + str(row[1]).strip()
            spm_entry_date = datetime.datetime.strptime(date_string, date_format)
            spm_entry_speed_text = str(row[2]).strip()
            spm_entry_inst_dist_text = str(row[3]).strip()

            if(not (spm_entry_speed_text=='' or spm_entry_speed_text=='nan' or spm_entry_inst_dist_text=='' or spm_entry_inst_dist_text=='nan')):
                #Speed extraction
                spm_entry_speed = float(spm_entry_speed_text)
                
                #Distance extraction and calculation            
                spm_entry_inst_distance = float(spm_entry_inst_dist_text)
                spm_cumulative_distance += spm_entry_inst_distance
                
                #Create SpmEntryRecord and add to list of records
                spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
                spmEntryRecords.append(spmEntryRecord)
                
                #Print
                #print(str(line_num) + '::' + str(spmEntryRecord))
        except ValueError:
            pass  # Ignore rows with invalid date format

    #Return Spm Entries List
    return spmEntryRecords

#Parser to parse a CSV File in format Date, Time, Speed, Distance
def csvParser(fileName):
    #Read CSV File
    data = pd.read_csv(fileName)
    
    #Create the lists from corresponding CSV headers
    date_list_csv = data['Date'].tolist()
    time_list_csv = data['Time'].tolist()
    speed_list_csv = data['Speed'].tolist()
    distance_list_csv = data['Distance'].tolist()

    #Data Initialization
    date_format = '%d-%m-%Y %H:%M:%S'
    line_num = 0
    spm_cumulative_distance = 0
    spmEntryRecords = []
    print(f'CSV Parser length of records is {len(date_list_csv)}')
    # Iterate through each CSV Record
    for i in range(len(date_list_csv)):
        try:
            #Try to parse the first two columns which are expected to be in date and time formats
            date_string = str(date_list_csv[i]).strip() + ' ' + str(time_list_csv[i]).strip()
            spm_entry_date = datetime.datetime.strptime(date_string, date_format)

            #Extract Speed and Instantaneous distances
            spm_entry_speed_text = str(speed_list_csv[i]).strip()
            spm_entry_inst_dist_text = str(distance_list_csv[i]).strip()

            #Check if the speed and instantaneous distances are not empty or not numbers
            if(not (spm_entry_speed_text=='' or spm_entry_speed_text=='nan' or spm_entry_inst_dist_text=='' or spm_entry_inst_dist_text=='nan')):
                #Speed conversion to float
                spm_entry_speed = float(spm_entry_speed_text)
                
                #Instantaneous distance conversion to float and Cumulative Distance Calculation            
                spm_entry_inst_distance = float(spm_entry_inst_dist_text)
                spm_cumulative_distance += spm_entry_inst_distance
                
                #Create SpmEntryRecord and add to list of records
                spmEntryRecord = SpmEntryRecord(entryDate=spm_entry_date, entrySpeed=spm_entry_speed, entryInstDist=spm_entry_inst_distance, entryCumDist=spm_cumulative_distance)
                spmEntryRecords.append(spmEntryRecord)
                
                #Increment Line Number after successful processing
                line_num += 1

                #Print
                #print(str(line_num) + '::' + str(spmEntryRecord))
        except ValueError:
            pass  # Ignore rows with invalid date format

    #Return Spm Entries List
    print(f'SPM Records {len(spmEntryRecords)} processed.')
    return spmEntryRecords

#Function to output CSV File from list of SPM Entry Records
def outputCsv(listSpmEntryRecords, fileName):
    #Open the passed Filename
    out_file = open(fileName, 'w')

    #Define CSV header and data initialization
    csv_header = 'Date,Time,Speed,Distance,Cum_Distance,Voltage,Current,Pf,Halt Energy,Run Energy,Total Energy\n'
    out_lines = []
    out_lines.append(csv_header)

    #Iterate through the list of SPM Records
    for spmEntryRecord in listSpmEntryRecords:
        #Format the SPM Record as a CSV record and append to list of output lines
        out_line = spmEntryRecord.entryDate.strftime('%d-%m-%y') + ',' + spmEntryRecord.entryDate.strftime('%H:%M:%S') + ',' + str(spmEntryRecord.entrySpeed) + ',' + str(round(spmEntryRecord.entryInstDist,2)) + ',' + str(round(spmEntryRecord.entryCumDist,2)) + ',' + str(round(spmEntryRecord.voltage,2)) + ',' + str(round(spmEntryRecord.current,2)) + ',' + str(round(spmEntryRecord.pf,2)) + ',' + str(round(spmEntryRecord.haltEnergy,2)) + ',' + str(round(spmEntryRecord.runEnergy,2)) + ',' + str(round(spmEntryRecord.totalEnergy,2)) + '\n'
        out_lines.append(out_line)
    
    #Write Output to file and close
    out_file.writelines(out_lines)
    out_file.close()

if __name__=='__main__':
    spmEntryRecordsList = aalCsvParser('D:/Pydir/aalSt.csv')
    outputCsv(spmEntryRecordsList, 'D:/Pydir/outputAalSt.csv')
    print(len(spmEntryRecordsList))