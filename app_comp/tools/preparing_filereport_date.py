import pprint
import re


def select_unique_component(read_object: bytes, pcb_name):
    """
    :param read_object: byte str geted from file_report 
    example:
           b'Count;;RefDes;PatternName;Value\r\n;;;;\r\n6;;C1;SMD_0805;0.1 mkF 50V X7R\r\n
    :pcb_name: name PCB with version (psb+_vers) (pu_v1.2)   
    
    return list:        
        [psb_name, {value1:{
                        count:N, RefDes:rd, PatternName:pn },
                    value2:{
                        count:N, RefDes:rd, PatternName:pn }
            }]
    example:
        ['U160TRANS-2.0', {'10MR 0.25W': {
                                        'Count':'4',
                                        'RefDes': 'R7',
                                        'PatternName': 'R_SMD_1210_M'}
            }]
    """
    list_read_object = read_object.split(b'\r\n')  # get every component
    list_read_object = [field.decode('utf-8').split(';') for field in list_read_object]
    column_name = list_read_object[0]
    pcb_values = dict()
    for field in list_read_object[1:]:
        # count(field[0]) not empty and value(field[-1]) != nm and not empty
        if field[0] and field[-1] and field[-1].lower() not in ('nm', 'not mount'):
            pcb_values[field[-1]] = {column_name[i]: field[i] for i in range(len(column_name) - 1)}
    return [pcb_name, pcb_values]


def define_category(refdes, map_rdcateg: dict):
    """
    :param refdes: "C12", 'VD33' ets.
    :param map_rdcateg: {rd:cat} get from db
    :return:  category
    """
    rd = filter(lambda x: x.isalpha(), refdes)
    rd = ''.join(rd).upper()
    if re.search(r'X', rd) or rd == 'J':
        rd = 'X'
    elif rd == 'ZD':
        rd = 'VD'

    if rd in map_rdcateg.keys():
        return map_rdcateg[rd]
    else:
        return f'Category with Refdes:{rd} not exist'


def define_pattern(pcb_pattern: str, category: str) -> str:
    if category == "capacitor" or category == "resistor":
        smd = re.search(r'SMD.?[08512635]{4}', pcb_pattern.upper())
        if smd:
            return smd.group()[:3] + '_' + smd.group()[-4:]
        else:
            return pcb_pattern
    else:
        return pcb_pattern


def define_count(count):
    if count:
        return int(count.strip())
    else:
        return 0


def define_value(value_pcb: str, category: str) -> dict:
    """
    :param value_pcb:  example: '0.1mkF 50V X7R', 'MBR0560', '5.1k-5%'
    :param category:   example: 'capacitor",     'diode',  'resistor'
    :return: {value, tolerance,voltage,power,comment}
    """
    out_value = {"value": '', "tolerance": '', 'voltage': '', "power": '', "comment": '', }
    value_pcb = value_pcb.replace(',', '.')
    if category == "capacitor" or category == "resistor":  # R or C
        value_pcb = re.split(r'[-\s]', value_pcb)

        if re.search(r'F|R', value_pcb[0]):
            out_value['value'] = value_pcb.pop(0)
        elif re.search(r'F|R', value_pcb[1]):
            out_value['value'] = value_pcb[0] + value_pcb[1]
            del value_pcb[0:2]
        elif category == "resistor" and not re.search(r'R', value_pcb[0]):
            out_value['value'] = value_pcb.pop(0) + 'R'
        else:
            pass  # todo? return error

        for v in value_pcb:
            if re.match(r'[0-9]+V', v.upper()):
                out_value['voltage'] = v.upper()
                value_pcb.remove(v)
            elif re.match(r'[0-9]+%', v):
                out_value['tolerance'] = v
                value_pcb.remove(v)
            elif re.match(r'[0-9]+W', v.upper()):
                out_value['power'] = v.upper()
                value_pcb.remove(v)

        if value_pcb:
            for i in range(len(value_pcb)):
                out_value['comment'] = f"{out_value['comment']}{value_pcb[i]}; "
    else:   # VD, VT, DD, etc.
        value_pcb = value_pcb.split()
        out_value['value'] = value_pcb.pop(0).upper()
        if value_pcb:
            for i in range(len(value_pcb)):
                out_value['comment'] = f"{out_value['comment']}{value_pcb[i]}; "

    return out_value


def parsing_one_component(key_value: str, params_comp_pcb: dict, map_rdcateg: dict) -> dict:
    """
    :param key_value: it`s 'value_pcb' example: '0.1 mkF 50V X7R'
    :param params_comp_pcb: dictionary: {Count;ComponentName;RefDes;PatternName}
    :param map_rdcateg: get from DB {'RefDes':'categ', ... }
    :return: dictionary
    """
    category = define_category(params_comp_pcb['RefDes'], map_rdcateg)
    if category[:8] == 'Category':
        return category  # 'Category with Refdes:{} not exist'
    out_value = define_value(key_value, category)
    return {'value': out_value['value'],
            'tolerance': out_value['tolerance'],
            'voltage': out_value['voltage'],
            'power': out_value['power'],
            'comment': out_value['comment'],
            'count': define_count(params_comp_pcb['Count']),
            'pattern_name': define_pattern(params_comp_pcb['PatternName'], category),
            'category_name': category}


def parsing_components(component_pcb: dict, map_rdcateg: dict) -> list:
    """
    :param component_pcb: {value: {parameters}} --> output "select_unique_component()"
    :param map_rdcateg: get from DB {'RefDes':'categ', ... }
    :return:  [{value:'some', tolerance:'', ... category_name}, {value:'some', tolerance, ... category_name}]
    """
    return [parsing_one_component(k, component_pcb[k], map_rdcateg) for k in component_pcb.keys()]


if __name__ == "__main__":
    pass
    # test.py --> TestParsReportFile
