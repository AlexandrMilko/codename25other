#!/bin/bash
source /root/miniconda3/etc/profile.d/conda.sh
source ~/.bashrc
cd /home/app/codename25
conda activate app
source env.sh
cd src
python run.py
