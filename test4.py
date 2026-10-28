# from fastapi import FastAPI, HTTPException
# import uvicorn
# from pydantic import BaseModel
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama import ChatOllama
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.documents import Document
# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
#
# loader = TextLoader('data.txt', encoding='utf-8')
# document = loader.load()
#
# docs = Document(
#     page_content='Данные академии Motion web',
#     metadata={'source': '{document}'}
# )
#
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=250,
#     chunk_overlap=10,
#     length_function=len
# )
#
# chunks = text_splitter.split_text(str(document))
#
# prompt = ChatPromptTemplate(
#     [
#         (
#             'system',
#             'Ты онлайн ассистент, должен отвечать на вопросы вежливо и понятно. '
#         ),
#         (
#             'human',
#             '{text}'
#         )
#     ]
# )
#
# model = ChatOllama(
#     model='llama3.2:latest',
#     temperature=0
# )
#
# chain = prompt | model | StrOutputParser()
#
# test_app = FastAPI()
#
#
# class QuestionSchema(BaseModel):
#     question: str
#
#
# @test_app.post('/questions/')
# async def questions(body: QuestionSchema):
#     user_question = body.question.strip()
#
#     if not user_question:
#         raise HTTPException(status_code=400, detail='Мындай маалымат жок')
#
#     response = await chain.ainvoke({'text': user_question})
#
#     return {'answer': response}
#
#
# if __name__ == '__main__':
#     uvicorn.run(test_app, host='127.0.0.1', port=8000)

