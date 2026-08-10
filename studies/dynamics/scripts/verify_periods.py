#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT/'src',ROOT/'scripts'):
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from recurrence_dynamics.periods import diagonal_species_histograms,histogram_rotation_period
from recurrence_dynamics.hpp import balanced_random_state,density,step
from generate_periods import four_particle_zero_momentum_states,decompose,enumerate_reference_fiber,advance

s3=four_particle_zero_momentum_states(3); p3,_,c3=decompose(s3,3)
assert len(s3)==9153 and len(c3)==2061
assert Counter(p3)=={3:4023,6:2754,9:2268,12:108}
s4=four_particle_zero_momentum_states(4); p4,_,c4=decompose(s4,4)
assert len(s4)==94336 and len(c4)==19448
assert Counter(p4)=={2:112,4:66464,6:240,8:17024,12:4800,20:320,28:5376}
classes={}
for s,p in zip(s4,p4):
    x=s; w=[]
    for _ in range(4): w.append(density(x)); x=step(x,4,4)
    key=tuple(w); old=classes.setdefault(key,p); assert old==p
ref=balanced_random_state(5,75202,opposite_pairs=7)
g=histogram_rotation_period(diagonal_species_histograms(ref,5)); assert g==5
fiber=enumerate_reference_fiber(ref); assert len(fiber)==2209
macro=lambda s:advance(s,5,5)
_,cids,cycles=decompose(fiber,5,macro)
assert sorted((len(c) for c in cycles),reverse=True)==[1941,46,45,44,28,18,14,14,10,9,8,8,7,5,5,4,3]
assert len(cycles[cids[{s:i for i,s in enumerate(fiber)}[ref]]])==1941
print('Period-navigation exact verification: PASS')
print('3x3 states/cycles: 9153 / 2061')
print('4x4 states/cycles: 94336 / 19448')
print('5x5 seed-B fiber/macroperiod: 2209 / 1941')
