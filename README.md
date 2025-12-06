# conan-nested-repository
Example project created with intent of demonstrating how complicated project structure can raise problems [when using Git and Conandata coordinates/checkouts in source() and export() methods](https://github.com/conan-io/conan/issues/19325).
## Compile and run our main target
by calling `conan build . --build-missing` inside **src/some_binary** directory on any branch.
## Reproduce the problem
by calling `conan create . --build-missing` inside **src/some_binary** directory on **main** branch,
It leads to an error:
>CMake Error: The source directory "[...]/.conan2/p/b/some_83ee8ffd28d1b/b/src/some_binary" does not appear to contain CMakeLists.txt.
>Specify --help for usage, or press the help button on the CMake GUI.
>
>some_binary/1.0: ERROR: 
>Package '9ba585daca407606d04aaddf685f658ee492f8bc' build failed
>some_binary/1.0: WARN: Build folder [...]/.conan2/p/b/some_83ee8ffd28d1b/b/src/some_binary/build/Release
>ERROR: some_binary/1.0: Error in build() method, line 31
>        cmake.configure()
>        ConanException: Error 1 while executing

As we can see, original paths have been violated. 

`tree [...]/.conan2/p/b/some_83ee8ffd28d1b/b/src/some_binary/`

    [...]/.conan2/p/b/some_83ee8ffd28d1b/b/src/some_binary/
    ├── build
    │   └── Release
    │       └── generators
    │           ├── cmakedeps_macros.cmake
    │           ├── CMakePresets.json
    [...]
    ├── README.md
    └── src
        ├── conanfile.py
        ├── some_binary
        │   ├── CMakeLists.txt
        │   ├── conanfile.py
        │   └── main.cpp
        └── some_library
            ├── CMakeLists.txt
            ├── include
            │   └── print.h
            └── print.cpp
    
    8 directories, 24 files


And, when we change `Git(self)` to `Git(self, "../..)`:

> some_binary/1.0: Calling source() in [...]/.conan2/p/some_e217bc9e074d4/s/src/some_binary
> some_binary/1.0: Cloning git repo   some_binary/1.0: RUN: git clone "<hidden>" --origin=origin "."   
> ERROR: some_binary/1.0: Error in source() method, line 27   git.checkout_from_conandata_coordinates()  
> ConanException: Command 'git clone "git@github.com:archetypiarz/conan-nested-repository.git" --origin=origin "."' failed with errorcode '128'   b"fatal: destination path '.' already exists and is not an empty directory.\n"
### What is the problem here?
`source()` method is being called from `self.source_folder`, which in case of this project consists of joined git project root path and `conan.folders.subproject` defined in `layout()`. That means *git* tries to clone starting from a project subdirectory, which is apparently a problem. It causes a path mismatch. 
It also conflicts with `Git(self, self.folders.root)` when our recipe lays not on the top of project structure. Calling `checkout_from_conandata_coordinates()` or just `git clone` from there leads to an error, beacuse you can't *clone* from non-empty directory.

## First walkaround: `with conan.tools.files.chdir`
Call `conan create . --build=missing` inside **src/some_binary** directory on **walkaround_with** branch.
### What changed here?
`source()` method now calls `git clone "."` from upper directory after `cd`-ing to root of the repo and removes empty directories leading to `self.folders.subproject`: **src/some_binary**.

    def source(self):
            assert self.folders.root == "../.."
            with chdir(self, os.path.join(self.source_folder, self.folders.root)):
                rmdir(self, "src")
                git = Git(self)
                git.checkout_from_conandata_coordinates()
