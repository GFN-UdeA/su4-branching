#!/usr/bin/env python3

"""
SU(4) Branching Rules - Command-Line Interface (CLI)
with Pauli Exclusion Principle Constraint Checking
and SU(4) Irrep Simplification (Jupyter-style)

Run from terminal: python su4_cli.py

"""

import argparse
import os, sys
from pathlib import Path
from typing import Tuple
import numpy as np

# Add module path
module_path = os.path.abspath("/home/pvalen/su4-branching/su4_branching")
if module_path not in sys.path:
    sys.path.append(module_path)

class SymmetryError(ValueError):
    """Exception for symmetry constraint violations"""
    pass

def u6_to_su4_irrep(u6_irrep: Tuple[int, ...]) -> Tuple[int, int, int, int]:
    """
    Convert U(6) Young tableau to SU(4) irrep with proper validation and simplification.
    
    Uses EXACT algorithm from Jupyter Notebook:
    1. Validate input (6 elements, non-negative, non-increasing)
    2. Check Pauli constraint: f1 <= 4
    3. Compute conjugate partition (transpose Young diagram)
    4. Simplify by removing columns of height 4 or greater
    5. Return [f1, f2, f3, f4]
    """
    # Validate input format and constraints
    if len(u6_irrep) != 6 or any(not isinstance(x, int) or x < 0 for x in u6_irrep):
        raise SymmetryError("Input must be 6 non-negative integers")
    
    if list(u6_irrep) != sorted(u6_irrep, reverse=True):
        raise SymmetryError("Young diagram must be non-increasing sequence")
        
    # CHECK PAULI EXCLUSION PRINCIPLE CONSTRAINT on U(6) FIRST COLUMN: f1 <= 4
    f1_u6 = u6_irrep[0]
    
    if f1_u6 > 4:
        u6_label = "{" + ", ".join(map(str, u6_irrep)) + "}"
        raise SymmetryError(
            f"❌ PAULI EXCLUSION PRINCIPLE VIOLATED ❌\n"
            f"   U(6) irrep: {u6_label}\n"
            f"   f₁ᵁ⁽⁶⁾ = {f1_u6} > 4 NOT ALLOWED\n"
            f"   First row of U(6) Young diagram cannot exceed 4 boxes\n"
            f"   Physical reason: Cannot have >4 nucleons in same spatial state\n"
            f"   (spin-isospin: 2 spin × 2 isospin = 4 quantum states per spatial orbital)"
        )    
    
    # Compute conjugate partition (transpose Young diagram)
    current = np.array(u6_irrep, dtype=np.int32)
    su4_irrep = []
    
    while np.any(current > 0):
        # Count non-zero elements in current column (height of column)
        non_zero_count = np.count_nonzero(current)
        su4_irrep.append(non_zero_count)
        # Remove first column and decrement remaining elements
        current = current[current > 0] - 1
    
    # Simplify SU(4) irrep by removing columns of length 4 or greater
    while (len(su4_irrep) >= 4):
        last_element = su4_irrep[-1]
        su4_irrep = [x - last_element for x in su4_irrep[:-1]]

    f1 = su4_irrep[0] if len(su4_irrep) > 0 else 0    
    # Pad with zeros to ensure exactly 4 elements
    su4_irrep.extend([0] * (4 - len(su4_irrep)))
    
    f1, f2, f3, f4 = tuple(int(x) for x in su4_irrep[:4])
    
    return f1, f2, f3, f4

def u10_to_su4_irrep(u10_irrep: Tuple[int, ...]) -> Tuple[int, int, int, int]:
    """
    Convert U(10) Young tableau to SU(4) irrep with proper validation and simplification.
    
    Uses EXACT algorithm from Jupyter Notebook (adapted for U(10)):
    1. Validate input (10 elements, non-negative, non-increasing)
    2. Check Pauli constraint: f1 <= 4
    3. Compute conjugate partition (transpose Young diagram)
    4. Simplify by removing columns of height 4 or greater
    5. Return [f1, f2, f3, f4]
    """
    # Validate input format and constraints
    if len(u10_irrep) != 10 or any(not isinstance(x, int) or x < 0 for x in u10_irrep):
        raise SymmetryError("Input must be 10 non-negative integers")
    
    if list(u10_irrep) != sorted(u10_irrep, reverse=True):
        raise SymmetryError("Young diagram must be non-increasing sequence")
        
    # CHECK PAULI EXCLUSION PRINCIPLE CONSTRAINT on U(10) FIRST COLUMN: f1 <= 4
    f1_u10 = u10_irrep[0]
    
    if f1_u10 > 4:
        u10_label = "{" + ", ".join(map(str, u10_irrep)) + "}"
        raise SymmetryError(
            f"❌ PAULI EXCLUSION PRINCIPLE VIOLATED ❌\n"
            f"   U(10) irrep: {u10_label}\n"
            f"   f₁ᵁ⁽¹⁰⁾ = {f1_u10} > 4 NOT ALLOWED\n"
            f"   First row of U(10) Young diagram cannot exceed 4 boxes\n"
            f"   Physical reason: Cannot have >4 nucleons in same spatial state\n"
            f"   (spin-isospin: 2 spin × 2 isospin = 4 quantum states per pf orbital)"
        )    
    
    # Compute conjugate partition (transpose Young diagram)
    current = np.array(u10_irrep, dtype=np.int32)
    su4_irrep = []
    
    while np.any(current > 0):
        # Count non-zero elements in current column (height of column)
        non_zero_count = np.count_nonzero(current)
        su4_irrep.append(non_zero_count)
        # Remove first column and decrement remaining elements
        current = current[current > 0] - 1
    
    # Simplify SU(4) irrep by removing columns of length 4 or greater
    while (len(su4_irrep) >= 4):
        last_element = su4_irrep[-1]
        su4_irrep = [x - last_element for x in su4_irrep[:-1]]

    f1 = su4_irrep[0] if len(su4_irrep) > 0 else 0    
    # Pad with zeros to ensure exactly 4 elements
    su4_irrep.extend([0] * (4 - len(su4_irrep)))
    
    f1, f2, f3, f4 = tuple(int(x) for x in su4_irrep[:4])
    
    return f1, f2, f3, f4

