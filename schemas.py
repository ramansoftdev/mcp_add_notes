from pydantic import BaseModel , Field

class InputFileParam(BaseModel):
  file_name:str = Field(min_length=1)
  file_content:str = Field(min_length=1)

class OutputParam(BaseModel):
  file_name:str