# PyROOT Example on CMS' NanoAOD

Simple example on how to access CMS' NanoAOD files and read some information from it.

**Note:** Assuming (1) CMSSW environment is available, (2) the user have GRID certificate (3) registered to CMS' VO.

**More info:**
- https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookStartingGrid
- https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideLcgAccess

![pyroot_example_nanoaod](https://github.com/ftorresd/pyroot_example_nanoaod/raw/main/content/pyroot_example_nanoaod.gif)

## Download or clone (HTTPS) or clone (SSH)

``` 
wget https://github.com/ftorresd/pyroot_example_nanoaod/archive/refs/heads/main.zip
unzip main.zip
cd pyroot_example_nanoaod-main
```
or 

```
git clone https://github.com/ftorresd/pyroot_example_nanoaod.git
```

or 

```
git clone git@github.com:ftorresd/pyroot_example_nanoaod.git
```

## Setup

Only once per session.

```
source setup_env.sh
```

## Run 

```
python analyser.py
```

## Output

Histograms will be saved at `output_file.root`.
