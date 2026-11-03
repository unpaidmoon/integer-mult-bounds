"""Independent exhaustive nonlinear composition check over F3.

Jerry Chen (@CubeJerry), OpenAI Codex lead-agent assistance. Apache-2.0.
This uses the authenticated source emitter, with a separate field interpreter
and direct endpoint formula; it imports no primary verifier or polynomial engine.
"""
from pathlib import Path
import itertools, runpy, hashlib, json
from fractions import Fraction
source=Path(__file__).resolve().parent/'source/compiler.py'
raw=source.read_bytes()
if hashlib.sha256(raw).hexdigest()!='9d7b71ed4da90360f8a0f15b7a89599340efbb4eb1ff40054e11e621f85df5bf':
    raise ValueError('source compiler hash mismatch')
mod=runpy.run_path(str(source))
a,b=(3,5),(2,-1)
def f3(q):
    q=Fraction(q)
    return q.numerator*pow(q.denominator,-1,3)%3
def execute(word,state):
    state=list(state)
    for op,d,s,q in word:
        if op=='ADD': state[d]=(state[d]+q*state[s])%3
        elif op=='SCALE': state[d]=q*state[d]%3
        else: raise ValueError(op)
    return tuple(state)
def consumer(word,f,state):
    t=execute(word,state)
    t=(*t[:2],f[t[2]])
    return execute(word,t)
cases=0
functions=list(itertools.product(range(3),repeat=3))
states=list(itertools.product(range(3),repeat=3))
for repeat in ['a','b','cheapest']:
    word=[(op,d,s,f3(q)) for op,d,s,q in mod['compile_exchange'](a,b,repeat)]
    for f,g in itertools.product(functions,repeat=2):
        composed=tuple(g[f[t]] for t in range(3))
        for x in states:
            separate=consumer(word,g,consumer(word,f,x))
            fused=consumer(word,composed,x)
            t=(a[0]*x[0]+a[1]*x[1])%3
            oracle=((x[0]+b[0]*(composed[t]-t))%3,(x[1]+b[1]*(composed[t]-t))%3,x[2])
            if separate!=fused or fused!=oracle:
                raise ValueError((repeat,f,g,x,separate,fused,oracle))
            cases+=1
# Distinct pairs may each satisfy duality yet leak arbitrary spare values.
incoming=[(op,d,s,f3(q)) for op,d,s,q in mod['compile_exchange']((1,1),(1,0))]
outgoing=[(op,d,s,f3(q)) for op,d,s,q in mod['compile_exchange']((1,1),(0,1))]
leak=[]
for z in range(3):
    after=execute(incoming,(0,0,z))
    result=execute(outgoing,after)
    leak.append(result)
if leak!=[(0,0,0),(1,2,1),(2,1,2)]: raise ValueError(leak)
print(json.dumps({'status':'PASS_INDEPENDENT_NONLINEAR_EXCHANGE_COMPOSITION','cases':cases,'pair':{'a':a,'b':b},'domain':'every F3 scalar map pair, every three-role F3 input, all three emitter modes','source_sha256':hashlib.sha256(raw).hexdigest(),'mismatched_column_leak':leak},indent=2))
