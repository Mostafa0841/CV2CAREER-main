import aspose.words as aw
from bs4 import BeautifulSoup

class WordParser:
    def __init__(self , file_path):
        self.file_path = file_path
        self.soup = None
        self.paragraphs = None

    def Segmenting_Resume(self):

        doc = aw.Document(self.file_path)
        doc.save("TEMP/HTML_Format/temp.html")

        with open("TEMP/HTML_Format/temp.html", "r", encoding="utf-8") as html_file:
            html = html_file.read()
            soup = BeautifulSoup(html, 'html.parser')
            self.soup = soup
    def get_html_segments(self):
        soup = self.soup
        results = []
        outer_div = soup.find_all(['p','li','h1'])
        for p in outer_div:
            paragraph_text=""
            spans_or_br = p.find_all(['span','br'])
            for s in spans_or_br:
                if(s.name=='span'):
                    text = s.get_text(strip=True)
                    cond = s.get_text(strip=True) and len(s.get_text(strip=True))>0  
                    
                    if text and cond:
                        paragraph_text += " "+text

                else:
                    paragraph_text += "\n"
            if(len(paragraph_text.strip())>0 and "Aspose" not in paragraph_text):
                cleaned_text = ''.join(char for char in paragraph_text if ord(char) < 128)
                cleaned_text = cleaned_text.lstrip()
                results.append(cleaned_text) 
        self.paragraphs = results


    def getParagraphs(self):
        self.Segmenting_Resume()
        self.get_html_segments()
        return self.paragraphs

  



