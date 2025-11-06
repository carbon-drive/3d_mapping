# Usage Guide

This guide will help you get started with the 3D Mapping Service.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Docker and Docker Compose for containerized deployment

### Option 1: Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/carbon-drive/3d_mapping.git
   cd 3d_mapping
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Run the application:**
   ```bash
   # Development mode with debug enabled
   FLASK_DEBUG=1 python run.py
   
   # Production mode (debug disabled)
   python run.py
   ```

5. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

### Option 2: Docker Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/carbon-drive/3d_mapping.git
   cd 3d_mapping
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

## Using the Web Interface

1. **Open the application** in your browser at `http://localhost:5000`

2. **Select images:**
   - Click "Choose images..." button
   - Select one or more images from your computer
   - Supported formats: JPG, JPEG, PNG, BMP, TIFF
   - Maximum file size: 10MB per image

3. **Generate 3D model:**
   - Click "Generate 3D Model" button
   - Wait for processing to complete
   - The system will process your images and create a 3D reconstruction

4. **Download result:**
   - Once complete, click "Download 3D Model" button
   - Save the .obj file to your computer
   - You can view this file in 3D modeling software like Blender, MeshLab, or online viewers

## Using the API

### Health Check

Check if the service is running:

```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "service": "3d-mapping",
  "model_ready": true
}
```

### Upload Images

Upload images to generate a 3D model:

```bash
curl -X POST http://localhost:5000/api/upload \
  -F "images=@/path/to/image1.jpg" \
  -F "images=@/path/to/image2.jpg"
```

Response:
```json
{
  "status": "success",
  "num_images": 2,
  "num_views_processed": 2,
  "output_file": "model_output.obj",
  "download_url": "/api/download/model_output.obj"
}
```

### Download Model

Download the generated 3D model:

```bash
curl -O http://localhost:5000/api/download/model_output.obj
```

## Python API Usage

You can also use the components directly in your Python code:

```python
from mapping_service.image_processor import ImageProcessor
from mapping_service.model_generator import ModelGenerator

# Initialize components
processor = ImageProcessor(upload_dir="my_uploads")
generator = ModelGenerator(output_dir="my_outputs")

# Process images
image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
views = processor.preprocess_images(image_paths)

# Generate 3D model
results = generator.generate_3d_model(views, output_name="my_model.obj")

if results:
    print(f"Success! Model saved to: {results['output_path']}")
    print(f"Processed {results['num_views']} views")
else:
    print("Failed to generate model")
```

## Development

### Running Tests

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src/mapping_service --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

### Code Quality

Format code:
```bash
black src/ tests/
```

Check style:
```bash
flake8 src/ tests/
```

Type checking:
```bash
mypy src/
```

## Integrating Real MapAnything

This implementation uses a mock version of MapAnything. To use the real model:

1. **Install MapAnything:**
   ```bash
   git clone https://github.com/facebookresearch/map-anything.git
   cd map-anything
   conda create -n mapanything python=3.12 -y
   conda activate mapanything
   pip install -e .
   ```

2. **Update model_generator.py:**
   
   Replace the mock implementation in the `load_model()` method:
   
   ```python
   def load_model(self) -> bool:
       try:
           from mapanything import MapAnything
           self.model = MapAnything.from_pretrained(self.model_id)
           self.model_loaded = True
           return True
       except Exception as e:
           logger.error(f"Error loading model: {e}")
           return False
   ```
   
   Replace the mock implementation in `generate_3d_model()`:
   
   ```python
   def generate_3d_model(self, views, output_name=None):
       if not self.model_loaded:
           if not self.load_model():
               return None
       
       try:
           # Real MapAnything inference
           results = self.model.infer(views)
           
           # Process and save results
           # ... (implementation depends on MapAnything output format)
           
           return results
       except Exception as e:
           logger.error(f"Error generating 3D model: {e}")
           return None
   ```

## Troubleshooting

### Port already in use

If port 5000 is already in use, you can change it:

```python
# In run.py or app.py
app.run(host="0.0.0.0", port=8080, debug=debug_mode)
```

### Out of memory

If processing large images causes memory issues:

1. Reduce image size before upload
2. Process fewer images at once
3. Increase system memory allocation for Docker

### Import errors

Make sure you've installed the package:
```bash
pip install -e .
```

And set PYTHONPATH if running directly:
```bash
export PYTHONPATH=/path/to/3d_mapping/src:$PYTHONPATH
```

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the README.md for more information
- Review the test files for usage examples
