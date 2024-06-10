from bot_station.domain.llm.llm import LLM


class MockLLM(LLM):
    next_answer = ""

    async def call(self, query: str) -> str:
        return self.next_answer

    def set_next_answer(self, answer: str):
        self.next_answer = answer
