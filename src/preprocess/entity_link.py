import time
import preprocess
from collections import defaultdict
import swat_ned
import os
import sys
dirname = os.path.dirname(__file__)
relative_path = os.path.join(dirname, "rel_ned")
sys.path.insert(0, relative_path) 
from ned_utils import REL_NedAnalyzer

def add_entity(src_dataset_path, dst_dataset_path, entity_list_path, subset=None):
    # init
    start_time = time.time()
    dataset = preprocess.getDataset(src_dataset_path)
    rel_analyzer = REL_NedAnalyzer()
    entitiesToArticle_dict = defaultdict(list)
    # urlToName_dict = defaultdict(set)
    articles = dataset if subset == None else dataset[0:subset]

    # process entities
    article_entity_dict = rel_analyzer.analyze_entity(articles)
    for article in articles:
        entity_list = article_entity_dict[article["id"]]
        article["entities"] = entity_list
        for entity in entity_list:
            entitiesToArticle_dict[entity].append(article["id"])
        # google entities
        # google_entities = google_sa.analyze_entity(sentences)
        # for entity in google_entities:
        #     entitiesToArticle_dict[entity.metadata["wikipedia_url"]].append(article["id"])
        #     urlToName_dict[entity.metadata["wikipedia_url"]].add(entity.name)
        # article["entities"] = [next(iter((urlToName_dict[entity.metadata["wikipedia_url"]]))) for entity in google_entities] 

        # swat entities
        # swat_entities, entityIdToName_dict = swat_ned.getEntityList(sentences, article["headline"])
        # for entityId in swat_entities:
        #     entitiesToArticle_dict[entityId].append(article["id"])
        #     urlToName_dict[entityId].update(entityIdToName_dict[entityId])
        # article["entities"] = [next(iter((urlToName_dict[entityId]))) for entityId in swat_entities]

        # REL
        # rel_entities = rel_analyzer.analyze_entity(article)
        # for entity in rel_entities:
        #     entitiesToArticle_dict[entity].append(article["id"])
        # article["entities"] = rel_entities

    # urlToName_dict = {k: list(v) for k, v in urlToName_dict.items()}
    preprocess.dict_to_json(entitiesToArticle_dict, filepath=entity_list_path)
    preprocess.dict_to_json(articles, filepath=dst_dataset_path)
    # preprocess.dict_to_json(urlToName_dict, filepath="data/WikiIDToEntityName.json")
