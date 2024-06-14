import torch
import networkx as nx
from torch_geometric.data import Data
from UDLayer.graphlayer import GraphLayer
from osgeo import osr, gdal
import dgl

def get_coord_type(filedir: str, row: int, col: int):
    """
    Get the type of coordinates from the file directory

    Parameters
    --------------------
        filedir (str): The file directory of the coordinates
    
    Returns
    --------------------
        coord_type (tuple): The coordinate of the position of the row and column. To get the type of the coordinate, run `get_coord_type(filedir, 0, 0)` to get the coordinate of the top left corner.
        If the tuple is (latitute, longitude), then the parameter "coord_type" is "latlon". Otherwise, the parameter "coord_type" is "lonlat".
    """

    if not isinstance(filedir, str):
        raise TypeError("Input must be string.")

    # get the existing coordinate system
    ds = gdal.Open(filedir)
    old_cs = osr.SpatialReference()
    old_cs.ImportFromWkt(ds.GetProjectionRef())

    # create the new coordinate system
    wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs.ImportFromWkt(wgs84_wkt)

    # create a transform object to convert between coordinate systems
    transform = osr.CoordinateTransformation(old_cs, new_cs)

    # get the point to transform, pixel (0,0) in this case
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()

    data = ds.ReadAsArray()

    y = gt[3] + row * gt[5] + col * gt[4]
    x = gt[0] + col * gt[1] + row * gt[2]
    coord = transform.TransformPoint(x, y)
    return coord


def graph_to_nx(graph: GraphLayer):
    """
    Convert a graph to a networkx graph

    Parameters
    --------------------:
        graph (Graphlayer): The Graphlayer to be transformed
    """

    if not isinstance(graph, GraphLayer):
        raise TypeError("Input must be GraphLayer.")

    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(graph.data.nodes)
    nx_graph.add_edges_from(graph.data.edges)
    return nx_graph


def graph_to_torch(graph: GraphLayer):
    """
    Convert a graph to a torch_geometric graph

    Parameters
    --------------------:
        graph (Graphlayer): The Graphlayer to be transformed
    """

    if not isinstance(graph, GraphLayer):
        raise TypeError("Input must be GraphLayer.")

    x, edge_index = [], []
    for node in graph.data.nodes:
        if len(node[1]) > 2:
            x.append([node[1]["lat"], node[1]["lon"], node[1][graph.name]])
        else:
            x.append([node[1]["lat"], node[1]["lon"]])
    for edge in graph.data.edges:
        edge_index.append([edge[0], edge[1]])
        edge_index.append([edge[1], edge[0]])
    pyg = Data(x=x, edge_index=edge_index.t().contiguous(), y=torch.zeros(len(x), 1))
    return pyg


def graph_to_dgl(graph: GraphLayer):
    """
    Convert a graph to a dgl graph

    Parameters
    --------------------:
        graph (Graphlayer): The Graphlayer to be transformed
    """

    if not isinstance(graph, GraphLayer):
        raise TypeError("Input must be GraphLayer.")
    
    source , target = [] , []
    for edge in graph.data.edges:
        source.append(edge[0])
        target.append(edge[1])
    source , target = torch.tensor(source) , torch.tensor(target)
    g = dgl.graph(source,target)
    if graph.directed==False:
        g = dgl.to_bidirected(g)

    return g
