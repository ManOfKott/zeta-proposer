#!/usr/bin/env python3
"""
Debug script to test diagram generation and Word document insertion
"""

import os
import sys
from pathlib import Path
import logging

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.graphviz_diagram import GraphvizDiagramGenerator
from src.word_generator import WordDocumentGenerator

def setup_logging():
    """Setup logging for debugging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def test_diagram_generation():
    """Test diagram generation"""
    logger = setup_logging()
    logger.info("=== Testing Diagram Generation ===")
    
    # Test concept with DOT code
    test_concept = {
        'sections': {
            'system_scope': '''
# System Scope and Boundaries

This is a test system scope section.

```dot
digraph G {
    A [label="User Interface"];
    B [label="Backend API"];
    C [label="Database"];
    
    A -> B;
    B -> C;
}
```

This is the end of the section.
            ''',
            'architecture_tech_stack': '''
# Architecture and Technology Stack

This is a test architecture section.

```dot
digraph G {
    subgraph cluster_frontend {
        label="Frontend";
        A [label="React App"];
        B [label="UI Components"];
    }
    
    subgraph cluster_backend {
        label="Backend";
        C [label="API Server"];
        D [label="Database"];
    }
    
    A -> C;
    C -> D;
}
```

This is the end of the architecture section.
            '''
        }
    }
    
    # Create diagram generator
    visio_gen = GraphvizDiagramGenerator()
    visio_gen.logger = logger
    
    # Generate diagrams
    logger.info("Generating diagrams...")
    diagram_infos = visio_gen.create_diagrams(test_concept)
    
    logger.info(f"Generated {len(diagram_infos)} diagrams:")
    for info in diagram_infos:
        logger.info(f"  Section: {info['section']}")
        logger.info(f"  Path: {info['path']}")
        logger.info(f"  Caption: {info['caption']}")
        
        # Check if file exists
        if os.path.exists(info['path']):
            logger.info(f"  ✓ File exists: {info['path']}")
            logger.info(f"  File size: {os.path.getsize(info['path'])} bytes")
        else:
            logger.error(f"  ✗ File does not exist: {info['path']}")
    
    return diagram_infos

def test_word_document_creation(diagram_infos):
    """Test Word document creation with diagrams"""
    logger = setup_logging()
    logger.info("=== Testing Word Document Creation ===")
    
    # Test concept
    test_concept = {
        'sections': {
            'system_scope': 'This is the system scope section with a diagram.',
            'architecture_tech_stack': 'This is the architecture section with a diagram.',
            'external_interfaces': 'This is the external interfaces section.',
            'ci_cd': 'This is the CI/CD section.',
            'testing_concept': 'This is the testing concept section.',
            'deployment_operation': 'This is the deployment section.',
            'ux_ui': 'This is the UX/UI section.'
        }
    }
    
    # Create word generator
    word_gen = WordDocumentGenerator()
    word_gen.logger = logger
    
    # Create document
    logger.info("Creating Word document...")
    output_path = word_gen.create_document(test_concept, diagram_infos)
    
    logger.info(f"Word document created: {output_path}")
    
    # Check if file exists
    if os.path.exists(output_path):
        logger.info(f"✓ Word document exists: {output_path}")
        logger.info(f"File size: {os.path.getsize(output_path)} bytes")
    else:
        logger.error(f"✗ Word document does not exist: {output_path}")
    
    return output_path

def main():
    """Main test function"""
    print("=== Zeta Proposer Diagram Debug Test ===")
    print()
    
    # Test diagram generation
    diagram_infos = test_diagram_generation()
    print()
    
    # Test Word document creation
    if diagram_infos:
        output_path = test_word_document_creation(diagram_infos)
        print()
        print(f"=== Test Complete ===")
        print(f"Check the generated files:")
        print(f"  - Diagrams: output/diagrams/")
        print(f"  - Word document: {output_path}")
    else:
        print("No diagrams were generated, skipping Word document test.")

if __name__ == "__main__":
    main() 