from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="temp_sms",
    version="1.0",
    description="Temporary phone numbers for receiving SMS in python.",
    author="Commenter123321",
    packages=["temp_sms"],
    install_requires=["playwright"],
    license="GPL-3.0",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        "temporary",
        "sms",
        "number",
        "python",
        "phone",
        "receive"
    ]
)
