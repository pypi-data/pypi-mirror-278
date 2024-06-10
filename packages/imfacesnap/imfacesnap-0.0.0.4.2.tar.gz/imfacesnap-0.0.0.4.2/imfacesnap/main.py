import argparse
from pathlib import Path
import os

def main():
    parser = argparse.ArgumentParser("imface cli for image vector")
    parser.add_argument("-v", "--version", help="version", default=False, action="store_true")
    
    subparsers = parser.add_subparsers(dest="command")
    #generate vector represent
    represent_parser = subparsers.add_parser("represent")
    represent_parser.add_argument("-p", "--path", help="path image file", required=True)
    represent_parser.add_argument("-d", "--detector", help="detector", required=True)
    represent_parser.add_argument("-t", "--threshold", help="Face Detector Threshold", required=False, default=0.75)
    represent_parser.add_argument('-check_blurry', action='store_true')

    #generate vector selfie
    selfie_parser = subparsers.add_parser("selfie")
    selfie_parser.add_argument("-p", "--path", help="path image file", required=True)
    selfie_parser.add_argument("-d", "--detector", help="detector", required=True)
    #generate image album
    generate_parser = subparsers.add_parser("generate-crop-img")
    generate_parser.add_argument("-p", "--path", help="path to image file", required=True)
    generate_parser.add_argument("-o", "--output", help="directory to save image", required=True)
    generate_parser.add_argument("-d", "--detector", help="face detector", required=True)
    generate_parser.add_argument("-t", "--threshold", help="Face Detector Threshold", required=False, default=0.75)
    generate_parser.add_argument('-check_blurry', action='store_true')

    args = parser.parse_args()

    version =  "0.0.0.4.2"
    if args.version:
        os.environ.setdefault("DEEPFACE_HOME", "/app")
        print(version + str(os.getenv("DEEPFACE_HOME", default=str(Path.home()))))
        exit(0)

    elif args.command == "represent":
        try:
            os.environ.setdefault("DEEPFACE_HOME", "/app")

            from imfacesnap.utils import deepface_util as utils
            embed = utils.get_embedding_vector(path=args.path, detector=args.detector, threshold=float(args.threshold), check_blurry=args.check_blurry)
            print(embed)
        except Exception as e:
            print("error " + repr(e))
            raise SystemExit(1)

    elif args.command == "selfie":
        try:
            os.environ.setdefault("DEEPFACE_HOME", "/app")
            
            from imfacesnap.utils import deepface_util as utils
            data = utils.extract_face(path=args.path, detector=args.detector)
            if len(data) > 1:
                print("error only allowed one face")
                raise SystemExit(1)
            else:
                print(data[0]['embedding'])
        except Exception as e:
            print("error" + repr(e))
            raise SystemExit(1)

    elif args.command == "generate-crop-img":
        try:
            os.environ.setdefault("DEEPFACE_HOME", "/app")
            if not os.path.exists(args.output):
                os.makedirs(args.output)

            from imfacesnap.utils import deepface_util as utils
            file_names = utils.generate_faces_image(path=args.path, album_dir=args.output, detector=args.detector, threshold=float(args.threshold), check_blurry=args.check_blurry)
            print(file_names)
        except Exception as e:
            print("error " + repr(e))
            raise SystemExit(1)

if __name__ == "__main__":
    main()