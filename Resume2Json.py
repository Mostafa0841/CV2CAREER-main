


## use self.lstm.predict_line(line) >> returns line type (Meta ,Content , Header).
## use self.distill.predict_segment(merged_content) >> returns section name (Personal_Info , Skills , etc).

from Utilis.Resume_Parser_Paragraphs_Extractor import *
import json
class Resume2Json:
    def __init__(self ,file_path ,LSTM_Model , DISTILL_Model):
        self.lstm  = LSTM_Model
        self.distill = DISTILL_Model
        self.resumeToList = WordParser(file_path)
        self.resume_json = {}
       
    def parse(self):
        Resume_Lines = self.resumeToList.getParagraphs()
        Undefined_json_Sections = self.Resume_Lines_To_undefined_json_Sections(Resume_Lines)
        defined_json_Sections =self.json_Sections_to_Defined_Sections(Undefined_json_Sections)
        return defined_json_Sections
        
    def Resume_Lines_To_undefined_json_Sections(self, Resume_Lines):
        
        ## Task : 1 - combine all lines together that appears before 1st header in a list.
        ##        2 - between each header segment all lines between them.
        #    example [Header1 , line1 , line2 , Header] so that line1,line1 should be in one list.
        ## You Have a list of lines => (-List-) Resume_Lines:
        ## [ 
        #    Name : Mostafa,
        #    Phone : 0109999999,
        #    Work Experience ,
        #    compnay: Facebook,
        #    jobtitle: Backend Dev.
        #    Skills,
        #    C++,
        #    Python,
        #    Pycharm,
        #    Education,
        # ]

        ## Required output => (-JSON-) json_data :
        ## {
        #   [ 
        #    Section1:[Name : Mostafa , Phone : 0109999999]
        #    Section2:[compnay: Facebook , jobtitle: Backend Dev.] 
        #    Section3:[ C++,Python,Pycharm,] 
        #    
        #   ]
        # }
        sections = []  # List to store the sections of the resume
       
        json_data = {f"section{i+1}": section for i, section in enumerate(sections)}

        return json_data


        
        
    def json_Sections_to_Defined_Sections(self,json_data):
        output_data = {}
        ## Required output => (-JSON-) (output_data) :
        ## {
        #   [ 
        #    PredictionOutput:[Name : Mostafa , Phone : 0109999999]
        #    PredictionOutput:[compnay: Facebook,jobtitle: Backend Dev.] 
        #    PredictionOutput:[ C++,Python,Pycharm,] 
        #    
        #   ]
        # }
        
        return output_data
         
    