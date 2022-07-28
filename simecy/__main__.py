
import os
import argparse
from .simecy import decode, encode

def main(args):
    assert os.path.exists(
        args.file_path), "{} file is not exists".format(args.file_path)
    if args.mode in ("encode", "e"):
        encode(args.file_path, args.password)
    elif args.mode in ("decode", "d"):
        decode(args.file_path, args.password)
    else:
        print("please run python -m simecy -h")
    print("simecy work done!")



def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-f", "--file_path", type=str, required=True,
                        help="need encode or decode file")
    parser.add_argument("-m", "--mode", type=str, default="encode", choices=[
                        "encode", "decode", "e", "d"], help=" will encode or decode,the value must be in decode,encode,d,e")
    parser.add_argument("-pd", "--password", type=str,
                        default="imsohandsome")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    main(args)
