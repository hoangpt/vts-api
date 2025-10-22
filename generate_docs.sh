#!/bin/bash
# Documentation Generation Script for VTS API
# This script provides easy access to documentation generation tools

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

show_help() {
    cat << EOF
VTS API Documentation Generator

Usage: ./generate_docs.sh [OPTION]

Options:
  --all         Generate all documentation types
  --pdoc        Generate pdoc documentation
  --mkdocs      Generate mkdocs documentation
  --sphinx      Generate Sphinx documentation
  --serve       Serve mkdocs documentation locally (use with --mkdocs)
  --install     Install documentation dependencies
  --clean       Clean all generated documentation
  --help        Show this help message

Examples:
  ./generate_docs.sh --install --mkdocs
  ./generate_docs.sh --mkdocs --serve
  ./generate_docs.sh --all

EOF
}

# Default values
DO_INSTALL=false
DO_PDOC=false
DO_MKDOCS=false
DO_SPHINX=false
DO_SERVE=false
DO_CLEAN=false

# Parse arguments
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            DO_PDOC=true
            DO_MKDOCS=true
            DO_SPHINX=true
            shift
            ;;
        --pdoc)
            DO_PDOC=true
            shift
            ;;
        --mkdocs)
            DO_MKDOCS=true
            shift
            ;;
        --sphinx)
            DO_SPHINX=true
            shift
            ;;
        --serve)
            DO_SERVE=true
            shift
            ;;
        --install)
            DO_INSTALL=true
            shift
            ;;
        --clean)
            DO_CLEAN=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Clean documentation
if [ "$DO_CLEAN" = true ]; then
    echo -e "${YELLOW}Cleaning generated documentation...${NC}"
    rm -rf docs/html/ site/ docs/_build/
    echo -e "${GREEN}✓ Documentation cleaned${NC}"
    exit 0
fi

# Install dependencies
if [ "$DO_INSTALL" = true ]; then
    echo -e "${YELLOW}Installing documentation dependencies...${NC}"
    pip install -q pdoc mkdocs mkdocs-material 'mkdocstrings[python]' sphinx sphinx-rtd-theme
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi

# Set environment for documentation generation
export IS_PRODUCTION=false
export DATABASE_URL=sqlite:///./storage/lengkeng.db
echo -e "${GREEN}✓ Environment configured for documentation generation${NC}"

# Generate pdoc documentation
if [ "$DO_PDOC" = true ]; then
    echo -e "\n${YELLOW}Generating pdoc documentation...${NC}"
    mkdir -p docs/html/pdoc
    python -m pdoc --output-directory docs/html/pdoc mod config main
    echo -e "${GREEN}✓ pdoc documentation generated in docs/html/pdoc/${NC}"
    echo -e "  Open: docs/html/pdoc/index.html"
fi

# Generate mkdocs documentation
if [ "$DO_MKDOCS" = true ]; then
    echo -e "\n${YELLOW}Generating mkdocs documentation...${NC}"
    if [ "$DO_SERVE" = true ]; then
        echo -e "${GREEN}Starting mkdocs development server...${NC}"
        echo -e "Documentation will be available at http://127.0.0.1:8000"
        mkdocs serve
    else
        mkdocs build
        echo -e "${GREEN}✓ mkdocs documentation generated in site/${NC}"
        echo -e "  Open: site/index.html"
    fi
fi

# Generate Sphinx documentation
if [ "$DO_SPHINX" = true ]; then
    echo -e "\n${YELLOW}Generating Sphinx documentation...${NC}"
    if [ ! -d "docs" ]; then
        echo -e "${RED}Sphinx docs directory not found. Run 'sphinx-quickstart docs' first.${NC}"
        exit 1
    fi
    sphinx-build -b html docs docs/_build
    echo -e "${GREEN}✓ Sphinx documentation generated in docs/_build/${NC}"
    echo -e "  Open: docs/_build/index.html"
fi

echo -e "\n${GREEN}✓ Documentation generation completed successfully!${NC}"
