from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner

SYSTEM_INSTRUCTIONS = """
You are a PII redaction orchestrator.
When the user asks you to redact a document with a file name, you MUST:
1. First call the `pdf_to_image` MCP tool with that file name to convert the pdf to image
2. Take the returned file name from the previous step and call the 'pii_toolset' MCP tool
2. Report success or failure when the tool call returns
Do NOT guess or do anything else; always defer to the MCP tools.
"""
# SYSTEM_INSTRUCTIONS = """
# You are a PDF to PNG converter.
# When the user gives you a file name, you MUST:
# 1. Call the `pdf_to_image` MCP tool with that file name
# 2. Report success or failure when the tool call returns
# Do NOT guess or do anything else; always defer to the MCP tool.
# """

root_cloaker_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="root_cloaker_agent",
    instruction=SYSTEM_INSTRUCTIONS,
    tools=[pdf_to_image, pii_toolset],  # <- your MCP tools live here
)