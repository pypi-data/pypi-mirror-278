import os
import pandas as pd
import numpy as np
import shutil
from joblib import Parallel, delayed
import logging
log_out = logging.getLogger('log_out')
log_out.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename='m3c.log', mode='w')
log_out.addHandler(fh)
log_out.debug('*********run make3dg*********')

path = '/cluster/home/Kangwen/Hic/data_new'
dr = 'sn_m3c_hum'
sh = '/cluster/home/Kangwen/Hic/analysis/dip-c-master/generate_cif.sh'
out = '/cluster/home/Kangwen/Hic/merge_pair/single_m3c_hum'


task = []
for r,d, fs in os.walk(path):
    for f in fs:
        if f.endswith('.pairs.gz') and 'dedup' in f:
            name = f.split('.')[0]
            task.append((os.path.join(r,f), name))

log_out.info('task is %s' % task)

def make_3dg(dr, name):
    cmd = 'bash %s %s %s %s' % (sh, dr, name, out)
    log_out.info('deal with %s' % name)
    
    res = os.system(cmd)
    log_out.info('finish %s : %s' % (name, res))

Parallel(n_jobs=5)(delayed(make_3dg)(dr, name) for dr, name in task)