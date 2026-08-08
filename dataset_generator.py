import os
import random
from PIL import Image, ImageDraw, ImageFilter

CATEGORIES = ["bathroom", "bedroom", "kitchen", "livingroom", "non_room"]

# Color themes and features per category
ROOM_STYLES = {
    "kitchen": [
        {"bg": (240, 235, 225), "cabinet": (70, 80, 95), "counter": (220, 220, 220), "accent": (180, 100, 50)},
        {"bg": (250, 250, 250), "cabinet": (210, 200, 180), "counter": (50, 50, 50), "accent": (100, 140, 110)},
        {"bg": (35, 40, 50), "cabinet": (50, 60, 75), "counter": (200, 190, 170), "accent": (210, 160, 90)},
        {"bg": (245, 240, 230), "cabinet": (140, 155, 140), "counter": (240, 240, 240), "accent": (160, 120, 90)}
    ],
    "livingroom": [
        {"bg": (235, 230, 220), "sofa": (80, 90, 110), "rug": (180, 170, 155), "accent": (190, 120, 60)},
        {"bg": (40, 40, 45), "sofa": (160, 140, 120), "rug": (70, 70, 80), "accent": (210, 180, 110)},
        {"bg": (245, 245, 240), "sofa": (120, 140, 130), "rug": (210, 200, 185), "accent": (140, 90, 70)},
        {"bg": (225, 220, 210), "sofa": (90, 60, 50), "rug": (190, 185, 175), "accent": (80, 110, 100)}
    ],
    "bathroom": [
        {"bg": (240, 245, 250), "tile": (200, 215, 225), "tub": (255, 255, 255), "accent": (100, 150, 170)},
        {"bg": (35, 40, 45), "tile": (60, 65, 75), "tub": (230, 230, 230), "accent": (180, 150, 100)},
        {"bg": (250, 245, 240), "tile": (220, 200, 190), "tub": (245, 245, 245), "accent": (120, 140, 120)},
        {"bg": (230, 235, 235), "tile": (170, 190, 190), "tub": (250, 250, 250), "accent": (70, 90, 90)}
    ],
    "bedroom": [
        {"bg": (245, 238, 230), "bed": (90, 70, 60), "blanket": (210, 180, 160), "accent": (180, 120, 90)},
        {"bg": (40, 35, 50), "bed": (180, 160, 140), "blanket": (90, 80, 110), "accent": (220, 170, 110)},
        {"bg": (235, 240, 235), "bed": (130, 150, 140), "blanket": (240, 240, 235), "accent": (110, 130, 120)},
        {"bg": (245, 230, 225), "bed": (150, 100, 90), "blanket": (220, 210, 200), "accent": (180, 140, 110)}
    ]
}

