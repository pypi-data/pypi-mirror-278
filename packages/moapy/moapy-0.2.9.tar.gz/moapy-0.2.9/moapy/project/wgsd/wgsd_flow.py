from dataclasses import dataclass, asdict, field as dataclass_field
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
import pandas as pd

# ==== Unit & Design Code ====

@dataclass
class gsdUnit:
    """
    GSD global unit class
    """
    force: str = dataclass_field(
        default="kN", metadata={"description": "Force unit"})
    length: str = dataclass_field(
        default="m", metadata={"description": "Length unit"})
    section_dimension: str = dataclass_field(
        default="mm", metadata={"description": "Section dimension unit"})
    pressure: str = dataclass_field(
        default="MPa", metadata={"description": "Pressure unit"})
    strain: str = dataclass_field(
        default="%", metadata={"description": "Strain unit"})

@dataclass
class gsdDesignCode:
    design_code: str = dataclass_field(default="ACI 318-19")
    sub_code: str = dataclass_field(default="SI")
    

# ==== Stress Strain Curve ====

@dataclass
class stress_strain_curve:
    """
    Stress strain curve class
    {
        "HEAD": ["Strain", "Stress"],
        "DATA": [[0.1, 2, 4, 4, 35], [0, 234235, 235, 235, 0]],
    }
    """
    HEAD: list[str, 2]
    DATA: list[list[float, 2]]


# ==== Concrete Material ====

@dataclass
class gsdConcreteGrade:
    """
    GSD concrete class
    """
    design_code: str = dataclass_field(
        default="ACI318M-19", metadata={"description": "Design code"})
    grade: str = dataclass_field(
        default="C12", metadata={"description": "Grade of the concrete"})

@dataclass
class concrete_general_properties:
    """
    GSD concrete general properties for calculation
    """
    strength: int = dataclass_field(
        default=12, metadata={"description": "Grade of the concrete"})
    elastic_modulus: float = dataclass_field(
        default=30000, metadata={"description": "Elastic modulus of the concrete"})
    density: float = dataclass_field(
        default=2400, metadata={"description": "Density of the concrete"})
    thermal_expansion_coefficient: float = dataclass_field(
        default=0.00001, metadata={"description": "Thermal expansion coefficient of the concrete"})
    poisson_ratio: float = dataclass_field(
        default=0.2, metadata={"description": "Poisson ratio of the concrete"})


@dataclass
class concrete_stress_uls_options_ACI:
    """
    GSD concrete stress options for ULS
    """
    material_model: str = dataclass_field(
        default="Rectangle", metadata={"description": "Material model for ULS"})
    factor_b1: float = dataclass_field(
        default=0.85, metadata={"description": "Plastic strain limit for ULS"})
    compressive_failure_strain: float = dataclass_field(
        default=0.003, metadata={"description": "Failure strain limit for ULS"})
    # read only data 가 있음, API 로는 출력 해줘야함


@dataclass
class concrete_stress_uls_options_Eurocode:
    """
    GSD concrete stress options for ULS
    """
    material_model: str = dataclass_field(
        default="Rectangle", metadata={"description": "Material model for ULS"})
    partial_factor_case: str = dataclass_field(
        default="1", metadata={"description": "Partial factor case for ULS"})
    partial_factor: float = dataclass_field(
        default=1.5, metadata={"description": "Partial factor for ULS"})
    compressive_failure_strain: float = dataclass_field(
        default=0.003, metadata={"description": "Failure strain limit for ULS"})


@dataclass
class concrete_sls_options:
    """
    GSD concrete stress options for SLS
    """
    material_model: str = dataclass_field(
        default="Linear", metadata={"description": "Material model for SLS"})
    plastic_strain_limit: float = dataclass_field(
        default=0.002, metadata={"description": "Plastic strain limit for SLS"})
    failure_compression_limit: float = dataclass_field(
        default=0.003, metadata={"description": "Failure compression limit for SLS"})
    material_model_tension: str = dataclass_field(
        default="interpolated", metadata={"description": "Material model for SLS tension"})
    failure_tension_limit: float = dataclass_field(
        default=0.003, metadata={"description": "Failure tension limit for SLS"})

# ==== Rebar Materials ====
@dataclass
class gsdRebarGrade:
    """
    GSD rebar grade class
    """
    design_code: str = dataclass_field(
        default="ACI318M-19", metadata={"description": "Design code"})
    grade: str = dataclass_field(
        default="Grade 420", metadata={"description": "Grade of the rebar"})

