# from inflection import underscore
from typing import Callable
from dmtgen.common.blueprint import Blueprint
from dmtgen.common.blueprint_attribute import BlueprintAttribute
from dmtgen.common.package import Package

def to_file_name(blueprint: Blueprint):
    """Convert blueprint name to source file name"""
    return blueprint.name + '.F90'

def to_type_name(blueprint: Blueprint):
    """Convert blueprint name to type name"""
     #TODO return underscore(name)+"_t"
    return blueprint.name

def to_field_name(name: str):
    """Convert attribute name to field name"""
    #TODO: return underscore(name)
    return name

def to_type_path(blueprint: Blueprint):
    """Convert to unverscored name"""
    return blueprint.get_path().replace("/","_")

def to_module_name(blueprint: Blueprint):
    """Convert to module name"""
    #TODO return underscore(blueprint.name)+"_mod"
    path=to_type_path(blueprint)
    return f"class_{path}"

def has_attribute(bp: Blueprint, test: Callable[[BlueprintAttribute], bool]):
    """Check if blueprint has a attribute that passes the test"""
    for attribute in bp.all_attributes.values():
        if test(attribute):
            return True
    return False

def to_package_module_name(package: Package) -> str:
    """Convert Package to module name"""
    if package.parent:
        return to_package_module_name(package.parent) + '_' + package.name
    else:
        return package.name
