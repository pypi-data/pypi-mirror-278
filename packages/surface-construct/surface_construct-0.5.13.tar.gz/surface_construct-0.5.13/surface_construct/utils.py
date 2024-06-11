from scipy.spatial import ConvexHull


def calc_hull_vertices(v):
    shape = v.shape
    if len(shape) != 2:
        print("Warning: The vector should be 2D, however {}D vector was provided!)".format(len(shape)))
        print("The Convex Hull Vertices won't be calculated.")
        return None
    if shape[1] > 5:
        print("Warning: The vector.shape[1]={} is too large to be calculated!)".format(shape[1]))
        print("The Convex Hull Vertices won't be calculated.")
        return None
    try:
        print("Calculate Convex Hull Vertices ...")
        hull = ConvexHull(v)
        vertices = hull.vertices
        return vertices
    except ValueError:
        return None


def get_calc_info(calc=None):
    if calc is None:
        return {}
    calc_name = calc.name
    calc_para = dict()
    if calc_name in ('vasp',):
        calc_para['xc'] = calc.parameters['xc']
        calc_para['encut'] = calc.parameters['encut']

    calc_info = {
        'name': calc_name,
        'para': calc_para,
    }
    return calc_info

