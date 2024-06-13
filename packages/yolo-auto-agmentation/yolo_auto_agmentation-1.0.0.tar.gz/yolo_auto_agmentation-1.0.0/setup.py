from setuptools import setup, find_packages

setup(
    name='yolo_auto_agmentation',
    version='1.0.0',
    description='enter dataset path with train, val, test. Then automatically augment every images to ready YOLO object detection train',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Na-I-Eon',
    author_email='112fkdldjs@naver.com',
    url='https://github.com/Nyan-SouthKorea/yolo_auto_augmentation',
    packages=find_packages(),
    install_requires=[
        'cv2', 'tqdm', 'albumentations', 'natsort'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)