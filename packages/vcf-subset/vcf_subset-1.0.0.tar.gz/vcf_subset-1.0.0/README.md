# vcf_subset
Efficient VCF subsetting by genome position. Written in C++, but provided as a python module to save ~3 minutes per TB GVCF

## Install
```
pip install vcf_subset
```

## Local (dev) install
```
# Optional virtual environment
python -m virtualenv env
source env/bin/activate

# Install requirements
pip install build

# Build dist
python -m build --sdist --outdir dist

# Install
pip install .
```
