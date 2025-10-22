# Documentation Generation Guide

This guide explains how to generate HTML documentation for the VTS API project using different tools.

## Overview

The project supports multiple documentation generation tools:

1. **pdoc** - Simple, clean HTML documentation from docstrings
2. **mkdocs** - Beautiful static site with navigation and search
3. **Sphinx** - Comprehensive documentation with advanced features

## Quick Start

### Install Documentation Dependencies

```bash
# Install all documentation tools
python generate_docs.py --install
```

Or install manually:

```bash
pip install pdoc mkdocs mkdocs-material mkdocstrings[python] sphinx sphinx-rtd-theme
```

### Generate All Documentation

```bash
python generate_docs.py --all
```

## Tool-Specific Generation

### Using pdoc

Generate simple HTML documentation directly from Python docstrings:

```bash
# Generate pdoc documentation
python generate_docs.py --pdoc

# Output: docs/html/pdoc/
# Open: docs/html/pdoc/index.html
```

**Features:**
- Simple, clean HTML output
- Automatically extracts docstrings
- No configuration needed
- Great for quick API reference

### Using mkdocs

Generate a beautiful static site with navigation and search:

```bash
# Build static site
python generate_docs.py --mkdocs

# Output: site/
# Open: site/index.html

# Or serve locally for development
python generate_docs.py --mkdocs --serve
# Visit: http://127.0.0.1:8000
```

**Features:**
- Beautiful Material Design theme
- Full-text search
- Navigation menu
- Mobile-responsive
- Markdown-based content
- Auto-extracts Python docstrings

**Configuration:** Edit `mkdocs.yml` to customize.

### Using Sphinx

Generate comprehensive documentation with advanced features:

```bash
# First time setup (one-time only)
sphinx-quickstart docs

# Generate documentation
python generate_docs.py --sphinx

# Output: docs/_build/
# Open: docs/_build/index.html
```

**Features:**
- Most comprehensive documentation system
- Cross-references and indexes
- Multiple output formats (HTML, PDF, ePub)
- Extensive plugin ecosystem
- Used by major Python projects

**Configuration:** Edit `docs/conf.py` to customize.

## Automated Generation Script

The `generate_docs.py` script handles environment setup automatically to bypass database configuration issues during documentation generation.

### Usage Examples

```bash
# Show help
python generate_docs.py --help

# Generate all documentation
python generate_docs.py --all

# Generate only pdoc docs
python generate_docs.py --pdoc

# Generate mkdocs and serve locally
python generate_docs.py --mkdocs --serve

# Install dependencies and generate all
python generate_docs.py --install --all
```

## Manual Generation

If you prefer manual control:

### pdoc Manual

```bash
# Set environment to bypass database checks
export IS_PRODUCTION=false
export DATABASE_URL=sqlite:///./storage/lengkeng.db

# Generate documentation
python -m pdoc --html --output-dir docs/html/pdoc --force mod config main
```

### mkdocs Manual

```bash
# Set environment
export IS_PRODUCTION=false
export DATABASE_URL=sqlite:///./storage/lengkeng.db

# Build documentation
mkdocs build

# Or serve locally
mkdocs serve
```

### Sphinx Manual

```bash
# Set environment
export IS_PRODUCTION=false
export DATABASE_URL=sqlite:///./storage/lengkeng.db

# Generate HTML
sphinx-build -b html docs docs/_build
```

## Troubleshooting

### Database Configuration Error

If you see an error about database configuration:

```
ValueError: SQLite database is not allowed in production environment
```

**Solution:** Use the `generate_docs.py` script which automatically sets `IS_PRODUCTION=false`, or set it manually:

```bash
export IS_PRODUCTION=false  # Linux/macOS
set IS_PRODUCTION=false     # Windows CMD
$env:IS_PRODUCTION="false"  # Windows PowerShell
```

### Import Errors

If documentation generation fails with import errors:

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check that you're in the project root directory
3. Verify Python path includes the project directory

### Missing Documentation

If some modules don't appear in the documentation:

1. Ensure modules have docstrings
2. Check that modules are imported correctly
3. Verify `__init__.py` files exist in all packages
4. Review the tool's configuration file

## Writing Good Docstrings

The documentation tools extract information from your docstrings. Follow these guidelines:

### Google-Style Docstrings (Recommended)

```python
def create_user(db: Session, user: UserCreateDTO) -> UserResponseDTO:
    """
    Create a new user with validation.
    
    This method handles the complete user creation process including
    validation and password hashing.
    
    Args:
        db (Session): SQLAlchemy database session
        user (UserCreateDTO): User data to create
    
    Returns:
        UserResponseDTO: Created user information
    
    Raises:
        HTTPException: 400 if email already registered
        HTTPException: 400 if username already taken
    
    Example:
        >>> user_data = UserCreateDTO(username="john", email="john@example.com")
        >>> new_user = create_user(db, user_data)
    """
    # Implementation
```

### NumPy-Style Docstrings

```python
def update_user(db, user_id, user_update):
    """
    Update an existing user's information.
    
    Parameters
    ----------
    db : Session
        SQLAlchemy database session
    user_id : int
        The unique identifier of the user
    user_update : UserUpdateDTO
        Fields to update
    
    Returns
    -------
    UserResponseDTO
        Updated user information
    
    Raises
    ------
    HTTPException
        404 if user not found
    """
    # Implementation
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Generate Documentation

on:
  push:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python generate_docs.py --install
      - name: Generate documentation
        run: python generate_docs.py --mkdocs
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

## Comparing Documentation Tools

| Feature | pdoc | mkdocs | Sphinx |
|---------|------|---------|--------|
| Ease of Setup | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Output Quality | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Customization | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Learning Curve | ⭐ | ⭐⭐ | ⭐⭐⭐ |
| API Docs | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Search | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Theming | ⭐ | ⭐⭐⭐ | ⭐⭐ |

### Recommendations

- **Quick API Reference**: Use **pdoc**
- **Beautiful Website**: Use **mkdocs**
- **Comprehensive Docs**: Use **Sphinx**
- **Best Overall**: Use **mkdocs** with mkdocstrings

## Additional Resources

- [pdoc Documentation](https://pdoc.dev/)
- [mkdocs Documentation](https://www.mkdocs.org/)
- [mkdocstrings Plugin](https://mkdocstrings.github.io/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Google Style Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
