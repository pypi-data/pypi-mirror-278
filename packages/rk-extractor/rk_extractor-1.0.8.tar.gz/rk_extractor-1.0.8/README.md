[[_TOC_]]

# Purpose

This project is used to calculate $R_K$ from:

1. The fitting model for the signal region.
1. The data in the signal region.
1. The $c_k^{r,t}$ vector and the corresponding covariance matrices.
1. Any constraint on the nuisance parameters

The tools used to do this are:

**Extractor** Which will build the likelihood and run the minimization   
**np_reader** Which is in charge of reading the nuisance parameters and provide them to the extractor   
**rk_ex_model** Which provides a toy model to run tests, while the actual model is been developed.   

These three tools come with unit tests.

# Installation 

# For use

This project has to be installed alongside other `rx` dependencies. It can be done by running:

```bash
pip install rx_extractor
```

or 

```bash
pip install -e .
```

in the directory with the code, after clonning it.

## For development

Use the `rx_setup` project to installing with the rest of the packages:

https://gitlab.cern.ch/r_k/setup#description

# Usage

Below is a description of how the project works:

```python
def test_real():
    rdr          = np_rdr(sys='v65', sta='v81', yld='v24')
    df_byld      = rdr.get_ryields()
    d_nent       = #function to get dictionary with yields from dataframe. {'all' : ([nent_bm_mm, nent_qm_mm], nent_ee)}

    mod          = model(preffix='real', d_nent=d_nent)
    d_mod        = mod.get_model()
    d_dat        = mod.get_data(d_nent=d_rare_yld)

    obj          = ext()
    obj.ck       = ck #Value of CK for toys, e.g. rk * nent_ee / nent_mm
    obj.cov      = var #variance of ck
    obj.data     = d_dat
    obj.model    = d_mod 
    obj.plt_dir  = 'tests/extractor/real'
    result       = obj.get_fit_result()

    log.info(f'Calculating errors')
    result.hesse()
    result.freeze()
    utnr.dump_pickle(result, 'tests/extractor/real/result.pkl')
```
which is taken from:

```
https://gitlab.cern.ch/r_k/rk_extractor/-/blob/master/tests/test_extractor.py?ref_type=heads#L128
```

## Loading of signal yields

This is done with `np_reader` will retrieve the expected yields of rare $B$ decays times the efficiencies, 
calculated from the muon yields in the normalization mode.

The inputs used are the versions of the efficiencies with the corresponding systematic and statistical variations (bootstrapping)
as well as the version of the resonant mode fits.

The nuisance parameters are obtained by reading files in the IHEP cluster. However these parameters can be `cached` with:

```python
def run():
    rdr           = np_rdr(sys='v65', sta='v63', yld='v24')
    d_ryld        = rdr.get_ryields()
```

in JSON files that become part of the project and therefore you need a new release everytime you update that.

## Model building

A class is used to build a toy model from the expected rare decays yield and the rare mode efficiencies. 
This class should be updated to use the correct model when available. 

## Configuration

