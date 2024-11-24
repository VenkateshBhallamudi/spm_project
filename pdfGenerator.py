import pdfDataClasses as pd
import spmAnalysis as sa
import numpy as np
import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image

def generateSpmSummaryReport(spmInfoData=None, spmInputData=None):
    generatedDate = datetime.datetime.now().strftime('%d.%m.%Y')
    headingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=12, align='L',textColor=(0,0,0), fillColor=(200,220,255), drawColor=(0,80,180),border=False,height=10)
    bodyStyle = pd.PdfStyle(font='helvetica', fontStyle='', fontSize=10, align='L',textColor=(0,0,0), fillColor=(224, 235, 255), drawColor=(255, 0, 0),border=False,height=10)
    endingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=8, align='C',textColor=(0,0,0), fillColor=(255,255,255), drawColor=(255,255,255),border=False,height=6)         
    summaryPage = pd.PdfSummaryPage(headingText=f'SPM Report by {spmInfoData.analysisBy} on {generatedDate}',headingStyle=headingStyle, endingText='***', endingStyle=endingStyle, bodyStyle=bodyStyle)
    infoFields = ['LP Name', 'LP Designation', 'LP HQ', 'LP PF No', 'LP CMS ID', 'ALP Name', 'ALP HQ', 'ALP CMS ID', 'LP CLI', 'CLI Pf No', 
         'From Station', 'Start Location (km)', 'To Station', 'End Location (km)', 'Section', 'Direction', 'Train', 'Train Length (m)', 'Service', 'No of Coaches/Wagons', 'Coach/Wagon Type', 'Total Load(incl Engine) (T)', 'Loaded/Empty', 
         'Loco No', 'Loco Type', 'Loco Base', 'Loco Schedule Due Date', 'Loco Schedule Due', 'Trip Date', 'MPS (kmph)', 'MPS Range From (kmph)', 'MPS Range To (kmph)', 'Attacking Speed (kmph)', 'SPM GPS Time Difference \n+/-hh:mm:ss', 'SPM Type', 'Remarks']
    
    infoValues = [spmInfoData.lpName,spmInfoData.lpDesg,spmInfoData.lpHq,spmInfoData.lpPfNo,spmInfoData.lpCmsId,spmInfoData.alpName,spmInfoData.alpHq,
                  spmInfoData.alpCmsId, spmInfoData.lpCli, spmInfoData.cliPfNo, spmInfoData.fromStn, spmInfoData.startLoc, spmInfoData.toStn, spmInfoData.endLoc,
                  spmInfoData.section, spmInfoData.direction, spmInfoData.train, spmInfoData.trainLength, spmInfoData.service, spmInfoData.noCw, spmInfoData.coachWagonType, spmInfoData.load, spmInfoData.loadedEmpty,
                  spmInfoData.locoNo, spmInfoData.locoType, spmInfoData.locoBase, spmInfoData.locoDueDate, spmInfoData.locoScheduleDue, spmInfoData.tripDate, spmInfoData.mps, 
                  spmInfoData.speedFrom, spmInfoData.speedTo, spmInfoData.attackSpeed, spmInfoData.spmTimeDiff, spmInputData.spmType, spmInfoData.remarks]
    
    for i, infoField in enumerate(infoFields):
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord(infoField, infoValues[i]))

    return summaryPage

def generateAnalysisSummaryReport(spmInfoData=None, date_time_vals=[], speed_vals=[], inst_dist_vals=[], cum_dist_vals=[], bftBptList=[],zeroClusters=[], current_vals=[], voltage_vals=[], haltEnergy_vals=[], runEnergy_vals=[], totalEnergy_vals=[], toShowBft=True, toShowBpt=True, showOverControl=True, showSpeedCompile=True):
    headingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=12, align='L',textColor=(0,0,0), fillColor=(200,220,255), drawColor=(0,80,180),border=False,height=10)
    bodyStyle = pd.PdfStyle(font='helvetica', fontStyle='', fontSize=10, align='L',textColor=(0,0,0), fillColor=(224, 235, 255), drawColor=(255, 0, 0),border=False,height=10)
    endingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=8, align='C',textColor=(0,0,0), fillColor=(255,255,255), drawColor=(255,255,255),border=False,height=6)         

    summaryPage = pd.PdfSummaryPage(headingText='Analysis Summary Report',headingStyle=headingStyle, endingText='***End of Analysis Summary Report***', endingStyle=endingStyle, bodyStyle=bodyStyle)

    generateAnalysisSummaryRecords(summaryPage, spmInfoData, date_time_vals, speed_vals, inst_dist_vals, cum_dist_vals, bftBptList, zeroClusters, spmInfoData.service, current_vals, voltage_vals, haltEnergy_vals, runEnergy_vals, totalEnergy_vals, toShowBft, toShowBpt, showOverControl, showSpeedCompile)
    return summaryPage

def generateSpmInfoSummaryRecord(infoField, infoValue, recordStyle=pd.PdfStyle(fontStyle='',textColor=(0,0,0), fillColor=(224, 235, 255))):
    spmInfoSummaryTuple = (infoField, infoValue)
    summaryRecord = pd.PdfSummaryRecord(spmInfoSummaryTuple, recordStyle)
    return summaryRecord

