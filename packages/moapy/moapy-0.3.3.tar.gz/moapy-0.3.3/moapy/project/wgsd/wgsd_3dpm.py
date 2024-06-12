from scipy.spatial import ConvexHull
from shapely import Polygon

from sectionproperties.pre.library.concrete_sections import add_bar
from concreteproperties.concrete_section import ConcreteSection
from concreteproperties.material import Concrete, SteelBar

import sectionproperties.pre.geometry as geometry
import sectionproperties.pre.pre as pre
import concreteproperties.stress_strain_profile as ssp
import concreteproperties.utils as utils
import concreteproperties.results
import numpy as np
import trimesh
import json

input = {
    "name": "Example1",
    "material": {
        "concrete": {
            "name": "C30",
            "curve": {
                "uls": {
                    "HEAD": ["Strain", "Stress"],
                    "DATA": [[0.0, 0.0006, 0.0006, 0.003], [0.0, 0.0, 34.0, 34.0]]
                },
                "sls": {
                    "HEAD": ["Strain", "Stress"],
                    "DATA": [[0.0, 0.001], [0, 32.8,]]
                }
            }
        },
        "rebar": {
            "code": "KS(RC)",
            "name": "SD500",
            "fy": "auto",
            "curve": {
                "uls": {
                    "HEAD": ["Strain", "Stress"],
                    "DATA": [[0.0, 0.0025, 0.05], [0, 500.0, 500.0]]
                },
                "sls": {
                    "HEAD": ["Strain", "Stress"],
                    "DATA": [[0.0, 0.0025, 0.05], [0, 500.0, 500.0]]
                }
            }
        },
    },
    "geometry" : {
        "concrete": {
            "outerpolygon": {
                "HEAD": ["x", "y"],
                "DATA": [[0.0, 400.0, 400.0, 0.0], [0.0, 0.0, 600.0, 600.0]]},
            "material": "C30"
        },
        "rebar": {
            "HEAD": ["x", "y", "diameter", "area", "material"],
            "DATA": [[40.0, 40.0, 20.0, 287.0, "SD500"], [360.0, 40.0, 20.0, 287.0, "SD500"], [360.0, 560.0, 20.0, 287.0, "SD500"], [4.0, 560.0, 20.0, 287.0, "SD500"]]
        },
    },
    "lcom": {
        "HEAD": ["name", "Fx", "My", "Mz"],
        "DATA": [["LCOM1", 1000000000.0, 0.0, 8000000.0], ["LCOM2", 1000000000.0, 8000000.0, 8000000.0]]
    },
    "dgncode": "ACI318M-19",
    "option": {
        "by_ecc_pu": "ecc"
    }
}


