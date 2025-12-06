# conan-nested-repository
Example project created with intent of demonstrating how complicated project structure can raise problems [when using Git and Conandata coordinates/checkouts in source() and export() methods](https://github.com/conan-io/conan/issues/19325).
# Compile and run our main target
by calling `conan build . --build-missing` inside **src/some_binary** directory on any branch.
# Reproduce the problem
by calling `conan create . --build-missing` inside **src/some_binary** directory on **main** branch,
It leads to an error:
> some_binary/1.0: Calling source() in [...]/.conan2/p/some_e217bc9e074d4/s/src/some_binary
> some_binary/1.0: Cloning git repo   some_binary/1.0: RUN: git clone "<hidden>" --origin=origin "."   
> ERROR: some_binary/1.0: Error in source() method, line 27   git.checkout_from_conandata_coordinates()  
> ConanException: Command 'git clone "git@github.com:archetypiarz/conan-nested-repository.git" --origin=origin "."' failed with errorcode '128'   b"fatal: destination path '.' already exists and is not an empty directory.\n"
