from setuptools import setup, find_packages

setup(
    name='sqlhttpcss',  # パッケージ名
    version='0.5',  # バージョン
    description='これは、C#のアプリケーションとHTTP通信して、データベース化したものです',  # パッケージの説明
    long_description=open('README.md').read(),  # README.md の内容を長い説明として使用
    long_description_content_type='text/markdown',  # README.md の形式
    author='Your Name',  # 作者
    author_email='your.email@example.com',  # 作者のメールアドレス
    url='https://github.com/yourusername/my_library',  # プロジェクトのURL
    license='MIT',  # ライセンス
    packages=find_packages(),  # パッケージを自動的に探す
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 対応するPythonのバージョン
    install_requires=[
        'requests',  # 依存パッケージ
    ],
)
