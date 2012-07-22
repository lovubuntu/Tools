import os

START_COMMENT   = '/*'
END_COMMENT     = '*/'
SINGLE_COMMENT  = '--'
UNDO            = '--//@UNDO'
REPORT_FILE     = 'Report.csv'
DEV_ONLY        = 'devonly'
SQL             = '.sql'

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
        for root,_,files in os.walk(path):
            for file_name in [ f for f in files if f.endswith(SQL)]:
                abs_path = os.path.join(root,file_name)
                target_file = open(abs_path)
                file_name = self.get_filename(file_name) 
                yield target_file,file_name
                
class FileReader(object):
    def check_empty(self,target_file):                
        for line in target_file:
            line = line.strip()
            if len(line) > 0:
                #Seeks file pointer to initial position
                target_file.seek(0)  
                return False
        return True

    def process_file(self,target_file):
        content = Content()
        if self.check_empty(target_file):
            return True,False,False
        #Seeks file to initial position to check if all content is commented
        target_file.seek(0)
        has_undo = content.check_undo(target_file)
         
        target_file.seek(0)
        if content.all_commented(target_file):
            return False,True,has_undo
        return False,False,has_undo

class Content(object):    
    def all_commented(self,target_file):
        for line in target_file:
            line = line.strip()
            line_len = len(line)
            #Checks if comment starts in this line
            if line_len > 0 and line[0:2]  == START_COMMENT:
                return self.find_end_comment(target_file)
            #Checks if there is a single line comment line
            elif line_len > 0 and line[:2] == SINGLE_COMMENT:
                return self.all_commented(target_file)
            #checks if the line contains end comment
            elif line_len > 0 and line[line_len-2:] == END_COMMENT:
                return self.all_commented(target_file)
            #The line is not a comment line
            elif line_len > 0:
                return False
        return True
    
    def find_end_comment(self,target_file):                        
        for line in target_file:
            line = line.strip()
            line_len = len(line)
            if line_len > 0 and line[line_len-2:]==END_COMMENT:
                return self.all_commented(target_file)
        #If there was no end comment invariably all text are commented
        return True

    def check_undo(self,target_file):
        for line in target_file:
            line.strip()
            if line.find(UNDO) != -1:
                return not self.all_commented(target_file)    
        return False
class FileSplit(object):
    def get_change_num_filename_devonly(self,filename):        
        change_num,filename = filename.split()        
        return change_num,filename,self.check_dev_only(filename)
    def check_dev_only(self,filename):
        filename = filename.lower()
        return filename.find(DEV_ONLY)!= -1

class ReportFile(object):
    def __init__(self,path):
        self.output = open(os.path.join(path,REPORT_FILE),'w')
    def create_header(self):
        heading = []
        heading.append('Filename')         
        heading.append('Change-Number')
        heading.append('Is_File_Empty')
        heading.append('Is_File_Commented_Out')
        heading.append('Has_Undo_Block')
        heading.append('is_file_Dev_only')
        self.output.write(','.join(heading)+'\n')
                
    def write_rows(self,*row):
        var_list = []
        for element in row:
            #Convert values to cast Boolean to String
            var_list.append(str(element))
        self.output.write(','.join(var_list)+'\n')
        
    def close_file(self):
        self.output.close()
        
class Main(object):    
    def __init__(self):
        self.path = None
            
    def get_user_input(self):
        self.path = raw_input('Enter the file path > ')
    def start(self):  
        self.get_user_input()
        Files_in_dest = FileSelect()
        Text = FileReader()
        split = FileSplit() 
        report = ReportFile(self.path)
        report.create_header()
        for target_file,file_name in Files_in_dest.get_all_files(self.path):
            change_num,filename,dev_only = split.get_change_num_filename_devonly(file_name)
            file_empty,file_commented_out,has_undo =Text.process_file(target_file)
            #Write to Output to Report File
            report.write_rows(filename,change_num,file_empty,file_commented_out,has_undo,dev_only)
            target_file.close()
        report.close_file()
        print 'Report Generated successfully'

QueryExistenceChecker = Main()
QueryExistenceChecker.start()