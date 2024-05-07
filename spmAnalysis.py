import datetime

def is_over_speed(speed_vals=[], mps_given=''):
    if(mps_given != None and mps_given.strip() != ''):
        try:
            mps_given_val = float(mps_given)
            over_speed = (True,'NO')
            if(mps_attained_val(speed_vals) > mps_given_val*1.05):
                over_speed = (False, 'YES')

        except BaseException as error:
            over_speed = (False,'INVALID MPS')
    else:
        over_speed = (False,'EMPTY MPS')
    
    return over_speed

def mps_attained_val(speed_vals=[]):
    return max(speed_vals)

def mps_attained(speed_vals=[]):
    if(speed_vals != None and len(speed_vals) > 0):
        return (True, str(mps_attained_val(speed_vals)))
    else:
        return (False, 'EMPTY DATA')

def is_speed_more(speed_vals=[], mps_given='', speedTested=0.0):
    if(mps_given != None and mps_given.strip() != ''):
        try:
            mps_given_val = float(mps_given)
            over_speed = (True,'NO')
            if(speedTested > mps_given_val*1.05):
                over_speed = (False, 'YES')

        except BaseException as error:
            over_speed = (False,'INVALID MPS')
    else:
        over_speed = (False,'EMPTY MPS')
    
    return over_speed

def compute_excess_mps_distance(mps_given='', distance_vals=[], speed_vals=[], date_time_vals=[]):
    if(mps_given != None and mps_given.strip() != ''):
        try:
            mps_val = float(mps_given)
            cum_excess_distance = 0.0
            total_seconds = 0

            for i, speed_val in enumerate(speed_vals):
                if (speed_val > mps_val*1.05):
                    cum_excess_distance += distance_vals[i]
                    if (i > 0):
                        seconds = (date_time_vals[i] - date_time_vals[i-1]).total_seconds()
                        total_seconds += seconds
            
            return (True, total_seconds, cum_excess_distance)
        except BaseException as error:
            return (False,'INVALID MPS', 'INVALID MPS')
    else:
        return (False,'EMPTY MPS', 'EMPTY MPS')

def compute_mps_distance(mps='', from_mps='', to_mps='', distance_vals=[], speed_vals=[]):
    mps_distance = 0.0
    mps_val, from_mps_val, to_mps_val = (0.0,0.0,0.0)
    mps_present=False
    from_default=False
    to_default=False
    if(mps != None and mps.strip() != ''):
        try:
            mps_val = float(mps)
            mps_present = True
        except BaseException as error:
            mps_present=False
    else:
        mps_present=False
    
    if(from_mps != None and from_mps.strip() != ''):
        try:
            from_mps_val = float(from_mps)
        except BaseException as error:
            if(mps_present):
                from_mps_val = mps_val*0.95
                from_default = True
            else:
                return (False, False, False,0.0,0.0, 'MPS/From/To MPS INVALID')
    else:
        if(mps_present):
            from_mps_val = mps_val*0.95
            from_default = True
        else:
            return (False, False, False,0.0,0.0, 'MPS/From/To MPS INVALID')

    if(to_mps != None and to_mps.strip() != ''):
        try:
            to_mps_val = float(to_mps)
        except BaseException as error:
            if(mps_present):
                to_mps_val = mps_val*1.05
                to_default = True
            else:
                return (False, False, False,0.0,0.0, 'MPS/From/To MPS INVALID')
    else:
        if(mps_present):
            to_mps_val = mps_val*1.05
            to_default = True
        else:
            return (False, False, False,0.0,0.0, 'MPS/From/To MPS INVALID')

    if(speed_vals == None or len(speed_vals) == 0):
        return (False, False,False,0.0,0.0, 'EMPTY SPEED DATA')
    
    print(f'(MPS, From MPS, To MPS) => ({str(mps_val)}, {str(from_mps_val)}, {str(to_mps_val)})')
    mps_distance = 0.0
    for i in range(len(speed_vals)):
        if (speed_vals[i] >= from_mps_val) and (speed_vals[i] <= to_mps_val):
            mps_distance += distance_vals[i]
    return (True, from_default, to_default,from_mps_val,to_mps_val, str(round(mps_distance/1000,2)))