def generateAnalysisSummaryRecords(summaryPage, spmInfoData, date_time_vals, speed_vals, inst_dist_vals, cum_dist_vals, bftBptList, zeroClusters, service, current_vals, voltage_vals, haltEnergy_vals, runEnergy_vals, totalEnergy_vals, toShowBft, toShowBpt, showOverControl, showSpeedCompile):
    summaryRecordStyleRight = pd.PdfStyle(fontStyle='',textColor=(0,0,0), fillColor=(224, 235, 255))
    summaryRecordStyleWrong = pd.PdfStyle(fontStyle='BI', textColor=(255,0,0), fillColor=(255, 255, 0))
    recordStyle = summaryRecordStyleWrong

    #Start and Ending Date Time
    success, start_date_time, end_date_time = sa.spm_start_end_datetime(date_time_vals)
    recordStyle= summaryRecordStyleRight if success else summaryRecordStyleWrong
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('SPM Start Date Time', start_date_time, recordStyle))
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('SPM End Date Time', end_date_time, recordStyle))

    #Duration
    success, total_time_duration = sa.total_time_duration(date_time_vals)
    recordStyle= summaryRecordStyleRight if success else summaryRecordStyleWrong
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('SPM Time Duration', total_time_duration, recordStyle))

    #Average Speed
    success, average_speed = sa.average_speed(date_time_vals, cum_dist_vals)
    recordStyle= summaryRecordStyleRight if success else summaryRecordStyleWrong
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Average Speed (kmph)', average_speed, recordStyle))

    #Running Duration
    success, running_duration = sa.running_time_duration(date_time_vals, speed_vals)
    recordStyle= summaryRecordStyleRight if success else summaryRecordStyleWrong
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Running Time Duration', running_duration, recordStyle))

    #Dynamic Speed
    success, dynamic_speed = sa.dynamic_speed(date_time_vals, cum_dist_vals, speed_vals)
    recordStyle= summaryRecordStyleRight if success else summaryRecordStyleWrong
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Dynamic Speed (kmph)', dynamic_speed, recordStyle))

    #Poor Running
    dynamic_percent_str = ''
    poor_running_str = ''
    if success:
        flag = False
        dynamic_speed = float(dynamic_speed)
        if(spmInfoData.mps != None and spmInfoData.mps != ''):
            try:
                mps_val = float(spmInfoData.mps)
                dynamic_percent = (dynamic_speed/mps_val)*100
                flag = True
            except BaseException as error:
                flag = False
        else:
            flag = False
    else:
        flag = False

    if(flag):
        dynamic_percent_str = str(round(dynamic_percent,2))
        if(dynamic_percent > 50):
            recordStyle= summaryRecordStyleRight
            poor_running_str = 'NO'
        else:
            recordStyle= summaryRecordStyleWrong
            poor_running_str = 'YES'

    else:
        dynamic_percent_str = 'NA'
        poor_running_str = 'NA'
        recordStyle= summaryRecordStyleWrong

    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Dynamic Speed/MPS %', dynamic_percent_str, recordStyle))
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Poor Running', poor_running_str, recordStyle))

    #Idle Duration and Percent
    idleSuccess, idle_time_duration = sa.idle_time_duration(date_time_vals, speed_vals)
    idlePerSuccess, idle_time_percent = sa.idle_time_percent(date_time_vals, speed_vals)
    notHighIdle = True

    if(idlePerSuccess):
        idle_time_per_val = float(idle_time_percent)
        if(idle_time_per_val >= 40):
            notHighIdle = False

    idleRecordStyle = summaryRecordStyleRight if idleSuccess and notHighIdle else summaryRecordStyleWrong
    idlePerRecordStyle= summaryRecordStyleRight if idlePerSuccess and notHighIdle else summaryRecordStyleWrong

    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Idle Duration', idle_time_duration, idleRecordStyle))
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Idle Percentage (%)', idle_time_percent, idlePerRecordStyle))

    #MPS Attained
    success, mps_attained = sa.mps_attained(speed_vals)
    recordStyle= summaryRecordStyleRight if success else summaryRecordStyleWrong
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('MPS Attained (kmph)', mps_attained, recordStyle))

    #Overspeeding
    success, over_speed = sa.is_over_speed(speed_vals, spmInfoData.mps)
    recordStyle= summaryRecordStyleRight if success else summaryRecordStyleWrong
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Over speeding', over_speed, recordStyle))

    #Total Distance
    total_distance_success, total_distance = sa.compute_total_distance(cum_dist_vals)
    recordStyle= summaryRecordStyleRight if total_distance_success else summaryRecordStyleWrong
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Total Distance (Km)', total_distance, recordStyle))

    #Near MPS Distance
    near_mps_distance_success, from_default, to_default,from_mps_val,to_mps_val, mps_distance = sa.compute_mps_distance(spmInfoData.mps, spmInfoData.speedFrom, spmInfoData.speedTo, inst_dist_vals, speed_vals)
    near_mps_str = 'Near MPS Distance (Km)'
    recordStyle= summaryRecordStyleRight if near_mps_distance_success else summaryRecordStyleWrong
    if(near_mps_distance_success):
        from_str = f'From:{str(from_mps_val)} kmph (.95*MPS)' if from_default else f'From:{str(from_mps_val)} kmph (Entered)'
        to_str = f'To:{str(to_mps_val)} kmph (1.05*MPS)' if to_default else f'To:{str(to_mps_val)} kmph (Entered)'
        near_mps_str = f'{near_mps_str}\n{from_str}\n{to_str}'

    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord(near_mps_str, mps_distance, recordStyle))

    #Near MPS Distance %
    if(total_distance_success and near_mps_distance_success):
        recordStyle = summaryRecordStyleRight
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Near MPS Distance %', str(round((float(mps_distance)/float(total_distance))*100, 2)), recordStyle))
    else:
        recordStyle = summaryRecordStyleWrong
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Near MPS Distance %', 'NA', recordStyle))

    #Excess MPS Distance, Time
    success, mps_excess_seconds, mps_excess_distance = sa.compute_excess_mps_distance(spmInfoData.mps, inst_dist_vals, speed_vals, date_time_vals)
    if(success):
        recordStyle= summaryRecordStyleWrong if mps_excess_distance > 0 else summaryRecordStyleRight
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Excess MPS distance (m)', str(round(mps_excess_distance,2)), recordStyle))
        recordStyle= summaryRecordStyleWrong if mps_excess_seconds > 0 else summaryRecordStyleRight
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Excess MPS Time (sec)', str(mps_excess_seconds), recordStyle))
    else:
        recordStyle= summaryRecordStyleWrong
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Excess MPS distance (m)', mps_excess_distance, recordStyle))
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Excess MPS Time (sec)', mps_excess_seconds, recordStyle))

    if(toShowBft):
        #BFT BPT
        bft_start_index = bftBptList[0]
        bft_end_index = bftBptList[1]
        bftProperImproper = 'PROPER'
        bftRecordStyle = summaryRecordStyleRight
        
        if(bft_start_index != -1 and bft_end_index != -1):
            bft_start_distance = str(round(cum_dist_vals[bft_start_index], 2))
            bft_end_distance = str(round(cum_dist_vals[bft_end_index], 2))
            bft_start_time = date_time_vals[bft_start_index].strftime('%d-%m-%y %H:%M:%S')
            bft_end_time = date_time_vals[bft_end_index].strftime('%d-%m-%y %H:%M:%S')
            total_seconds = (date_time_vals[bft_end_index] - date_time_vals[bft_start_index]).total_seconds()
            bft_duration = str(datetime.timedelta(seconds=total_seconds))
            bft_start_speed = str(round(speed_vals[bft_start_index],2))
            bft_end_speed = str(round(speed_vals[bft_end_index],2))
            bft_speed_reduction = str(round(((speed_vals[bft_start_index]-speed_vals[bft_end_index])/speed_vals[bft_start_index])*100,2))
            
            if service == 'GOODS':
                if(speed_vals[bft_start_index] <= 15 and speed_vals[bft_start_index] >= 10 and speed_vals[bft_end_index] <= 10 and speed_vals[bft_end_index] >= 0):
                    bftProperImproper = 'PROPER'
                else:
                    bftProperImproper = 'IMPROPER'
            else:
                if(speed_vals[bft_start_index] <= 15 and speed_vals[bft_start_index] >= 10 and speed_vals[bft_end_index] <= 10 and speed_vals[bft_end_index] >= 5):
                    bftProperImproper = 'PROPER'
                else:
                    bftProperImproper = 'IMPROPER'
        else:
            bft_start_distance, bft_end_distance, bft_start_time, bft_end_time, bft_start_speed, bft_end_speed, bft_duration, bft_speed_reduction  = ('NA','NA','NA','NA','NA','NA', 'NA', 'NA')
            bftProperImproper= 'NA'
        
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BFT start time', bft_start_time, bftRecordStyle))
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BFT end time', bft_end_time, bftRecordStyle))
        #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BFT duration', bft_duration, bftRecordStyle))
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BFT start speed (kmph)', bft_start_speed, bftRecordStyle))
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BFT end speed (kmph)', bft_end_speed, bftRecordStyle))
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BFT speed reduction %', bft_speed_reduction, bftRecordStyle))
        #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BFT start distance (m)', bft_start_distance, bftRecordStyle))
        #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BFT end distance (m)', bft_end_distance, bftRecordStyle))
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BFT Proper/Improper', bftProperImproper, bftRecordStyle))

    if(toShowBpt):
        bpt_start_index = bftBptList[2]
        bpt_end_index = bftBptList[3]
        bptProperImproper = 'PROPER'
        bptRecordStyle = summaryRecordStyleRight
        if(bpt_start_index != -1 and bpt_end_index != -1):
            bpt_start_distance = str(round(cum_dist_vals[bpt_start_index],2))
            bpt_end_distance = str(round(cum_dist_vals[bpt_end_index],2))
            bpt_start_time = date_time_vals[bpt_start_index].strftime('%d-%m-%y %H:%M:%S')
            bpt_end_time = date_time_vals[bpt_end_index].strftime('%d-%m-%y %H:%M:%S')
            total_seconds = (date_time_vals[bpt_end_index] - date_time_vals[bpt_start_index]).total_seconds()
            bpt_duration = str(datetime.timedelta(seconds=total_seconds))
            bpt_start_speed = str(round(speed_vals[bpt_start_index],2))
            bpt_end_speed = str(round(speed_vals[bpt_end_index],2))
            bpt_speed_reduction = str(round(((speed_vals[bpt_start_index]-speed_vals[bpt_end_index])/speed_vals[bpt_start_index])*100,2))
            if service == 'GOODS':
                if(speed_vals[bpt_start_index] <= 50 and speed_vals[bpt_start_index] >= 40 and speed_vals[bpt_end_index] <= 30 and speed_vals[bpt_end_index] >= 0):
                    bptProperImproper = 'PROPER'
                else:
                    bptProperImproper = 'IMPROPER'
            else:
                if(speed_vals[bpt_start_index] <= 70 and speed_vals[bpt_start_index] >= 60 and speed_vals[bpt_end_index] <= 40 and speed_vals[bpt_end_index] >= 20):
                    bptProperImproper = 'PROPER'
                else:
                    bptProperImproper = 'IMPROPER'
        else:
            bpt_start_distance, bpt_end_distance, bpt_start_time, bpt_end_time, bpt_start_speed, bpt_end_speed, bpt_duration, bpt_speed_reduction = ('NA','NA','NA','NA','NA','NA','NA','NA')
            bptProperImproper= 'NA'

        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BPT start time', bpt_start_time, bptRecordStyle))
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BPT end time', bpt_end_time, bptRecordStyle))
        #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BPT duration', bpt_duration, bptRecordStyle))
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BPT start speed (kmph)', bpt_start_speed, bptRecordStyle))
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BPT end speed (kmph)', bpt_end_speed, bptRecordStyle))
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BPT speed reduction %', bpt_speed_reduction, bptRecordStyle))
        #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BPT start distance (m)', bpt_start_distance, bptRecordStyle))
        #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BPT end distance (m)', bpt_end_distance, bptRecordStyle))
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('BPT Proper/Improper', bptProperImproper, bptRecordStyle))
    
    lateControlling = sa.late_controlling(zeroClusters=zeroClusters,speed_vals=speed_vals, cum_dist_vals=cum_dist_vals, service=service)
    recordStyle= summaryRecordStyleWrong if lateControlling else summaryRecordStyleRight
    lateControlling = 'YES' if lateControlling else 'NO'
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Late Controlling', lateControlling, recordStyle))

    if(showOverControl):
        overControlling = sa.over_controlling(zeroClusters=zeroClusters,speed_vals=speed_vals, cum_dist_vals=cum_dist_vals, service=service)
        recordStyle= summaryRecordStyleWrong if overControlling else summaryRecordStyleRight
        overControlling_str = 'YES' if overControlling else 'NO'
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Over Controlling', overControlling_str, recordStyle))
    
    abruptBraking = sa.abrupt_braking(zeroClusters=zeroClusters,speed_vals=speed_vals, cum_dist_vals=cum_dist_vals)
    recordStyle= summaryRecordStyleWrong if abruptBraking else summaryRecordStyleRight
    abruptBraking_str = 'YES' if abruptBraking else 'NO'
    summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Abrupt Braking', abruptBraking_str, recordStyle))

    if(showSpeedCompile):
        speedComplied = sa.speed_complied(zeroClusters=zeroClusters,speed_vals=speed_vals, cum_dist_vals=cum_dist_vals)
        recordStyle= summaryRecordStyleRight if speedComplied else summaryRecordStyleWrong
        speedComplied_str = 'YES' if speedComplied else 'NO'
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Speed Complied before Stop', speedComplied_str, recordStyle))

    recordStyle = summaryRecordStyleRight
    isCurrentPresent = sa.isCurrentPresent(current_vals)
    averageCurrent = 'NA'
    maxCurrent = 'NA'
    minCurrent = 'NA'

    if(isCurrentPresent):
        averageCurrent = sa.avg_current(current_vals)
        maxCurrent = sa.max_current(current_vals)
        minCurrent = sa.min_current(current_vals)
    
    #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Average Current (A)', averageCurrent, recordStyle))
    #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Max Current (A)', maxCurrent, recordStyle))
    #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Min Current (A)', minCurrent, recordStyle))

    isVoltagePresent = sa.isVoltagePresent(voltage_vals)
    averageVoltage = 'NA'
    maxVoltage = 'NA'
    minVoltage = 'NA'

    if(isVoltagePresent):
        averageVoltage = sa.avg_voltage(voltage_vals)
        maxVoltage = sa.max_voltage(voltage_vals)
        minVoltage = sa.min_voltage(voltage_vals)

    #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Average Voltage (kV)', averageVoltage, recordStyle))
    #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Max Voltage (kV)', maxVoltage, recordStyle))
    #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Min Voltage (kV)', minVoltage, recordStyle))

    haltEnergy, isHaltEnergyPresent = sa.cum_halt_energy(haltEnergy_vals)
    haltEnergy_str = str(round(haltEnergy, 2)) if isHaltEnergyPresent else 'NA'
    #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Halt Energy (kWh)', haltEnergy_str, recordStyle))

    runEnergy, isRunEnergyPresent = sa.cum_run_energy(runEnergy_vals)
    runEnergy_str = str(round(runEnergy, 2)) if isRunEnergyPresent else 'NA'
    #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Run Energy (kWh)', runEnergy_str, recordStyle))

    total_energy, isTotalEnergyPresent = sa.cum_total_energy(totalEnergy_vals)
    total_energy_str = str(round(total_energy, 2)) if isTotalEnergyPresent else 'NA'
    #summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Total Energy (kWh)', total_energy_str, recordStyle))

    sec = 'NA'
    if(isTotalEnergyPresent):
        cum_distance_km = cum_dist_vals[-1]/1000
        load_str = spmInfoData.load
        sec = sa.calculate_sec(total_energy, load_str, cum_distance_km)

    if(sec != 'NA'):
        summaryPage.add_pdfSummaryRecord(summaryRecord=generateSpmInfoSummaryRecord('Specific Energy Consumption (SEC)', sec, recordStyle))

