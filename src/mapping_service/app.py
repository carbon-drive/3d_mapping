"""
Flask web application for 3D mapping service.
"""

import os
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from .image_processor import ImageProcessor
from .model_generator import ModelGenerator


def create_app(config=None):
    """
    Create and configure the Flask application.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured Flask app
    """
    # Determine the correct template and static folders
    # Get the root directory (3 levels up from this file: app.py -> mapping_service -> src -> root)
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    template_folder = os.path.join(root_dir, "templates")
    static_folder = os.path.join(root_dir, "static")
    
    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder,
    )

    # Default configuration
    app.config.update(
        {
            "UPLOAD_FOLDER": "uploads",
            "OUTPUT_FOLDER": "outputs",
            "MAX_CONTENT_LENGTH": 50 * 1024 * 1024,  # 50MB max request size
        }
    )

    # Override with provided config
    if config:
        app.config.update(config)

    # Initialize services
    image_processor = ImageProcessor(upload_dir=app.config["UPLOAD_FOLDER"])
    model_generator = ModelGenerator(output_dir=app.config["OUTPUT_FOLDER"])

    @app.route("/")
    def index():
        """Render the main page."""
        return render_template("index.html")

    @app.route("/api/health")
    def health():
        """Health check endpoint."""
        return jsonify(
            {
                "status": "healthy",
                "service": "3d-mapping",
                "model_ready": model_generator.is_ready(),
            }
        )

    @app.route("/api/upload", methods=["POST"])
    def upload_images():
        """
        Handle image upload and 3D model generation.

        Returns:
            JSON response with generation results
        """
        if "images" not in request.files:
            return jsonify({"error": "No images provided"}), 400

        files = request.files.getlist("images")
        if not files or all(f.filename == "" for f in files):
            return jsonify({"error": "No selected files"}), 400

        # Save uploaded files
        file_paths = []
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = image_processor.save_uploaded_file(
                    file.read(), filename
                )
                file_paths.append(file_path)

        if not file_paths:
            return jsonify({"error": "No valid images uploaded"}), 400

        # Preprocess images
        views = image_processor.preprocess_images(file_paths)
        if not views:
            return jsonify({"error": "Failed to process images"}), 400

        # Generate 3D model
        results = model_generator.generate_3d_model(views)
        if results is None:
            return jsonify({"error": "Failed to generate 3D model"}), 500

        # Return results
        return jsonify(
            {
                "status": "success",
                "num_images": len(file_paths),
                "num_views_processed": results["num_views"],
                "output_file": os.path.basename(results["output_path"]),
                "download_url": f"/api/download/{os.path.basename(results['output_path'])}",
            }
        )

    @app.route("/api/download/<filename>")
    def download_model(filename):
        """
        Download a generated 3D model.

        Args:
            filename: Name of the file to download

        Returns:
            File download response
        """
        return send_from_directory(
            app.config["OUTPUT_FOLDER"],
            filename,
            as_attachment=True,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
