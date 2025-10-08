import os
from pathlib import Path
from src.document_analysis.data_analyser import DocumentAnalyser
from src.document_analysis.data_ingestion import DocumentHandler
pdf_path="/Users/apsara/Documents/llmops/document_portal/data/document_analysis/sample_1.pdf"
class DummyFile:
        def __init__(self,file_path):
            self.name=Path(file_path).name#creates system compatible path
            self._file_path=file_path

        
        def getbuffer(self):
            return open(self._file_path, "rb").read()
        
def main():

    
    

    try:
        #--Step 1:Data ingestion--
        print("Starting data ingestion")
        dummy_pdf=DummyFile(pdf_path)
        handler=DocumentHandler(session_id="test_ingestion_analysis")
        
        saved_path=handler.save_pdf(dummy_pdf)
        print("PDF saved at:",saved_path)

        content=handler.read_pdf(saved_path)
        print(f"Extracted content length:{len(content)} chars\n")

        #--Step 2:Data Analysis
        print("Starting metadata analysis")
        analyser=DocumentAnalyser()
        print("Analyser initialised")
        analysis_result=analyser.analyse_document(content)

        #--Step 3:Display result
        print("\n=== METADATA ANALYSIS RESULTS ===")
        for key,value in analysis_result.items():
            print(f"{key}:{value}")

        
    except Exception as e:
        print(f"Test failed with Error:{e}")

if __name__=="__main__":
    main()