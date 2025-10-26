"""
SU(4) to SU(2)×SU(2) Branching Rules Module

This module provides functionality to compute the branching rules for SU(4) irreducible 
representations into SU(2)×SU(2) (spin-isospin) representations.
Module conversion and enhancements added

Functions:
    racah_su4_to_st(f1, f2, f3, f4, verbose=True): Main function returning both DataFrames
    RacahSU4toST(f1, f2, f3, f4): Legacy function for backward compatibility
"""

import pandas as pd
import numpy as np
from fractions import Fraction
import sys

def racah_su4_to_st(f1, f2, f3, f4, verbose=True):
    """
    Compute SU(4) to SU(2)×SU(2) branching rules for given Young tableau.
    
    Parameters:
    -----------
    f1, f2, f3, f4 : int
        Young tableau parameters (must satisfy f1 ≥ f2 ≥ f3 ≥ f4)
    verbose : bool, default=True
        If True, prints formatted output. If False, returns DataFrames silently.
    
    tuple of (pd.DataFrame, pd.DataFrame)
        - SU(4) representation information DataFrame
        - ST branching rules DataFrame
    
    Raises:
    -------
    ValueError
        If Young tableau conditions are not satisfied
    
    Examples:
    ---------
    >>> su4_info, st_branching = racah_su4_to_st(2, 1, 1, 0)
    >>> su4_info, st_branching = racah_su4_to_st(3, 2, 1, 0, verbose=False)
    """
    
    # Validate Young tableau conditions
    if (f4 > f3) or (f3 > f2) or (f2 > f1):
        raise ValueError("Young tableau condition violated: f1 ≥ f2 ≥ f3 ≥ f4 required")
    
    # Alternative notation (alpha, beta, gamma)
    alpha = f1 - f2
    beta = f2 - f3
    gamma = f3 - f4
    
    # Alternative notation (p1, p2, p3)
    p1 = (f1 + f2 - f3 - f4) / 2.0
    p2 = (f1 - f2 + f3 - f4) / 2.0
    p3 = (f1 - f2 - f3 + f4) / 2.0
    
    max_st = max(p1, p2)
    
    def dimsu4(f1, f2, f3, f4):
        """Calculate SU(4) irrep dimension"""
        return (f1-f2+1)*(f1-f3+2)*(f1-f4+3)*(f2-f3+1)*(f2-f4+2)*(f3-f4+1)/12.
    
    def dimST(S, T, mult):
        """Calculate SU(2)×SU(2) irrep dimension"""
        return (2.*S + 1.) * (2.*T + 1.) * mult
    
    def cas2su4(alpha, beta, gamma):
        """Calculate second-order Casimir invariant"""
        casimir = (3*alpha*(alpha+4)
               + 4*beta*(beta+4)
               + 3*gamma*(gamma+4)
               + 4*beta*(alpha+gamma)
               + 2*alpha*gamma)
        return float(casimir)
    # Create SU(4) irrep information
    SU4_irrep = []
    SU4_irrep.append([
        "[", int(f1), int(f2), int(f3), int(f4), "]",
        "(", Fraction(p1), Fraction(p2), Fraction(p3), ")",
        "(", alpha, beta, gamma, ")",
        float(cas2su4(alpha, beta, gamma)),
        int(dimsu4(f1, f2, f3, f4))
    ])
    
    # Determine minimum S,T values
    if ((2*p1) % 2 == 0):
        min_st = 0.0
    else:
        min_st = 0.5
    
    def Q(x):
        """Helper function for WTS calculation"""
        if (x > 0):
            return int(x**2 / 4.)
        else:
            return 0.0
    
    def WTS(w1, w2, T, S):
        """Weight multiplicity function"""
        w12 = (w1 + w2) / 2.
        if (T <= w12 and S <= w12 and w1 >= w2):
            result = (Q(w2+2-abs(T-S)) - Q(w2+1-T-S) + 
                     Q(T+S-w1-1) - Q(T+S-abs(T-S)-w1+w2+1)/2.)
        else:
            result = 0.0
        return result
    
    def Multi(p1, p2, p3, T, S):
        """Calculate multiplicity"""
        return (WTS(p1+abs(p3), p1-abs(p3), T, S) - 
                WTS(p1+p2+1, p1-p2-1, T, S) - 
                WTS(p2+abs(p3)-1, p2-abs(p3)-1, T, S))
    
    # Calculate ST branching rules
    ST_irreps = []
    sum_dim_st = 0.0
    
    if (min_st == 0):
        for S in range(int(min_st), int(max_st)+1, +1):
            for T in range(int(min_st), int(max_st)+1, +1):
                mult = Multi(p1, p2, p3, T, S)
                if (mult != 0):
                    dim_st = int(dimST(S, T, mult))
                    sum_dim_st = sum_dim_st + dimST(S, T, mult)
                    ST_irreps.append([S, T, int(mult), int(dim_st), int(sum_dim_st)])
    else:
        for S in range(int(min_st*2), int(max_st*2)+2, +2):
            for T in range(int(min_st*2), int(max_st*2)+2, +2):
                mult = Multi(p1, p2, p3, T/2., S/2.)
                dim_st = int(dimST(S/2., T/2., mult))
                sum_dim_st = sum_dim_st + dimST(S/2., T/2., mult)
                if (mult != 0):
                    ST_irreps.append([Fraction(S/2.), Fraction(T/2.), int(mult), 
                                    int(dim_st), int(sum_dim_st)])
    
    # Create DataFrames
    su4_df = pd.DataFrame(np.array(SU4_irrep), 
                         columns=["[", "f1", "f2", "f3", "f4", "]", "(", "p1", "p2", "p3", ")", 
                                "(", "α", "β", "γ", ")", "C_2[SU(4)]", "dimension"])
    
    irreps_df = pd.DataFrame(np.array(ST_irreps), 
                           columns=["Spin", "Isospin", "mult", "dim (S,T)", "cum_sum_dim(S,T)"])
    
    # Print output if verbose
    if verbose:
        print("● SU(4) Representation Info:(irrep notations, casimir order two, irrep dimension)")
        display(su4_df)
        print("\n● Branching Rules to (S, T):")
        display(irreps_df)
    
    return su4_df, irreps_df


