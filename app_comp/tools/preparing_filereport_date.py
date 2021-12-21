import pprint
import re


def select_unique_component(read_object: bytes, pcb_name):
    """
    :param read_object: byte str geted from file_report 
    example:
           b'Count;ComponentName;RefDes;PatternName;Value\r\n;;;;\r\n6;C_SMD_0805;C1;SMD_0805;0.1 mkF 50V X7R\r\n
    :pcb_name: name PCB with version (psb+_vers) (pu_v1.2)   
    
    return list:        
        [psb_name, {value1:{
                        count:N, ComponentName:name, RefDes:rd, PatternName:pn },
                    value2:{
                        count:N, ComponentName:name, RefDes:rd, PatternName:pn }
            }]
    example:
        ['U160TRANS-2.0', {'10MR 0.25W': {
                                        'Count':'4', 
                                        'ComponentName':'R_SMD_1210_M', 
                                        'RefDes': 'R7',
                                        'PatternName': 'R_SMD_1210_M'}
            }]
    """
    list_read_object = read_object.split(b'\r\n')   # get every component
    list_read_object = [field.decode('utf-8').split(';') for field in list_read_object]
    column_name = list_read_object[0]
    pcb_values = dict()
    for field in list_read_object[1:]:
        # count(field[0]) not empty and value(field[-1]) != nm and not empty
        if field[0] and field[-1] and field[-1].lower() not in ('nm', 'not mount'):
            pcb_values[field[-1]] = {column_name[i]: field[i] for i in range(len(column_name)-1)}
    return [pcb_name, pcb_values]    


def define_category(refdes, map_rdcateg:dict):
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


def define_pattern(pcb_pattern:str, category:str) -> str:
    if category == "capacitor" or category == "resistor":
        smd = re.search(r'SMD.?[08512635]{4}', pcb_pattern.upper())
        if smd:
            smd = smd.group()[:3] + '_' + smd.group()[-4:]
            return smd
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
    if category == "capacitor" or category == "resistor":    # R or C
        value_pcb = re.split(r'[-\s]', value_pcb)
        
        if re.search(r'F|R', value_pcb[0]):
            out_value['value'] = value_pcb.pop(0)
        elif re.search(r'F|R', value_pcb[1]):
            out_value['value'] = value_pcb[0] + value_pcb[1]
            del value_pcb[0:2]
        elif category == "resistor" and not re.search(r'R', value_pcb[0]):
            out_value['value'] = value_pcb.pop(0) + 'R'
        else:
            pass    # todo? return error
           
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
                out_value['comment'] = f"{out_value['comment']}; {value_pcb[i]}"

    else:      # VD, VT, DD, etc.
        value_pcb = value_pcb.split()
        out_value['value'] = value_pcb.pop(0).upper()        
        if value_pcb and len(value_pcb) > 1:
                for i in range(len(value_pcb)):
                    out_value['comment'] = f"{out_value['comment']}{value_pcb[i]}; "
                else:
                    out_value['comment'] = value_pcb[0]
    return out_value


def parsing_one_component(key_value: str, component_pcb: dict, map_rdcateg: dict):
    out_comp = {'value': '',
            'tolerance': '',
            'voltage': '',
            'power': '',
            'comment': '',
            'count': '',
            'pattern_name': '',
            'category_name': '' }
    out_comp['category_name'] = define_category(component_pcb['RefDes'], map_rdcateg)    
    if out_comp['category_name'][:8] == 'Category':
        return out_comp['category_name']     # 'Category with Refdes:{} not exist'
    out_comp['count'] = define_count(component_pcb['Count'])
    out_comp['pattern_name'] = define_pattern(component_pcb['PatternName'], out_comp['category_name'])
    
    out_value = define_value(key_value, out_comp['category_name'])
    out_comp["value"] = out_value['value']
    out_comp["tolerance"] = out_value['tolerance']
    out_comp["voltage"] = out_value['voltage']
    out_comp["power"] = out_value['power']
    out_comp["comment"] = out_value['comment']
    print(out_comp)
    return out_comp


