import abc
import os
from typing import Any, Union

from delta.manifest.parser import InputModel
from delta.run.api.model import DataParameterModel


class Placeholder(abc.ABC):
    @abc.abstractmethod
    def evaluate(self) -> Any:
        raise NotImplementedError


class InputModelPlaceholder(Placeholder):
    _separator: str = " "

    def __init__(self, input_model: InputModel, value: Any):
        super().__init__()
        self._input = input_model
        self._value = value
        self._factory = {
            "boolean": self.__evaluate_boolean,
            "integer": self.__evaluate_number,
            "number": self.__evaluate_number,
            "string": self.__evaluate_string,
            "Data": self.__evaluate_data,
            "stdout": self.__evaluate_data,
        }

    def __evaluate_boolean(self) -> str:
        value = self._value or self._input.value
        if value and self._input.prefix:
            return self._input.prefix
        return ""

    def __evaluate_number(self) -> str:
        value = self._value or self._input.value
        if value:
            if self._input.prefix:
                return f"{self._input.prefix}{self._separator}{value}"
            return str(value.value)
        return ""

    def __evaluate_string(self) -> str:
        value = self._value or self._input.value
        if value:
            if self._input.prefix:
                return f"{self._input.prefix}{self._separator}{value}"
            return value.value
        return ""

    def __evaluate_data(self) -> str:
        value = self._value or self._input.value
        if value:
            if self._input.prefix:
                return f"{self._input.prefix}{self._separator}{value.path}"
            return os.path.join("/s3", value.path)
        return ""

    def evaluate(self) -> str:
        try:
            return self._factory[self._input.type]()
        except KeyError:
            return ""


class JobBuilder(abc.ABC):
    @staticmethod
    def placeholder_factory(model_part: InputModel, value: Any) -> Placeholder:
        if isinstance(model_part, InputModel):
            return InputModelPlaceholder(model_part, value)
        raise NotImplementedError

    @abc.abstractmethod
    def generate_dockerfile(self) -> str:
        raise NotImplementedError

    @staticmethod
    def generate_dockerfile_ctx() -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def build_command(self):
        raise NotImplementedError
