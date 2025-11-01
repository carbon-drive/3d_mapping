#!/usr/bin/env python
"""
Simple script to run the 3D Mapping Service.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from mapping_service.app import create_app

if __name__ == "__main__":
    app = create_app()
    print("=" * 60)
    print("🗺️  3D Mapping Service")
    print("=" * 60)
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)
