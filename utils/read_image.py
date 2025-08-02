from PIL import Image
from PIL.ExifTags import TAGS
import os

def read_image_with_metadata(filepath):
    """
    Read a PNG file and print out all its metadata including tEXt chunks.
    
    Args:
        filepath (str): Path to the PNG file
    """
    try:
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"Error: File '{filepath}' not found.")
            return
        
        # Open the image
        with Image.open(filepath) as img:
            print(f"Image file: {filepath}")
            print(f"Format: {img.format}")
            print(f"Mode: {img.mode}")
            print(f"Size: {img.size[0]} x {img.size[1]} pixels")
            print("-" * 50)
            
            # Print basic image info
            if hasattr(img, 'info') and img.info:
                print("Image Info (including tEXt metadata):")
                for key, value in img.info.items():
                    print(f"  {key}: {value}")
                print("-" * 50)
            else:
                print("No tEXt metadata found in image info.")
                print("-" * 50)
            
            # Try to get EXIF data (though PNG files typically don't have EXIF)
            try:
                exif_data = img._getexif()
                if exif_data:
                    print("EXIF Data:")
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        print(f"  {tag}: {value}")
                    print("-" * 50)
                else:
                    print("No EXIF data found (typical for PNG files).")
                    print("-" * 50)
            except AttributeError:
                print("No EXIF data available (typical for PNG files).")
                print("-" * 50)
            
            # For PNG files, check for additional metadata
            if img.format == 'PNG':
                print("PNG-specific metadata:")
                # Check for transparency
                if 'transparency' in img.info:
                    print(f"  Transparency: {img.info['transparency']}")
                
                # Check for gamma
                if 'gamma' in img.info:
                    print(f"  Gamma: {img.info['gamma']}")
                
                # Check for DPI
                if hasattr(img, 'info') and 'dpi' in img.info:
                    print(f"  DPI: {img.info['dpi']}")
                
                print("-" * 50)
    
    except Exception as e:
        print(f"Error reading image: {e}")

# Example usage
if __name__ == "__main__":
    # Test with the PNG file found in the workspace
    test_file = "/Users/rahulnunna/sources/mono/sim/output_images/20250801_170331.517/image_20250227_010016.814.png"
    read_image_with_metadata(test_file)
