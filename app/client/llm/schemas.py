from typing import List

from pydantic import BaseModel, Field


class SearchQueries(BaseModel):
    search_queries: List[str]

class Option(BaseModel):
    option: str
    description_for_customer: str

    def to_dict(self):
        return {
            "option": self.option,
            "description_for_customer": self.description_for_customer,
        }


class SelectQuestion(BaseModel):
    """This question is used when the user can select only one option"""
    question: str
    select_options: list[Option]
    main_parameter: str = Field(..., description="The main parameter that will be used to filter the results")

    def to_dict(self):
        return {
            "question": self.question,
            "select_options": [option.to_dict() for option in self.select_options],
            "main_parameter": self.main_parameter,
        }

class Guide(BaseModel):
    name: str
    questions: List[SelectQuestion]

    def to_dict(self):
        return {
            "name": self.name,
            "questions": [select_question.to_dict() for select_question in self.questions],
        }
