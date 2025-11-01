# Copilot Instructions for 3d_mapping

## Repository Overview

This repository contains a complete workflow for creating 3D models from images using Meta's MapAnything technology. The project focuses on AI-powered zero-shot 3D reconstruction, enabling users to generate 3D models without prior training on specific objects or scenes.

## Project Context

- **Primary Technology**: Meta's MapAnything for 3D reconstruction
- **Language**: Python
- **Purpose**: Tutorial and workflow for converting 2D images to 3D models
- **Target Audience**: Developers and researchers interested in AI-powered 3D reconstruction

## Code Style and Conventions

### Python Guidelines
- Follow PEP 8 style guidelines
- Use type hints where appropriate for function signatures
- Write clear, descriptive docstrings for all functions and classes
- Keep functions focused and single-purpose
- Use meaningful variable names that describe their purpose

### File Organization
- Keep code modular and organized by functionality
- Separate utility functions from main workflow code
- Use appropriate subdirectories for different components (e.g., `models/`, `utils/`, `scripts/`)

## Development Workflow

### Setting Up Development Environment
- Use Python virtual environments (`venv` or `conda`)
- Document all required dependencies in `requirements.txt`
- Include version specifications for critical dependencies
- Consider creating a `setup.py` or `pyproject.toml` for package installation

### Testing
- Write unit tests for core functionality
- Use `pytest` as the testing framework (if tests are added)
- Aim for meaningful test coverage of critical functions
- Include integration tests for the complete 3D reconstruction workflow

### Code Quality
- Run linters (e.g., `flake8`, `pylint`) before committing
- Use formatters like `black` for consistent code formatting
- Ensure code passes type checking with `mypy` if type hints are used

## 3D Reconstruction Workflow

### Key Components
1. **Image Input**: Accept various image formats (JPEG, PNG, etc.)
2. **Preprocessing**: Image preparation and validation
3. **MapAnything Integration**: Interface with Meta's MapAnything API/library
4. **3D Model Generation**: Process output and generate 3D models
5. **Export**: Save models in standard formats (e.g., OBJ, PLY, GLTF)

### Performance Considerations
- Optimize for memory usage when processing large images
- Consider batch processing capabilities for multiple images
- Implement proper error handling for API failures or invalid inputs
- Add progress indicators for long-running operations

## Dependencies and External Services

### Meta's MapAnything
- Document authentication requirements if applicable
- Include API rate limits and usage guidelines
- Provide fallback options if the service is unavailable
- Keep track of API version compatibility

### Common Python Libraries
- `numpy` for numerical operations
- `PIL/Pillow` for image processing
- `torch/tensorflow` if deep learning models are used locally
- `trimesh` or similar for 3D mesh operations

## Documentation

### Code Documentation
- Add inline comments for complex algorithms or non-obvious logic
- Document all public APIs thoroughly
- Include usage examples in docstrings
- Keep README.md up-to-date with installation and usage instructions

### Tutorial Content
- Provide step-by-step guides for users
- Include example images and expected outputs
- Document common issues and troubleshooting steps
- Add links to relevant papers and resources

## Error Handling

- Use try-except blocks for external API calls
- Provide informative error messages to users
- Log errors appropriately for debugging
- Validate inputs before processing

## Security Considerations

- Never commit API keys or credentials to the repository
- Use environment variables for sensitive configuration
- Validate and sanitize user inputs (especially file paths)
- Be cautious with file uploads and processing

## Contribution Guidelines

### Before Submitting Changes
- Test the complete workflow end-to-end
- Update documentation if adding new features
- Ensure code follows the style guidelines
- Add or update tests as appropriate

### Pull Request Best Practices
- Provide clear descriptions of changes
- Reference related issues
- Include before/after examples for visual changes
- Keep PRs focused on a single feature or fix

## Specific Guidance for Copilot

### When Adding New Features
- Prioritize code clarity and maintainability
- Consider backward compatibility
- Add appropriate error handling
- Update relevant documentation

### When Fixing Bugs
- Include a test case that reproduces the bug
- Explain the root cause in comments or PR description
- Verify the fix doesn't introduce regressions

### When Refactoring
- Preserve existing functionality
- Improve code organization and readability
- Add tests if coverage is lacking
- Document significant architectural changes

## Resources

- Meta's MapAnything Documentation - *Link to be added when available; check Meta AI research publications*
- [Python Best Practices](https://docs.python-guide.org/)
- [3D Model Formats](https://en.wikipedia.org/wiki/List_of_file_formats#3D_graphics)
- [3D Reconstruction Overview](https://en.wikipedia.org/wiki/3D_reconstruction)

## Notes for Copilot Agent

- This is primarily a tutorial/workflow repository focusing on demonstration and education
- Prioritize code clarity and educational value over extreme optimization
- Ensure examples are easy to follow and well-commented
- Consider users who may be new to 3D reconstruction or AI
- When in doubt, add documentation rather than assume knowledge
