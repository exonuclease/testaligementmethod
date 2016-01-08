import glob
from multiprocessing import Process
import os.path
def alignment(query,ref):
    catrgory = {'A':1,'M':2,'T':3,'G':1,'L':1,'P':4,'V':1,'S':3,'C':2,'H':5,'Y':6,'R':5,'E':7,'D':7,'K':5,'F':6,'I':1,'N':8,'Q':8,'W':6,'-':9}
    result = ''
    for i in range(0,len(query)):
        if(query[i] == ref[i]):
            result = result + query[i]
        else:
            if(catrgory[query[i]] == catrgory[ref[i]]):
                result = result + '+'
            else:
                result = result + ' '
    return result
def worker(fname):
    ref = 'QVQLQQSDAELVKPGASVKISCKASGYTFTDHAIHWVKQKPEQGLEWIGYISPGNGDIKYNEKFKGKATLTADKSSSTAYMQLNSLTSEDSAVYFCKRYYGNYDYWGQGTTLTVSS'
    tags = []
    seqs = []
    ntarget = 0
    file = open(fname)
    for line in file:
        if '>' in line:
            tags.append(line[1:].strip())
        else:
            seqs.append(line.strip())
    file.close()
    p,f = os.path.split(fname)
    file = open(os.path.join(p,f[0:8] + 'clusterresh-MLS128.csv'))
    for line in file:
        if line.split('_')[3] == 'IGHV1-78*01':
            ntarget = ntarget + 1
    file.close()
    for i in range(0,len(tags)):
        ratio = 100 * int(tags[i].split('_')[0]) / ntarget
        newtag = tags[i].split('_')
        newtag.insert(1,str(ratio))
        tags[i] = '_'.join(newtag)
    seqs = sorted(seqs,key=lambda x:float(tags[seqs.index(x)].split('_')[-1]),reverse=True)
    tags.sort(key=lambda x:float(x.split('_')[-1]),reverse=True)
    filew = open(fname[0:-4] + 'sortbyresemblance.txt','w')
    for i in range(0,len(tags)):
        filew.write(tags[i] + '\n')
        filew.write('query  ' + seqs[i] + '\n')
        filew.write('       ' + alignment(seqs[i],ref) + '\n')
        filew.write('ref    ' + ref + '\n')
    filew.close()
fnames = glob.glob(r'C:\Users\郭一凡\Documents\Visual Studio 2015\Projects\testaligementmethod\testaligementmethod\*aligementcnt.fa')
pool = []
if __name__ == '__main__':
    for fname in fnames:
        pool.append(Process(target=worker,args=(fname,)))
        pool[-1].start()