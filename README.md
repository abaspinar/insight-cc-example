Insight Data Engineering - Coding Challenge
===========================================================

The program is tested on python 2.7.6.

run.sh script file calls python script runner.py.

runner.py handles both features at the same time.

runner.py script requires 4 arguments;

Location of tweets.txt,
Location to save feature1,
Location to save feature2,
chunkSize for processes.

runner script uses multiprocessing library of python.

Algorithm to extract the features is given below;

1-Get line count to divide equal workload on processes
2-Create a pool of processes wrt cpu number
3-Initialize processes with equal number of line numbers
4-Each process reads file and create word count and dictionary for that part of the file concurrently.
5-Word counts are written on temp#.txt files.
6-Dictionaries are returned from pool.
7-Starting from temp0.txt files are merged and median_unique is generated.
8-Afterwards dictionaries from pool outputs are merged and word count feauture is also generated.

The main advantage is file can be processed using all cpu power of the single computer concurrently.
The disadvantage might be the memory limit, therefore I added extra parameter chunkSize to divide workload among processes. 
