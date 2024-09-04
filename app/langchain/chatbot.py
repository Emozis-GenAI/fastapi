from pathlib import Path 
from dotenv import load_dotenv 

load_dotenv()

from langchain_openai import ChatOpenAI 
from langchain_upstage import ChatUpstage
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from operator import itemgetter

from app.core.config import configs
from app.core.logger import logger

const = configs.langchain

class ChatBot:
    def __init__(self):
        self.template_name = "template.prompt"
        self._make_chain()
    
    def _read_template(self):
        file_path = Path(__file__).parents[1] / f"data/{self.template_name}"

        try:
            file_text = file_path.read_text(encoding="utf-8")
        except:
            file_text = ""
            logger.warning(f"Template 파일 경로를 찾을 수 없습니다.")
        
        return file_text

    def _get_prompts(self):
        template = self._read_template()
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{request}")
            ]
        )

        return prompt

    def _set_memory(self):
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )

    def _make_chain(self):
        self._set_memory()
        
        runnable = RunnablePassthrough.assign(
            chat_history=RunnableLambda(self.memory.load_memory_variables)
            | itemgetter("chat_history")
        )
        prompt = self._get_prompts()
        if const["model"] == "openai":
            model = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=const["temperature"]
            )
        else:
            model = ChatUpstage(
                model_name="solar-1-mini-chat",
                temperature=const["temperature"]
            )
        output_parser = StrOutputParser()

        self.chain = runnable | prompt | model | output_parser 
        logger.info("✅ Success Make Chain")

    def save_greeting(self, input):
        self.memory.save_context(
            {"ai": output}
        )

    def save_memory(self, input, output):
        self.memory.save_context(
            {"human": input},
            {"ai": output}
        )

    def reset(self):
        self._make_chain()
        logger.info("✅ Success Make New Chain")

chatbot = ChatBot()

