import os.path
import shutil
import sysconfig
from pathlib import Path
import time

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.sdist import sdist
from wheel.bdist_wheel import bdist_wheel


home_dir = Path.home()
install_dir = sysconfig.get_paths()["purelib"]
print(home_dir)
print(install_dir)

current = Path(__file__).parent.absolute()
src_dir = current / "src"

VERSION = "0.2.0"


def generate_sumake(home_dir, current):
    sumake_dir = home_dir / ".sumake"
    bin_dir = current / "bin"

    if not os.path.exists(sumake_dir):
        os.makedirs(sumake_dir)
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
    print("current", current)
    print("src_dir", src_dir)

    utils_mk = sumake_dir / "utils.mk"
    # shutil.copy(src_dir / "utils.mk", utils_mk)
    with os.scandir(src_dir) as dirs:
        for f in dirs:
            if f.is_file() and not f.name == "sumake":
                shutil.copy(f, sumake_dir / f.name)
    # shutil.copy(src_dir / "utils.py", sumake_dir / "utils.py")
    # open("./sumake")
    with open(src_dir / "sumake", "r") as template:
        with open(bin_dir / "sumake", "w") as target:
            res = template.read().format(
                UTILS_MK=utils_mk,
                VERSION=VERSION,
            )
            target.write(res)


def generate_version():
    with open(current / "version.txt", "w") as f:
        f.write(VERSION)
        # f.write(f"""VERSION = "{VERSION}" """)


class PreBdistWheel(bdist_wheel):
    def run(self):
        generate_sumake(home_dir, current)
        bdist_wheel.run(self)


class PreSDist(sdist):
    def run(self):
        generate_sumake(home_dir, current)
        sdist.run(self)


class PreInstall(install):
    def run(self):
        generate_sumake(home_dir, current)
        install.run(self)


if __name__ == "__main__":
    generate_version()
    setup(
        author="SuCicada",
        author_email="pengyifu@gmail.com",
        classifiers=[],
        description="A generic makefile for projects.",
        scripts=["bin/sumake"],
        cmdclass={
            "install": PreInstall,
            "bdist_wheel": PreBdistWheel,
            "sdist": PreSDist,
        },
        install_requires=["setuptools"],
        include_package_data=True,
        # package_data={
        #     '': ['sumake', 'utils.mk'],
        # },
        # install_requires=[],
        # keywords="",
        # license="",
        long_description=open("README.md").read(),
        name="sumake",
        # namespace_packages=[],
        # packages=find_packages(),
        # py_modules=["."],
        # test_suite="",
        url="https://github.com/SuCicada/sumake",
        version=VERSION,
        zip_safe=False,
        packages=find_packages("src"),
        package_dir={"": "src"},
        options={'egg_info': {'egg_base': "./"}},
)
