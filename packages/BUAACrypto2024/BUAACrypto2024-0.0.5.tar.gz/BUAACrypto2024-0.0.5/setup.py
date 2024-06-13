import setuptools

 
package_name = "BUAACrypto2024"
 
 
 
def upload():
    with open("README.rst", "r",encoding='utf-8') as fh:
        long_description = fh.read()
    with open('requirements.txt') as f:
        required = f.read().splitlines()
 
    setuptools.setup(
        name=package_name,
        version="0.0.5",
        author="pyrjx",  # 作者名称
        author_email="3441252502@qq.com", # 作者邮箱
        description="this is a simple crypto packet for some cryptomatic algorithm", # 库描述
        long_description=long_description,
         # 库的官方地址
        packages=setuptools.find_packages(),
        data_files=["requirements.txt"], # yourtools库依赖的其他库
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=required,
    )
 
 

def main():
    try:
        upload()
        print("Upload success ")
    except Exception as e:
        raise Exception("Upload package error", e)
 
 
if __name__ == '__main__':
    main()
