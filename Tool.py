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
            
class UnitTest(object):
    def __init__(self):
        self.open_all_files()
        
    def open_all_files(self):
        self.empty_file = open('D:\\TW\\Steps\\001 TFFemptyfile.txt')
        self.with_query = open('D:\\TW\\Steps\\001 FFTCheck.txt')
        self.with_undo =  open('D:\\TW\\Steps\\001 FTTCheck.txt')
        self.all_commented_no_undo = open('D:\\TW\\Steps\\001 FTFCheck.txt')
        self.with_query_no_undo = open('D:\\TW\\Steps\\001 FFFCheck.txt')
        
    def close_all_files(self):
        self.empty_file.close()
        self.with_query.close()
        self.with_undo.close()
        self.all_commented_no_undo.close()
        self.with_query_no_undo.close()
        
    def files_to_intial_pos(self):
        self.empty_file.seek(0)
        self.with_query.seek(0)
        self.with_undo.seek(0)
        self.all_commented_no_undo.seek(0)
        self.with_query_no_undo.seek(0)
        
    def test_file_select(self):
        tool_test = FileSelect()
        assert(tool_test.get_filename('filename.txt')) == 'filename'
        assert(tool_test.get_filename('filename')) == 'filename'
        print 'All FileSelect test cases passed'
        
    def test_filereader(self):
        test_filereader = FileReader()
        assert(test_filereader.check_empty(self.empty_file))==True
        assert(test_filereader.check_empty(self.with_query))==False
        self.empty_file.seek(0)
        self.with_query.seek(0)
        assert(test_filereader.process_file(self.empty_file))==(True,False,False)
        assert(test_filereader.process_file(self.with_query))==(False,False,True)
        assert(test_filereader.process_file(self.with_undo))==(False,True,True)
        assert(test_filereader.process_file(self.all_commented_no_undo))==(False,True,False)
        assert(test_filereader.process_file(self.with_query_no_undo))==(False,False,False)
        
        self.close_all_files()
        print 'All Filereader test cases passed'

    def test_Content(self):
        self.close_all_files()
        self.open_all_files()
        test_content = Content()
        #Check if all the code are commented
        assert(test_content.all_commented(self.empty_file))== True
        assert(test_content.all_commented(self.with_query))== False
        assert(test_content.all_commented(self.with_undo))== True
        assert(test_content.all_commented(self.all_commented_no_undo))== True
        assert(test_content.all_commented(self.with_query_no_undo))== False
        
        #check if there is an end comment in the file
        self.files_to_intial_pos()
        assert(test_content.check_undo(self.empty_file)) == False
        assert(test_content.check_undo(self.with_query))==True
        assert(test_content.check_undo(self.with_undo))==True
        assert(test_content.check_undo(self.all_commented_no_undo))==False
        assert(test_content.check_undo(self.with_query_no_undo))==False
        self.close_all_files()        
        print 'Content Tested Successfully'
        
    def test_FileSplit(self):
        test_filesplit = FileSplit()
        filename = '001 FFTCheck'
        devonly_file = '001 FFTDevOnlyCheck'
        assert(test_filesplit.get_change_num_filename_devonly(filename)) == ('001','FFTCheck',False)
        assert(test_filesplit.get_change_num_filename_devonly(devonly_file)) == ('001','FFTDevOnlyCheck',True)
        
        assert(test_filesplit.check_dev_only(filename)) == False
        assert(test_filesplit.check_dev_only(devonly_file)) == True
        
        print 'FileSplit Tested Successfully'

    def all_tests(self):
        self.test_file_select()
        self.test_filereader()
        self.test_Content()
        self.test_FileSplit()
        
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