def u6_conjugate(u6_young):
    """Convert U(6) Young tableau to SU(4) (wrapper for Jupyter-style function)"""
    return u6_to_su4_irrep(u6_young)

def u10_conjugate(u10_young):
    """Convert U(10) Young tableau to SU(4) (wrapper for Jupyter-style function)"""
    return u10_to_su4_irrep(u10_young)

def run_example_sd_shell():
    """Run example with sd-shell nuclei (U(6))"""
    print("\n" + "=" * 80)
    print("EXAMPLE: sd-shell nuclei (U(6) ⊗ SU(4))")
    print("=" * 80 + "\n")
    
    import su4_branching
    
    u6_irrep = (2, 1, 1, 0, 0, 0)
    
    print(f"U(6) irrep: {u6_irrep}")
    print(f"Pauli check: f₁ = {u6_irrep[0]} ≤ 4 ✓")
    
    f1, f2, f3, f4 = u6_conjugate(u6_irrep)
    
    print(f"SU(4) irrep (simplified): [{f1}, {f2}, {f3}, {f4}]\n")
    
    su4_df, st_df = su4_branching.racah_su4_to_st(
        f1, f2, f3, f4, verbose=False
    )
    
    print("Branching decomposition (S, T) multiplets:")
    print("-" * 80)
    print(st_df.to_string(index=False))
    print("-" * 80 + "\n")

def run_example_pf_shell():
    """Run example with pf-shell nuclei (U(10))"""
    print("\n" + "=" * 80)
    print("EXAMPLE: pf-shell nuclei (U(10) ⊗ SU(4))")
    print("=" * 80 + "\n")
    
    import su4_branching
    
    u10_irrep = (2, 2, 1, 1, 0, 0, 0, 0, 0, 0)
    
    print(f"U(10) irrep: {u10_irrep}")
    print(f"Pauli check: f₁ = {u10_irrep[0]} ≤ 4 ✓")
    
    f1, f2, f3, f4 = u10_conjugate(u10_irrep)
    
    print(f"SU(4) irrep (simplified): [{f1}, {f2}, {f3}, {f4}]\n")
    
    su4_df, st_df = su4_branching.racah_su4_to_st(
        f1, f2, f3, f4, verbose=False
    )
    
    print(f"Branching decomposition ({len(st_df)} (S, T) multiplets):")
    print("-" * 80)
    print(st_df.head(15).to_string(index=False))
    if len(st_df) > 15:
        print(f"... ({len(st_df) - 15} more rows)")
    print("-" * 80 + "\n")

def run_custom_sd(u6_irrep):
    """Run custom sd-shell U(6) calculation with Pauli checking"""
    print("\n" + "=" * 80)
    print(f"CUSTOM SD-SHELL: U(6) irrep {u6_irrep}")
    print("=" * 80 + "\n")
    
    import su4_branching
    
    # Convert U(6) to SU(4) (includes Pauli check and simplification)
    try:
        f1, f2, f3, f4 = u6_conjugate(u6_irrep)
        print(f"Pauli check: f₁ = {u6_irrep[0]} ≤ 4 ✓")
        print(f"Converted to SU(4) irrep (simplified): [{f1}, {f2}, {f3}, {f4}]\n")
        
        su4_df, st_df = su4_branching.racah_su4_to_st(
            f1, f2, f3, f4, verbose=False
        )
        
        try:
            total_dim = int(st_df['dim (S,T)'].sum())
            print(f"Dimension: {total_dim:,}")
        except (KeyError, ValueError):
            pass
        
        print(f"\nBranching decomposition ({len(st_df)} (S, T) multiplets):")
        print("-" * 80)
        print(st_df.to_string(index=False))
        print("-" * 80 + "\n")
        
    except SymmetryError as e:
        print(str(e) + "\n")
        return False
    
    return True

