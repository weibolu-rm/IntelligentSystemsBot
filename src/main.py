from intelligent_system_bot.rdf import DataBuilder
from intelligent_system_bot.parse import TikaPreprocessor

def main():
    data_builder = DataBuilder()
    preprocessor = TikaPreprocessor()

    data_builder.run()
    preprocessor.run()

if __name__ == "__main__":
    main()
