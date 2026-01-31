import os
from openai import OpenAI
from tools import write_file, summarize_text

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TOOLS = {
    "write_file": write_file,
    "summarize_text": summarize_text
}

SYSTEM_PROMPT = """
You are an AI automation agent.

Process:
1. Given a goal, break it into steps.
2. Propose which tool to use.
3. WAIT for user approval before execution.
4. When approved, output:
   TOOL: <tool_name>
   ARGS: <arguments>

Only use tools that exist.
"""

def plan(goal):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": goal}
        ]
    )
    return response.choices[0].message.content


def execute(tool_name, args):
    if tool_name in TOOLS:
        return TOOLS[tool_name](**args)
    else:
        return "Unknown tool."