class gsdRebarProp:
    """
    GSD rebar prop
    """
    area: float = dataclass_field(
        default=287.0, metadata={"description": "Area of the rebar"})
    material: gsdRebarGrade = dataclass_field(
        default_factory=gsdRebarGrade, metadata={"description": "Material of the rebar"})
    
    
@dataclass
class rebar_general_properties:
    """
    GSD rebar general properties for calculation
    """
    strength: int = dataclass_field(
        default=420, metadata={"description": "Grade of the rebar"})
    elastic_modulus: float = dataclass_field(
        default=200000, metadata={"description": "Elastic modulus of the rebar"})
    density: float = dataclass_field(
        default=7850, metadata={"description": "Density of the rebar"})
    thermal_expansion_coefficient: float = dataclass_field(
        default=0.00001, metadata={"description": "Thermal expansion coefficient of the rebar"})
    poisson_ratio: float = dataclass_field(
        default=0.3, metadata={"description": "Poisson ratio of the rebar"})

@dataclass
class rebar_stress_uls_options_ACI:
    """
    GSD rebar stress options for ULS
    """
    material_model: str = dataclass_field(
        default="Elastic-Plastic", metadata={"description": "Material model for ULS"})
    failure_strain: float = dataclass_field(default=0.7, metadata={"description": "Failure strain limit for ULS"})


@dataclass
class rebar_stress_sls_options:
    """
    GSD rebar stress options for SLS
    """
    material_model: str = dataclass_field(
        default="Elastic-Plastic", metadata={"description": "Material model for SLS"})
    failure_strain: float = dataclass_field(default=0.7, metadata={"default" : 0.7, "description": "Failure strain limit for SLS"})


@dataclass
class gsdMaterialRebar:
    """
    GSD rebar class
    """
    code: str = dataclass_field(
        default="ASTM A615", metadata={
            "description": "Rebar code"})
    grade: str = dataclass_field(
        default="60", metadata={
            "description": "Grade of the rebar"})
    fy: float = dataclass_field(
        default=420, metadata={
            "description": "Yield strength of the rebar"})
    curve_uls: stress_strain_curve = dataclass_field(
        default_factory=stress_strain_curve, metadata={"description": "Stress strain curve"})
    curve_sls: stress_strain_curve = dataclass_field(
        default_factory=stress_strain_curve, metadata={"description": "Stress strain curve"})


@dataclass
class gsdMaterialTendon:
    """
    GSD tendon class
    """
    code: str = dataclass_field(
        default="ASTM A416", metadata={"description": "Tendon code"})
    curve_uls: stress_strain_curve = dataclass_field(
        default_factory=stress_strain_curve, metadata={"description": "Stress strain curve"})
    curve_sls: stress_strain_curve = dataclass_field(
        default_factory=stress_strain_curve, metadata={"description": "Stress strain curve"})


@dataclass
class gsdMaterialConcrete:
    """
    GSD material for Concrete class
    """
    grade: gsdConcreteGrade = dataclass_field(
        default_factory=gsdConcreteGrade, metadata={"description": "Grade of the concrete"})
    curve_uls: stress_strain_curve = dataclass_field(
        default_factory=stress_strain_curve, metadata={"description": "Stress strain curve"})
    curve_sls: stress_strain_curve = dataclass_field(
        default_factory=stress_strain_curve, metadata={"description": "Stress strain curve"})


@dataclass
class gsdMaterial:
    """
    GSD concrete class
    """
    concrete: gsdMaterialConcrete = dataclass_field(
        default=None, metadata={"description": "Concrete properties"})
    rebar: gsdMaterialRebar = dataclass_field(
        default=None, metadata={"description": "Rebar properties"})
    tendon: gsdMaterialTendon = dataclass_field(
        default=None, metadata={"description": "Tendon properties"})

@dataclass
class gsdMaterialBind:
    """
    GSD material bind class
    """
    uls: gsdMaterial = dataclass_field(
        default=None, metadata={"description": "Material for ULS"})
    sls: gsdMaterial = dataclass_field(
        default=None, metadata={"description": "Material for SLS"})

# ==== Geometry ====

