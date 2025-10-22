# Documentation Generation - Quick Reference

## Quick Start Commands

### Python Script (Cross-Platform)
```bash
# Install dependencies and generate all docs
python generate_docs.py --install --all

# Generate mkdocs only
python generate_docs.py --mkdocs

# Serve mkdocs locally
python generate_docs.py --mkdocs --serve
```

### Bash Script (Linux/macOS)
```bash
# Make executable (first time only)
chmod +x generate_docs.sh

# Install and generate mkdocs
./generate_docs.sh --install --mkdocs

# Serve mkdocs locally
./generate_docs.sh --mkdocs --serve

# Clean all generated docs
./generate_docs.sh --clean
```

### PowerShell Script (Windows)
```powershell
# Install and generate mkdocs
.\generate_docs.ps1 -Install -Mkdocs

# Serve mkdocs locally
.\generate_docs.ps1 -Mkdocs -Serve

# Clean all generated docs
.\generate_docs.ps1 -Clean
```

## Manual Commands

### pdoc
```bash
# Set environment
export IS_PRODUCTION=false
export DATABASE_URL=sqlite:///./storage/lengkeng.db

# Generate docs
python -m pdoc --output-directory docs/html/pdoc mod config main
```

### mkdocs
```bash
# Build static site
mkdocs build

# Serve locally
mkdocs serve
```

### Sphinx
```bash
# First-time setup
sphinx-quickstart docs

# Generate HTML
sphinx-build -b html docs docs/_build
```

## Output Locations

- **pdoc**: `docs/html/pdoc/index.html`
- **mkdocs**: `site/index.html`
- **Sphinx**: `docs/_build/index.html`

## Viewing Documentation

### Open in Browser (Linux/macOS)
```bash
# pdoc
xdg-open docs/html/pdoc/index.html

# mkdocs
xdg-open site/index.html

# Sphinx
xdg-open docs/_build/index.html
```

### Open in Browser (Windows)
```powershell
# pdoc
Start-Process docs/html/pdoc/index.html

# mkdocs
Start-Process site/index.html

# Sphinx
Start-Process docs/_build/index.html
```

## Troubleshooting

### Database Configuration Error
If you see: `ValueError: SQLite database is not allowed in production environment`

**Solution:**
```bash
# Linux/macOS
export IS_PRODUCTION=false

# Windows CMD
set IS_PRODUCTION=false

# Windows PowerShell
$env:IS_PRODUCTION="false"
```

### Import Errors
```bash
# Install project dependencies
pip install -r requirements.txt

# Install doc dependencies
python generate_docs.py --install
```

### Permission Denied (Linux/macOS)
```bash
chmod +x generate_docs.sh
chmod +x generate_docs.py
```

## CI/CD Integration

See `.github/workflows/documentation.yml` for GitHub Actions example.

## More Information

See [DOCUMENTATION.md](DOCUMENTATION.md) for comprehensive documentation guide.
