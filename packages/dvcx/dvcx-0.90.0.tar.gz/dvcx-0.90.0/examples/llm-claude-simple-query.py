import os

import pandas as pd

from dvcx.lib.claude import (
    Rating,
    TextAnalytics,
)
from dvcx.lib.dataset import Dataset
from dvcx.lib.file import File
from dvcx.query.schema import C

SOURCE = "s3://ldb-public/remote/chatbots-public/"
model = "claude-3-opus-20240229"

PROMPT = """Consider the dialogue between the 'user' and the 'bot'. \
The 'user' is a human trying to find the best mobile plan. \
The 'bot' is a chatbot designed to query the user and offer the \
best  solution. The dialog is successful if the 'bot' is able to \
gather the information and offer a plan, or inform the user that \
such plan does not exist. The dialog is not successful if the \
conversation ends early or the 'user' requests additional functions \
the 'bot' cannot perform. Read the dialogue below and rate it 'Success' \
if it is successful, and 'Failure' if not. After that, provide \
one-sentence explanation of the reasons for this rating. Use only \
JSON object as output with the keys 'status', and 'explanation'.
"""

chats = Dataset(SOURCE, anon=True).filter(C.name.glob("*.txt")).limit(5)

content = chats.map(
    TextAnalytics(
        prompt=PROMPT,
        model_name=model,
        temperature=0.9,
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    ),
    parallel=3,
)

with pd.option_context("display.max_columns", None):
    df = content.select(File.name, Rating).to_pandas()
    print(df)

    errors = df[df.rating__error != ""]
    if len(errors) > 0:
        print("Errors: ", len(errors))
