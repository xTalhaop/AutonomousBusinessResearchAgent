# agent_3.py
import os
import pypandoc
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def run_formatter_agent(raw_filepath: str, topic: str) -> str:
    """
    Reads the raw scraped data, uses Gemini to synthesize a professional
    business report, and converts it to a DOCX file using Pandoc.
    """
    print("\n[Agent 3] Activating... Reading raw data and synthesizing report.")

    # 1. Read the messy raw data from the file Agent 2 created
    try:
        with open(raw_filepath, 'r', encoding='utf-8') as file:
            raw_data = file.read()
    except Exception as e:
        return f"Agent 3 Error: Could not read raw file. {e}"

    if len(raw_data) < 50:
        return "Agent 3 Error: Raw data file is empty or too short."

    # 2. Instruct Gemini to act as a Business Consultant
    system_instructions = """
    You are an expert Business Consultant. Your job is to take raw, messy web-scraped 
    text and synthesize it into a highly structured, professional business report.

    RULES:
    1. Base your report ONLY on the provided scraped text. Ignore navigation menus and ads.
    2. Use professional Markdown formatting (Headers: #, ##, Bullet points: -, Bold text: **).
    3. Structure the report exactly like this:
       - # Executive Summary
       - ## Market Overview
       - ## Step-by-Step Guide to Starting
       - ## Estimated Costs & Financials
       - ## Key Risks & Mitigation
    4. Make the tone professional, objective, and easy to read.
    """

    print("[Agent 3] Sending data to Gemini for structuring...")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=f"Topic: {topic}\n\nRAW SCRAPED DATA:\n{raw_data}",
            config=types.GenerateContentConfig(
                system_instruction=system_instructions,
                temperature=0.3  # Low temperature for factual structuring
            )
        )

        cleaned_markdown = response.text

        # 3. Save the Cleaned Markdown temporarily
        base_filename = topic.replace(" ", "_").lower()
        cleaned_md_path = f"{base_filename}_final_report.md"
        docx_path = f"{base_filename}_Business_Plan.docx"

        with open(cleaned_md_path, "w", encoding="utf-8") as file:
            file.write(cleaned_markdown)

        print("[Agent 3] AI structuring complete. Converting to DOCX with Pandoc...")

        # 4. Use Pypandoc to convert the cleaned Markdown into a DOCX file
        try:
            # We tell pandoc to read markdown and write docx
            pypandoc.convert_file(cleaned_md_path, 'docx', outputfile=docx_path)
            print(f"[Agent 3] Success! Final document saved as: {docx_path}")
            return docx_path
        except Exception as pandoc_err:
            print(f"Pandoc Error (Is Pandoc installed on your OS?): {pandoc_err}")
            return cleaned_md_path  # Fallback to returning the MD file if Pandoc fails

    except Exception as e:
        print(f"Agent 3 Error during AI generation: {e}")
        return ""