import os

import pandas as pd

from dvcx.lib.claude import AggregateTextAnalytics, Summary
from dvcx.lib.dataset import Dataset
from dvcx.query.schema import C
from dvcx.sql.functions import path

SOURCE = "s3://ldb-public/remote/chatbots-public/"
model = "claude-3-opus-20240229"

PROMPT = """Consider the following dialogues between the 'user' and the 'bot' separated\
 by '===='. The 'user' is a human trying to find the best mobile plan. The 'bot' is a \
chatbot designed to query the user and offer the best solution. The dialog is \
successful if the 'bot' is able to gather the information and offer a plan, or inform \
the user that such plan does not exist. The dialog is not successful if the \
conversation ends early or the 'user' requests additional functions the 'bot' \
cannot perform. Read the dialogues and classify them into a fixed number of concise \
failure reasons covering most failure cases. Present output as JSON list of reason \
strings and nothing else.
"""

chats = Dataset(SOURCE, anon=True).filter(C.name.glob("*.txt"))

content = chats.limit(50).aggregate(
    AggregateTextAnalytics(
        prompt=PROMPT,
        model_name=model,
        messages=[
            {
                "role": "assistant",
                "content": "Here is the JSON object in curly brackets:",
            }
        ],
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    ),
    partition_by=path.file_ext(C.name),
)

with pd.option_context("display.max_columns", None):
    df = content.select(Summary).to_pandas()
    print(df)

    errors = df[df.summary__error != ""]
    if len(errors) > 0:
        print("Errors: ", len(errors))
