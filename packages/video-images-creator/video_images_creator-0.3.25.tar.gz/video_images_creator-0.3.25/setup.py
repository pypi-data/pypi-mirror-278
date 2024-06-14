from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='video_images_creator',
    version='0.3.25',
    description= "Create videos from images using the 'video_images_creator' package.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='Nikhil Sharma',
    author_email='nikhilsharma972@gmail.com',
    license='BSD 2-clause',
    packages=['video_images_creator'],
    package_dir={"": "src"},
    package_data={"video_images_creator": ["*.ttf", "video-music.wav", "instantvideoaudio.wav", "audionew.wav", "thanks.wav", "background_music.wav", '*.jpg', '*.jpeg', '*.png']},
    install_requires=['opencv-python', 'numpy', 'pillow', 'azure-cognitiveservices-speech==1.37.0','pydub','requests'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)
