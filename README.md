# SU(4) Branching Rules Toolkit

**Complete Guide for Installation, Terminal Use, and Jupyter Notebook**

Calculate SU(4) → SU(2)_S ⊗ SU(2)_T decompositions for nuclear structure theory.

**Developed by:** J.P. Valencia, S. Cordoba, R. Henao

---

## 📋 Quick Start (TL;DR)

```bash-zsh
# 1. Install using corrected installer
python install_su4_branching.py

# 2. Test
python su4_cli.py --test

# 3. Run examples
python su4_cli.py --sd-shell
python su4_cli.py --pf-shell

# 4. Use Jupyter
jupyter notebook su4branching_test.ipynb
```

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Terminal Usage (su4_cli.py)](#terminal-usage)
5. [Jupyter Notebook Usage](#jupyter-notebook-usage)
6. [Project Structure](#project-structure)
7. [Troubleshooting](#troubleshooting)

---

## Features

✅ Compute SU(4) branching rules to (S,T) multiplets  
✅ Support for sd-shell (U(6)) and pf-shell (U(10)) nuclei  
✅ High-dimensional irreps (up to 10⁶ dimension)  
✅ Multiple export formats (.dat, .csv, .tex)  
✅ Interactive Jupyter notebook with examples  
✅ Command-line interface for batch processing  
✅ Modern Python packaging (PEP 517/518)  
✅ Automatic U(6) ⊗ SU(4) and U(10) ⊗ SU(4) conversion  

---

## Requirements

### System
- **OS:** Linux, macOS, or Windows
- **Python:** 3.8 or later
- **Disk Space:** ~100 MB

### Python Packages (Auto-installed)
| Package | Version | Purpose |
|---------|---------|---------|
| numpy | ≥1.19.0 | Numerical computing |
| pandas | ≥1.1.0 | Data tables |
| matplotlib | ≥3.3.0 | Plotting |
| jupyter | latest | Notebooks |
| setuptools | ≥64 | Package management |

---

## Installation

### Option 1: Corrected Automated Installer (Recommended)

```bash-zsh
# 1. clone git repository
git clone  https://github.com/GFN-UdeA/su4-branching.git


# 2. Run installer (creates CORRECT __init__.py)
python install_su4_branching.py

# 3. Follow prompts and select installation directory
# Default: ~/su4-branching

# 4.Copy your files
 - su4_branching.py → su4_branching/
 - su4_export.py → su4_branching/
 - su4_cli.py → project root
 - su4branching_test.ipynb → project root

```
**What the installer does:**
- ✓ Checks Python version (3.8+)
- ✓ Installs/verifies dependencies
- ✓ Creates CORRECT `__init__.py` (no broken imports)
- ✓ Creates modern `pyproject.toml`
- ✓ Creates `setup.py` (fallback)
- ✓ Installs package with `pip install --use-pep517 -e .`
- ✓ Tests installation

 
### Option 2: Manual Installation
```bash-zsh
# Create project directory
mkdir su4-branching
cd su4-branching

# Install dependencies
pip install --upgrade numpy pandas setuptools jupyter matplotlib

# Create package structure
mkdir su4_branching
touch su4_branching/__init__.py
# Install package
pip install --use-pep517 -e .
```

### Verify Installation

```bash-zsh
# Test import
python -c "import su4_branching; print('✓ Success')"

# Test CLI
python su4_cli.py --test

# Expected output:
# ✓ su4_branching module found
# ✓ racah_su4_to_st function available ✓
```

---

## Terminal Usage (su4_cli.py)

### Basic Commands

#### 1. Test Installation
```bash-zsh
python su4_cli.py --test
```

#### 2. Run sd-shell Example (U(6) ⊗ SU(4))
```bash-zsh
python su4_cli.py --sd-shell
```

**Output:** Shows branching for 4 nucleons in sd-shell configuration

#### 3. Run pf-shell Example (U(10) ⊗ SU(4))
```bash-zsh
python su4_cli.py --pf-shell
```

**Output:** Shows branching for 6 nucleons in pf-shell configuration

### Custom Calculations

#### 4. Custom U(6) Calculation (sd-shell)
```bash-zsh
# Format: --custom-sd [6 numbers for U(6) Young diagram]
python su4_cli.py --custom-sd 3 2 1 0 0 0

# Other examples:
python su4_cli.py --custom-sd 2 1 1 0 0 0
python su4_cli.py --custom-sd 4 2 0 0 0 0
```

#### 5. Custom U(10) Calculation (pf-shell)
```bash-zsh
# Format: --custom-pf [10 numbers for U(10) Young diagram]
python su4_cli.py --custom-pf 3 3 2 2 0 0 0 0 0 0

# Other examples:
python su4_cli.py --custom-pf 2 2 1 1 0 0 0 0 0 0
python su4_cli.py --custom-pf 4 3 2 1 0 0 0 0 0 0
```

#### 6. Direct SU(4) Calculation
```bash-zsh
# Format: --custom-su4 [f1 f2 f3 (f4)]
python su4_cli.py --custom-su4 8 5 5 0
python su4_cli.py --custom-su4 5 3 2
python su4_cli.py --custom-su4 12 6 3 0
```

### Help and Options

```bash-zsh
python su4_cli.py --help
```

---

## Jupyter Notebook Usage (su4branching_test.ipynb)

### Start Jupyter

```bash-zsh
jupyter notebook su4branching_test.ipynb
```

Browser will open at `http://localhost:8888`

### Cell 1: Import Modules

```python
import su4_branching
import pandas as pd
print("✓ Modules imported")
```

### Cell 2: Simple Calculation

```python
# Calculate [8, 5, 5, 0]
f1, f2, f3, f4 = 8, 5, 5, 0
su4_df, st_df = su4_branching.racah_su4_to_st(f1, f2, f3, f4, verbose=False)

print(f"SU(4) irrep: [{f1}, {f2}, {f3}, {f4}]")
print(f"Number of (S,T) multiplets: {len(st_df)}")
print("\nBranching decomposition:")
print(st_df)
```

### Cell 3: U(6) → SU(4) Conversion

```python
# Define U(6) Young diagram
u6_irrep = (3, 2, 1, 0, 0, 0)

# Manual conversion function (from su4_cli)
def u6_conjugate(u6_young):
    current = list(u6_young)
    su4 = []
    while any(x > 0 for x in current):
        count = sum(1 for x in current if x > 0)
        su4.append(count)
        current = [x - 1 for x in current if x > 0]
    while len(su4) < 4:
        su4.append(0)
    return tuple(su4[:4])

f1, f2, f3, f4 = u6_conjugate(u6_irrep)
print(f"U(6) {u6_irrep} → SU(4) [{f1}, {f2}, {f3}, {f4}]")

# Calculate branching
su4_df, st_df = su4_branching.racah_su4_to_st(f1, f2, f3, f4, verbose=False)
print(f"Total dimension: {int(st_df['dim (S,T)'].sum()):,}")
print(st_df)
```

### Cell 4: U(10) → SU(4) Conversion

```python
# Define U(10) Young diagram
u10_irrep = (3, 3, 2, 2, 0, 0, 0, 0, 0, 0)

# Manual conversion function
def u10_conjugate(u10_young):
    current = list(u10_young)
    su4 = []
    while any(x > 0 for x in current):
        count = sum(1 for x in current if x > 0)
        su4.append(count)
        current = [x - 1 for x in current if x > 0]
    while len(su4) < 4:
        su4.append(0)
    return tuple(su4[:4])

f1, f2, f3, f4 = u10_conjugate(u10_irrep)
print(f"U(10) {u10_irrep} → SU(4) [{f1}, {f2}, {f3}, {f4}]")

# Calculate branching
su4_df, st_df = su4_branching.racah_su4_to_st(f1, f2, f3, f4, verbose=False)
print(f"Total dimension: {int(st_df['dim (S,T)'].sum()):,}")
print(st_df.head(10))
```

### Tips

- **Run cell:** Shift + Enter
- **Save notebook:** Ctrl + S
- **Clear outputs:** Kernel → Restart & Clear Output
- **Insert cell:** Insert → Cell Below

---

## Project Structure

```
su4-branching/
├── README.md                    ← This file
├── setup.py                     ← Setup script (minimal)
├── pyproject.toml              ← Modern Python config (PEP 517/518)
│
├── su4_cli.py                  ← Command-line interface
├── su4branching_test.ipynb     ← Jupyter notebook with examples
│
└── su4_branching/              ← Python package
    ├── __init__.py             ← CORRECT (imports only racah_su4_to_st)
    ├── su4_branching.py        ← Core calculations
    └── su4_export.py           ← Export to .dat/.csv/.tex
```

---

## Troubleshooting

### Problem 1: Python Not Found

```bash-zsh
python: command not found
```

**Solution:**
```bash-zsh
python3 --version
# Use python3 instead of python
python3 su4_cli.py --test
```

### Problem 2: Import Error

```bash-zsh
ModuleNotFoundError: No module named 'su4_branching'
```

**Solution:**
```bash-zsh
# Reinstall package
cd su4-branching
pip install --use-pep517 -e .
```

### Problem 3: Jupyter Not Found

```bash-zsh
jupyter: command not found
```

**Solution:**
```bash-zsh
pip install jupyter
jupyter notebook su4branching_test.ipynb
```

### Problem 4: Import Warnings

```bash-zsh
Warning: Could not import modules: cannot import name 'su4_dimension'
```

**Solution:** This is FIXED with the corrected installer. If you see this:
1. Delete old `__init__.py`
2. Use the corrected installer: `python install_su4_branching_corrected.py`

### Problem 5: Permission Denied

```bash-zsh
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash-zsh
pip install --user --use-pep517 -e .
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python su4_cli.py --test` | Test installation |
| `python su4_cli.py --sd-shell` | Run sd-shell example |
| `python su4_cli.py --pf-shell` | Run pf-shell example |
| `python su4_cli.py --custom-sd 3 2 1 0 0 0` | Custom sd-shell |
| `python su4_cli.py --custom-pf 3 3 2 2 0 0 0 0 0 0` | Custom pf-shell |
| `python su4_cli.py --custom-su4 8 5 5 0` | Direct SU(4) calc |
| `python su4_cli.py --help` | Show all options |
| `jupyter notebook su4branching_test.ipynb` | Open notebook |

---

## Citation

If you use this toolkit in your research, please cite:

```bibtex
@misc{quintero2025automatedcalculationspinisospin,
 395 │       title={Automated calculation of spin, isospin branching rules for su(4) irreps}, 
 396 │       author={S. Quintero and R. Henao and J. P. Valencia},
 397 │       year={2025},
 398 │       eprint={2511.00216},
 399 │       archivePrefix={arXiv},
 400 │       primaryClass={nucl-th},
 401 │       url={https://arxiv.org/abs/2511.00216}, 
 402 │ }
```

---

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review Jupyter notebook examples
3. Run `python su4_cli.py --help`
4. Contact: patricio.valencia@udea.edu.co

---

**Last Updated:** October 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✓
