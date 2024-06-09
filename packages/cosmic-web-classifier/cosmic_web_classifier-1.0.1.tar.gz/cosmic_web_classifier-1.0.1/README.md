# CosmicWebClassifier - A Python package for classifying cosmic web structures

[![Last commit](https://img.shields.io/github/last-commit/ChenYangyao/cosmic-web-classifier/master)](https://github.com/ChenYangyao/cosmic-web-classifier/commits/master)
[![Workflow Status](https://img.shields.io/github/actions/workflow/status/ChenYangyao/cosmic-web-classifier/run-test.yml)](https://github.com/ChenYangyao/cosmic-web-classifier/actions/workflows/run-test.yml)
[![MIT License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/ChenYangyao/cosmic-web-classifier/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/cosmic-web-classifier)](https://pypi.org/project/cosmic-web-classifier/)

The package provides a set of tools to compute the density and tidal field from a sample of particles (usually obtained by N-body/hydrodynamical simulations), and classify the cosmic web structures into knots, filaments, sheets and voids based on the fields.

To install, run:
```bash
pip install cosmic-web-classifier
```
Alternatively, you can clone the repository and install the package locally via `pip install -e /path/to/the/repo`.


## Usage 

See the Jupyter notebooks under `docs/`.
- `cosmic_web_types.ipynb`: demonstrates how to generate a sample of dark matter particles from a particle-mesh code, and perform the classification based on the particle distribution.

## Example images

<div align="center">
    <div align="middle">
        <img width="33%" src="https://raw.githubusercontent.com/ChenYangyao/cosmic-web-classifier/master/docs/figures/density.jpeg"/>
        <img width="33%" src="https://raw.githubusercontent.com/ChenYangyao/cosmic-web-classifier/master/docs/figures/voids.jpeg"/>
    </div>
    <div width="80%">Left: The evaluated density field. Right: The regions classified as voids (shown in white).</div>
</div>


## Contributors

- Yangyao Chen (USTC, [yangyaochen.astro@foxmail.com](mailto:yangyaochen.astro@foxmail.com)).

## Citation

If you use this package in your research, please cite the following papers:
- Huiyuan Wang et al. 2016, ApJ 831, 164 ([https://arxiv.org/abs/1608.01763](https://arxiv.org/abs/1608.01763))
- Yangyao Chen et al. 2020, ApJ, 899, 81 ([https://arxiv.org/abs/2003.05137](https://arxiv.org/abs/2003.05137))