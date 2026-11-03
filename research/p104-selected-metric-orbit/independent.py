"""Independent selected-port energy replay in a nonorthogonal A8 basis.

Jerry Chen (@CubeJerry), with OpenAI Codex lead-agent assistance. Apache-2.0.
This imports no primary checker, geometry helper, or eigenvector certificate.
"""
import gzip, json, math, hashlib
from itertools import combinations, product
from pathlib import Path

source = Path(__file__).resolve().parents[2] / 'research/p104-helper470-twin-rung-removal/WORD.json.gz'
if hashlib.sha256(source.read_bytes()).hexdigest() != '7834725d9e34ee846a9ccc615221ea81e0201613938afa185d2eda0c9a6c232f':
    raise ValueError('selected word source mismatch')
ports = json.loads(gzip.decompress(source.read_bytes()))['ports']
def root(label):
    bits = [i for i in range(9) if label >> i & 1]
    if len(bits) == 3:
        return tuple(2 if i in bits else -1 for i in range(9))
    if len(bits) == 7:
        a,b = [i for i in range(9) if i not in bits]
        return tuple(3*(int(i==a)-int(i==b)) for i in range(9))
    raise ValueError(label)
roots = list(map(root,ports))
if not (len(set(ports)) == 104 and all(sum(v)==0 and sum(z*z for z in v)==18 for v in roots)):
    raise ValueError('selected root domain')
indices = [(i,i) for i in range(8)] + list(combinations(range(8),2))
H = [[0]*36 for _ in range(36)]
edges=0
for u,v in combinations(roots,2):
    if sum(x*y for x,y in zip(u,v)):
        continue
    edges+=1
    c=[u[i]*v[j] if i==j else u[i]*v[j]+u[j]*v[i] for i,j in indices]
    for i in range(36):
        for j in range(36): H[i][j]+=c[i]*c[j]
# B=(e_i-e_8), B^T B=I+J; 9*(B^T B)^-1=9I-J.
K=[[9*int(i==j)-1 for j in range(8)] for i in range(8)]
KE=[]
for i,j in indices:
    E=[[0]*8 for _ in range(8)]
    E[i][j]=E[j][i]=1
    KE.append([[sum(K[a][k]*E[k][b] for k in range(8)) for b in range(8)] for a in range(8)])
M=[[sum(KE[i][a][b]*KE[j][b][a] for a in range(8) for b in range(8)) for j in range(36)] for i in range(36)]
def rank(a):
    a=[row[:] for row in a]
    k=0
    for c in range(len(a[0])):
        p=next((i for i in range(k,len(a)) if a[i][c]),None)
        if p is None: continue
        a[k],a[p]=a[p],a[k]
        for i in range(k+1,len(a)):
            if not a[i][c]: continue
            q,pivot=a[i][c],a[k][c]
            a[i]=[pivot*x-q*y for x,y in zip(a[i],a[k])]
            g=math.gcd(*a[i])
            if g>1: a[i]=[x//g for x in a[i]]
        k+=1
    return k
observed={str(m)+'/4':36-rank([[H[i][j]-m*M[i][j] for j in range(36)] for i in range(36)]) for m in [0,150,151,152,165,182,199]}
expected={'0/4':1,'150/4':6,'151/4':8,'152/4':7,'165/4':4,'182/4':6,'199/4':4}
if observed!=expected: raise ValueError(observed)
if sum(observed.values()) !=36 or rank(M)!=36: raise ValueError('incomplete eigenspaces')
# A true coefficient perturbation must destroy the claimed complete spectrum.
changed=[row[:] for row in H]
changed[0][0]+=1
changed_dims={str(m)+'/4':36-rank([[changed[i][j]-m*M[i][j] for j in range(36)] for i in range(36)]) for m in [0,150,151,152,165,182,199]}
if changed_dims == expected:
    raise ValueError('coefficient fault escaped')
# Every original root sign is immaterial; a pair's coefficient outer product
# is unchanged under either sign. Check this directly for all retained pairs.
for u,v in combinations(roots,2):
    if sum(x*y for x,y in zip(u,v)): continue
    c=[u[i]*v[j] if i==j else u[i]*v[j]+u[j]*v[i] for i,j in indices]
    d=[(-u[i])*v[j] if i==j else (-u[i])*v[j]+(-u[j])*v[i] for i,j in indices]
    if any(x != -y for x,y in zip(c,d)):
        raise ValueError('sign covariance')
print(json.dumps({'status':'PASS_INDEPENDENT_A8_METRIC_SPECTRUM','word_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'ports':len(ports),'orthogonal_pairs':edges,'eigenspace_dimensions':observed,'metric_rank':rank(M),'coefficient_fault_rejected':True,'sign_covariance_pairs':edges,'method':'Direct 104-port energy in nonorthogonal A8 basis; fraction-free integer elimination; no predecessor or worker code imports'},indent=2))

# Independently check the Hermitian extension in the original 9D A8 coordinates.
# H = 202 M + cross corresponds to E_P(K) = (101/2)||K||^2 + X_FG.
labels=[sum(1<<i for i in s) for k in (3,7) for s in combinations(range(9),k)]
full=[root(q) for q in labels]
dot=lambda x,y:sum(a*b for a,b in zip(x,y))
for i in range(9):
 for j in range(9):
  if sum(u[i]*u[j] for u in full)!=270*int(i==j)-30:raise ValueError('full tight frame')
for r in full:
 star=[s for s in full if dot(r,s)==0]
 if len(star)!=63:raise ValueError('star count')
 for i in range(9):
  for j in range(9):
   if sum(s[i]*s[j] for s in star)!=162*int(i==j)-18-9*r[i]*r[j]:raise ValueError('star moment')
indices=list(combinations(range(8),2))
def energy(pairs):
 out=[[0]*28 for _ in range(28)]
 for u,v in pairs:
  if dot(u,v):continue
  c=[u[i]*v[j]-u[j]*v[i] for i,j in indices]
  for i in range(28):
   for j in range(28):out[i][j]+=c[i]*c[j]
 return out
KE=[]
for i,j in indices:
 E=[[0]*8 for _ in range(8)];E[i][j]=1;E[j][i]=-1
 KE.append([[sum(K[a][k]*E[k][b] for k in range(8)) for b in range(8)] for a in range(8)])
M=[[-sum(KE[i][a][b]*KE[j][b][a] for a in range(8) for b in range(8)) for j in range(28)] for i in range(28)]
F=set([7,25,42,52,76,82,97,127]);G=set(labels)-set(ports)-F
if len(G)!=8 or len(F)!=8 or F&G or F|G!=set(labels)-set(ports):raise ValueError('complement')
for frame in (F,G):
 if any(dot(root(a),root(b)) for a,b in combinations(frame,2)):raise ValueError('nonorthogonal frame')
H=energy(combinations(roots,2))
cross=energy(product([root(q) for q in F],[root(q) for q in G]))
if any(H[i][j]!=202*M[i][j]+cross[i][j] for i in range(28) for j in range(28)):raise ValueError('skew puncture identity')
if rank(M)!=28:raise ValueError('skew metric rank')
print(json.dumps({'status':'PASS_INDEPENDENT_HERMITIAN_EXTENSION','full_second_moment_entries':81,'star_second_moment_entries':9720,'skew_identity_entries':784,'skew_minimum_guarantee':'101/2','selected_skew_equality_dimension':28-rank(cross)},indent=2))
