import multiprocessing as multi
import sys
global infileName
global outfileName1
global outfileName2
#chunkSize specifies the number of lines to work for each process
global chunkSize

#counts number of lines in file to divide job size to similar chunks among processes
def file_len():
    with open(infileName) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def start_process():
    print 'Starting', multi.current_process().name

def processFile(start):
    aDict = {}
    with open(infileName) as infile:
        f = open('temp%d.txt' %start, 'w')
        for i,line in enumerate(infile):
            if start <= i < (start+chunkSize):
                value,dict = process(line)
                for key in dict:
                    try:
                        aDict[key] += dict[key]
                    except:
                        aDict[key] = dict[key]
                aDict.update(dict)
                f.write(value+'\n')
        f.close()
    return aDict

#Read each line and create number of unique words and also a dictionary with word:count pairs
def process(line):
    aDict = {}
    temp = line.strip()
    words = line.split()
    count = 0
    for word in words:
        try:
            aDict[word] += 1
        except:
            aDict[word] = 1
            count += 1
    return str(count),aDict

def run():
    #creates cpu count * 2 times processes
    pool_size = multi.cpu_count() * 2
    #initialize multiprocessing pool
    pool = multi.Pool(processes=pool_size,
                                    initializer=start_process,
                                    maxtasksperchild=2,
                                    )

    inputs = range(0,file_len(),chunkSize)
    #pool map function calls processFile with args in inputs processFile returns dictionary
    pool_outputs = pool.map(processFile,inputs)
    pool.close()
    pool.join()

    #calculate the median_unique
    count = 0
    prev = 0
    fhnd = open(outfileName2,'w')
    for fid in inputs:
        try:
            with open('temp%d.txt' %fid) as f:
                for line in f:
                    value = line.strip()
                    median = float((prev * count) + int(value))/(count+1)
                    count += 1
                    prev = median
                    fhnd.write('%g\n' %median)
        except:
            print 'temp%d.txt' %fid + ' does not exitst.'
    fhnd.close()

    #Calculates and writes total number of times each word has been tweeted
    aDict = {}
    for dd in pool_outputs:
        for key in dd:
            try:
                aDict[key] += dd[key]
            except:
                aDict[key] = dd[key]

    fhnd = open(outfileName1,'w')
    for key in sorted(aDict):
        fhnd.write(key+'\t'+str(aDict[key])+'\n')
    fhnd.close()

if len(sys.argv) != 5:
    print 'Invalid format:'
    print 'Correct format: python ./src/runner.py tweet_input tweet_output median_output chunkSize'
else:
    infileName = sys.argv[1]
    outfileName1 = sys.argv[2]
    outfileName2 = sys.argv[3]
    chunkSize = int(sys.argv[4])
    run()
