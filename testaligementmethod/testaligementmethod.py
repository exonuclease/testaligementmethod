from math import log2
import glob
from multiprocessing import Process
def cpsfm(lines):
    n = len(lines)
    psfm = []
    for i in range(0,len(lines[0])):
        psfm.append({})
        for line in lines:
            if line[i] in psfm[i]:
                psfm[i][line[i]] = psfm[i][line[i]] + 1 / n
            else:
                psfm[i][line[i]] = 1 / n
        for i in range(0,len(psfm)):
            se = 0
            for feq in psfm[i].values():
                se = se - feq * log2(feq)
            if se > 1.7:
                psfm[i] = {}
    return psfm
def cprob(seqs,psfm):
    probs = []
    for i in range(0,len(seqs)):
        prob = 1
        for j in range(0,len(seqs[i])):
            if psfm[j]:
                if seqs[i][j] in psfm[j]:
                    prob = prob * psfm[j][seqs[i][j]]
                else:
                    prob = prob * 0.01
        probs.append(prob)
    return probs
def worker(fname):
    file = open(r'/home/ldzeng/yfguo/jmzeng-summary/cluster/MLS128/trainset.txt')
    trainset = []
    for line in file:
        for i in range(0,2):
            trainset.append(line.strip())
    file.close()
    file = open(fname)
    lines = []
    seqs = []
    for line in file:
        if line.split(',')[-1] == '98\n':
            lines.append(line.strip())
    file.close()
    for line in lines:
        seqs.append(line.split(',')[-4])
    if 0.0001 * len(seqs) < 1:
        tsize = 0
    else:
        tsize = int(0.0001 * len(seqs))
    for i in range(0,5):
        psfm = cpsfm(trainset)
        probs = cprob(seqs,psfm)
        for i in range(0,tsize):
            trainset.append(seqs.pop(probs.index(max(probs))))
            del probs[probs.index(max(probs))]
    seqs = []
    for line in lines:
        seqs.append(line.split(',')[-4])
    probs = cprob(seqs,psfm)
    file = open(r'/home/ldzeng/yfguo/jmzeng-summary/cluster/MLS128/trainset.txt')
    ptrainset = []
    for line in file:
        ptrainset.append(line.strip())
    tprobs = cprob(ptrainset,psfm)
    cutoff = min(tprobs)
    file.close()
    filew = open(fname[0:-4] + 'aligementall.csv','w')
    for i in range(0,len(lines)):
        if probs[i] > 0:
            filew.write(lines[i] + ',' + str(probs[i]) + '\n')
    filew.close()
    filew = open(fname[0:-4] + 'aligement.csv','w')
    for i in range(0,len(lines)):
        if probs[i] > cutoff:
            filew.write(lines[i] + ',' + str(probs[i]) + '\n')
    filew.close()
fnames = glob.glob(r'/home/ldzeng/yfguo/jmzeng-summary/cluster/MLS128/*MLS128.csv')
pool = []
if __name__ == '__main__':
    for fname in fnames:
        pool.append(Process(target=worker,args=(fname,)))
        pool[-1].start()