[![UnitTest](https://github.com/ncc-gap/GCATRunner/actions/workflows/UnitTest.yml/badge.svg)](https://github.com/ncc-gap/GCATRunner/actions/workflows/UnitTest.yml)
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

G-CAT Runner
===============
G-CAT Runner is a task runner for [G-CAT Workflow](https://github.com/ncc-gap/GCATWorkflow) and others.

## Setup

1. Install

```
pip install gcat_runner
```

## How to use

1. Bash script

For example, run.sh
```
set -x

echo "success"
```

2. Config file

With YAML format, for example, conf.yml
```
log_dir: .           # log output directory
max_task: 0          # count of array job (default 0)
qsub_option: ''      # qsub/slurm command options (invalid with bash-runner)
retry_count: 1       # number for retry 
runner: bash         # choose in ['qsub', 'drmaa', 'slurm', 'bash']
                     # qsub: task runs with 'qsub -sync'
                     # drmaa: task runs with drmaa library
                     # slurm: task runs with 'sbatch --wait'
                     # qsub: task runs with 'bash'
```

3. Run

```
gcat_runner run.sh conf.yml
```

options:  
  `--interval seconds`: Randomly modify job submission within the specified range of 0 to the specified number of seconds.
