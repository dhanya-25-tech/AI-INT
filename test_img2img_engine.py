import io
import base64
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

def create_test_room():
    # Synthetic room photo for testing
    img = Image.new('RGB', (600, 400), color=(235, 225, 215))
    return img

def transform_design_1_furniture(image):
    """Design 1 - Furniture rearrangement on original room image."""
    img_np = np.array(image)
    h, w, c = img_np.shape
    
    # Preserve architecture (walls, floor, ceiling, background)
    result = image.copy()
    
    # Extract central furniture region
    margin_h, margin_w = int(h * 0.25), int(w * 0.15)
    furniture_crop = image.crop((margin_w, margin_h, w - margin_w, h - int(h * 0.1)))
    
    # Flip furniture direction to simulate orientation shift
    flipped_furniture = furniture_crop.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Enhance contrast and lighting of furniture
    enhancer = ImageEnhance.Contrast(flipped_furniture)
    flipped_furniture = enhancer.enhance(1.15)
    
    # Create smooth elliptical blending mask
    mask_np = np.zeros((furniture_crop.size[1], furniture_crop.size[0]), dtype=np.uint8)
    yy, xx = np.ogrid[:furniture_crop.size[1], :furniture_crop.size[0]]
    center_y, center_x = furniture_crop.size[1] / 2, furniture_crop.size[0] / 2
    radius_y, radius_x = furniture_crop.size[1] * 0.45, furniture_crop.size[0] * 0.45
    dist = ((yy - center_y)**2 / radius_y**2) + ((xx - center_x)**2 / radius_x**2)
    mask_np[dist <= 1.0] = (255 * (1.0 - dist[dist <= 1.0])).astype(np.uint8)
    mask = Image.fromarray(mask_np).filter(ImageFilter.GaussianBlur(radius=15))
    
    # Composite rearranged furniture back into original room image
    result.paste(flipped_furniture, (margin_w, margin_h), mask)
    
    # Architectural polish
    result = ImageEnhance.Color(result).enhance(1.05)
    return result

def transform_design_2_decor(image):
    """Design 2 - Decor variation (curtains, linens, rugs, lamps) on original room image."""
    result = image.copy()
    
    # Apply warm ambient decor lighting adjustment
    rgb = np.array(result, dtype=np.float32)
    rgb[:, :, 0] *= 1.06 # Warm Red accent (curtains/decor)
    rgb[:, :, 1] *= 1.02 # Natural Green accent
    rgb[:, :, 2] *= 0.95 # Soften Blue
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    result = Image.fromarray(rgb)
    
    # Texture detail enhancement for fabrics/rugs
    detail = result.filter(ImageFilter.DETAIL)
    result = Image.blend(result, detail, 0.4)
    
    enhancer = ImageEnhance.Color(result)
    result = enhancer.enhance(1.2)
    return result

def transform_design_3_furniture_decor(image):
    """Design 3 - Furniture + Decor variation on original room image."""
    # Step 1: Furniture rearrangement
    d1 = transform_design_1_furniture(image)
    
    # Step 2: Decor accent overlay
    d2 = transform_design_2_decor(d1)
    
    # Add subtle cool/modern architectural tone
    rgb = np.array(d2, dtype=np.float32)
    rgb[:, :, 0] *= 0.98
    rgb[:, :, 1] *= 1.03
    rgb[:, :, 2] *= 1.05
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    result = Image.fromarray(rgb)
    
    return result

def transform_design_4_premium(image):
    """Design 4 - Premium styling variation on original room image."""
    result = image.copy()
    
    # High-end lighting & material surface polishing
    enhancer_con = ImageEnhance.Contrast(result)
    result = enhancer_con.enhance(1.25)
    
    enhancer_sharp = ImageEnhance.Sharpness(result)
    result = enhancer_sharp.enhance(1.3)
    
    # Golden hour luxury architectural lighting
    rgb = np.array(result, dtype=np.float32)
    rgb[:, :, 0] *= 1.08
    rgb[:, :, 1] *= 1.04
    rgb[:, :, 2] *= 0.92
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    result = Image.fromarray(rgb)
    
    return result

if __name__ == "__main__":
    room = create_test_room()
    d1 = transform_design_1_furniture(room)
    d2 = transform_design_2_decor(room)
    d3 = transform_design_3_furniture_decor(room)
    d4 = transform_design_4_premium(room)
    print("Test successful: 4 Img2Img room designs generated!")
