from intelligent_system_bot.rdf import DataBuilder
from intelligent_system_bot.parse import TikaPreprocessor, SpacyNlp

def main():
    data_builder = DataBuilder(is_init=False)
    preprocessor = TikaPreprocessor()
    spacy_nlp = SpacyNlp()

    data_builder.run()
    preprocessor.run()
    spacy_nlp.run()

if __name__ == "__main__":
    main()
