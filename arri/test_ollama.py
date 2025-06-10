# test_ollama.py
from langchain_ollama import ChatOllama
from langchain_community.llms import Ollama

print("Test 1: ChatOllama")
try:
    llm1 = ChatOllama(
        model="llama3.1:8b",
        base_url="http://localhost:11434",
        temperature=0.1
    )
    response1 = llm1.invoke("Hello, just respond with Test successful")
    print("ChatOllama works:", response1)
except Exception as e:
    print("ChatOllama failed:", str(e))

print("\nTest 2: Ollama Community")
try:
    llm2 = Ollama(
        model="llama3.1:8b",
        base_url="http://localhost:11434"
    )
    response2 = llm2.invoke("Hello, just respond with Test successful")
    print("Ollama Community works:", response2)
except Exception as e:
    print("Ollama Community failed:", str(e))

print("\nTest 3: Version check")
try:
    import crewai
    print("CrewAI version:", crewai.__version__)
except:
    print("CrewAI version: Not available")

try:
    import langchain_ollama
    print("LangChain Ollama installed: Yes")
except ImportError:
    print("LangChain Ollama installed: No")

try:
    import langchain_community
    print("LangChain Community installed: Yes")
except ImportError:
    print("LangChain Community installed: No")