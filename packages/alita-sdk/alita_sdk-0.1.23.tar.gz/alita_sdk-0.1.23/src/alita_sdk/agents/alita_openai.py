import json 
from json import JSONDecodeError

from typing import Sequence, Union, Any, Dict, Optional
from traceback import format_exc

from langchain_core.messages import BaseMessage
from langchain_core.callbacks import CallbackManager
from langchain_core.load import dumpd
from langchain.agents.openai_assistant.base import OutputType
from langchain_core.runnables import RunnableConfig, RunnableSerializable, ensure_config

from .mixedAgentRenderes import conversation_to_messages, format_to_langmessages
from langchain_core.agents import AgentAction, AgentFinish

class AlitaDialOpenAIAssistantRunnable(RunnableSerializable):
    client: Optional[Any]
    assistant: Optional[Any]
    chat_history: list[BaseMessage] = []

    def invoke(self, input: dict, config: RunnableConfig | None = None) -> OutputType:
        config = ensure_config(config)
        callback_manager = CallbackManager.configure(
            inheritable_callbacks=config.get("callbacks"),
            inheritable_tags=config.get("tags"),
            inheritable_metadata=config.get("metadata"),
        )
        run_manager = callback_manager.on_chain_start(
            dumpd(self), input, name=config.get("run_name")
        )
        messages = []
        if input.get("intermediate_steps"):
            messages = format_to_langmessages(input["intermediate_steps"])
        try:
            mgs = self.chat_history + conversation_to_messages(input["chat_history"][:-1]) + messages
            try:
                mgs += conversation_to_messages([input["chat_history"][-1]])
            except IndexError:
                ...
            print(mgs)
            callback_manager.on_llm_start(dumpd(self), [message.content for message in mgs])
            run = self._create_thread_and_run(mgs)
            response = self._get_response(run)
        except BaseException as e:
            run_manager.on_chain_error(e, metadata=format_exc())
            raise e
        else:
            run_manager.on_chain_end(response)
            return response
    
    
    def _get_response(self, run: BaseMessage) -> Any:
        if run.additional_kwargs.get("function_call"):
            action = run.additional_kwargs["function_call"].get("name")
            tool_input = json.loads(run.additional_kwargs["function_call"].get("arguments"))
            return AgentAction(action, tool_input, run.content)
        else:
            return AgentFinish({"output": run.content}, run.content)
        
    
    def _create_thread_and_run(self, messages: list[BaseMessage]) -> Any:
        return self.assistant.predict(messages)
