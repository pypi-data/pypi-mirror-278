import inspect
import io
import sys
import traceback
from collections.abc import Sequence
from typing import Any, Optional, Union

from pydantic import ValidationError as PydanticValidationError

from dvcx.catalog import Catalog
from dvcx.lib.feature import Feature
from dvcx.lib.feature_types import FeatureLike, FeatureTypes
from dvcx.lib.file import File
from dvcx.lib.udf import Aggregator, BatchMapper, Generator, Mapper, UDFBase
from dvcx.lib.utils import DvcxError
from dvcx.query import Stream


class ValidationError(DvcxError):
    pass


class SchemaError(ValidationError):
    def __init__(self, udf_name: str, context: str, message: str):
        super().__init__(f"'{udf_name}' {context} schema validation error: {message}")


class OutputError(ValidationError):
    def __init__(self, udf_name: str, message: str, num: Optional[int] = None):
        num_str = "" if num is None else f"#{num + 1} "
        super().__init__(f"Output {num_str}of '{udf_name}' error: {message}")


class UserCodeError(DvcxError):
    def __init__(self, class_name: str, message: str):
        super().__init__(f"Error in user code in class '{class_name}': {message}")


class FeatureConverter:
    @property
    def udf_params_list(self):
        return self._udf_params_list

    @property
    def udf_output_spec(self):
        return self._udf_output_spec

    @property
    def cache(self):
        return self._udf.catalog.cache

    @staticmethod
    def has_feature_stream(fr_classes: Sequence[type[Feature]]):
        return any(
            f._is_file  # type: ignore[attr-defined]
            for f in fr_classes
        )

    @staticmethod
    def has_row_stream(row):
        if len(row) == 0:
            return False
        return isinstance(row[0], (Stream, io.IOBase))

    def __init__(
        self,
        udf: UDFBase,
        inputs: Union[FeatureLike, Sequence[FeatureLike]] = (),
        outputs: Union[FeatureLike, Sequence[FeatureLike]] = (),
    ):
        self._udf = udf

        self._inputs, self._is_single_input = self._convert_to_sequence(inputs)
        self._outputs, self._is_single_output = self._convert_to_sequence(outputs)

        self._validate_schema("params", self._inputs)
        self._validate_schema("output", self._outputs)

        self._udf_params_list = self.get_flattened_params(self._inputs)
        self._udf_output_spec = Feature._features_to_udf_spec(self._outputs)  # type: ignore[attr-defined]

    @staticmethod
    def get_flattened_params(fr_classes: Sequence[type[Feature]]):
        udf_params_spec = Feature._features_to_udf_spec(fr_classes)
        stream_prm = (
            [Stream()] if FeatureConverter.has_feature_stream(fr_classes) else []
        )
        return stream_prm + list(udf_params_spec.keys())

    @staticmethod
    def _convert_to_sequence(
        arg: Union[FeatureLike, Sequence[FeatureLike]],
    ) -> tuple[Sequence[type[Feature]], bool]:
        if not isinstance(arg, Sequence) or isinstance(arg, str):
            return FeatureTypes._to_features(*[arg]), True
        return FeatureTypes._to_features(*arg), False

    @staticmethod
    def deserialize(
        rows: Sequence[Sequence],
        params: Sequence[str],
        fr_classes: Sequence[type[Feature]],
        catalog: Catalog,
        caching_enabled: bool,
    ) -> Sequence[Sequence[Feature]]:
        clean_rows, streams = FeatureConverter._separate_streams_from_rows(
            rows, fr_classes
        )

        feature_rows = [
            FeatureConverter._row_with_params_to_features(row, fr_classes, params)
            for row in clean_rows
        ]

        for features, stream in zip(feature_rows, streams):
            for feature in features:
                if isinstance(feature, File):
                    feature.set_catalog(catalog)  # type: ignore [attr-defined]
                    feature.set_file(stream, caching_enabled)  # type: ignore [attr-defined]

        return feature_rows

    @staticmethod
    def _separate_streams_from_rows(
        rows, fr_classes: Sequence[type[Feature]]
    ) -> tuple[Sequence, Sequence]:
        streams = []
        res_rows = []
        if FeatureConverter.has_feature_stream(fr_classes):
            for row in rows:
                if FeatureConverter.has_row_stream(row):
                    streams.append(row[0])
                    res_rows.append(row[1:])
                else:
                    streams.append(None)  # type: ignore [arg-type]
                    res_rows.append(row)
        else:
            res_rows = rows
        return res_rows, streams

    @staticmethod
    def _row_with_params_to_features(
        row: Sequence, fr_classes: Sequence[type[Feature]], params: Sequence[str]
    ) -> Sequence[Feature]:
        new_params = (
            params
            if not FeatureConverter.has_feature_stream(fr_classes)
            else params[1:]
        )
        return [cls._unflatten(dict(zip(new_params, row))) for cls in fr_classes]

    def _validate_schema(self, context: str, features: Sequence[type[Feature]]):
        for type_ in features:
            if not isinstance(type_, type):
                raise SchemaError(
                    self._udf.name,
                    context,
                    "cannot accept objects, a 'Feature' class must be provided",
                )
            if not Feature.is_feature_class(type_):
                raise SchemaError(
                    self._udf.name,
                    context,
                    f"cannot accept type '{type_.__name__}', "
                    f"the type must be a subclass of 'Feature'",
                )

    def output_to_features(self, row: Sequence[Any]) -> list[Feature]:
        fr_row = []
        for val, fr in zip(row, self._outputs):
            if isinstance(val, fr):
                fr_row.append(val)
            else:
                try:
                    fr_row.append(fr(**dict(zip(fr.model_fields.keys(), [val]))))
                except PydanticValidationError as exc:
                    raise OutputError(self._udf.name, str(exc)) from exc
        return fr_row

    def validate_output_obj(self, result_objs, *args, **kwargs):
        for row in result_objs:
            if not isinstance(row, (list, tuple)) and isinstance(
                self._outputs, (list, tuple)
            ):
                raise OutputError(
                    self._udf.name,
                    f"expected list of objects, "
                    f"but found a single value of type '{type(row).__name__}'",
                )

            if len(row) != len(self._outputs):
                raise OutputError(
                    self._udf.name,
                    f"length mismatch - expected {len(self._outputs)} "
                    f"objects, but {len(row)} were provided",
                )

    def process_rows(self, rows, is_input_batched=True, is_output_batched=True):
        obj_rows = FeatureConverter.deserialize(
            rows,
            self._udf.params,
            self._inputs,
            self._udf.catalog,
            self._udf.caching_enabled,
        )

        if self._is_single_input:
            obj_rows = [objs[0] for objs in obj_rows]

        if not is_input_batched:
            assert (
                len(obj_rows) == 1
            ), f"{self._udf.name} takes {len(obj_rows)} rows while it's not batched"
            obj_rows = obj_rows[0]

        result_objs = self.run_user_code(obj_rows)

        if not is_output_batched:
            result_objs = [result_objs]

        if self._is_single_output:
            result_objs = [[x] for x in result_objs]

        self.validate_output_obj(result_objs)
        result_objs = [self.output_to_features(o) for o in result_objs]

        res = [Feature._flatten_list(objs) for objs in result_objs]

        if not is_output_batched:
            assert len(res) == 1, (
                f"{self._udf.name} returns {len(obj_rows)} "
                f"rows while it's not batched"
            )
            res = res[0]
        return res

    def run_user_code(self, obj_rows):
        try:
            result_objs = self._udf.process(obj_rows)
            if inspect.isgeneratorfunction(self._udf.process):
                result_objs = list(result_objs)
        except Exception as e:  # noqa: BLE001
            msg = (
                f"============== Error in user code: '{self._udf.name}' =============="
            )
            print(msg)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback.tb_next)
            print("=" * len(msg))
            raise UserCodeError(self._udf.name, str(e)) from None
        return result_objs


