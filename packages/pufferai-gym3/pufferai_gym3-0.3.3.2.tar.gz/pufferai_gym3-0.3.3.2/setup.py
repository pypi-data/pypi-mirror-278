import os

from setuptools import setup, find_packages

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
README = open(os.path.join(SCRIPT_DIR, "README.md"), "rb").read().decode("utf8")

setup(
    name="pufferai_gym3",
    packages=find_packages(),
    version="0.3.3.2",
    install_requires=[
        "numpy>=1.11.0,<2.0.0",
        "cffi>=1.13.0,<2.0.0",
        "imageio>=2.6.0,<3.0.0",
        "imageio-ffmpeg>=0.3.0,<0.4.0",
        "glfw==2.7",
        "moderngl>=5.5.4,<6.0.0",
    ],
    package_data={"gym3": ["libenv.h", "internal/font.bin"]},
    python_requires=">=3.6.0",
    extras_require={
        "test": [
            "pytest==5.2.1",
            "pytest-benchmark==3.2.2",
            "gym-retro==0.8.0",
            "gym==0.17.2",
            "tensorflow==1.15.0",
            "mpi4py==3.0.3",
        ]
    },
    description="Vectorized Reinforcement Learning Environment Interface",
    # this is broken in twine for some reason
    #   warning: `long_description_content_type` missing.  defaulting to `text/x-rst`.
    # long_description=README,
    # long_description_content_type="text/markdown",
    url="https://github.com/pufferai/gym3",
    author="OpenAI",
)
