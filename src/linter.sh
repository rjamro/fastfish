#!/usr/bin/env sh

echo "isort..."
isort . --overwrite-in-place

echo "flake8..."
flake8 --config setup.cfg .
