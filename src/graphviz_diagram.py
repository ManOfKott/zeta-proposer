import os
from pathlib import Path
from typing import Dict, Any, List
import logging
from graphviz import Digraph
import re

class GraphvizDiagramGenerator:
    def __init__(self, node_colors=None):
        self.output_dir = Path("output/diagrams")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.logger.info("GraphvizDiagramGenerator initialized")
        self.logger.info("Output directory: %s", self.output_dir)
        # Konfigurierbare Farben (jetzt: weiß, dunkelblau, blau, hellblau)
        self.node_colors = node_colors or ["#ffffff", "#09182F", "#034EA2", "#C7FDFF"]
        self.fontname = "Inter"

    def set_node_colors(self, colors):
        if isinstance(colors, list) and len(colors) == 4:
            self.node_colors = colors
        else:
            raise ValueError("You must provide a list of exactly 4 colors.")

    def set_font(self, fontname):
        self.fontname = fontname

    def _patch_dot_code(self, dot_code: str) -> str:
        """Fügt allen Knoten die Schriftart und abwechselnd eine der 4 Farben hinzu."""
        # Finde alle Knoten-Definitionen (vereinfachte Annahme: eine pro Zeile, keine Subgraphen)
        lines = dot_code.splitlines()
        patched_lines = []
        color_idx = 0
        node_pattern = re.compile(r'^(\s*\w+\s*\[)([^\]]*)(\])')
        for line in lines:
            m = node_pattern.match(line)
            if m:
                attrs = m.group(2)
                # Schriftart setzen
                if 'fontname=' not in attrs:
                    attrs += f', fontname="{self.fontname}"'
                # Farbe setzen
                if 'fillcolor=' not in attrs:
                    color = self.node_colors[color_idx % 4]
                    attrs += f', style=filled, fillcolor="{color}"'
                    color_idx += 1
                patched_line = f'{m.group(1)}{attrs}{m.group(3)}'
                patched_lines.append(patched_line)
            else:
                patched_lines.append(line)
        return '\n'.join(patched_lines)

    def create_diagrams(self, concept: Dict[str, Any]) -> List[Dict[str, str]]:
        """Erzeuge Diagramme nur aus separat generiertem DOT-Code in concept['sections'][key]['dot_code']."""
        self.logger.info("Starting diagram creation from concept")
        self.logger.info("Concept sections count: %d", len(concept.get('sections', {})))
        
        diagram_infos = []
        sections = concept.get('sections', {})
        
        for section_key, section_data in sections.items():
            self.logger.info("Processing section: %s", section_key)
            
            dot_code = section_data.get('dot_code', '')
            if not dot_code or not dot_code.strip():
                self.logger.warning("No DOT code found or DOT code is empty for section %s", section_key)
                continue
                
            # Logge einen Ausschnitt des DOT-Codes
            preview = dot_code.strip().replace('\n', ' ')[:120]
            self.logger.info("DOT code for %s: %s...", section_key, preview)
            self.logger.info("DOT code length: %d characters", len(dot_code))
            
            try:
                self.logger.info("Rendering diagram for section: %s", section_key)
                png_path = self._dot_to_graphviz_png(dot_code, section_key)
                
                if png_path:
                    self.logger.info("Diagram successfully created for section %s: %s", section_key, png_path)
                    diagram_infos.append({'section': section_key, 'dot': dot_code, 'png_path': png_path})
                else:
                    self.logger.error("Failed to create diagram for section %s", section_key)
                    
            except Exception as e:
                self.logger.error("Error rendering diagram for %s: %s", section_key, e)
                
        self.logger.info("Diagram creation completed. Created %d diagrams", len(diagram_infos))
        return diagram_infos

    def _extract_dot_code(self, text: str) -> str:
        """Extrahiere den ersten ```dot ... ```-Block aus dem Text."""
        self.logger.info("Extracting DOT code from text")
        self.logger.info("Input text length: %d characters", len(text) if text else 0)
        
        if not text:
            self.logger.warning("No text provided for DOT code extraction")
            return ''
            
        import re
        m = re.search(r'```dot\s*([\s\S]+?)```', text, re.IGNORECASE)
        if m:
            code = m.group(1).strip()
            self.logger.info("Extracted DOT code length: %d characters", len(code))
            self.logger.debug("Extracted DOT code: %s", code)
            return code
        else:
            self.logger.warning("No DOT code block found in text")
            return ''

    def _log_output_dir_contents(self, expected_name=None):
        self.logger.info("Logging output directory contents")
        cwd = os.getcwd()
        self.logger.info("Current working directory: %s", cwd)
        self.logger.info("Output directory: %s", self.output_dir)
        
        if not self.output_dir.exists():
            self.logger.warning("Output directory does not exist")
            return
            
        self.logger.info("Contents of %s:", self.output_dir)
        for f in self.output_dir.iterdir():
            self.logger.info("  - %s (%d bytes)", f.name, f.stat().st_size)
            
        if expected_name:
            similar = [f for f in self.output_dir.iterdir() if expected_name in f.name]
            self.logger.info("Files similar to '%s':", expected_name)
            for f in similar:
                self.logger.info("  - %s (%d bytes)", f.name, f.stat().st_size)

    def _dot_to_graphviz_png(self, dot_code: str, section_key: str) -> str:
        self.logger.info("Converting DOT code to PNG for section: %s", section_key)
        self.logger.info("DOT code length: %d characters", len(dot_code))
        try:
            from graphviz import Source
            import subprocess
            import tempfile
            self.output_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info("Output directory ensured: %s", self.output_dir)
            png_filename = f"{section_key}_diagram"
            png_path = self.output_dir / (png_filename + ".png")
            render_path = str(self.output_dir / png_filename)
            self.logger.info("PNG path: %s", png_path)
            self.logger.info("Render path: %s", render_path)
            # --- PATCH DOT CODE ---
            dot_code = self._patch_dot_code(dot_code)
            # Try using graphviz Python library first
            try:
                self.logger.info("Attempting to render with Python graphviz library")
                src = Source(dot_code)
                src.format = 'png'
                abs_render_path = str(Path(render_path).absolute())
                self.output_dir.mkdir(parents=True, exist_ok=True)
                self.logger.info("Rendering to: %s", abs_render_path)
                src.render(abs_render_path, cleanup=True)
                self.logger.info("Python graphviz library rendered successfully: %s.png", abs_render_path)
                self._log_output_dir_contents(section_key)
                expected_png = abs_render_path + ".png"
                if os.path.exists(expected_png):
                    self.logger.info("PNG file created with expected name: %s", expected_png)
                    if expected_png != str(png_path):
                        import shutil
                        shutil.move(expected_png, str(png_path))
                        self.logger.info("Moved PNG file to correct location: %s", png_path)
            except Exception as py_error:
                self.logger.warning("Python graphviz failed: %s", py_error)
                self._log_output_dir_contents(section_key)
                try:
                    self.logger.info("Attempting fallback with command line dot")
                    import tempfile
                    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.dot') as tmp_dot:
                        tmp_dot.write(dot_code)
                        dot_file_path = tmp_dot.name
                    self.logger.info("Temporary DOT file created: %s", dot_file_path)
                    cmd = ['dot', '-Tpng', '-o', str(png_path), dot_file_path]
                    self.logger.info("Running command: %s", ' '.join(cmd))
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    self.logger.info("Command line dot rendered successfully: %s", png_path)
                    self.logger.debug("Command stdout: %s", result.stdout)
                    self._log_output_dir_contents(section_key)
                    try:
                        os.remove(dot_file_path)
                        self.logger.info("Temporary DOT file cleaned up")
                    except Exception as cleanup_error:
                        self.logger.warning("Failed to clean up temporary DOT file: %s", cleanup_error)
                except subprocess.CalledProcessError as cmd_error:
                    self.logger.error("Command line dot failed: %s", cmd_error)
                    self.logger.error("Command stderr: %s", cmd_error.stderr)
                    self.logger.error("Command stdout: %s", cmd_error.stdout)
                    self._log_output_dir_contents(section_key)
                    return ''
                except Exception as cmd_error:
                    self.logger.error("Command line dot exception: %s", cmd_error)
                    self._log_output_dir_contents(section_key)
                    return ''
            abs_path = os.path.abspath(png_path)
            self.logger.info("Checking if PNG file was created: %s", abs_path)
            if os.path.exists(abs_path):
                file_size = os.path.getsize(abs_path)
                self.logger.info("PNG successfully created: %s (%d bytes)", abs_path, file_size)
                return abs_path
            else:
                self.logger.error("PNG file was not created: %s", abs_path)
                self._log_output_dir_contents(section_key)
                return ''
        except Exception as e:
            self.logger.error("Error rendering DOT code for %s: %s", section_key, e, exc_info=True)
            self._log_output_dir_contents(section_key)
            return '' 