def average_speed(date_time_vals=[], cum_distance_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0 and cum_distance_vals != None and len(cum_distance_vals) > 0):
        start_date_time = date_time_vals[0]
        end_date_time = date_time_vals[-1]
        total_distance = cum_distance_vals[-1]/1000 #In km
        total_time = (end_date_time - start_date_time).total_seconds()/3600
        average_speed = total_distance/total_time
        return (True, str(round(average_speed,2)))
    else:
        return (False,'EMPTY DATA')

def average_speed_between(startIndex, endIndex, date_time_vals=[], cum_distance_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0 and cum_distance_vals != None and len(cum_distance_vals) > 0):
        start_date_time = date_time_vals[startIndex]
        end_date_time = date_time_vals[endIndex]
        total_distance = (cum_distance_vals[endIndex] - cum_distance_vals[startIndex])/1000 #In km
        total_time = (end_date_time - start_date_time).total_seconds()/3600
        average_speed = total_distance/total_time
        return (True, str(round(average_speed,2)))
    else:
        return (False,'EMPTY DATA')
    
def compute_total_distance(cum_distance_vals=[]):
    if(cum_distance_vals != None and len(cum_distance_vals) > 0):
        total_distance = cum_distance_vals[-1]/1000 #In km
        return (True, str(round(total_distance,2)))
    else:
        return (False,'EMPTY DATA')

def dynamic_speed(date_time_vals=[], cum_distance_vals=[], speed_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0 and cum_distance_vals != None and len(cum_distance_vals) > 0):
        total_distance = cum_distance_vals[-1]/1000 #In km
        running_time = running_time_seconds(date_time_vals, speed_vals)/3600
        dynamic_speed = total_distance/running_time
        return (True,str(round(dynamic_speed,2)))
    else:
        return (False,'EMPTY DATA')

def dynamic_speed_between(startIndex, endIndex, date_time_vals=[], cum_distance_vals=[], speed_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0 and cum_distance_vals != None and len(cum_distance_vals) > 0):
        total_distance = (cum_distance_vals[endIndex] - cum_distance_vals[startIndex])/1000 #In km
        running_time = running_time_between_seconds(startIndex, endIndex, date_time_vals, speed_vals)/3600
        if(running_time != 0):
            dynamic_speed = total_distance/running_time
        else:
            dynamic_speed = 0
        return (True,str(round(dynamic_speed,2)))
    else:
        return (False,'EMPTY DATA')
    
def total_time_duration(date_time_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0):
        start_date_time = date_time_vals[0]
        end_date_time = date_time_vals[-1]
        total_seconds = (end_date_time - start_date_time).total_seconds()
        return (True, str(datetime.timedelta(seconds=total_seconds)))
    else:
        return (False,'EMPTY DATA')

def late_controlling(zeroClusters=[], speed_vals=[], cum_dist_vals=[], service='GOODS'):
    lateControlling = False
    for i, zeroCluster in enumerate(zeroClusters):
        index, cumDist = (zeroCluster)
        if(cumDist != 0):
            lateControlling = check_late_controlling(zeroCluster, speed_vals, cum_dist_vals, service)
            if(lateControlling):
                return lateControlling
    
    return lateControlling

def check_late_controlling(zeroCluster, speed_vals, cum_dist_vals, service):
    index, cumDist = zeroCluster
    lateControlling = False

    thou_speed = float('-inf')
    i = index
    
    for cum_dist_val in cum_dist_vals[index:0:-1]:
        dist_from_zero = cumDist - cum_dist_val
        
        if(dist_from_zero >= 1000 and thou_speed == float('-inf')):
            thou_speed = speed_vals[i]
        i -= 1

    if(service == 'GOODS'):
        lateControlling = True if thou_speed > 40 else False
    else:
        lateControlling = True if thou_speed > 70 else False

    return lateControlling

