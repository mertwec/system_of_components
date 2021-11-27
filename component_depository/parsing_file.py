import os
import pprint

 
class FileInPath:    
    path_to_files = r'./'   # this directory
    
    def __init__(self, path=path_to_files, type_file='csv'):
        self.path = os.path.abspath(path_to_files)
        self.type_file = type_file
    
    def message(self):
        _notexist = f'not exist file with exp {self.type_file}'
        _notcorrect = "inputed uncorrect key, try again"
        
        
    def find_file(self):
        """select file with expansion (type_file) default=.csv
        return list of all files"""    
        return [file for file in os.listdir(self.path) if file.endswith(f'.{self.type_file}')]


    def numbering_file_to_key(self) -> dict:
        """enumerate files"""
        return {k:v for(k,v) in zip(range(1,(len(self.find_file)+1)),self.find_file)}
    
    #TODO
    def select_file(self, files: dict):
        """select file in terminal"""
        pprint.pprint(files)
        while files:
            sel = input("input key of file: ")
            if sel.isdigit() and int(sel) in files.keys():
                return files[int(sel)]
            else:
                print(self.message._notexist)
        else:
            print(self.message._notcorrect)


if __name__ == "__main__":
    fop = FileInPath() 
    #TODO
    input()
