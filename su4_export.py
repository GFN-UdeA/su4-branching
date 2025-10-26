"""
su4_export.py
====================

Enhanced export functions for SU(4) branching data with representation labels.
Creates separate CSV and LaTeX files with proper identification.
"""

from pathlib import Path
import pandas as pd

def export_su4_with_labels(f1: int, f2: int, f3: int, f4: int, 
                          su4_module,
                          out_dir: str | Path = ".",
                          verbose: bool = True):
    """
    Export SU(4) representation data to labeled CSV and LaTeX files.
    
    Parameters:
    -----------
    f14 : int
        Young tableau parameters
    su4_module : module
        The su4_branching module
    out_dir : str or Path, default "."
        Output directory
    verbose : bool, default True
        Print progress messages
    
    Returns:
    --------
    dict
        Dictionary with paths to generated files
    """
    # Validate parameters
    if not (f1 >= f2 >= f3 >= f4):
        raise ValueError(f"Invalid Young tableau: [{f1},{f2},{f3},{f4}] must satisfy f1≥f2≥f3≥f4")
    
    # Create representation identifiers
    notation = f"[{f1},{f2},{f3},{f4}]"
    tag = f"{f1}_{f2}_{f3}_{f4}"
    
    # Generate DataFrames
    if verbose:
        print(f"Processing SU(4) representation {notation}...")
    
    su4_info, st_branching = su4_module.racah_su4_to_st(f1, f2, f3, f4, verbose=False)
    
    # Setup output directory
    out_dir = Path(out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Define file paths
    files = {
        'su4_csv': out_dir / f"su4_representation_{tag}.csv",
        'st_csv': out_dir / f"su4_branching_rules_{tag}.csv", 
        'su4_tex': out_dir / f"su4_representation_{tag}.tex",
        'st_tex': out_dir / f"su4_branching_rules_{tag}.tex"
    }
    
    # Export CSV files
    if verbose:
        print("Exporting CSV files...")
    su4_info.to_csv(files['su4_csv'], index=False)
    st_branching.to_csv(files['st_csv'], index=False)
    
    # Export LaTeX files
    if verbose:
        print("Exporting LaTeX files...")
    
    # SU(4) representation table
    with open(files['su4_tex'], "w", encoding="utf-8") as f:
        f.write(f"% SU(4) Representation {notation} Information\n")
        f.write(f"% Generated automatically\n\n")
        f.write(
            su4_info.to_latex(
                index=False,
                escape=False,
                column_format="|" + "c|" * len(su4_info.columns),  # DINÁMICO
                caption=rf"SU(4) Representation {notation} - Basic Information",
                label=f"tab:su4_info_{tag}",
                longtable=False,
                multicolumn=True,
                multicolumn_format="c",
                bold_rows=True,
                position="htbp"
            )
        )
    
    # Branching rules table
    with open(files['st_tex'], "w", encoding="utf-8") as f:
        f.write(f"% Branching Rules for SU(4) Representation {notation}\n")
        f.write(f"% Generated automatically\n\n")
        f.write(
            st_branching.to_latex(
                index=False,
                escape=False,
                column_format="|c|c|c|c|c|",  # CORREGIDO - comilla de cierre añadida
                caption=rf"Branching Rules for SU(4) Representation {notation} to $(S,T)$",
                label=f"tab:branching_rules_{tag}",
                longtable=False,
                multicolumn=True,
                multicolumn_format="c",
                bold_rows=True,
                position="htbp"
            )
        )
    
    # Report results
    if verbose:
        print(f"\nFiles created for representation {notation}:")
        for file_type, path in files.items():
            print(f" • {path.name}")
        print(f"\nLaTeX labels:")
        print(f" • tab:su4_info_{tag}")
        print(f" • tab:branching_rules_{tag}")
    
    return files

def export_multiple_representations(irrep_list: list[tuple[int,int,int,int]], 
                                   su4_module,
                                   out_dir: str | Path = ".",
                                   verbose: bool = True):
    """
    Export multiple SU(4) representations with labels.
    
    Parameters:
    -----------
    irrep_list : list of tuples
        List of (f1,f2,f3,f4) Young tableau parameters
    su4_module : module
        The su4_branching module
    out_dir : str or Path, default "."
        Output directory
    verbose : bool, default True
        Print progress messages
    
    Returns:
    --------
    dict
        Dictionary mapping each representation to its generated files
    """
    results = {}
    successful = 0
    failed = 0
    
    if verbose:
        print(f"Batch export: {len(irrep_list)} representations")
        print("-" * 50)
    
    for i, (f1, f2, f3, f4) in enumerate(irrep_list, 1):
        try:
            if verbose:
                print(f"[{i:2d}/{len(irrep_list)}] [{f1},{f2},{f3},{f4}]...", end=" ")
            
            files = export_su4_with_labels(f1, f2, f3, f4, su4_module, 
                                         out_dir, verbose=False)
            results[(f1, f2, f3, f4)] = files
            successful += 1
            
            if verbose:
                print("✓")
                
        except Exception as e:
            failed += 1
            if verbose:
                print(f"✗ Error: {e}")
    
    if verbose:
        print("-" * 50)
        print(f"Summary: {successful} successful, {failed} failed")
    
    return results

# Command line interface
if __name__ == "__main__":
    import argparse
    import su4_branching
    
    parser = argparse.ArgumentParser(
        description="Export SU(4) representation data with labels"
    )
    parser.add_argument("f1", type=int)
    parser.add_argument("f2", type=int)  
    parser.add_argument("f3", type=int)
    parser.add_argument("f4", type=int)
    parser.add_argument("-o", "--out_dir", default=".",
                        help="Output directory")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress output messages")
    
    args = parser.parse_args()
    
    try:
        files = export_su4_with_labels(
            args.f1, args.f2, args.f3, args.f4,
            su4_branching, args.out_dir, 
            verbose=not args.quiet
        )
        if not args.quiet:
            print(f"\nExport completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
