#!/bin/bash
echo "Setting up the environment..."
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
echo "Setup complete!"
