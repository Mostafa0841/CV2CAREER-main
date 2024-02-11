from Utilis.Models import Models
from datetime import datetime
from dateutil import parser
import re
from string import punctuation
import json
import os
class ResumeParser:
    def __init__(self , ner , ner_dates , zero_shot_classifier , tagger):
        self.models = Models()
        self.ner, self.ner_dates, self.zero_shot_classifier, self.tagger = ner , ner_dates , zero_shot_classifier , tagger 
        self.parsed_cv = {}

    def save_parse_as_json(self, data_dict, folder_path, file_name):
        print("Saving the parse...")
        # Create the folder if it does not exist
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w', encoding="utf-8") as f:
            json.dump(data_dict, f, indent=4, default=str, ensure_ascii=False)
    
    def parse(self, resume_lines):
        resume_segments = resume_lines
        print("***************************** Parsing the Resume...***************************** ")
        for segment_name in resume_segments:
            if segment_name == "Work_Experience":
                print("---Parsing Work Experience---")
                resume_segment = resume_segments[segment_name]
                self.parse_job_history(resume_segment)
                print("---Finished Parsing Work Experience---")
            elif segment_name == "Personal_Info" or segment_name == "Summary":
                print("---Parsing Personal_Info---")
                contact = resume_segments[segment_name]
                self.parse_contact_info(contact)
                print("---Finished Parsing Personal_Info---")
            elif segment_name == "Education":
                print("---Parsing Education---")
                education = resume_segments[segment_name]
                self.parse_education(education)
                print("---Finished Parsing Education---")
            elif segment_name == "Skills1" or segment_name == "Skills2":
                print("---Parsing Skills---")
                skills= resume_segments[segment_name]
                self.parse_skills(skills)
                print("---Finished Parsing Skills---")
            elif segment_name == "Projects":
                print("---Parsing Projects---")
                projects = resume_segments[segment_name]
                self.parse_projects(projects)
                print("---Finished Parsing Projects---")
            elif segment_name == "Certificates":
                print("---Parsing Certificates---")
                projects = resume_segments[segment_name]
                self.parse_certifications(projects)
                print("---Finished Parsing Certificates---")
            elif segment_name == "Languages":
                print("---Parsing Languages---")
                languages = resume_segments[segment_name]
                self.parse_languages(languages)
                print("---Finished Parsing Languages---")
            elif segment_name == "References":
                print("---Parsing References---")
                references = resume_segments[segment_name]
                self.parse_references(references)
                print("---Finished Parsing References---")
           
        return self.parsed_cv

 

    def parse_contact_info(self, contact_info):
        contact_info_dict = {}
        name = self.find_person_name(contact_info)
        email = self.find_contact_email(contact_info)
        phone = self.find_contact_phone(contact_info)
        self.parsed_cv['Name'] = name
        contact_info_dict["Email"] = email
        contact_info_dict["Phone"] = phone
        self.parsed_cv['Personal_Info'] = contact_info_dict
    
    def find_person_name(self, items):

        class_score = []
        splitter = re.compile(r'[{}]+'.format(re.escape(punctuation.replace("&", "") )))
        classes = ["person name", "address", "email", "title"]
        for item in items: 
            elements = splitter.split(item)
            for element in elements:
                element = ''.join(i for i in element.strip() if not i.isdigit())
                if not len(element.strip().split()) > 1: continue
                out = self.zero_shot_classifier(element, classes)
                highest = sorted(zip(out["labels"], out["scores"]), key=lambda x: x[1])[-1]
                if highest[0] == "person name":
                    class_score.append((element, highest[1]))
        if len(class_score):
            return sorted(class_score, key=lambda x: x[1], reverse=True)[0][0]
        return ""
    def find_contact_email(self, items):
        emails = []
        # Regular expression pattern to capture various email formats
        profile_pattern = r'(?:https?://)?(?:www\.)?(?:linkedin\.com/[A-Za-z0-9_-]+|github\.com/[A-Za-z0-9_-]+|twitter\.com/[A-Za-z0-9_-]+)'
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        combined_pattern = f'{email_pattern}|{profile_pattern}'
        
        for item in items: 
            matches = re.findall(combined_pattern, item)
            emails.extend(matches)
        
        return emails
    def find_contact_phone(self, items):
        """Extracts phone numbers in various country formats from the given items."""
        phone_numbers = []
        PN = validate_phone_number_pattern = r"\b\+?[0-9][0-9\s]{7,14}\b"
        for item in items:
            matches = re.findall(PN, item)
            phone_numbers.extend(matches)

        return phone_numbers
    
    def parse_job_history(self, resume_segment):
        """Parses job history information from the given resume segment."""

        # 1. Get job title indices:
        idx_job_title = self.get_job_titles(resume_segment)  # Returns line indices containing job titles

        # 2. Handle cases with no job titles found:
        current_and_below = False  # Flag for handling job structure variations
        if not len(idx_job_title):
            self.parsed_cv["Work_Experience"] = []  # Set empty job history
            return  # Exit if no job titles found

        # 3. Check for current job at the beginning:
        if idx_job_title[0][0] == 0:
            current_and_below = True  # Adjust parsing strategy if current job is first

        # 4. Initialize job history list:
        job_history = []

        # 5. Iterate through each job title:
        for ls_idx, (idx, job_title) in enumerate(idx_job_title):
            job_info = {}  # Create a dictionary for current job information
            job_info["Job Title"] = self.filter_job_title(job_title)  # Store filtered job title

            # 6. Extract company information:
            if current_and_below:
                line1, line2 = idx, idx + 1  # Look below for company if current job
            else:
                line1, line2 = idx, idx - 1  # Look above for company otherwise
            job_info["Company"] = self.get_job_company(line1, line2, resume_segment)

            # 7. Determine starting span for date extraction:
            if current_and_below:
                st_span = idx  # Include current job line for dates
            else:
                st_span = idx - 1  # Exclude current job line

            # 8. Extract job dates:
            if ls_idx == len(idx_job_title) - 1:
                end_span = len(resume_segment)  # Include all remaining lines for last job
            else:
                end_span = idx_job_title[ls_idx + 1][0]  # End at next job title
            start, end = self.get_job_dates(st_span, end_span, resume_segment)
            job_info["Start Date"] = start
            job_info["End Date"] = end

            # 9. Extract job responsibilities:
            job_info["Responsibilities"] = self.get_job_responsibilities(idx,end_span, resume_segment)

            # 10. Append parsed job info to job history:
            job_history.append(job_info)

        # 11. Store parsed job history in parsed_cv:
        self.parsed_cv["Work_Experience"] = job_history


    def get_job_titles(self, resume_segment):
        classes = ["organization", "institution", "company", "job title", "work details"]
        idx_line = []
        for idx, line in enumerate(resume_segment):
            has_verb = False
            line_modifed = ''.join(i for i in line if not i.isdigit())
            sentence = self.models.get_flair_sentence(line_modifed)
            self.tagger.predict(sentence)
            tags = []
            for entity in sentence.get_labels('pos'):
                tags.append(entity.value)
                if entity.value.startswith("V"): 
                    has_verb = True
            
            most_common_tag = max(set(tags), key=tags.count)
            if (most_common_tag == "NNP") or (most_common_tag == "NN"):
            # if most_common_tag == "NNP":
                if not has_verb:
                    out = self.zero_shot_classifier(line, classes)
                    class_score = zip(out["labels"], out["scores"])
                    highest = sorted(class_score, key=lambda x: x[1])[-1]

                    if (highest[0] == "job title") or (highest[0] == "organization"):
                    # if highest[0] == "job title":
                        idx_line.append((idx, line))
           
        return idx_line

    def get_job_dates(self, st, end, resume_segment):
        search_span = resume_segment[st:end]
        dates = []
        for line in search_span:
            for dt in self.get_ner_in_line(line, "DATE"):
                if self.isvalidyear(dt.strip()):
                    dates.append(dt)
        if len(dates): first = dates[0]
        exists_second = False
        if len(dates) > 1:
            exists_second = True
            second = dates[1]
        
        if len(dates) > 0:
            if self.has_two_dates(first):
                d1, d2 = self.get_two_dates(first)
                return self.format_date(d1), self.format_date(d2)
            elif exists_second and self.has_two_dates(second): 
                d1, d2 = self.get_two_dates(second)
                return self.format_date(d1), self.format_date(d2)
            else: 
                if exists_second: 
                    st = self.format_date(first)
                    end = self.format_date(second)
                    return st, end
                else: 
                    return (self.format_date(first), "") 
        else: return ("", "")

    
    
    def filter_job_title(self, job_title):
        job_title_splitter = re.compile(r'[{}]+'.format(re.escape(punctuation.replace("&", "") )))
        job_title = ''.join(i for i in job_title if not i.isdigit())
        tokens = job_title_splitter.split(job_title)
        tokens = [''.join([i for i in tok.strip() if (i.isalpha() or i.strip()=="")]) for tok in tokens if tok.strip()] 
        classes = ["company", "organization", "institution", "job title", "responsibility",  "details"]
        new_title = []
        for token in tokens:
            if not token: continue
            res = self.zero_shot_classifier(token, classes)
            class_score = zip(res["labels"], res["scores"])
            highest = sorted(class_score, key=lambda x: x[1])[-1]
            if (highest[0] == "job title") or (highest[0] == "organization"):
            # if highest[0] == "job title":
                new_title.append(token.strip())
        if len(new_title):
            return ', '.join(new_title)
        else: return ', '.join(tokens)

    def has_two_dates(self, date):
        years = self.get_valid_years()
        count = 0
        for year in years:
            if year in str(date):
                count+=1
        return count == 2
    
    def get_two_dates(self, date):
        years = self.get_valid_years()
        idxs = []
        for year in years:
            if year in date: 
                idxs.append(date.index(year))
        min_idx = min(idxs)  
        first = date[:min_idx+4]
        second = date[min_idx+4:]
        return first, second
    def get_valid_years(self):
        current_year = datetime.today().year
        years = [str(i) for i in range(current_year-100, current_year)]
        return years

    def format_date(self, date):
        out = self.parse_date(date)
        if out: 
            return out
        else: 
            date = self.clean_date(date)
            out = self.parse_date(date)
            if out: 
                return out
            else: 
                return date

    def clean_date(self, date): 
        try:
            date = ''.join(i for i in date if i.isalnum() or i =='-' or i == '/')
            return date
        except:
            return date
    def parse_date(self, date):
        try:
            date = parser.parse(date)
            return date.strftime("%m-%Y")
        except: 
            try:
                date = datetime(date)
                return date.strftime("%m-%Y")
            except: 
                return 0 
    def isvalidyear(self, date):
        current_year = datetime.today().year
        years = [str(i) for i in range(current_year-100, current_year)]
        for year in years:
            if year in str(date):
                return True 
        return False
    def get_ner_in_line(self, line, entity_type):
        if entity_type == "DATE": ner = self.ner_dates
        else: ner = self.ner
        return [i['word'] for i in ner(line) if i['entity_group'] == entity_type]
        

    def get_job_company(self, idx, idx1, resume_segment):
        job_title = resume_segment[idx]
        if not idx1 <= len(resume_segment)-1: context = ""
        else:context = resume_segment[idx1]
        candidate_companies = self.get_ner_in_line(job_title, "ORG") + self.get_ner_in_line(context, "ORG")
        classes = ["organization", "company", "institution", "not organization", "not company", "not institution"]
        scores = []
        for comp in candidate_companies:
            res = self.zero_shot_classifier(comp, classes)['scores']
            scores.append(max(res[:3]))
        sorted_cmps = sorted(zip(candidate_companies, scores), key=lambda x: x[1], reverse=True)
        if len(sorted_cmps): return sorted_cmps[0][0]
        return context
   
    def get_job_responsibilities(self, job_title_idx, end_idx, resume_segment):
        """Parses job responsibilities from the resume segment.

        Args:
            job_title_idx: The index of the line containing the job title.
            end_idx: The index of the line after which to stop searching for responsibilities.
            resume_segment: The list of lines in the resume segment.

        Returns:
            A list of parsed job responsibilities.
        """

        responsibilities = []

        for line_idx in range(job_title_idx + 1, end_idx):
            line = resume_segment[line_idx]

            # Use the zero-shot classifier to identify responsibilities:
            classes = ["job duty", "responsibility", "task", "accomplishment", "work detail" , "date"]  # Removed "not job duty" as it's not relevant for positive classification
            out = self.zero_shot_classifier(line, classes)
            class_score = zip(out["labels"], out["scores"])
            highest = sorted(class_score, key=lambda x: x[1])[-1]
            if highest[0] in classes[:5]:  # Check if the highest-scoring class is one of the relevant ones
                responsibilities.append(line)

        # Filter and format responsibilities if needed
        responsibilities = [self.filter_responsibility(r) for r in responsibilities]

        return responsibilities

    def filter_responsibility(self, responsibility):
        """Filters and formats a responsibility string (optional)."""

        # Example: Remove punctuation, extra spaces, etc.
        responsibility = re.sub(r"[^\w\s]", "", responsibility).strip()

        return responsibility

    def parse_education(self, education):
        self.parsed_cv['Education'] = education

    def parse_skills(self, skills):
        self.parsed_cv['Skills'] = skills
    def parse_projects(self, projects):
        self.parsed_cv['Projects'] = projects

    def parse_certifications(self, certifications):
        self.parsed_cv['Certificates'] = certifications
        
    def parse_languages(self, languages):
        self.parsed_cv['Languages'] = languages
    def parse_references(self, references):
        self.parsed_cv['References'] = references

    def print_data(self):
        print("Name : ", self.parsed_cv["Name"])
        print("----------------------------------")
        print("Phone :", self.parsed_cv["Personal_Info"]["Phone"])
        print("Emails:" )
        for email in self.parsed_cv["Personal_Info"]["Email"]:
            print(email)
        print("----------------------------------")
        print("Work Experience :" )
        for w in self.parsed_cv["Work_Experience"]:
            print("----------")
            print("Job Title : ",w["Job Title"])
            print("Company : " , w["Company"])
            print("Start Date : ", w["Start Date"])
            print("End Date :" , w["End Date"])
            print("Responsibilities :" , )
            for d in w["Responsibilities"]:
                print(d)
            print("----------")
        print("----------------------------------")
        print("Skills : " )
        for skill in self.parsed_cv['Skills']:
            print(skill)
        print("----------------------------------")
        print("Education : " )
        for e in self.parsed_cv['Education']:
            print(e)
        print("----------------------------------")
        print("Certificates : " )
        for c in self.parsed_cv['Certificates']:
            print(c)
        print("----------------------------------")
        print("Languages : " )
        for l in self.parsed_cv['Languages']:
            print(l)
    
