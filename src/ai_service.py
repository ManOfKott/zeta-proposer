import os
import json
import requests
import logging
from typing import Dict, Any, Optional
import openai
from openai import OpenAI
import re

class AIServiceManager:
    def __init__(self):
        self.openai_client = None
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        self.logger = logging.getLogger(__name__)
        self.alignment_threshold = 0.6  # Default, kann von außen überschrieben werden
        
    def _setup_openai(self):
        """Setup OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Please configure it in the settings.")
        
        self.openai_client = OpenAI(api_key=api_key)
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        self.logger.info("Calling OpenAI API with prompt length: %d", len(prompt))
        self.logger.debug("OpenAI prompt preview: %s...", prompt[:200])
        
        if not self.openai_client:
            self.logger.info("Setting up OpenAI client")
            self._setup_openai()
        if not self.openai_client:
            self.logger.error("OpenAI client could not be initialized")
            raise Exception("OpenAI client could not be initialized. Check your API key and installation.")
        
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.logger.info("Using OpenAI model: %s", model)
        
        try:
            self.logger.info("Sending request to OpenAI API")
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            content = response.choices[0].message.content
            if content is None:
                self.logger.error("OpenAI returned empty response")
                raise Exception("OpenAI returned empty response")
            
            self.logger.info("OpenAI response received, length: %d", len(content))
            self.logger.debug("OpenAI response preview: %s...", content[:200])
            return content
        except Exception as e:
            self.logger.error("OpenAI API error: %s", str(e))
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API (new /api/chat endpoint for Ollama >=0.9.x)"""
        self.logger.info("Calling Ollama API with prompt length: %d", len(prompt))
        self.logger.debug("Ollama prompt preview: %s...", prompt[:200])
        self.logger.info("Using Ollama model: %s", self.ollama_model)
        
        try:
            url = f"{self.ollama_url}/api/chat"
            payload = {
                "model": self.ollama_model,
                "messages": [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
            self.logger.info("Sending request to Ollama API at: %s", url)
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            # The response format: {"message": {"role": ..., "content": ...}, ...}
            content = result["message"]["content"]
            self.logger.info("Ollama response received, length: %d", len(content))
            self.logger.debug("Ollama response preview: %s...", content[:200])
            return content
        except requests.exceptions.RequestException as e:
            self.logger.error("Ollama API request error: %s", str(e))
            raise Exception(f"Ollama API error: {str(e)}")
        except Exception as e:
            self.logger.error("Error calling Ollama: %s", str(e))
            raise Exception(f"Error calling Ollama: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for technical concept generation (strict, user-defined outline and length, with diagrams for sections 1 and 2, and NO extra sections)."""
        return '''You are an expert software architect and technical writer. Your task is to create a technical concept for a software project, strictly following the outline and content requirements below.

CRITICAL REQUIREMENTS:
- Provide ONLY the following 7 sections, with EXACTLY the headers and numbering as shown below. Do NOT add any other sections, such as project costs, payment plan, summary, conclusion, or anything else.
- For each section, address ONLY the listed content points. Do NOT add any other topics, examples, or sections.
- STRICTLY adhere to the maximum length for each section (e.g., "max. ½ page"). NEVER exceed the specified length.
- Use clear, professional language. No summaries, no introductions, no additional explanations.
- Use the exact section headers and numbering as shown below.
- Write in continuous text (no bullet points unless explicitly requested).
- Do NOT use markdown formatting.
- Do NOT include any diagram code, DOT code, or visual elements.
- Repeat: Do NOT add any other sections, such as project costs, payment plan, summary, conclusion, or anything else. Only the 7 sections below are allowed. Use the exact headers and numbering. No summaries, no introductions, no additional explanations.'''
    
    def generate_technical_concept(self, project_description: str, provider: str = "openai", proposal_context: str = "") -> Dict[str, Any]:
        """Generate technical concept from project description with optional proposal context"""
        self.logger.info("Starting technical concept generation")
        self.logger.info("Provider: %s", provider)
        self.logger.info("Project description length: %d", len(project_description))
        self.logger.info("Proposal context provided: %s", bool(proposal_context and proposal_context.strip()))
        
        # Build context-aware prompt
        if proposal_context and proposal_context.strip():
            self.logger.info("Building prompt with existing proposal context")
            prompt = f"""Please create a comprehensive technical concept for the following project, ensuring consistency with the existing proposal content:

PROJECT DESCRIPTION:
{project_description}

EXISTING PROPOSAL CONTEXT:
{proposal_context}

IMPORTANT: The technical concept should be consistent with and complement the existing proposal content. Avoid contradictions and ensure the technical approach aligns with what has been described in the proposal.

Please provide a detailed technical analysis and concept document as specified in the system prompt."""
        else:
            self.logger.info("Building prompt without proposal context")
            prompt = f"""Please create a comprehensive technical concept for the following project:

{project_description}

Please provide a detailed technical analysis and concept document as specified in the system prompt."""

        self.logger.info("Final prompt length: %d", len(prompt))

        try:
            self.logger.info("Calling AI provider: %s", provider)
            if provider == "openai":
                response = self._call_openai(prompt)
            elif provider == "ollama":
                response = self._call_ollama(prompt)
            else:
                self.logger.error("Unsupported AI provider: %s", provider)
                raise ValueError(f"Unsupported AI provider: {provider}")
            
            self.logger.info("AI response received, parsing concept")
            # Parse the response into structured format
            concept = self._parse_concept_response(response)
            self.logger.info("Technical concept generation completed successfully")
            return concept
            
        except Exception as e:
            self.logger.error("Failed to generate technical concept: %s", str(e))
            raise Exception(f"Failed to generate technical concept: {str(e)}")
    
    def _parse_concept_response(self, response: str) -> Dict[str, Any]:
        self.logger.info("AI raw response: %s", response)
        
        # Parse sections
        sections = {}
        section_names = [
            ("system_scope", "System scope and boundaries"),
            ("architecture_tech_stack", "Architecture and technology stack"),
            ("external_interfaces", "System-external interfaces and integrations"),
            ("ci_cd", "CI/CD Pipelines"),
            ("testing_concept", "Specific testing concept"),
            ("deployment_operation", "Deployment and Operation environment"),
            ("ux_ui", "UX/UI design and prototyping")
        ]
        
        for key, title in section_names:
            content = self._extract_section(response, title)
            sections[key] = content
            self.logger.info(f"Extracted {key}: {len(content)} chars")
            
            # If section extraction failed, try fallback
            if content.startswith("Section") or content.startswith("Error") or len(content) < 50:
                self.logger.info(f"Section {key} extraction failed, trying fallback")
                fallback_content = self._extract_section_fallback(response, key, title)
                if fallback_content and len(fallback_content) > 50:
                    sections[key] = fallback_content
                    self.logger.info(f"Fallback extracted {key}: {len(fallback_content)} chars")
        
        return {
            "raw_response": response,
            "sections": sections,
            "metadata": {
                "generated_by": "Zeta Proposer",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }
    
    def _extract_section(self, text: str, section_name: str) -> str:
        try:
            self.logger.info("Extracting section: %s", section_name)
            self.logger.info("Raw text length: %d", len(text))
            self.logger.info("Raw text preview: %s...", text[:200])
            
            lines = text.split('\n')
            section_start = -1
            section_end = -1
            section_name_lower = section_name.lower().strip()
            
            # Find section start (allow leading number and dot, ignore case)
            for i, line in enumerate(lines):
                line_clean = line.strip().lower()
                # Check for exact match
                if line_clean.startswith(section_name_lower):
                    section_start = i
                    self.logger.info("Found section start at line %d: %s", i, line.strip())
                    break
                # Check for numbered format (1. section name)
                if line_clean.startswith(tuple(f"{n}. " for n in range(1, 10))) and section_name_lower in line_clean:
                    section_start = i
                    self.logger.info("Found numbered section start at line %d: %s", i, line.strip())
                    break
                # Check for partial match (section name contains the key words)
                if section_name_lower in line_clean and len(line_clean) < 100:
                    section_start = i
                    self.logger.info("Found partial section start at line %d: %s", i, line.strip())
                    break
            
            if section_start == -1:
                self.logger.info("Section '%s' not found in response", section_name)
                return f"Section '{section_name}' not found in response"
            
            # Find section end by looking for next numbered section or end of text
            for i in range(section_start + 1, len(lines)):
                line = lines[i].strip()
                line_lower = line.lower()
                if (line and len(line) < 100 and (
                    (line[0].isdigit() and '.' in line[:5]) or
                    any(h in line_lower for h in [
                        'system scope and boundaries',
                        'architecture and technology stack',
                        'system-external interfaces and integrations',
                        'ci/cd pipelines',
                        'specific testing concept',
                        'deployment and operation environment',
                        'ux/ui design and prototyping'])
                )):
                    section_end = i
                    self.logger.info("Found section end at line %d: %s", i, line.strip())
                    break
            
            if section_end == -1:
                section_end = len(lines)
                self.logger.info("Section extends to end of text")
            
            # Extract the section content
            section_content = '\n'.join(lines[section_start:section_end]).strip()
            self.logger.info("Raw section content length: %d", len(section_content))
            
            # Remove the section header line itself
            if section_content.lower().startswith(section_name_lower) or any(section_content.lower().startswith(f"{n}. {section_name_lower}") for n in range(1, 10)):
                lines_content = section_content.split('\n')
                if len(lines_content) > 1:
                    section_content = '\n'.join(lines_content[1:]).strip()
                    self.logger.info("Removed header, new content length: %d", len(section_content))
            
            if not section_content:
                self.logger.info("Section '%s' is empty after processing", section_name)
                return f"Section '{section_name}' is empty"
            
            self.logger.info("Final section content preview: %s...", section_content[:100])
            return section_content
            
        except Exception as e:
            self.logger.info("Error extracting section '%s': %s", section_name, str(e))
            return f"Error extracting section '{section_name}': {str(e)}"
    
    def _extract_section_fallback(self, text: str, key: str, title: str) -> str:
        """Fallback method to extract content using keywords"""
        try:
            self.logger.info(f"Fallback extraction for {key}")
            
            # Define keywords for each section
            keywords = {
                "system_scope": ["scope", "boundaries", "stakeholders", "system"],
                "architecture_tech_stack": ["architecture", "technology", "stack", "framework", "components"],
                "external_interfaces": ["interfaces", "integrations", "apis", "external", "services"],
                "ci_cd": ["ci/cd", "continuous", "deployment", "pipeline", "automation"],
                "testing_concept": ["testing", "test", "quality", "assurance", "coverage"],
                "deployment_operation": ["deployment", "operation", "infrastructure", "monitoring", "scaling"],
                "ux_ui": ["ux", "ui", "user experience", "interface", "design", "prototyping"]
            }
            
            if key not in keywords:
                return ""
            
            lines = text.split('\n')
            relevant_lines = []
            
            for line in lines:
                line_lower = line.lower()
                # Check if line contains keywords for this section
                if any(keyword in line_lower for keyword in keywords[key]):
                    relevant_lines.append(line)
            
            if relevant_lines:
                content = '\n'.join(relevant_lines).strip()
                self.logger.info(f"Fallback found {len(relevant_lines)} relevant lines for {key}")
                return content
            else:
                self.logger.info(f"Fallback found no relevant lines for {key}")
                return ""
                
        except Exception as e:
            self.logger.info(f"Fallback extraction failed for {key}: {str(e)}")
            return ""
    


    def _review_section(self, key, content, original_content=None, check_dot_block=True):
        """Review a section based on dynamic descriptions from the file."""
        self.logger.info("Reviewing section: %s", key)
        self.logger.info("Content length: %d characters", len(content))
        self.logger.debug("Content preview: %s...", content[:200])
        
        try:
            self.logger.info("Loading section descriptions")
            section_descriptions = self._load_section_descriptions()
            if key not in section_descriptions:
                self.logger.error("Unknown section key: %s", key)
                return False, f"Unknown section key: {key}"
            
            section_data = section_descriptions[key]
            description = section_data.get('description', '')
            self.logger.info("Section description length: %d characters", len(description))
            
            # Check if we have JSON format with word_count configuration
            if isinstance(section_data, dict) and "word_count" in section_data:
                # Use JSON configuration directly
                word_count_config = section_data.get("word_count", {})
                min_words = word_count_config.get("min", 30)
                max_words = word_count_config.get("max", 100)
                
                self.logger.info("Using JSON word count config: min=%d, max=%d", min_words, max_words)
            else:
                # Fallback to old method
                max_words = self._extract_max_words_from_description(description)
                if max_words:
                    min_words, max_words_with_tolerance = self._get_word_count_tolerance(max_words)
                    self.logger.info("Word count tolerance: min=%d, max=%d", min_words, max_words_with_tolerance)
                    max_words = max_words_with_tolerance
                else:
                    self.logger.info("No word count requirement found in description")
                    min_words, max_words = 150, 325  # Default values
            
            # Calculate word count (moved outside if/else block)
            words = len(re.findall(r"\w+", content))
            self.logger.info("Actual word count: %d", words)
                
            if words < min_words or words > max_words:
                self.logger.warning("Section length out of bounds: %d words (min %d, max %d)", words, min_words, max_words)
                return False, f"Section length out of bounds: {words} words (min {min_words}, max {max_words})"
            else:
                self.logger.info("Word count within acceptable range")
            
            # DOT-Code-Block im Fließtext NICHT mehr prüfen
            self.logger.info("Checking content alignment")
            alignment_score = self._check_content_alignment(content, description)
            self.logger.info("Alignment score: %.2f", alignment_score)
            
            threshold = getattr(self, 'alignment_threshold', 0.6)
            self.logger.info("Alignment threshold: %.2f", threshold)
            
            if alignment_score < threshold:
                self.logger.warning("Content does not align well with section requirements (alignment score: %.2f)", alignment_score)
                return False, f"Content does not align well with section requirements (alignment score: {alignment_score:.2f})"
            
            self.logger.info("Section review passed successfully")
            return True, "ok"
        except Exception as e:
            self.logger.error("Error in review_section for %s: %s", key, e)
            return False, f"Review error: {str(e)}"
    
    def _extract_max_words_from_description(self, description: str) -> Optional[int]:
        """Extract maximum word count from description text."""
        # Look for patterns like "Maximum length: half a page" or "max 250 words"
        patterns = [
            r"Maximum length:\s*half a page",
            r"Maximum length:\s*one page", 
            r"Maximum length:\s*one third of a page",
            r"max\s+(\d+)\s+words",
            r"maximum\s+(\d+)\s+words"
        ]
        
        for pattern in patterns:
            if re.search(pattern, description, re.IGNORECASE):
                # All sections now use half a page (250 words)
                return 250
        
        # Default values if no length specification found in description
        default_limits = {
            "system_scope": 250,
            "architecture_tech_stack": 250,
            "external_interfaces": 250,
            "ci_cd": 250,
            "testing_concept": 250,
            "deployment_operation": 250,
            "ux_ui": 250
        }
        
        # Try to determine from section key in description
        for section_key, limit in default_limits.items():
            if section_key in description.lower():
                return limit
        
        return 250  # Default to half a page for all sections
    
    def _get_word_count_tolerance(self, max_words: int) -> tuple[int, int]:
        """Get the acceptable word count range with tolerance."""
        # Allow 30% tolerance above the limit (more generous)
        tolerance = int(max_words * 0.3)
        # Set minimum to 60% of max_words to ensure substantial content
        min_words = int(max_words * 0.6)  # 60% of max_words as minimum
        max_words_with_tolerance = max_words + tolerance
        
        return min_words, max_words_with_tolerance
    
    def _check_content_alignment(self, content: str, description: str) -> float:
        """Check how well the content aligns with the description requirements."""
        try:
            # Extract key topics from description
            description_lower = description.lower()
            content_lower = content.lower()
            
            # Define topic keywords based on description sections
            topics = []
            
            if "business" in description_lower:
                topics.extend(["business", "objective", "goal", "value", "roi"])
            if "stakeholder" in description_lower:
                topics.extend(["stakeholder", "user", "persona", "role"])
            if "boundary" in description_lower or "scope" in description_lower:
                topics.extend(["boundary", "scope", "include", "exclude"])
            if "requirement" in description_lower:
                topics.extend(["requirement", "functional", "non-functional"])
            if "architecture" in description_lower:
                topics.extend(["architecture", "component", "technology", "framework"])
            if "integration" in description_lower:
                topics.extend(["integration", "api", "interface", "external"])
            if "testing" in description_lower:
                topics.extend(["testing", "test", "quality", "coverage"])
            if "deployment" in description_lower:
                topics.extend(["deployment", "infrastructure", "monitoring"])
            if "design" in description_lower:
                topics.extend(["design", "ux", "ui", "user experience"])
            
            # Count how many topics are covered in content
            covered_topics = 0
            for topic in topics:
                if topic in content_lower:
                    covered_topics += 1
            
            # Calculate alignment score
            if topics:
                alignment_score = covered_topics / len(topics)
                return alignment_score
            else:
                return 0.5  # Default score if no topics found
                
        except Exception as e:
            self.logger.error(f"Error in content alignment check: {e}")
            return 0.5  # Default score on error

    def _review_section_with_ai(self, section_name, definition, content, provider):
        """Review a section using the AI, returning (score, reason)."""
        review_prompt = f"""You are an expert technical reviewer. Please review the following text for the section '{section_name}' according to these requirements: {definition}\n\nText:\n{content}\n\nGive a score from 0 to 100 based on how well the text fulfills ALL requirements. Then, in one line, output only: SCORE: <number> - <short reason>."""
        try:
            if provider == "openai":
                response = self._call_openai(review_prompt)
            elif provider == "ollama":
                response = self._call_ollama(review_prompt)
            else:
                return 0, "[REVIEW ERROR] Unsupported provider"
            import re
            m = re.search(r"SCORE:\s*(\d+)[^\d]*(.*)", response, re.IGNORECASE)
            if m:
                score = int(m.group(1))
                reason = m.group(2).strip()
                return score, reason
            else:
                return 0, f"[REVIEW ERROR] Could not parse score: {response.strip()}"
        except Exception as e:
            return 0, f"[REVIEW ERROR] {str(e)}"

    def _load_section_descriptions(self) -> Dict[str, Dict[str, Any]]:
        """Load section descriptions from JSON file or use defaults."""
        try:
            # Try to load from JSON file first
            json_path = "section_descriptions.json"
            if os.path.exists(json_path):
                self.logger.info("Loading section descriptions from JSON file: %s", json_path)
                with open(json_path, 'r', encoding='utf-8') as f:
                    descriptions = json.load(f)
                self.logger.info("Loaded %d section descriptions from JSON file", len(descriptions))
                return descriptions
        except Exception as e:
            self.logger.warning("Failed to load JSON descriptions: %s", str(e))
        
        try:
            # Fallback to text file
            txt_path = "section_descriptions.txt"
            if os.path.exists(txt_path):
                self.logger.info("Loading section descriptions from text file: %s", txt_path)
                return self._parse_text_descriptions(txt_path)
        except Exception as e:
            self.logger.warning("Failed to load text descriptions: %s", str(e))
        
        # Use defaults if no file found
        self.logger.info("Using default section descriptions")
        return self._get_default_section_descriptions()
    
    def _parse_text_descriptions(self, txt_path: str) -> Dict[str, Dict[str, str]]:
        """Parse text-based section descriptions (fallback method)."""
        descriptions = {}
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Parse the file content
            lines = content.split('\n')
            current_section = None
            current_data = {}
            in_description = False
            description_lines = []
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if line.startswith('[') and line.endswith(']'):
                    # Save previous section if exists
                    if current_section and current_data:
                        if description_lines:
                            current_data['description'] = '\n'.join(description_lines).strip()
                        descriptions[current_section] = current_data
                    
                    # Start new section
                    current_section = line[1:-1]  # Remove brackets
                    current_data = {}
                    in_description = False
                    description_lines = []
                    
                elif line.startswith('Section:'):
                    current_data['title'] = line.split(':', 1)[1].strip()
                    
                elif line.startswith('Description:'):
                    in_description = True
                    # Start collecting description lines
                    description_lines = []
                    
                elif in_description:
                    # Collect all lines until we hit the next section or another field
                    if line.startswith('[') or line.startswith('Section:'):
                        # We've hit the next section, stop collecting
                        in_description = False
                        if description_lines:
                            current_data['description'] = '\n'.join(description_lines).strip()
                        continue
                    else:
                        # Add line to description
                        description_lines.append(line)
            
            # Save last section
            if current_section and current_data:
                if description_lines:
                    current_data['description'] = '\n'.join(description_lines).strip()
                descriptions[current_section] = current_data
            
            self.logger.info("Loaded %d section descriptions from text file", len(descriptions))
            return descriptions
            
        except Exception as e:
            self.logger.error("Error parsing text descriptions: %s", str(e))
            return {}
    
    def _get_default_section_descriptions(self) -> Dict[str, Dict[str, str]]:
        """Fallback default descriptions if file is not found."""
        return {
            "system_scope": {
                "title": "System Scope and Boundaries",
                "description": "Describe the system's purpose and function, what is included and excluded, target users, and constraints. At the very end, add a valid Graphviz DOT code block (```dot ... ```) that visualizes the system scope, boundaries, stakeholders, and main components. Do NOT use Mermaid or any other diagram code. Do NOT add any other content. Maximum length: half a page."
            },
            "architecture_tech_stack": {
                "title": "Architecture and Technology Stack",
                "description": "Describe the architecture model (e.g., microservices, monolith), core technologies and frameworks, data storage, and communication. At the very end, add a valid Graphviz DOT code block (```dot ... ```) that shows the main components, their relationships, and key technologies. Do NOT use Mermaid or any other diagram code. Do NOT add any other content. Maximum length: half a page."
            },
            "external_interfaces": {
                "title": "System-external Interfaces and Integrations",
                "description": "Describe external systems and interface types, authentication, and responsibilities. Do NOT add any other content. Maximum length: half a page."
            },
            "ci_cd": {
                "title": "CI/CD Pipelines",
                "description": "Describe tools and stages (build, test, deploy), security, and quality assurance. Do NOT add any other content. Maximum length: half a page."
            },
            "testing_concept": {
                "title": "Specific Testing Concept",
                "description": "Describe test types (unit, E2E, etc.), tools and metrics, and handling of AI tests. Do NOT add any other content. Maximum length: half a page."
            },
            "deployment_operation": {
                "title": "Deployment and Operation Environment",
                "description": "Describe infrastructure (cloud, containers, orchestration), monitoring, and operations. Do NOT add any other content. Maximum length: half a page."
            },
            "ux_ui": {
                "title": "UX/UI Design and Prototyping",
                "description": "Describe design tools and processes, responsive design, and accessibility. Do NOT add any other content. Maximum length: half a page."
            }
        }

    def generate_technical_concept_sections(self, project_description: str, provider: str = "openai", proposal_context: str = "", cancel_callback=None) -> Dict[str, Any]:
        self.logger.info("Starting section-by-section technical concept generation")
        self.logger.info("Provider: %s", provider)
        self.logger.info("Project description length: %d", len(project_description))
        self.logger.info("Proposal context provided: %s", bool(proposal_context and proposal_context.strip()))
        
        section_descriptions = self._load_section_descriptions()
        self.logger.info("Loaded %d section descriptions", len(section_descriptions))
        
        results = {}
        threshold = getattr(self, 'alignment_threshold', 0.6)
        self.logger.info("Alignment score threshold: %.2f", threshold)
        
        for key, section_data in section_descriptions.items():
            # Skip documentation or invalid entries
            if not isinstance(section_data, dict) or 'title' not in section_data:
                self.logger.info("Skipping non-section entry: %s", key)
                continue
            self.logger.info("Processing section: %s", key)
            
            if cancel_callback and callable(cancel_callback) and cancel_callback():
                self.logger.info("Generation cancelled before section %s", key)
                break
                
            title = section_data["title"]
            
            # Handle both old text format and new JSON format
            if isinstance(section_data, dict) and "word_count" in section_data:
                # New JSON format
                definition = section_data["description"]
                word_count_config = section_data.get("word_count", {})
                target_words = word_count_config.get("target", 70)
                min_words = word_count_config.get("min", 30)
                max_words = word_count_config.get("max", 100)
                
                self.logger.info("Section title: %s", title)
                self.logger.info("Section definition length: %d", len(definition))
                self.logger.info("Word count config: target=%d, min=%d, max=%d", target_words, min_words, max_words)
                
                word_count_instruction = f"\n\nWORD COUNT REQUIREMENTS:\n- Minimum: {min_words} words\n- Maximum: {max_words} words\n- Target: {target_words} words\n\n"
                self.logger.info("Word count requirements: min=%d, max=%d, target=%d", min_words, max_words, target_words)
            else:
                # Old text format
                definition = section_data["description"]
                self.logger.info("Section title: %s", title)
                self.logger.info("Section definition length: %d", len(definition))
                
                max_words = self._extract_max_words_from_description(definition)
                if max_words:
                    min_words, max_words_with_tolerance = self._get_word_count_tolerance(max_words)
                    word_count_instruction = f"\n\nWORD COUNT REQUIREMENTS:\n- Minimum: {min_words} words\n- Maximum: {max_words_with_tolerance} words\n- Target: {max_words} words\n\n"
                    self.logger.info("Word count requirements: min=%d, max=%d, target=%d", min_words, max_words_with_tolerance, max_words)
                else:
                    word_count_instruction = "\n\nWORD COUNT REQUIREMENTS:\n- Minimum: 150 words\n- Maximum: 400 words\n- Target: 250 words\n\n"
                    self.logger.info("Using default word count requirements")
                

                
            previous_errors = []
            section_accepted = False
            best_attempt = None  # (score, content, reason)
            best_score = float('-inf')
            best_content = None
            best_reason = None
            # 1. Fließtext generieren (ohne Diagramm)
            self.logger.info("Starting text generation for section: %s", key)
            for attempt in range(10):
                self.logger.info("Text generation attempt %d/10 for section: %s", attempt + 1, key)
                if cancel_callback and callable(cancel_callback) and cancel_callback():
                    self.logger.info("Generation cancelled during section %s, attempt %d", key, attempt + 1)
                    break
                # Verwende nur die spezifische Beschreibung für diese Sektion
                section_description = definition
                self.logger.info("Using section-specific description for %s: %d characters", key, len(section_description))
                prompt = f"""You are an expert software architect and technical writer. Your task is to write ONLY the following section of a technical concept for a software project, in clear professional English. Do NOT add any other sections, summaries, introductions, conclusions, bullet points, lists, or headings.\n\nSection: {title}\n\nProject Description:\n{project_description}"""
                if proposal_context and proposal_context.strip():
                    prompt += f"\n\nExisting Proposal Context:\n{proposal_context}"
                # Verwende nur die spezifische Beschreibung für diese Sektion
                prompt += f"\n\nInstructions:\n{section_description}{word_count_instruction}Output ONLY the content for this section. Do NOT include the section header or any other text. Do NOT include any diagram or code block."
                if attempt > 0 and previous_errors:
                    error_context = "\n".join([f"- {error}" for error in previous_errors])
                    prompt += f"\n\nIMPORTANT: The previous attempt failed due to these issues. Please ensure you address ALL of these problems:\n{error_context}\n\nMake sure to fix these specific issues in your response."
                    self.logger.info("Adding error context from previous attempts: %d errors", len(previous_errors))
                self.logger.debug("Text generation prompt length: %d", len(prompt))
                if provider == "openai":
                    response = self._call_openai(prompt)
                elif provider == "ollama":
                    response = self._call_ollama(prompt)
                else:
                    self.logger.error("Unsupported AI provider: %s", provider)
                    raise ValueError(f"Unsupported AI provider: {provider}")
                content = response.strip()
                self.logger.info("Generated content length: %d characters", len(content))
                # Review prüft nicht mehr auf DOT-Code-Block im Fließtext
                self.logger.info("Reviewing generated content")
                score, reason = self._review_section(key, content, content, check_dot_block=False)
                self.logger.info("Section %s review result: score=%s, reason=%s", key, score, reason)
                # Speichere bestes Ergebnis
                if isinstance(score, (int, float)) and score > best_score:
                    best_score = score
                    best_content = content
                    best_reason = reason
                if score:
                    results[key] = {"text": content}
                    section_accepted = True
                    self.logger.info("Section %s accepted after %d attempts", key, attempt + 1)
                    break
                else:
                    previous_errors.append(reason)
                    self.logger.warning("Section %s rejected (attempt %d): %s", key, attempt + 1, reason)
                    if attempt == 9:
                        self.logger.warning("Section %s using best effort after 10 failed attempts", key)
                        if best_content is not None:
                            results[key] = {"text": f"[BEST EFFORT]\n{best_content}\n\n[REVIEW] {best_reason}"}
                        else:
                            results[key] = {"text": f"[BEST EFFORT]\n{content}\n\n[REVIEW] {reason}"}
            
            
        
        self.logger.info("Section-by-section generation completed. Generated %d sections", len(results))
        return {"sections": results, "metadata": {"generated_by": "Zeta Proposer", "mode": "section_by_section_ai_reviewed_graphviz"}} 

    def generate_project_name(self, project_description: str, provider: str = "openai") -> str:
        """Generate a project name from the project description using AI."""
        prompt = (
            "Generate a short, clear, and professional project name (max 7 words, no quotes, no punctuation at the end) "
            "for the following software project. Only output the name, nothing else.\n\n"
            f"Project Description:\n{project_description}"
        )
        self.logger.info("Generating project name with provider: %s", provider)
        if provider == "openai":
            name = self._call_openai(prompt)
        elif provider == "ollama":
            name = self._call_ollama(prompt)
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
        # Nur die erste Zeile nehmen und ggf. trimmen
        return name.strip().split('\n')[0].strip('"') 