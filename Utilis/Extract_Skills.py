from flashtext import KeywordProcessor


# Loading Skills Dict
with open("TOOLS/all_skills_keys.txt", "r" , encoding="utf-8") as f:
    lines = f.readlines()
term_list = []
for line in lines:
    term_list.extend(line.strip().split(","))



keyword_processor = KeywordProcessor()
keyword_processor.add_keywords_from_list(term_list)
sen = """
Skill Highlights

•	Skill Highlights

•	Project management

•	Strong decision maker

•	Complex problem solver

•	Creative design

•	Innovative

•	Service-focused C++


"""
print(keyword_processor.extract_keywords(sen.lower()))