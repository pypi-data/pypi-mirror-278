import setuptools

with open('readme.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="turing-planet",
    version="0.1.4",
    author="jianwu6",
    author_email="jianwu6@iflytek.com",
    description="Python Extension Framework For Turing Planet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://code.iflytek.com/osc/_source/Y_RDG-TURING/gpt/turing-planet/-/tree/heads%2Fdevelop",
    python_requires=">=3.9.0, <3.10.0",
    packages=setuptools.find_packages(),
    install_requires=[
        'langchain==0.1.0',
        'llama-index==0.10.0',
        'websocket-client==1.6.4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
