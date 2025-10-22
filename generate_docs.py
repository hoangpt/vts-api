#!/usr/bin/env python3
"""
Documentation Generation Script

This script generates HTML documentation for the VTS API project using multiple tools:
- pdoc: Simple API documentation from docstrings
- mkdocs: Static site generator with mkdocstrings plugin
- sphinx: Comprehensive documentation with autodoc

The script handles environment configuration to bypass database checks during
documentation generation.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def setup_mock_environment():
    """
    Set up environment variables to bypass database configuration checks.
    
    This allows documentation generation without requiring a database connection.
    """
    # Set IS_PRODUCTION to false to allow SQLite during doc generation
    os.environ['IS_PRODUCTION'] = 'false'
    # Use a mock database URL
    os.environ['DATABASE_URL'] = 'sqlite:///./storage/lengkeng.db'
    print("✓ Mock environment configured for documentation generation")

def generate_pdoc_docs(output_dir='docs/html/pdoc'):
    """
    Generate documentation using pdoc.
    
    pdoc creates simple, clean HTML documentation directly from Python docstrings.
    
    Args:
        output_dir: Directory where HTML files will be generated
    """
    print("\n📚 Generating documentation with pdoc...")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        # Generate docs for the main modules
        cmd = [
            sys.executable, '-m', 'pdoc',
            '--output-directory', str(output_path),
            'mod',
            'config',
            'main'
        ]
        subprocess.run(cmd, check=True)
        print(f"✓ pdoc documentation generated in {output_path}")
        print(f"  Open: {output_path}/index.html")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error generating pdoc documentation: {e}")
        return False
    return True

def generate_mkdocs(serve=False):
    """
    Generate documentation using mkdocs with mkdocstrings.
    
    mkdocs creates a beautiful static site with navigation and search.
    
    Args:
        serve: If True, serve the docs locally instead of just building
    """
    print("\n📚 Generating documentation with mkdocs...")
    
    try:
        if serve:
            cmd = [sys.executable, '-m', 'mkdocs', 'serve']
            print("Starting mkdocs development server...")
            print("Documentation will be available at http://127.0.0.1:8000")
            subprocess.run(cmd)
        else:
            cmd = [sys.executable, '-m', 'mkdocs', 'build']
            subprocess.run(cmd, check=True)
            print("✓ mkdocs documentation generated in site/")
            print("  Open: site/index.html")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error generating mkdocs documentation: {e}")
        return False
    except FileNotFoundError:
        print("✗ mkdocs.yml not found. Please create mkdocs configuration first.")
        return False
    return True

def generate_sphinx_docs(output_dir='docs/_build'):
    """
    Generate documentation using Sphinx.
    
    Sphinx provides comprehensive documentation with advanced features.
    
    Args:
        output_dir: Directory where HTML files will be generated
    """
    print("\n📚 Generating documentation with Sphinx...")
    
    docs_dir = Path('docs')
    if not docs_dir.exists():
        print("✗ Sphinx docs directory not found. Run 'sphinx-quickstart docs' first.")
        return False
    
    try:
        cmd = [sys.executable, '-m', 'sphinx', '-b', 'html', 'docs', output_dir]
        subprocess.run(cmd, check=True)
        print(f"✓ Sphinx documentation generated in {output_dir}")
        print(f"  Open: {output_dir}/index.html")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error generating Sphinx documentation: {e}")
        return False
    return True

def install_dependencies():
    """Install required documentation dependencies."""
    print("\n📦 Installing documentation dependencies...")
    try:
        cmd = [
            sys.executable, '-m', 'pip', 'install', '-q',
            'pdoc', 'mkdocs', 'mkdocs-material', 'mkdocstrings[python]',
            'sphinx', 'sphinx-rtd-theme'
        ]
        subprocess.run(cmd, check=True)
        print("✓ Documentation dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def main():
    """Main entry point for documentation generation."""
    parser = argparse.ArgumentParser(
        description='Generate HTML documentation for VTS API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all documentation
  python generate_docs.py --all
  
  # Generate only pdoc documentation
  python generate_docs.py --pdoc
  
  # Generate mkdocs and serve locally
  python generate_docs.py --mkdocs --serve
  
  # Install dependencies first
  python generate_docs.py --install
        """
    )
    
    parser.add_argument('--all', action='store_true',
                        help='Generate documentation using all available tools')
    parser.add_argument('--pdoc', action='store_true',
                        help='Generate documentation using pdoc')
    parser.add_argument('--mkdocs', action='store_true',
                        help='Generate documentation using mkdocs')
    parser.add_argument('--sphinx', action='store_true',
                        help='Generate documentation using Sphinx')
    parser.add_argument('--serve', action='store_true',
                        help='Serve mkdocs documentation locally (use with --mkdocs)')
    parser.add_argument('--install', action='store_true',
                        help='Install documentation dependencies')
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if not any([args.all, args.pdoc, args.mkdocs, args.sphinx, args.install]):
        parser.print_help()
        return
    
    # Install dependencies if requested
    if args.install:
        if not install_dependencies():
            sys.exit(1)
        if not any([args.all, args.pdoc, args.mkdocs, args.sphinx]):
            return
    
    # Set up mock environment for documentation generation
    setup_mock_environment()
    
    success = True
    
    # Generate documentation based on arguments
    if args.all or args.pdoc:
        if not generate_pdoc_docs():
            success = False
    
    if args.all or args.mkdocs:
        if not generate_mkdocs(serve=args.serve):
            success = False
    
    if args.all or args.sphinx:
        if not generate_sphinx_docs():
            success = False
    
    if success:
        print("\n✓ Documentation generation completed successfully!")
    else:
        print("\n⚠ Some documentation generation steps failed. See errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
