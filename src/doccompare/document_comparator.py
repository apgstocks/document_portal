import sys
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.model import *
from prompt.prompt_library import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentComparatorLLM:

    def __init__(self):
        load_dotenv()
        self.log=CustomLogger().get_Logger(__name__)
        self.loader=ModelLoader()
        self.llm=self.loader.load_llm()
        self.parser=JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixingparser=OutputFixingParser.from_llm(parser=self.parser,llm=self.llm)
        self.prompt=PROMPT_REGISTRY['document_comparison']
        self.chain=self.prompt | self.llm | self.parser | self.fixingparser
        self.log.info("Document comparator has been initialised")
    def compare_documents(self,)->dict:
        try:
            pass

        except Exception as e:
            self.log.error(f"Error in initialising DocumentComparatorLLM: {e}")
            raise DocumentPortalException("Error occured while comparing documents", sys)

    def _format_response(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error in formatting response into DataFrame",error=str(e))
            raise DocumentPortalException("Error occured while formatting response", sys) 