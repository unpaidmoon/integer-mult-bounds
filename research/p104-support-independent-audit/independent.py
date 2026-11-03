"""Independent support stability census, without package or predecessor imports.

Jerry Chen (@CubeJerry), with OpenAI Codex worker B assistance. Apache-2.0.
Finite corroboration of the written theorem; no physical supplier claim.
"""
from itertools import product, combinations
from collections import Counter
from pathlib import Path
from hashlib import sha256
import gzip, json


def rank(a, p):
    a = [[x % p for x in row] for row in a]
    h = 0
    for j in range(len(a[0]) if a else 0):
        k = next((k for k in range(h, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[k], a[h] = a[h], a[k]
        inv = pow(a[h][j], -1, p)
        a[h] = [(v * inv) % p for v in a[h]]
        for k in range(h+1, len(a)):
            if a[k][j]:
                t = a[k][j]
                a[k] = [(v-t*w) % p for v,w in zip(a[k], a[h])]
        h += 1
    return h

def good(a, retained, p):
    # Direct forbidden-pattern characterization, without decomposition.
    for i in retained:
        neighbors = [j for j in retained if i != j and (a[i][j] % p or a[j][i] % p)]
        if len(neighbors) > 1:
            return False
        if neighbors and a[i][neighbors[0]] * a[neighbors[0]][i] % p != 1:
            return False
    return True

def distance(a,p):
    n=len(a)
    for k in range(n,-1,-1):
        for kept in combinations(range(n),k):
            if good(a,kept,p):
                return n-k
    raise RuntimeError('empty matrix must be good')

root=Path(__file__).resolve().parents[2]
raw=(root/'research/p104-helper-subspace-splits/WORD.json.gz').read_bytes()
if sha256(raw).hexdigest()!='bbb072bced5824a8d9094c49be2fc51fbfdd05fb2b7dab8106e1275053075099':
    raise RuntimeError('port source hash')
ports=json.loads(gzip.decompress(raw))['ports']

positions=[(i,j) for i in range(4) for j in range(4) if i!=j]
stats=Counter()
for vals in product(range(3),repeat=12):
    a=[[int(i==j) for j in range(4)] for i in range(4)]
    for (i,j),v in zip(positions,vals):
        a[i][j]=v
    r=rank(a,3)
    s=sum(v!=0 for v in vals)-2*(4-r)
    d=distance(a,3)
    if s<0 or d>2*s:
        raise RuntimeError(('counterexample',a,r,s,d))
    stats[(s,d)]+=1

# Independently verify the rank routine on all 3x3 matrices with diagonal 1
# by counting the complete kernel, not elimination or determinant minors.
kernel_cases=0
for vals in product(range(3),repeat=6):
    a=[[int(i==j) for j in range(3)] for i in range(3)]
    for (i,j),v in zip(((i,j) for i in range(3) for j in range(3) if i!=j),vals):
        a[i][j]=v
    kernel_count=sum(all(sum(ai*xj for ai,xj in zip(row,x))%3==0 for row in a)
                     for x in product(range(3),repeat=3))
    if kernel_count!=3**(3-rank(a,3)):
        raise RuntimeError('kernel rank disagreement')
    kernel_cases+=1

allowed=lambda i,j:(ports[i]&ports[j]).bit_count()%2==0
if not all(allowed(i,j) for i,j in combinations(range(3),2)):
    raise RuntimeError('triangle not allowed')
unused=list(range(3,104)); pairs=[]
for _ in range(47):
    i=unused.pop(0)
    j=next(j for j in unused if allowed(i,j))
    unused.remove(j);pairs.append((i,j))
a=[[int(i==j) for j in range(104)] for i in range(104)]
a[0][1]=a[1][2]=1;a[2][0]=-1
for i,j in pairs:a[i][j]=a[j][i]=1
if any(a[i][j] and i!=j and not allowed(i,j) for i in range(104) for j in range(104)):
    raise RuntimeError('mask violation')
p104=[]
for p in (2,3,5,7,11,13):
    r=rank(a,p);m=sum(a[i][j]%p!=0 for i in range(104) for j in range(104) if i!=j)
    if (r,m)!=(56,97):raise RuntimeError('P104 rank/support')
    for gone in range(104):
        if good(a,[i for i in range(104) if i!=gone],p):
            raise RuntimeError('one deletion should fail')
    if not good(a,[i for i in range(104) if i not in (1,2)],p):
        raise RuntimeError('two deletions should work')
    p104.append({'p':p,'rank':r,'m':m})

if sum(stats.values())!=531441 or kernel_cases!=729 or stats[(1,2)]!=32:
    raise RuntimeError('coverage or sharpness census mismatch')

print(json.dumps({'status':'PASS_INDEPENDENT_C_STABILITY_AUDIT','all_4x4_F3':sum(stats.values()),
    'kernel_count_rank_oracle_3x3_F3':kernel_cases,
    's0_cases':sum(v for (s,d),v in stats.items() if s==0),
    'sharp_s1_distance2_cases':stats[(1,2)],
    'p104':p104,'source_ports_first3':ports[:3]},sort_keys=True))
