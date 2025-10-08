import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    def __init__(self,base_dir:str="data/document_compare"):
        self.log=CustomLogger().get_Logger(__name__)
        self.base_dir=Path(base_dir)
        self.base_dir.mkdir(parents=True,exist_ok=True)

    def delete_existing_file(self):
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file:
                        self.log.info(f"Deleting file",path=str(file))
                        file.unlink()
                self.log.info("Directory cleaned",directory=str(self.base_dir))
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
        
    def combine_documents(self)->str:
        try:
            content_dic={}
            doc_parts=[]
            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix==".pdf":
                    content_dic[filename.name]=self.read_pdf(filename)
                
            for filename,content in content_dic.items():
                doc_parts.append(f"Document: {filename}\n{content}")
            combined_text="\n\n".join(doc_parts)
            self.log.info("Documents combined",count=len(doc_parts))
            return combined_text
        except Exception as e:
            self.log.error(f"Error in combining documents", error=str(e))
            raise DocumentPortalException("Error occured while combining documents", sys)