#!/bin/bash
source /root/miniconda3/etc/profile.d/conda.sh
source ~/.bashrc
cd /home/ubuntu/ComfyUI
conda activate app
python main.py
