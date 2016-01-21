import glob
from math import log2,log10
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
fnames = glob.glob(r'C:\Users\郭一凡\Documents\Visual Studio 2015\Projects\testaligementmethod\testaligementmethod\*aligement.csv')
for fname in fnames:
    seqs = []
    file = open(fname)
    filew = open(fname[0:-4] + 'consregion.txt','w')
    for line in file:
        seqs.append(line.split(',')[1])
    file.close()
    if seqs == []:
        continue
    psfm = cpsfm(seqs)
    for i in range(0,len(psfm)):
        if psfm[i] == {}:
            filew.write(str(i) + ',N,0,0' + '\n')
        se = 0
        for feq in psfm[i].values():
            se = se - feq * log2(feq)
        repaa = ''
        repaafeq = 0
        for aa,feq in psfm[i].items():
            if feq > repaafeq:
                repaa = aa
                repaafeq = feq
        filew.write(str(i) + ',' + repaa + ',' + str(repaafeq) + ',' + str(-log10(se + 0.3)) + '\n')
    filew.close()
seqs = []
filew = open('allseqs.txt','w')
for fname in fnames:
    file = open(fname)
    for line in file:
        seqs.append(line.split(',')[1])
    file.close()
psfm = cpsfm(seqs)
for i in range(0,len(psfm)):
    if psfm[i] == {}:
        filew.write(str(i) + ',N,0,0' + '\n')
    se = 0
    for feq in psfm[i].values():
        se = se - feq * log2(feq)
    repaa = ''
    repaafeq = 0
    for aa,feq in psfm[i].items():
        if feq > repaafeq:
            repaa = aa
            repaafeq = feq
    filew.write(str(i) + ',' + repaa + ',' + str(repaafeq) + ',' + str(-log10(se)) + '\n')
filew.close()
lines = []
primers = []
file = open('allseqs.txt')
for line in file:
    lines.append((line.strip().split(',')))
filew.close()
for i in range(0,len(lines) - 7):
    seq = ''
    prob = 1
    for j in range(i,i + 7):
        seq = seq + lines[j][1]
        prob = prob * float(lines[j][2])
    primers.append([i,seq,prob])
primers.sort(key=lambda x:x[2],reverse=True)
filew = open('preprobs.txt','w')
for pri in primers:
    filew.write(','.join([str(i) for i in pri]) + '\n')
filew.close()