import math

H0 = 68.11
OMEGA_M = 0.3042
OMEGA_L = 0.6958
Z_RADIATION_MATTER_EQUALITY = 3387.0
A_RADIATION_MATTER_EQUALITY = 1/(1 + Z_RADIATION_MATTER_EQUALITY)
HUBBLE_TIME_GYR = (3.0856775814913673e19/H0)/(3600*24*365.25*1e9)

A_ACCELERATION_ONSET = (OMEGA_M/(2*OMEGA_L))**(1/3)
A_DARK_ENERGY_EQUALITY = (OMEGA_M/OMEGA_L)**(1/3)
A_M4 = (9*OMEGA_M/OMEGA_L)**(1/3)

def phi_from_a(a):
    return 2/math.pi * math.atan((OMEGA_L/OMEGA_M)*a**3)

def a_from_phi(phi):
    if not 0 < phi < 1:
        raise ValueError("Phi_C must satisfy 0 < Phi_C < 1 for finite conversion.")
    return ((OMEGA_M/OMEGA_L)*math.tan(math.pi*phi/2))**(1/3)

def age_from_a(a):
    if a <= 0:
        raise ValueError("Scale factor must be positive.")
    return (2/(3*math.sqrt(OMEGA_L))
            * math.asinh(math.sqrt(OMEGA_L/OMEGA_M)*a**1.5)
            * HUBBLE_TIME_GYR)

def macrostate_from_a(a):
    if a < A_RADIATION_MATTER_EQUALITY:
        return "M0"
    if a < A_ACCELERATION_ONSET:
        return "M1"
    if a < A_DARK_ENERGY_EQUALITY:
        return "M2"
    if a < A_M4:
        return "M3"
    return "M4"

def coordinate_from_redshift(z):
    if z <= -1:
        raise ValueError("Redshift must be greater than -1.")
    a = 1/(1+z)
    return macrostate_from_a(a), phi_from_a(a), age_from_a(a)

def coordinate_from_phase(phi):
    a = a_from_phi(phi)
    return macrostate_from_a(a), phi, age_from_a(a), 1/a - 1

if __name__ == "__main__":
    M, phi, t = coordinate_from_redshift(0)
    print(f"{M} / Phi_C={phi:.4f} / t_ref={t:.3f} Gyr")
