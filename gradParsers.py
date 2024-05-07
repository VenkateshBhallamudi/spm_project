import os
from pandas import *
from spmDataClasses import Gradient

def compute_y2(x1=0.0, x2=0.0, y1=0.0, slope=0, direction='LEVEL'):
    slope_mul = 1
    direction_val = direction.strip().upper()
    if direction_val == '' or direction_val.startswith('L'):
        slope_mul = 0
    elif direction_val.startswith('F'):
        slope_mul = -1
    else:
        slope_mul = 1
    offset = slope_mul*slope*(x2-x1)
    y2 = y1 + offset
    return y2

def output_gradient_csv(fileName, gradientRecords):
    out_file = open(fileName, 'w')
    csv_header = 'From,To,Direction,Gradient\n'
    out_lines = []
    out_lines.append(csv_header)
    for gradientRecord in gradientRecords:
        #print(str(gradientRecord))
        out_line = str(gradientRecord.from_km) + ',' + str(gradientRecord.to_km) + ',' + gradientRecord.direction + ',' + str(gradientRecord.gradient) + '\n'
        out_lines.append(out_line)
    #Output
    out_file.writelines(out_lines)
    out_file.close()

def filter_gradients(from_list=[], to_list=[], direction_list=[], gradient_list=[], startKm=0.0, direction='DOWN', multiplier=1):
    gradient_records = []
    for i in range(len(from_list)):
        from_list[i] = from_list[i] - startKm
        to_list[i] = to_list[i] - startKm

        if direction == 'UP':
            if(from_list[i] > 0):
                from_list[i] = 0
            if(to_list[i] > 0):
                to_list[i] = 0

        if direction == 'DOWN':
            if(from_list[i] < 0):
                from_list[i] = 0
            if(to_list[i] < 0):
                to_list[i] = 0

        if(not(from_list[i] == 0 and to_list[i] == 0)):
            from_km = round(abs(from_list[i]),2)
            to_km = round(abs(to_list[i]),2)
            direction_val = direction_list[i]
            if(from_km > to_km):
                temp = from_km
                from_km = to_km
                to_km = temp
                if(direction_list[i] == 'RISE'):
                    direction_val = 'FALL'
                elif(direction_list[i] == 'FALL'):
                    direction_val = 'RISE'

            gradient_record = Gradient(from_km=from_km*multiplier, to_km=to_km*multiplier, direction=direction_val, gradient=gradient_list[i])
            gradient_records.append(gradient_record)
    
    return sorted(gradient_records)

def plot_gradient(axis, plotColor='tab:olive', multiplier=1000, gradientRecords=[]):
    from_list = [gradientRecord.from_km for gradientRecord in gradientRecords]
    to_list = [gradientRecord.to_km for gradientRecord in gradientRecords]
    direction_list = [gradientRecord.direction for gradientRecord in gradientRecords]
    gradient_list = [gradientRecord.gradient for gradientRecord in gradientRecords]

    x_vals = [from_list[0]]
    y_vals = [0.0]

    for i, from_val in enumerate(from_list):
        x_current = x_vals[-1]
        y_current = y_vals[-1]
        x_next = x_current + ((to_list[i] - from_val))
        gradient_val = 0.0
        slope_val = 0.0
        try:
            gradient_val = float(gradient_list[i])
        except ValueError:
            print("LEVEL")

        if(gradient_val != 0.0):
            slope_val = 1/gradient_val
        
        direction_val = direction_list[i].strip()
        y_next = compute_y2(x1=x_current, x2=x_next, y1=y_current, slope=slope_val, direction=direction_val)
        x_vals.append(x_next)
        y_vals.append(y_next)
        #print('{} -> {}, {}, {}, {}:::{}, {}, {}, {}'.format(i, from_val, to_list[i], gradient_list[i], direction_list[i].strip(), x_current, y_current, x_next, y_next))

    x_plot_vals = [x_val*multiplier for x_val in x_vals]
    y_plot_vals = [y_val*multiplier for y_val in y_vals]
    axis.plot(x_plot_vals, y_plot_vals, color=plotColor)
    return (x_plot_vals, y_plot_vals)

def gradientParser(fileName, startKm, cum_distance, direction):
    data = read_csv(fileName)
    
    from_list_csv = data['From'].tolist()
    to_list_csv = data['To'].tolist()
    direction_list_csv = data['Direction'].tolist()
    gradient_list_csv = data['Gradient'].tolist()

    min_km = min(from_list_csv[0], from_list_csv[-1], to_list_csv[0], to_list_csv[-1])
    max_km = max(from_list_csv[0], from_list_csv[-1], to_list_csv[0], to_list_csv[-1])
    gradient_records = []
    return_gradient_records = []

    if(startKm >= min_km and startKm <= max_km):
        #print(len(from_list_csv))
        gradient_records = filter_gradients(from_list_csv, to_list_csv, direction_list_csv, gradient_list_csv, startKm, direction)
        for gradientRecord in gradient_records:
            if(gradientRecord.from_km > cum_distance):
                gradientRecord.from_km = cum_distance
            if(gradientRecord.to_km > cum_distance):
                gradientRecord.to_km = cum_distance
            
            if(not(gradientRecord.from_km == cum_distance and gradientRecord.to_km == cum_distance)):
                return_gradient_records.append(gradientRecord)
    else:
        print('Start Km out of bounds in gradient data')

    return return_gradient_records

if __name__ == '__main__':
    #323.7, 275.6, 0.0824, -0.0824
    #gradientRecords = gradientParser("D:/Pydir/Map Files/Gradient.csv", 300, 30, 'UP')
    #output_gradient_csv('D:/Pydir/Map Files/GradientFiltered.csv',gradientRecords)
    #plot_gradient(axis=ax2, plotColor=color, multiplier=1000, gradientRecords=gradientRecords)
    #plot_gradient(gradientRecords)
    path = str(os.getcwd()) + '\\spm_project\\railwaylogo.ico'
    print((str(os.getcwd()) + '\\spm_project\\railwaylogo.ico').replace('\\', '/'))