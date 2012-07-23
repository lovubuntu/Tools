import os
REPORT_FILE     = 'Report.csv'
class FileSelect(object):
    def __init__(self):
        self.file_name = None
        self.all_files = None
        self.target_file = None
    
    def get_filename(self,filename):
        if filename.find('.') != -1:
            return filename[:filename.find('.')]
        return filename
    
    def get_all_files(self,path):
        all_files = os.listdir(path)
        for file_name in all_files:
            if file_name == REPORT_FILE:
                continue 
            abs_path = os.path.join(path,file_name)
            target_file = open(abs_path)
            file_name = self.get_filename(file_name) 
            yield target_file,file_name