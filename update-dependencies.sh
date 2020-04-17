#!/usr/bin/env bash

pip install --upgrade pip pip-tools setuptools wheel
pip-compile --upgrade
pip-sync
