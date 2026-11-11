"""Independent A8-chart spectral review; no author eigenspace data/code imported.

Jerry Chen, @CubeJerry; OpenAI Codex assistance, worker D seed79. Apache-2.0.
Use integer root representatives 3r in R^9, and physical symmetric operators
A=B S B^t, B=[e_0-e_8,...,e_7-e_8]. Energy=s^t H s/4.
"""
from fractions import Fraction as Q
from itertools import combinations
from hashlib import sha256
from pathlib import Path
from math import gcd
import argparse,json

F=(7,25,42,52,76,82,97,127)
REPS=((11,21,38,56,140,146,161,191),(11,21,44,50,134,152,161,191),(11,22,44,49,133,152,162,191))
SPECTRA=({0:1,148:6,152:16,182:12,216:1},{0:1,148:1,150:8,152:12,182:10},{0:1,150:6,151:8,152:7,165:4,182:6,199:4}) # values are 4 lambda
SOURCE_SHA='7834725d9e34ee846a9ccc615221ea81e0201613938afa185d2eda0c9a6c232f'
PAIRS=[(i,i) for i in range(8)]+list(combinations(range(8),2))

def need(ok,why):
    if not ok:raise ValueError(why)

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def matvec(a,v):return [dot(r,v) for r in a]
def matrix_product(a,b):return [[dot(r,c) for c in zip(*b)] for r in a]
def transpose(a):return list(map(list,zip(*a)))

def roots():
    out={}
    for i,j in combinations(range(9),2):out[511-(1<<i)-(1<<j)]=tuple(3*(int(k==i)-int(k==j)) for k in range(9))
    for t in combinations(range(9),3):out[sum(1<<i for i in t)]=tuple(2 if k in t else -1 for k in range(9))
    need(len(out)==120 and all(sum(v)==0 and dot(v,v)==18 for v in out.values()),'ROOT_NORMALIZATION')
    return out

def rank_and_kernel(a):
    """Exact rational forward elimination and back substitution (not mod p)."""
    m=[list(map(Q,r)) for r in a]; cols=len(m[0]); piv=[]
    for c in range(cols):
        rr=next((r for r in range(len(piv),len(m)) if m[r][c]),None)
        if rr is None:continue
        k=len(piv);m[k],m[rr]=m[rr],m[k]
        p=m[k][c];m[k]=[x/p for x in m[k]]
        for r in range(k+1,len(m)):
            x=m[r][c]
            if x:m[r]=[y-x*z for y,z in zip(m[r],m[k])]
        piv.append(c)
    basis=[]
    for f in range(cols):
        if f in piv:continue
        v=[Q(0)]*cols;v[f]=Q(1)
        for k in reversed(range(len(piv))):v[piv[k]]=-dot(m[k],v)
        need(not any(matvec(a,v)),'KERNEL_BACK_SUBSTITUTION')
        basis.append(v)
    return len(piv),basis

def positive_ldl(a):
    """No-pivot rational LDL: positive pivots iff this symmetric matrix is PD."""
    m=[list(map(Q,r)) for r in a];piv=[]
    need(m==transpose(m),'LDL_NOT_SYMMETRIC')
    for k in range(len(m)):
        d=m[k][k];need(d>0,'LDL_NOT_POSITIVE');piv.append(d)
        for i in range(k+1,len(m)):
            for j in range(i,len(m)):
                m[i][j]-=m[i][k]*m[j][k]/d;m[j][i]=m[i][j]
    return piv

def physical_basis():
    # Build each physical 9x9 operator without using F coordinates.
    basis=[]
    for i,j in PAIRS:
        a=[[0]*9 for _ in range(9)]
        for p,q in ((i,j),) if i==j else ((i,j),(j,i)):
            for r in (p,8):
                for s in (q,8):a[r][s]+=(1 if r==p else -1)*(1 if s==q else -1)
        basis.append(a)
    return basis

