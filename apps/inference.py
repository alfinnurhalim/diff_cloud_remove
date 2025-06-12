import torch
import numpy as np
from PIL import Image
from torchvision.utils import save_image

from denoising_diffusion_pytorch import Unet, GaussianDiffusion
import apps.config as config

# Load model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = Unet(
    dim=64,
    dim_mults=(1, 2, 4, 8),
    flash_attn=False
).to(device)

diffusion = GaussianDiffusion(
    model,
    image_size=config.IMAGE_SIZE,
    timesteps=1000,
    sampling_timesteps=250
).to(device)

# Load state
state = torch.load(config.MODEL_PATH)
diffusion.load_state_dict(state['model'])

def run_inpainting_from_image(pil_image, threshold=config.THRESHOLD):
    # Preprocess
    image = pil_image.convert("RGB").resize((config.IMAGE_SIZE, config.IMAGE_SIZE))
    gt = torch.from_numpy(np.array(image)).permute(2,0,1).float() / 255.0
    gt = gt.unsqueeze(0).to(device)

    cloudy_gray = image.convert("L")
    mask_np = (np.array(cloudy_gray) < threshold).astype(np.float32)
    mask = torch.from_numpy(mask_np).unsqueeze(0).unsqueeze(0).to(device)

    with torch.no_grad():
        out_tensor = diffusion.sample(batch_size=1, resample=False, gt=gt, mask=mask)

    out_np = out_tensor.squeeze().permute(1,2,0).cpu().clamp(0,1).numpy()
    out_img = Image.fromarray((out_np * 255).astype(np.uint8))

    # Save tensor result for downstream use
    save_image(out_tensor, f"{config.OUTPUT_DIR}/stylized_result.jpg")

    return out_img, out_tensor
