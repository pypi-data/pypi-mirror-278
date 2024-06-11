import dataclasses
import datetime
import inspect
import json
import os
import subprocess
import tempfile
from abc import ABC
from decimal import Decimal
from pathlib import Path
from shutil import rmtree, which
from typing import Any

from pydantic import BaseModel

from griff.services.path.path_service import PathService


class AbstractTestCase(ABC):  # pragma: no cover
    _base_dir = None
    _base_test_dir = "/_tests"
    _fixture_dir = None
    _common_fixture_dir = None

    @classmethod
    def setup_class(cls):
        if hasattr(super(), "setup_class"):
            raise RuntimeError("Must be the last class in the inheritance chain")
        cls.clean_sandbox()
        cls.read_file = PathService().read_file

    def setup_method(self):
        if hasattr(super(), "setup_method"):
            raise RuntimeError("Must be the last class in the inheritance chain")

    @classmethod
    def teardown_class(cls):
        pass

    def teardown_method(self):
        pass

    @classmethod
    def get_dataset(cls, dataset):
        """
        Get fixture dataset if is json, load it else just read it
        Args:
            dataset(str): relative path to dataset directory
        Returns:
            mixed
        """
        return cls._get_dataset(dataset, cls.get_datasets_dir(dataset))

    @classmethod
    def get_datasets_dir(cls, relative_path=None) -> str:
        dir = f"{cls._get_test_fixtures_dir()}/datasets"
        if relative_path:
            return f"{dir}/{relative_path}"
        return dir

    def assert_equals_resultset(self, actual, **kwargs):
        # build resultset filename from caller filename
        calling_filename = kwargs.get("calling_filename", None)
        filename = self._get_calling_filename()
        calling_frame = self._get_calframe(calling_filename)
        method_name = self._get_calling_method_name(calling_frame)
        sub_dir = self._get_test_subdir(filename)
        filename_noext = Path(filename).name.replace(".py", "")
        resultset_filename = Path(
            f"{self._get_resultsets_dir()}/{sub_dir}/{filename_noext}"
            f"/{method_name}.json"
        )
        self._create_missing_directories(resultset_filename)

        actual_json = self._json_dump(actual)

        # get expected result sets from file
        if resultset_filename.exists() is False:
            # create missing file
            data = (
                actual_json
                if os.environ.get("TEST_RESULTSET_AUTOSAVE", False)
                else "{}"
            )
            with resultset_filename.open("w") as f:
                f.write(data)

        with resultset_filename.open() as json_file:
            expected = json_file.read()

        # assert

        try:
            assert expected == actual_json
        except AssertionError as e:
            tmp_dir = self._get_tmp_dir()

            # build fix result set
            tmp_actual_filename = Path(
                f"{tmp_dir}/{filename_noext}-{method_name}_ACTUAL.json"
            )
            self._create_missing_directories(tmp_actual_filename)

            with tmp_actual_filename.open("w") as f:
                f.write(actual_json)

            common_cmd = f"{resultset_filename} {tmp_actual_filename}"
            if which("bcompare") is not None:
                common_cmd = f"bcompare {common_cmd}"
            elif which("pycharm") is not None:
                common_cmd = f"pycharm diff {common_cmd}"
            elif which("charm") is not None:
                common_cmd = f"charm diff {common_cmd}"
            elif which("pycharm-community") is not None:
                common_cmd = f"pycharm-community diff {common_cmd}"
            elif which("meld") is not None:
                common_cmd = f"meld {common_cmd}"
            # noinspection SubprocessShellMode
            subprocess.Popen(common_cmd, shell=True)

            print(f"\n\033[1;31m=== TEST {method_name} has failed !!")
            print(f"file: {filename}")
            os.system(f"diff {resultset_filename} {tmp_actual_filename}")
            print(f"=== TEST {method_name}\n\033[0m")
            raise e

    @classmethod
    def clean_sandbox(cls):
        cls._empty_dir(cls._get_base_sandbox_dir())

    @classmethod
    def get_sandbox_dir(cls, filename=None) -> str:
        sandbox_path = cls._get_base_sandbox_dir().joinpath(cls.__name__)
        if filename is None:
            sandbox_path.mkdir(parents=True, exist_ok=True)
            return str(sandbox_path)
        filename = Path(f"{sandbox_path}/{filename}")
        cls._create_missing_directories(filename)
        return str(filename)

    @staticmethod
    def assert_path_exists(path):
        assert os.path.exists(path), path

    @staticmethod
    def assert_path_not_exists(path):
        assert not os.path.exists(path), path

    @classmethod
    def _empty_dir(cls, directory: Path) -> None:
        full_path = Path(directory)
        if full_path.exists():
            rmtree(full_path)
            full_path.mkdir()

    @classmethod
    def _get_dataset(cls, dataset, dataset_filename):
        filename, file_extension = os.path.splitext(dataset)
        with open(dataset_filename) as file:
            if file_extension == ".json":
                dataset = json.load(file)
                if "__generated_by__" in dataset:
                    dataset.pop("__generated_by__")
                return dataset
            return file.read()

    @classmethod
    def _get_tmp_dir(cls):
        """Get tmp test directory"""
        return f"{tempfile.tempdir}/.donotcommit_tmp"

    @classmethod
    def _get_test_fixtures_dir(cls) -> str:
        """
        Get fixtures directory

        Returns:
            str: fixtures directory
        """
        if not cls._fixture_dir:
            filename = cls._get_calling_filename()
            pos = filename.find(cls._base_test_dir)
            if not pos > 0:
                raise ValueError(f"Unable to determine root tests path from {filename}")
            cls._fixture_dir = f"{filename[:pos]}{cls._base_test_dir}/_fixtures"

        return cls._fixture_dir

    @classmethod
    def _get_resultsets_dir(cls) -> str:
        """
        Get result sets dir

        Returns:
            str: result sets directory
        """
        return f"{cls._get_test_fixtures_dir()}/resultsets"

    @classmethod
    def _get_base_sandbox_dir(cls):
        return Path(f"{cls._get_test_fixtures_dir()}/sandbox")

    @classmethod
    def _get_calling_filename(cls) -> str:
        return inspect.getfile(cls)

    @classmethod
    def _get_calframe(cls, calling_filename=None) -> inspect.FrameInfo:
        # find calling frame
        calframe = inspect.getouterframes(inspect.currentframe(), 2)
        test_filename = (
            cls._get_calling_filename() if not calling_filename else calling_filename
        )
        for frame in calframe:
            if frame.filename.find(test_filename) >= 0:
                return frame
        raise ValueError("Unable to determine calling frame")

    @staticmethod
    def _get_calling_method_name(frame) -> Any:
        return frame[3]

    @staticmethod
    def _get_calling_lineno(frame) -> str:
        return frame.lineno

    @staticmethod
    def _create_missing_directories(filename: Path) -> None:
        if filename.exists():
            return None

        filename = filename.parent
        filename.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _get_test_subdir(cls, filename):
        dir_names = str(Path(filename).parent).split("/")

        # search tests dir
        for _ in range(0, len(dir_names)):
            dir_name = dir_names.pop(0)
            if dir_name == "_tests":
                break

        return "/".join(dir_names)

    @classmethod
    def _json_dump(cls, data):
        json_dump = json.dumps(
            cls._convert_data(data),
            indent=4,
            separators=(",", ": "),
            default=str,
            # disable non-ASCII characters escape with \uXXXX sequences
            ensure_ascii=False,
        )
        # for respecting file empty last line convention
        return f"{json_dump}\n"

    @classmethod
    def _convert_data(cls, data):
        if isinstance(data, Decimal):
            return float(data)

        if dataclasses.is_dataclass(data):
            return dataclasses.asdict(data)

        if isinstance(data, BaseModel):
            return data.model_dump()

        if isinstance(data, bytes):
            return data.decode("utf-8")

        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = cls._to_json_dumpable(v)
            return data

        if isinstance(data, list):
            for idx, i in enumerate(data):
                data[idx] = cls._to_json_dumpable(i)
            return data

        if isinstance(data, tuple):
            data = cls._to_json_dumpable(list(data))

        if isinstance(data, set):
            data = cls._to_json_dumpable(list(data))

        return data

    @classmethod
    def _to_json_dumpable(cls, data):
        """
        Convert data to be json dumpable
        """
        if isinstance(data, BaseModel):
            data = data.model_dump()

        if isinstance(data, tuple):
            data = list(data)

        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = cls._to_json_dumpable(v)
            return data

        if isinstance(data, list):
            for i in data:
                cls._to_json_dumpable(i)
            return data

        if isinstance(data, set):
            data = cls._to_json_dumpable(list(data))

        if isinstance(data, Decimal):
            return float(data)

        # if isinstance(data, Arrow):
        #     return data.format()

        elif isinstance(data, datetime.datetime) or isinstance(data, datetime.date):
            return data.strftime("%Y-%m-%d %H:%M:%S")

        return data
