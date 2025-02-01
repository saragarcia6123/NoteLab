#!/bin/bash

# Check if there is an active venv environment
if [ -n "$VIRTUAL_ENV" ]; then
    read -r -p "There is a venv environment already active. Would you like to deactivate it? (y/n)" choice
    choice="${choice:-y}"
    case "$choice" in
        y|Y ) deactivate;;
        * ) echo "Proceeding with the currently active Virtual Environment.";;
    esac
fi

# Check if there is an active conda environment
if command -v conda &> /dev/null; then
    if conda info --envs | grep -q "\*" ; then
        read -r -p "There is a conda environment already active. Would you like to deactivate it? (y/n): " choice
        choice="${choice:-y}"
        case "$choice" in
            y|Y ) conda deactivate; echo "Conda environment deactivated.";;
            * ) echo "Proceeding with the currently active Conda environment.";;
        esac
    fi
fi