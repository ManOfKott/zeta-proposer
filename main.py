#!/usr/bin/env python3
"""
Zeta Proposer - Technical Concept Generator
Main entry point for the application
"""

import sys
import os
from pathlib import Path
import pythoncom

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.gui import main as gui_main

def main():
    """Main entry point"""
    print("Starting Zeta Proposer...")
    print("Technical Concept Generator")
    print("=" * 40)
    
    try:
        # Check if required directories exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        pythoncom.CoInitialize()
        gui_main()
        pythoncom.CoUninitialize()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except ImportError as e:
        print(f"Import error: {str(e)}")
        print("Please make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 