from setuptools import setup

with open('README.md', encoding='utf-8') as f: # README.md 내용 읽어오기
    long_description = f.read()

setup(
    name='baseball-data', # 패키지 이름
    version='0.0.0.1', # 버전 등록
    long_description=long_description, # readme.md 등록
    long_description_content_type='text/markdown',  # readme.md 포맷
    description='baseball API', # 패키지 설명
    author='basekk', # 작성자 등록
    author_email='jino152637@gmail.com', # 이메일 등록
    url='', # url 등록
    license='MIT', # 라이센스 등록
    python_requires='>=3.4', #파이썬 버전 등록
    install_requires=["pymysql", "prettytable", "tabulate"], # module 필요한 다른 module 등록
    packages=['baseball_data'] # 업로드할 module이 있는 폴더 입력
)
