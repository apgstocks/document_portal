import os
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader
from model import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser 
from prompt.prompt_library import *
import sys

class DocumentAnalyser:
    """
    Analyse the document using pre-trained model
    Automically logs all the actions 
    """

    def __init__(self):
        self.log=CustomLogger().get_Logger(__name__)

        try:
            self.loader=ModelLoader()
            self.llm=self.loader.load_llm()
            #Preparing Parsers
            self.parser=JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser=OutputFixingParser.from_llm(parser=self.parser,llm=self.llm)

            self.prompt=prompt
            self.log.info("DocumentAnalyser initialised successfully")
        except Exception as e:
            self.log.error(f"Error in initialising DocumentAnalyser: {e}")
            raise DocumentPortalException("Error in initialising DocumentAnalyser", sys)

    def analyse_metadata(self,document_path):
        self.model_loader=ModelLoader()
        self.logger=CustomLogger(__file__)
