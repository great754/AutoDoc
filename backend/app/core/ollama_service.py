import requests
import json
from typing import Optional


class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "gpt-oss:120b-cloud"

    def generate_analysis(
        self,
        project_name: str,
        purpose: str,
        business_summary: str,
        stakeholders: list,
        flow_content: Optional[str] = None,
    ) -> str:
        """
        Send process metadata to Ollama for analysis.

        Args:
            project_name: Name of the RPA project
            purpose: Why the project exists
            business_summary: High-level process description
            stakeholders: List of stakeholder info
            flow_content: Power Automate flow XML (optional)

        Returns:
            Analysis text from Ollama
        """
        # Truncate flow content if too large (leave room for prompt + response)
        MAX_FLOW_CHARS = 50000  # ~12,500 tokens, leaving room for prompt and response
        truncated = False
        if flow_content and len(flow_content) > MAX_FLOW_CHARS:
            print(f"Flow content too large ({len(flow_content)} chars). Truncating to {MAX_FLOW_CHARS} chars")
            flow_content = flow_content[:MAX_FLOW_CHARS]
            truncated = True

        # Build comprehensive prompt
        prompt = self._build_prompt(
            project_name, purpose, business_summary, stakeholders, flow_content, truncated
        )

        try:
            # Call Ollama API
            print(f"Sending prompt to Ollama:\n{prompt[:500]}...")  # Log first 500 chars of prompt
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "temperature": 0.7,
                },
                timeout=300,  # 5 minute timeout for model processing
                stream=True,
            )

            print(f"Response status code: {response.status_code}")

            # Check for HTTP errors
            if response.status_code != 200:
                error_text = response.text
                print(f"Error response: {error_text}")
                raise Exception(f"HTTP {response.status_code}: {error_text}")

            print("Received response from Ollama, processing stream...")

            # Handle streaming responses
            full_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if chunk.get("response"):
                        full_response += chunk.get("response", "")
                    if chunk.get("done"):
                        break

            print(f"Analysis complete. Response length: {len(full_response)}")
            return full_response if full_response else "No response from Ollama"

        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {str(e)}")
            raise ConnectionError(
                f"Could not connect to Ollama at {self.base_url}. "
                "Make sure Ollama is running with: `ollama serve`"
            )
        except requests.exceptions.Timeout as e:
            print(f"Timeout error: {str(e)}")
            raise TimeoutError("Ollama request timed out (exceeded 5 minutes)")
        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Ollama error: {str(e)}")

    def _build_prompt(
        self,
        project_name: str,
        purpose: str,
        business_summary: str,
        stakeholders: list,
        flow_content: Optional[str] = None,
        truncated: bool = False,
    ) -> str:
        """Build a comprehensive prompt for Ollama analysis."""
        stakeholder_text = "\n".join(
            [f"- {s.get('name', 'Unknown')} ({s.get('role', 'Unknown role')})" for s in stakeholders]
        )

        prompt = f"""Analyze the following RPA (Robotic Process Automation) process and provide comprehensive documentation:

PROJECT NAME: {project_name}

PURPOSE:
{purpose}

BUSINESS SUMMARY:
{business_summary}

STAKEHOLDERS:
{stakeholder_text}
"""

        if flow_content:
            truncation_notice = "\n[Note: Flow content was truncated to fit context limits. Analysis based on first 50,000 characters.]" if truncated else ""
            prompt += f"""
POWER AUTOMATE FLOW{truncation_notice}:
{flow_content}
"""

        prompt += """
Please provide:
1. A detailed process description explaining what happens at each step
2. Key business value and benefits
3. Potential risks or failure points
4. Data inputs and outputs
5. Integration points with other systems
6. Recommended improvements or optimizations
7. Estimated processing time per record (if applicable)
8. Success metrics and KPIs

Format your response in clear sections with markdown formatting."""

        return prompt


# Create a singleton instance
ollama_service = OllamaService()