def generateSrReport(spmInfoData, srRecords, speed_vals=[], cum_dist_vals=[], inst_dist_vals=[], date_time_vals=[]):
    headingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=12, align='L',textColor=(0,0,0), fillColor=(200,220,255), drawColor=(0,80,180),border=False,height=6)
    bodyStyle = pd.PdfStyle(font='helvetica', fontStyle='', fontSize=7, align='C',textColor=(0,0,0), fillColor=(224, 235, 255), drawColor=(255, 0, 0),border=True,height=8)
    endingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=8, align='C',textColor=(0,0,0), fillColor=(255,255,255), drawColor=(255,255,255),border=False,height=6)
    
    srPage = pd.PdfTableRecordPage(headingText='Speed Restriction Report',headingStyle=headingStyle, endingText='***End of Speed Restriction Report***', endingStyle=endingStyle, bodyStyle=bodyStyle)
    
    srHeadingData = ['S.No','SR From', 'SR To', 'Train Length (TL)', 'Distance SR', 'Distance with TL', 'SR Speed', 'SR Type', 'Entry Speed', 'Exit Speed', 'Max Speed', 'Min Speed', 'Avg Speed', 'Violation Dist', 'Violation Time', 'Complied']
    srHeadingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=7, align='C',textColor=(0,0,0), fillColor=(255, 100, 0), drawColor=(255, 0, 0),border=True,height=6)
    srHeading = pd.PdfTableRecord(srHeadingData, srHeadingStyle)

    srRecordStyleRight = pd.PdfStyle(fontStyle='',textColor=(0,0,0), fillColor=(224, 235, 255))
    srRecordStyleWrong = pd.PdfStyle(fontStyle='BI', textColor=(255,0,0), fillColor=(255, 255, 0))
    srRecordStyle = srRecordStyleWrong

    srPage.add_pdfTableRecord(srHeading)
    
    for i, srRecord in enumerate(srRecords):
        complied, srRecordData = create_sr_table_record(spmInfoData, i+1, srRecord, speed_vals, cum_dist_vals, inst_dist_vals, date_time_vals)
        srRecordStyle= srRecordStyleRight if complied else srRecordStyleWrong
        srRecord = pd.PdfTableRecord(srRecordData, srRecordStyle)
        srPage.add_pdfTableRecord(srRecord)
    
    return srPage