@dataclass
class gsdPoint:
    """
    GSD polygon class
    "HEAD": ["x", "y"],
    "DATA": [[0.0, 400.0, 400.0, 0.0], [0.0, 0.0, 600.0, 600.0]],
    """
    HEAD: list[str, 2] = dataclass_field(
        default=None, metadata={"description": "Head of the polygon"})
    DATA: list[list[float, 2]] = dataclass_field(
        default=None, metadata={"description": "Data of the polygon"})


class gsdConcreteGeometry:
    """
    GSD concrete geometry class
    """
    outerPolygon: gsdPoint = dataclass_field(
        default=None, metadata={"description": "Outer polygon of the concrete"})
    innerPolygon: gsdPoint = dataclass_field(
        default=None, metadata={"description": "Inner polygon of the concrete"})
    material: gsdConcreteGrade = dataclass_field(
        default=None, metadata={"description": "Material of the concrete"})


class gsdRebarGeometry:
    """
    GSD rebar geometry class
    """
    position: gsdPoint = dataclass_field(
        default=None, metadata={"description": "position of the rebar"})
    prop: gsdRebarProp = dataclass_field(
        default=None, metadata={"description": "properties of the rebar"})

@dataclass
class gsdGeometry:
    """
    GSD geometry class
    """
    concrete: gsdConcreteGeometry = dataclass_field(
        default=None, metadata={"description": "Concrete geometry"})
    rebar: list[gsdRebarGeometry] = dataclass_field(
        default=None, metadata={"description": "Rebar geometry"})

# ==== Load ====

@dataclass
class loadcomb:
    """
    GSD load comb class
    "HEAD": ["Name", "Fx", "My", "Mz", "Desc"],
    "DATA": [["1", 100, 10, 10, "D"], ["2", 200, 10, 20, "D+L"]],
    """
    HEAD: list[str, 2] = dataclass_field(
        default=None, metadata={"description": "Head of the lcom"})
    DATA: list[list[float, 2]] = dataclass_field(
        default=None, metadata={"description": "Data of the lcom"})

@dataclass
class gsdLcbBind:
    """
    GSD load combination class
    """
    uls: loadcomb = dataclass_field(
        default=None, metadata={"description": "uls load combination"})
    sls: loadcomb = dataclass_field(
        default=None, metadata={"description": "sls load combination"})

# ==== options ====

class gsdOptions:
    """
    GSD options class
    """
    by_ecc_pu: str = dataclass_field(
        default="ecc", metadata={"description": "ecc or P-U"})


# ==== functions ====

def conc_properties_design(
    units: gsdUnit,
    design_code: gsdDesignCode,
    grade: str,
    general: concrete_general_properties = None,
    uls: concrete_stress_uls_options_ACI = None,
    sls: concrete_sls_options = None
) -> dict[str, stress_strain_curve]:
    """
    Return the concrete material properties based on the design code

    Args:
        units: units
        design_code: design code
        grade: grade of the concrete
        general: general concrete properties
        uls: concrete stress options for ULS
        sls: concrete stress options for SLS

    return:
        { "ULS": "strain":[0.1,2,4,4,35,], "stress":[0,234235,235,235,], "SLS": stress_strain_curve }: material properties of selected data
    """
    if general is None:
        general = concrete_general_properties()
    if uls is None:
        uls = concrete_stress_uls_options_ACI()
    if sls is None:
        sls = concrete_sls_options()

    if uls.material_model == 'Rectangle':
        _uls_strains = [
            0,
            uls.compressive_failure_strain * (1 - uls.factor_b1),
            uls.compressive_failure_strain * (1 - uls.factor_b1),
            uls.compressive_failure_strain,
        ]
        _uls_stress = [
            0,
            0,
            uls.factor_b1 * general.strength,
            uls.factor_b1 * general.strength,
        ]

    if sls.material_model == 'Linear':
        _sls_strains = [
            0,
            sls.failure_compression_limit,
        ]
        _sls_stress = [
            0,
            general.strength,
        ]

    return {
        "ULS": asdict(stress_strain_curve(["Strain", "Stress"], [_uls_strains, _uls_stress])),
        "SLS": asdict(stress_strain_curve(["Strain", "Stress"], [_sls_strains, _sls_stress])),
    }

