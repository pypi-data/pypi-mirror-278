from ..models.input import Input


class InputDataParser:
    __id: int = 0

    def get_parsed_data(self, input: Input) -> dict[int, str]:
        parsed_data: dict[int, str] = {}

        lines: list[str] = input.data.split('\n')

        for line in lines:
            key_value: tuple[int, str] = self.__get_key_value_pairs(line)
            key, value = key_value
            parsed_data[key] = value

        return parsed_data

    def __get_key_value_pairs(self, line: str) -> tuple[int, str]:
        key: int = self.__id
        value: str = line

        self.__id += 1

        return (key, value)