def over_controlling(zeroClusters=[], speed_vals=[], cum_dist_vals=[], service='GOODS'):
    overControl = False
    for i, zeroCluster in enumerate(zeroClusters):
        index, cumDist = (zeroCluster)
        if(cumDist != 0):
            overControl = check_over_controlling(zeroCluster, speed_vals, cum_dist_vals, service)
            if(overControl):
                return overControl
    
    return overControl

def check_over_controlling(zeroCluster, speed_vals, cum_dist_vals, service):
    index, cumDist = zeroCluster
    overControl = False

    thou_speed = float('-inf')
    i = index
    
    for cum_dist_val in cum_dist_vals[index:0:-1]:
        dist_from_zero = cumDist - cum_dist_val
        
        if(dist_from_zero >= 1000 and thou_speed == float('-inf')):
            thou_speed = speed_vals[i]
        i -= 1

    if(service == 'GOODS'):
        overControl = False if thou_speed > 20 else True
    else:
        overControl = False if thou_speed > 45 else True

    return overControl

def abrupt_braking(zeroClusters=[], speed_vals=[], cum_dist_vals=[]):
    abruptBraking = False
    for i, zeroCluster in enumerate(zeroClusters):
        index, cumDist = (zeroCluster)
        if(cumDist != 0):
            abruptBraking = check_abrupt_braking(zeroCluster, speed_vals, cum_dist_vals)
            if(abruptBraking):
                return abruptBraking
    
    return abruptBraking

def check_abrupt_braking(zeroCluster, speed_vals, cum_dist_vals):
    index, cumDist = zeroCluster
    abruptBraking = False

    ten_speed, fifty_speed, hun_speed = (float('-inf'), float('-inf'), float('-inf'))
    i = index
    
    for cum_dist_val in cum_dist_vals[index:0:-1]:
        dist_from_zero = cumDist - cum_dist_val
        
        if(dist_from_zero >= 10 and ten_speed == float('-inf')):
            ten_speed = speed_vals[i]
        
        if(dist_from_zero >= 50 and fifty_speed == float('-inf')):
            fifty_speed = speed_vals[i]

        if(dist_from_zero >= 100 and hun_speed == float('-inf')):
            hun_speed = speed_vals[i]

        i -= 1

    if(ten_speed > 15 or fifty_speed > 25 or hun_speed > 30):
        abruptBraking = True

    return abruptBraking

def speed_complied(zeroClusters=[], speed_vals=[], cum_dist_vals=[]):
    speedComplied = True
    for i, zeroCluster in enumerate(zeroClusters):
        index, cumDist = (zeroCluster)
        if(cumDist != 0):
            speedComplied = check_speed_complied(zeroCluster, speed_vals, cum_dist_vals)
            if(not speedComplied):
                return speedComplied
    
    return speedComplied

def check_speed_complied(zeroCluster, speed_vals, cum_dist_vals):
    index, cumDist = zeroCluster
    speedComplied = True

    ten_speed, fifty_speed, hun_speed = (float('-inf'), float('-inf'), float('-inf'))
    i = index
    
    for cum_dist_val in cum_dist_vals[index:0:-1]:
        dist_from_zero = cumDist - cum_dist_val
        
        if(dist_from_zero >= 10 and ten_speed == float('-inf')):
            ten_speed = speed_vals[i]
        
        if(dist_from_zero >= 50 and fifty_speed == float('-inf')):
            fifty_speed = speed_vals[i]

        if(dist_from_zero >= 100 and hun_speed == float('-inf')):
            hun_speed = speed_vals[i]

        i -= 1

    if(ten_speed > 8 or fifty_speed > 8 or hun_speed > 15):
        speedComplied = False

    return speedComplied

def time_duration_between(startIndex, endIndex, date_time_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0):
        start_date_time = date_time_vals[startIndex]
        end_date_time = date_time_vals[endIndex]
        total_seconds = (end_date_time - start_date_time).total_seconds()
        return (True, str(datetime.timedelta(seconds=total_seconds)))
    else:
        return (False,'EMPTY DATA')
    
