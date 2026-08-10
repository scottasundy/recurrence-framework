# Cosmic Coordinate

## Purpose

A compact coordinate describing where the universe lies on a reference cosmological history.

## Official coordinate

`M3 / Phi_C=0.7376`

Reference inputs:
- H0 = 68.11 km s^-1 Mpc^-1
- Omega_m0 = 0.3042
- Omega_Lambda0 = 0.6958
- matter-radiation equality reference redshift = 3387

## Coordinate grammar

`M / Phi_C`

Nothing else is part of the coordinate.

## Macrostate registry

The M states are operational epochs on the reference history:

- M0: radiation-dominated era.
- M1: matter-dominated era before the reference acceleration-onset boundary.
- M2: transition interval after acceleration begins but before dark energy overtakes matter.
- M3: dark-energy-dominated accelerating era.
- M4: deep dark-energy era, operationally beginning when the dark-energy fraction reaches 0.90.

M4 is a CPS-defined threshold rather than a standard named cosmological epoch.

## Composition phase

Phi_C = (2/pi) atan(rho_DE/rho_m)

with

0 <= Phi_C <= 1.

Interpretation:
- Phi_C -> 0: matter strongly dominates dark energy.
- Phi_C = 0.5: equal matter and dark-energy densities.
- Phi_C -> 1: dark energy strongly dominates matter.

Phi_C is not a percentage of the universe's total lifetime.

## Reference cosmic clock

For the flat matter+Lambda reference cosmology,

rho_Lambda/rho_m = (Omega_Lambda0/Omega_m0) a^3

so

a(Phi_C) =
[(Omega_m0/Omega_Lambda0) tan(pi Phi_C/2)]^(1/3)

and the late-time analytic age relation is

t(Phi_C) =
2 / (3 H0 sqrt(Omega_Lambda0))
asinh[sqrt(tan(pi Phi_C/2))].

This converts Phi_C into a reference scale factor, redshift, and cosmic age.

Current reference age:
13.787 Gyr.

Important: the analytic age relation neglects radiation, so the very early M0/M1 boundary is anchored separately to the matter-radiation equality reference rather than inferred from the late-time formula.

## Reference timeline

- M0 -> M1: near z = 3387, about 51,500 years after the Big Bang.
- M1 -> M2: z = 0.6600, reference age 7.555 Gyr.
- M2 -> M3: z = 0.3176, reference age 10.113 Gyr, Phi_C = 0.5000.
- Current: `M3 / Phi_C=0.7376`, reference age 13.787 Gyr.
- M3 -> M4: under an unchanged flat-Lambda reference, in 7.077 Gyr, at Phi_C=0.9296.

Time elapsed since M3 entry:
3.674 Gyr.

Fraction of the reference M3-to-M4 interval elapsed:
34.17%.

## Phase milestones from now

- Phi_C = 0.7400: 49.1 Myr
- Phi_C = 0.7500: 259.4 Myr
- Phi_C = 0.8000: 1.451 Gyr
- Phi_C = 0.8500: 2.985 Gyr
- Phi_C = 0.9000: 5.167 Gyr
- Phi_C = 0.9900: 18.039 Gyr

## Scientific status

This is a model-conditional coordinate system tied to an explicit reference cosmology. It is a descriptive cosmic clock, not a claim that the reference model is the exact fundamental theory.
