from setuptools import setup, find_packages

setup(
    name="roop-pip",
    version="1.0.0-alpha",
    packages=find_packages(),
    install_requires=[
        "numpy==1.24.3",
        "opencv-python==4.8.0.74",
        "onnx==1.14.0",
        "insightface==0.7.3",
        "psutil==5.9.5",
        "tk==0.1.0",
        "customtkinter==5.2.0",
        "tkinterdnd2==0.3.0; sys_platform != 'darwin' and platform_machine != 'arm64'",
        "tkinterdnd2-universal==1.7.3; sys_platform == 'darwin' and platform_machine == 'arm64'",
        "pillow==10.0.0",
        "onnxruntime==1.15.1; python_version != '3.9' and sys_platform == 'darwin' and platform_machine != 'arm64'",
        "onnxruntime-coreml==1.13.1; python_version == '3.9' and sys_platform == 'darwin' and platform_machine == 'arm64'",
        "onnxruntime-silicon==1.13.1; sys_platform == 'darwin' and platform_machine == 'arm64'",
        "onnxruntime-gpu==1.15.1; sys_platform != 'darwin'",
        "tensorflow==2.13.0",
        "opennsfw2==0.10.2",
        "protobuf==4.23.4",
        "tqdm==4.65.0",
        "gfpgan==1.3.8",
    ],
    dependency_links=[
        "https://download.pytorch.org/whl/cu118"
    ],
    author="Amartya Deshmukh",
    author_email="dedsec.konohamaru@gmail.com",
    description="One-click face swap",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Konohamaru04/roop-pip",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'roop=roop.run:main',  # Adjust if necessary
        ],
    },
)
