# Filter hepmc files
```
pip install pyhepmc
python filter.py
```

# Visualise event history
### for ubuntu
```
sudo apt-get install graphviz
# pip install --upgrade pyhepmc
pip install graphviz # Python Package (optional, for integration)
python visualize_nohad_align.py
```

- `visualize.py`: Visualise full event history
- `visualize_align.py`: Same as `visualize.py` but algin final state particles
- `visualize_nohad.py`: Visualise event history before hadronisation
- `visualize.nohad_align.py`: Same as `visualize_nohad.py` but align final state hadrons
