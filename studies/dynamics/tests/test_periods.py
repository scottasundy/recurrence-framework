from pathlib import Path
import csv
from recurrence_dynamics.periods import (
    analytic_period_divisor, brent_period, checkerboard_modes,
    diagonal_species_histograms, line_momenta, locate_phase,
    rotated_histograms, transport_clock,
)
from recurrence_dynamics.hpp import balanced_random_state, particle_number, step

ROOT=Path(__file__).resolve().parents[1]

def test_transport_and_diagonal_clocks():
    for L in range(3,7):
        for seed in range(4):
            s=balanced_random_state(L,91000+100*L+seed,opposite_pairs=2)
            t=step(s,L,L)
            assert (transport_clock(t,L)-transport_clock(s,L))%L==particle_number(s)%L
            assert diagonal_species_histograms(t,L)==rotated_histograms(diagonal_species_histograms(s,L),1)

def test_line_momenta():
    for L in range(3,7):
        s=balanced_random_state(L,92000+L,opposite_pairs=3)
        assert line_momenta(step(s,L,L),L)==line_momenta(s,L)

def test_checkerboard_modes_flip():
    for L in (4,6):
        s=balanced_random_state(L,93000+L,opposite_pairs=3)
        assert checkerboard_modes(step(s,L,L),L)==tuple(-x for x in checkerboard_modes(s,L))

def test_reference_period_and_phase():
    ref=balanced_random_state(5,75202,opposite_pairs=7)
    assert brent_period(ref,5,cap=40000).period==9705
    assert analytic_period_divisor(ref,5)==5
    x=ref; targets={}
    for t in range(1,9003):
        x=step(x,5,5)
        if t in (703,9002): targets[t]=x
    assert locate_phase(ref,targets[703],5,9705).phase==703
    assert locate_phase(ref,targets[9002],5,9705).phase==9002

def test_committed_summaries():
    d=ROOT/'data/periods'
    with (d/'4x4-periods.csv').open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    assert sum(int(r['state_count']) for r in rows)==94336
    assert sum(int(r['cycle_count']) for r in rows)==19448
    with (d/'5x5-summary.csv').open(newline='',encoding='utf-8') as f:
        r=next(csv.DictReader(f))
    assert int(r['microscopic_period_T'])==9705
    assert int(r['fixed_histogram_line_momentum_fiber_states'])==2209
    assert int(r['interaction_macroperiod_T_over_g'])==1941
    assert int(r['minimum_orbit_hamming_distance'])==4
    assert int(r['greedy_single_snapshot_velocity_sensors'])==49
    assert int(r['greedy_three_frame_density_sensors'])==11
