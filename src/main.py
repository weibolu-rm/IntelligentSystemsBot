import os
from intelligent_system_bot.rdf import DataBuilder
from intelligent_system_bot.parse import TikaPreprocessor, SpacyNlp
from intelligent_system_bot.spotlight import Spotlight


def main():
    data_builder = DataBuilder(is_init=False)
    preprocessor = TikaPreprocessor()
    spacy_nlp = SpacyNlp()
    spotlight = Spotlight()

    data_builder.run()
    preprocessor.run()
    spacy_nlp.run(preprocessor.preprocessed_mapping)
    spotlight.run(spacy_nlp.token_mapping)

    # fuseki server needs to be up and running at this point,
    # with the uploaded knowledge base
    data_builder.load_topics_from_processed()
    data_builder.inference_step()

    # now serializing after extracting topics from resources
    data_builder.serialize_knowledge_graph()



if __name__ == "__main__":
    main()
