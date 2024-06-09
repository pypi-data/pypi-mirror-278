from cv_smart_house_camera.utils.get_modules_from_toml import get_modules_from_toml

import os

# Define the path
path = '.\\.tmp'
file_path = os.path.join(path, 'modules_list.py')

# Check if the directory exists and create it if it doesn't
if not os.path.exists(path):
    os.makedirs(path)




def generate_code():
    print("Generating code...")
    modules = get_modules_from_toml()
    import_code = []
    modules_list = []



    for package, version in modules:
        print(f"Processing package {package} with version {version}")
        import_statement = f"import {package}"
        import_code.append(import_statement)
        module_item = f"""{{ "name": {package}.name, "package_name": "{package}", "processing": {package}.processing, "options": {package}.options }}"""

        modules_list.append(module_item)

    # Write to the file
    with open(file_path, 'w') as out_file:
        out_file.write('\n'.join([*import_code, "\n", "modules = [", ", ".join(modules_list), "]"]))

if __name__ == "__main__":
    generate_code()