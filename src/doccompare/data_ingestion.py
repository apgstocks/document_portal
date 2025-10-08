import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentComparator:
    def __init__(self):
        pass

    def delete_existing_file(self):
        try:
            pass    
        except Exception as e:
            self.log.error(f"Error in deleting existing file",error=str(e))
            raise DocumentPortalException("Error occured while deleting existing file", sys)

    def save_uploaded_files(self,reference_file,actual_file):
        try:
            self.delete_existing_file()
            self.log.info("Existing files deleted successfully")

            ref_path=self.base_dir
            act_path=self.base_dir
            if not reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise ValueError("Only PDF files are allowed")
            
            with open(reference_file,"wb") as f:
                f.write(reference_file.getbuffer())
            
            with open(actual_file, "wb") as f:
                f.write(actual_file.getbuffer())
        except Exception as e:
            self.log.error(f"Error in saving uploaded files", error=str(e))
            raise DocumentPortalException("Error occured while saving uploaded files", sys)

    def read_pdf(self,pdf_path:Path)->str:
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encryped():
                    raise ValueError("PDF is encrypted and cannot be read")
                
                all_text=list()
                for page_num in range(doc.page_count):
                    page=doc.load_page(page_num)
                    text=page.get_text()

                    if text.strip():
                        all_text.append(f"\n ---{page_num+1} ---\n{text}")

            return "\n".join(all_text) 

               
        except Exception as e:
            self.log.error(f"Error in reading PDF", error=str(e))
            raise DocumentPortalException("Error occured while reading PDF", sys)
        