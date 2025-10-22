# Documentation Generation Script for VTS API (Windows PowerShell)
# This script provides easy access to documentation generation tools

param(
    [switch]$All,
    [switch]$Pdoc,
    [switch]$Mkdocs,
    [switch]$Sphinx,
    [switch]$Serve,
    [switch]$Install,
    [switch]$Clean,
    [switch]$Help
)

function Show-Help {
    Write-Host @"
VTS API Documentation Generator

Usage: .\generate_docs.ps1 [OPTIONS]

Options:
  -All         Generate all documentation types
  -Pdoc        Generate pdoc documentation
  -Mkdocs      Generate mkdocs documentation
  -Sphinx      Generate Sphinx documentation
  -Serve       Serve mkdocs documentation locally (use with -Mkdocs)
  -Install     Install documentation dependencies
  -Clean       Clean all generated documentation
  -Help        Show this help message

Examples:
  .\generate_docs.ps1 -Install -Mkdocs
  .\generate_docs.ps1 -Mkdocs -Serve
  .\generate_docs.ps1 -All

"@
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

# Show help if no parameters or Help flag
if ($Help -or ($PSBoundParameters.Count -eq 0)) {
    Show-Help
    exit 0
}

# Clean documentation
if ($Clean) {
    Write-Info "Cleaning generated documentation..."
    if (Test-Path "docs/html") { Remove-Item -Recurse -Force "docs/html" }
    if (Test-Path "site") { Remove-Item -Recurse -Force "site" }
    if (Test-Path "docs/_build") { Remove-Item -Recurse -Force "docs/_build" }
    Write-Success "Documentation cleaned"
    exit 0
}

# Install dependencies
if ($Install) {
    Write-Info "Installing documentation dependencies..."
    python -m pip install -q pdoc mkdocs mkdocs-material 'mkdocstrings[python]' sphinx sphinx-rtd-theme
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Dependencies installed"
    } else {
        Write-Error "Failed to install dependencies"
        exit 1
    }
}

# Set environment for documentation generation
$env:IS_PRODUCTION = "false"
$env:DATABASE_URL = "sqlite:///./storage/lengkeng.db"
Write-Success "Environment configured for documentation generation"

# Determine what to generate
$GeneratePdoc = $All -or $Pdoc
$GenerateMkdocs = $All -or $Mkdocs
$GenerateSphinx = $All -or $Sphinx

# Generate pdoc documentation
if ($GeneratePdoc) {
    Write-Host ""
    Write-Info "Generating pdoc documentation..."
    New-Item -ItemType Directory -Force -Path "docs/html/pdoc" | Out-Null
    python -m pdoc --output-directory docs/html/pdoc mod config main
    if ($LASTEXITCODE -eq 0) {
        Write-Success "pdoc documentation generated in docs/html/pdoc/"
        Write-Host "  Open: docs/html/pdoc/index.html"
    } else {
        Write-Error "Failed to generate pdoc documentation"
    }
}

# Generate mkdocs documentation
if ($GenerateMkdocs) {
    Write-Host ""
    Write-Info "Generating mkdocs documentation..."
    if ($Serve) {
        Write-Success "Starting mkdocs development server..."
        Write-Host "Documentation will be available at http://127.0.0.1:8000"
        mkdocs serve
    } else {
        mkdocs build
        if ($LASTEXITCODE -eq 0) {
            Write-Success "mkdocs documentation generated in site/"
            Write-Host "  Open: site/index.html"
        } else {
            Write-Error "Failed to generate mkdocs documentation"
        }
    }
}

# Generate Sphinx documentation
if ($GenerateSphinx) {
    Write-Host ""
    Write-Info "Generating Sphinx documentation..."
    if (-not (Test-Path "docs")) {
        Write-Error "Sphinx docs directory not found. Run 'sphinx-quickstart docs' first."
        exit 1
    }
    sphinx-build -b html docs docs/_build
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Sphinx documentation generated in docs/_build/"
        Write-Host "  Open: docs/_build/index.html"
    } else {
        Write-Error "Failed to generate Sphinx documentation"
    }
}

Write-Host ""
Write-Success "Documentation generation completed successfully!"
