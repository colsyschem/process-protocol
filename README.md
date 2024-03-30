# Protocol for efficient research

```
			A project without a goal is a hobby
			A goal without a project is a dream
							--- Tiago Forte ---
```

## Getting Started

Copy the folder to your hard disk, rename its name by our name and surname, example, marekgrzelczak. this is a unique name that will be used and stored in NAS system.

### Prerequisites

* Python3

### Installing

If you are using python to analyse data and generate plots and figures, you need to make virtual enviroments and install requirement modules:
```
pip install -r requirements.txt
```

## Project structure

The folder tree below shows the distribution and the system for naming files and folders. 

1. Data accquisition. 
Run experiments and colect raw data by placing them in a folder which name starts with date (e.g. 20230620, year-month-day) followed by working title (invent_short_name). Important, use double underscore, __ , to separate date from working_title. This is important when collecting raw data for repository once the paper is submitted.

2.  Data analysis
Copy template script located in 'src' folder and name it with the folder name in 'data' folder. 

3.  Plot generation

4.  Report writing (weekly or biweekly).

5.  Repeat steps 1 to 4.  

```
.
├─data
│ ├─ 20230620__working_title
│ │  ├─ Emission
│ │  ├─ TEM
│ │  └─ UV-Vis-NIR
│ │     └─ Example_UV_Vis_Rods.csv
│ └─ 20230625__working_title
├─doc
│   ├── draft
│   │   ├── Readme
│   │   └── working_title
│   └── reports
│       └── 20230620__working_title.docx
├─ results
│   ├── figs
│   │   └── working_title
│   │       └── final
│   └── plots
│       ├── UVVIS_2by2__20230620__working_title.pdf
│       └── UVVis_all__20230620__working_title.pdf
├─ src
│   ├── misc
│   │   ├── __init__.py
│   │   ├── misc_nano_param.py
│   │   └── misc_process.py
│   ├── 20230620__working_title.ipynb
│	└── figs__working_title.ipynb
├── LICENSE.txt
└── readme.md

```



## Authors contribution (https://casrai.org/credit/)
Marek Grzelczak - *Current contributor, developing new features
Another person - 
## Acknowledgments



* Marek Grzelczak - PI for the project and inventor of the abstraction
