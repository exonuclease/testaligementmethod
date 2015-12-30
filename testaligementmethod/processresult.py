import glob
from multiprocessing import Process
def alignment(query,ref):
    catrgory={'A':1,'M':2,'T':3,'G':1,'L':1,'P':4,'V':1,'S':3,'C':2,'H':5,'Y':6,'R':5,'E':7,'D':7,'K':5,'F':6,'I':1,'N':8,'Q':8,'W':6}
    result=''
    for i in range(0,len(query)):
        if(query[i]==ref[i]):
            result=result+query[i]
        else:
            if(catrgory[query[i]]==catrgory[ref[i]]):
                result=result+'+'
            else:
                result=result+' '
    return result
def worker(fname):
    ref='QVQLQQSDAELVKPGASVKISCKASGYTFTDHAIHWVKQKPEQGLEWIGYISPGNGDIKYNEKFKGKATLTADKSSSTAYMQLNSLTSEDSAVYFCKRYYGNYDYWGQGTTLTVSS'
    lines=[]
    file=open(fname)
    for line in file:
        lines.append(line.strip())
    file.close()
    lines.sort(key=lambda x:x.strip().split(',')[-1],reverse=True)
    filew=open(fname[0:-4]+'res.txt','w')
    for line in lines: 
        filew.write(line.split(',')[0]+' '+line.split(',')[3]+'/'+line.split(',')[4]+'\n')
        filew.write('query  '+line.split(',')[1]+'\n')
        filew.write('       '+alignment(line.split(',')[1],ref)+'\n')
        filew.write('ref    '+ref+'\n')
    filew.close()
fnames = glob.glob(r'C:\Users\郭一凡\Documents\Visual Studio 2015\Projects\testaligementmethod\testaligementmethod\*aligement.csv')
pool = []
if __name__ == '__main__':
    for fname in fnames:
        pool.append(Process(target=worker,args=(fname,)))
        pool[-1].start()