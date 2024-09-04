# 기본 코드
from dotenv import load_dotenv 

load_dotenv()

from langchain_openai import ChatOpenAI 
from langchain_upstage import ChatUpstage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class SummaryBot:
    def __init__(self):
        self.template = """
        # Instruction 
        - DETAILS는 AI 캐릭터의 성격을 설명합니다. 
        - 20자 이상 40자 이내 한 줄로 요약해주세요.
        - 한글로 요약하세요

        # DETAILS: {details}
        """
        self._make_chain()
    
    def _make_prompt(self):
        return PromptTemplate.from_template(self.template)

    def _make_chain(self):
        model = ChatUpstage(model_name = "solar-1-mini-chat") 
        # model = ChatOpenAI(model_name = "gpt-3.5-turbo") 
        prompt = self._make_prompt()
        output_parser = StrOutputParser()

        self.chain = prompt | model | output_parser

    async def ainvoke(self, request):
        response = await self.chain.ainvoke(request)
        # print(response)
        return response 


summarybot = SummaryBot()