
import re

from research_framework.base.plugin.base_plugin import BasePlugin
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora.dictionary import Dictionary

from research_framework.container.container import Container
from research_framework.flyweight.flyweight_manager import OutputFlyManager
from research_framework.plugins.wrappers import CoherenceMetricWrapper

from gensim.utils import simple_preprocess

@Container.bind(OutputFlyManager, CoherenceMetricWrapper)
class Coherence(BasePlugin):
    def __init__(self, topk=10, processes=1, measure='c_npmi'):
        """
        Initialize metric

        Parameters
        ----------
        topk : how many most likely words to consider in
        the evaluation
        measure : (default 'c_npmi') measure to use.
        processes: number of processes
        other measures: 'u_mass', 'c_v', 'c_uci', 'c_npmi'
        """
        super().__init__()
        
        self.topk = topk
        self.processes = processes
        self.measure = measure

    
    def fit(self, x, y=None):...
    def predict(self, df, predicted):
        _, d_y, _ = predicted

        topics = list(d_y.values())

        texts = df.text.progress_apply(
            lambda text: [word for word in simple_preprocess(text) if word in self.f_vocab or any(word in topic for topic in topics) ]
        )

        texts = texts.drop(texts[texts.apply(len) == 0].index).values.tolist()

        dictionary = Dictionary(texts)

        if self.topk > len(topics[0]):
            raise Exception('Words in topics are less than topk')
        else:
            npmi = CoherenceModel(
                topics=topics,
                texts=texts,
                dictionary=dictionary,
                coherence=self.measure,
                processes=self.processes,
                topn=self.topk)
            
            return npmi.get_coherence()
        

@Container.bind(OutputFlyManager, CoherenceMetricWrapper)        
class u_mass(BasePlugin):
    def __init__(self, topk=10, processes=1):
        self.metric = Coherence(topk=topk, processes=processes, measure='u_mass')
    
    def fit(self, x, y=None):...
    def predict(self, df, predicted):
        return self.metric.predict(df, predicted)
    
    
@Container.bind(OutputFlyManager, CoherenceMetricWrapper)        
class c_v(BasePlugin):
    def __init__(self, topk=10, processes=1):
        self.metric = Coherence(topk=topk, processes=processes, measure='c_v')
    
    def fit(self, x, y=None):...
    def predict(self, df, predicted):
        return self.metric.predict(df, predicted)
    
    
@Container.bind(OutputFlyManager, CoherenceMetricWrapper)        
class c_uci(BasePlugin):
    def __init__(self, topk=10, processes=1):
        self.metric = Coherence(topk=topk, processes=processes, measure='c_uci')
    
    def fit(self, x, y=None):...
    def predict(self, df, predicted):
        return self.metric.predict(df, predicted)
    
    
@Container.bind(OutputFlyManager, CoherenceMetricWrapper)        
class c_npmi(BasePlugin):
    def __init__(self, topk=10, processes=1):
        self.metric = Coherence(topk=topk, processes=processes, measure='c_npmi')
    
    def fit(self, x, y=None):...
    def predict(self, df, predicted):
        return self.metric.predict(df, predicted)