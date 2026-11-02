import pathlib,sys,random,json
from fractions import Fraction as Q
sys.path.insert(0,str(pathlib.Path('scripts').resolve()))
import certify_rational_rank as tool
rng=random.Random(6272);checked=0;rejected=0;old=tool.MAX_PRODUCT_SCALE_BITS
for cap in [old,0]:
 tool.MAX_PRODUCT_SCALE_BITS=cap
 for _ in range(400):
  m,k,n=[rng.randrange(5) for i in range(3)]
  a=[[Q(rng.randrange(-7,8),rng.randrange(1,14)) for j in range(k)] for i in range(m)]
  b=[[Q(rng.randrange(-7,8),rng.randrange(1,14)) for j in range(n)] for i in range(k)]
  c=[[sum((a[i][t]*b[t][j] for t in range(k)),Q(0)) for j in range(n)] for i in range(m)]
  if tool._product_equal(a,b,c,m,k,n) is not True:raise ValueError('exact product rejected')
  checked+=1
  if m and n:
   c[rng.randrange(m)][rng.randrange(n)]+=Q(1,97)
   if tool._product_equal(a,b,c,m,k,n) is not False:raise ValueError('wrong product accepted')
   rejected+=1
tool.MAX_PRODUCT_SCALE_BITS=old
print(json.dumps(dict(status='PASS',oracle='Fraction sum of exact products',valid_products=checked,invalid_products_rejected=rejected,scaling_caps=[old,0],scope='Finite independent checks of integer-scaled and forced fallback paths, including empty factors. Not a universal proof.')))
