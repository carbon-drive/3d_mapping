# 🗺️ 3D Mapping Service

The complete workflow for creating 3D models from any image using Meta's MapAnything. This Python application provides an easy-to-use web interface for AI-powered zero-shot 3D reconstruction.

## Features

- 🖼️ **Easy Image Upload**: Web-based interface for uploading single or multiple images
- 🤖 **AI-Powered**: Uses Meta's MapAnything for advanced 3D reconstruction
- 🎯 **Zero-Shot**: No training required, works with any images
- 📦 **Containerized**: Docker support for easy deployment
- 🧪 **Well-Tested**: Comprehensive test suite following TDD principles
- 🏗️ **Modular Architecture**: Clean separation of concerns for maintainability

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip
- (Optional) Docker and Docker Compose

### Installation

1. Clone the repository:
```bash
git clone https://github.com/carbon-drive/3d_mapping.git
cd 3d_mapping
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

### Running the Application

#### Option 1: Python Script
```bash
python run.py
```

#### Option 2: Docker
```bash
docker-compose up
```

The application will be available at `http://localhost:5000`

## Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Click "Choose images..." to select one or more images
3. Click "Generate 3D Model" to start the reconstruction process
4. Once complete, download your 3D model (.obj file)

## Architecture

The application follows a microservice-inspired architecture with clear separation of concerns:

### Components

- **Image Processor** (`image_processor.py`): Handles image validation, loading, and preprocessing
- **Model Generator** (`model_generator.py`): Manages 3D model generation using MapAnything
- **Web Application** (`app.py`): Flask-based REST API and web interface
- **Frontend**: HTML/CSS/JavaScript interface for user interaction

### API Endpoints

- `GET /` - Main web interface
- `GET /api/health` - Health check endpoint
- `POST /api/upload` - Upload images and generate 3D model
- `GET /api/download/<filename>` - Download generated model

## Development

### Running Tests

The project includes comprehensive unit tests following TDD principles:

```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src/mapping_service --cov-report=html
```

### Code Quality

Format code with Black:
```bash
black src/ tests/
```

Check code style:
```bash
flake8 src/ tests/
```

Type checking:
```bash
mypy src/
```

## Project Structure

```
3d_mapping/
├── src/
│   └── mapping_service/
│       ├── __init__.py
│       ├── app.py              # Flask application
│       ├── image_processor.py  # Image handling
│       └── model_generator.py  # 3D model generation
├── tests/
│   ├── conftest.py            # Test fixtures
│   ├── test_app.py            # App tests
│   ├── test_image_processor.py
│   └── test_model_generator.py
├── templates/
│   └── index.html             # Web interface
├── static/
│   ├── style.css              # Styling
│   └── script.js              # Frontend logic
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
└── README.md                  # This file
```

## Technology Stack

- **Backend**: Python 3.12, Flask
- **AI/ML**: PyTorch, Meta's MapAnything (mock implementation)
- **Testing**: pytest, pytest-cov
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Containerization**: Docker, Docker Compose

## Note on MapAnything Integration

This implementation includes a mock version of MapAnything for demonstration purposes. To integrate with the actual MapAnything model:

1. Install MapAnything:
```bash
git clone https://github.com/facebookresearch/map-anything.git
cd map-anything
pip install -e .
```

2. Update `model_generator.py` to use the real MapAnything API:
```python
from mapanything import MapAnything
self.model = MapAnything.from_pretrained("facebook/map-anything")
results = self.model.infer(views)
```

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass
2. Code is formatted with Black
3. New features include tests
4. Documentation is updated

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
