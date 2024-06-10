import gzip
import sys
import os
chromsome = ['chr%s' % i for i in range(1,20)]
chromsome += ['chrX','chrY']

pairs = sys.argv[1]
out = sys.argv[2]

with gzip.open(pairs, 'r') as f:
    lines  = f.readlines()

lines = [x.decode().strip() for x in lines]

new_lines = []
for l in lines:
    if l.startswith('#'):
        if '_' in l and '@PG' not in l and '#columns:' not in l :
       
            continue
        else:
            new_lines.append(l)
    else:
        tmp = l.split('\t')
        if tmp[1] not in chromsome or tmp[3] not in chromsome:
            
                continue
        else:
            new_lines.append(tmp)

if out.endswith('gz'):
    out = out[:-3]
with open(out, 'w+') as f:
    for l in new_lines:
        if type(l) == str:
            if l.startswith('#'):
                f.write(l)
                f.write('\n')
        else:
            tmp = '\t'.join(l)
            f.write(tmp)
            f.write('\n')

f.close()

os.system('gzip %s' % out)