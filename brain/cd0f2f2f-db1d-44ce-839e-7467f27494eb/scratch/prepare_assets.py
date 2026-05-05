import os
import shutil
from PIL import Image

# Source paths
base_dir = r"d:\DataForEntrepreneurs\PartyGamesHub"
shared_assets = os.path.join(base_dir, "SharedAssets")
gold_logo = os.path.join(shared_assets, "gold.png")
feature_graphic = os.path.join(shared_assets, "feature_graphic_1024x500.png")
dashboard_img = os.path.join(shared_assets, "Dashboard.png")
phone_tutorial = os.path.join(base_dir, "Games", "Launcher", "dist", "drawjudge", "dj_tutorial_1.png")

# Target directory
target_dir = os.path.join(base_dir, "PlayStoreAssets")
os.makedirs(target_dir, exist_ok=True)

# 1. App Icon 512x512
app_icon_path = os.path.join(target_dir, "app_icon_512x512.png")
print("Generating App Icon 512x512...")
icon_img = Image.open(gold_logo).convert("RGBA")
icon_img = icon_img.resize((512, 512), Image.Resampling.LANCZOS)
icon_img.save(app_icon_path)

# 2. Feature Graphic
print("Copying Feature Graphic...")
target_feature = os.path.join(target_dir, "feature_graphic_1024x500.png")
shutil.copy(feature_graphic, target_feature)

# 3. Screenshots
print("Copying Screenshots...")
target_tv_screenshot = os.path.join(target_dir, "screenshot_1_tv.png")
shutil.copy(dashboard_img, target_tv_screenshot)

target_phone_screenshot = os.path.join(target_dir, "screenshot_2_phone.png")
shutil.copy(phone_tutorial, target_phone_screenshot)

print(f"\nAll Play Store assets have been prepared successfully in: {target_dir}")
