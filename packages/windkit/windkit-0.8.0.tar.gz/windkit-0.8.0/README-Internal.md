# WindKit

This project provides common xarray data structures for several wind energy related data formats, as well as plotting and spatial manipulation routines.

## Downstream projects:

- [daTap](https://gitlab-internal.windenergy.dtu.dk/ram/software/tech-team/web-apps/daTap)
- [PyWAsP](https://gitlab-internal.windenergy.dtu.dk/ram/software/pywasp/pywasp)
- [PyWAsP Swarm](https://gitlab-internal.windenergy.dtu.dk/ram/software/pywasp/pywasp-swarm)
- [WindSider Validation](https://gitlab.windenergy.dtu.dk/windsider)

## Developer documentation

[Developer documentation](https://ram.pages-internal.windenergy.dtu.dk/software/pywasp/pywasp-developer-docs/) is maintained in the [Pywasp Developer Docs repository](https://gitlab-internal.windenergy.dtu.dk/ram/software/pywasp/pywasp-developer-docs) using mkdocs.

### Use of lock files

`conda-lock --mamba -f dev_env.yaml -p linux-64 -p osx-64 -p win-64`
`mamba create -n pywasp_env --file conda-lock_linux-64.lock`

## Build and deploy new version

Make sure `CHANGELOG.md` is updated with all changes since last release, and add the correct version.

```sh
export SETUPTOOLS_SCM_PRETEND_VERSION=<version>
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=<global-token> # global token can be found in bitwarden under pypi, username wasp

# Create build environment
mamba create -n build boa build python=3.9 twine setuptools_scm conda-verify
conda activate build

# install the package such that the above version code (in SETUPTOOLS_SCM_PRETEND_VERSION) will be written to the dist package that is uplaoded to pypi
pip install -e .

# Build & deploy Pypi
rm -r dist
python -m build
python3 -m twine upload dist/*

# Build & deploy conda
# This cannot be done from a submodule folder, windkit must be cloned in a different folder.
rm -r conda_build
export VERSION=<version>
time conda mambabuild -c https://conda.windenergy.dtu.dk/channel/open --output-folder conda_build  ./recipe

rsync -auPv conda_build/ VIND-pWASPint01:~/.
ssh VIND-pWASPint01
  sudo rsync --ignore-existing -tprm --include=*/ --include=*.tar.bz2 --exclude=* conda_build/ /mnt/data/external/rw/conda-channel/basic_auth_node_server/conda/open/
  sudo chown -R 1000:1000 /mnt/data/external/rw/conda-channel/basic_auth_node_server/conda/
  # To check whether it worked correctly, go to  https://conda.windenergy.dtu.dk/channel/open/noarch/
```

### Build and deploy docs

Make sure you have an environment with all sphinx related dependencies.


```sh
cd docs
make clean
make html
# Copy to the machine
rsync -auPv --delete build/html VIND-pWASPint01:/mnt/data/external/ro/web_documentation/windkit
```