def create_sr_table_record(spmInfoData, sNo, srRecord, speed_vals, cum_dist_vals, inst_dist_vals, date_time_vals):
    #'S.No','SR From', 'SR To', 'Train Length (TL)', 'Distance SR', 'Distance with TL', 'SR Speed', 'SR Type', 'Entry Speed', 'Exit Speed', 'Max Speed', 'Min Speed', 'Avg Speed', 'Violation Dist', 'Violation Time', 'Complied'
    from_sr_chainage = srRecord.from_sr_chainage*1000
    to_sr_chainage = srRecord.to_sr_chainage*1000
    distance_sr = to_sr_chainage - from_sr_chainage
    
    sr_speed = srRecord.sr_speed
    sr_type = srRecord.sr_type.strip()
    complied = False

    try:
        train_length = float(spmInfoData.trainLength)
    except BaseException as error:
        train_length = 0

    distance_sr_tl = (to_sr_chainage + train_length) - from_sr_chainage
    diff_list_from = [cum_dist_val - from_sr_chainage for cum_dist_val in cum_dist_vals]
    diff_list_to = [cum_dist_val - (to_sr_chainage + train_length) for cum_dist_val in cum_dist_vals]

    from_index = np.argmin(np.abs(diff_list_from))
    nearest_from_dist = cum_dist_vals[from_index]
    entry_speed = speed_vals[from_index]

    to_index = np.argmin(np.abs(diff_list_to))
    nearest_to_dist = cum_dist_vals[to_index]
    exit_speed = speed_vals[to_index]
    #distance_spm = (nearest_to_dist - nearest_from_dist)

    max_speed = max(speed_vals[from_index:to_index])
    min_speed = min(speed_vals[from_index:to_index])
    avg_speed = round(sum(speed_vals[from_index:to_index])/len(speed_vals[from_index:to_index]), 2) if len(speed_vals[from_index:to_index]) > 0 else 0

    distance_violation = 0.0
    violation_seconds = 0
    index = from_index
    for speed_val in speed_vals[from_index:to_index]:
        if speed_val > sr_speed:
            distance_violation += inst_dist_vals[index]
            total_seconds = (date_time_vals[index] - date_time_vals[index-1]).total_seconds() if index > 0 else 0
            violation_seconds += total_seconds
        index += 1

    violation_time_str = str(datetime.timedelta(seconds=violation_seconds))
    srRecordData = [str(sNo), srRecord.from_sr.strip(), srRecord.to_sr.strip(), str(round(train_length,2)), str(round(distance_sr,2)), str(round(distance_sr_tl,2)), str(sr_speed), sr_type, str(entry_speed), str(exit_speed), 
                    str(max_speed), str(min_speed), str(avg_speed), str(round(distance_violation,2)), violation_time_str]
    
    #if(entry_speed <= sr_speed and exit_speed <= sr_speed and max_speed <= sr_speed and min_speed <= sr_speed and distance_violation == 0.0):
    if(distance_violation == 0.0):
        complied = True

    srRecordData.append('YES') if complied else srRecordData.append('NO')

    return (complied, srRecordData)

def generateSpeedGroupsReport(spmInfoData=None, date_time_vals=[], speed_vals=[], inst_dist_vals=[], cum_dist_vals=[]):
    headingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=12, align='L',textColor=(0,0,0), fillColor=(200,220,255), drawColor=(0,80,180),border=False,height=6)
    bodyStyle = pd.PdfStyle(font='helvetica', fontStyle='', fontSize=7, align='C',textColor=(0,0,0), fillColor=(224, 235, 255), drawColor=(255, 0, 0),border=True,height=7)
    endingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=8, align='C',textColor=(0,0,0), fillColor=(255,255,255), drawColor=(255,255,255),border=False,height=6)
    
    sgPage = pd.PdfTableRecordPage(headingText='Speed Groups Report',headingStyle=headingStyle, endingText='***End of Speed Groups Report***', endingStyle=endingStyle, bodyStyle=bodyStyle)
    
    sgHeadingData = ['S.No','Speed Group (SG)', 'Distance in SG', 'Distance (%)', 'Cumulative Distance', 'Cumulative Distance %', 'Time in SG', 'Time (%)', 'Cumulative Time', 'Cumulative Time (%)']
    sgHeadingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=7, align='C',textColor=(0,0,0), fillColor=(255, 100, 0), drawColor=(255, 0, 0),border=True,height=6)
    sgHeading = pd.PdfTableRecord(sgHeadingData, sgHeadingStyle)
    
    sgRecordStyleRight = pd.PdfStyle(fontStyle='',textColor=(0,0,0), fillColor=(224, 235, 255))
    sgRecordStyleWrong = pd.PdfStyle(fontStyle='BI', textColor=(255,0,0), fillColor=(255, 255, 0))
    sgRecordStyle = sgRecordStyleWrong

    sgPage.add_pdfTableRecord(sgHeading)
    max_speed = sa.mps_attained_val(speed_vals)
    speed_intervals = list(range(0,int(max_speed),10))
    speed_intervals.append(max_speed)
    total_cum_distance = cum_dist_vals[-1]
    total_running_time = sa.running_time_seconds(date_time_vals, speed_vals)

    x_vals = []
    y_vals_dist = []
    y_vals_time = []

    for i, speed_interval in enumerate(speed_intervals):
        if(i < (len(speed_intervals)-1)):
            start_speed = speed_interval
            end_speed = speed_intervals[i+1]
            (right, sgRecordData) = create_sg_table_record(spmInfoData, i+1, start_speed, end_speed, date_time_vals, speed_vals, inst_dist_vals, cum_dist_vals, total_cum_distance, total_running_time)
            sgRecordStyle= sgRecordStyleRight if right else sgRecordStyleWrong
            sgRecord = pd.PdfTableRecord(sgRecordData, sgRecordStyle)
            x_vals.append(sgRecordData[1])
            dist_val_percent = sgRecordData[3]
            dist_percent = dist_val_percent[0:dist_val_percent.find('%')-1].strip()
            y_vals_dist.append(float(dist_percent))
            time_val_percent = sgRecordData[7]
            time_percent = time_val_percent[0:time_val_percent.find('%')-1].strip()
            y_vals_time.append(float(time_percent))
            sgPage.add_pdfTableRecord(sgRecord)

    fig = Figure(figsize=(6, 4), dpi=300)
    fig.tight_layout(pad=5.0)
    ax1, ax2 = fig.subplots(2)
    
    ax1.set_title("Speed Groups vs Distance & Time %", fontsize=8)
    ax1.bar(x_vals, y_vals_dist, color ='blue', width = 0.4)
    ax1.tick_params(labelsize=6, width=1)
    ax1.set_ylabel('Distance %', fontsize=8)
    
    ax2.bar(x_vals, y_vals_time, color ='maroon', width = 0.4)
    ax2.tick_params(labelsize=6, width=1)
    ax2.set_ylabel('Time %', fontsize=8)
    ax2.set_xlabel('Speed Groups', fontsize=8)

    canvas = FigureCanvas(fig)
    canvas.draw()
    img = Image.fromarray(np.asarray(canvas.buffer_rgba()))

    sgPage.pageImage = img
    return sgPage

