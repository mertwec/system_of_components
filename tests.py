import sys
import unittest
from app_comp import db, abs_path
from app_comp.models import temp_bd, \
                            Category, \
                            Pattern, \
                            Component, \
                            PCBoard, \
                            AssociatedCompPcb
# from app_comp.tools import database_tools as dt
from app_comp.tools import forms_validation as fv
import app_comp.tools.database_tools as dbt
import app_comp.tools.preparing_filereport_date as prepfr


def test_get_comps_from_cat(category, db=db):
    cfcat = dbt.get_components_from_category(db, category, Component)
    return cfcat


def test_add_comp_pcb():
    b1 = db.session.query(PCBoard).get(1)
    comp2 = db.session.query(Component).get(7)
    comp3 = db.session.query(Component).get(8)
    print(b1)
    print(comp2, '\n', comp3)
    ass1 = AssociatedCompPcb(comp_count=2, pcb_id=b1.id, comp_id=comp2.id)
    ass2 = AssociatedCompPcb(comp_count=2, pcb_id=b1.id, comp_id=comp3.id)
    db.session.add_all([ass1, ass2])
    print(db.session.new)
    db.session.commit()
    print('done')


def test_get_pcb():
    pcbs = db.session.query(PCBoard).get(1)
    print(pcbs)
    for i in pcbs.components:
        print(i.component.get_parameters_as_dict())


def test_get_pcb_from_comp():
    c = db.session.query(Component).get(5)
    print(c)
    print(c.pcboards)
    for i in c.pcboards:
        print(i.pcb)
        print(i.component)



