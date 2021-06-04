#!/bin/bash

sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv -y

python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt

for service in country_api population_api stats_api server
do
python3 -m pytest $service --cov=$service --cov-report=xml --junitxml=junit/test-results.xml
done

# python3 -m pytest country_api --cov=country_api --cov-report=xml --junitxml=junit/test-results.xml

# python3 -m pytest population_api --cov=population_api --cov-report=xml --junitxml=junit/test-results.xml

# python3 -m pytest stats_api --cov=stats_api --cov-report=xml --junitxml=junit/test-results.xml

# python3 -m pytest server --cov=server --cov-report=xml --junitxml=junit/test-results.xml