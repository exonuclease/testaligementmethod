import glob
from multiprocessing import Process
import os.path
def worker(fname):
    file = open(fname)
    ratio = 0
    flag = False
    for line in file:
        if '_' in line:
            if line.split('_')[5] != 'IGHV1-78*01':
                flag = True
            else:
                ratio = ratio + float(line.split('_')[1])
    if flag:
        filew.write(os.path.split(fname)[1][0:7] + ',' + 'V gene is not IGHV1-78*01' + '\n')
    else:
        filew.write(os.path.split(fname)[1][0:7] + ',' + str(ratio) + '\n')
fnames = glob.glob(r'C:\Users\郭一凡\Documents\Visual Studio 2015\Projects\testaligementmethod\testaligementmethod\*aligementcnsortbyresemblance.txt')
filew = open(r'C:\Users\郭一凡\Documents\Visual Studio 2015\Projects\testaligementmethod\testaligementmethod\summary.txt','a')
pool = []
if __name__ == '__main__':
    for fname in fnames:
        pool.append(Process(target=worker,args=(fname,)))
        pool[-1].start()