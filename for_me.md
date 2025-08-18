pip install pdm
pdm init
pdm add requests
pdm add --dev pytest
pdm remove requests
pdm run python script.py
pdm venv activate