# Zendesk Ticket Viewer
A python CLI utility to view support tickets through Zendesk's API

## Installation
**Dependencies**: Python 3.7.3, Pandas 0.24.2
1. Clone this repository to your local machine or download as zip file
2. Ensure you have Python 3.7.3 and Pandas installed

**Installing Python**: To install the latest version of Python, please follow [this guide](https://docs.python-guide.org/starting/install3/osx/). It includes installing Homebrew, a package manager

The full environment in which this script was run is provided below this readme for reference

## Usage
1. Credentials will be provided separately for security reasons. This will be emailed to you directly or if it does not go through, please request it from my email
2. The default path of credentials should be placed in the same directory as the script. The path to the credentials file should be provided as the first argument to the zendesk_coding_challenge.py as below:
```
$ python3 zendesk_coding_challenge.py credentials.txt
```
## Further Notes
Although I am familiar with Java, I took this opportunity to learn Python after consulation with my peers as I judge it to be the most suitable language for this specific task.

Full environment: 
```
basicauth==0.4.1
certifi==2019.3.9
chardet==3.0.
idna==2.8
numpy==1.16.4
pandas==0.24.2
python-dateutil==2.8.0
pytz==2019.1
requests==2.22.0
six==1.12.0
urllib3==1.25.3
```
