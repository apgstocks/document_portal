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
            print("Logger inside")
            self.log=CustomLogger().get_Logger(__name__)
            print("Here")
            self.data_dir=data_dir or os.getenv("DATA_STORAGE_PATH",os.path.join(os.getcwd(),"data","document_analysis"))
            self.session_id=session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            #create a session directory
            self.session_path=os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)
            self.log.info(f"PDF handler initialised:", session_id=self.session_id,session_path=self.session_path)
        except Exception as e:
            self.log.error(f"Error in initialising PDF handler: {e}")
            raise DocumentPortalException("Error initialised DocumentHandler", e) from e
    def save_pdf(self,uploaded_file):
        try:
            filename=os.path.basename(uploaded_file.name)
            
            if not filename.lower().endswith(".pdf"):
                raise DocumentPortalException("Uploaded file is not a PDF")
            
            save_path=os.path.join(self.session_path, filename)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            self.log.info("PDF saved successfully",file=filename,session_id=self.session_id,path=save_path)
            return save_path
        except Exception as e:
            self.log.error(f"Error in saving PDF: {e}")
            raise DocumentPortalException("Error in saving PDF", e) from e

    def read_pdf(self,pdf_path:str)->str:
        try:
            text_chunks=[]
            with fitz.open(pdf_path) as doc:
                for page_num,page in enumerate(doc, start=1):
                        text_chunks.append(f"\n-- Page {page_num} --\n{page.get_text()}")
                text="\n".join(text_chunks)

                self.log.info("PDF read successfully", pdf_path=pdf_path,session_id=self.session_id)
                return text
            
        except Exception as e:
            self.log.error(f"Error in reading PDF: {e}")
            raise DocumentPortalException("Error in reading PDF", e) from e

if __name__=="__main__":
    from pathlib import Path
    from io import BytesIO
    
    pdf_path=r"/Users/apsara/Documents/llmops/document_portal/data/document_analysis/sample.pdf"


    
    class DummyFile:
        def __init__(self,file_path):
            self.name=Path(file_path).name#creates system compatible path
            self._file_path=file_path

        
        def getbuffer(self):
            return open(self._file_path, "rb").read()
        
    dummy=DummyFile(pdf_path)
    handler=DocumentHandler()

    try:
        print("In Doc Handler")
        print(dummy)
        saved_path=handler.save_pdf(dummy)
        print(saved_path)
        content=handler.read_pdf(saved_path)
        print("Printing PDF content:")
        print(content[:500])
        
    except Exception as e:
        print(f"Error:{e}")