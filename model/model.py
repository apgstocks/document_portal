from pydantic import BaseModel,Field,RootModel
from typing import Optional,List,Dict,Any,Union

class Metadata(BaseModel):
    Summary:List[str]=Field(default_factory=list,description="Summary of the document")
    Title:str
    Author:str
    Date_created:str
    Publisher:str
    Language:str
    Pagecount : Union[int,str]
    SentimentTone:str

class ChangeFormat(BaseModel):
    Pages:str
    Changes:str

class SummaryResponse(RootModel[ist[ChangeFormat]]):
    pass