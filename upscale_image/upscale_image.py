from PIL import Image

def upscale_image(input_image_path, output_image_path, scale_factor):
    # Open the input image
    image = Image.open(input_image_path)
    
    # Calculate the new size based on the scale factor
    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    # Upscale the image using the 'nearest' resampling method
    upscaled_image = image.resize((new_width, new_height), Image.NEAREST)
    
    # Save the upscaled image
    upscaled_image.save(output_image_path)

# Example usage
input_path = 'input_image.jpg'    # Replace with the path to your input image
output_path = 'upscaled_image.jpg'    # Replace with the desired output path
scale_factor = 2    # Replace with the desired scale factor

upscale_image(input_path, output_path, scale_factor)
