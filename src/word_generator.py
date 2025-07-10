from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from typing import Dict, Any, List, Optional
from pathlib import Path
import os
import re
import logging
from datetime import datetime

class WordDocumentGenerator:
    def __init__(self):
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.template_path = None  # Path to selected template
        self.logger = logging.getLogger(__name__)
        self.logger.info("WordDocumentGenerator initialized")
        self.logger.info("Output directory: %s", self.output_dir)
    
    def set_template(self, template_path: Optional[str]):
        self.logger.info("Setting template: %s", template_path)
        self.template_path = template_path
    
    def _clean_markdown(self, text: str) -> str:
        """Remove markdown formatting from text"""
        self.logger.debug("Cleaning markdown from text")
        self.logger.debug("Input text length: %d", len(text) if text else 0)
        
        if not text:
            self.logger.debug("No text to clean")
            return text
        
        # Remove markdown headers (# ## ### etc.)
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        
        # Remove bold formatting (**text** or __text__)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'__(.*?)__', r'\1', text)
        
        # Remove italic formatting (*text* or _text_)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'_(.*?)_', r'\1', text)
        
        # Remove code formatting (`text`)
        text = re.sub(r'`(.*?)`', r'\1', text)
        
        # Remove bullet points and dashes at the beginning of lines
        text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)
        
        # Clean up extra whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        self.logger.debug("Cleaned text length: %d", len(text))
        return text
    
    def _remove_mermaid_blocks(self, text: str) -> str:
        self.logger.debug("Removing mermaid blocks from text")
        self.logger.debug("Input text length: %d", len(text) if text else 0)
        
        if not text:
            return text
        # Entfernt ```mermaid ... ``` Blöcke
        text = re.sub(r'```mermaid[\s\S]+?```', '', text, flags=re.IGNORECASE)
        # Entfernt Zeilen, die mit 'mermaid' oder 'graph' beginnen
        lines = text.splitlines()
        cleaned_lines = [line for line in lines if not line.strip().lower().startswith(('mermaid', 'graph'))]
        result = '\n'.join(cleaned_lines)
        
        self.logger.debug("Text after mermaid removal length: %d", len(result))
        return result
    
    def _remove_section_heading(self, content: str, title: str) -> str:
        """Remove the section heading/title from the AI content if present."""
        self.logger.debug("Removing section heading for title: %s", title)
        self.logger.debug("Content length: %d", len(content) if content else 0)
        
        if not content:
            return ''
        lines = content.strip().split('\n')
        # Remove first line if it matches the title (with or without numbering)
        if lines and (title.lower() in lines[0].lower() or lines[0].strip().startswith(tuple(str(i) for i in range(1, 10)))):
            result = '\n'.join(lines[1:]).lstrip()
            self.logger.debug("Removed heading, new length: %d", len(result))
            return result
        self.logger.debug("No heading removed, content unchanged")
        return content

    def _find_diagram_info(self, diagram_infos, section_key):
        """Find diagram info dict for a given section key."""
        self.logger.debug("Finding diagram info for section: %s", section_key)
        self.logger.debug("Diagram infos count: %d", len(diagram_infos) if diagram_infos else 0)
        
        if not diagram_infos:
            self.logger.debug("No diagram infos provided")
            return None
        for info in diagram_infos:
            if info.get('section') == section_key:
                self.logger.debug("Found diagram info for section: %s", section_key)
                return info
        self.logger.debug("No diagram info found for section: %s", section_key)
        return None

    def _insert_single_section(self, doc, insert_after, key, title, ai_sections, diagram_infos, heading_style, normal_style):
        """Replace the placeholder in the paragraph/cell directly with content and diagram, keeping document order stable."""
        self.logger.info("Inserting single section: %s", key)
        self.logger.info("Section title: %s", title)
        
        # Hole Fließtext aus neuer Struktur
        value = ai_sections.get(key)
        if isinstance(value, dict):
            content = value.get('text', '')
        else:
            content = value
        if not content:
            for k, v in ai_sections.items():
                if title.lower() in k.replace('_', ' ').lower():
                    if isinstance(v, dict):
                        content = v.get('text', '')
                    else:
                        content = v
                    break
        self.logger.info("Section %s: value length = %d", key, len(content) if content else 0)
        self.logger.debug("Section %s: value preview = %s", key, content[:100] if content else 'None')
        
        # Remove heading/title from AI content
        content = self._remove_section_heading(content, title)
        content = self._remove_mermaid_blocks(content)
        content = self._remove_dot_blocks(content)
        
        if content and not content.startswith("Section") and not content.startswith("Error"):
            content = self._clean_markdown(content)
            self.logger.info("Section %s: cleaned content length = %d", key, len(content))
            self.logger.debug("Section %s: content preview = %s", key, content[:200])
        else:
            content = f"(No information available for {title})"
            self.logger.info("Section %s: using fallback content", key)
            
        diagram_info = self._find_diagram_info(diagram_infos, key)
        
        # Paragraph case
        if insert_after is not None and hasattr(insert_after, 'text') and hasattr(insert_after, '_element'):
            self.logger.info("Inserting content in paragraph/cell for section: %s", key)
            insert_after.text = content
            self.logger.info("Replaced placeholder for section %s with content in paragraph/cell", key)
            
            if diagram_info:
                try:
                    parent = insert_after._parent
                    if hasattr(parent, 'paragraphs'):
                        idx = None
                        for i, p in enumerate(parent.paragraphs):
                            if p == insert_after:
                                idx = i
                                break
                        if idx is not None:
                            img_para = parent.add_paragraph()
                            run = img_para.add_run()
                            img_path = os.path.abspath(diagram_info['png_path'])
                            self.logger.info("Trying to insert image for section %s: %s", key, img_path)
                            
                            if not os.path.exists(img_path):
                                self.logger.error("File does not exist: %s", img_path)
                                parent.add_paragraph(f"Diagram file not found: {Path(diagram_info['png_path']).name}", style=normal_style)
                                return
                                
                            run.add_picture(img_path, width=Inches(5.5))
                            caption_para = parent.add_paragraph("Diagram generated from Graphviz DOT code.", style=normal_style)
                            parent.paragraphs.insert(idx + 1, img_para)
                            parent.paragraphs.insert(idx + 2, caption_para)
                            self.logger.info("Inserted diagram and caption for section %s after paragraph (image: %s)", key, img_path)
                except Exception as e:
                    parent.add_paragraph(f"Error adding diagram: {str(e)}", style=normal_style)
                    self.logger.error("Error adding diagram for section %s (image: %s): %s", key, img_path, str(e), exc_info=True)
            else:
                self.logger.warning("No diagram found for section %s, no image inserted", key)
                parent = insert_after._parent
                parent.add_paragraph(f"[No diagram available for this section]", style=normal_style)
                
        # Table cell case
        elif hasattr(insert_after, 'text') and hasattr(insert_after, 'add_paragraph'):
            self.logger.info("Inserting content in table cell for section: %s", key)
            insert_after.text = content
            self.logger.info("Replaced placeholder for section %s with content in table cell", key)
            
            if diagram_info:
                try:
                    img_para = insert_after.add_paragraph()
                    run = img_para.add_run()
                    img_path = os.path.abspath(diagram_info['png_path'])
                    self.logger.info("Trying to insert image for section %s: %s", key, img_path)
                    
                    if not os.path.exists(img_path):
                        self.logger.error("File does not exist: %s", img_path)
                        insert_after.add_paragraph(f"Diagram file not found: {Path(diagram_info['png_path']).name}", style=normal_style)
                        return
                        
                    run.add_picture(img_path, width=Inches(5.5))
                    caption_para = insert_after.add_paragraph("Diagram generated from Graphviz DOT code.", style=normal_style)
                    self.logger.info("Inserted diagram and caption for section %s in table cell (image: %s)", key, img_path)
                except Exception as e:
                    insert_after.add_paragraph(f"Error adding diagram: {str(e)}", style=normal_style)
                    self.logger.error("Error adding diagram for section %s in table cell (image: %s): %s", key, img_path, str(e), exc_info=True)
            else:
                self.logger.warning("No diagram found for section %s, no image inserted (table cell)", key)
                insert_after.add_paragraph(f"[No diagram available for this section]", style=normal_style)
        else:
            # Add content only (no heading)
            self.logger.info("Adding content only for section: %s", key)
            content_para = doc.add_paragraph(content, style=normal_style)
            self.logger.info("Added content for section %s: %d chars", key, len(content))
            
            if diagram_info:
                try:
                    img_para = doc.add_paragraph()
                    run = img_para.add_run()
                    img_path = os.path.abspath(diagram_info['png_path'])
                    self.logger.info("Trying to insert image for section %s: %s", key, img_path)
                    
                    if not os.path.exists(img_path):
                        self.logger.error("File does not exist: %s", img_path)
                        doc.add_paragraph(f"Diagram file not found: {Path(diagram_info['png_path']).name}", style=normal_style)
                        return
                        
                    run.add_picture(img_path, width=Inches(5.5))
                    caption_para = doc.add_paragraph("Diagram generated from Graphviz DOT code.", style=normal_style)
                    self.logger.info("Inserted diagram and caption for section %s (no template mode, image: %s)", key, img_path)
                except Exception as e:
                    doc.add_paragraph(f"Error adding diagram: {str(e)}", style=normal_style)
                    self.logger.error("Error adding diagram for section %s (no template mode, image: %s): %s", key, img_path, str(e), exc_info=True)
            else:
                self.logger.warning("No diagram found for section %s, no image inserted (no template mode)", key)
                doc.add_paragraph(f"[No diagram available for this section]", style=normal_style)
    
    def create_document(self, concept: Dict[str, Any], diagram_infos: Optional[list] = None) -> str:
        """Create Word document from technical concept, using template if set. diagram_infos is a list of dicts with section, path, caption."""
        self.logger.info("Starting document creation")
        self.logger.info("Concept sections count: %d", len(concept.get('sections', {})))
        self.logger.info("Diagram infos count: %d", len(diagram_infos) if diagram_infos else 0)
        
        section_placeholders = [
            ("system_scope", "System scope and boundaries"),
            ("architecture_tech_stack", "Architecture and technology stack"),
            ("external_interfaces", "System-external interfaces and integrations"),
            ("ci_cd", "CI/CD Pipelines"),
            ("testing_concept", "Specific testing concept"),
            ("deployment_operation", "Deployment and Operation environment"),
            ("ux_ui", "UX/UI design and prototyping")
        ]
        
        self.logger.info("Template path: %s", self.template_path)
        self.logger.info("Template exists: %s", os.path.exists(self.template_path) if self.template_path else False)
        
        if self.template_path and os.path.exists(self.template_path):
            self.logger.info("Using existing template: %s", self.template_path)
            doc = Document(self.template_path)
            heading_style = 'Heading 1'
            normal_style = 'Normal'
            ai_sections = concept.get('sections', {})
            
            self.logger.info("Extracted ai_sections:")
            for k, v in ai_sections.items():
                if isinstance(v, str):
                    preview = v[:100]
                elif isinstance(v, dict) and 'text' in v and isinstance(v['text'], str):
                    preview = v['text'][:100]
                else:
                    preview = str(v)[:100]
                self.logger.info("  %s: %s", k, preview)
                
            # Check if template has any placeholders
            template_has_placeholders = False
            placeholder_found = None
            
            # Check paragraphs for placeholders
            self.logger.info("Checking paragraphs for placeholders")
            for para in doc.paragraphs:
                for key, title in section_placeholders:
                    if f"{{{{{key}}}}}" in para.text:
                        template_has_placeholders = True
                        placeholder_found = key
                        self.logger.info("Found placeholder %s in paragraph: %s...", f"{{{{{key}}}}}", para.text[:50])
                        break
                if template_has_placeholders:
                    break
                    
            # Check tables for placeholders
            self.logger.info("Checking tables for placeholders")
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for key, title in section_placeholders:
                            if f"{{{{{key}}}}}" in cell.text:
                                template_has_placeholders = True
                                placeholder_found = key
                                self.logger.info("Found placeholder %s in table cell: %s...", f"{{{{{key}}}}}", cell.text[:50])
                                break
                        if template_has_placeholders:
                            break
                    if template_has_placeholders:
                        break
                if template_has_placeholders:
                    break
                    
            self.logger.info("Template has placeholders: %s", template_has_placeholders)
            if placeholder_found:
                self.logger.info("Found placeholder: %s", placeholder_found)
                
            if template_has_placeholders:
                # Replace placeholders in existing template
                self.logger.info("Replacing placeholders in existing template")
                for key, title in section_placeholders:
                    self.logger.info("Processing placeholder for section: %s", key)
                    
                    # Insert in paragraphs
                    for para in doc.paragraphs:
                        if f"{{{{{key}}}}}" in para.text:
                            self.logger.info("Found placeholder %s in paragraph. Inserting content.", f"{{{{{key}}}}}")
                            self._insert_single_section(doc, para, key, title, ai_sections, diagram_infos or [], heading_style, normal_style)
                            
                    # Insert in tables
                    for table in doc.tables:
                        for row in table.rows:
                            for cell in row.cells:
                                if f"{{{{{key}}}}}" in cell.text:
                                    self.logger.info("Found placeholder %s in table cell. Inserting content.", f"{{{{{key}}}}}")
                                    self._insert_single_section(doc, cell, key, title, ai_sections, diagram_infos or [], heading_style, normal_style)
            else:
                # Create new document structure if no placeholders found
                self.logger.info("No placeholders found in template, creating new document structure")
                doc = Document()
                self._setup_document_styles(doc)
                heading_style = 'CustomHeading1'
                normal_style = 'CustomNormal'
                
                # Add title
                doc.add_paragraph("Technical Concept Document", style='CustomTitle')
                doc.add_paragraph()
                
                # Add sections
                for key, title in section_placeholders:
                    self.logger.info("Adding section %s: %s", key, title)
                    self._insert_single_section(doc, None, key, title, ai_sections, diagram_infos or [], heading_style, normal_style)
        else:
            self.logger.info("No template found, creating new document")
            doc = Document()
            self._setup_document_styles(doc)
            heading_style = 'CustomHeading1'
            normal_style = 'CustomNormal'
            ai_sections = concept.get('sections', {})
            
            self.logger.info("Extracted ai_sections:")
            for k, v in ai_sections.items():
                if isinstance(v, str):
                    preview = v[:100]
                elif isinstance(v, dict) and 'text' in v and isinstance(v['text'], str):
                    preview = v['text'][:100]
                else:
                    preview = str(v)[:100]
                self.logger.info("  %s: %s", k, preview)
                
            # Add title
            doc.add_paragraph("Technical Concept Document", style='CustomTitle')
            doc.add_paragraph()
            
            # Add sections
            for key, title in section_placeholders:
                self.logger.info("Inserting section %s (no template mode)", key)
                self._insert_single_section(doc, None, key, title, ai_sections, diagram_infos or [], heading_style, normal_style)
                
            self._add_metadata(doc, concept)
            
        docx_output_dir = Path(self.output_dir) / "docx"
        docx_output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"technical_concept_{timestamp}.docx"
        output_path = docx_output_dir / filename
        
        self.logger.info("Saving document to: %s", output_path)
        doc.save(str(output_path))
        self.logger.info("Document saved successfully: %s", output_path)
        return str(output_path)
    
    def _setup_document_styles(self, doc):
        """Setup document styles"""
        # Title style
        title_style = doc.styles.add_style('CustomTitle', WD_STYLE_TYPE.PARAGRAPH)
        title_style.font.name = 'Inter Light'
        title_style.font.size = Pt(24)
        title_style.font.bold = True
        title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_style.paragraph_format.space_after = Pt(12)
        
        # Heading 1 style
        h1_style = doc.styles.add_style('CustomHeading1', WD_STYLE_TYPE.PARAGRAPH)
        h1_style.font.name = 'Inter Light'
        h1_style.font.size = Pt(16)
        h1_style.font.bold = True
        h1_style.paragraph_format.space_before = Pt(12)
        h1_style.paragraph_format.space_after = Pt(6)
        
        # Heading 2 style
        h2_style = doc.styles.add_style('CustomHeading2', WD_STYLE_TYPE.PARAGRAPH)
        h2_style.font.name = 'Inter Light'
        h2_style.font.size = Pt(14)
        h2_style.font.bold = True
        h2_style.paragraph_format.space_before = Pt(10)
        h2_style.paragraph_format.space_after = Pt(4)
        
        # Normal text style
        normal_style = doc.styles.add_style('CustomNormal', WD_STYLE_TYPE.PARAGRAPH)
        normal_style.font.name = 'Inter Light'
        normal_style.font.size = Pt(11)
        normal_style.paragraph_format.space_after = Pt(6)
    
    def _add_title_page(self, doc, concept: Dict[str, Any]):
        """Add title page"""
        # Title
        title = doc.add_paragraph("Technical Concept Document", style='CustomTitle')
        
        # Subtitle
        subtitle = doc.add_paragraph("Generated by Zeta Proposer", style='CustomNormal')
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Date
        date_para = doc.add_paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", style='CustomNormal')
        date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add some space
        doc.add_paragraph()
        doc.add_paragraph()
        
        # Project overview from concept
        if 'sections' in concept and 'project_overview' in concept['sections']:
            overview = concept['sections']['project_overview']
            if overview and overview != "Section 'PROJECT OVERVIEW' not found in response":
                # Clean markdown and extract project name if possible
                cleaned_overview = self._clean_markdown(overview)
                lines = cleaned_overview.split('\n')
                project_name = "Technical Project"
                for line in lines[:5]:  # Check first 5 lines
                    if line.strip() and not line.startswith('-') and len(line.strip()) < 100:
                        project_name = line.strip()
                        break
                
                project_title = doc.add_paragraph(project_name, style='CustomHeading1')
                project_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Page break
        doc.add_page_break()
    
    def _add_table_of_contents(self, doc):
        """Add table of contents placeholder"""
        toc_heading = doc.add_paragraph("Table of Contents", style='CustomHeading1')
        toc_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add TOC entries
        toc_entries = [
            "1. Project Overview",
            "2. System Architecture", 
            "3. Technical Requirements",
            "4. Implementation Approach",
            "5. Diagrams and Visualizations"
        ]
        
        for entry in toc_entries:
            toc_para = doc.add_paragraph(entry, style='CustomNormal')
            toc_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        doc.add_page_break()
    
    def _add_project_overview(self, doc, concept: Dict[str, Any]):
        """Add project overview section"""
        heading = doc.add_paragraph("1. Project Overview", style='CustomHeading1')
        
        if 'sections' in concept and 'project_overview' in concept['sections']:
            overview = concept['sections']['project_overview']
            if overview and overview != "Section 'PROJECT OVERVIEW' not found in response":
                # Clean markdown and split into paragraphs
                cleaned_overview = self._clean_markdown(overview)
                paragraphs = cleaned_overview.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        doc.add_paragraph(para.strip(), style='CustomNormal')
            else:
                doc.add_paragraph("Project overview information not available.", style='CustomNormal')
        else:
            doc.add_paragraph("Project overview information not available.", style='CustomNormal')
    
    def _add_system_architecture(self, doc, concept: Dict[str, Any], diagram_paths: Optional[List[str]] = None):
        """Add system architecture section"""
        if diagram_paths is None:
            diagram_paths = []
        heading = doc.add_paragraph("2. System Architecture", style='CustomHeading1')
        
        if 'sections' in concept and 'system_architecture' in concept['sections']:
            architecture = concept['sections']['system_architecture']
            if architecture and architecture != "Section 'SYSTEM ARCHITECTURE' not found in response":
                # Clean markdown and split into paragraphs
                cleaned_architecture = self._clean_markdown(architecture)
                paragraphs = cleaned_architecture.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        doc.add_paragraph(para.strip(), style='CustomNormal')
            else:
                doc.add_paragraph("System architecture information not available.", style='CustomNormal')
        else:
            doc.add_paragraph("System architecture information not available.", style='CustomNormal')
        
        # Add architecture diagram if available
        if diagram_paths:
            for diagram_path in diagram_paths:
                if "architecture" in diagram_path.lower():
                    try:
                        # Ensure absolute path
                        abs_path = os.path.abspath(diagram_path)
                        self.logger.info(f"[DIAGRAM-INSERT] Trying to insert architecture diagram: {abs_path}")
                        
                        # Check if file exists
                        if not os.path.exists(abs_path):
                            self.logger.error(f"[DIAGRAM-INSERT] Architecture diagram file does not exist: {abs_path}")
                            doc.add_paragraph("System Architecture Diagram (file not found)", style='CustomNormal')
                            continue
                        
                        doc.add_paragraph("System Architecture Diagram:", style='CustomHeading2')
                        doc.add_picture(abs_path, width=Inches(6))
                        self.logger.info(f"[DIAGRAM-INSERT] Successfully inserted architecture diagram: {abs_path}")
                    except Exception as e:
                        self.logger.error(f"[DIAGRAM-INSERT] Error adding architecture diagram {diagram_path}: {str(e)}", exc_info=True)
                        doc.add_paragraph(f"Error adding architecture diagram: {str(e)}", style='CustomNormal')
    
    def _add_technical_requirements(self, doc, concept: Dict[str, Any]):
        """Add technical requirements section"""
        heading = doc.add_paragraph("3. Technical Requirements", style='CustomHeading1')
        
        if 'sections' in concept and 'technical_requirements' in concept['sections']:
            requirements = concept['sections']['technical_requirements']
            if requirements and requirements != "Section 'TECHNICAL REQUIREMENTS' not found in response":
                # Clean markdown and split into paragraphs
                cleaned_requirements = self._clean_markdown(requirements)
                paragraphs = cleaned_requirements.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        doc.add_paragraph(para.strip(), style='CustomNormal')
            else:
                doc.add_paragraph("Technical requirements information not available.", style='CustomNormal')
        else:
            doc.add_paragraph("Technical requirements information not available.", style='CustomNormal')
    
    def _add_implementation_approach(self, doc, concept: Dict[str, Any]):
        """Add implementation approach section"""
        heading = doc.add_paragraph("4. Implementation Approach", style='CustomHeading1')
        
        if 'sections' in concept and 'implementation_approach' in concept['sections']:
            approach = concept['sections']['implementation_approach']
            if approach and approach != "Section 'IMPLEMENTATION APPROACH' not found in response":
                # Clean markdown and split into paragraphs
                cleaned_approach = self._clean_markdown(approach)
                paragraphs = cleaned_approach.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        doc.add_paragraph(para.strip(), style='CustomNormal')
            else:
                doc.add_paragraph("Implementation approach information not available.", style='CustomNormal')
        else:
            doc.add_paragraph("Implementation approach information not available.", style='CustomNormal')
    
    def _add_diagrams_section(self, doc, diagram_paths: List[str]):
        """Add diagrams section"""
        self.logger.info("Adding diagrams to document:")
        self.logger.info(diagram_paths)
        heading = doc.add_paragraph("5. Diagrams and Visualizations", style='CustomHeading1')
        
        for diagram_path in diagram_paths:
            try:
                # Ensure absolute path
                abs_path = os.path.abspath(diagram_path)
                self.logger.info(f"[DIAGRAM-INSERT] Trying to insert: {abs_path}")
                
                # Check if file exists
                if not os.path.exists(abs_path):
                    self.logger.error(f"[DIAGRAM-INSERT] File does not exist: {abs_path}")
                    doc.add_paragraph(f"Diagram file not found: {Path(diagram_path).name}", style='CustomNormal')
                    continue
                
                # Extract diagram name from path
                diagram_name = Path(diagram_path).stem.replace('_', ' ').title()
                doc.add_paragraph(f"{diagram_name}:", style='CustomHeading2')
                
                # Add picture with absolute path
                doc.add_picture(abs_path, width=Inches(6))
                self.logger.info(f"[DIAGRAM-INSERT] Successfully inserted: {abs_path}")
                doc.add_paragraph()  # Add some space
            except Exception as e:
                self.logger.error(f"[DIAGRAM-INSERT] Error adding diagram {diagram_path}: {str(e)}", exc_info=True)
                doc.add_paragraph(f"Error adding diagram {Path(diagram_path).name}: {str(e)}", style='CustomNormal')
    
    def _add_metadata(self, doc, concept: Dict[str, Any]):
        """Add document metadata"""
        doc.add_page_break()
        
        heading = doc.add_paragraph("Document Information", style='CustomHeading1')
        
        # Add metadata
        metadata_items = [
            f"Generated by: {concept.get('metadata', {}).get('generated_by', 'Zeta Proposer')}",
            f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}",
            f"Document version: 1.0"
        ]
        
        for item in metadata_items:
            doc.add_paragraph(item, style='CustomNormal') 

    def _remove_dot_blocks(self, text: str) -> str:
        if not text:
            return text
        self.logger.info(f"[DOT-REMOVE] Vorher: {text[:200]}")
        # Entfernt alle ```dot ... ```-Blöcke, auch mit optionalen Whitespaces/Zeilenumbrüchen
        text = re.sub(r'```\s*dot[\s\S]+?```', '', text, flags=re.IGNORECASE)
        # Entfernt Zeilen, die mit 'digraph' oder 'graph' beginnen (zur Sicherheit)
        lines = text.splitlines()
        cleaned_lines = [line for line in lines if not line.strip().lower().startswith(('digraph', 'graph'))]
        result = '\n'.join(cleaned_lines)
        self.logger.info(f"[DOT-REMOVE] Nachher: {result[:200]}")
        return result 