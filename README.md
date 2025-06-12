# Cloud Removal System

A Flask-based web app that fetches Sentinel-2 satellite images from Microsoft Planetary Computer, runs a diffusion model to “remove” clouds, and serves the result via a simple web interface.

---

## 📁 Repository Structure

```
cloud_removal/
├── run.py                        # App runner (starts Flask + ngrok)
├── model/                        # Place your pretrained model here
│   └── model-41.pt
├── apps/
│   ├── __init__.py
│   ├── config.py
│   ├── inference.py
│   ├── services/planetary_service.py
│   ├── routes/main.py
│   └── templates/index.html
├── requirements.txt              # Python dependencies
├── setup.py                      # Optional install script
└── README.md                     # (this file)
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/cloud_removal.git
cd cloud_removal
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

_or_

```bash
python setup.py install
```

### 3. Download the pretrained model

Download the checkpoint from Google Drive and place it in the `model/` folder, renaming as needed:

- **Download link**:  
  https://drive.google.com/file/d/1rlODW1GRIcKzon5U2kVUpgSR-fD7tR3N/view?usp=sharing  
- **Save as**:  
  ```
  model/model-41.pt
  ```

### 4. (Optional) Configure your environment

Ngrok is used to expose your local server publicly. By default, the code will look for an environment variable `NGROK_TOKEN`. You can either:

```bash
export NGROK_TOKEN="your-ngrok-auth-token"
```

…or just edit `apps/config.py` to hard-code your token.

---

## ▶️ Usage

Simply run:

```bash
python run.py
```

- The console will print a local URL (`http://0.0.0.0:5000`) and an ngrok public URL.
- Open either URL in your browser to load the **Cloud Removal System** UI.

---

## 🔧 How it works

1. **Front end** (`index.html`) lets you choose latitude/longitude (or pick a preset), then fetch available dates.
2. **Backend** (`main.py`) routes:
   - **GET `/available_dates`** → queries STAC for cloud-free images.
   - **GET `/process`** → downloads the bands, stitches them into RGB, runs the diffusion model, and returns two base64 images.
3. **Inference** (`inference.py`) wraps your diffusion model (U-Net + GaussianDiffusion) for mask-based inpainting.

---

## ⚙️ Customization

- Adjust sampling steps or image size in `apps/config.py`.
- Tweak CSS/JS in `apps/templates/index.html` to fit your branding.
- Add more **preset locations** in the `<select id="preset">` element.

---

## 📜 License

This project is licensed under the terms of the [MIT License](LICENSE).
