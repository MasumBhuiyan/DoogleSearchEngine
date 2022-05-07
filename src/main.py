import subprocess 
from glob import glob 

if __name__ == "__main__":
    files = sorted(glob('./res/text/*.txt'))
    for file in files:
        #print("file: {}".format(file.split('/')[-1]))
        subprocess.run("cat {} | python src/mapper.py | sort | python src/reducer.py | python src/indexing.py >> report.txt".format(file, file), shell=True)