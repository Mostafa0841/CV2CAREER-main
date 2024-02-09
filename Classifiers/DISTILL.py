from transformers import  pipeline
import tensorflow as tf 

class DISTILL:
    def __init__(self) :
        self.Model = None
    
    def Load_Model(self, model_path=None):
        if model_path == None :
            model_path = "Models/pytorch-DISTILLBERT-ResumeSectionClassifier"
        self.Model = pipeline("text-classification", model=model_path)

    def predict_segment(self,txt):
        # Use the pipeline's predict method to get predictions directly
        result = self.Model(txt)
        predicted_label = result[0]["label"]
        print(f"{txt} : {predicted_label}")
        return predicted_label


if __name__ == "__main__":
    distil = DISTILL()


    distil.Load_Model()
    y = distil.predict_segment("""
Phone:
+49 800 600 600
E-Mail:
christoper.morgan@gmail.com
Linkedin:
linkedin.com/christopher.morgan
christopasdasder.morgan@gmail.com"
CHRISTOPHER MORGAN
                               """)
    print(y)