def rebar_properties_design(
    general: rebar_general_properties,
    uls: rebar_stress_uls_options_ACI,
    sls: rebar_stress_sls_options
) -> dict[str, stress_strain_curve]:
    """
    Return the material properties based on the design code

    Args:
        general: general rebar properties
        uls: rebar stress options for ULS
        sls: rebar stress options for SLS

    return:
        { "ULS": "strain":[0.1,2,4,4,35,], "stress":[0,234235,235,235,], "SLS": stress_strain_curve }: material properties of selected data
    """
    yield_strain = general['strength'] / general['elastic_modulus']

    _sls_strains = [
        0,
        yield_strain,
        sls['failure_strain']
    ]
    _sls_stress = [
        0,
        general['strength']
    ]

    _uls_strains = [
        0,
        yield_strain,
        uls['failure_strain']
    ]
    _uls_stress = [
        0,
        general['strength']
    ]

    print(_sls_strains)
    print(_uls_strains)

    return {
        "ULS": asdict(stress_strain_curve(["Strain", "Stress"], [_uls_strains, _uls_stress])),
        "SLS": asdict(stress_strain_curve(["Strain", "Stress"], [_sls_strains, _sls_stress])),
    }


def get_schema_of_dataclass(dataclass):
    """
    """

    return {
        "type": "object",
        "properties": {
                "material_model": {"type": "string"},
                "factor_b1": {"type": "number"},
                "compressive_failure_strain": {"type": "number"},
        }
    }

# front 에서 쓰면 될거
def get_uls_model_schema(design_code: str) -> dict:
    """
    Return the ULS model schema based on the design code

    Args:
        design_code: design code

    return:
        dict: ULS model schema
    """

    target_cls = get_uls_model_class(design_code)
    return get_schema_of_dataclass(target_cls)

# python 에서는 더 직접적으로
def get_uls_model_class(design_code: str) -> dataclass:
    """
    Return the ULS model class based on the design code

    Args:
        design_code: design code

    return:
        dataclass: ULS model class
    """

    if design_code == "ACI 318M-19":
        return concrete_stress_uls_options_ACI
    elif design_code == "Eurocode 2":
        return concrete_stress_uls_options_Eurocode


def calc_uls_model_properties(design_code: str) -> dataclass:
    """
    Return the ULS model class based on the design code

    Args:
        design_code: design code

    return:
        dataclass: ULS model class
    """

    # 기준별 uls 데이터 모델을 가져옴(class)
    uls = get_uls_model_class(design_code)

    # 데이터 클래스를 초기화 하는 것이 값을 설정하는 것과 같음
    obj = uls(design_code)

    return obj


# @database
# def get_rebar_properties(design_code:str, grade:str)->dict:
#     """
#     Return the material properties of single data based on the design code

#     Args:
#         design_code: design code
#         grade: grade of the concrete

#     return:
#         dict: material properties of selected data
#     """

#     db_unit = get_db_unit("concrete rebar properties for &{design_code}")   # 현재 DB Unit 을 가져옴
#     dia = get_from_db("concrete rebar properties for &{design_code}", grade)  # 이 읽기 전용 DB 의 단위계를 통일 할 수 없음(길이: m, 강도: MPa, 밀도: kg/m^3)
#                                          # 이건 데이터 종류에 따라서 적합한 단위계가 다르다.
#     code_unit = get_design_code_unit(design_code)
#     if( code_unit != db_unit):
#         dia_out = convert_unit(code_unit, dia)
#     #{ "dia" : 10}
#     return dia_out


def calc_reinforcing_steel_properties(
    units: gsdUnit,
    design_code: str,
    stregnth: float,
    density: float
) -> dict:
    """
    Return the material properties of single data based on the design code

    Args:
        units: units
        design_code: design code
        strength: strength of the concrete
        density: density of the concrete

    return:
        dict: material properties of selected data
    """
    return {
        "ELASITC_MODULUS": 30000,
        "STRESS_STRAIN_CURVE": {
            ...
        }
    }


def calc_prestressing_steel_properties(
    units: gsdUnit,
    design_code: str,
    stregnth: float,
    density: float
) -> dict:
    """
    Return the material properties of single data based on the design code

    Args:
        units: units
        design_code: design code
        strength: strength of the concrete
        density: density of the concrete

    return:
        dict: material properties of selected data
    """
    return {
        "ELASITC_MODULUS": 30000,
        "STRESS_STRAIN_CURVE": {
            ...
        }
    }


