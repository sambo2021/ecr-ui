from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
import datetime

app = FastAPI()
templates= Jinja2Templates(directory="templates")
ecr_client = boto3.client('ecr')

registry_id="REPLACE_ME"

@app.get('/',response_class=HTMLResponse)
def ecr_repos(request: Request ):
    try:
        repos = get_repositories(registry_id)['repositories']
        registry = {}
        for repo in repos:
            key = repo['repositoryName']
            images = get_images(registry_id,repo['repositoryName'])['imageDetails']
            value = images
            registry[key] = value
        return  templates.TemplateResponse("index.html",{"request": request, "repositories": registry})
    except (BotoCoreError, NoCredentialsError) as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get('/json')
def ecr_repos():
    try:
        repos = get_repositories(registry_id)['repositories']
        registry = {}
        for repo in repos:
            key = repo['repositoryName']
            images_before = get_images(registry_id,repo['repositoryName'])['imageDetails']
            ## list comperhension with dictionary unpacking
            ## to manipulate images dictionary keys 
            images_after =  [{
                            **image,
                            "imagePushedAt": image['imagePushedAt'].strftime("%d/%m/%Y, %H:%M:%S"),
                            "imageSizeInMB": round(image.get('imageSizeInBytes', 0) / (1024 * 1024), 1)
                        } for image in images_before
            ]
            keys_to_drop = ["imageSizeInBytes","registryId","repositoryName","imageManifestMediaType","artifactMediaType"]
            value = {"date": repo['createdAt'].strftime("%d/%m/%Y, %H:%M:%S"),
                     "url": repo['repositoryUri'],
                     "images": [
                         ## list comperhension with dictionary unpacking
                         ## to drop some image's dictionary keys 
                         {k: v for k, v in item.items() if k not in keys_to_drop}for item in images_after
                        ]
            }
            registry[key] = value
        return  registry
    except (BotoCoreError, NoCredentialsError) as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

# return all repos
def get_repositories(registry_id):
    paginator = ecr_client.get_paginator('describe_repositories')
    page_iterator = paginator.paginate(registryId=registry_id)
    response = {'repositories': []}
    for page in page_iterator:
        response['repositories'].extend(page['repositories'])
    return response


# return all images for specific repo
def get_images(registry_id, repository_name):
    paginator = ecr_client.get_paginator('describe_images')
    page_iterator = paginator.paginate(
        registryId=registry_id, repositoryName=repository_name)
    response = {'imageDetails': []}
    for page in page_iterator:
        response['imageDetails'].extend(page['imageDetails'])
    return response