def create_sg_table_record(spmInfoData, sNo, start_speed, end_speed, date_time_vals, speed_vals, inst_dist_vals, cum_dist_vals, total_distance, total_time):
    #'S.No','Speed Group (SG)', 'Distance in SG', 'Distance (%)', 'Cumulative Distance', 'Cumulative Distance %', 'Time in SG', 'Time (%)', 'Cumulative Time', 'Cumulative Time (%)'
    speed_group = str(start_speed) + '-' + str(end_speed)
    distance_sg = sa.range_distance(inst_dist_vals, speed_vals, start_speed, end_speed)
    distance_percent = str(round((distance_sg/total_distance)*100,2)) + ' %'
    cum_sg_distance = sa.range_distance(inst_dist_vals, speed_vals, 0, end_speed)
    cum_sg_distance_percent = str(round((cum_sg_distance/total_distance)*100,2)) + ' %'
    time_sg_seconds = sa.range_time_seconds(date_time_vals,speed_vals, start_speed, end_speed)
    time_sg_percent = str(round((time_sg_seconds/total_time)*100,2)) + ' %'
    cum_time_sg_seconds = sa.range_time_seconds(date_time_vals,speed_vals, 0, end_speed)
    cum_time_sg_percent = str(round((cum_time_sg_seconds/total_time)*100,2)) + ' %'
    time_sg_str = str(datetime.timedelta(seconds=time_sg_seconds))
    cum_time_sg_str = str(datetime.timedelta(seconds=cum_time_sg_seconds))

    sgRecordData = [str(sNo), speed_group, str(round(distance_sg/1000,2)), distance_percent, str(round(cum_sg_distance/1000,2)), cum_sg_distance_percent, time_sg_str, time_sg_percent, cum_time_sg_str, cum_time_sg_percent]
    (success, response) = sa.is_speed_more(speed_vals, spmInfoData.mps, end_speed)
    if(response == 'NO' or response =='YES'):
        return (success, sgRecordData)
    else:
        return (True, sgRecordData)

def generateStoppageDistanceReport(zeroClusters=[], date_time_vals=[], speed_vals=[], cum_dist_vals=[], spmInfoData=None, showOverControl=True, showSpeedCompile=True):
    headingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=12, align='L',textColor=(0,0,0), fillColor=(200,220,255), drawColor=(0,80,180),border=False,height=6)
    bodyStyle = pd.PdfStyle(font='helvetica', fontStyle='', fontSize=7, align='C',textColor=(0,0,0), fillColor=(224, 235, 255), drawColor=(255, 0, 0),border=True,height=7)
    endingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=8, align='C',textColor=(0,0,0), fillColor=(255,255,255), drawColor=(255,255,255),border=False,height=6)
    
    sdPage = pd.PdfTableRecordPage(headingText='Stoppage Distance Report',headingStyle=headingStyle, endingText='***End of Stoppage Distance Report***', endingStyle=endingStyle, bodyStyle=bodyStyle)
    
    sdHeadingData = ['S.No','Stoppage Location', 'Date Time','Speed ~10m', 'Speed ~50m', 'Speed ~100m', 'Speed ~300m', 'Speed ~500m', 'Speed ~1000m', 'Late Controlling', 'Abrupt Braking']
    if(showOverControl):
        sdHeadingData.append('Over Controlling')
    
    if(showSpeedCompile):
        sdHeadingData.append('Speed Complied before Stop')

    sdHeadingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=7, align='C',textColor=(0,0,0), fillColor=(255, 100, 0), drawColor=(255, 0, 0),border=True,height=6)
    sdHeading = pd.PdfTableRecord(sdHeadingData, sdHeadingStyle)
    
    sdRecordStyleRight = pd.PdfStyle(fontStyle='',textColor=(0,0,0), fillColor=(224, 235, 255))
    sdRecordStyleWrong = pd.PdfStyle(fontStyle='BI', textColor=(255,0,0), fillColor=(255, 255, 0))
    sdRecordStyle = sdRecordStyleWrong

    sdPage.add_pdfTableRecord(sdHeading)
    sNo = 1
    for i, zeroCluster in enumerate(zeroClusters):
        index, cumDist = (zeroCluster)
        if(cumDist != 0):
            complied, sdRecordData = create_sd_table_record(sNo, zeroCluster, date_time_vals, speed_vals, cum_dist_vals, spmInfoData, showOverControl, showSpeedCompile)
            sdRecordStyle= sdRecordStyleRight if complied else sdRecordStyleWrong
            srRecord = pd.PdfTableRecord(sdRecordData, sdRecordStyle)
            sdPage.add_pdfTableRecord(srRecord)
            sNo += 1
    
    return sdPage

