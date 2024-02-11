from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import pipeline
from flair.data import Sentence
from flair.models import SequenceTagger
from Classifiers.LSTM import *
from Classifiers.DISTILL import *
import pickle



class Models:

    def pickle_it(self, obj, file_name):
        with open(f'{file_name}.pickle', 'wb') as f:
            pickle.dump(obj, f)

    def unpickle_it(self, file_name):
        with open(f'{file_name}.pickle', 'rb') as f:
            return pickle.load(f)

    def load_trained_models(self, pickle=False):
        lstm_obj = BidirectionalLstm()
        lstm_obj.Load_Model("Models/LSTM-LineType-Classifier/")
        self.lstm = lstm_obj
        
        distill_obj = DISTILL()
        distill_obj.Load_Model()
        self.distill=distill_obj
        
        #NER (dates)
        
        tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
        model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
        self.ner_dates = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

        #Zero Shot Classification
        self.zero_shot_classifier = pipeline("zero-shot-classification", model='valhalla/distilbart-mnli-12-6')

        # Ner
        tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
        self.ner = pipeline('ner', model=model, tokenizer=tokenizer, grouped_entities=True)

        # Pos Tagging
        self.tagger = SequenceTagger.load("flair/pos-english-fast")


        if pickle:
            self.pickle_models()
        
        return self.ner, self.ner_dates, self.zero_shot_classifier, self.tagger ,self.lstm , self.distill
    
    def pickle_models(self):
        self.pickle_it(self.ner, "Models/Parsing_Models/ner")
        self.pickle_it(self.zero_shot_classifier, "Models/Parsing_Models/zero_shot_classifier_6")
        self.pickle_it(self.ner_dates, "Models/Parsing_Models/ner_dates")
        self.pickle_it(self.tagger, "Models/Parsing_Models/pos_tagger_fast")


    def load_pickled_models(self):
        ner_dates = self.unpickle_it('Models/Parsing_Models/ner_dates')
        ner = self.unpickle_it('Models/Parsing_Models/ner')
        zero_shot_classifier = self.unpickle_it('Models/Parsing_Models/zero_shot_classifier_6')
        tagger = self.unpickle_it("Models/Parsing_Models/pos_tagger_fast")
        return ner_dates, ner, zero_shot_classifier, tagger
    
    def get_flair_sentence(self, sent):
        return Sentence(sent)