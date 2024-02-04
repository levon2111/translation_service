Create www directory where project sites and environment dir

    mkdir /var/www && mkdir /var/envs && mkdir /var/envs/bin

Install virtualenvwrapper

    sudo pip3 install virtualenvwrapper
    sudo pip3 install --upgrade virtualenv

Add these to your bashrc virutualenvwrapper work

    export WORKON_HOME=/var/envs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    export PROJECT_HOME=/var/www
    export VIRTUALENVWRAPPER_HOOK_DIR=/var/envs/bin
    source /usr/local/bin/virtualenvwrapper.sh

Create virtualenv

    mkvirtualenv --python=python3 translation_service


Install Docker and docker-compose.
    Before Running please configure the environment variables.
        1. create a copy from .env.example > .env
        2. set GOOGLE_APPLICATION_CREDENTIALS (for test purposes we have `[google_creds.json](google_creds.json)``)
        3. set GOOGLE_PARENT_PROJECT_ID
        4. other env variables no need to change


Run this:

    ```bash
    docker-compose -f local.yml build
    docker-compose -f local.yml up -d
    ```

Git hook scripts
    Useful for identifying simple issues before submission to code review.
     - Run `pre-commit install`