def running_time_duration(date_time_vals=[], speed_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0 and speed_vals != None and len(speed_vals) > 0):
        return (True,str(datetime.timedelta(seconds=running_time_seconds(date_time_vals, speed_vals))))
    else:
        return (False, 'EMPTY DATA')
       
def running_time_seconds(date_time_vals=[], speed_vals=[]):
    total_time_seconds = 0
    for i, date_time_val in enumerate(date_time_vals):
        if(i > 0):
            if(speed_vals[i-1] > 0):
                time_delta = (date_time_val - date_time_vals[i-1])
                total_time_seconds += time_delta.total_seconds()
    return total_time_seconds

def running_time_between_duration(startIndex, endIndex, date_time_vals=[], speed_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0 and speed_vals != None and len(speed_vals) > 0):
        return (True,str(datetime.timedelta(seconds=running_time_between_seconds(startIndex, endIndex, date_time_vals, speed_vals))))
    else:
        return (False, 'EMPTY DATA')
       
def running_time_between_seconds(startIndex=0, endIndex=-1, date_time_vals=[], speed_vals=[]):
    total_time_seconds = 0
    for index, date_time_val in enumerate(date_time_vals):
        if(index > startIndex and index <= endIndex):
            if(speed_vals[index-1] > 0):
                time_delta = (date_time_val - date_time_vals[index-1])
                total_time_seconds += time_delta.total_seconds()
    return total_time_seconds

def idle_time_duration(date_time_vals=[], speed_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0 and speed_vals != None and len(speed_vals) > 0):
        return (True,str(datetime.timedelta(seconds=idle_time_seconds(date_time_vals, speed_vals))))
    else:
        return (False, 'EMPTY DATA')
    
def idle_time_seconds(date_time_vals=[], speed_vals=[]):
    start_date_time = date_time_vals[0]
    end_date_time = date_time_vals[-1]
    total_seconds = (end_date_time - start_date_time).total_seconds()
    return total_seconds - running_time_seconds(date_time_vals, speed_vals)

def idle_time_between_duration(startIndex, endIndex, date_time_vals=[], speed_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0 and speed_vals != None and len(speed_vals) > 0):
        return (True,str(datetime.timedelta(seconds=idle_time_between_seconds(startIndex, endIndex, date_time_vals, speed_vals))))
    else:
        return (False, 'EMPTY DATA')
    
def idle_time_between_seconds(startIndex, endIndex, date_time_vals=[], speed_vals=[]):
    start_date_time = date_time_vals[startIndex]
    end_date_time = date_time_vals[endIndex]
    total_seconds = (end_date_time - start_date_time).total_seconds()
    return total_seconds - running_time_between_seconds(startIndex, endIndex, date_time_vals, speed_vals)

def idle_time_percent(date_time_vals=[], speed_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0 and speed_vals != None and len(speed_vals) > 0):
        start_date_time = date_time_vals[0]
        end_date_time = date_time_vals[-1]
        total_seconds = (end_date_time - start_date_time).total_seconds()
        idle_time_sec = idle_time_seconds(date_time_vals, speed_vals)
        percent = round((idle_time_sec/total_seconds)*100, 2)
        return (True, str(percent))
    else:
        return (False, 'EMPTY DATA')

def idle_time_between_percent(startIndex, endIndex, date_time_vals=[], speed_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0 and speed_vals != None and len(speed_vals) > 0):
        start_date_time = date_time_vals[startIndex]
        end_date_time = date_time_vals[endIndex]
        total_seconds = (end_date_time - start_date_time).total_seconds()
        idle_time_sec = idle_time_between_seconds(startIndex, endIndex, date_time_vals, speed_vals)
        percent = round((idle_time_sec/total_seconds)*100, 2)
        return (True, str(percent))
    else:
        return (False, 'EMPTY DATA')
    
def range_time_seconds(date_time_vals=[], speed_vals=[], speed_from=0.0, speed_to=0.0):
    total_time_seconds = 0
    for i, date_time_val in enumerate(date_time_vals):
        if(i > 0):
            if(speed_vals[i-1]>speed_from and speed_vals[i-1] <= speed_to):
                time_delta = (date_time_val - date_time_vals[i-1])
                total_time_seconds += time_delta.total_seconds()
    return total_time_seconds

