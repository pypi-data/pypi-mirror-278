[[_TOC_]]

# Description

Code used to do checks on data and MC.

# Installation

Use it as part of the rest of the analysis code through:

```
https://gitlab.cern.ch/r_k/setup
```

# Scripts

The project can do the following:

## Check for missing cached ntuples

In order to do several studies a selection is applied to the ntuples. The resulting files are named as `x_y.root` (i.e. `3_5.root`). Meaning that this is the `xth` file out of `y` files. This is needed to parallelize the selection and send it to the cluster. These numbers can be used to check that no files is missing with:

```bash
check_cached_ntuples -v v10.21p2
```

where the argument is the version of the ntuples. It is assumed that for each ntuple there will be 3 other files. This is specified inside the script as:

```python
files_per_tuple = 4
```

and it can be changed if needed.

## Truth matching

### Check truth matching efficiency

Some peaky structure gets dropped every time we use `TRUEID` to truth match. We have to account for it to compensate its effect in the efficiency calculation. The code will:

1. Apply the full selection but the mass, bdt and truth matching cut.
1. Fit the passed and failed truth matching sample
1. Produce a JSON file with the efficiency correction

Use it as:

```bash
check_truth_eff -p ctrl -t ETOS -y 2018 -v v10.21p2 -k all_gorder_no_truth_mass_bdt -m trueid -i /eos/home-a/acampove/Data/RK/cache/tools/apply_selection/
```

where `-i` is optional, if not used, it will take the files from the `CASDIR/tools/apply_selection`. This is done in order to access the ntuples from the closest site (IHEP, CERN, etc).

To run over all triggers, processes and years do:

```bash
check_truth_eff -v v10.21p2 -k all_gorder_no_truth_mass_bdt -m trueid -i /eos/home-a/acampove/Data/RK
```

### Plot truth efficiency

The script above will produce a JSON file with efficiencies, run:

```bash
plot_truth_eff -v v10.21p2 -m trueid
```

to make that JSON file into a set of plots with the efficiencies compared, as well as the ratios and double ratios of efficiencies.

## Check clone tracks

As part of the convenors comments, we were asked to check the angle between the Kaon and lepton. This is done with

```bash
check_clone -t MTOS -y all -q jpsi
```

for instance. This will make a plot of the angle for the SS and OS pairs and save them in the current directory.

## Extract mass scales and resolutions

For this we:

1. Fit simulation after the full selelction 
1. Fit data with tails of signal fixed according to fit above.
1. From the fitting parameters we make plots and tables.

### Fit unconstrained mass distribution

For this run:

```bash
unconstrained_fits
```

use `-h` to know what options to pass. This will dump plots of the fits and JSON files with the fit parameters.

### Make plots and tables

For this run:

```bash
check_scales -v v3 -y 2018
```
which will take the parameters from fit version `v3` (done with the lines above) and year `2018`. Do not pass the year if you want 
to do every year.


