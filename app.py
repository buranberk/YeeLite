from flask import Flask, render_template, request, redirect, url_for
from yeelight import Bulb

# Replace with your bulb's IP address
bulb_ip = "192.168.1.x"
bulb = Bulb(bulb_ip)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/toggle/<action>')
def toggle(action):
    if action == "on":
        bulb.turn_on()
    elif action == "off":
        bulb.turn_off()
    return redirect(url_for('home'))


@app.route('/set_color', methods=['POST'])
def set_color():
    h = request.form.get('h')
    s = request.form.get('s')
    v = request.form.get('v')
    if h and s and v:
        # Convert HSV to RGB using the colorsys module
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(float(h)/360, float(s)/100, float(v)/100)
        bulb.set_rgb(int(r*255), int(g*255), int(b*255))
        bulb.set_brightness(int(v))
    return redirect(url_for('home'))

@app.route('/get_state', methods=['GET'])
def get_state():
    state = bulb.get_properties()
    return state


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