def run_custom_pf(u10_irrep):
    """Run custom pf-shell U(10) calculation with Pauli checking"""
    print("\n" + "=" * 80)
    print(f"CUSTOM PF-SHELL: U(10) irrep {u10_irrep}")
    print("=" * 80 + "\n")
    
    import su4_branching
    
    # Convert U(10) to SU(4) (includes Pauli check and simplification)
    try:
        f1, f2, f3, f4 = u10_conjugate(u10_irrep)
        print(f"Pauli check: f₁ = {u10_irrep[0]} ≤ 4 ✓")
        print(f"Converted to SU(4) irrep (simplified): [{f1}, {f2}, {f3}, {f4}]\n")
        
        su4_df, st_df = su4_branching.racah_su4_to_st(
            f1, f2, f3, f4, verbose=False
        )
        
        try:
            total_dim = int(st_df['dim (S,T)'].sum())
            print(f"Dimension: {total_dim:,}")
        except (KeyError, ValueError):
            pass
        
        print(f"\nBranching decomposition ({len(st_df)} (S, T) multiplets):")
        print("-" * 80)
        print(st_df.to_string(index=False))
        print("-" * 80 + "\n")
        
    except SymmetryError as e:
        print(str(e) + "\n")
        return False
    
    return True

def run_custom(f1, f2, f3, f4=0):
    """Run custom SU(4) irrep calculation"""
    print("\n" + "=" * 80)
    print(f"CUSTOM SU(4): irrep [{f1}, {f2}, {f3}, {f4}]")
    print("=" * 80 + "\n")
    
    import su4_branching
    
    su4_df, st_df = su4_branching.racah_su4_to_st(
        f1, f2, f3, f4, verbose=False
    )
    
    try:
        total_dim = int(st_df['dim (S,T)'].sum())
        print(f"Dimension: {total_dim:,}")
    except (KeyError, ValueError):
        pass
    
    print(f"\nBranching decomposition ({len(st_df)} (S, T) multiplets):")
    print("-" * 80)
    print(st_df.to_string(index=False))
    print("-" * 80 + "\n")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description='SU(4) Branching Rules Calculator with Pauli Constraint and SU(4) Simplification',
        epilog="""Examples:

python su4_cli.py --test

python su4_cli.py --sd-shell

python su4_cli.py --pf-shell

python su4_cli.py --custom-sd 3 2 1 0 0 0

python su4_cli.py --custom-pf 2 2 1 1 0 0 0 0 0 0

python su4_cli.py --custom-pf 4 2 0 0 0 0 0 0 0 0

python su4_cli.py --custom-su4 8 5 5 0

""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument('--test', action='store_true',
                       help='Test package installation')
    group.add_argument('--sd-shell', action='store_true',
                       help='Run sd-shell example (U(6) ⊗ SU(4))')
    group.add_argument('--pf-shell', action='store_true',
                       help='Run pf-shell example (U(10) ⊗ SU(4))')
    group.add_argument('--custom-sd', nargs=6, type=int, metavar='YOUNG',
                       help='Custom U(6): [f1 f2 f3 f4 f5 f6]')
    group.add_argument('--custom-pf', nargs=10, type=int, metavar='YOUNG',
                       help='Custom U(10): [f1 f2 ... f10]')
    group.add_argument('--custom-su4', nargs='+', type=int, metavar='IRREP',
                       help='Custom SU(4): [f1 f2 f3 (f4)]')
    
    args = parser.parse_args()
    
    # Test mode
    if args.test:
        print("\n" + "=" * 80)
        print("TESTING INSTALLATION")
        print("=" * 80 + "\n")
        try:
            import su4_branching
            print("✓ su4_branching imported successfully")
            return 0
        except ImportError as e:
            print(f"✗ Failed: {e}")
            return 1
    
    # SD-shell example
    if args.sd_shell:
        try:
            run_example_sd_shell()
            return 0
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    # PF-shell example
    if args.pf_shell:
        try:
            run_example_pf_shell()
            return 0
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    # Custom SD-shell
    if args.custom_sd:
        try:
            u6_irrep = tuple(args.custom_sd)
            success = run_custom_sd(u6_irrep)
            return 0 if success else 1
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    # Custom PF-shell
    if args.custom_pf:
        try:
            u10_irrep = tuple(args.custom_pf)
            success = run_custom_pf(u10_irrep)
            return 0 if success else 1
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    # Custom SU(4)
    if args.custom_su4:
        try:
            if len(args.custom_su4) < 3 or len(args.custom_su4) > 4:
                print("✗ SU(4) irrep requires 3 or 4 integers: [f1 f2 f3 (f4)]")
                return 1
            
            f1, f2, f3 = args.custom_su4[:3]
            f4 = args.custom_su4[3] if len(args.custom_su4) == 4 else 0
            
            run_custom(f1, f2, f3, f4)
            return 0
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