def create_sd_table_record(sNo, zeroCluster, date_time_vals, speed_vals, cum_dist_vals, spmInfoData, showOverControl, showSpeedCompile):
    #'S.No','Stoppage Location', 'Date Time','Speed ~10m', 'Speed ~50m', 'Speed ~100m', 'Speed ~300m', 'Speed ~500m', 'Speed ~1000m', 'Late Controlling', 'Over Controlling', 'Abrupt Braking', 'Speed Complied before Stop'
    index, cumDist = zeroCluster

    zero_date_time = date_time_vals[index]
    ten_speed, fifty_speed, hun_speed, threehun_speed, fivehun_speed, thou_speed = (float('-inf'),float('-inf'),float('-inf'),float('-inf'),float('-inf'),float('-inf'))
    ten_dist, fifty_dist, hun_dist, threehun_dist, fivehun_dist, thou_dist = (float('-inf'),float('-inf'),float('-inf'),float('-inf'),float('-inf'),float('-inf'))
    i = index
    
    for cum_dist_val in cum_dist_vals[index:0:-1]:
        dist_from_zero = cumDist - cum_dist_val
        if(dist_from_zero >= 10 and ten_speed == float('-inf')):
            ten_speed = speed_vals[i]
            ten_dist = dist_from_zero
        
        if(dist_from_zero >= 50 and fifty_speed == float('-inf')):
            fifty_speed = speed_vals[i]
            fifty_dist = dist_from_zero

        if(dist_from_zero >= 100 and hun_speed == float('-inf')):
            hun_speed = speed_vals[i]
            hun_dist = dist_from_zero

        if(dist_from_zero >= 300 and threehun_speed == float('-inf')):
            threehun_speed = speed_vals[i]
            threehun_dist = dist_from_zero

        if(dist_from_zero >= 500 and fivehun_speed == float('-inf')):
            fivehun_speed = speed_vals[i]
            fivehun_dist = dist_from_zero
        
        if(dist_from_zero >= 1000 and thou_speed == float('-inf')):
            thou_speed = speed_vals[i]
            thou_dist = dist_from_zero

        i -= 1

    stopLoc_str = str(round(cumDist/1000,2))
    date_time_str = zero_date_time.strftime('%d-%m-%y %H:%M:%S')
    ten_entry = f'{ten_speed} ({round(ten_dist,2)})' if ten_speed != float('-inf') else 'NA'
    fifty_entry = f'{fifty_speed} ({round(fifty_dist,2)})' if fifty_speed != float('-inf') else 'NA'
    hun_entry = f'{hun_speed} ({round(hun_dist,2)})' if hun_speed != float('-inf') else 'NA'
    threehun_entry = f'{threehun_speed} ({round(threehun_dist,2)})' if threehun_speed != float('-inf') else 'NA'
    fivehun_entry = f'{fivehun_speed} ({round(fivehun_dist,2)})' if fivehun_speed != float('-inf') else 'NA'
    thou_entry = f'{thou_speed} ({round(thou_dist,2)})' if thou_speed != float('-inf') else 'NA'

    service = spmInfoData.service
    abruptBraking = False
    lateControlling = False
    overControlling = False
    speedComplied = True
    complied = False

    if(ten_speed > 15 or fifty_speed > 25 or hun_speed > 30):
        abruptBraking = True
    
    if(thou_speed != float('-inf')):
        if(service == 'GOODS'):
            overControlling = False if thou_speed > 20 else True
        else:
            overControlling = False if thou_speed > 45 else True

    if(service == 'GOODS'):
        lateControlling = True if thou_speed > 40 else False
    else:
        lateControlling = True if thou_speed > 70 else False

    if(ten_speed > 8 or fifty_speed > 8 or hun_speed > 15):
        speedComplied = False

    abruptBraking_str = 'YES' if abruptBraking else 'NO'
    overControlling_str = 'YES' if overControlling else 'NO'
    lateControlling_str = 'YES' if lateControlling else 'NO'
    speedComplied_str = 'YES' if speedComplied else 'NO'
    
    #'S.No','Stoppage Location', 'Date Time','Speed ~10m', 'Speed ~50m', 'Speed ~100m', 'Speed ~300m', 'Speed ~500m', 'Speed ~1000m', 'Late Controlling', 'Over Controlling', 'Abrupt Braking', 'Speed Complied before Stop'
    sdRecordData = [str(sNo), stopLoc_str, date_time_str, ten_entry, fifty_entry, hun_entry, threehun_entry, fivehun_entry, thou_entry, lateControlling_str, abruptBraking_str]
    if(showOverControl):
        sdRecordData.append(overControlling_str)

    if(showSpeedCompile):
        sdRecordData.append(speedComplied_str)
    
    overControlling = overControlling if showOverControl else False
    speedComplied = speedComplied if showSpeedCompile else True

    if(speedComplied and (not abruptBraking) and (not overControlling) and (not lateControlling)):
        complied = True

    return (complied, sdRecordData)

def generateStoppageItemReport(zeroClusters, itemRecords, date_time_vals, speed_vals, cum_dist_vals, spmInfoData):
    headingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=12, align='L',textColor=(0,0,0), fillColor=(200,220,255), drawColor=(0,80,180),border=False,height=6)
    bodyStyle = pd.PdfStyle(font='helvetica', fontStyle='', fontSize=7, align='C',textColor=(0,0,0), fillColor=(224, 235, 255), drawColor=(255, 0, 0),border=True,height=7)
    endingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=8, align='C',textColor=(0,0,0), fillColor=(255,255,255), drawColor=(255,255,255),border=False,height=6)

    siPage = pd.PdfTableRecordPage(headingText='Stoppage Signal Report',headingStyle=headingStyle, endingText='***End of Stoppage Signal Report***', endingStyle=endingStyle, bodyStyle=bodyStyle)
    
    siHeadingData = ['S.No','Stoppage Location', 'Date Time','One Signal Before (Distance, Speed, DateTime)', 'Two Signal Before (Distance, Speed, DateTime)', 'Three Signal Before (Distance, Speed, DateTime)', 'One signal After (Distance, Speed, DateTime)', 'Two signal After (Distance, Speed, DateTime)']
    siHeadingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=7, align='C',textColor=(0,0,0), fillColor=(255, 100, 0), drawColor=(255, 0, 0),border=True,height=6)
    siHeading = pd.PdfTableRecord(siHeadingData, siHeadingStyle)
    
    siRecordStyleRight = pd.PdfStyle(fontStyle='',textColor=(0,0,0), fillColor=(224, 235, 255))
    siRecordStyleWrong = pd.PdfStyle(fontStyle='BI', textColor=(255,0,0), fillColor=(255, 255, 0))
    siRecordStyle = siRecordStyleWrong

    siPage.add_pdfTableRecord(siHeading)

    sNo = 1
    for i, zeroCluster in enumerate(zeroClusters):
        index, cumDist = (zeroCluster)
        if(cumDist != 0):
            siRecordData, complied = create_si_table_record(sNo, zeroCluster, itemRecords, date_time_vals, speed_vals, cum_dist_vals, spmInfoData.service)
            siRecordStyle= siRecordStyleRight if complied else siRecordStyleWrong
            siRecord = pd.PdfTableRecord(siRecordData, siRecordStyle)
            siPage.add_pdfTableRecord(siRecord)
            sNo += 1
    
    return siPage

def create_si_table_record(sNo, zeroCluster, itemRecords, date_time_vals, speed_vals, cum_dist_vals,service):
    #'S.No','Stoppage Location', 'Date Time','One Signal Before (Distance, Speed, DateTime)', 'Two Signal Before (Distance, Speed, DateTime)', 'Three Signal Before (Distance, Speed, DateTime)', 'One signal After (Distance, Speed, DateTime)', 'Two signal After (Distance, Speed, DateTime)'
    index, zeroDist = zeroCluster

    zero_date_time = date_time_vals[index]
    stopLoc_str = str(round(zeroDist/1000,2))
    date_time_str = zero_date_time.strftime('%d-%m-%y %H:%M:%S')
    i = index
    listItemTuplesLeft = []
    listItemTuplesRight = []
    for itemRecord in itemRecords:
        distance_from_stoppage = itemRecord.km_chainage*1000 - zeroDist
        if(distance_from_stoppage < 0):
            itemTupleLeft = (abs(distance_from_stoppage), itemRecord.itemNo, zeroDist)
            listItemTuplesLeft.append(itemTupleLeft)
        else:
            itemTupleRight = (abs(distance_from_stoppage),itemRecord.itemNo, zeroDist)
            listItemTuplesRight.append(itemTupleRight)
    
    listItemTuplesLeft = sorted(listItemTuplesLeft)
    listItemTuplesRight = sorted(listItemTuplesRight)

    siRecordData = [str(sNo), stopLoc_str, date_time_str]
    leftCount = 0
    first_left_speed = float('-inf')
    first_left_distance = float('-inf')
    for itemTupleLeft in listItemTuplesLeft:
        if(leftCount < 3):
            signal_entry, signal_distance, signal_speed = construct_signal_entry(itemTupleLeft, itemRecords, cum_dist_vals, date_time_vals, speed_vals)
            if(signal_entry != ''):
                siRecordData.append(signal_entry)
                leftCount += 1
                if(leftCount == 1):
                    first_left_distance = abs(signal_distance)
                    first_left_speed = signal_speed
    
    while leftCount < 3:
        siRecordData.append('NA')
        leftCount += 1

    rightCount = 0
    first_right_speed = float('-inf')
    first_right_distance = float('-inf')
    for itemTupleRight in listItemTuplesRight:
        if(rightCount < 2):
            signal_entry, signal_distance, signal_speed = construct_signal_entry(itemTupleRight, itemRecords, cum_dist_vals, date_time_vals, speed_vals)
            if(signal_entry != ''):
                siRecordData.append(signal_entry)
                rightCount += 1
                if(rightCount == 1):
                    first_right_distance = abs(signal_distance)
                    first_right_speed = signal_speed
    
    while rightCount < 2:
        siRecordData.append('NA')
        rightCount += 1

    complied = True
    if(first_left_distance != float('-inf') and first_right_distance != float('-inf') and first_right_distance <= 300 and first_left_distance <= 1500):
        if(service == 'GOODS' and first_left_speed >= 35):
            complied = False
        elif(service == 'COACHING' and first_left_speed >= 65):
            complied = False
        else:
            complied = True
    return (siRecordData, complied)

