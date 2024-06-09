import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from cv_smart_house_camera.data.frames import modules_result
import uuid
import google_crc32c
from cv_smart_house_camera.database.database import update_record

# Create an RTCPeerConnection instance
pc = RTCPeerConnection()
data_channel = pc.createDataChannel("camera")
print("Peer connection created")

async def offer_async(module: str):
    offer = await pc.createOffer()

    @pc.on("icecandidate")
    async def on_icecandidate(candidate):
        if candidate:
            print("ICE candidate:", candidate)

    @data_channel.on("open")
    def on_open():
        print("Data channel is open")

        # Example function to send an image
        async def send_image():
            while True:
                # Send the image data
                module_result = modules_result.get(module)
                if module_result is None or module_result.get("ok") == False:
                    raise Exception(f"Module {module} failed processing")
                frame = module_result.get("frame")
                data_channel.send(frame)

                # Wait for some time before sending the next image
                await asyncio.sleep(1000/60)

        asyncio.ensure_future(send_image())

    @data_channel.on("message")
    def on_message(message):
        if isinstance(message, str) and message == "BYE":
            print("Exiting")
            asyncio.get_event_loop().stop()

    # Create and set the local description
    await pc.setLocalDescription(offer)

    # Prepare the response data with local SDP and type
    response_data = {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

    print("Offer created", response_data)

    update_record("camera", "offer", response_data)

def offer(module:str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.ensure_future(offer_async(module))
    loop.run_forever()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(offer("test"))


