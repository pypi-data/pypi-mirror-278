from cv_smart_house_camera.modules.modules_list import modules
from cv_smart_house_camera.data.frames import modules_result
import concurrent.futures
from cv_smart_house_camera.database.database import crud_factory
import cv2
from cv_smart_house_camera.utils.get_local_ip import get_local_ip

# Define a thread pool
pool = concurrent.futures.ThreadPoolExecutor()

# Dictionary to hold futures for each module
module_futures = {}


def modules_processing(originalFrame, frame_number):
	frameCopy = originalFrame.copy()

	# Submit each module processing task to the thread pool
	for module in modules:
		previous_module_future = module_futures.get(module.get("name"))
		skip_frames = None
		if module and module.get("options"):
			skip_frames = module.get("options").get("processing_frame")

		# Check if the previous module is done processing
		if previous_module_future is None or (skip_frames is None and previous_module_future.running() is False) or (skip_frames is not None and frame_number % skip_frames == 0):
			# Submit module processing task to the thread pool and store the future

			future = pool.submit(module.get("processing"), frameCopy, frame_number, crud_factory(get_local_ip(), module.get("name")))
			module_futures[module.get("name")] = future
			future.add_done_callback(lambda f, moduleName=module.get("name"): store_result(f, moduleName, originalFrame))

def store_result(future, module_name, original_frame):
	try:
		result = future.result()
		# Get the frame from the result or use the original frame
		frame = result.get("frame") if result is not None and result.get("frame") is not None else original_frame
		modules_result[module_name] = {
			"ok": True,
			# convert to jpeg and save in variable
			"frame": cv2.imencode('.jpg', frame)[1].tobytes()
		}
	except Exception as e:
		modules_result[module_name] = {"ok": False}
		print(f"Error store frame in {module_name} module: {e}")