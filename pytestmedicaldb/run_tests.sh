#!/bin/bash

python3 -m unittest -v utmedicaldb.py > "/app/logs/unit-test-$(date +%Y-%m-%d-%H%M%S).log" 2>&1
