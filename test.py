# import os
# from pathlib import Path
# from src.document_analysis.data_analyser import DocumentAnalyser
# from src.document_analysis.data_ingestion import DocumentHandler
# pdf_path="/Users/apsara/Documents/llmops/document_portal/data/document_analysis/sample_1.pdf"
# class DummyFile:
#         def __init__(self,file_path):
#             self.name=Path(file_path).name#creates system compatible path
#             self._file_path=file_path

        
#         def getbuffer(self):
#             return open(self._file_path, "rb").read()
        
# def main():

    
    

#     try:
#         #--Step 1:Data ingestion--
#         print("Starting data ingestion")
#         dummy_pdf=DummyFile(pdf_path)
#         handler=DocumentHandler(session_id="test_ingestion_analysis")
        
#         saved_path=handler.save_pdf(dummy_pdf)
#         print("PDF saved at:",saved_path)

#         content=handler.read_pdf(saved_path)
#         print(f"Extracted content length:{len(content)} chars\n")

#         #--Step 2:Data Analysis
#         print("Starting metadata analysis")
#         analyser=DocumentAnalyser()
#         print("Analyser initialised")
#         analysis_result=analyser.analyse_document(content)

#         #--Step 3:Display result
#         print("\n=== METADATA ANALYSIS RESULTS ===")
#         for key,value in analysis_result.items():
#             print(f"{key}:{value}")

        
#     except Exception as e:
#         print(f"Test failed with Error:{e}")

# if __name__=="__main__":
#     main()

import io
from pathlib import Path
from src.doccompare.data_ingestion import DocumentIngestion
from src.doccompare.document_comparator import DocumentComparatorLLM

def load_fake_uploaded_file(file_path:Path):
    return io.BytesIO(file_path.read_bytes)

def test_compare_documents():
    ref_path="/Users/apsara/Documents/llmops/document_portal/data/document_compare/Report_v1.pdf"
    act_path="/Users/apsara/Documents/llmops/document_portal/data/document_compare/Report_v2.pdf"

    class Fakeupload:   
        def __init__(self,file_path:Path) -> None:
            self.name=Path(file_path).name
            self._buffer=file_path.read_bytes()

        def getbuffer(self):
            return self._buffer
    
    comparator=DocumentIngestion()
    ref_upload=Fakeupload(ref_path)
    act_upload=Fakeupload(act_path)

    ref_file,act_file=comparator.save_uploaded_files(ref_upload,act_upload)
    combined_text=comparator.combine_text(ref_file, act_file)

    print("\n Combined Text Preview (First 1000 char):\n")
    print(combined_text[:1000])
    
    llm_comparator=DocumentComparatorLLM()
    comparison_df=llm_comparator.compare_documents(combined_text)
    print("\n Comparison Results:")
    print(comparison_df.head())

if __name__=="__main__":
    test_compare_documents()