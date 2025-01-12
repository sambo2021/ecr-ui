# ecr-ui
=============
- This is a quick web interface to list the repositories, and the images they contain in an [Amazon ECR] registry. It consists of python code in FastApi frameworks and simple js,html ans css.
- To allow people in teams to view the list of different types of images we hold in our registry and what tags we have for a given container.

# FastAPI
=============
- A simple web app, mostly it is a proxy to the [Boto3] methods `describe_repositories` and `describe_images`. Because of hundreds of repositories, the Boto3 methods support pagination.

# Config
======
- One thing to configure, the registry-id

# How To run app locally or on ec2 machine
=============
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- uvicorn app:app --reload --port 5050


# web interface
=============
![Example of the homepage](https://raw.githubusercontent.com/sambo2021/ecr-ui/master/screenshots/screen.png "Example of the homepage")
