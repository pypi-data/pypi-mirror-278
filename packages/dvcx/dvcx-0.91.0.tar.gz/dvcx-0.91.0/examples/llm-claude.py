import os

import pandas as pd

from dvcx.lib.claude import Claude, ClaudeMessage
from dvcx.lib.dataset import Dataset
from dvcx.lib.file import File
from dvcx.query.schema import C

SOURCE = "s3://ldb-public/remote/chatbots-public/"
MODEL = "claude-3-opus-20240229"
PROMPT = """Summarise the dialog in a sentence"""

ds = (
    Dataset(SOURCE, anon=True)
    .filter(C.name.glob("*.txt"))
    .limit(5)
    .map(
        ClaudeMessage(
            prompt=PROMPT,
            model_name=MODEL,
            temperature=0.9,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        ),
        parallel=3,
        cache=True,
    )
)

df = ds.select(File.name, Claude).to_pandas()

with pd.option_context("display.max_columns", None):
    print(df)
