from gensim import corpora
import pickle
import gensim
import pandas as pd
import numpy as np
import pyLDAvis.gensim
import pyLDAvis

class LDA():
    """
    this cless makes, saves to desk, and loads
        1- gensim dictionary
        2- corpus
        3- gensim lda model
    Args:
        data -> pandas series of type object (containing text) (optional)
        dictionary -> gensim.corpora.dictionary
        corpus-> gensim corpus (optional)
        model-> gensim lda model (optional)
        text_data= pandas cleaned text (optional)
        vis= pyLDAvis.display objec (optional)
    """
    def __init__(self, data=None, model=None, corpus=None, dictionary=None, text_data=None, vis=None):
        self.data = data
        self.model = model
        self.corpus = corpus
        self.dictionary = dictionary
        self.text_data = text_data
        self.vis = vis

    "________________________DICTIONARY______________________"
    def make_dict(self):
        """takes pandas series and returns dictionary to use with gensim   """
        text_data = self.data.apply(lambda i: str(i).split(' '))
        dictionary = corpora.Dictionary(text_data)
        self.dictionary = dictionary
        self.text_data = text_data

    def save_dict(self, dict_name = 'dict'):
        """saves the dictionary to the disk
            dict_name --> dictionary path + filename
        """
        self.dictionary.save('{}.gensim'.format(dict_name))

    def load_dict(self, dict_name):
        dictionary = gensim.corpora.Dictionary.load('{}.gensim'.format(dict_name))
        self.dictionary = dictionary

    "________________________CORPUS___________________________"
    def make_corpus(self):
        """ makes a corpus from gensim.corpora.dictionary object """
        corpus = [self.dictionary.doc2bow(text) for text in self.text_data]
        self.corpus = corpus

    def save_corpus(self, corpus_name='corpus'):
        self.corpus.dump( self.corpus, open( "{}.pkl".format(corpus_name), "wb" ))

    def load_corpus(corpus_name='corpus'):
        self.corpus = pickle.load(open( "{}.pkl".format(corpus_name), "rb" ))

    "________________________MODEL____________________________"
    def make_model(self,num_top=10):
        self.model = gensim.models.ldamodel.LdaModel(self.corpus, num_topics=num_top,
                                               id2word= self.dictionary, passes = 15)

    def save_model(self, model_name='model'):
        self.model.save('{}.gensim'.format(model_name))

    def load_model(self, model_name='model'):
        self.model = gensim.models.ldamodel.LdaModel.load('{}.gensim'.format(model_name))

    "________________________VIS_____________________________"
    def make_vis(self, sort_topics=True):
        lda_display = pyLDAvis.gensim.prepare(self.model,self.corpus,self.dictionary,sort_topics=sort_topics)
        self.vis = pyLDAvis.display(lda_display)
