#!/usr/bin/env python3
"""Generate period-navigation certificates and summaries."""
from __future__ import annotations

import argparse, csv, math, sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from random import Random
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from recurrence_dynamics.periods import (
    analytic_period_divisor, collision_orientation_frame,
    diagonal_species_histograms, histogram_rotation_period,
    interaction_fiber_signature, line_momenta,
)
from recurrence_dynamics.hpp import (
    EAST, NORTH, SOUTH, WEST, VECTOR,
    balanced_random_state, collision_site_count, density, momentum,
    particle_number, state_hex, step, velocity_bit_hamming,
)


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def four_particle_zero_momentum_states(L):
    out=[]
    for occupied in combinations(range(4*L*L), 4):
        px=py=0; cells=[0]*(L*L)
        for ch in occupied:
            cell, bit = divmod(ch,4); d=1<<bit
            dx,dy=VECTOR[d]; px+=dx; py+=dy; cells[cell]|=d
        if px==0 and py==0:
            out.append(tuple(cells))
    return out


def decompose(states,L,update=None):
    update = update or (lambda s: step(s,L,L))
    idx={s:i for i,s in enumerate(states)}
    succ=[idx[update(s)] for s in states]
    seen=[False]*len(states); periods=[0]*len(states); cids=[-1]*len(states); cycles=[]
    for start in range(len(states)):
        if seen[start]: continue
        c=[]; j=start
        while not seen[j]:
            seen[j]=True; c.append(j); j=succ[j]
        assert j==start
        cid=len(cycles)
        for q in c: periods[q]=len(c); cids[q]=cid
        cycles.append(c)
    return periods,cids,cycles


def word(state,L,k,obs):
    out=[]
    for _ in range(k):
        out.append(obs(state)); state=step(state,L,L)
    return tuple(out)


def period_summary(periods,cycles):
    sc=Counter(periods); cc=Counter(len(c) for c in cycles)
    return [{'least_period':p,'state_count':sc[p],'cycle_count':cc[p]} for p in sorted(sc)]


def horizon_summary(states,periods,L,obs,maxk):
    rows=[]
    for k in range(1,maxk+1):
        groups=defaultdict(lambda:[set(),0])
        for s,p in zip(states,periods):
            e=groups[word(s,L,k,obs)]; e[0].add(p); e[1]+=1
        amb=[v for v in groups.values() if len(v[0])>1]
        rows.append({'horizon':k,'observation_classes':len(groups),
                     'ambiguous_period_classes':len(amb),
                     'ambiguous_states':sum(v[1] for v in amb),
                     'period_determined_for_all_states':not amb})
    return rows


def collision_words_3(states,periods):
    mp=defaultdict(set)
    for s,p in zip(states,periods):
        x=s; w=[]
        for _ in range(6):
            w.append(collision_site_count(x)); x=step(x,3,3)
        mp[tuple(w)].add(p)
    assert all(len(v)==1 for v in mp.values())
    return [{**{f'c{i}':w[i] for i in range(6)},'least_period':next(iter(mp[w]))}
            for w in sorted(mp)]


def fiber_summary_4(states,periods):
    groups=defaultdict(list); gd=Counter(); violations=0
    for i,(s,p) in enumerate(zip(states,periods)):
        sig=interaction_fiber_signature(s,4); groups[sig].append(i)
        g=histogram_rotation_period(diagonal_species_histograms(s,4)); gd[g]+=1
        violations += int(p%g!=0)
    exact_fibers=exact_states=0
    for sig,inds in groups.items():
        g=histogram_rotation_period(sig[0]); ps={periods[i] for i in inds}
        if len(ps)==1:
            p=next(iter(ps))
            if p%g==0 and len(inds)==p//g:
                exact_fibers+=1; exact_states+=len(inds)
    return [{'total_states':len(states),'interaction_fibers':len(groups),
             'single_macrocycle_fibers':exact_fibers,
             'states_in_single_macrocycle_fibers':exact_states,
             'fraction_states_directly_resolved':f'{exact_states/len(states):.12f}',
             'g_2_states':gd[2],'g_4_states':gd[4],
             'period_divisibility_violations':violations}]


