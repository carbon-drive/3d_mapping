"""Pytest configuration and fixtures."""

import os
import pytest
import tempfile
import shutil
from PIL import Image
import numpy as np


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_image_path(temp_dir):
    """Create a sample image for testing."""
    img_path = os.path.join(temp_dir, "test_image.jpg")
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    img.save(img_path)
    return img_path


@pytest.fixture
def sample_images(temp_dir):
    """Create multiple sample images for testing."""
    images = []
    for i in range(3):
        img_path = os.path.join(temp_dir, f"test_image_{i}.jpg")
        img = Image.new("RGB", (100, 100), color=(i * 80, 0, 0))
        img.save(img_path)
        images.append(img_path)
    return images


@pytest.fixture
def app():
    """Create a Flask app for testing."""
    from mapping_service.app import create_app
    
    temp_dir = tempfile.mkdtemp()
    
    app = create_app({
        "TESTING": True,
        "UPLOAD_FOLDER": os.path.join(temp_dir, "uploads"),
        "OUTPUT_FOLDER": os.path.join(temp_dir, "outputs"),
    })
    
    yield app
    
    shutil.rmtree(temp_dir)


@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()
