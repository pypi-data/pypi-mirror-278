import numpy as np
from cosmic_web_classifier import classifiler_from_particles
from pyhipp.stats import Rng


def test_get_classifier():

    rng = Rng(10086)
    ptcls = rng.uniform(0.0, 500.0, (128**3, 3))

    classifiler_from_particles(l_box=500.0, n_grids=128, positions=ptcls,
                               r_sm=10.0, lam_th=0.2)
