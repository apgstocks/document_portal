from langchain_core.prompts import ChatPromptTemplate
document_analysis_prompt=ChatPromptTemplate.from_template("""
You are a highly capable assistant trained to analyse and summarise documents.
Return ONLY valid JSON matching the exact schema below
{format_instructions}
                                        
Analyse this document:
{document_text}
                """)


document_comparison_prompt=ChatPromptTemplate.from_template("""
You will be provided with contents from two PDF files.Your task are as follows:

1.compare the content in two PDF files.
2.Identify the difference in PDF and note down the page number.
3.The output you provide must be pagewise comparison content.
4.If any page does not contain any change/difference,mention as 'NO CHANGE'.
                                                            
INPUT DOCUMENTS:
{combined_docs}

Your response should follow this format:
{format_instructions}
                                                            
                                        """)
PROMPT_REGISTRY={"document_analysis":document_analysis_prompt,
                 "document_comparison":document_comparison_prompt}