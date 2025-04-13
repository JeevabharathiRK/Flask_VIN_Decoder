import subprocess
import time
import requests
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

ngrok_process = None
public_url = None

def run():
    global ngrok_process, public_url

    # Start ngrok in the background on port 5000
    ngrok_process = subprocess.Popen(["ngrok", "http", "5000"], stdout=subprocess.DEVNULL)

    # Wait for the ngrok API to be ready
    time.sleep(2)

    # Fetch public URL from ngrok's local API
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                public_url = tunnel["public_url"]
                break
        print("✅ Public URL:", public_url)
    except Exception as e:
        print("❌ Error fetching public URL:", e)
        return None

    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(public_url)
    qr.make(fit=True)

    qr_image = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(
            back_color=(255, 255, 255),
            front_color=(30, 30, 60)
        )
    )
    # qr_image.show()
    qr_image.save("static/qr.png")
    return public_url