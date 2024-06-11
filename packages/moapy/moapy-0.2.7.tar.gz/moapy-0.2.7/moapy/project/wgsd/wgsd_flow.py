from dataclasses import dataclass, asdict, field as dataclass_field
from enum import Enum

import pprint
import json


@dataclass
class gsdUnit:
    """
    GSD global unit class
    """
    force: str = dataclass_field(
        default="kN", metadata={
            "description": "Force unit"})
    length: str = dataclass_field(
        default="m", metadata={
            "description": "Length unit"})
    section_dimension: str = dataclass_field(
        default="mm", metadata={
            "description": "Section dimension unit"})
    pressure: str = dataclass_field(
        default="MPa", metadata={
            "description": "Pressure unit"})
    strain: str = dataclass_field(
        default="%", metadata={
            "description": "Strain unit"})


@dataclass
class gsdConcreteProp:
    """
    GSD concrete class
    """
    design_code: str = dataclass_field(
        default="ACI 318M-19",
        metadata={
            "description": "Design code"})
    grade: str = dataclass_field(
        default="C12", metadata={
            "description": "Grade of the concrete"})


@dataclass
class concrete_general_properties:
    """
    GSD concrete general properties for calculation
    """
    strength: int = dataclass_field(
        default=12, metadata={
            "description": "Grade of the concrete"})
    elastic_modulus: float = dataclass_field(
        default=30000, metadata={
            "description": "Elastic modulus of the concrete"})
    density: float = dataclass_field(
        default=2400, metadata={
            "description": "Density of the concrete"})
    thermal_expansion_coefficient: float = dataclass_field(
        default=0.00001, metadata={
            "description": "Thermal expansion coefficient of the concrete"})
    poisson_ratio: float = dataclass_field(
        default=0.2, metadata={
            "description": "Poisson ratio of the concrete"})


@dataclass
class concrete_stress_uls_options_ACI:
    """
    GSD concrete stress options for ULS
    """
    material_model: str = dataclass_field(
        default="Rectangle", metadata={
            "description": "Material model for ULS"})
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
        default="Rectangle", metadata={
            "description": "Material model for ULS"})
    partial_factor_case: str = dataclass_field(
        default="1", metadata={
            "description": "Partial factor case for ULS"})
    partial_factor: float = dataclass_field(
        default=1.5, metadata={
            "description": "Partial factor for ULS"})
    compressive_failure_strain: float = dataclass_field(
        default=0.003, metadata={"description": "Failure strain limit for ULS"})


@dataclass
class concrete_sls_options:
    """
    GSD concrete stress options for SLS
    """
    material_model: str = dataclass_field(
        default="Linear", metadata={
            "description": "Material model for SLS"})
    plastic_strain_limit: float = dataclass_field(
        default=0.002, metadata={
            "description": "Plastic strain limit for SLS"})
    failure_compression_limit: float = dataclass_field(
        default=0.003, metadata={
            "description": "Failure compression limit for SLS"})
    material_model_tension: str = dataclass_field(
        default="interpolated", metadata={
            "description": "Material model for SLS tension"})
    failure_tension_limit: float = dataclass_field(
        default=0.003, metadata={
            "description": "Failure tension limit for SLS"})

# Rebar
@dataclass
class rebar_general_properties:
    """
    GSD rebar general properties for calculation
    """
    strength: int = dataclass_field(
        default=420, metadata={
            "description": "Grade of the rebar"})
    elastic_modulus: float = dataclass_field(
        default=200000, metadata={
            "description": "Elastic modulus of the rebar"})
    density: float = dataclass_field(
        default=7850, metadata={
            "description": "Density of the rebar"})
    thermal_expansion_coefficient: float = dataclass_field(
        default=0.00001, metadata={
            "description": "Thermal expansion coefficient of the rebar"})
    poisson_ratio: float = dataclass_field(
        default=0.3, metadata={
            "description": "Poisson ratio of the rebar"})

@dataclass
class rebar_stress_uls_options_ACI:
    """
    GSD rebar stress options for ULS
    """
    material_model: str = dataclass_field(
        default="Elastic-Plastic", metadata={
            "description": "Material model for ULS"})
    failure_strain: float = dataclass_field(
        default=0.7, metadata={"description": "Failure strain limit for ULS"})


@dataclass
class rebar_stress_sls_options:
    """
    GSD rebar stress options for SLS
    """
    material_model: str = dataclass_field(
        default="Elastic-Plastic", metadata={
            "description": "Material model for SLS"})
    failure_strain: float = dataclass_field(
        default=0.7, metadata={"default" : 0.7, "description": "Failure strain limit for SLS"})


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


@dataclass
class gsdDesignCode:
    design_code: str = dataclass_field(default="ACI 318-19")
    sub_code: str = dataclass_field(default="SI")

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
class gsdLcb:
    """
    GSD load combination class
    """
    uls: loadcomb = dataclass_field(
        default=None, metadata={"description": "uls load combination"})
    sls: loadcomb = dataclass_field(
        default=None, metadata={"description": "sls load combination"})

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
        default=None, metadata={"description": "Stress strain curve"})
    curve_sls: stress_strain_curve = dataclass_field(
        default=None, metadata={"description": "Stress strain curve"})


