from typing import Optional, Union
import pandas as pd
from client import Client
import prompts


def divide_df_into_chunks(df: Union[pd.DataFrame, pd.Series], chunks_quantity: int) -> list[pd.DataFrame]:
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

def get_summaries(id_session: int):
    meetings = pd.read_csv("meetings.csv")
    meeting = meetings[meetings["id_session"] == id_session]

    chunks = divide_df_into_chunks(meeting, 10)

    summaries_file = open('summaries.txt', 'a')

    previous_context = None
    for chunk in chunks[: len(chunks) - 1]:
        summary = get_summary_for_chunk(chunk, previous_context).replace('```', '')

        summaries_file.write(summary)
        summaries_file.write('\n')

        previous_context = summary

    summary = get_summary_for_chunk(chunks[-1], previous_context)
    summaries_file.write(summary)

    summaries_file.close()

def get_stances():
    summaries_file = open('summaries.txt', 'r')

    all_summaries = summaries_file.read()
    summaries_file.close()

    client = Client()
    response = client.get_response_gpt3(
        prompt=prompts.summarization_prompt_for_stances(all_summaries),
        system=prompts.get_stance_system(),
    )

    if not response:
        raise ValueError(f"Response is empty for stances")

    with open('stances.json', 'w') as f:
        f.write(response)

def main():
    get_summaries(25355)
    get_stances()


if __name__ == "__main__":
    main()
