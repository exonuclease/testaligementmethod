import glob
from multiprocessing import Process
import os.path
def worker(fname):
    areads = 0
    reads = 0
    file = open(fname)
    for line in file:
        areads = areads + int(line.split(',')[0].split('_')[1])
    file.close()
    fnames = glob.glob(r'/home/ldzeng/yfguo/jmzeng-summary/cluster/' + os.path.basename(fname)[0:8] + '*' + '.csv')
    for fn in fnames:
        file=open(fn)
        for line in file:
            reads = reads + int(line.split(',')[0].split('_')[1])
        file.close()
    filew = open(r'/home/ldzeng/yfguo/jmzeng-summary/cluster/MLS128/summary.csv','a')
    filew.write(os.path.basename(fname) + ',' + str(areads) + ',' + str(reads) + ',' + str(areads / reads) + '\n')
    filew.close()
fnames = glob.glob(r'/home/ldzeng/yfguo/jmzeng-summary/cluster/MLS128/*MLS128aligement.csv')
pool = []
if __name__ == '__main__':
    for fname in fnames:
        if os.path.getsize(fname) > 0:
            pool.append(Process(target=worker,args=(fname,)))
            pool[-1].start()
file=open(r'/home/ldzeng/yfguo/jmzeng-summary/cluster/MLS128/summary.csv')
lines=[]
for line in file:
    lines.append(line)
file.close()
lines.sort(reverse=True,key=lambda x:float(x.strip().split(',')[-1]))
filew=open(r'/home/ldzeng/yfguo/jmzeng-summary/cluster/MLS128/summary.csv','w')
for line in lines:
    filew.write(line)
filew.close()