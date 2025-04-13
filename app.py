from flask import Flask, render_template, render_template_string, request
from api import vinBar, IND as ind, NHTSA as us , ngrokQR as ng     
import atexit
import subprocess , os

app = Flask(__name__)

US_OUT = '''
<!DOCTYPE html>
<html>
<head>
    <title>NHTSA API Fetch</title>
</head>
<body style="font-family:sans-serif; background:#f5f5f5; text-align:center; padding:50px;">
    <h1>U.S. Department of Transportation</h1>
    <h2>National Highway Traffic Safety Administration:</h2>
    <br/>
    <div style="text-align:left; margin:auto; width:50%;">
    <h3>VIN Barcode ⇣ </h3>
    <img src="{{ barPath }}" width="300px"/>
    </div>
    <br/>
    <h3>🔍 Vehicle Details ⇣</h3>
    {% if data %}
        <div style="text-align:left; margin:auto; width:50%;">
        {% for item in data %}
            <p><strong>{{ item['Variable'] }}:</strong> {{ item['Value'] }}</p>
        {% endfor %}
        </div>
    {% endif %}
</body>
</html>
'''

IND_OUT = '''
<!DOCTYPE html>
<html>
<head>
    <title>Indian VIN Decode</title>
</head>
<body style="font-family:sans-serif; background:#f5f5f5; text-align:center; padding:50px;">
    <h1>Ministry of Road Transport & Highways</h1>
    <h2>India VIN Decoding Result:</h2>
    <br/>
    <div style="text-align:left; margin:auto; width:50%;">
    <h3>VIN Barcode ⇣ </h3>
    <img src="{{ barPath }}" width="300px"/>
    </div>
    <br/>
    <h3>🔍 Vehicle Details ⇣</h3>
    {% if data %}
        <div style="text-align:left; margin:auto; width:50%;">
        {% for key, value in data.items() %}
            <p><strong>{{ key }}:</strong> {{ value }}</p>
        {% endfor %}
        </div>
    {% endif %}
</body>
</html>
'''

tunnel_url = None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        country = request.form.get("country")
        text_input = request.form.get("text_input")
        image = request.files.get("image")

        #UNITED STATES
        if country == "United States":
            if text_input and len(text_input.strip()) != 0:
                if len(text_input) == 17:
                    barPath = vinBar.generateBarCode(text_input)
                    data = us.vinUS(text_input)
                    return render_template_string(US_OUT, barPath="static/"+barPath+".png", data=data)
                else:
                    return "❌ Invalid VIN / Chassis Number"
            elif image and image.filename != "":
                vin = vinBar.extractVin(image)
                if len(vin) == 17:
                    barPath = vinBar.generateBarCode(vin)
                    data = us.vinUS(vin)
                    return render_template_string(US_OUT, barPath="static/"+barPath+".png", data=data)
                else:
                    return "❌ Invalid VIN / Chassis Number"

            else:
                return "⚠️ Please fill either the text field or upload an image."
        
        #INDIA
        else:
            if text_input and len(text_input.strip()) != 0:
                if len(text_input) == 17:
                    barPath = vinBar.generateBarCode(text_input)
                    data = ind.vinIND(text_input)
                    return render_template_string(IND_OUT, barPath="static/"+barPath+".png", data=data)
                else:
                    return "❌ Invalid VIN / Chassis Number"
            elif image and image.filename != "":
                vin = vinBar.extractVin(image)
                if len(vin) == 17:
                    barPath = vinBar.generateBarCode(vin)
                    data = ind.vinIND(vin)
                    return render_template_string(IND_OUT, barPath="static/"+barPath+".png", data=data)
                else:
                    return "❌ Invalid VIN / Chassis Number"

            else:
                return "⚠️ Please fill either the text field or upload an image."

    return render_template("index.html")

def shutdown():
    print("🛑 Shutting down...")
    try:
        subprocess.run("taskkill /f /im ngrok.exe", shell=True)
        print("✅ ngrok killed.")
    except Exception as e:
        print("❌ Error killing ngrok:", e)

atexit.register(shutdown)

#auto-reloader gaurd for ngrok Use it when the debugger is on. 
#if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
tunnel_url = ng.run()

if __name__ == "__main__":
    app.run()
