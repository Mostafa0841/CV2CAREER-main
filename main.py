from ResumeParser import *
from Utilis.Models import *
from Utilis.render_resume import *
if __name__ == '__main__':
    data = {
        "Personal_Info": [
            """ Phone:
+49 800 600 600
""",
"""
E-Mail:
christoper.morgan@gmail.com
""",
"""
Linkedin:

linkedin.com/christopher.morgan
""",
"""
christopasdasder.morgan@gmail.com"""
""".
CHRISTOPHER MORGAN"""
       
        ],
        
"Work_Experience" : [

"Backend Developer - Tech Solutions Inc., San Francisco"
,
"01/2017 05/2020"
,
"•	Cooperate with designers to create clean interfaces and simple, intuitive interactions and experiences."
,
"•	Develop project concepts and maintain optimal workflow."
,

"Web Developer at Luna Web Design, New York"
,
"09/2015 05/2019"
,
"•	Work with senior developer to manage large, complex design projects for corporate clients."
,
"•	Complete detailed programming and development tasks for front end public and internal websites as well as challenging back-end server code."
,
"•	Carry out quality assurance tests to discover errors and optimize usability."
]
,
"Skills" : ["C++" , "C#"  , "Python" , "AWS"],
"Education" : ["2014-2019" , """Bachelor of Science: Computer Information Systems - Columbia University, NY""" ],
"Certificates" : ["PHP Framework (certificate): Zend, Codeigniter, Symfony." , """Programming Languages: JavaScript, HTML5, PHP OOP, CSS, SQL, MySQL.""" ]
,"Languages" : ["Arabic" , "English" , "Chinese"]
    }

#Loading Models 
ner , ner_dates , zero_shot_classifier , tagger = Models().load_trained_models()

R = ResumeParser(ner , ner_dates , zero_shot_classifier , tagger)

infos = R.parse(data)
R.save_parse_as_json(infos,"TEMP","ParsedResume.json")
generate_resume_from_json(infos , "TEMP")


    
    
    
    


