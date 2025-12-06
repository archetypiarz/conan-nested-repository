# conan-nested-repository
Example project created with intent of demonstrating how complicated project structure can raise problems [when using Git and Conandata coordinates/checkouts in source() and export() methods](https://github.com/conan-io/conan/issues/19325).
## Compile and run our main target
by calling `conan build . --build-missing` inside **src/some_binary** directory on any branch.
## Reproduce the problem
by calling `conan create . --build-missing` inside **src/some_binary** directory on **main** branch,
It leads to an error:
> some_binary/1.0: Calling source() in [...]/.conan2/p/some_e217bc9e074d4/s/src/some_binary
> some_binary/1.0: Cloning git repo   some_binary/1.0: RUN: git clone "<hidden>" --origin=origin "."   
> ERROR: some_binary/1.0: Error in source() method, line 27   git.checkout_from_conandata_coordinates()  
> ConanException: Command 'git clone "git@github.com:archetypiarz/conan-nested-repository.git" --origin=origin "."' failed with errorcode '128'   b"fatal: destination path '.' already exists and is not an empty directory.\n"
### What is the problem here?
`source()` method is being called from `self.source_folder`, which in case of this project consists of joined git project root path and `conan.folders.subproject` defined in `layout()`. That means *git* tries to clone starting from a project subdirectory, which is apparently a problem. Even if that worked it would cause a path mismatch. 
What's more, it's conflicting with `checkout_from_conandata_coordinates()`, beacuse apparently you can't clone to a non-empty directory. Calling `git = Git(self, "../..")` doesn't lead to the actual changing of the current directory, nor it passes that path to internal *git* calls.
You have to change directory to the root folder, remove everything and then proceed to clone.

## First walkaround: `with conan.tools.files.chdir`
Call `conan create . --build=missing` inside **src/some_binary** directory on **walkaround_with** branch.
### What changed here?
`source()` method now calls `git clone "."` from upper directory after `cd`-ing to root of the repo and removes empty directories: **src/some_binary**.

    def source(self):
            assert self.folders.root == "../.."
            with chdir(self, os.path.join(self.source_folder, self.folders.root)):
                rmdir(self, "src")
                git = Git(self)
                git.checkout_from_conandata_coordinates()
