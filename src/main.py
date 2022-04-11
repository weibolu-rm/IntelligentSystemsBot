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
    spacy_nlp.run()

    # TODO: pass spacy_nlp.tokens
    spotlight.run({"Obama", "concordia university"})

    



if __name__ == "__main__":
    main()
