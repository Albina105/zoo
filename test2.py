from langchain.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

temperatures = [0, 0.3, 0.5, 0.7, 1.0]

message = [
    SystemMessage(
        content=''
    ),
    HumanMessage(
        content='Python это ...'
    )
]

for i in temperatures:
    model = ChatOllama(
        model='llama3.2:latest',
        temperature=i,
        num_predict = 50
    )

    print(f'temperature: {i}')
    response = model.invoke(message)
    print(response.content)
    print(response.response_metadata.get("done_reason"))
    print(response.response_metadata.get('eval_count'))