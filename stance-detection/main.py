from typing import Optional
import pandas as pd
from client import Client
import prompts


def divide_df_into_chunks(df: pd.DataFrame, chunks_quantity: int) -> list[pd.DataFrame]:
    chunks = []
    chunk_size = len(df) // chunks_quantity
    for i in range(0, len(df), chunk_size):
        chunks.append(df[i : i + chunk_size])
    return chunks


def get_summary_for_chunk(
    chunk: pd.DataFrame, previous_context: Optional[str] = None
) -> str:
    csv_to_prompt = chunk.to_csv(index=False)
    client = Client()
    response = client.get_response_gpt3(
        prompt=prompts.summarization_prompt(csv_to_prompt, previous_context),
        system=prompts.get_system(),
    )

    if not response:
        raise ValueError(f"Response is empty for chunk {chunk}")

    return response


def main():
    meetings = pd.read_csv("meetings.csv")
    meeting = meetings[meetings["id_session"] == 25355]

    chunks = divide_df_into_chunks(meeting, 10)

    previous_context = None
    for chunk in chunks[: len(chunks) - 1]:
        summary = get_summary_for_chunk(chunk, previous_context)
        previous_context = summary

    summary = get_summary_for_chunk(chunks[-1], previous_context)

    with open("response.json", "w") as f:
        if summary:
            f.write(summary)


if __name__ == "__main__":
    main()
