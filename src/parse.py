import os
import tika
from tika import parser

def main():

    tika.initVM()

    
    # TODO: do something with this
    res_dir = "resources/courses/COMP432/lectures"
    for f in os.listdir(res_dir):
        parsed = parser.from_file(f"{res_dir}/{f}")
        print(parsed["metadata"])
        print(parsed["content"])



if __name__ == "__main__":
    main()
