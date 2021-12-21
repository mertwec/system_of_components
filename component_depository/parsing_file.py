import os
import pprint

 
class FileInPath:    
    path_to_files = r'./'   # this directory
    
    def __init__(self, type_file='csv'):
        self.path = os.path.abspath(self.path_to_files)
        self.type_file = type_file
        
        self.message_notexist = f'not exist file with exp {self.type_file}'
        self.message_notcorrect = "inputed uncorrect key, try again"      

    def find_file(self):
        """select file with expansion (type_file) default=.csv
        return list of all files"""    
        return [file for file in os.listdir(self.path) if file.endswith(f'.{self.type_file}')]

    def numbering_file_to_key(self) -> dict:
        """enumerate files"""
        return {k: v for(k, v) in zip(range(1, (len(self.find_file())+1)), self.find_file())}
    
    def select_file(self, files:dict):
        """select file in terminal"""
        
        pprint.pprint(files)
        while files:
            sel = input("input key of file: ")
            if sel.isdigit() and int(sel) in files.keys():
                return files[int(sel)]
            else:
                print(self.message_notcorrect)
        else:
            print(self.message_notexist)
            

def open_csv_file(path_to_file):
    pass


if __name__ == "__main__":
    fop = FileInPath(type_file='csv') 
    fop.path_to_files = r"d:/PyProgect/system_of_components/component_depository/"
    lf = fop.find_file()
    dfile = fop.numbering_file_to_key()
    #sf = fop.select_file(dfile)
    print(lf)
    
    
    
