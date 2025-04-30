from PIL import Image

def pixelate_image(input_path, output_path, pixel_size):
    image = Image.open(input_path)
    
    # shrink image based on pixel size then resize it back to original size to pixelate
    small_image = image.resize((image.width // pixel_size, image.height // pixel_size),resample=Image.NEAREST)
    pixelated_image = small_image.resize((image.width, image.height),resample=Image.NEAREST)
    
    # Save the pixelated image
    pixelated_image.save(output_path)
    print(f"Pixelated image saved as {output_path}")

pixelate_image("brock_before.jpg", "brock_after.png", pixel_size=5)