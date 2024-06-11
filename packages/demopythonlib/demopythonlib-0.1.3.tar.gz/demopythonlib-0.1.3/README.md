# Guide
0. Require:
    - Python >= 3.7
    - Poetry >= 1.2.0
1. Prepare
    - Install poetry 
    - Using poetry to create new source or init to existed source

2. Configure pyproject.toml
    - Minimum requirements
    ```
    [tool.poetry]
    name = "demopythonlib"      -> project / package name
    version = "0.1.0"           -> pypi only accept code with new version 
    packages = [{include = "demopythonlib"}] -> is package should be packed then push to pypi
    
    ...

    [tool.poetry.dependencies]
    python = "^3.12"            -> python version should fit with your project
    ...

    [tool.poetry.scripts]
    say-hi = "demopythonlib:say_hi"     -> add custom command to run directly from terminal -> like "celery -A worker ...."
    ...

    ```
3. Prepare your pypi account
    - Create new if you need: https://pypi.org/account/register/ 
    - Add 2FA to your account
    - Login > Account Settings > Tokens
    - Add API Token: create a token for all projects (for first time publish) - copy it and securely storage

4. Publish first time
    - Build 
        ```
        $ poetry build
        
        ->  Building demopythonlib (0.1.0)
            - Building sdist
            - Built demopythonlib-0.1.0.tar.gz
            - Building wheel
            - Built demopythonlib-0.1.0-py3-none-any.whl
        ```
    - Add credential
        ``` https://python-poetry.org/docs/repositories/#configuring-credentials
        $ poetry config pypi-token.pypi <your-token>
        ```
    - Publish
        ```
        $ poetry publish

        ->  Publishing demopythonlib (0.1.0) to PyPI
            - Uploading demopythonlib-0.1.0-py3-none-any.whl 100%
            - Uploading demopythonlib-0.1.0.tar.gz 100%
        ```

    - Recheck: go to https://pypi.org/project/project-name/
        ```
        for my example ->  https://pypi.org/project/demopythonlib/
        ```

5. Revoke your full access token above, then create new token for this project for security 

6. Publish new version
    - In pyproject.toml, change version manually 
        ``` pyproject.toml
        [tool.poetry]
        name = "demopythonlib"
        version = "0.1.1"       -> change from 0.1.0 to 0.1.1 for example  
        
        ```
    - Or use bump2version (https://github.com/c4urself/bump2version)
    - Build then publish
        ```
        $ poetry build

        ->  Building demopythonlib (0.1.1)
            - Building sdist
            - Built demopythonlib-0.1.1.tar.gz
            - Building wheel
            - Built demopythonlib-0.1.1-py3-none-any.whl


        $ poetry publish

        ->  Publishing demopythonlib (0.1.1) to PyPI
            - Uploading demopythonlib-0.1.1-py3-none-any.whl 100%
            - Uploading demopythonlib-0.1.1.tar.gz 100%
        ```

7. Integrate locally
    - From main project, You need to import this library locally, 
    ```
    $ poetry add ./<path/to/your/lib> --editable
    ```
    - Use option "--editable" if you want changes in your local library to be reflected immediately in your project

8. What next? 
    - Add precommit, bump2verion, ...
    - Add tests
    - Integrate with github/gitlab
        + run workflow CI/CD  
        + build then publish new release to pypi automatically
