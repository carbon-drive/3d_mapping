"""Tests for Flask application."""

import os
import json
import io
import pytest
from PIL import Image


class TestFlaskApp:
    """Test suite for Flask application."""

    def test_index_page_loads(self, client):
        """Test that the index page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"3D Mapping Service" in response.data

    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert data["service"] == "3d-mapping"
        assert "model_ready" in data

    def test_upload_no_files(self, client):
        """Test upload endpoint with no files."""
        response = client.post("/api/upload")
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert "error" in data

    def test_upload_empty_files(self, client):
        """Test upload endpoint with empty file list."""
        response = client.post(
            "/api/upload",
            data={"images": (io.BytesIO(b""), "")},
            content_type="multipart/form-data",
        )
        assert response.status_code == 400

    def test_upload_valid_image(self, client):
        """Test upload endpoint with a valid image."""
        # Create a test image
        img = Image.new("RGB", (100, 100), color=(255, 0, 0))
        img_io = io.BytesIO()
        img.save(img_io, "JPEG")
        img_io.seek(0)

        response = client.post(
            "/api/upload",
            data={"images": (img_io, "test.jpg")},
            content_type="multipart/form-data",
        )
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["num_images"] == 1
        assert "output_file" in data
        assert "download_url" in data

    def test_upload_multiple_images(self, client):
        """Test upload endpoint with multiple images."""
        images = []
        for i in range(3):
            img = Image.new("RGB", (100, 100), color=(i * 80, 0, 0))
            img_io = io.BytesIO()
            img.save(img_io, "JPEG")
            img_io.seek(0)
            images.append((img_io, f"test_{i}.jpg"))

        response = client.post(
            "/api/upload",
            data={"images": images},
            content_type="multipart/form-data",
        )
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["num_images"] == 3
        assert data["num_views_processed"] == 3

    def test_download_generated_model(self, client):
        """Test downloading a generated model."""
        # First upload and generate a model
        img = Image.new("RGB", (100, 100), color=(255, 0, 0))
        img_io = io.BytesIO()
        img.save(img_io, "JPEG")
        img_io.seek(0)

        upload_response = client.post(
            "/api/upload",
            data={"images": (img_io, "test.jpg")},
            content_type="multipart/form-data",
        )
        
        upload_data = json.loads(upload_response.data)
        download_url = upload_data["download_url"]

        # Now download the model
        download_response = client.get(download_url)
        assert download_response.status_code == 200
        assert b"# Mock 3D Model Output" in download_response.data

    def test_download_nonexistent_model(self, client):
        """Test downloading a non-existent model returns 404."""
        response = client.get("/api/download/nonexistent.obj")
        assert response.status_code == 404

    def test_app_config(self, app):
        """Test that app configuration is set correctly."""
        assert app.config["TESTING"] is True
        assert "UPLOAD_FOLDER" in app.config
        assert "OUTPUT_FOLDER" in app.config
        assert "MAX_CONTENT_LENGTH" in app.config
