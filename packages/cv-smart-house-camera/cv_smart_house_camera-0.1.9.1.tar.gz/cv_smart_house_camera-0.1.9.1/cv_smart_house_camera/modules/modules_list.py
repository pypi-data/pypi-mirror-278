import os
import importlib.util
from cv_smart_house_camera.constants import MODULE_LIST_FILE

# Path to the file
file_path = MODULE_LIST_FILE

# Check if the file exists
if os.path.exists(file_path):
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("modules_list", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Import the `modules` variable from the loaded module
    modules = getattr(module, 'modules', [])
else:
    # Return an empty list if the file does not exist
    modules = []


def original_frame_processing(frame, frame_number):
	return

modules.append({ "name": "Original Frame", "package_name": "internal", "processing": original_frame_processing })