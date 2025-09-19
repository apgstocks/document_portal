import os
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader
from model import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentAnalyser:
    """
    Analyse the document using pre-trained model
    Automically logs all the actions 
    """

    def __init__(self):
        pass

    def analyse_metadata(self,document_path):
        self.model_loader=ModelLoader()
        self.logger=CustomLogger(__file__)
