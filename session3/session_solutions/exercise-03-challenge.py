import os
from openai import OpenAI

## The QWEN LLm model is a smaller model, and version '7B' on its own indicates the BASE model which is not chat compliant - added the 'INSTRUCT' verison of the LLM model
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
TEXT_FILE = "session3/les_miserables.txt"
CHUNK_SIZE = 30
MAX_CHUNKS = 3

## Note: Need to be registered via a platform first to get the API Key for authentication with QWEN LLM, I used HuggingFace, signed up and then retrieved a random API key -- 
## defined here as OPEN_API_KEY variable/secret
def ask_openai(prompt):
    client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)
    response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
      ],
    )
    
    return response.choices[0].message

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
    ##Instructing the LLM to return text in English only as QWEN defaults to Chinese and my Chinese is not great...
    return f""""You are in STRICT EXTRACTION MODE.

RULES:
1. Use ONLY information inside the SOURCE block.
2. If something is not explicitly in the source, output "NOT PRESENT".
3. Do NOT infer, guess, or add context.
4. Do NOT use metadata (title, author, translator, URLs, dates).
5. Characters must be human individuals explicitly named in the text.
6. Events must be actions explicitly described in the text.
7. Summary must contain ONLY facts from the source.
8. If the source contains no characters/events, return empty lists.
9. If unsure, choose "NOT PRESENT".

STEP 1 — QUOTE EXTRACTION:
List 3–5 direct quotes from the SOURCE TEXT that support your output.
If no quotes exist, output ["NO QUOTES PRESENT"].

STEP 2 — STRUCTURED OUTPUT:
Return only valid JSON with these keys:
{{
  "chunk": {chunk_number},
  "characters": [string],
  "events": [string],
  "summary": string,
  "uncertainty": [string]
}}

Chunk number: {chunk_number}

    Excerpt:
    SOURCE TEXT (use ONLY what is inside this block):
    <<<SOURCE
    {chunk_text}
    SOURCE>>>
    """

for chunk_number, chunk_text in enumerate(
    book_chunks(TEXT_FILE, chunk_size=CHUNK_SIZE, max_chunks=MAX_CHUNKS),
    start=1,
):
    prompt = build_summary_prompt(chunk_text, chunk_number)
    summary = ask_openai(prompt)
    print(f"Chunk {chunk_number}")
    print(summary)
    print()

    ## Key Takeaways/Findings:
    # Following testing: The QWEN LLM 5B and Instruct models were smaller models that hallucinated, and inferred content, it also did not handle translation well
    # In addition, QWEN kept hallucinating unless specific restrictive instructions were provided following testing
    # Instead I used a larger model QWEN version '7B' on its own indicates the BASE model which is not chat compliant - added the 'INSTRUCT' verison of the LLM model and ran with 
    ## greater accuracy within clear instruction parameters