def construct_signal_entry(itemTuple, itemRecords, cum_dist_vals, date_time_vals, speed_vals):
    distance_from_stoppage, itemNo, zeroDist = itemTuple
    distance_from_stoppage_str = str(round(distance_from_stoppage/1000, 3))
    itemRecord = None

    for ir in itemRecords:
        if ir.itemNo == itemNo:
            itemRecord = ir
    
    signal_entry = ''
    print(itemRecord)
    if(itemRecord is not None):
        if(len(itemRecord.signalRecords) > 0):
            diff_list = [cum_dist_value - itemRecord.km_chainage*1000 for cum_dist_value in cum_dist_vals]
            index = np.argmin(np.abs(diff_list))
            
            item_dist_from_zero_str = str(round((cum_dist_vals[index] - zeroDist),2))
            item_date_time = date_time_vals[index].strftime('%d-%m-%Y %H:%M:%S')
            item_speed = str(speed_vals[index])
            signal_str = ''
            for signalRecord in itemRecord.signalRecords:
                signal_str = signalRecord.signal_name + ':' + signalRecord.signal_location if signal_str == '' else signal_str + '#' + signalRecord.signal_name + ':' + signalRecord.signal_location
            
            signal_entry = f'{signal_str} ({item_dist_from_zero_str}, {item_speed}, {item_date_time})'
    
    if(signal_entry != ''):
        return signal_entry, round((cum_dist_vals[index] - zeroDist),2), speed_vals[index]
    else:
        return signal_entry, 0, 0

def generateStationToStationReport(itemRecords=[], date_time_vals=[], cum_dist_vals=[], speed_vals=[]):
    headingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=12, align='L',textColor=(0,0,0), fillColor=(200,220,255), drawColor=(0,80,180),border=False,height=6)
    bodyStyle = pd.PdfStyle(font='helvetica', fontStyle='', fontSize=7, align='C',textColor=(0,0,0), fillColor=(224, 235, 255), drawColor=(255, 0, 0),border=True,height=7)
    endingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=8, align='C',textColor=(0,0,0), fillColor=(255,255,255), drawColor=(255,255,255),border=False,height=6)
    
    ssPage = pd.PdfTableRecordPage(headingText='Station to Station Report',headingStyle=headingStyle, endingText='***End of Station to Station Report***', endingStyle=endingStyle, bodyStyle=bodyStyle)
    
    ssHeadingData = ['S.No','From Station', 'To Station','Distance', 'Total Time', 'Running Time', 'Idle Time', 'Idle Percent', 'Average Speed', 'Dynamic Speed']
    ssHeadingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=7, align='C',textColor=(0,0,0), fillColor=(255, 100, 0), drawColor=(255, 0, 0),border=True,height=6)
    ssHeading = pd.PdfTableRecord(ssHeadingData, ssHeadingStyle)
    
    ssRecordStyleRight = pd.PdfStyle(fontStyle='',textColor=(0,0,0), fillColor=(224, 235, 255))
    ssRecordStyleWrong = pd.PdfStyle(fontStyle='BI', textColor=(255,0,0), fillColor=(255, 255, 0))
    ssRecordStyle = ssRecordStyleRight

    ssPage.add_pdfTableRecord(ssHeading)
    sNo = 1
    prevStation = 'START (S)'
    prevIndex = 0
    prevDistance = 0
    displayIndex = 0

    x_vals = []
    y_vals_avg = []
    y_vals_dyn = []

    for itemRecord in itemRecords:
        stationRecords = itemRecord.stationRecords
        if(len(stationRecords) > 0):
            station = stationRecords[0].station_name
            km_chainage = itemRecord.km_chainage
            diff_list = [cum_dist_value - km_chainage*1000 for cum_dist_value in cum_dist_vals]
            index = np.argmin(np.abs(diff_list))
            
            distance = round(km_chainage - prevDistance, 2)
            ssRecordData = create_ss_table_record(sNo, prevStation, station,  prevIndex, index, distance, date_time_vals, cum_dist_vals, speed_vals, displayIndex)
            ssRecord = pd.PdfTableRecord(ssRecordData, ssRecordStyle)
            
            ssPage.add_pdfTableRecord(ssRecord)
            displayStr = ''
            if displayIndex == 0:
                displayStr = f'S-{displayIndex+1}'
            else:
                displayStr = f'{displayIndex}-{displayIndex+1}'

            x_vals.append(displayStr)

            y_vals_avg.append(float(ssRecordData[8]))
            y_vals_dyn.append(float(ssRecordData[9]))

            print(f'{prevStation}, {station}, {prevIndex}, {index}')

            prevStation = station
            prevIndex = index
            prevDistance = km_chainage
            sNo += 1
            displayIndex += 1
            
    distance = round(cum_dist_vals[-1]/1000 - prevDistance, 2)
    
    ssRecordData = create_ss_table_record(sNo, prevStation, 'END (E)', prevIndex, len(cum_dist_vals) - 1, distance, date_time_vals, cum_dist_vals, speed_vals, displayIndex)
    ssPage.add_pdfTableRecord(pd.PdfTableRecord(ssRecordData, ssRecordStyle))

    displayStr = ''
    if displayIndex == 0:
        displayStr = f'S-E'
    else:
        displayStr = f'{displayIndex}-E'

    x_vals.append(displayStr)
    y_vals_avg.append(float(ssRecordData[8]))
    y_vals_dyn.append(float(ssRecordData[9]))
    
    fig = Figure(figsize=(6, 4), dpi=300)
    fig.tight_layout(pad=5.0)
    ax1, ax2 = fig.subplots(2)
    
    ax1.set_title("Station-Station Average & Dynamic Speeds", fontsize=8)
    ax1.bar(x_vals, y_vals_avg, color ='blue', width = 0.4)
    ax1.tick_params(labelsize=6, width=1)
    ax1.set_ylabel('Average Speed', fontsize=8)
    
    ax2.bar(x_vals, y_vals_dyn, color ='maroon', width = 0.4)
    ax2.tick_params(labelsize=6, width=1)
    ax2.set_ylabel('Dynamic Speed', fontsize=8)
    ax2.set_xlabel('Station sections', fontsize=8)

    canvas = FigureCanvas(fig)
    canvas.draw()
    img = Image.fromarray(np.asarray(canvas.buffer_rgba()))

    ssPage.pageImage = img
    return ssPage
    
