from http.server import HTTPServer
from REL.mention_detection import MentionDetection
from REL.entity_disambiguation import EntityDisambiguation
from REL.ner import Cmns, load_flair_ner
from REL.server import make_handler
from REL.utils import process_results



wiki_version = "wiki_2019"
base_url = "/Users/samytlee/Documents/mediabias/src/preprocess/rel_ned"

config = {
    "mode": "eval",
    "model_path": "{}/{}/generated/model".format(base_url, wiki_version),
}
salience_threshold = 0.5

class REL_NedAnalyzer:
    def __init__(self):
        self.mention_detection = MentionDetection(base_url, wiki_version)
        # self.tagger_ner = load_flair_ner("ner-fast")

        self.tagger_ngram = Cmns(base_url, wiki_version, n=5)
        self.model = EntityDisambiguation(base_url, wiki_version, config)
    
    def analyze_entity(self, dataset):
        dataset = format_dataset(dataset) 
        mentions_dataset, n_mentions = self.mention_detection.find_mentions(dataset, self.tagger_ngram)
        predictions, timing = self.model.predict(mentions_dataset)
        results = process_results(mentions_dataset, predictions, dataset)
        doc_entity_dict = {} 
        for doc in results:
            entities = [entity[3] for entity in results[doc]] 
            doc_entity_dict[doc] = list(set(entities))
            # for entity in entities:
            #     mention = entity["mention"]
            #     prediction = entity["prediction"]
        return doc_entity_dict

def format_dataset(dataset):
    # dataset should have format [article], article = {"id":xxx, "content":xxx}
    processed = {}
    # user does some stuff, which results in the format below.
    for article in dataset:
        processed[article["id"]] = [article["content"], []]
    return processed
