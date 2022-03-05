#!/bin/bash

export FLASK_APP=main.py

flask db upgrade

python main.py