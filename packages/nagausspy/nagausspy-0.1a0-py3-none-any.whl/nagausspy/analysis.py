import numpy as np
import networkx

def clasify_geometries(geometries, align_index,
                       reference_indexes, tolerance=1):
    """
    Filters the input geometries to group the identical ones.

    Note
    ----
    All the geometries must correspond to the same system and with the
    atoms in the same order

    Parameters
    ----------
    geometries : dict(label: nagausspy.GaussianGeometry)
        Dictionary with the geometries to clasify and a label to
        identify them. They key of the dictionary is the label and the
        values are the geometries.

    align_index : list(int)
        List with 3 indexes of the atoms that will be used to align
        the different geometries. The atoms should be chosen such that
        they are in the same relative position in the different
        geometries. Moreover they can't be 3 atoms in the same line.

    reference_indexes : list(int)
        List with the indexes of the atoms than will be used to
        identify the structures

    tolerance : float
        Max displacement of each one of the reference atoms in angstroms.

    Returns
    -------
    result : dict(structure: list(label)) - optional
        Dictionary with the diferent structures and which labels faell
        in that category. Default 1.

    """

    connection = np.zeros((len(geometries), len(geometries)))

    labels, geoms = list(zip(*geometries.items()))

    for index1, geom1 in enumerate(geoms):
        for index2, geom2 in enumerate(geoms):
            if index1 >= index2:
                continue
            if check_geometry_equivalence(geom1, geom2, align_index,
                                          reference_indexes,
                                          tolerance=tolerance):
                connection[index1, index2] = 1
                connection[index2, index1] = 1

    graph = networkx.from_numpy_array(connection)
    clusters = networkx.connected_components(graph)
    out = {}
    for index, geoindexes in enumerate(clusters):
        out[index] = []
        for geoindex in geoindexes:
            out[index].append(labels[geoindex])
    return out

def check_geometry_equivalence(geometry1, geometry2, align_index,
                               reference_indexes, tolerance=0.8):
    """
    geometry1, geometry2 : nagausspy.GaussianGeometry
        The 2 geometries to compare.
    align_index : list(int)
        List with 3 indexes of the atoms that will be used to align
        the different geometries. The atoms should be chosen such that
        they are in the same relative position in the different
        geometries. Moreover they can't be 3 atoms in the same line.

    reference_indexes : list(int)
        List with the indexes of the atoms than will be used to
        identify the structures

    tolerance : float
        Max displacement of each one of the reference atoms in angstroms.

    Returns
    -------
    result : bool
        Wether the 2 geometries are equivalent or not
    """

    geometry2.align_with(align_index,
                         geometry1.coordinates[align_index])

    delta = (geometry2.coordinates[reference_indexes]
             - geometry1.coordinates[reference_indexes])

    return np.all(np.linalg.norm(delta, axis=1) < tolerance)