class PM3DCurve:
    """
    Class for PM3D Curve Calculation
    """
    def __init__(self, matl=gsdMaterialBind, geom=gsdGeometry, lcb=gsdLcbBind, opt=gsdOptions):
        self.material_uls = matl.uls
        self.concrete_material_uls = self.material_uls.
        self.rebar_material_uls = self.material_uls.get("rebar", {})

        self.material_sls = matl.sls
        self.concrete_material_sls = self.material_sls.get("concrete", {})
        self.rebar_material_sls = self.material_sls.get("rebar", {})

        self.geom = geom.get("geometry", {})
        self.concrete_geom = self.geom.get("concrete", {})
        self.rebar_geom = self.geom.get("rebar", {})

        self.lcom = lcb.get("lcom", {})
        self.lcom_uls = self.lcom.get("uls", {})
        self.lcom_sls = self.lcom.get("sls", {})

        self.option = opt

    def get_concrete_material_curve(self, type_):
        curve_data = self.concrete_material.get("curve", {}).get(type_, {})
        head = curve_data.get("HEAD", [])
        data = curve_data.get("DATA", [])
        if head and data:
            strain = data[0]
            stress = data[1]
            return {"Strain": strain, "Stress": stress}
        return {}

    def get_max_strain_with_zero_stress(self, data):
        df = pd.DataFrame(data["DATA"]).transpose()
        df.columns = data["HEAD"]

        zero_stress_strains = df[df["Stress"] == 0.0]["Strain"]

        max_strain = zero_stress_strains.max()
        return max_strain

    def get_concrete_geom(self):
        return self.concrete_geom

    def get_rebar_geom(self):
        return self.rebar_geom

    def get_lcom_uls_data(self):
        return self.lcom_uls.get("DATA", [])
    
    def get_lcom_sls_data(self):
        return self.lcom_sls.get("DATA", [])

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
        
        ss_rebar_uls = ssp.StressStrainProfile(self.rebar_material_uls["curve"]["uls"]["Strain"], self.rebar_material["curve"]["uls"]["Stress"])
        ss_rebar_sls = ssp.StressStrainProfile(self.rebar_material_sls["curve"]["sls"]["Strain"], self.rebar_material["curve"]["sls"]["Stress"])

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

    lcoms_uls = data.get_lcom_uls_data()
    result_lcom_uls = []
    for lcom in lcoms_uls:
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

        result_lcom_uls.append([lcom_name, locations[0, 2], locations[0, 0], locations[0, 1]])
    
    lcoms_sls = data.get_lcom_sls_data()
    result_lcom_sls = []        
    for lcom in lcoms_sls:
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

        result_lcom_sls.append([lcom_name, locations[0, 2], locations[0, 0], locations[0, 1]])

    hull_points_list = hull.points.tolist() if isinstance(hull.points, np.ndarray) else hull.points
    res = {
        "uls_3DPM": {
            "HEAD": ["Mx", "My", "P"],
            "DATA": hull_points_list
        },
        "sls_3DPM": {
            "HEAD": ["Mx", "My", "P"],
            "DATA": hull_points_list
        },
        "uls_strength": {
            "HEAD": ["Name", "Mny", "Mnz", "Pn"],
            "DATA": result_lcom_uls
        },
        "sls_strength": {
            "HEAD": ["Name", "Mny", "Mnz", "Pn"],
            "DATA": result_lcom_sls
        }
    }

    return json.dumps(res)

def calc_3dpm(
    material: gsdMaterialBind, geometry: gsdGeometry, lcb: gsdLcbBind, opt: gsdOptions
) -> dict:
    """
    Return the 3D PM Curve & norminal strength points

    Args:
        material: material
        geometry: geometry
        lcb: lcb

    return:
        dict: 3DPM curve & norminal strength points about lcom
    """
    pm = PM3DCurve(material, geometry, lcb, opt)
    res = pm.make_3dpm_data()
    print(res)


material = gsdMaterialBind
geom = gsdGeometry
lcb = gsdLcbBind
opt = gsdOptions
res = calc_3dpm(material, geom, lcb, opt)
print(res)


# inp = {
# "general": {
#     "strength": 420,
#     "elastic_modulus": 200000,
#     "density": 7850,
#     "thermal_expansion_coefficient": 0.00001,
#     "poisson_ratio": 0.3
# },
# "uls": {
#     "material_model": "Elastic-Plastic",
#     "failure_strain": 0.7
# },
# "sls": {
#     "material_model": "Elastic-Plastic",
#     "failure_strain": 0.7
# }
# }

# res = rebar_properties_design(**inp)
# print(res)