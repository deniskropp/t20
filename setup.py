from setuptools import setup, find_packages

setup(
    name="t20-system-runtime",
    version="0.1.0",
    py_modules=["runtime"],
    packages=find_packages(),
    install_requires=[
        "google-genai",
        "python-dotenv",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "t20-system=runtime.sysmain:system_main",
            "t20-temp=runtime.temp:temp_main",
        ],
    },
)