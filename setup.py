from setuptools import setup, find_packages

setup(
    name="t20-system-runtime",
    version="0.1.0",
    py_modules=["runtime"],
    packages=find_packages(),
    install_requires=[
        "google-genai==1.26.0",
        "python-dotenv==1.0.0",
        "pyyaml==6.0.2",
        "ollama==0.5.3",
        "colorama==0.4.6",
        "huggingface_hub==0.34.4",
        "openai==1.107.0",
        "mistralai==1.9.10",
    ],
    entry_points={
        "console_scripts": [
            "t20-system=runtime.sysmain:main",
            "t20-console=runtime.cli:main",
        ],
    },
)