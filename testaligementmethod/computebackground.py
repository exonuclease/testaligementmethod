from multiprocessing import Manager,pool
import pickle
import glob
def worker(fname,bg):
    seqs = []
    file = open(fname)
    for line in file:
        if line.split(',')[-1] == '98\n':
            seqs.append(line.strip().split(',')[-4])
    file.close()
    for seq in seqs:
        for aa in list(seq):
            bg[aa] = bg[aa] + 1
if __name__ == '__main__':
    m = Manager()
    bg = m.dict()
    for aa in list('ARDCQEHIGNLKMFPSTWYV-'):
        bg[aa] = 0
    fnames = glob.glob(r'C:\Users\郭一凡\Documents\Visual Studio 2015\Projects\testaligementmethod\testaligementmethod\1-new-D.clusterresh-MLS128.csv')
    p = pool.Pool(processes=3)
    for fname in fnames:
        p.apply_async(worker,(fname,bg))
    p.close()
    p.join()
    sum = 0
    for value in bg.values():
        sum = sum + value
    for key in bg.keys():
        bg[key] = bg[key] / sum
    bg=dict(bg)
    filew = open(r'C:\Users\郭一凡\Documents\Visual Studio 2015\Projects\testaligementmethod\testaligementmethod\background.pkl','wb')
    pickle.dump(bg,filew)