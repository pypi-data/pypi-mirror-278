from cv_smart_house_camera.server import configure_camera_server

def main():
    configure_camera_server(allow_origins=["*"],
                            allow_methods=["*"],
                            allow_headers=["*"])

if __name__ == "__main__":
    main()