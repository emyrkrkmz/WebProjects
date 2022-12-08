from tortoise import models, fields
from pydantic import BaseModel, Extra
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime


class apost(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50)
    votes = fields.IntField(default = 0)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

post_ = pydantic_model_creator(apost, name="post")
postIn = pydantic_model_creator(apost, name="CreatePost", exclude_readonly=True)


class acomment(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)
    
comment_ = pydantic_model_creator(acomment, name="comment")
comIn = pydantic_model_creator(acomment, name="CreateComment", exclude_readonly=True)