def RacahSU4toST(f1, f2, f3, f4):
    """
    Legacy function for backward compatibility.
    
    This function maintains the exact same interface and behavior as the original code.
    
    Parameters:
    -----------
    f1, f2, f3, f4 : int
        Young tableau parameters (must satisfy f1 ≥ f2 ≥ f3 ≥ f4)
    
    Returns:
    --------
    pd.DataFrame
        ST branching rules DataFrame
    """
    try:
        su4_df, irreps_df = racah_su4_to_st(f1, f2, f3, f4, verbose=True)
        return irreps_df
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


# Additional utility functions
def validate_young_tableau(f1, f2, f3, f4):
    """
    Validate Young tableau conditions.
    
    Parameters:
    -----------
    f1, f2, f3, f4 : int
        Young tableau parameters
    
    Returns:
    --------
    bool
        True if valid Young tableau, False otherwise
    """
    return (f1 >= f2 >= f3 >= f4)


def get_su4_dimension(f1, f2, f3, f4):
    """
    Calculate the dimension of SU(4) irrep.
    
    Parameters:
    -----------
    f1, f2, f3, f4 : int
        Young tableau parameters
    
    Returns:
    --------
    int
        Dimension of the SU(4) irrep
    """
    if not validate_young_tableau(f1, f2, f3, f4):
        raise ValueError("Invalid Young tableau")
    
    return int((f1-f2+1)*(f1-f3+2)*(f1-f4+3)*(f2-f3+1)*(f2-f4+2)*(f3-f4+1)/12.)


def get_casimir_su4(f1, f2, f3, f4):
    """
    Calculate the second-order Casimir invariant for SU(4).
    
    Parameters:
    -----------
    f1, f2, f3, f4 : int
        Young tableau parameters
    
    Returns:
    --------
    float
        Second-order Casimir invariant
    """
    if not validate_young_tableau(f1, f2, f3, f4):
        raise ValueError("Invalid Young tableau")
    
        casimir = (3*alpha*(alpha+4)
               + 4*beta*(beta+4)
               + 3*gamma*(gamma+4)
               + 4*beta*(alpha+gamma)
               + 2*alpha*gamma)
        return float(casimir) 
