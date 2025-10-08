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
        self.chain = self.prompt | self.llm | self.fixingparser

        self.log.info("Document comparator has been initialised")
    def compare_documents(self,combined_docs)->pd.DataFrame:
        try:
            inputs={
                "combined_docs":combined_docs,
                "format_instructions":self.parser.get_format_instructions()
            }
            self.log.info("Starting document comparison")
            response=self.chain.invoke(inputs)
            self.log.info("Document comparison completed")
            return self._format_response(response)

        except Exception as e:
            self.log.error(f"Error in initialising DocumentComparatorLLM: {e}")
            raise DocumentPortalException("Error occured while comparing documents", sys)

    def _format_response(self,res:list[dict])->pd.DataFrame:
        try:
            df=pd.DataFrame(res)
            self.log.info("Response formatted into DataFrame",dataframe=df)
            return df
        except Exception as e:
            self.log.error(f"Error in formatting response into DataFrame",error=str(e))
            raise DocumentPortalException("Error occured while formatting response", sys) 