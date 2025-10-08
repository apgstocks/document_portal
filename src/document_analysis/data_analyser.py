import os
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader
from model.model import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser 
from prompt.prompt_library import PROMPT_REGISTRY
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

            self.prompt=PROMPT_REGISTRY['document_analysis']
            self.log.info("DocumentAnalyser initialised successfully")
        except Exception as e:
            self.log.error(f"Error in initialising DocumentAnalyser: {e}")
            raise DocumentPortalException("Error in initialising DocumentAnalyser", sys)


    def analyse_document(self,document_text:str)->dir:
        try:
            chain=self.prompt | self.llm | self.fixing_parser
            self.log.info("Meta-data analysis chain initiated")
            response=chain.invoke({"format_instructions":self.parser.get_format_instructions(),
                                   "document_text":document_text})
            self.log.info("Meta-data analysis chain completed",keys=list(response.keys()))
            return response
        except Exception as e:
            self.log.error(f"Metadata analysis failed: {e}")
            raise DocumentPortalException("Metadata extraction failed", e) from e
            
    def analyse_metadata(self,document_path):
        self.model_loader=ModelLoader()
        self.logger=CustomLogger(__file__)
