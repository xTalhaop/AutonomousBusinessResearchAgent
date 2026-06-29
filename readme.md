# Autonomous Business Research Agent

An intelligent, multi-agent Python pipeline that autonomously researches any business or startup topic, scrapes live verified sources, and synthesizes the data into a professional, ready-to-read Word Document (`.docx`).

This project demonstrates a fully functional **Agentic Architecture** where specific tasks are delegated to specialized AI agents and deterministic Python tools, all controlled by a central orchestrator.

---

## Key Features

* **Zero-Hallucination Searching:** Uses native Python libraries (DuckDuckGo Search) to interact with the live internet, ensuring the AI only processes real, existing URLs.
* **Auto-Validation Layer:** Actively pings every discovered URL and filters out 403/404 errors *before* passing data to the scraper, saving compute time and API quotas.
* **Raw Data Lake:** Automatically saves unedited, scraped text to a local `.md` backup file. If you want to re-format the final report, you don't have to waste time or API calls re-scraping the web.
* **Automated Document Generation:** Leverages `pypandoc` to automatically convert AI-generated Markdown into a clean, formatted `.docx` business plan.

---

## System Architecture

The pipeline consists of three specialized agents orchestrated by a master script:

1. **`main.py` (The Orchestrator):** The controller that takes user input, passes data variables between agents, and manages the file saving processes.
2. **`agent_1.py` (The Searcher):** Uses Gemini to interpret the query, triggers a deterministic Python search tool, verifies link health, and outputs a clean JSON array of active URLs.
3. **`agent_2.py` (The Scraper):** A deterministic Python agent (Zero AI). It takes the JSON URLs, crawls the sites, strips away HTML clutter/menus using BeautifulSoup, and extracts pure readable text.
4. **`agent_3.py` (The Synthesizer):** Reads the massive raw text dump, uses Gemini (acting as a Business Consultant) to structure the data into a professional report, and exports it to Word.

---

## Prerequisites

Before running the pipeline, ensure you have the following installed:

1. **Python 3.8+**
2. **A Google Gemini API Key:** Get a free key from [Google AI Studio](https://aistudio.google.com/).
3. **Pandoc (Required for Word Export):** * **Windows:** Download and run the standard `.msi` installer from the [Pandoc Releases Page](https://github.com/jgm/pandoc/releases).
   * *Critical:* After installing Pandoc, you **must** close and restart your terminal/code editor so Python can recognize the new system PATH.

---

