import pandas as pd
from client import Client
import prompts


def main():
    meetings = pd.read_csv("meetings.csv")
    meeting = meetings[meetings["id_session"] == 25355]

    csv_to_prompt = meeting.to_csv(index=False)

    client = Client()
    response = client.get_response(
        prompt=prompts.classification_prompt(csv_to_prompt),
        system=prompts.get_system(),
    )
    print(response)

    with open("response.json", "w") as f:
        f.write(response)


if __name__ == "__main__":
    main()
