import os
import tika
from pathlib import Path
from tika import parser
from .base import Base
from tqdm import tqdm
import spacy


class TikaPreprocessor(Base):
    def __init__(
        self,
        data_dir: Path = "data",
        res_dir: Path = "resources",
        rdf_dir: Path = "rdf",
        is_init: bool = True,
    ):
        super().__init__(
            data_dir=data_dir, res_dir=res_dir, rdf_dir=rdf_dir, is_init=is_init
        )
        tika.initVM()

    def preprocess_slides(self):
        for root, _, files in os.walk(self.res_dir):
            for file in tqdm(files, desc="Preprocessing resources.."):
                item = os.path.join(root, file)
                item = Path(item)
                parsed = parser.from_file(str(item))

                out_dir = self.data_dir / item.parent
                os.makedirs(out_dir, exist_ok=True)

                with open(out_dir / f"{item.stem}.txt", "w") as f:
                    f.write(parsed["content"])

    def run(self):
        self.preprocess_slides()


class SpacyNlp(Base):
    def __init__(
        self,
        data_dir: Path = "data",
        res_dir: Path = "resources",
        rdf_dir: Path = "rdf",
        is_init: bool = True,
        nlp_model: str = "en_core_web_sm",
    ):
        super().__init__(
            data_dir=data_dir, res_dir=res_dir, rdf_dir=rdf_dir, is_init=is_init
        )
        self.nlp = spacy.load(nlp_model)
        self.tokens = set()

    def tokenize(self):
        for root, _, files in os.walk(self.data_dir / "resources"):
            for file in tqdm(files, desc="Tokenizing.."):
                item = os.path.join(root, file)
                with open(item) as f:
                    doc = self.nlp(f.read())
                # for token in doc.ents:
                #     if token.label_ not in ["CARDINAL", "PERCENT", "DATE"]:
                #         print(token.text, token.label_)
                for token in doc:
                    if token.pos_ in ["PROPN", "NOUN"] and token.is_alpha and len(token) > 2:
                        self.tokens.add(token.text)
        print(f"Done. {len(self.tokens)} unique tokens added.")



    def run(self):
        self.tokenize()

def main():
    preprocessor = TikaPreprocessor(is_init=False)
    spacy_nlp = SpacyNlp()
    preprocessor.run()
    spacy_nlp.run()


if __name__ == "__main__":
    main()
