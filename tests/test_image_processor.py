"""Tests for ImageProcessor class."""

import os
import pytest
from PIL import Image
import numpy as np
from mapping_service.image_processor import ImageProcessor


class TestImageProcessor:
    """Test suite for ImageProcessor."""

    def test_init_creates_upload_dir(self, temp_dir):
        """Test that initialization creates the upload directory."""
        upload_dir = os.path.join(temp_dir, "uploads")
        processor = ImageProcessor(upload_dir)
        assert os.path.exists(upload_dir)

    def test_validate_image_valid(self, sample_image_path):
        """Test validation of a valid image."""
        processor = ImageProcessor()
        assert processor.validate_image(sample_image_path) is True

    def test_validate_image_invalid_format(self, temp_dir):
        """Test validation rejects invalid file format."""
        invalid_path = os.path.join(temp_dir, "test.txt")
        with open(invalid_path, "w") as f:
            f.write("Not an image")
        
        processor = ImageProcessor()
        assert processor.validate_image(invalid_path) is False

    def test_validate_image_nonexistent(self):
        """Test validation of non-existent file."""
        processor = ImageProcessor()
        assert processor.validate_image("nonexistent.jpg") is False

    def test_load_image_returns_numpy_array(self, sample_image_path):
        """Test that load_image returns a numpy array."""
        processor = ImageProcessor()
        img_array = processor.load_image(sample_image_path)
        
        assert img_array is not None
        assert isinstance(img_array, np.ndarray)
        assert img_array.shape == (100, 100, 3)

    def test_load_image_converts_to_rgb(self, temp_dir):
        """Test that images are converted to RGB."""
        # Create a grayscale image
        gray_path = os.path.join(temp_dir, "gray.png")
        img = Image.new("L", (50, 50), color=128)
        img.save(gray_path)
        
        processor = ImageProcessor()
        img_array = processor.load_image(gray_path)
        
        assert img_array is not None
        assert img_array.shape == (50, 50, 3)

    def test_preprocess_images_valid(self, sample_images):
        """Test preprocessing of valid images."""
        processor = ImageProcessor()
        views = processor.preprocess_images(sample_images)
        
        assert len(views) == 3
        for view in views:
            assert "img" in view
            assert "file_path" in view
            assert isinstance(view["img"], np.ndarray)

    def test_preprocess_images_filters_invalid(self, sample_images, temp_dir):
        """Test that preprocessing filters out invalid images."""
        # Add an invalid file
        invalid_path = os.path.join(temp_dir, "invalid.txt")
        with open(invalid_path, "w") as f:
            f.write("Not an image")
        
        all_paths = sample_images + [invalid_path]
        
        processor = ImageProcessor()
        views = processor.preprocess_images(all_paths)
        
        # Should only process valid images
        assert len(views) == 3

    def test_save_uploaded_file(self, temp_dir):
        """Test saving an uploaded file."""
        upload_dir = os.path.join(temp_dir, "uploads")
        processor = ImageProcessor(upload_dir)
        
        test_data = b"test image data"
        filename = "test_upload.jpg"
        
        saved_path = processor.save_uploaded_file(test_data, filename)
        
        assert os.path.exists(saved_path)
        with open(saved_path, "rb") as f:
            assert f.read() == test_data

    def test_save_uploaded_file_sanitizes_filename(self, temp_dir):
        """Test that filenames are sanitized for security."""
        upload_dir = os.path.join(temp_dir, "uploads")
        processor = ImageProcessor(upload_dir)
        
        # Try a filename with path traversal
        dangerous_filename = "../../../etc/passwd"
        test_data = b"test data"
        
        saved_path = processor.save_uploaded_file(test_data, dangerous_filename)
        
        # Should be saved in the upload directory only
        assert upload_dir in saved_path
        assert os.path.dirname(saved_path) == upload_dir
