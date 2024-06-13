import tensorflow as tf

class XTokenizer:
    def __init__(self):
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer(lower=True, filters='')

    def fit_on_texts(self, texts):
        self.tokenizer.fit_on_texts(texts)

    def texts_to_sequences(self, texts):
        return self.tokenizer.texts_to_sequences(texts)

    def pad_sequences(self, sequences, maxlen=None, padding='post', truncating='post', value=0):
        return tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=maxlen, padding=padding, truncating=truncating, value=value)
