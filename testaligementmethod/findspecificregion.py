import glob
from math import log2,log10,pow
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
    return psfm
def cprob(start,seq,psfm):
    for i in range(0,len(seq)):
        prob = 1
        if psfm[start + i]:
            if seq[i] in psfm[start + i]:
                prob = prob * psfm[start + i][seq[i]]
            else:
                prob = prob * 0.01
    return prob
fnames = glob.glob(r'C:\Users\郭一凡\Documents\Visual Studio 2015\Projects\testaligementmethod\testaligementmethod\*MLS128.csv')
seqs = []
for fname in fnames:
    file = open(fname)
    for line in file:
        if line and len(line.strip().split(',')[1]) == 98:
            seqs.append(line.strip().split(',')[1])
    file.close()
bpsfm = cpsfm(seqs)
primers = []
file = open('preprobs.txt')
for line in file:
    primers.append(line.strip().split(','))
file.close()
for i in range(0,len(primers)):
    start = int(primers[i][0])
    bprob = cprob(start,primers[i][1],bpsfm)
    ratio = float(primers[i][2]) / bprob
    primers[i].extend([bprob,ratio])
primers.sort(key=lambda x:x[-1],reverse=True)
filew = open('preprobs.txt','w')
for pri in primers:
    filew.write(','.join([str(i) for i in pri]) + '\n')
filew.close()
filew = open('allseqscon.txt','w')
for i in range(0,len(bpsfm)):
    se = 0
    for feq in bpsfm[i].values():
        se = se - feq * log2(feq)
    repaa = ''
    repaafeq = 0
    for aa,feq in bpsfm[i].items():
        if feq > repaafeq:
            repaa = aa
            repaafeq = feq
    filew.write(str(i) + ',' + repaa + ',' + str(repaafeq) + ',' + str(-log10(se)) + '\n')
filew.close()