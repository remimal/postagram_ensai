import json
import boto3
from botocore.config import Config
import os
from dotenv import load_dotenv
from typing import Union
import logging
from fastapi import FastAPI, Request, status, Header
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import uuid

from getSignedUrl import getSignedUrl

load_dotenv()

app = FastAPI()
logger = logging.getLogger("uvicorn")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logger.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Post(BaseModel):
    title: str
    body: str


my_config = Config(
    region_name='us-east-1',
    signature_version='v4',
)

dynamodb = boto3.resource('dynamodb', config=my_config)
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))
s3_client = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4'))
bucket = os.getenv("BUCKET")


@app.post("/posts")
async def post_a_post(post: Post, authorization: str | None = Header(default=None)):

    logger.info(f"title : {post.title}")
    logger.info(f"body : {post.body}")
    logger.info(f"user : {authorization}")

    # Doit retourner le résultat de la requête la table dynamodb
    item = {
        'user': f"USER#{authorization}",
        'id': f'POST#{uuid.uuid4()}',
        'title': post.title,
        'body': post.body,
    }

    response = table.put_item(Item=item)
    return response

@app.get("/posts")
async def get_all_posts(user: Union[str, None] = None):

    # Doit retourner une liste de post

    if(user is None):
         response = table.scan()
    else:    
        response = table.query(
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression="user = :user",
            ExpressionAttributeValues={
                ":user": f"USER#{user}",
            },
        )

    logger.info(json.dumps(response, indent=2))
    return response["Items"]

    
@app.delete("/posts/{post_id}")
async def get_post_user_id(post_id: str):

    #### post_id ne doit pas avoir le "POST#" du début !
    #### post_id="svcfshiusjsuud" -> bien
    #### post_id="POST#svcfshiusjsuud" -> pas bien

    # Doit retourner le résultat de la requête la table dynamodb
    post_to_delete_list = table.query(
        Select='ALL_ATTRIBUTES',
        IndexName="InvertedIndex",
        KeyConditionExpression="id = :id",
        ExpressionAttributeValues={
            ":id": f"POST#{post_id}",
        },
    )

    post_to_delete = post_to_delete_list["Items"][0]

    # TODO: delete picture in s3

    response = table.delete_item(
         Key= {
              "user": post_to_delete["user"],
              "id": post_to_delete["id"]
         }
    )

    return response

@app.get("/signedUrlPut")
async def get_signed_url_put(filename: str,filetype: str, postId: str,authorization: str | None = Header(default=None)):
    return getSignedUrl(filename, filetype, postId, authorization)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")

