from ResumeParser import *
from Utilis.Models import *

from Utilis.render_resume import *
from Resume2Json import *
if __name__ == '__main__':
    file_path = "Data/resume1.docx"
    ############################LOADING MODELS ######################################
    ner , ner_dates , zero_shot_classifier , tagger , lstm , distill = Models().load_trained_models()
    R = ResumeParser(ner , ner_dates , zero_shot_classifier , tagger)
    R2JSON = Resume2Json(file_path,lstm,distill)
    ##################################################################################
   
    defined_sections = R2JSON.parse()
    detailed_parsed_defined_sections = R.parse(defined_sections)
    R.save_parse_as_json(detailed_parsed_defined_sections,"TEMP","ParsedResume.json")
    generate_resume_from_json(detailed_parsed_defined_sections , "TEMP")





    
    
    
    


