import pytest

from main import app, Status
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from models import apost, acomment

import sqlite3


db = sqlite3.connect('post_data.db')

cursor = db.cursor()
cursor.execute(''' SELECT * FROM apost
            	''')
postdatas = cursor.fetchall()
cursor.execute(''' SELECT * FROM acomment
            	''')

commentdatas = []
for i in cursor.fetchall():
    if i not in postdatas:
        commentdatas.append(i)



db_post = {
    "title": "emir",
    "votes": 10,
}

db_comment = {
    "title": "max",
}


@pytest.fixture(scope="module", autouse=True)
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def client():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client


@pytest.mark.anyio
async def test_get_postlist(client: AsyncClient):
    global postdatas
    response = await client.get("/posts")
    assert postdatas == response.json()


async def test_root(client):
     response = await client.get("/")
     assert response.status_code == 200
     assert response.json() == "OK"


async def test_create_post(client: AsyncClient):
    response = await client.post("/posts", json=db_post)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == db_post["title"]
    assert data["votes"] == db_post["votes"]
    assert "id" in data
    post_id = data["id"]

    post_obj = await apost.get(id=post_id)
    assert post_obj.id ==post_id

async def delete_post(client: AsyncClient):
    response = await client.delete("/post/{post_id}")
    assert response.status_code == 200
    


#COMMENT TESTS

async def test_create_comment(client: AsyncClient):
    response = await client.post("/comments", json=db_comment)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == db_comment["title"]
    assert "id" in data
    comment_id = data["id"]

    comment_obj = await acomment.get(id=comment_id)
    assert comment_obj.id ==comment_id
    
@pytest.mark.anyio
async def test_get_commentlist(client: AsyncClient):
    global commentdatas
    response = await client.get("/comments")
    assert commentdatas == response.json()




# async def test_get_one_post_after_creation(client ):
#     response = await client.get("/posts")
#     assert response.status_code == 200
#     data = await response.json()
#     data[0].pop('created_at')
#     data[0].pop('updated_at')
#     assert data == [db_post]

# def test_update_post():
#     post = {
#         "title": "different post",
#         "votes": 10,
#     }
#     response = client.put(f"/posts/{db_post['id']}", json=post)
#     assert response.status_code == 200
#     data = response.json()
#     assert data['title'] == post['title']
#     assert data['votes'] == post['votes']
    
# def test_upvote_post():
#     response = client.patch(f"/posts/upvote/{db_post['id']}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data['votes'] == db_post['votes'] + 1

# def test_downvote_post():
#     response = client.patch(f"/posts/downvote/{db_post['id']}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data['votes'] == db_post['votes']


# def test_del_post():
#     response = client.delete(f"/posts/{db_post['id']}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data == db_post['id']

# # ##COMMENT PART


# def test_get_empty_comment():
#     response = client.get("/comments")
#     assert response.status_code == 200
#     data = response.json()
#     assert data == []

# def test_create_comment():
#     comment = {
#         "title": db_comment["title"]
#     }
#     response = client.post("/comments", json=comment)
#     assert response.status_code == 200
#     data = response.json()
#     data.pop('created_at')
#     data.pop('updated_at')
#     assert data == db_comment  

# def test_get_one_comment():
#     response = client.get(f"/comments/{db_comment['post_id']}")
#     assert response.status_code == 200
#     data = response.json()
#     data.pop('created_at')
#     data.pop('updated_at')
#     assert data == db_comment  
    
# def test_update_comment():
#     comment = {
#         "new_title": "different comment",
#     }
#     response = client.put(f"/comments/{db_comment['post_id']}", json=comment)
#     assert response.status_code == 200
#     data = response.json()
#     assert data['title'] == comment['new_title']

# def test_del_comment():
#     response = client.delete(f"/comments/{db_comment['post_id']}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data == db_comment['post_id']
