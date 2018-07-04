from PIL import Image

background = Image.open("bg.png")
overlay = Image.open("001.png")

background = background.convert("RGBA")
overlay = overlay.convert("RGBA")

new_img = Image.blend(background, overlay, 0.5)
new_img.save("new.png","PNG")
