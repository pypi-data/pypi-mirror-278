import toml
from cv_smart_house_camera.constants import PATTERN

def get_modules_from_toml():
    with open('pyproject.toml', 'r') as file:
        pyproject_data = toml.load(file)

    if 'tool' in pyproject_data and 'poetry' in pyproject_data['tool']:
        dependencies = pyproject_data['tool']['poetry'].get('dependencies', {})

    # filter out the modules that start with the PATTERN
    modules = [module for module in dependencies.items() if module[0].startswith(PATTERN)]

    return modules