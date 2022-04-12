from intelligent_system_bot.rdf import DataBuilder
from intelligent_system_bot.parse import TikaPreprocessor, SpacyNlp
from intelligent_system_bot.spotlight import Spotlight
from intelligent_system_bot.sparl import Sparql


def main():
    data_builder = DataBuilder(is_init=False)
    preprocessor = TikaPreprocessor()
    spacy_nlp = SpacyNlp()
    spotlight = Spotlight()

    data_builder.run()
    preprocessor.run()
    spacy_nlp.run()
    spotlight.run(spacy_nlp.tokens)

    # fuseki server needs to be up and running at this point,
    # with the uploaded knowledge base

    sparql = Sparql()
    sparql.query(
    """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX vivo: <http://vivoweb.org/ontology/core#>
    PREFIX exp: <http://example.org/property/>

    SELECT DISTINCT ?course ?title
    WHERE {
        ?course rdf:type vivo:Course.
        ?course vivo:title ?title.
        ?course exp:courseNumber ?num.
      FILTER (?num = "474")
    }
    """
    )


if __name__ == "__main__":
    main()
