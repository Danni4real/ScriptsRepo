#!/bin/bash

cd /home/dan/weekly_report/
python3 -m venv .venv
source .venv/bin/activate
python3 gen_report.py

