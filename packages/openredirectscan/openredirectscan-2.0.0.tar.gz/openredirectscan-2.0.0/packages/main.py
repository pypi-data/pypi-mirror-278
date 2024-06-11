import argparse
import webbrowser
from includes import scan
from utils import banner,  chknet

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="Enter URL")
parser.add_argument("-i", "--input", help="Enter input file name")
parser.add_argument("-o", "--output", help="Enter the output file name", default="output.txt")
parser.add_argument("-b", "--blog", action='store_true', help="Open the blog")
args = parser.parse_args()

def main():
    if args.url:
        banner.banner()
        result = scan.process_url(args.url)
        print(result)
    
    if args.input:
        banner.banner()
        with open(args.input, 'r') as file:
            urls = file.readlines()
        results = []
        for url in urls:
            result = scan.process_url(url.strip())
            results.append(result)
        with open(args.output, 'w') as file:
            for result in results:
                file.write(result + '\n')

    if args.blog:
        banner.banner()
        webbrowser.open('https://blogs.cappriciosec.com/')

if __name__ == "__main__":
    if chknet.net():
        main()
    else:
        print("\ncheck internet")
   