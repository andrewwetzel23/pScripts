from setuptools import setup, find_packages

setup(
    name="mf",  # Replace with your own package name
    version="0.1.0",
    description="My Functions",  # Replace with your own description
    author="Andrew Wetzel",  # Replace with your own name
    author_email="youremail@example.com",  # Replace with your own email
    url="https://github.com/username/Your-Package-Name",  # Replace with the URL of your project
    packages=find_packages(),  # Automatically find all packages and subpackages. Or you can manually specify them as a list, like ["mypackage", "mypackage.subpackage", "mypackage.another_subpackage"]
    install_requires=[
        "numpy",  
        "matplotlib",
        "opencv-python-headless",  # cv2
        "pillow",
        "tqdm",
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
