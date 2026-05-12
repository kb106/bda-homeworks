import os
from google import genai

MODEL_NAME = "gemini-2.5-flash"
TEXT_FILE = "session3/les_miserables.txt"
CHUNK_SIZE = 30
MAX_CHUNKS = 3

def ask_gemini(prompt):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return response.text

def book_chunks(path, chunk_size=30, max_chunks=3):
    chunk = []
    chunks_sent = 0

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue

            # Build small chunks of text iterating line-by-line through the text file. When the chunk reaches the specified chunk size, yield it and start a new chunk.
            if len(chunk) >= chunk_size:
                # yield join with chunkof txt with space as separator
                yield " ".join(chunk)
                chunk = []
                # iterate with an increment for each line read and chunk sent, if the number of chunks sent reaches the max_chunks, stop the iteration
                chunks_sent += 1
                if chunks_sent >= max_chunks:
                    print(f"Reached maximum number of chunks ({max_chunks}). Stopping.")
                    return

            else:
                chunk.append(line)

    # Provide here your solution
    return " ".join(chunk)


def build_summary_prompt(chunk_text, chunk_number):
    # Prompt use to summarise txt chunk, include the chunk number in the prompt to provide context to the model about which part of the book it is summarizing.
    return f""""Summarize one chunk from Les Miserables

    Return only valid JSON with these keys:
    - chunk: the chunk number
    - characters: important character names mentioned
    - events: short event descriptions
    - summary: a 2-3 sentence summary
    - uncertainty: anything unclear

    Rules:
    - Do not include Markdown fences.
    - Do not add commentary outside the JSON.
    - If there are no clear events, use an empty list.

    Chunk number: {chunk_number}

    Excerpt:
    {chunk_text}
    """

for chunk_number, chunk_text in enumerate(
    book_chunks(TEXT_FILE, chunk_size=CHUNK_SIZE, max_chunks=MAX_CHUNKS),
    start=1,
):
    prompt = build_summary_prompt(chunk_text, chunk_number)
    summary = ask_gemini(prompt)
    print(f"Chunk {chunk_number}")
    print(summary)
    print()

## 1. Which tasks were best solved with streaming?
## Line by line reading of the file using yield was the best solution as it is more process efficient.
## 2. Which tasks required loading all data?
## Building the prompt for Google Gemini involved loading the entire text, which periodically caused memory issues, and created a timeout with the Gemini API.
## 3. Why is a generator with `yield` still an iterator?
## Because we still need to stream the text line by line to yield the output.
## 4. When does `yield` save memory compared with `readlines()`?
## Yield saves memory as it reads line by line, it can also be made more process efficient when a break is included immediately after it is called.
## 5. Why is sending the whole book to Gemini in one prompt a bad idea?
## Gemini may not respond and may also cause memory issues as it may not be able to process all text at once.
