import numpy as np
import tensorflow as tf
from nltk.tokenize import word_tokenize

class BidirectionalLstm():
    def __init__(self):
        self.essentials = None
        self.vocab_size = None
        self.max_len = None
        self.labels = None
        self.word2idx = None
        self.idx2word = None
        self.embedding_matrix = None
    @staticmethod
    def get_architect_file_path(model_dir_path):
        return model_dir_path + '/BidirectionalLstm_architecture.json'

    @staticmethod
    def get_weight_file_path(model_dir_path):
        return model_dir_path + '/BidirectionalLstm_weights.h5'

    @staticmethod
    def get_config_file_path(model_dir_path):
        return model_dir_path + '/BidirectionalLstm_config.npy'

    def Load_Model(self,model_dir_path=None):
        if model_dir_path==None:
            model_dir_path = "Models\LSTM-LineType-Classifier"
        
        json = open(self.get_architect_file_path(model_dir_path), 'r').read()
        self.model = tf.keras.models.model_from_json(json)
        self.model.load_weights(self.get_weight_file_path(model_dir_path))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        config_file_path = self.get_config_file_path(model_dir_path)

        self.essentials = np.load(config_file_path, allow_pickle = True).item()
        self.idx2word = self.essentials['idx2word']
        self.word2idx = self.essentials['word2idx']
        self.max_len = self.essentials['text_max_len']
        self.vocab_size = self.essentials['vocab_size']
        self.labels = self.essentials['labels']
        

    def predict_line(self, sentence):
        predicted = self.predict(sentence)
        return self.labels[np.argmax(predicted)]
    def predict(self, sentence):
        x = []
        tokens = [w.lower() for w in word_tokenize(sentence)]
        word_idx = [self.word2idx[token] if token in self.word2idx else 0 for token in tokens]
        x.append(word_idx)
        X = tf.keras.preprocessing.sequence.pad_sequences(x, self.max_len)
        output = self.model.predict(X)
        return output[0]
    
if __name__ == "__main__":
    lstm = BidirectionalLstm()

    lstm.Load_Model("Models/LSTM-LineType-Classifier")
    y = lstm.predict_line("""Profile name : mostafa """)
    print(y)

