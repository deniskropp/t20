from setuptools import setup, find_packages

setup(
    name="t20",
    version="0.1.0",
    description="The T20 Multi-Agent System SDK",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "google-genai==1.26.0",
        "python-dotenv==1.0.0",
        "pyyaml==6.0.2",
        "ollama==0.5.3",
        "colorama==0.4.6",
        "huggingface_hub==0.34.4",
        "openai==1.107.0",
        "mistralai==1.9.10",
        "fastapi==0.111.0",
        "uvicorn==0.29.0",
        "pydantic>=2.0.0",
        "sse-starlette",
        "rich",
        "typer"
    ],
    entry_points={
        "console_scripts": [
            "t20-system=t20_cli.system:main",
            "t20-hitl=t20_cli.hitl:main",
            "t20-api=t20_api.main:main",
        ],
    },
)