def create_ss_table_record(sNo, prevStation, presentStation, prevIndex, presentIndex, distance, date_time_vals, cum_dist_vals, speed_vals, displayIndex):
    #'S.No','From Station', 'To Station','Distance', 'Total Time', 'Running Time', 'Idle Time', 'Idle Percent', 'Average Speed', 'Dynamic Speed'
    _, time_duration = sa.time_duration_between(prevIndex, presentIndex, date_time_vals)
    _, running_time_duration = sa.running_time_between_duration(prevIndex, presentIndex, date_time_vals, speed_vals)
    _, idle_time_duration = sa.idle_time_between_duration(prevIndex, presentIndex, date_time_vals, speed_vals)
    _, idle_percent = sa.idle_time_between_percent(prevIndex,presentIndex,date_time_vals,speed_vals)
    _, average_speed = sa.average_speed_between(prevIndex, presentIndex, date_time_vals, cum_dist_vals)
    _, dynamic_speed = sa.dynamic_speed_between(prevIndex, presentIndex, date_time_vals, cum_dist_vals, speed_vals)

    prevDisplayStr = 'S' if displayIndex == 0 else str(displayIndex)
    ssRecordData = [str(sNo), f'{prevStation} ({prevDisplayStr})', f'{presentStation} ({displayIndex+1})', str(distance), time_duration, running_time_duration, idle_time_duration, idle_percent, average_speed, dynamic_speed]
    
    return ssRecordData

def generateItemReport(itemRecords, date_time_vals=[], speed_vals=[], cum_dist_vals=[]):
    headingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=12, align='L',textColor=(0,0,0), fillColor=(200,220,255), drawColor=(0,80,180),border=False,height=6)
    bodyStyle = pd.PdfStyle(font='helvetica', fontStyle='', fontSize=7, align='C',textColor=(0,0,0), fillColor=(224, 235, 255), drawColor=(255, 0, 0),border=True,height=8)
    endingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=8, align='C',textColor=(0,0,0), fillColor=(255,255,255), drawColor=(255,255,255),border=False,height=6)
    
    itemPage = pd.PdfTableRecordPage(headingText='Signal/Item Report',headingStyle=headingStyle, endingText='***End of Signal/Item Report***', endingStyle=endingStyle, bodyStyle=bodyStyle)
    
    itemHeadingData = ['S.No','Item', 'Item Code','Km (Mapping)', 'Km (SPM)', 'Date Time', 'Speed']
    itemHeadingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=7, align='C',textColor=(0,0,0), fillColor=(255, 100, 0), drawColor=(255, 0, 0),border=True,height=6)
    itemHeading = pd.PdfTableRecord(itemHeadingData, itemHeadingStyle)

    itemRecordStyleRight = pd.PdfStyle(fontStyle='',textColor=(0,0,0), fillColor=(224, 235, 255))
    #itemRecordStyleWrong = pd.PdfStyle(fontStyle='BI', textColor=(255,0,0), fillColor=(255, 255, 0))
    itemRecordStyle = itemRecordStyleRight

    itemPage.add_pdfTableRecord(itemHeading)
    
    for i, itemRecord in enumerate(itemRecords):
        itemRecordData = create_item_table_record(i+1, itemRecord, date_time_vals, speed_vals, cum_dist_vals)
        itemRecord = pd.PdfTableRecord(itemRecordData, itemRecordStyle)
        itemPage.add_pdfTableRecord(itemRecord)
    
    return itemPage

def create_item_table_record(sNo, itemRecord, date_time_vals, speed_vals, cum_dist_vals):
    #'S.No','Item', 'Item Code', 'Km (Mapping)', 'Km (SPM)', 'Date Time', 'Speed'
    km_chainage = itemRecord.km_chainage*1000

    diff_list = [cum_dist_val - km_chainage for cum_dist_val in cum_dist_vals]
    index = np.argmin(np.abs(diff_list))
    nearest_dist = cum_dist_vals[index]
    date_time_val = date_time_vals[index].strftime('%d-%m-%Y %H:%M:%S')
    speed = speed_vals[index]

    itemRecord = [str(sNo), itemRecord.item.strip(), itemRecord.item_code.strip(), str(round(itemRecord.km_chainage, 3)), str(round(nearest_dist/1000, 3)), 
                    date_time_val, str(speed)]

    return itemRecord

def generateGradientReport(gradientRecords=[], attackSpeed=0, date_time_vals=[], speed_vals=[], cum_dist_vals=[]):
    headingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=12, align='L',textColor=(0,0,0), fillColor=(200,220,255), drawColor=(0,80,180),border=False,height=6)
    bodyStyle = pd.PdfStyle(font='helvetica', fontStyle='', fontSize=7, align='C',textColor=(0,0,0), fillColor=(224, 235, 255), drawColor=(255, 0, 0),border=True,height=8)
    endingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=8, align='C',textColor=(0,0,0), fillColor=(255,255,255), drawColor=(255,255,255),border=False,height=6)
    
    gradientPage = pd.PdfTableRecordPage(headingText='Rising Gradient Report',headingStyle=headingStyle, endingText='***End of Gradient Report***', endingStyle=endingStyle, bodyStyle=bodyStyle)
    
    gradientHeadingData = ['S.No','Gradient From (km)', 'Gradient To (km)', 'Distance (m)', 'Direction', 'Gradient (1 in _)', 'Speed', 'Date Time', 'Attack Speed', 'Complied']
    gradientHeadingStyle = pd.PdfStyle(font='helvetica', fontStyle='B', fontSize=7, align='C',textColor=(0,0,0), fillColor=(255, 100, 0), drawColor=(255, 0, 0),border=True,height=6)
    gradientHeading = pd.PdfTableRecord(gradientHeadingData, gradientHeadingStyle)

    gradientRecordStyleRight = pd.PdfStyle(fontStyle='',textColor=(0,0,0), fillColor=(224, 235, 255))
    gradientRecordStyleWrong = pd.PdfStyle(fontStyle='BI', textColor=(255,0,0), fillColor=(255, 255, 0))
    gradientRecordStyle = gradientRecordStyleRight

    gradientPage.add_pdfTableRecord(gradientHeading)
    sNo = 1
    for i, gradientRecord in enumerate(gradientRecords):
        if(gradientRecord.direction == 'RISE'):
            complied, gradientRecordData = create_gradient_table_record(sNo, gradientRecord, attackSpeed, date_time_vals, speed_vals, cum_dist_vals)
            gradientRecordStyle= gradientRecordStyleRight if complied else gradientRecordStyleWrong
            gradientRecord = pd.PdfTableRecord(gradientRecordData, gradientRecordStyle)
            gradientPage.add_pdfTableRecord(gradientRecord)
            sNo += 1
    
    return gradientPage

def create_gradient_table_record(sNo, gradientRecord, attackSpeed, date_time_vals, speed_vals, cum_dist_vals):
    #'S.No','Gradient From', 'Gradient To', 'Distance', 'Direction', 'Gradient', 'Speed', 'Date Time', 'Attack Speed', 'Complied'
    from_chainage = gradientRecord.from_km*1000
    to_chainage = gradientRecord.to_km*1000

    diff_list = [cum_dist_val - from_chainage for cum_dist_val in cum_dist_vals]
    index = np.argmin(np.abs(diff_list))
    nearest_dist = cum_dist_vals[index]
    date_time_val = date_time_vals[index].strftime('%d-%m-%Y %H:%M:%S')
    speed = speed_vals[index]

    distance = to_chainage - from_chainage
    complied = True if speed > attackSpeed else False
    complied_str = 'YES ' if complied else 'NO'
    gradientRecord = [str(sNo), str(round(gradientRecord.from_km,2)) + f'({str(round(nearest_dist/1000,2))})', str(gradientRecord.to_km), str(distance), gradientRecord.direction, str(gradientRecord.gradient), 
                      str(speed), date_time_val, str(attackSpeed), complied_str]

    return (complied, gradientRecord)
