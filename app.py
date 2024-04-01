# app.py
import os
import qrcode
from PIL import Image
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    url = request.form['url']
    background_color = request.form['background_color']
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color=background_color)

    choice = request.form.get('customize_logo')

    if choice == 'yes':
        logo_path = request.files['logo']
        logo_img = Image.open(logo_path)
        max_logo_size = min(img.width, img.height) // 2
        resize_factor = 0.4
        new_size = (int(logo_img.width * resize_factor), int(logo_img.height * resize_factor))
        logo_img = logo_img.resize(new_size)
        shift_factor = 5.1
        paste_position = ((img.width - logo_img.width) // 2 + int(img.width * shift_factor),
                          (img.height - logo_img.height) // 2)
        img.paste(logo_img, paste_position)

    img_path = os.path.join('static', 'generated_qr.jpg')
    img.save(img_path)
    return render_template('qr_display.html', qr_image=img_path)

if __name__ == '__main__':
    app.run(debug=True)