The configuration is done through `toml` files stored
[here](https://gitlab.cern.ch/r_k/rk_extractor/-/tree/master/src/extractor_data/config)

and they look like:

```toml

#This will do the fits for the whole R1 + R2 dataset for the TOS category.
[input]
datasets=['all_TOS']

[systematics]

fix_var=[]
# Specify signal models to try in toy fit
sig_mod=['sig_ETOS:sys1', 'sig_MTOS:sys1']
# It also can be left empty
sig_mod=[]

# For backgrounds, we will do bootstrapping. This will turn off the bootstrapping:
rpr_mod='rpr_ETOS:bts_1_1'
cpr_mod='cpr_ETOS:bts_1_1'

# This will turn it on for 20 bootstrapped models for each component
rpr_mod='rpr_ETOS:bts_1_20'
cpr_mod='cpr_ETOS:bts_1_20'
```


## Extraction of results

The `extractor` class provides a `zfit` result object, which can be pickled.

# Toy tests

In order to verify that the model is not biased and has the right coverage, a set of scripts are available in

`scripts/jobs`

these are installed as part of the project, but should be ran outside the corresponding virtual environment.

## Software

The code is taken from an LCG view, given that this code will have to run on the GRID eventually.   
The code not available in the view: 

### Local tests

This code will, for now, go to:

```bash
/publicfs/lhcb/user/campoverde/SFT/RK_TOY
```
and will be re-used, to speed up tests. If any version is updated, remove the directory and re-run the local test as shown below.

### Grid

The code will be installed from zero in each grid node.

## Local tests

Before submitting one can test locally by running

```bash
rxe_local -j 001 -n 1 -v v3
```

where `v3` is the version of the TOML file in `src/extractor_data/config` that specifies the setting. The options mean:

```bash
Used to run local tests of toy fits

optional arguments:
  -h, --help            show this help message and exit
  -j JOB_ID, --job_id JOB_ID
                        Index of job
  -n NFITS, --nfits NFITS
                        Number of fits per job
  -v VERS, --vers VERS  Version of output
  -s SNDBX, --sndbx SNDBX
                        Directory for output, optional
  -u {0,1}, --upgrade {0,1}
                        Will upgrade before running
  -d DIRNAME, --dirname DIRNAME
                        Name of directory with code, optional
```

## IHEP tests

For small tests that still require multiple fits but that can be done in the cluster:

```bash
./rxe_ihep_jobs -j 3 -f 1 -v v1
```

where it would send one fit for each of three jobs, using the  `v1` version of the config file.
The full options are:

```
Usage:
Script used to send toy fits to IHEP cluster, for debugging purposes
    -j: Number of jobs
    -f: Number of fits per job
    -v: Version of configuration file
    -m: Memory, default 4000 (MB)
    -q: Queue, default mid
```

## Grid submission
To use them do:

```bash
. /cvmfs/lhcb.cern.ch/lib/LbEnv
#make grid proxy for 100 hours
lhcb-proxy-init -v 100:00
lb-dirac bash

#you might need tqdm installed locally, in case it is not available in your system.
pip install --user tqdm

cd scripts/jobs

./rkex_jobs -n job_name -j J -f F -v config_version -m [local, wms]

#For example
./rxe_grid_jobs -n test_local_001 -j 1 -f 1 -v v3 -m local
```
where:

1. `J` is the number of jobs
1. `F` is the number of fits per jobs
1. `local` or `wms` specify wether the jobs are ran locally (for tests) or in the grid.
1. `v` Version of config file.

these jobs can be monitored in the dirac website as any other job.

__IMPORTANT:__ 

1. Do not send more than 1000 fits per job. Otherwise (given the way `submit.py` is written) random seeds will overlap between jobs.
1. What the job actually does is in `scripts/jobs/rxe_run_toys`. As shown, the project used is already online and will be downloaded before starting
the job.
1. If a new version of the project is available, it has to be added to `pypi` first.
1. The inputs are the _cached_ parameters stored in a tarball, mentioned above. These parameters are to be found in the `v65_v63_v24` directory
created from the ` $EXTDIR/v65_v63_v24.tar.gz` tarball, where for now

```bash
EXTDIR=/publicfs/lhcb/user/campoverde/Data/rx_extractor
```

therefore, the jobs have to be sent from the IHEP cluster or this variable has to be modified.

## Retrieving outputs

1. Start with an environment where DIRAC (and a valid grid certificate) is available.
1. Go to the directory where the outputs (e.g. `sandbox_test_004`) are.
1. Run:

```bash
./rxe_download -n test_004
```

where the argument is the name of the job.

## Plotting

### Systematics

Run:

```bash
rxe_plot_syst -d output_syst_006 -o plots_syst_006
```

to 

1. Read all the `JSON` files in the retrieved sandboxes in the output directory
1. Make a dataframe with the fit parameters.
3. Make plots and send them to the `plots` directory.

## Acceprances for partially reconstructed decays

The partially reconstructed decays have acceptances that have to be calculated without requiring that the extra track be in the LHCb acceptance. 
This is done by:

1. Generate samples with RapidSim
2. Calculate the acceptances

### Sample generation

One has to:

1. In the IHEP cluster or LXPLUS follow [these](https://github.com/gcowan/RapidSim?tab=readme-ov-file#setup) instructions.
2. The input decay files are in [this](src/prec_files) directory.

Then run:

```bash
  $RAPIDSIM_ROOT/bin/RapidSim.exe /publicfs/ucas/user/campoverde/Packages/RapidSim-master/install/user_config/bpk2kpipiee 10000 1
```

1. Run over a small number of events, alongside the decay files will be the config files, created by this run. 
2. Modify the lines below:

```
geometry: LHCb
paramsStable : P, PT
```

to

```
geometry: 4pi
paramsStable : P, PT, eta
```

to add the _eta_ branch, which will be used to calculate $`\theta`$.

3. Generate again with the full statistics, 100K.

### Efficiencies calculation

