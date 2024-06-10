class OutputDataParser:
    def parse(self, words: dict[int, str]) -> str:
        return '\n'.join(word for word in list(words.values()))