def row_options(L,diff):
    return [(e,w) for e in range(1<<L) for w in range(1<<L)
            if e.bit_count()-w.bit_count()==diff]

def col_options(L,diff):
    return [(s,n) for s in range(1<<L) for n in range(1<<L)
            if s.bit_count()-n.bit_count()==diff]


def enumerate_reference_fiber(ref,L=5):
    hs=diagonal_species_histograms(ref,L); rowpx,colpy=line_momenta(ref,L)
    target=tuple(v for h in hs for v in h)
    hopts=[]
    for y,diff in enumerate(rowpx):
        options=[]
        for e,w in row_options(L,diff):
            c=[[0]*L for _ in range(4)]
            for x in range(L):
                if (e>>x)&1:
                    c[0][(x-y)%L]+=1; c[1][(x+y)%L]+=1
                if (w>>x)&1:
                    c[2][(-x-y)%L]+=1; c[3][(-x+y)%L]+=1
            flat=tuple(v for h in c for v in h)
            if all(flat[i]<=target[i] for i in range(4*L)): options.append((e,w,flat))
        hopts.append(options)
    horiz=[]
    def rec_h(y,acc,es,ws):
        if y==L: horiz.append((tuple(acc),tuple(es),tuple(ws))); return
        for e,w,c in hopts[y]:
            new=[acc[i]+c[i] for i in range(4*L)]
            if all(new[i]<=target[i] for i in range(4*L)):
                rec_h(y+1,new,es+[e],ws+[w])
    rec_h(0,[0]*(4*L),[],[])

    vopts=[]
    for x,diff in enumerate(colpy):
        options=[]
        for s,n in col_options(L,diff):
            c=[[0]*L for _ in range(4)]
            for y in range(L):
                if (n>>y)&1:
                    c[0][(x-y)%L]+=1; c[2][(-x-y)%L]+=1
                if (s>>y)&1:
                    c[1][(x+y)%L]+=1; c[3][(-x+y)%L]+=1
            flat=tuple(v for h in c for v in h)
            if all(flat[i]<=target[i] for i in range(4*L)): options.append((s,n,flat))
        vopts.append(options)
    vert=[]
    def rec_v(x,acc,ss,ns):
        if x==L: vert.append((tuple(acc),tuple(ss),tuple(ns))); return
        for s,n,c in vopts[x]:
            new=[acc[i]+c[i] for i in range(4*L)]
            if all(new[i]<=target[i] for i in range(4*L)):
                rec_v(x+1,new,ss+[s],ns+[n])
    rec_v(0,[0]*(4*L),[],[])
    vmap=defaultdict(list)
    for c,ss,ns in vert: vmap[c].append((ss,ns))
    out=[]
    for hc,es,ws in horiz:
        rem=tuple(target[i]-hc[i] for i in range(4*L))
        for ss,ns in vmap.get(rem,[]):
            cells=[0]*(L*L)
            for y in range(L):
                for x in range(L):
                    if (es[y]>>x)&1: cells[y*L+x]|=EAST
                    if (ws[y]>>x)&1: cells[y*L+x]|=WEST
            for x in range(L):
                for y in range(L):
                    if (ss[x]>>y)&1: cells[y*L+x]|=SOUTH
                    if (ns[x]>>y)&1: cells[y*L+x]|=NORTH
            out.append(tuple(cells))
    assert len(out)==len(set(out))
    return out


def advance(s,L,n):
    for _ in range(n): s=step(s,L,L)
    return s


