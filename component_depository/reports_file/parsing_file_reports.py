import csv
import os
import sys
import pprint


path_to_files = r'./' 


def find_file(path = path_to_files, type_file="csv"):
    """select file with expansion (type_file) default=.csv
    return list of all files"""    
    lfile_ = [File for File in os.listdir(path) if File.endswith(f'.{type_file}')]
    # D={k:v for(k,v) in zip(range(1,(len(lfile)+1)),lfile)} # файлы с заданными ключами
    return lfile_


def select_unic_component(readed_object, pcb_name) -> dict:
    """
    return list:
        
        [psb_name, {value1:{
                        count:N, ComponentName:name, RefDes:rd, PatternName:pn },
                    value2:{
                        count:N, ComponentName:name, RefDes:rd, PatternName:pn }
            }]
    exmple:
        ['U160TRANS-2.0', {'10MR 0.25W': {
                                        'Count':'4', 
                                        'ComponentName':'R_SMD_1210_M', 
                                        'RefDes': 'R7',
                                        'PatternName': 'R_SMD_1210_M'}
            }]
    """
    
    col_name = readed_object.__next__()
    readed_object.__next__() # skip empty line
    print(col_name)
    pcb_values = dict()
    for field in readed_object:
        if field[0] and field[-1].lower() != 'nm' and field[-1].lower() != 'not mount':  # count not empty and value != nm
            pcb_values[field[-1]] = {col_name[i]: field[i] for i in range(len(col_name)-1)}
    return [pcb_name, pcb_values]


def refdes_to_cat():
    pass

def parsing_value(): 
    """
    return: value, tolerance, voltage, power"""
    pass


def preparation_components(pcb_components:dict):
    """comps: dict
    {value1:{
          count:N, ComponentName:name, RefDes:rd, PatternName:pn },
    value2:{
        count:N, ComponentName:name, RefDes:rd, PatternName:pn }
    
    """
    for comp in pcb_components:
        category = refdes_to_cat()
        count = pass # todo
        pattern = pass # todo
        value, tolerance, voltage, power = parsing_value
        
    

if __name__ == "__main__":
    report_file = find_file()[0]
    print(report_file[:-4])		# breack ".pcb"
    with open(report_file, newline='', encoding='utf-8', ) as object_csv:
        rowreader = csv.reader(object_csv,  delimiter=';')
        try:
            pcb_object = select_unic_component(rowreader, report_file[:-4])
        except csv.Error as e:
            sys.exit(f'file {report_file}, line {rowreader.line_num}: {e}')
        
        pprint.pprint(pcb_object)
