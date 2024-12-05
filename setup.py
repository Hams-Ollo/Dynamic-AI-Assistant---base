from setuptools import setup, find_packages

setup(
    name="dynamic-ai-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "langchain",
        "langchain-groq",
        "langchain-community",
        "langchain-core",
        "langchain-huggingface",
        "langchain-chroma",
        "chromadb",
    ],
)