class TestParsReportFile(unittest.TestCase):
    pcb_name = "pu" + 'v1.2'
    getbin = b'Count;ComponentName;RefDes;PatternName;Value\r\n;;;;\r\n6;C_SMD_0805;C1;SMD_0805;0.1mkF 50V X7R\r\n;C_SMD_0805;C2;SMD_0805;0.1 mkF 50V X7R\r\n;C_SMD_0805;C7;SMD_0805;0.1 mkF 50V X7R\r\n;C_SMD_0805;C22;SMD_0805;0.1 mkF 50V X7R\r\n;C_SMD_0805;C25;SMD_0805;0.1 mkF 50V X7R\r\n;C_SMD_0805;C26;SMD_0805;0.1 mkF 50V X7R\r\n;C_SMD_0805;C9;SMD_0805;0.1 mkF-10%\r\n;C_SMD_0805;C14;SMD_0805;0.1 mkF-10%\r\n;C_SMD_0805;C15;SMD_0805;0.1 mkF-10%\r\n2;R_SMD1206;R55;SMD1206;1kR\r\n;R_SMD1206;R56;SMD1206;1kR\r\n1;TYCO 796636-3;XPU5;WIRE_TO_BOARD_3_5.08;2EDGV-5.08-3 + 2EDGK-5.08-3\r\n6;C_SMD_0805;C10;C_SMD_0805;4.7mkF-10%\r\n;C_SMD_0805;C11;C_SMD_0805;4.7mkF-10%\r\n;C_SMD_0805;C12;C_SMD_0805;4.7mkF-10%\r\n;C_SMD_0805;C13;C_SMD_0805;4.7mkF-10%\r\n;C_SMD_0805;C16;C_SMD_0805;4.7mkF-10%\r\n;C_SMD_0805;C17;C_SMD_0805;4.7mkF-10%\r\n2;R_SMD_0805;R8;R_SMD_0805;5.1k-5%\r\n;R_SMD_0805;R12;R_SMD_0805;5.1k-5%\r\n6;R_SMD_0805;R5;R_SMD_0805;10-5%\r\n;R_SMD_0805;R6;R_SMD_0805;10-5%\r\n;R_SMD_0805;R7;R_SMD_0805;10-5%\r\n;R_SMD_0805;R9;R_SMD_0805;10-5%\r\n;R_SMD_0805;R10;R_SMD_0805;10-5%\r\n;R_SMD_0805;R11;R_SMD_0805;10-5%\r\n4;CAP ALUM D=6 H=12;C3;AL-0612;22uF\r\n;CAP ALUM D=6 H=12;C6;AL-0612;22uF\r\n;CAP ALUM D=6 H=12;C27;AL-0612;22uF\r\n;CAP ALUM D=6 H=12;C28;AL-0612;22uF\r\n2;R_SMD_0805;R22;R_SMD_0805;100-5%\r\n;R_SMD_0805;R25;R_SMD_0805;100-5%\r\n2;LQH32CNXX;L2;LQH32CNXX;240R\r\n;LQH32CNXX;L3;LQH32CNXX;240R\r\n2;C_SMD_0805;C29;C_SMD_0805;270pF-10%  16V-X7R-\r\n;C_SMD_0805;C30;C_SMD_0805;270pF-10%  16V-X7R-\r\n4;R_SMD_0805;R21;R_SMD_0805;560-5%\r\n;R_SMD_0805;R23;R_SMD_0805;560-5%\r\n;R_SMD_0805;R24;R_SMD_0805;560-5%\r\n;R_SMD_0805;R26;R_SMD_0805;560-5%\r\n2;ADM2483BRW;DD1;SOIC-16W;ADM2483\r\n;ADM2483BRW;DD2;SOIC-16W;ADM2483\r\n2;DLW31SNXXXSQ2;L5;DLW31S;DLW31SN601SQ2\r\n;DLW31SNXXXSQ2;L7;DLW31S;DLW31SN601SQ2\r\n2;AM4T-24XXS;DA1;AM3T-2415DNZ;FDD03-05S2\r\n;AM4T-24XXS;DA10;AM3T-2415DNZ;FDD03-05S2\r\n2;KP-2012XXX;VD6;LED_0805;GREEN\r\n;KP-2012XXX;VD7;LED_0805;GREEN\r\n2;LQH32CNXX;L4;LQH32CNXX;LQH32CN220K23L\r\n;LQH32CNXX;L6;LQH32CNXX;LQH32CN220K23L\r\n2;MBR05XX;VD26;SOD-123;MBR0560\r\n;MBR05XX;VD27;SOD-123;MBR0560\r\n6;CPC1035N;DA2;CPC1035N;not mount\r\n;CPC1035N;DA3;CPC1035N;not mount\r\n;CPC1035N;DA6;CPC1035N;not mount\r\n;CPC1035N;DA7;CPC1035N;not mount\r\n;CPC1035N;DA8;CPC1035N;not mount\r\n;CPC1035N;DA9;CPC1035N;not mount\r\n4;C_SMD_0805;C18;C_SMD_0805;not mount\r\n;C_SMD_0805;C19;C_SMD_0805;not mount\r\n;C_SMD_0805;C20;C_SMD_0805;not mount\r\n;C_SMD_0805;C21;C_SMD_0805;not mount\r\n4;C_SMD_1808;C4;C_SMD_1808;Not Mount\r\n;C_SMD_1808;C5;C_SMD_1808;Not Mount\r\n;C_SMD_1808;C23;C_SMD_1808;Not Mount\r\n;C_SMD_1808;C24;C_SMD_1808;Not Mount\r\n6;KP-2012XXX;VD22;LED_0805;not mount\r\n;KP-2012XXX;VD23;LED_0805;not mount\r\n;KP-2012XXX;VD24;LED_0805;not mount\r\n;KP-2012XXX;VD25;LED_0805;not mount\r\n;KP-2012XXX;VD32;LED_0805;not mount\r\n;KP-2012XXX;VD33;LED_0805;not mount\r\n2;MMBT3904;VT1;MMBT3904;not mount\r\n;MMBT3904;VT2;MMBT3904;not mount\r\n8;PMLL4148L;VD2;SOD80C;not mount\r\n;PMLL4148L;VD3;SOD80C;not mount\r\n;PMLL4148L;VD8;SOD80C;not mount\r\n;PMLL4148L;VD9;SOD80C;not mount\r\n;PMLL4148L;VD28;SOD80C;not mount\r\n;PMLL4148L;VD29;SOD80C;not mount\r\n;PMLL4148L;VD30;SOD80C;not mount\r\n;PMLL4148L;VD31;SOD80C;not mount\r\n8;R_SMD1206;R35;SMD1206;not mount\r\n;R_SMD1206;R38;SMD1206;not mount\r\n;R_SMD1206;R40;SMD1206;not mount\r\n;R_SMD1206;R42;SMD1206;not mount\r\n;R_SMD1206;R44;SMD1206;not mount\r\n;R_SMD1206;R46;SMD1206;not mount\r\n;R_SMD1206;R48;SMD1206;not mount\r\n;R_SMD1206;R50;SMD1206;not mount\r\n24;R_SMD_0805;R1;R_SMD_0805;not mount\r\n;R_SMD_0805;R2;R_SMD_0805;not mount\r\n;R_SMD_0805;R13;R_SMD_0805;not mount\r\n;R_SMD_0805;R14;R_SMD_0805;not mount\r\n;R_SMD_0805;R17;R_SMD_0805;not mount\r\n;R_SMD_0805;R18;R_SMD_0805;not mount\r\n;R_SMD_0805;R27;R_SMD_0805;not mount\r\n;R_SMD_0805;R28;R_SMD_0805;not mount\r\n;R_SMD_0805;R29;R_SMD_0805;not mount\r\n;R_SMD_0805;R30;R_SMD_0805;not mount\r\n;R_SMD_0805;R31;R_SMD_0805;not mount\r\n;R_SMD_0805;R32;R_SMD_0805;not mount\r\n;R_SMD_0805;R33;R_SMD_0805;not mount\r\n;R_SMD_0805;R34;R_SMD_0805;not mount\r\n;R_SMD_0805;R36;R_SMD_0805;not mount\r\n;R_SMD_0805;R37;R_SMD_0805;not mount\r\n;R_SMD_0805;R39;R_SMD_0805;not mount\r\n;R_SMD_0805;R41;R_SMD_0805;not mount\r\n;R_SMD_0805;R43;R_SMD_0805;not mount\r\n;R_SMD_0805;R45;R_SMD_0805;not mount\r\n;R_SMD_0805;R47;R_SMD_0805;not mount\r\n;R_SMD_0805;R49;R_SMD_0805;not mount\r\n;R_SMD_0805;R51;R_SMD_0805;not mount\r\n;R_SMD_0805;R52;R_SMD_0805;not mount\r\n2;SMAJXXCA;VD12;SMA;not mount\r\n;SMAJXXCA;VD13;SMA;not mount\r\n1;TYCO 796636-4;XPU3;WIRE_TO_BOARD_4_5.08;not mount\r\n1;TYCO 796636-6;XPU4;WIRE_TO_BOARD_6_5.08;not mount\r\n2;PE-65855;L1;PE-65855;PE-65855\r\n;PE-65855;L8;PE-65855;PE-65855\r\n2;90663-1101;XPU1;90663-1101;SCM-10\r\n;90663-1101;XPU2;90663-1101;SCM-10\r\n6;SMAJXXCA;VD16;SMA;SMAJ5CA\r\n;SMAJXXCA;VD17;SMA;SMAJ5CA\r\n;SMAJXXCA;VD18;SMA;SMAJ5CA\r\n;SMAJXXCA;VD19;SMA;SMAJ5CA\r\n;SMAJXXCA;VD20;SMA;SMAJ5CA\r\n;SMAJXXCA;VD21;SMA;SMAJ5CA\r\n1;SS24;VD1;SMA;SS24\r\n1;HY-STM32V;M1;HY-STM32V;\r\n2;JMP3;J1;JMP_3;\r\n;JMP3;J2;JMP_3;\r\n'
    out_list = ['puv1.2', {'0.1mkF 50V X7R': {'Count': '6', 'ComponentName': 'C_SMD_0805', 'RefDes': 'C1', 'PatternName': 'SMD_0805'}, '1kR': {'Count': '2', 'ComponentName': 'R_SMD1206', 'RefDes': 'R55', 'PatternName': 'SMD1206'}, '2EDGV-5.08-3 + 2EDGK-5.08-3': {'Count': '1', 'ComponentName': 'TYCO 796636-3', 'RefDes': 'XPU5', 'PatternName': 'WIRE_TO_BOARD_3_5.08'}, '4.7mkF-10%': {'Count': '6', 'ComponentName': 'C_SMD_0805', 'RefDes': 'C10', 'PatternName': 'C_SMD_0805'}, '5.1k-5%': {'Count': '2', 'ComponentName': 'R_SMD_0805', 'RefDes': 'R8', 'PatternName': 'R_SMD_0805'}, '10-5%': {'Count': '6', 'ComponentName': 'R_SMD_0805', 'RefDes': 'R5', 'PatternName': 'R_SMD_0805'}, '22uF': {'Count': '4', 'ComponentName': 'CAP ALUM D=6 H=12', 'RefDes': 'C3', 'PatternName': 'AL-0612'}, '100-5%': {'Count': '2', 'ComponentName': 'R_SMD_0805', 'RefDes': 'R22', 'PatternName': 'R_SMD_0805'}, '240R': {'Count': '2', 'ComponentName': 'LQH32CNXX', 'RefDes': 'L2', 'PatternName': 'LQH32CNXX'}, '270pF-10%  16V-X7R-': {'Count': '2', 'ComponentName': 'C_SMD_0805', 'RefDes': 'C29', 'PatternName': 'C_SMD_0805'}, '560-5%': {'Count': '4', 'ComponentName': 'R_SMD_0805', 'RefDes': 'R21', 'PatternName': 'R_SMD_0805'}, 'ADM2483': {'Count': '2', 'ComponentName': 'ADM2483BRW', 'RefDes': 'DD1', 'PatternName': 'SOIC-16W'}, 'DLW31SN601SQ2': {'Count': '2', 'ComponentName': 'DLW31SNXXXSQ2', 'RefDes': 'L5', 'PatternName': 'DLW31S'}, 'FDD03-05S2': {'Count': '2', 'ComponentName': 'AM4T-24XXS', 'RefDes': 'DA1', 'PatternName': 'AM3T-2415DNZ'}, 'GREEN': {'Count': '2', 'ComponentName': 'KP-2012XXX', 'RefDes': 'VD6', 'PatternName': 'LED_0805'}, 'LQH32CN220K23L': {'Count': '2', 'ComponentName': 'LQH32CNXX', 'RefDes': 'L4', 'PatternName': 'LQH32CNXX'}, 'MBR0560': {'Count': '2', 'ComponentName': 'MBR05XX', 'RefDes': 'VD26', 'PatternName': 'SOD-123'}, 'PE-65855': {'Count': '2', 'ComponentName': 'PE-65855', 'RefDes': 'L1', 'PatternName': 'PE-65855'}, 'SCM-10': {'Count': '2', 'ComponentName': '90663-1101', 'RefDes': 'XPU1', 'PatternName': '90663-1101'}, 'SMAJ5CA': {'Count': '6', 'ComponentName': 'SMAJXXCA', 'RefDes': 'VD16', 'PatternName': 'SMA'}, 'SS24': {'Count': '1', 'ComponentName': 'SS24', 'RefDes': 'VD1', 'PatternName': 'SMA'}, '': {'Count': '2', 'ComponentName': 'JMP3', 'RefDes': 'J1', 'PatternName': 'JMP_3'}}]

    def setUp(self):
        print('_'*60+"\nTest module 'app_comp.tools.preparing_filereport_date'")

    def test_select_unique_component(self):
        self.assertEqual(self.out_list,
                         prepfr.select_unique_component(self.getbin, self.pcb_name),
                         'not correct select_unique_component from report file')

    def test_define_category(self):
        map_rc = dbt.map_refdes_category(db=db)
        cat = prepfr.define_category(refdes=self.out_list[1]['0.1mkF 50V X7R']["RefDes"],
                                     map_rdcateg=map_rc)
        self.assertEqual(cat, 'capacitor')

    def test_total_preparation_comp(self):
        in_comp = {'0.1mkF 50V X7R': {'ComponentName': 'C_SMD_0805',
                                      'Count': '6',
                                      'PatternName': 'SMD_0805',
                                      'RefDes': 'C1'}}

        out_comp = {'value': '0.1mkF',
                    'tolerance': '',
                    'voltage': '50V',
                    'comment': 'X7R; ',
                    'count': 6,
                    'power': '',
                    'pattern_name': 'SMD_0805',
                    'category_name': 'capacitor',
                    }
        self.assertEqual(out_comp, prepfr.preparation_component(in_comp))

if __name__ == '__main__':
    # est_get_comps_from_cat('resistor', db=db)
    # test_get_pcb()
    map_rc = dbt.map_refdes_category(db=db)
    print(map_rc)
    # unittest.main()