def range_distance(inst_dist_vals=[], speed_vals=[], speed_from=0.0, speed_to=0.0):
    range_cum_dist = 0.0
    for i, inst_dist_val in enumerate(inst_dist_vals):
            if(speed_vals[i]>speed_from and speed_vals[i] <= speed_to):
                range_cum_dist += inst_dist_val
    return range_cum_dist

def spm_start_end_datetime(date_time_vals=[]):
    if(date_time_vals != None and len(date_time_vals) > 0):
        date_time_format = '%d/%m/%Y %H:%M:%S'
        return (True, date_time_vals[0].strftime(date_time_format), date_time_vals[-1].strftime(date_time_format))
    else:
        return (False, 'EMPTY DATA', 'EMPTY DATA')

def isCurrentPresent(current_vals=[]):
    isCurrentPresent = False
    for current_val in current_vals:
        if(current_val != 0.0):
            isCurrentPresent = True

    return isCurrentPresent

def isVoltagePresent(voltage_vals=[]):
    isVoltagePresent = False
    for voltage_val in voltage_vals:
        if(voltage_val != 0.0):
            isVoltagePresent = True
    
    return isVoltagePresent

def avg_current(current_vals=[]):
    avg_current = sum(current_vals)/len(current_vals) if len(current_vals) != 0 else 0.0
    return str(round(avg_current, 2))

def max_current(current_vals=[]):
    max_current = max(current_vals) if len(current_vals) != 0 else 0.0
    return str(round(max_current,2))

def min_current(current_vals=[]):
    min_current = min(current_vals) if len(current_vals) != 0 else 0.0
    return str(round(min_current,2))

def avg_voltage(voltage_vals=[]):
    avg_voltage = sum(voltage_vals)/len(voltage_vals) if len(voltage_vals) != 0 else 0.0
    return str(round(avg_voltage, 2))

def max_voltage(voltage_vals=[]):
    max_voltage = max(voltage_vals) if len(voltage_vals) != 0 else 0.0
    return str(round(max_voltage,2))

def min_voltage(voltage_vals=[]):
    min_voltage = min(voltage_vals) if len(voltage_vals) != 0 else 0.0
    return str(round(min_voltage,2))

def cum_halt_energy(haltEnergy_vals=[]):
    isHaltEnergyPresent = False
    cum_halt_energy = 0.0
    if(len(haltEnergy_vals) > 1):
        cum_halt_energy = haltEnergy_vals[-1] - haltEnergy_vals[0]
        if(cum_halt_energy != 0.0):
            isHaltEnergyPresent = True

    return cum_halt_energy, isHaltEnergyPresent

def cum_run_energy(runEnergy_vals=[]):
    isRunEnergyPresent = False
    cum_run_energy = 0.0
    if(len(runEnergy_vals) > 1):
        cum_run_energy = runEnergy_vals[-1] - runEnergy_vals[0]
        if(cum_run_energy != 0.0):
            isRunEnergyPresent = True

    return cum_run_energy, isRunEnergyPresent

def cum_total_energy(totalEnergy_vals=[]):
    isTotalEnergyPresent = False
    cum_total_energy = 0.0
    if(len(totalEnergy_vals) > 1):
        cum_total_energy = totalEnergy_vals[-1] - totalEnergy_vals[0]
        if(cum_total_energy != 0.0):
            isTotalEnergyPresent = True

    return cum_total_energy, isTotalEnergyPresent

def calculate_sec(total_energy, load_str, cum_distance_km):
    sec = 'NA'
    try:
        load_float = float(load_str.strip()) if load_str != None and load_str.strip() != '' else 0.0
        if(load_float != 0.0 and cum_distance_km != 0.0):
            sec = str(round((total_energy * 1000)/(load_float * cum_distance_km), 2))
    except ValueError:
        pass

    return sec