@dataclass
class gsdMaterialTendon:
    """
    GSD tendon class
    """
    code: str = dataclass_field(
        default="ASTM A416", metadata={
            "description": "Tendon code"})
    # name 은 왜 필요한지?
    curve_uls: stress_strain_curve = dataclass_field(
        default=None, metadata={"description": "Stress strain curve"})
    curve_sls: stress_strain_curve = dataclass_field(
        default=None, metadata={"description": "Stress strain curve"})


@dataclass
class gsdMaterialConcrete:
    """
    GSD material for Concrete class
    """
    # name 은 왜 필요한지?
    conc_prop: gsdConcreteProp = dataclass_field(
        default=None, metadata={
            "description": "Concrete properties"})
    curve_uls: stress_strain_curve = dataclass_field(
        default=None, metadata={"description": "Stress strain curve"})
    curve_sls: stress_strain_curve = dataclass_field(
        default=None, metadata={"description": "Stress strain curve"})


@dataclass
class gsdMaterial:
    """
    GSD concrete class
    """
    concrete: gsdMaterialConcrete = dataclass_field(
        default=None, metadata={"description": "Concrete properties"})
    rebar: gsdMaterialRebar = dataclass_field(
        default=None, metadata={
            "description": "Rebar properties"})
    tendon: gsdMaterialTendon = dataclass_field(
        default=None, metadata={
            "description": "Tendon properties"})


@dataclass
class gsdPolygon:
    """
    GSD polygon class
    "HEAD": ["x", "y"],
    "DATA": [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]],
    """
    HEAD: list[str, 2] = dataclass_field(
        default=None, metadata={"description": "Head of the polygon"})
    DATA: list[list[float, 2]] = dataclass_field(
        default=None, metadata={"description": "Data of the polygon"})


@dataclass
class gsdGeometry:
    """
    GSD geometry class
    """


@dataclass
class gsdMaterialConcreteShape:
    """
    GSD material Shape class
    """

# @forUI
# DB functions


def get_design_code() -> list[str]:
    """
    Return the list available of design codes

    return:
        list[gsdDesignCode]: list of design codes
    """
    # return gsdDesignCode enum list
    return ["ACI 318M-19", "ACI 318-19", ...]

# @forUI
# DB functions


def get_design_sub_code(design_code: str) -> list[str]:
    """
    Return the list available of design sub codes

    Args:
        design_code: design code

    return:
        list[str]: list of design sub codes
    """
    # return gsdDesignCode enum list
    return ["SI", "IN-LB", ...]


def get_general_concrete_properties(grade: str) -> concrete_general_properties:
    """
    Return the general concrete properties based on the grade

    Args:
        grade: grade of the concrete

    return:
        concrete_general_properties: general concrete properties
    """
    return concrete_general_properties()


def calc_concrete_properties(
        design_code: gsdDesignCode,
        grade: str) -> dict:
    """
    Return the material properties based on the design code

    Args:
        units: units
        design_code: design code,
        grade: grade of the concrete

    return:
        dict: material properties of selected data
    """

    general = get_general_concrete_properties(grade)
    uls_props = calc_uls_model_properties(design_code.design_code)
    sls_props = calc_sls_model_properties(design_code.design_code)

    return {
        "general": asdict(general),
        "uls": asdict(uls_props),
        "sls": asdict(sls_props)
    }


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
        "properties": {
            "general": asdict(general),
            "uls": asdict(uls),
            "sls": asdict(sls)
        },
        "ULS": stress_strain_curve(["Strain", "Stress"], [_uls_strains, _uls_stress]),
        "SLS": stress_strain_curve(["Strain", "Stress"], [_sls_strains, _sls_stress]),
    }

def rebar_properties_design(
    units: gsdUnit,
    design_code: gsdDesignCode,
    grade: str,
    general: rebar_general_properties = None,
    uls: rebar_stress_uls_options_ACI = None,
    sls: rebar_stress_sls_options = None
) -> dict[str, stress_strain_curve]:
    """
    Return the material properties based on the design code

    Args:
        units: units
        design_code: design code,
        grade: grade of the concrete

    return:
        { "ULS": "strain":[0.1,2,4,4,35,], "stress":[0,234235,235,235,], "SLS": stress_strain_curve }: material properties of selected data
    """
    yield_strain = general.strength / general.elastic_modulus

    _sls_strains = [
        0,
        yield_strain,
        sls.failure_strain
    ]
    _sls_stress = [
        0,
        general.strength
    ]

    _uls_strains = [
        0,
        yield_strain,
        uls.failure_strain
    ]
    _uls_stress = [
        0,
        general.strength
    ]

    print(_sls_strains)
    print(_uls_strains)

    return {
        "properties": {
            "general": asdict(general),
            "uls": asdict(uls),
            "sls": asdict(sls)
        },
        "ULS": stress_strain_curve(["Strain", "Stress"], [_uls_strains, _uls_stress]),
        "SLS": stress_strain_curve(["Strain", "Stress"], [_sls_strains, _sls_stress]),
    }

# pprint.pprint(conc_properties_design_ACI(gsdUnit(), gsdDesignCode(), "C12"))


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


# bschoi
# def generate_pm_curve()

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