def parsing_components(component_pcb: dict, map_rdcateg: dict) -> list:
    """
    :param component_pcb: {value: {parameters}} --> output "select_unique_component()"
    :return:  {value, tolerance, voltage, power, comment, count, pattern_name, category_name} 
    """
    pcboard = component_pcb[0]
    component_pcb = component_pcb[1]
    return [parsing_one_component(k, component_pcb[k], map_rdcateg) for k in component_pcb.keys()]


if __name__ == "__main__":

    pcb_name = "pu"+'v1.2'
    getbin = b'''Count;ComponentName;RefDes;PatternName;Value\r\n;;;;\r\n6;C_SMD_0805;C1;SMD_0805;0.1 mkF 50V X7R\r\n;C_SMD_0805;C2;SMD_0805;0.1 mkF 50V X7R\r\n;C_SMD_0805;C7;SMD_0805;0.1mkF 50V X7R\r\n;C_SMD_0805;C22;SMD_0805;0.1 mkF 50V X7R\r\n;C_SMD_0805;C25;SMD_0805;0.1 mkF 50V X7R\r\n;C_SMD_0805;C26;SMD_0805;0.1 mkF 50V X7R\r\n;C_SMD_0805;C8;SMD_0805;0.1 mkF-10%\r\n;C_SMD_0805;C9;SMD_0805;0.1 mkF-10%\r\n;C_SMD_0805;C14;SMD_0805;0.1 mkF-10%\r\n;C_SMD_0805;C15;SMD_0805;0.1 mkF-10%\r\n2;R_SMD1206;R55;SMD1206;1kR\r\n;R_SMD1206;R56;SMD1206;1kR\r\n1;TYCO 796636-3;XPU5;WIRE_TO_BOARD_3_5.08;2EDGV-5.08-3 + 2EDGK-5.08-3\r\n6;C_SMD_0805;C10;C_SMD_0805;4.7mkF-10%\r\n;C_SMD_0805;C11;C_SMD_0805;4.7mkF-10%\r\n;C_SMD_0805;C12;C_SMD_0805;4.7mkF-10%\r\n;C_SMD_0805;C13;C_SMD_0805;4.7mkF-10%\r\n;C_SMD_0805;C16;C_SMD_0805;4.7mkF-10%\r\n;C_SMD_0805;C17;C_SMD_0805;4.7mkF-10%\r\n2;R_SMD_0805;R8;R_SMD_0805;5.1k-5%\r\n;R_SMD_0805;R12;R_SMD_0805;5.1k-5%\r\n6;R_SMD_0805;R5;R_SMD_0805;10-5%\r\n;R_SMD_0805;R6;R_SMD_0805;10-5%\r\n;R_SMD_0805;R7;R_SMD_0805;10-5%\r\n;R_SMD_0805;R9;R_SMD_0805;10-5%\r\n;R_SMD_0805;R10;R_SMD_0805;10-5%\r\n;R_SMD_0805;R11;R_SMD_0805;10-5%\r\n4;CAP ALUM D=6H=12;C3;AL-0612;22uF\r\n;CAP ALUM D=6 H=12;C6;AL-0612;22uF\r\n;CAP ALUM D=6 H=12;C27;AL-0612;22uF\r\n;CAP ALUM D=6 H=12;C28;AL-0612;22uF\r\n2;R_SMD_0805;R22;R_SMD_0805;100-5%\r\n;R_SMD_0805;R25;R_SMD_0805;100-5%\r\n2;LQH32CNXX;L2;LQH32CNXX;240R\r\n;LQH32CNXX;L3;LQH32CNXX;240R\r\n2;C_SMD_0805;C29;C_SMD_0805;270pF-10%  16V-X7R-\r\n;C_SMD_0805;C30;C_SMD_0805;270pF-10%  16V-X7R-\r\n4;R_SMD_0805;R21;R_SMD_0805;560-5%\r\n;R_SMD_0805;R23;R_SMD_0805;560-5%\r\n;R_SMD_0805;R24;R_SMD_0805;560-5%\r\n;R_SMD_0805;R26;R_SMD_0805;560-5%\r\n2;ADM2483BRW;DD1;SOIC-16W;ADM2483\r\n;ADM2483BRW;DD2;SOIC-16W;ADM2483\r\n2;DLW31SNXXXSQ2;L5;DLW31S;DLW31SN601SQ2\r\n;DLW31SNXXXSQ2;L7;DLW31S;DLW31SN601SQ2\r\n2;AM4T-24XXS;DA1;AM3T-2415DNZ;FDD03-05S2\r\n;AM4T-24XXS;DA10;AM3T-2415DNZ;FDD03-05S2\r\n2;KP-2012XXX;VD6;LED_0805;GREEN\r\n;KP-2012XXX;VD7;LED_0805;GREEN\r\n2;LQH32CNXX;L4;LQH32CNXX;LQH32CN220K23L\r\n;LQH32CNXX;L6;LQH32CNXX;LQH32CN220K23L\r\n2;MBR05XX;VD26;SOD-123;MBR0560\r\n;MBR05XX;VD27;SOD-123;MBR0560\r\n6;CPC1035N;DA2;CPC1035N;not mount\r\n;CPC1035N;DA3;CPC1035N;not mount\r\n;CPC1035N;DA6;CPC1035N;not mount\r\n;CPC1035N;DA7;CPC1035N;not mount\r\n;CPC1035N;DA8;CPC1035N;not mount\r\n;CPC1035N;DA9;CPC1035N;not mount\r\n4;C_SMD_0805;C18;C_SMD_0805;not mount\r\n;C_SMD_0805;C19;C_SMD_0805;not mount\r\n;C_SMD_0805;C20;C_SMD_0805;not mount\r\n;C_SMD_0805;C21;C_SMD_0805;not mount\r\n4;C_SMD_1808;C4;C_SMD_1808;Not Mount\r\n;C_SMD_1808;C5;C_SMD_1808;Not Mount\r\n;C_SMD_1808;C23;C_SMD_1808;Not Mount\r\n;C_SMD_1808;C24;C_SMD_1808;Not Mount\r\n6;KP-2012XXX;VD22;LED_0805;not mount\r\n;KP-2012XXX;VD23;LED_0805;not mount\r\n;KP-2012XXX;VD24;LED_0805;not mount\r\n;KP-2012XXX;VD25;LED_0805;not mount\r\n;KP-2012XXX;VD32;LED_0805;not mount\r\n;KP-2012XXX;VD33;LED_0805;not mount\r\n2;MMBT3904;VT1;MMBT3904;not mount\r\n;MMBT3904;VT2;MMBT3904;not mount\r\n8;PMLL4148L;VD2;SOD80C;not mount\r\n;PMLL4148L;VD3;SOD80C;not mount\r\n;PMLL4148L;VD8;SOD80C;not mount\r\n;PMLL4148L;VD9;SOD80C;not mount\r\n;PMLL4148L;VD28;SOD80C;not mount\r\n;PMLL4148L;VD29;SOD80C;not mount\r\n;PMLL4148L;VD30;SOD80C;not mount\r\n;PMLL4148L;VD31;SOD80C;not mount\r\n8;R_SMD1206;R35;SMD1206;not mount\r\n;R_SMD1206;R38;SMD1206;not mount\r\n;R_SMD1206;R40;SMD1206;not mount\r\n;R_SMD1206;R42;SMD1206;not mount\r\n;R_SMD1206;R44;SMD1206;not mount\r\n;R_SMD1206;R46;SMD1206;not mount\r\n;R_SMD1206;R48;SMD1206;not mount\r\n;R_SMD1206;R50;SMD1206;not mount\r\n24;R_SMD_0805;R1;R_SMD_0805;not mount\r\n;R_SMD_0805;R2;R_SMD_0805;not mount\r\n;R_SMD_0805;R13;R_SMD_0805;not mount\r\n;R_SMD_0805;R14;R_SMD_0805;not mount\r\n;R_SMD_0805;R17;R_SMD_0805;not mount\r\n;R_SMD_0805;R18;R_SMD_0805;not mount\r\n;R_SMD_0805;R27;R_SMD_0805;not mount\r\n;R_SMD_0805;R28;R_SMD_0805;not mount\r\n;R_SMD_0805;R29;R_SMD_0805;not mount\r\n;R_SMD_0805;R30;R_SMD_0805;not mount\r\n;R_SMD_0805;R31;R_SMD_0805;not mount\r\n;R_SMD_0805;R32;R_SMD_0805;not mount\r\n;R_SMD_0805;R33;R_SMD_0805;not mount\r\n;R_SMD_0805;R34;R_SMD_0805;not mount\r\n;R_SMD_0805;R36;R_SMD_0805;not mount\r\n;R_SMD_0805;R37;R_SMD_0805;not mount\r\n;R_SMD_0805;R39;R_SMD_0805;not mount\r\n;R_SMD_0805;R41;R_SMD_0805;not mount\r\n;R_SMD_0805;R43;R_SMD_0805;not mount\r\n;R_SMD_0805;R45;R_SMD_0805;not mount\r\n;R_SMD_0805;R47;R_SMD_0805;not mount\r\n;R_SMD_0805;R49;R_SMD_0805;not mount\r\n;R_SMD_0805;R51;R_SMD_0805;not mount\r\n;R_SMD_0805;R52;R_SMD_0805;not mount\r\n2;SMAJXXCA;VD12;SMA;not mount\r\n;SMAJXXCA;VD13;SMA;not mount\r\n1;TYCO 796636-4;XPU3;WIRE_TO_BOARD_4_5.08;not mount\r\n1;TYCO 796636-6;XPU4;WIRE_TO_BOARD_6_5.08;not mount\r\n2;PE-65855;L1;PE-65855;PE-65855\r\n;PE-65855;L8;PE-65855;PE-65855\r\n2;90663-1101;XPU1;90663-1101;SCM-10\r\n;90663-1101;XPU2;90663-1101;SCM-10\r\n6;SMAJXXCA;VD16;SMA;SMAJ5CA\r\n;SMAJXXCA;VD17;SMA;SMAJ5CA\r\n;SMAJXXCA;VD18;SMA;SMAJ5CA\r\n;SMAJXXCA;VD19;SMA;SMAJ5CA\r\n;SMAJXXCA;VD20;SMA;SMAJ5CA\r\n;SMAJXXCA;VD21;SMA;SMAJ5CA\r\n1;SS24;VD1;SMA;SS24\r\n1;HY-STM32V;M1;HY-STM32V;\r\n2;JMP3;J1;JMP_3;\r\n;JMP3;J2;JMP_3;\r\n'''
    
    map_rc={'C': 'capacitor', 'R': 'resistor', 'ZQ': 'quartz', 'L': 'inductance', 'VD': 'diode', 'VT': 'transistor', 'DA': 'integrated circuit analog', 'DD': 'integrated circuit digital', 'X': 'connector'}
    suc = select_unique_component(getbin, pcb_name)
    print(suc)
    #ksuc = list(suc[1].keys())
    #print(ksuc)
    
    #cat = ["capacitor", "resistor", 'none']
    #pval = define_value(ksuc[13], cat[2])    
    #print(pval)
    
    #for i in suc:
        #pprint.pprint(i)        
 
    out = parsing_components(suc, map_rc)
    print(out)
    for i in out:
        pprint.pprint(i['value'])    