class PM3DCurve:
    def __init__(self, data):
        self.name = data.get("name")

        self.material = data.get("material")
        self.concrete_material = self.material.get("concrete", {})
        self.rebar_material = self.material.get("rebar", {})

        self.geometry = data.get("geometry", {})
        self.concrete_geom = self.geometry.get("concrete", {})
        self.rebar_geom = self.geometry.get("rebar", {})

        self.lcom = data.get("lcom", {})

        self.dgncode = data.get("dgncode")
        self.dgncode_params = data.get("dgncode_params", {})
        self.option = data.get("option", {})

    def get_concrete_material_curve(self, type_):
        curve_data = self.concrete_material.get("curve", {}).get(type_, {})
        head = curve_data.get("HEAD", [])
        data = curve_data.get("DATA", [])
        if head and data:
            strain = data[0]
            stress = data[1]
            return {"Strain": strain, "Stress": stress}
        return {}

    def get_concrete_geom(self):
        return self.concrete_geom

    def get_rebar_geom(self):
        return self.rebar_geom

    def get_lcom_data(self):
        return self.lcom.get("DATA", [])

    def get_dgncode_param(self, param):
        return self.dgncode_params.get(param)

    def get_option(self, option):
        return self.option.get(option)

    def compound_section(
        self,
        concrete: list[dict],
        all_bar: list[dict],
        conc_mat: pre.Material = pre.DEFAULT_MATERIAL,
        steel_mat: pre.Material = pre.DEFAULT_MATERIAL,
    ) -> geometry.CompoundGeometry:
        conc_polygon = concrete.get("outerpolygon", {})
        coords = conc_polygon.get("DATA", [])

        def convert_data(data):
            x_coords = data[0]
            y_coords = data[1]

            if len(x_coords) != len(y_coords):
                raise ValueError("The length of x and y coordinates must be the same.")

            # Create tuples of (x, y)
            result = [(x_coords[i], y_coords[i]) for i in range(len(x_coords))]

            return result

        polygon = Polygon(convert_data(coords))
        concrete_geometry = geometry.Geometry(geom=polygon, material=conc_mat)

        for bar in all_bar["DATA"]:
            concrete_geometry = add_bar(
                geometry=concrete_geometry,
                area=bar[3],
                material=steel_mat,
                x=bar[0],
                y=bar[1],
                n=4
            )

        if isinstance(concrete_geometry, geometry.CompoundGeometry):
            return concrete_geometry
        else:
            raise ValueError("Concrete section generation failed.")

    def get_Cb(self, sect, theta_rad, ecu, esu):
        d_ext, _ = sect.extreme_bar(theta=theta_rad)
        return (ecu / (ecu + esu)) * d_ext

    def make_3dpm_data(self):
        beta1 = 0.8
        ecu = 0.003
        esu = 0.05
        fck = 30.0
        ss_conc_ser = ssp.ConcreteServiceProfile(self.get_concrete_material_curve("sls")["Strain"], self.get_concrete_material_curve("sls")["Stress"], ecu)
        ss_conc_uls = ssp.ConcreteUltimateProfile(self.get_concrete_material_curve("uls")["Strain"], self.get_concrete_material_curve("uls")["Stress"], fck)

        # ss_rebar_uls = ssp.StressStrainProfile(self.rebar_material["curve"]["uls"]["Strain"], self.rebar_material["curve"]["uls"]["Stress"])
        # ss_rebar_sls = ssp.StressStrainProfile(self.rebar_material["curve"]["sls"]["Strain"], self.rebar_material["curve"]["sls"]["Stress"])

        concrete_matl = Concrete(
            name=self.concrete_material['name'],
            density=2.4e-6,
            stress_strain_profile=ss_conc_ser,
            ultimate_stress_strain_profile=ss_conc_uls,
            flexural_tensile_strength=0.6 * np.sqrt(40),
            colour="lightgrey",
        )

        steel_matl = SteelBar(
            name=self.rebar_material['name'],
            density=7.85e-6,
            stress_strain_profile=ssp.SteelElasticPlastic(
                yield_strength=500,
                elastic_modulus=200e3,
                fracture_strain=esu,
            ),
            colour="grey",
        )

        # reference geometry
        compound_sect = self.compound_section(self.get_concrete_geom(), self.get_rebar_geom(), concrete_matl, steel_matl)
        ref_sec = ConcreteSection(compound_sect)
        results = []
        theta_range = np.arange(0.0, 361.0, 15.0).tolist()

        for theta in theta_range:
            theta_rad = np.radians(theta)
            x11_max, x11_min, y22_max, y22_min = utils.calculate_local_extents( 
                geometry=ref_sec.compound_geometry,
                cx=ref_sec.gross_properties.cx,
                cy=ref_sec.gross_properties.cy,
                theta=theta_rad
            )

            C_Max = abs(y22_max - y22_min) / beta1
            d_n_range = np.linspace(0.0001, C_Max * 1.01, 10).tolist()  # numpy 배열을 float 리스트로 변환

            Cb = self.get_Cb(ref_sec, theta_rad, ecu, esu)
            d_n_range.append(Cb)

            for d_n in d_n_range:
                res = concreteproperties.results.UltimateBendingResults(theta_rad)
                res = ref_sec.calculate_ultimate_section_actions(d_n, res)
                results.append(res)

        return results

def Do(json_data):
    dict_data = json.loads(json_data)
    data = PM3DCurve(dict_data)
    results = data.make_3dpm_data()

    d_n_values = [result.n for result in results]
    m_x_values = [result.m_x for result in results]
    m_y_values = [result.m_y for result in results]

    points = np.column_stack((m_x_values, m_y_values, d_n_values))
    hull = ConvexHull(points)
    mesh1 = trimesh.Trimesh(vertices=hull.points, faces=hull.simplices)
    ray = trimesh.ray.ray_pyembree.RayMeshIntersector(mesh1)

    lcoms = data.get_lcom_data()

    result_lcom = []
    for lcom in lcoms:
        lcom_name = lcom[0]
        lcom_point = [lcom[1], lcom[2], lcom[3]]

        if data.get_option("by_ecc_pu") == "ecc":
            origin = np.array([0, 0, 0])
        else:
            origin = np.array([0, 0, lcom_point[2]])

        direction = lcom_point - origin
        direction = direction / np.linalg.norm(direction)

        locations, index_ray, index_tri = ray.intersects_location(
            ray_origins=np.array([origin]),
            ray_directions=np.array([direction])
        )

        result_lcom.append([lcom_name, locations[0, 2], locations[0, 0], locations[0, 1]])

    hull_points_list = hull.points.tolist() if isinstance(hull.points, np.ndarray) else hull.points
    res = {
        "3DPM": {
            "HEAD": ["Mx", "My", "P"],
            "DATA": hull_points_list
        },
        "norminal_strength": {
            "HEAD": ["Name", "Mny", "Mnz", "Pn"],
            "DATA": result_lcom
        }
    }

    return json.dumps(res)


# res = Do(json.dumps(input))
# print(res)