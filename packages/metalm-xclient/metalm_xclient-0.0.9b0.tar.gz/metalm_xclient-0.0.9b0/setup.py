from setuptools import setup
with open('./README.md','r') as f:
    data = f.read()
if __name__ == "__main__":
    setup(long_description=data)
