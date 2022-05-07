from genericpath import isdir, isfile
import subprocess
from tqdm import tqdm
import time
import PyPDF2
from urllib.request import Request, urlopen
import os
from glob import glob 
from google.cloud import storage
import argparse
from pprint import pprint
from prettytable import PrettyTable

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--keys', nargs='+')

DOWNLOAD_DIR = "./res/pdf/"
MAP_REDUCE_INPUT_DIR = "./res/text/"

print("\033[1;32m ### Google Cloud Storage \033[0m", end="")
print("\033[1;32mconnected\033[0m")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'token.json'
storage_client = storage.Client()
bucket_name = 'map-reduce-s3'

"""
Get Bucket
"""
my_bucket = storage_client.get_bucket(bucket_name)
pprint(vars(my_bucket))

class PDF:
    def __init__(self, url, file):
        self.url = url 
        self.file = file 
    
    # def download(self):
    #     response = urlopen(Request(self.url, headers={'User-Agent': 'Mozilla/5.0'}))    
    #     file = open(os.path.join(DOWNLOAD_DIR, self.file + ".pdf"), 'wb')
    #     file.write(response.read())
    #     file.close()

    def download(self):
        location = os.path.join(DOWNLOAD_DIR, self.file + ".pdf")
        with open(location, 'wb') as f:
            storage_client.download_blob_to_file(uri, f)
    
    def extractText(self):
        readFile = open(os.path.join(DOWNLOAD_DIR, self.file + ".pdf"), "rb")
        writeFile = open(os.path.join(MAP_REDUCE_INPUT_DIR, self.file + ".txt"), "w")
        reader = PyPDF2.PdfFileReader(readFile)
        
        i = 0
        self.textData = ""
        while i < reader.numPages:
            self.textData += reader.getPage(i).extractText()
            i += 1

        writeFile.write(self.textData)
        readFile.close()
        writeFile.close()

if __name__ == "__main__":
    args = parser.parse_args()
    
    keys = args.keys
    # print(keys)

    with open("keys.txt", 'w') as f:
        f.writelines(keys)

    print("\033[1;32m ### Keywords: {}\033[0m".format(keys))

    DOCS = 10
    for i in range(DOCS):
        uri = 'gs://cloud-security-s3/input-{}.pdf'.format(i + 1)
        saveTo = 'input-{}'.format(i + 1)

        if(isfile(MAP_REDUCE_INPUT_DIR + saveTo + ".txt")):
            continue
        
        paper = PDF(uri.format(i + 1), saveTo)
        paper.download()
        paper.extractText()

    files = sorted(glob(MAP_REDUCE_INPUT_DIR + "*"))

    for file in files:
        subprocess.run("cat {} | python src/mapper.py | sort | python src/reducer.py | python src/indexing.py >> report.txt".format(file, file, keys), shell=True)

    print("\033[1;32m ### Running mapper\033[0m")
    print("\033[1;32m ### Running reducer\033[0m")
    print("\033[1;32m ### Indexing results\033[0m")



    docs = []
    with open('res/docsList.txt', 'r') as f:
        while True:
            doc = f.readline()
            # print(doc)
            if not doc:
                break 
            docs.append(doc)

    
    reports = []
    i = 0
    with open('report.txt', 'r') as file:
        while True:
            point = file.readline()
           # print(point, docs[i])
            if not point or i > 9:
                break 
            reports.append([-int(point), docs[i]])
            i += 1

    reports = sorted(reports)


    for i in range(len(reports)):
        point = -reports[i][0]
        doc = reports[i][1]
        reports[i] = [i + 1, doc, point]

    
    print("\033[1;32m ### Results\033[0m")
    table = PrettyTable(['Rank', 'Paper', 'Relevance'])
    for report in reports:
        table.add_row(report)
    print(table)


    file = open("report.txt","r+")
    file. truncate(0)
    file. close()

    file = open("keys.txt","r+")
    file. truncate(0)
    file. close()

