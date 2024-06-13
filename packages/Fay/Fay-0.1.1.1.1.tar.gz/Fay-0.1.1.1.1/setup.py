import platform
from setuptools import setup, find_packages
import setuptools

# 获取当前操作系统
current_os = platform.system()

# 基于操作系统的依赖项
common_requires = [
    'requests',
    'numpy',
    'websockets~=10.2',
    'ws4py~=0.5.1',
    'pyaudio~=0.2.11',
    'flask~=3.0.0',
    'openpyxl~=3.0.9',
    'pygame~=2.1.2',
    'flask_cors~=3.0.10',
    'PyQtWebEngine~=5.15.5',
    'eyed3~=0.9.6',
    'websocket-client',
    'azure-cognitiveservices-speech',
    'aliyun-python-sdk-core==2.13.3',
    'scipy~=1.10.0',
    'simhash',
    'pytz',
    'gevent~=22.10.1',
    'edge_tts~=6.1.3',
    'ultralytics~=8.0.2',
    'pydub',
    'cemotion',
    'langchain==0.0.336',
    'eyed3',
    'chromadb',
]

if current_os == 'Windows':
    os_specific_requires = [
        'pyqt5~=5.15.6',
    ]
else:
    os_specific_requires = [
        'pyqt5~=5.13',
    ]

install_requires = common_requires + os_specific_requires

setup(
    name='Fay',
    version='0.1.1.1.1',
    include_package_data=False,
    install_requires=install_requires,
    url='https://github.com/xszyou/Fay/tree/fay-assistant-edition',
    license='MIT',
    author='Fay',
    author_email='xszyou@yaheen.com',
    description='Fay is an open-source digital human framework integrating language models and digital characters. It offers retail, assistant, and agent versions for diverse applications like virtual shopping guides, broadcasters, assistants, waiters, teachers, and voice or text-based mobile assistants.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)