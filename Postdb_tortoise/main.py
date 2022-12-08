from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Extra
from datetime import datetime

from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from models import post_, postIn, apost, comment_, comIn, acomment

app = FastAPI(title="My Reddit")


class Status(BaseModel):
    message: str


@app.get("/")
def root():
    return "OK"

@app.get("/posts", response_model=List[post_])
async def get_posts():
    return await post_.from_queryset(apost.all())


@app.get("/posts/{post_id}", response_model=post_)
async def get_one(post_id: int):
    return await post_.from_queryset_single(apost.get(id=post_id))

@app.post("/posts", response_model=post_)
async def create_post(post: postIn):
    post_obj = await apost.create(**post.dict(exclude_unset=True))
    return post_obj


@app.patch("/posts/upvote/{post_id}")
async def upvote_post(post_id: int):
    post = await apost.get(id=post_id)
    await apost.filter(id=post_id).update(votes = post.votes + 1)
    return await post_.from_queryset_single(apost.get(id=post_id))


@app.patch("/posts/downvote/{post_id}")
async def downvote_post(post_id: int):
    post = await apost.get(id=post_id)
    await apost.filter(id=post_id).update(votes = post.votes - 1)
    return await post_.from_queryset_single(apost.get(id=post_id))


@app.put("/posts/{post_id}", response_model=post_, responses={404: {"model": HTTPNotFoundError}})
async def update_post(post_id: int, post: postIn):
    await apost.filter(id=post_id).update(**post.dict(exclude_unset=True))
    return await post_.from_queryset_single(apost.get(id=post_id))


@app.delete("/posts/{post_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_post(post_id: int):
    deleted_count = await apost.filter(id=post_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404)
    return Status(message=f"Deleted user {post_id}")

## COMMENTS


@app.get("/comments", response_model=List[comment_])
async def get_posts():
    return await comment_.from_queryset(acomment.all())

@app.get("/comments/{comment_id}", response_model=comment_)
async def get_one(comment_id: int):
    return await comment_.from_queryset_single(apost(id=comment_id))

@app.post("/comments")
async def create_comment(comment: comIn):
    comment_obj = await acomment.create(**comment.dict(exclude_unset=True))
    return await comment_.from_tortoise_orm(comment_obj)

@app.put("/comments/{comment_id}")
async def update_comment(comment_id: int, comment: comIn):
    await acomment.filter(id=comment_id).update(**comment.dict(exclude_unset=True))
    return await comment_.from_queryset_single(acomment.get(id=comment_id))

@app.delete("/comments/{comment_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_comment(comment_id: int):
    deleted_com = await acomment.filter(id=comment_id).delete()
    if not deleted_com:
        raise HTTPException(status_code=404)
    return Status(message=f"Deleted comment {comment_id}")    
    

register_tortoise(
    app,
    db_url="sqlite://post_data.db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)