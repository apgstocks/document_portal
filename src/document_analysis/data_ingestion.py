import os
import fitz #wrapper on top of pypdf
import uuid #Universal identification number to create unique id
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    """
    Handles pdf saving and reading operations
    Automatically logs all actions
    """
    def __init__(self,data_dir=None,session_id=None):
        try:
            self.log=CustomLogger.get_Logger(__name__)
            self.data_dir=data_dir or os.getenv("DATA_STORAGE_PATH",os.path.join(os.getcwd(),"data","document_analysis"))
            self.session_id=session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            #create a session directory
            self.session_path=os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)
            self.log.info(f"PDF handler initialised:", session_id=self.session_id,session_path=self.session_path)
        except Exception as e:
            self.log.error(f"Error in initialising PDF handler: {e}")
            raise DocumentPortalException("Error initialised DocumentHandler", e) from e
    def save_pdf(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error in saving PDF: {e}")
            raise DocumentPortalException("Error in saving PDF", e) from e

    def read_pdf(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error in reading PDF: {e}")
            raise DocumentPortalException("Error in reading PDF", e) from e

if __name__==__main__:
    handler=DocumentHandler()
    print(f"session id:{handler.session_id}")
    print(f"session path:{handler.session_path}")