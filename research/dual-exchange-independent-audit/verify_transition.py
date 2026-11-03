"""Source-bound transition verification; no predecessor verifier is executed.

@CubeJerry with OpenAI Codex assistance; Apache-2.0.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import runpy

HERE=Path(__file__).resolve().parent
# Reuse only our independent source authentication, scalar interpreter and
# tariff extraction. This module does not execute the predecessor verifier.
V=runpy.run_path(str(HERE/'verify.py'))
T=runpy.run_path(str(HERE/'transition.py'))
need=V['need'];literal=V['literal'];price=V['price']
compile_transition=T['compile_transition']


def prefix(ops,n):
    columns=[[Q(i==j) for i in range(n+1)] for j in range(n+1)]
    largest=Q(1)
    for step in ops:
        columns=[literal([step],v) for v in columns]
        largest=max(largest,max(sum(abs(v[i]) for v in columns) for i in range(n+1)))
    return largest,columns


def direct(a,b,d,values):
    x,z=values[:-1],values[-1]
    residual=z-sum(q*v for q,v in zip(a,x))
    return [v+(q-r)*residual for v,q,r in zip(x,b,d)]+[z]


def macro(first,last,junction,state,functions):
    x=literal(first,state)
    x[-1]=functions[0](x[-1])
    x=literal(junction,x)
    x[-1]=functions[1](x[-1])
    return literal(last,x)


def main():
    raw,tariff_raw=V['bindings']();compiler=V['load_compiler'](raw)
    tariff=V['source_tariff_expression'](tariff_raw)
    # This is an additional source obligation beyond the numeric ADD tariff.
    need(b"need(abs(q)+1 < 2**16, 'Fixed scalar growth bound')" in tariff_raw,'PINNED_GROWTH_ADMISSION')
    fixtures=[((1,),(1,),(1,)),((3,5),(2,-1),(7,-4)),((1,0),(1,2),(1,-3)),
              ((Q(1,2),Q(1,4)),(2,0),(1,2)),((1,0,0),(1,2,-1),(1,0,3)),
              ((1,)+(0,)*15,(1,)+(1,)*15,(1,)+(-1,)*15)]
    checks=0
    for a,b,d in fixtures:
        compiler['pair'](a,b);compiler['pair'](a,d)
        ops=compile_transition(a,b,d)
        e=[Q(x)-Q(y) for x,y in zip(b,d)]
        expected=0 if not any(e) else 2*sum(V['price_coefficient'](x) for x in a if x)+sum(V['price_coefficient'](x) for x in e if x)
        need(price(ops)==expected==compiler['allowance'](ops),'TRANSITION_TARIFF')
        for op,r,s,q in ops:
            need(op=='ADD' and r!=s and abs(q)+1<2**16,'EMITTED_SOURCE_ADMISSION')
            need(eval(tariff,{'__builtins__':{}},{'n':abs(q.numerator),'d':q.denominator})==V['price_coefficient'](q),'ACTUAL_SOURCE_TARIFF')
        bound=(1+sum(map(abs,a)))**2*(1+sum(map(abs,e)))
        peak,columns=prefix(ops,len(a));need(peak<=bound,'SCALAR_PREFIX_BOUND')
        for mode1,mode2 in product(('a','b','cheapest'),repeat=2):
            left=compiler['compile_exchange'](a,b,mode1)+compiler['compile_exchange'](a,d,mode2)
            need(all(abs(q)+1<2**16 for _,_,_,q in left),'BASELINE_SOURCE_ADMISSION')
            _,old_columns=prefix(left,len(a))
            need(columns==old_columns,'SOURCE_JUNCTION_COLUMNS')
            for j,column in enumerate(columns):
                state=[Q(i==j) for i in range(len(a)+1)]
                need(column==direct(a,b,d,state),'DIRECT_JUNCTION_COLUMNS')
            checks+=1
    a,b,d=fixtures[1];first=compiler['compile_exchange'](a,b);last=compiler['compile_exchange'](a,d)
    junction=compile_transition(a,b,d);old=first+last
    function_pairs=((lambda x:x*x+1,lambda x:abs(x)-2),(lambda x:Q(3),lambda x:x*x-x),(lambda x:-x,lambda x:x+Q(1,2)))
    cases=0
    for state in product(range(-2,3),repeat=3):
        need(literal(junction,state)==literal(old,state)==direct(a,b,d,state),'DIRTY_JUNCTION')
        for functions in function_pairs:
            before=macro(first,last,old,state,functions)
            after=macro(first,last,junction,state,functions)
            # Independently apply the two closed nonlinear consumers on data.
            x=list(map(Q,state));z=x[-1]
            for column,fn in zip((b,d),functions):
                ax=sum(q*v for q,v in zip(a,x[:-1]));delta=fn(ax)-ax
                x=[v+q*delta for v,q in zip(x[:-1],column)]+[z]
            need(before==after==x,'COMPLETE_NONLINEAR_MACRO')
            cases+=1
    need((price(first),price(last),price(junction))==(64,82,78),'NAMED_ALLOWANCES')
    full_old=first+old+last;full_new=first+junction+last
    need((price(full_old),price(full_new),len(full_old),len(full_new))==(292,224,28,20),'COMPLETE_LOCAL_BUDGET')
    # Compare also against the immediate source peephole: the final sign of
    # S_b and the initial sign of S_d are adjacent inverse operations.
    sign=('SCALE',len(a),len(a),Q(-1))
    need(first[-1]==last[0]==sign,'ADJACENT_SOURCE_SIGNS')
    reduced_junction=first[:-1]+last[1:]
    need(prefix(reduced_junction,2)[1]==prefix(old,2)[1]==prefix(junction,2)[1],
         'SIGN_CANCELLED_ALL_COLUMNS')
    reduced_full=first+reduced_junction+last
    need((price(reduced_junction),price(reduced_full),len(reduced_full))==(142,288,26),
         'SIGN_CANCELLED_COMPLETE_BUDGET')
    for large_column in ((1,2**64-1),(1,-(2**64-1))):
        compiler['pair']((1,0),large_column)
    controls=0
    for call,reason in [
        (lambda:compile_transition((3,5),(2,-1),(7,-3)),'SECOND_DUALITY'),
        (lambda:compile_transition((1,0),(1,65534),(1,-65534)),'EMITTED_SOURCE_GROWTH'),
        (lambda:compile_transition((1,0),(1,2**64-1),(1,-(2**64-1))),'NUMERATOR_BOUND'),
        (lambda:compile_transition((1,Q(1,3)),(1,0),(1,0)),'DYADIC_DENOMINATOR'),
        (lambda:compile_transition((True,0),(1,0),(1,0)),'EXACT_COEFFICIENTS')]:
        controls+=V['expect_reject'](call,reason)
    # Concrete semantic controls: missing restoration and reversed E sign.
    need(literal(junction[:-2],[1,0,7])!=direct(a,b,d,[1,0,7]),'MISSING_RESTORATION_CONTROL')
    reverse=compile_transition(a,d,b)
    need(literal(reverse,[1,0,7])!=direct(a,b,d,[1,0,7]),'REVERSED_TRANSITION_CONTROL')
    # An observation at the eliminated restored-spare boundary is not preserved.
    state=[Q(1),Q(0),Q(7)];inner=literal(first,state);inner[-1]+=1
    boundary=literal(first,inner)
    need(boundary[-1]!=inner[-1],'ELIMINATED_BOUNDARY_OBSERVER_CONTROL')
    need(compile_transition(a,b,b)==[],'EMPTY_DIFFERENCE')
    # A dyadic borrow can make the difference expensive despite small magnitude.
    ua,ub,ud=(1,0),(1,1),(1,Q(1,2**32))
    unfavorable_old=compiler['compile_exchange'](ua,ub)+compiler['compile_exchange'](ua,ud)
    unfavorable_new=compile_transition(ua,ub,ud)
    need((price(unfavorable_old),price(unfavorable_new))==(132,212),'UNFAVORABLE_TARIFF_DISCRIMINATOR')
    need(prefix(unfavorable_old,2)[1]==prefix(unfavorable_new,2)[1],'UNFAVORABLE_VALID_ENDPOINT')
    return {'status':'PASS_SOURCE_BOUND_CHANGING_DUAL_TRANSITION','base_commit':'2485805a6d47f36ea83ddde6327d453ac82d44dc','source_head':V['SOURCE_HEAD'],
            'fixture_count':len(fixtures),'source_factorization_pairs':checks,'dirty_junction_states':125,'complete_nonlinear_macro_cases':cases,
            'named_case':{'a':list(a),'b':list(b),'d':list(d),'junction_allowance_before':price(old),'junction_allowance_after':price(junction),
                          'complete_allowance_before':price(full_old),'complete_allowance_after':price(full_new),'complete_scalar_gates_before':len(full_old),'complete_scalar_gates_after':len(full_new),
                          'sign_cancelled_complete_allowance_before':price(reduced_full),'sign_cancelled_complete_instructions_before':len(reduced_full),
                          'saving_against_sign_cancelled_baseline':price(reduced_full)-price(full_new),'saving_against_literal_baseline':price(full_old)-price(full_new),
                          'both_inner_calls_retained':True,'junction_prefix_before':str(prefix(old,2)[0]),'junction_prefix_after':str(prefix(junction,2)[0]),'junction_prefix_envelope':729},
            'unfavorable_tariff_discriminator':{'two_exchanges':132,'three_shears':212},
            'negative_controls':controls+3,'no_new_kappa':True}

if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
