#!/usr/bin/env python3
"""
SU(4) Branching Rules - Command-Line Interface (CLI)
Run from terminal: python su4_cli.py
"""

import argparse
import os, sys
from pathlib import Path

# Add module path
module_path = os.path.abspath("/home/pvalen/su4-branching/su4_branching")
if module_path not in sys.path:
    sys.path.append(module_path)


def u6_conjugate(u6_young):
    """Convert U(6) Young tableau to SU(4) via conjugate partition"""
    # Compute conjugate: count non-zero elements in each column
    current = list(u6_young)
    su4 = []
    
    while any(x > 0 for x in current):
        count = sum(1 for x in current if x > 0)
        su4.append(count)
        current = [x - 1 for x in current if x > 0]
    
    # Pad to 4 elements
    while len(su4) < 4:
        su4.append(0)
    
    return tuple(su4[:4])


def u10_conjugate(u10_young):
    """Convert U(10) Young tableau to SU(4) via conjugate partition"""
    # Same algorithm as U(6)
    current = list(u10_young)
    su4 = []
    
    while any(x > 0 for x in current):
        count = sum(1 for x in current if x > 0)
        su4.append(count)
        current = [x - 1 for x in current if x > 0]
    
    # Pad to 4 elements
    while len(su4) < 4:
        su4.append(0)
    
    return tuple(su4[:4])


def run_example_sd_shell():
    """Run example with sd-shell nuclei (U(6))"""
    print("\n" + "=" * 80)
    print("EXAMPLE: sd-shell nuclei (U(6) ⊗ SU(4))")
    print("=" * 80 + "\n")
    
    import su4_branching
    
    u6_irrep = (2, 1, 1, 0, 0, 0)
    print(f"U(6) irrep: {u6_irrep}")
    
    f1, f2, f3, f4 = u6_conjugate(u6_irrep)
    print(f"SU(4) irrep: [{f1}, {f2}, {f3}, {f4}]\n")
    
    su4_df, st_df = su4_branching.racah_su4_to_st(f1, f2, f3, f4, verbose=False)
    
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
    
    f1, f2, f3, f4 = u10_conjugate(u10_irrep)
    print(f"SU(4) irrep: [{f1}, {f2}, {f3}, {f4}]\n")
    
    su4_df, st_df = su4_branching.racah_su4_to_st(f1, f2, f3, f4, verbose=False)
    
    print(f"Branching decomposition ({len(st_df)} (S, T) multiplets):")
    print("-" * 80)
    print(st_df.head(15).to_string(index=False))
    if len(st_df) > 15:
        print(f"... ({len(st_df) - 15} more rows)")
    print("-" * 80 + "\n")


def run_custom_sd(u6_irrep):
    """Run custom sd-shell U(6) calculation"""
    print("\n" + "=" * 80)
    print(f"CUSTOM SD-SHELL: U(6) irrep {u6_irrep}")
    print("=" * 80 + "\n")
    
    import su4_branching
    
    # Convert U(6) to SU(4)
    f1, f2, f3, f4 = u6_conjugate(u6_irrep)
    print(f"Converted to SU(4) irrep: [{f1}, {f2}, {f3}, {f4}]\n")
    
    su4_df, st_df = su4_branching.racah_su4_to_st(f1, f2, f3, f4, verbose=False)
    
    try:
        total_dim = int(st_df['dim (S,T)'].sum())
        print(f"Dimension: {total_dim:,}")
    except (KeyError, ValueError):
        pass
    
    print(f"\nBranching decomposition ({len(st_df)} (S, T) multiplets):")
    print("-" * 80)
    print(st_df.to_string(index=False))
    print("-" * 80 + "\n")


def run_custom_pf(u10_irrep):
    """Run custom pf-shell U(10) calculation"""
    print("\n" + "=" * 80)
    print(f"CUSTOM PF-SHELL: U(10) irrep {u10_irrep}")
    print("=" * 80 + "\n")
    
    import su4_branching
    
    # Convert U(10) to SU(4)
    f1, f2, f3, f4 = u10_conjugate(u10_irrep)
    print(f"Converted to SU(4) irrep: [{f1}, {f2}, {f3}, {f4}]\n")
    
    su4_df, st_df = su4_branching.racah_su4_to_st(f1, f2, f3, f4, verbose=False)
    
    try:
        total_dim = int(st_df['dim (S,T)'].sum())
        print(f"Dimension: {total_dim:,}")
    except (KeyError, ValueError):
        pass
    
    print(f"\nBranching decomposition ({len(st_df)} (S, T) multiplets):")
    print("-" * 80)
    print(st_df.to_string(index=False))
    print("-" * 80 + "\n")


def run_custom(f1, f2, f3, f4=0):
    """Run custom SU(4) irrep calculation"""
    print("\n" + "=" * 80)
    print(f"CUSTOM SU(4): irrep [{f1}, {f2}, {f3}, {f4}]")
    print("=" * 80 + "\n")
    
    import su4_branching
    
    su4_df, st_df = su4_branching.racah_su4_to_st(f1, f2, f3, f4, verbose=False)
    
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
        description='SU(4) Branching Rules Calculator',
        epilog='''Examples:
  python su4_cli.py --test
  python su4_cli.py --sd-shell
  python su4_cli.py --pf-shell
  python su4_cli.py --custom-sd 3 2 1 0 0 0
  python su4_cli.py --custom-pf 2 2 1 1 0 0 0 0 0 0
  python su4_cli.py --custom-su4 8 5 5 0
        ''',
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
                      help='Custom U(6) calculation: [f1 f2 f3 f4 f5 f6]')
    group.add_argument('--custom-pf', nargs=10, type=int, metavar='YOUNG',
                      help='Custom U(10) calculation: [f1 f2 ... f10]')
    group.add_argument('--custom-su4', nargs='+', type=int, metavar='IRREP',
                      help='Custom SU(4) calculation: [f1 f2 f3 (f4)]')
    
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
            run_custom_sd(u6_irrep)
            return 0
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    # Custom PF-shell
    if args.custom_pf:
        try:
            u10_irrep = tuple(args.custom_pf)
            run_custom_pf(u10_irrep)
            return 0
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    # Custom SU(4)
    if args.custom_su4:
        try:
            if len(args.custom_su4) == 3:
                f1, f2, f3 = args.custom_su4
                run_custom(f1, f2, f3, 0)
            elif len(args.custom_su4) == 4:
                f1, f2, f3, f4 = args.custom_su4
                run_custom(f1, f2, f3, f4)
            else:
                print("✗ Provide 3 or 4 arguments for SU(4)")
                return 1
            return 0
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
