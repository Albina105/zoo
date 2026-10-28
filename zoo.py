# import re
# from langchain_ollama import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnableLambda, RunnableBranch
#
# BANNED = {'бомба', 'бомбу', 'взлом', 'наркотик'}
#
# prompt = ChatPromptTemplate([
#     (
#         'system',
#         "Ты опытный ментор и разработчик по Python. "
#         "А также уровень английского языка C1. "
#         "Отвечай на вопросы кратко и с примерами. "
#         "На русском языке."
#     ),
#     ('human', '{text}'),
# ])
#
# model = ChatOllama(model='llama3.2:latest')
#
# def is_banned(text: str) -> bool:
#     words = re.findall(r'\w+', text.lower())
#     return any(w in BANNED for w in words)
#
# llm_chain = prompt | model | StrOutputParser()
#
# chain = RunnableBranch(
#     (is_banned, RunnableLambda(lambda _: 'На такие вопросы не можем ответить')),
#     llm_chain,
# )
#
# print(chain.invoke('Как создать бомбу?'))


import datetime as dt
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

with open('nnn.txt', encoding='utf-8') as file:
    text = file.read()
chunks = [Document(page_content=p.strip()) for p in text.split('\n\n') if p.strip()]
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)
vector_store = InMemoryVectorStore.from_documents(chunks, embeddings)
prompt = ChatPromptTemplate(
    [
        (
            'system',
            'Ты онлайн менеджер зоомагазина Лапки. '
            'При ответе ты должен сначала посмотреть Базу Знаний: '
            '"База знаний {base_knowledge}" '
            'Должен отвечать на вопросы коротко и вежливо. '
            '"Если не нашел ответ в базе знаний напиши что не знаешь." '
        ),
        (
            'human',
            '{content}'
        )
    ]
)

model = ChatOllama(
    model='llama3.2:latest',
    temperature=0
)

class AnswerSchema(BaseModel):
    answer: str
structured_model = model.with_structured_output(AnswerSchema)
def clean_question(data):
    data['content'] = data['content'].strip().lower()
    return data
def make_greeting(result):
    return 'Здравствуйте! ' + result.answer.lower()
def add_emoji(text):
    return text + ' 🐶🐱🐹'
chain = (
    RunnableLambda(clean_question)
    | prompt
    | structured_model
    | RunnableLambda(make_greeting)
    | RunnableLambda(add_emoji)
)
test_app = FastAPI()
class QuestionSchema(BaseModel):
    question: str
class QuestionsSchema(BaseModel):
    questions: list[str]
class QuestionOutputSchema(BaseModel):
    id: int
    answer: str
    datetime: dt.datetime

def get_knowledge(question):
    found = vector_store.similarity_search(question, k=3)
    return '\n\n'.join(doc.page_content for doc in found)
@test_app.post('/questions/', response_model=QuestionOutputSchema)
async def answer(data: QuestionSchema):
    question = data.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail='Маалымат берилген жок')
    result = chain.batch([{'content': question, 'base_knowledge': get_knowledge(question)}])
    return QuestionOutputSchema(
        id=1,
        answer=result[0],
        datetime=dt.datetime.now()
    )
@test_app.post('/questions/batch/', response_model=list[QuestionOutputSchema])
async def answer_many(data: QuestionsSchema):
    inputs = []
    for q in data.questions:
        q = q.strip()
        if not q:
            raise HTTPException(status_code=400, detail='Маалымат берилген жок')
        inputs.append({'content': q, 'base_knowledge': get_knowledge(q)})
    results = chain.batch(inputs)
    output = []
    for number, r in enumerate(results, start=1):
        output.append(
            QuestionOutputSchema(
                id=number,
                answer=r,
                datetime=dt.datetime.now()
            )
        )

    return output
if __name__ == '__main__':
    uvicorn.run(test_app, host='127.0.0.1', port=8000)