def target_collision_horizon(fiber,cycles,cids,target):
    pby={}; cby={}
    for cid,c in enumerate(cycles):
        for i in c: pby[fiber[i]]=len(c); cby[fiber[i]]=cid
    tc=cby[target]; rows=[]
    for k in range(1,10):
        groups=defaultdict(list)
        for s in fiber: groups[word(s,5,k,collision_orientation_frame)].append(s)
        amb=sum(len(v) for v in groups.values() if len({pby[s] for s in v})>1)
        tg=groups[word(target,5,k,collision_orientation_frame)]
        rows.append({'horizon':k,'observation_classes':len(groups),'ambiguous_period_states':amb,
                     'period_determined_for_all_states':amb==0,
                     'all_states_uniquely_identified':len(groups)==len(fiber),
                     'target_candidate_states':len(tg),
                     'target_candidate_macroperiods':';'.join(map(str,sorted({pby[s] for s in tg}))),
                     'target_same_macrocycle_only':all(cby[s]==tc for s in tg)})
    return rows


def bits(s):
    return tuple((m>>b)&1 for m in s for b in range(4))


def greedy_sensors(rows,ncols):
    selected=[]; signatures=[()]*len(rows); remaining=set(range(ncols))
    while len(set(signatures))<len(rows):
        best=max(sorted(remaining), key=lambda c: len({signatures[i]+(rows[i][c],) for i in range(len(rows))}))
        selected.append(best); remaining.remove(best)
        signatures=[signatures[i]+(rows[i][best],) for i in range(len(rows))]
    return selected


def min_hamming_certificate(orbit):
    codes=[]
    for s in orbit:
        code=0
        for i,b in enumerate(bits(s)):
            if b: code|=1<<i
        codes.append(code)
    S=set(codes)
    for code in codes:
        ones=[i for i in range(100) if (code>>i)&1]
        zeros=[i for i in range(100) if not ((code>>i)&1)]
        for a in ones:
            core=code^(1<<a)
            for b in zeros:
                assert (core^(1<<b)) not in S
    seen={}
    for j,code in enumerate(codes):
        ones=[i for i in range(100) if (code>>i)&1]
        for a,b in combinations(ones,2):
            core=code^(1<<a)^(1<<b)
            i=seen.get(core)
            if i is not None and (code^codes[i]).bit_count()==4: return 4,i,j
            seen.setdefault(core,j)
    raise AssertionError('no distance-4 witness')