def energy(root,deleted):
    labels=sorted(set(root)-set(deleted));need(len(labels)==104,'PUNCTURE_SIZE')
    w={q:tuple((root[q][i]-root[q][8])//3 for i in range(8)) for q in labels}
    need(all(all((root[q][i]-root[q][8])%3==0 for i in range(8)) for q in labels),'A8_INTEGRAL')
    h=[[0]*36 for _ in range(36)];count=0
    for q,r in combinations(labels,2):
        if dot(root[q],root[r]):continue
        count+=1;u,v=w[q],w[r]
        l=[u[i]*v[j] if i==j else u[i]*v[j]+u[j]*v[i] for i,j in PAIRS]
        nonzero=[(i,x) for i,x in enumerate(l) if x]
        for i,x in nonzero:
            for j,y in nonzero:h[i][j]+=x*y
    need(count==2860,'ORTHOGONAL_PAIR_COUNT')
    return h,count

def shift(h,w,a):return [[x-a*y for x,y in zip(r,s)] for r,s in zip(h,w)]
def symmetric(v):
    a=[[Q(0)]*8 for _ in range(8)]
    for (i,j),x in zip(PAIRS,v):a[i][j]=a[j][i]=x
    return a

def run(source):
    need(sha256(Path(source).read_bytes()).hexdigest()==SOURCE_SHA,'SOURCE_SHA256')
    root=roots();physical=physical_basis();flat=[sum(a,[]) for a in physical]
    w=[[dot(a,b) for b in flat] for a in flat]
    wp=positive_ldl(w);need(len(wp)==36,'FROBENIUS_DIMENSION')
    trace=[sum(a[i][i] for i in range(9)) for a in physical]
    need(trace==[2]*36,'TRACE_COORDINATES')
    identity=[Q(8,9) if i==j else Q(-1,9) for i,j in PAIRS]
    need(dot(identity,matvec(w,identity))==8,'IDENTITY_NORM')
    rows=[];matrices=[]
    for rep,spectrum,orbit in zip(REPS,SPECTRA,(28,336,896)):
        h,count=energy(root,F+rep);matrices.append(h)
        need(not any(matvec(h,identity)),'SCALAR_KERNEL')
        found={};bases={}
        for value,multiplicity in spectrum.items():
            rank,basis=rank_and_kernel(shift(h,w,value));need(36-rank==multiplicity,'RATIONAL_MULTIPLICITY')
            need(all(not dot(trace,v) for v in basis) if value else True,'TRACE_FREE_EIGENSPACE')
            found[str(Q(value,4))]=36-rank;bases[value]=basis
        need(sum(found.values())==(32 if orbit==336 else 36),'RATIONAL_COVERAGE')
        c=min(v for v in spectrum if v)
        # A concrete sharp perturbation: in A8 coordinates I+tA, then pull back
        # via B. The physical matrix on V has identity P=I_9-J_9/9.
        v=bases[c][0];a=[[sum(v[k]*physical[k][i][j] for k in range(36)) for j in range(9)] for i in range(9)]
        bound=max(sum(abs(x) for x in r) for r in a);t=Q(1,2)/bound
        s=symmetric([x+t*y for x,y in zip(identity,v)])
        pd=positive_ldl(s) # B injective; BSB^t restricted to V is PD iff S is PD.
        need(dot(v,matvec(h,v))==c*dot(v,matvec(w,v)),'SHARP_ATTAINER')
        rows.append({'orbit':orbit,'orthogonal_pairs':count,'rational_multiplicities':found,'sharp_constant':str(Q(c,4)),'equality_dimension':len(bases[c]),'positive_definite_attainer_t':str(t),'pd_pivots_positive':len(pd)})
    # Independent construction of the stated quadratic subspace in 9D,
    # then top-left 8x8 extraction into the nonorthogonal S chart.
    bs=[]
    b1=[[0]*8 for _ in range(8)];b2=[[0]*8 for _ in range(8)]
    for i in (0,1):b1[i][i]=1
    for i in (4,5):b1[i][i]=-1
    for i in (2,3):b2[i][i]=1
    for i in (6,7):b2[i][i]=-1
    b3=[[0]*8 for _ in range(8)];b4=[[0]*8 for _ in range(8)]
    for a,i,j,x in ((b3,0,1,1),(b3,4,5,-1),(b4,2,3,1),(b4,6,7,1)):a[i][j]=a[j][i]=x
    rf=[[root[q][i] for q in F] for i in range(8)]
    for b in (b1,b2,b3,b4):
        s=matrix_product(matrix_product(rf,b),transpose(rf))
        bs.append([Q(s[i][j],18) for i,j in PAIRS])
    v=transpose(bs);c=[[796,0,0,-68],[0,796,68,0],[0,68,660,0],[-68,0,0,660]]
    hv=matrix_product(matrices[1],v);wvc=matrix_product(matrix_product(w,v),c)
    need([[4*x for x in r] for r in hv]==wvc,'QUADRATIC_ACTION')
    need(rank_and_kernel(transpose(v))[0]==4,'QUADRATIC_DIMENSION')
    cc=matrix_product(c,c)
    need(all(cc[i][j]-1456*c[i][j]+520736*(i==j)==0 for i in range(4) for j in range(4)),'QUADRATIC_POLYNOMIAL')
    need(sum(c[i][i] for i in range(4))==2912,'QUADRATIC_MULTIPLICITIES')
    need(all((4*x)**2-1456*(4*x)+520736!=0 for x in SPECTRA[1]),'QUADRATIC_RATIONAL_OVERLAP')
    need(32**2>2*17**2,'QUADRATIC_LOWER_BOUND')
    # Independent negative controls: wrong normalization and changed action
    # must fail exact equations, not merely alter display fields.
    need(any(any(x for x in r) for r in shift(matrices[0],w,296)),'NEGATIVE_NORM_TRIVIAL')
    wrong_rank,_=rank_and_kernel(shift(matrices[0],w,296))
    need(wrong_rank==36,'NEGATIVE_DOUBLE_ENERGY')
    bad=[r[:] for r in c];bad[0][3]=68
    need([[4*x for x in r] for r in hv]!=matrix_product(matrix_product(w,v),bad),'NEGATIVE_QUADRATIC_SIGN')
    need(rank_and_kernel(transpose([r[:3] for r in v]))[0]==3,'NEGATIVE_MISSING_QUADRATIC_COLUMN')
    return {'status':'PASS_INDEPENDENT_A8_ALL_SPECTRA','source_sha256':SOURCE_SHA,'normalization':'energy=s^t H s/4; Frobenius=s^t W s; independent A8 chart','frobenius_positive_pivots':len(wp),'classes':rows,'quadratic_mu_polynomial':[1,-1456,520736],'quadratic_dimension':4,'quadratic_lambda':'(182 +/- 17 sqrt(2))/4, each multiplicity 2','negative_controls':3,'no_new_kappa':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',default=Path(__file__).resolve().parents[2]/'research/p104-helper470-twin-rung-removal/WORD.json.gz');a=p.parse_args()
    print(json.dumps(run(a.source),sort_keys=True,indent=2))
