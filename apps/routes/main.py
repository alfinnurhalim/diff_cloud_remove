import io
import base64
import matplotlib.pyplot as plt
from flask import Blueprint, request, jsonify, render_template
from PIL import Image

from apps.services.planetary_service import get_available_dates, fetch_image
from apps.inference import run_inpainting_from_image
import apps.config as config

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/available_dates')
def available_dates():
    lat = float(request.args.get('lat', 47.6062))
    lon = float(request.args.get('lon', -122.3321))
    dates = get_available_dates(lat, lon)
    return jsonify({'dates': dates})

@main_blueprint.route('/process')
def process():
    lat = float(request.args.get('lat', 47.6062))
    lon = float(request.args.get('lon', -122.3321))
    date = request.args.get('date')
    print((lat, lon, date))
    rgb = fetch_image(lat, lon, date)
    if rgb is None:
        return jsonify(error=f'No image for {lat}/{lon}/{date}'), 404

    # raw image
    buf1 = io.BytesIO()
    plt.imsave(buf1, rgb)
    raw_b64 = base64.b64encode(buf1.getvalue()).decode('utf-8')

    # stylized
    img_pil = Image.fromarray((rgb * 255).astype('uint8'))
    out_img, out_tensor = run_inpainting_from_image(img_pil)
    buf2 = io.BytesIO()
    plt.imsave(buf2, plt.imread(f"{config.OUTPUT_DIR}/stylized_result.jpg"))
    styled_b64 = base64.b64encode(buf2.getvalue()).decode('utf-8')

    return jsonify(raw_image=raw_b64, styled_image=styled_b64)
