import os
import tika
from pathlib import Path
from tika import parser


class TikaPreprocessor:
    def __init__(
        self,
        data_dir: Path = "data",
        res_dir: Path = "resources",
    ):
        self.data_dir = Path(data_dir)
        self.res_dir = Path(res_dir)
        self._initialize_dirs()
        tika.initVM()

    def _initialize_dirs(self):
        os.makedirs(self.data_dir, exist_ok=True)

    def preprocess_slides(self):
        for root, _, files in os.walk(self.res_dir):
            for file in files:
                item = os.path.join(root, file)
                item = Path(item)
                parsed = parser.from_file(str(item))

                out_dir = self.data_dir / item.parent
                os.makedirs(out_dir, exist_ok=True)

                with open(out_dir / f"{item.stem}.txt", "w") as f:
                    f.write(parsed["content"])


    def run(self):
        print("Preprocessing resources...")
        self.preprocess_slides()

def main():
    preprocessor = TikaPreprocessor()
    preprocessor.run()


if __name__ == "__main__":
    main()