def rank_mod(M,p=1000003):
    A=[[x%p for x in row] for row in M]; m=len(A); n=len(A[0]); r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i][c]),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]; inv=pow(A[r][c],p-2,p)
        A[r]=[(x*inv)%p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                f=A[i][c]; A[i]=[(A[i][j]-f*A[r][j])%p for j in range(n)]
        r+=1
        if r==m: break
    return r


def bit_index(x,y,d,L): return 4*(y*L+x)+{NORTH:0,EAST:1,SOUTH:2,WEST:3}[d]

def known_linear_invariants(L=5):
    rows=[]
    fam=((EAST,NORTH,lambda x,y:x-y),(EAST,SOUTH,lambda x,y:x+y),
         (WEST,NORTH,lambda x,y:-x-y),(WEST,SOUTH,lambda x,y:-x+y))
    for a,b,coord in fam:
        for u in range(L):
            v=[0]*(4*L*L)
            for y in range(L):
                for x in range(L):
                    if coord(x,y)%L==u:
                        v[bit_index(x,y,a,L)]+=1; v[bit_index(x,y,b,L)]+=1
            rows.append(v)
    for y in range(L):
        v=[0]*(4*L*L)
        for x in range(L): v[bit_index(x,y,EAST,L)]+=1; v[bit_index(x,y,WEST,L)]-=1
        rows.append(v)
    for x in range(L):
        v=[0]*(4*L*L)
        for y in range(L): v[bit_index(x,y,SOUTH,L)]+=1; v[bit_index(x,y,NORTH,L)]-=1
        rows.append(v)
    return rows


def linear_certificate():
    rng=Random(12345); diffs=[]
    for _ in range(80):
        s=tuple(rng.randrange(16) for _ in range(25)); t=advance(s,5,5)
        a=bits(s); b=bits(t); diffs.append([b[i]-a[i] for i in range(100)])
    kr=rank_mod(known_linear_invariants()); dr=rank_mod(diffs)
    assert kr==27 and dr==73
    return [{'lattice_size':5,'map':'F^5','binary_state_variables':100,
             'known_invariant_vectors':30,'known_invariant_rank':kr,
             'explicit_difference_witnesses':80,'difference_constraint_rank_mod_1000003':dr,
             'universal_linear_invariant_dimension':100-dr,'witness_seed':12345}]

# Fast bitboard dynamics for the fixed empirical period sample.
def bb_from_state(s,L):
    n=e=ss=w=0
    for i,m in enumerate(s):
        if m&NORTH:n|=1<<i
        if m&EAST:e|=1<<i
        if m&SOUTH:ss|=1<<i
        if m&WEST:w|=1<<i
    return n,e,ss,w

def bb_step(bb,L):
    n,e,s,w=bb; full=(1<<(L*L))-1
    ew=e&w&~n&~s&full; ns=n&s&~e&~w&full
    e=(e&~ew)|ns; w=(w&~ew)|ns; n=(n&~ns)|ew; s=(s&~ns)|ew
    first=sum(1<<(y*L) for y in range(L)); last=first<<(L-1)
    e2=((e&~last)<<1)|((e&last)>>(L-1)); w2=((w&~first)>>1)|((w&first)<<(L-1))
    top=(1<<L)-1; n2=(n>>L)|((n&top)<<(L*(L-1))); s2=((s<<L)&full)|(s>>(L*(L-1)))
    return n2,e2,s2,w2

def brent_bb(x,L,cap=500000):
    power=lam=1; tort=x; hare=bb_step(x,L); ev=1
    while tort!=hare:
        if ev>=cap: raise RuntimeError('period cap exceeded')
        if power==lam: tort=hare; power*=2; lam=0
        hare=bb_step(hare,L); ev+=1; lam+=1
    return lam,ev

def empirical_sample():
    rows=[]
    for seed in range(880000,880500):
        s=balanced_random_state(5,seed,opposite_pairs=7); p,ev=brent_bb(bb_from_state(s,5),5)
        x=s; collisions=[]; hamming=[]; dens=[]
        for t in range(31):
            dens.append(density(x))
            if t<30:
                collisions.append(collision_site_count(x)); y=step(x,5,5)
                hamming.append(velocity_bit_hamming(x,y)); x=y
        row={'seed':seed,'period':p,'log10_period':f'{math.log10(p):.12f}','brent_evaluations':ev,
             'analytic_period_divisor':analytic_period_divisor(s,5),'initial_collision_sites':collisions[0],
             'mean_collision_sites_30':f'{mean(collisions):.12f}','max_collision_sites_30':max(collisions),
             'nonzero_collision_steps_30':sum(c>0 for c in collisions),
             'mean_step_hamming_30':f'{mean(hamming):.12f}','unique_density_frames_31':len(set(dens))}
        for i,v in enumerate(collisions): row[f'collision_t{i}']=v
        for i,v in enumerate(hamming): row[f'hamming_t{i}']=v
        rows.append(row)
    return rows


def generate(data_root):
    out=data_root/'periods'; out.mkdir(parents=True,exist_ok=True)
    s3=four_particle_zero_momentum_states(3); p3,_,c3=decompose(s3,3)
    write_csv(out/'3x3-periods.csv',period_summary(p3,c3))
    write_csv(out/'3x3-collisions.csv',horizon_summary(s3,p3,3,collision_site_count,6))
    write_csv(out/'3x3-words.csv',collision_words_3(s3,p3))

    s4=four_particle_zero_momentum_states(4); p4,_,c4=decompose(s4,4)
    write_csv(out/'4x4-periods.csv',period_summary(p4,c4))
    write_csv(out/'4x4-density.csv',horizon_summary(s4,p4,4,density,4))
    write_csv(out/'4x4-invariants.csv',fiber_summary_4(s4,p4))

    ref=balanced_random_state(5,75202,opposite_pairs=7); g=histogram_rotation_period(diagonal_species_histograms(ref,5)); assert g==5
    orbit=[ref]; x=ref
    while True:
        x=step(x,5,5)
        if x==ref: break
        orbit.append(x)
        assert len(orbit)<20000
    assert len(orbit)==9705
    fiber=enumerate_reference_fiber(ref); assert len(fiber)==2209
    macro=lambda s: advance(s,5,g)
    _,cids,cycles=decompose(fiber,5,macro)
    lens=sorted((len(c) for c in cycles),reverse=True)
    assert lens==[1941,46,45,44,28,18,14,14,10,9,8,8,7,5,5,4,3]
    fi={s:i for i,s in enumerate(fiber)}; target_cid=cids[fi[ref]]; assert len(cycles[target_cid])==1941
    cycle_rows=[]
    for rank,c in enumerate(sorted(cycles,key=len,reverse=True),1):
        states={fiber[i] for i in c}
        cycle_rows.append({'rank':rank,'macroperiod_under_F_power_g':len(c),'full_F_period':g*len(c),
                           'state_count_in_fixed_histogram_fiber':len(c),'contains_reference_seed_75202':ref in states})
    write_csv(out/'5x5-cycles.csv',cycle_rows)
    write_csv(out/'5x5-collisions.csv',target_collision_horizon(fiber,cycles,cids,ref))

    md,a,b=min_hamming_certificate(orbit); bit_s=greedy_sensors([bits(s) for s in orbit],100)
    drows=[]
    for s in orbit:
        frames=[]; x=s
        for _ in range(3): frames.append(density(x)); x=step(x,5,5)
        drows.append(tuple(tuple(frames[t][site] for t in range(3)) for site in range(25)))
    den_s=greedy_sensors(drows,25)
    write_csv(out/'5x5-summary.csv',[{'reference_seed':75202,'lattice_size':5,'particles':particle_number(ref),
        'momentum_x':momentum(ref)[0],'momentum_y':momentum(ref)[1],'reference_state_hex':state_hex(ref,5,5),
        'microscopic_period_T':9705,'geometric_histogram_period_g':g,'interaction_macroperiod_T_over_g':1941,
        'fixed_histogram_line_momentum_fiber_states':2209,'macrocycles_in_fiber':17,
        'minimum_orbit_hamming_distance':md,'minimum_distance_witness_phase_a':a,'minimum_distance_witness_phase_b':b,
        'greedy_single_snapshot_velocity_sensors':len(bit_s),'velocity_sensor_indices':';'.join(map(str,bit_s)),
        'greedy_three_frame_density_sensors':len(den_s),'density_sensor_indices':';'.join(map(str,den_s))}])

    seeded=[]
    for L in range(3,8):
        for label,bseed in zip(('A','B','C'),(101,202,303)):
            seed=bseed+L*1000+70000; s=balanced_random_state(L,seed,opposite_pairs=7); x=s
            for t in range(1,600001):
                x=step(x,L,L)
                if x==s: break
            else: raise RuntimeError('seeded period cap exceeded')
            d=analytic_period_divisor(s,L)
            seeded.append({'size':L,'seed_label':label,'rng_seed':seed,'period':t,
                           'analytic_period_divisor':d,'period_divisible_by_analytic_divisor':t%d==0})
    write_csv(out/'seeded-constraints.csv',seeded)
    write_csv(out/'invariants.csv',linear_certificate())
    emp=empirical_sample(); write_csv(out/'5x5-sample.csv',emp)
    ps=[r['period'] for r in emp]
    write_csv(out/'5x5-sample-summary.csv',[{'states':500,'seed_start':880000,'seed_end':880499,
        'distinct_periods':len(set(ps)),'minimum_period':min(ps),'maximum_period':max(ps)}])


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output-root',type=Path,default=ROOT/'data')
    args=ap.parse_args(); generate(args.output_root); print(args.output_root/'periods')
if __name__=='__main__': main()
