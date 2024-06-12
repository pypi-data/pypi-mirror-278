import datetime
import json

from dvcx.dataset import DatasetRow
from dvcx.storage import StorageURI
from dvcx.utils import JSONSerialize


def test_dataset_row_from_dict():
    row = DatasetRow(
        id=37,
        vtype="",
        dir_type=1,
        parent="000002",
        name="0000020572.json",
        etag="c16a68901b0a3222beccaa53c34a6c0c",
        version="",
        is_latest=True,
        last_modified=datetime.datetime(2022, 12, 27, 1, 16, 57),
        size=625,
        owner_name="",
        owner_id="",
        random=1234,
        location=None,
        source=StorageURI("s3://bucket-name"),
    )

    row_dict = json.loads(json.dumps(row, cls=JSONSerialize))

    assert row == DatasetRow.from_dict(row_dict)