def draw_room_image(category, index, size=(300, 300)):
    """Draws synthetic training images for rooms & non-rooms."""
    img = Image.new("RGB", size, color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    w, h = size
    
    if category == "non_room":
        # Draw outdoor scenery, cars, abstract patterns, animals, text
        sub_type = index % 4
        if sub_type == 0:
            # Outdoor nature sky + grass + sun
            draw.rectangle([0, 0, w, int(h*0.6)], fill=(135, 206, 235)) # Sky
            draw.rectangle([0, int(h*0.6), w, h], fill=(34, 139, 34)) # Grass
            draw.ellipse([int(w*0.7), 20, int(w*0.9), 80], fill=(255, 223, 0)) # Sun
        elif sub_type == 1:
            # Car silhouette outdoor road
            draw.rectangle([0, 0, w, int(h*0.5)], fill=(100, 110, 130))
            draw.rectangle([0, int(h*0.5), w, h], fill=(50, 50, 55)) # Asphalt
            draw.rectangle([50, int(h*0.45), w-50, int(h*0.75)], fill=(200, 30, 30)) # Car body
            draw.ellipse([80, int(h*0.7), 130, int(h*0.85)], fill=(20, 20, 20)) # Wheel 1
            draw.ellipse([w-130, int(h*0.7), w-80, int(h*0.85)], fill=(20, 20, 20)) # Wheel 2
        elif sub_type == 2:
            # Abstract geometric graphic pattern
            for x in range(0, w, 40):
                for y in range(0, h, 40):
                    col = ((x*7)%255, (y*11)%255, (x+y*13)%255)
                    draw.rectangle([x, y, x+35, y+35], fill=col)
        else:
            # Text / Document page
            draw.rectangle([0, 0, w, h], fill=(250, 250, 245))
            for y in range(30, h-30, 20):
                draw.line([30, y, w-30, y], fill=(60, 60, 70), width=3)
                
        return img

    styles = ROOM_STYLES[category]
    style = styles[index % len(styles)]
    bg = style["bg"]
    
    # Wall background
    draw.rectangle([0, 0, w, int(h * 0.68)], fill=bg)
    # Floor
    floor_color = (max(0, bg[0]-40), max(0, bg[1]-40), max(0, bg[2]-40))
    draw.rectangle([0, int(h * 0.68), w, h], fill=floor_color)
    draw.line([0, int(h * 0.68), w, int(h * 0.68)], fill=(120, 120, 120), width=2)
    
    if category == "kitchen":
        cab_color = style["cabinet"]
        cnt_color = style["counter"]
        acc_color = style["accent"]
        # Upper cabinets
        draw.rectangle([20, 15, w-20, 80], fill=cab_color, outline=(30, 30, 30))
        # Counter top
        draw.rectangle([10, 135, w-10, 155], fill=cnt_color, outline=(40, 40, 40))
        # Lower cabinets
        draw.rectangle([15, 155, w-15, int(h*0.75)], fill=cab_color, outline=(30, 30, 30))
        # Fridge/stove accent
        draw.rectangle([w-85, 65, w-25, int(h*0.75)], fill=acc_color)
        
    elif category == "livingroom":
        sofa_col = style["sofa"]
        rug_col = style["rug"]
        acc_col = style["accent"]
        # Wall art frame
        draw.rectangle([int(w*0.3), 25, int(w*0.7), 85], fill=acc_col, outline=(255, 255, 255), width=3)
        # Rug on floor
        draw.polygon([(35, int(h*0.7)), (w-35, int(h*0.7)), (w-15, h-10), (15, h-10)], fill=rug_col)
        # Main Sofa
        draw.rectangle([35, 120, w-35, 175], fill=sofa_col, outline=(30, 30, 30))
        draw.rectangle([25, 130, 45, 175], fill=sofa_col) # Armrest
        draw.rectangle([w-45, 130, w-25, 175], fill=sofa_col)
        # Coffee table
        draw.rectangle([int(w*0.35), 170, int(w*0.65), 200], fill=(120, 80, 50), outline=(20, 20, 20))
        
    elif category == "bathroom":
        tile_col = style["tile"]
        tub_col = style["tub"]
        acc_col = style["accent"]
        # Tiled wall grid lines
        for y in range(15, int(h*0.68), 20):
            draw.line([0, y, w, y], fill=tile_col, width=1)
        for x in range(15, w, 25):
            draw.line([x, 0, x, int(h*0.68)], fill=tile_col, width=1)
        # Mirror
        draw.ellipse([int(w*0.38), 20, int(w*0.62), 75], fill=(220, 235, 245), outline=(180, 180, 180), width=3)
        # Vanity sink
        draw.rectangle([int(w*0.3), 85, int(w*0.7), 125], fill=tub_col, outline=(150, 150, 150))
        # Shower glass / Bathtub
        draw.rectangle([15, 130, int(w*0.45), int(h*0.78)], fill=tub_col, outline=acc_col, width=3)
        
    elif category == "bedroom":
        bed_col = style["bed"]
        blk_col = style["blanket"]
        acc_col = style["accent"]
        # Prominent Large Bed Headboard
        draw.rectangle([30, 40, w-30, 125], fill=acc_col, outline=(30, 30, 30), width=3)
        # Bed mattress & duvet
        draw.rectangle([40, 115, w-40, 225], fill=bed_col, outline=(20, 20, 20), width=2)
        draw.rectangle([40, 145, w-40, 225], fill=blk_col) # Blanket fold
        # 2 White Pillows on bed
        draw.rectangle([50, 95, int(w*0.46), 125], fill=(255, 255, 255), outline=(180, 180, 180), width=2)
        draw.rectangle([int(w*0.54), 95, w-50, 125], fill=(255, 255, 255), outline=(180, 180, 180), width=2)
        # Nightstand lamps
        draw.ellipse([15, 110, 35, 130], fill=(255, 235, 170))
        draw.ellipse([w-35, 110, w-15, 130], fill=(255, 235, 170))

    return img

def create_dataset(base_dir="dataset", train_count=35, val_count=10):
    """Creates directory structure and populates train/val dataset split."""
    print("Generating room dataset with non_room out-of-domain class...")
    total_images = 0
    for split, count in [("train", train_count), ("val", val_count)]:
        for cat in CATEGORIES:
            cat_dir = os.path.join(base_dir, split, cat)
            os.makedirs(cat_dir, exist_ok=True)
            for i in range(count):
                img = draw_room_image(cat, i)
                filepath = os.path.join(cat_dir, f"{cat}_{i+1:03d}.jpg")
                img.save(filepath, quality=92)
                total_images += 1
                
    print(f"Dataset successfully created in '{base_dir}/': {total_images} total images across {len(CATEGORIES)} categories.")

if __name__ == "__main__":
    create_dataset()
