from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

model = ChatOllama(
    model='llama3.2',
    temperature=0
)

message = [
    SystemMessage(
        content=(
            'Ты опытный специалист по Python Backend, '
            'отвечай на вопросы кратко и с примерами'
        )
    ),
    HumanMessage(
        content=(
            'Что такое Python? для чего используем?'
        )
    )
]

response = model.invoke(message)
print(response.content)