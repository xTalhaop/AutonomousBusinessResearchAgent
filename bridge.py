# main.py
from agent_1 import run_research_agent
from agent_2 import scrape_urls_agent
from agent_3 import run_formatter_agent

def main():
    print("=== STARTING THE FULL BUSINESS RESEARCH PIPELINE ===")

    # 1. Get the topic
    user_query = input("Enter the business or startup topic: ")

    # 2. Agent 1: Find the links
    print("\n[Phase 1] Searching for verified sources...")
    agent_1_output_json = run_research_agent(user_query)

    # 3. Agent 2: Scrape the raw text
    print("\n[Phase 2] Extracting raw text from websites...")
    agent_2_output_text = scrape_urls_agent(agent_1_output_json)

    # 4. Save the Raw Data
    print("\n[Phase 3] Saving raw data to a backup Markdown file...")
    raw_filename = user_query.replace(" ", "_").lower() + "_raw_data.md"

    with open(raw_filename, "w", encoding="utf-8") as file:
        file.write(f"# Raw Scraped Data: {user_query.title()}\n\n")
        file.write(agent_2_output_text)

    print(f"Raw data saved to: {raw_filename}")

    # 5. Agent 3: Synthesize and Convert to DOCX
    print("\n[Phase 4] Formatting into professional document...")
    # We pass the filepath of the raw data to Agent 3
    final_doc = run_formatter_agent(raw_filepath=raw_filename, topic=user_query)

    print("\n=== PIPELINE COMPLETE ===")
    print(f"Your final business plan is ready: {final_doc}")


if __name__ == "__main__":
    main()