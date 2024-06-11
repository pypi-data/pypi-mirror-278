from sectionproperties.analysis.section import Section
from sectionproperties.pre.geometry import Polygon, Geometry
import json
import moapy.mdreporter

def calc(dictvertices):
    polygon = Polygon(dictvertices)
    geom = Geometry(polygon)
    geom.create_mesh(mesh_sizes=100.0)

    section = Section(geom)
    section.calculate_geometric_properties()
    return section.get_perimeter(), section.get_area(), section.get_c(), section.get_ic()

def mdreport(json_data):
    dict_vertex = json.loads(json_data)
    peri, area, centroid, Ic = calc(dict_vertex["vertices"])
    rpt = moapy.mdreporter.ReportUtil("test.md", "section properties")
    rpt.add_line_fvu("Perimeter", peri, moapy.mdreporter.enUnit.LENGTH)
    rpt.add_line_fvu("Area", area, moapy.mdreporter.enUnit.AREA)
    rpt.add_line_fvu("Cx", centroid[0], moapy.mdreporter.enUnit.LENGTH)
    rpt.add_line_fvu("Cy", centroid[1], moapy.mdreporter.enUnit.LENGTH)
    rpt.add_line_fvu("Ix", Ic[0], moapy.mdreporter.enUnit.INERTIA)
    rpt.add_line_fvu("Iy", Ic[1], moapy.mdreporter.enUnit.INERTIA)
    return rpt.get_md_text()

#json_data = '{"vertices": [[10,10], [300,10], [300,300], [10, 300]]}'
# json_data = '{"vertices": [[0.0, 0.0], [400.0, 0.0], [400.0, 600.0], [0.0, 600.0], [0.0, 0.0]]}'
# md = mdreport(json_data)
# print(md)
