"""Tests for ModelGenerator class."""

import os
import pytest
import numpy as np
from mapping_service.model_generator import ModelGenerator


class TestModelGenerator:
    """Test suite for ModelGenerator."""

    def test_init_creates_output_dir(self, temp_dir):
        """Test that initialization creates the output directory."""
        output_dir = os.path.join(temp_dir, "outputs")
        generator = ModelGenerator(output_dir=output_dir)
        assert os.path.exists(output_dir)

    def test_load_model_returns_true(self, temp_dir):
        """Test that load_model returns True on success."""
        generator = ModelGenerator(output_dir=temp_dir)
        assert generator.load_model() is True
        assert generator.model_loaded is True

    def test_is_ready_loads_model(self, temp_dir):
        """Test that is_ready loads the model if not loaded."""
        generator = ModelGenerator(output_dir=temp_dir)
        assert generator.model_loaded is False
        assert generator.is_ready() is True
        assert generator.model_loaded is True

    def test_generate_3d_model_with_valid_views(self, temp_dir):
        """Test 3D model generation with valid views."""
        generator = ModelGenerator(output_dir=temp_dir)
        
        # Create mock views
        views = [
            {"img": np.random.rand(100, 100, 3) * 255},
            {"img": np.random.rand(100, 100, 3) * 255},
        ]
        
        results = generator.generate_3d_model(views)
        
        assert results is not None
        assert results["status"] == "success"
        assert results["num_views"] == 2
        assert "output_path" in results
        assert os.path.exists(results["output_path"])

    def test_generate_3d_model_empty_views(self, temp_dir):
        """Test that generation fails with empty views."""
        generator = ModelGenerator(output_dir=temp_dir)
        results = generator.generate_3d_model([])
        assert results is None

    def test_generate_3d_model_creates_obj_file(self, temp_dir):
        """Test that a .obj file is created."""
        generator = ModelGenerator(output_dir=temp_dir)
        
        views = [{"img": np.random.rand(50, 50, 3) * 255}]
        results = generator.generate_3d_model(views, output_name="test_model.obj")
        
        assert results is not None
        output_path = results["output_path"]
        assert output_path.endswith(".obj")
        assert os.path.exists(output_path)
        
        # Check file content
        with open(output_path, "r") as f:
            content = f.read()
            assert "# Mock 3D Model Output" in content
            assert "v " in content  # Vertices
            assert "f " in content  # Faces

    def test_generate_mock_depth_maps(self, temp_dir):
        """Test generation of mock depth maps."""
        generator = ModelGenerator(output_dir=temp_dir)
        
        views = [
            {"img": np.zeros((50, 50, 3))},
            {"img": np.zeros((100, 100, 3))},
        ]
        
        depth_maps = generator._generate_mock_depth_maps(views)
        
        assert len(depth_maps) == 2
        assert depth_maps[0].shape == (50, 50)
        assert depth_maps[1].shape == (100, 100)
        assert isinstance(depth_maps[0], np.ndarray)

    def test_generate_mock_camera_poses(self, temp_dir):
        """Test generation of mock camera poses."""
        generator = ModelGenerator(output_dir=temp_dir)
        
        poses = generator._generate_mock_camera_poses(3)
        
        assert len(poses) == 3
        for i, pose in enumerate(poses):
            assert pose.shape == (4, 4)
            assert np.allclose(pose[:3, :3], np.eye(3))  # Rotation is identity
            assert pose[0, 3] == i * 0.1  # Translation in x

    def test_generate_3d_model_includes_metadata(self, temp_dir):
        """Test that results include all expected metadata."""
        generator = ModelGenerator(output_dir=temp_dir)
        
        views = [{"img": np.random.rand(80, 80, 3) * 255}]
        results = generator.generate_3d_model(views)
        
        assert "status" in results
        assert "num_views" in results
        assert "output_path" in results
        assert "depth_maps" in results
        assert "camera_poses" in results
        assert "metric_scale" in results
        assert results["metric_scale"] == 1.0
