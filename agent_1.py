# agent_1.py
import json
import os
import requests
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


# =====================================================================
# THE DETERMINISTIC TOOL
# =====================================================================
def verified_web_search_tool(query: str) -> str:
    """
    Searches the live web for a query, checks every URL to ensure it is active,
    and returns a clean JSON array of verified working links (no 404s).
    """
    print(f"\n[Tool Executing] Searching the web for: '{query}'...")
    raw_urls = []
    valid_urls = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=8))
            for result in results:
                raw_urls.append(result['href'])

        print("[Tool Executing] Validating link health... filtering out broken pages.")

        for url in raw_urls:
            try:
                response = requests.get(url, headers=headers, timeout=3)
                if response.status_code == 200:
                    valid_urls.append(url)
                    if len(valid_urls) == 5:
                        break
            except requests.RequestException:
                continue

    except Exception as e:
        print(f"Tool Internal Error: {e}")

    return json.dumps(valid_urls)


# =====================================================================
# THE AI AGENT (Updated to use 'chats.create' for automatic tool execution)
# =====================================================================
def run_research_agent(user_query: str) -> str:
    system_instructions = """
    You are a Research Agent (Agent 1) in a multi-agent startup pipeline.
    Your only job is to provide high-quality, verified URLs related to the user's business query.

    CRITICAL PROTOCOL:
    1. You MUST call the `verified_web_search_tool` to discover links.
    2. Once you receive the list from the tool, output ONLY the URLs inside a raw JSON array of strings.
    3. DO NOT wrap the output in markdown block markers (e.g., do not write ```json ... ```).
    4. Do not include any explanations, greetings, or conversational filler.
    """

    try:
        # 1. Use client.chats.create() to enable AUTOMATIC tool running
        chat_session = client.chats.create(
            model='gemini-2.5-flash-lite',
            config=types.GenerateContentConfig(
                system_instruction=system_instructions,
                tools=[verified_web_search_tool],
                temperature=0.1,  # Keep temperature low so it strictly follows JSON rules
            )
        )

        # 2. Send the message to trigger the flow
        response = chat_session.send_message(user_query)
        output = response.text.strip()

        # 3. Failsafe: Clean up the output if the AI accidentally adds markdown backticks
        if output.startswith("```"):
            output = output.replace("```json", "").replace("```", "").strip()

            print(f"\n[Agent 1 Output Generated]:\n{output}\n")
        return output

    except Exception as e:
        print(f"\nAgent 1 Execution Failed: {e}")
        return "[]"