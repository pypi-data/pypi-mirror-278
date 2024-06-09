from pyhipp.field.cubic_box import Field, Mesh, DensityField, TidalField, TidalClassifier
import numpy as np


def classifiler_from_particles(
        l_box: float, n_grids: int, positions: np.ndarray, r_sm: float,
        lam_th: float = 0.2):
    
    '''
    @l_box: float, box size.
    @n_grids: int, number of grids per side.
    @positions: np.ndarray, shape=(n, 3), where n is the number of particles.
    @r_sm: float, smoothing scale.
    @lam_th: float, threshold for the tidal field eigenvalues.
    '''
    
    df = DensityField(l_box=l_box, n_grids=n_grids)
    df.add(positions)

    mesh = Mesh.new(n_grids, l_box)
    field = Field.new_by_data(df.data, mesh)
    tf = TidalField(r_sm=r_sm)
    res = tf.run(field)

    clsf = TidalClassifier(res.lam, mesh, lam_th=lam_th)
    
    return clsf
