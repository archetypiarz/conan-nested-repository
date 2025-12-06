import os
from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMake
from conan.tools.scm import Git

class some_binary(ConanFile):
    name = "some_binary"
    version = "1.0"
    url="https://github.com/archetypiarz/conan-nested-repository.git"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("fmt/12.1.0")

    def layout(self):
        self.folders.root = "../.."
        self.folders.subproject = "src/some_binary"
        cmake_layout(self)

    def export(self):
        git = Git(self, "../..")
        git.coordinates_to_conandata() 

    def source(self):
        git = Git(self)
        git.checkout_from_conandata_coordinates()
        
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        self.run(os.path.join(self.cpp.build.bindirs[0], "some_binary"))
