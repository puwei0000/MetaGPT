import re
from examples.st_game.actions.st_action import STAction
from examples.st_game.memory.agent_memory import BasicMemory
from metagpt.logs import logger

class AgentWhisperThoughtAction(STAction):

    def __init__(self, name="AgentWhisperThoughtAction", context: list[BasicMemory] = None, llm=None):
        super().__init__(name, context, llm)

    def _func_validate(self, llm_resp: str, prompt: str) -> bool:
        try:
            self._func_cleanup(llm_resp, prompt)
            return True
        except:
            return False

    def _func_cleanup(self, llm_resp: str, prompt: str = "") -> list:
        return llm_resp.split('"')[0].strip()

    def _func_fail_default_resp(self) -> str:
        pass

    async def run(self, role: "STRole", statements: str, test_input=None, verbose=False) -> str:
        def create_prompt_input(role: "STRole", statements, test_input=None):
            prompt_input = [role.scratch.name, statements]
            return prompt_input

        prompt_input = create_prompt_input(role, statements)
        prompt = self.generate_prompt_with_tmpl_filename(prompt_input,
                                                         "whisper_inner_thought_v1.txt")

        output = await self._run_v1(prompt)
        logger.info(f"Run action: {self.__class__.__name__} with result: {output}")
        return output
