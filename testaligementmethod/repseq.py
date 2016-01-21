import glob
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
fnames = glob.glob(r'C:\Users\郭一凡\Documents\Visual Studio 2015\Projects\testaligementmethod\testaligementmethod\rawreads\*lg*.txt')
for fname in fnames:
    seqs = []
    file = open(fname)
    for line in file:
        seqs.append(line.strip())
    file.close()
psfm = cpsfm(seqs)
filew = open(r'mostprobseq.txt','w')
repseq = ''
for i in range(0,len(psfm)):
    repaa = ''
    repaafeq = 0
    for aa,feq in psfm[i].items():
        if feq > repaafeq:
            repaa = aa
            repaafeq = feq
    repseq = repseq + repaa
filew.write(repseq + '\n')
aaseq = []
file = open(r'C:\Users\郭一凡\Documents\Visual Studio 2015\Projects\testaligementmethod\testaligementmethod\rawreads\allseqs.txt')
for line in file:
    aaseq.append(line.split(',')[1])
aaseq.reverse()
output = ''
for aa in aaseq:
    output = output + ' ' + aa + ' '
filew.write(output)
filew.close()