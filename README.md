# PNal28A21

Topics analysis by protesters tweets about the tax reform law in April 28th 2021. The analysis has started previous to the protest event and pretends continue the analysis for a couple of weeks after the protest.

## Tools and configuration

### Python 3 

Check your current version and set or [install the version 3](https://dev.to/meetsohail/change-the-python3-default-version-in-ubuntu-1ekb)

### Pip

To manage dependencies and packages

``` 

sudo apt install python3 python3-dev python3-venv
```

Create an alias for pip3. 

``` 

cd <your home directory>
vim .bashrc
#Add the followin line
alias pip=pip3
```

Close your console and open a new one.

### VSCode 

Code editor. 

### Black 

Code formatter here you have an[installation and configuration guide](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0)

### Virtualenv 

To isolate your dependencies. See section: [Using venv to isolate dependencies](https://cloud.google.com/python/docs/setup#linux_2)

### google-cloud 

SDK for developers. Recommendation: Install the SDK in your virtual environment.
To activate your virtual env is active:

``` 

source env/bin/activate
```

To install google cloud sdk

``` 

pip install google-cloud
```

# How to run

1. Init your cloud SDK

``` 

./google-cloud-sdk/bin/gcloud init  
```

2. Set the path to your service account key file

``` 

export GOOGLE_APPLICATION_CREDENTIALS="<PATH_TO_SERVICE_ACCOUNT_JSON_KEY_FILE>"
```

3. Set enviromental variables.

``` 
export BEARER_TOKEN=<YOUR_TOKEN> 
```

4. Execute `python streaming.py`
