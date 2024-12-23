from PIL import Image

def load(path):
    image = Image.open(path)
    wid, hei = image.size
    pixels = list(image.convert("RGB").getdata())
    return wid, hei, pixels

def convert_to_gray_scale(pixels):
    gray_pixel = []
    for r, g, b in pixels:
        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        gray_pixel.append((gray, gray, gray))
    return gray_pixel

def convert_to_b_and_w(pixels, limiar=128):
    binaries = []
    for r, g, b in pixels:
        cinza = int(0.299 * r + 0.587 * g + 0.114 * b)
        binary = 255 if cinza >= limiar else 0
        binaries.append((binary, binary, binary))
    return binaries

def save(path, wid, hei, pixels):
    image = Image.new("RGB", (wid, hei))
    image.putdata(pixels)
    image.save(path)

image_path = "../assets/image.png"

wid, hei, pixels = load(image_path)
gray_pixel = convert_to_gray_scale(pixels)
binary_pixel = convert_to_b_and_w(pixels)

save("../assets/image_gray_scale.png", wid, hei, gray_pixel)
save("../assets/image_p&b.png", wid, hei, binary_pixel)

print("success")