from setuptools import setup, find_packages

setup(
    name="pinyinPDF",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # 在这里添加你的依赖包，例如：
        # "numpy",
        "reportlab",
    ],
    author="mohist",
    author_email="yangxiaohua@mohist.ai",
    description="Generate PinYinPDF pdf file package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hellotern/pinyin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
