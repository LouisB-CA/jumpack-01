
# Requirements

## Create a requirements list
* After establishing a virtual environment, do this
```bash
source .venv/bin/activate
echo "" >> docs/requirements.txt
date >> docs/requirements.txt
pip freeze >> docs/requirements.txt
```


## Restore a venv using the requirements list
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

