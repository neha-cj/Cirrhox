# backend/ml/preprocess_image.py
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image
import io

def preprocess_ultrasound(file_bytes):
    """
    Takes raw file bytes from the API, resizes to 224x224, and normalizes.
    Returns a numpy array ready for the model.
    """
    try:
        # 1. Open the image directly from bytes (no need to save to disk first)
        img = Image.open(io.BytesIO(file_bytes))
        
        # 2. Convert to RGB. This prevents errors if a grayscale image is uploaded.
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # 3. Resize to 224x224 (The exact size your DenseNet expects)
        img = img.resize((224, 224))
        
        # 4. Convert to Numpy Array
        img_array = image.img_to_array(img)
        
        # 5. Add "Batch" Dimension: (224, 224, 3) -> (1, 224, 224, 3)
        img_array = np.expand_dims(img_array, axis=0)
        
        # 6. Normalize pixel values (0 to 255 -> 0 to 1)
        img_array = img_array / 255.0
        
        return img_array

    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return None
