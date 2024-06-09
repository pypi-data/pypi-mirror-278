from cv_smart_house_camera.server import configure_camera_server

if __name__ == "__main__":
    configure_camera_server(allow_origins=["*"],
                            allow_methods=["*"],
                            allow_headers=["*"])