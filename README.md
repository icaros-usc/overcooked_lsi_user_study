# Overcooked-LSI User Study

This repository contains the data of all 27 subjects of the user study of the paper:
"On the importance of environments in Human-Robot Coordination". Matthew Fontaine*, Ya-Chuan Hsu*, Yulun Zhang*, Bryon Tjanaka and Stefanos Nikolaidis. RSS 2021.


You can view the data and replay the collaborated human-robot game play here.

## The user study data.

The data of the user study are under the `user_study/results` directory. There are 27 directories in total, each containing the data of one subject. The data of each subject is in its corresponding `<subject_ID>/human_log_refined.csv` file.

## Replay the human-robot traces.

### Install Overcooked-AI

It is useful to set up a conda environment with Python 3.7 using
[Anaconda](https://www.anaconda.com/products/individual):

```
conda create -n overcooked_lsi_user_study python=3.7
conda activate overcooked_lsi_user_study
```

To complete the installation after cloning the repo, run the following commands:

```
cd overcooked_lsi_user_study
pip install -e .
```

### Run the replay

Use the following command to run the replay:

```
python replay_user_study.py -l <subject_ID> -type <lvl_type>
```

`<subject_ID>` is the directory name (note: not the full path) of the subject and `<lvl_type>` is the type of the corresponding level that you want to replay. `<lvl_type>` must be one of the following:
```
even_workloads-0
even_workloads-1
even_workloads-2
uneven_workloads-0
uneven_workloads-1
uneven_workloads-2
high_team_fluency-0
high_team_fluency-1
high_team_fluency-2
low_team_fluency-0
low_team_fluency-1
low_team_fluency-2
```
For example, if you want to replay the trace of the subject `1` playing the level `even_workloads-0`, use the following command:

```
python replay_user_study.py -l 1 -type even_workloads-0
```