class FeatureAggregator(Aggregator):
    def __init__(
        self,
        inputs: Union[FeatureLike, Sequence[FeatureLike]] = (),
        outputs: Union[FeatureLike, Sequence[FeatureLike]] = (),
        batch=1,
    ):
        self._fc = FeatureConverter(self, inputs, outputs)
        super().__init__(self._fc.udf_params_list, self._fc.udf_output_spec, batch)

    def __call__(self, rows):
        return self._fc.process_rows(rows)


class FeatureMapper(Mapper):
    def __init__(
        self,
        inputs: Union[FeatureLike, Sequence[FeatureLike]] = (),
        outputs: Union[FeatureLike, Sequence[FeatureLike]] = (),
        batch=1,
    ):
        self._fc = FeatureConverter(self, inputs, outputs)
        super().__init__(self._fc.udf_params_list, self._fc.udf_output_spec, batch)

    def __call__(self, *row):
        return self._fc.process_rows([row], False, False)


class FeatureBatchMapper(BatchMapper):
    def __init__(
        self,
        inputs: Union[FeatureLike, Sequence[FeatureLike]] = (),
        outputs: Union[FeatureLike, Sequence[FeatureLike]] = (),
        batch=1,
    ):
        self._fc = FeatureConverter(self, inputs, outputs)
        super().__init__(self._fc.udf_params_list, self._fc.udf_output_spec, batch)

    def __call__(self, rows):
        return self._fc.process_rows(rows)


class FeatureGenerator(Generator):
    def __init__(
        self,
        inputs: Union[FeatureLike, Sequence[FeatureLike]] = (),
        outputs: Union[FeatureLike, Sequence[FeatureLike]] = (),
        batch=1,
    ):
        self._fc = FeatureConverter(self, inputs, outputs)
        super().__init__(self._fc.udf_params_list, self._fc.udf_output_spec, batch)

    def __call__(self, *row):
        return self._fc.process_rows([row], False)
