from dataclasses import dataclass
import random
from pathlib import Path

from faker import Faker
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('main'),
    autoescape=select_autoescape()
)

template = env.get_template("index.html")

fake = Faker()

subreddits = ('rust', 'python', 'js', 'css', 'webdev', 'html', 'oss', 'linux', 'gaming', 'cs')


@dataclass
class Post:
    name: str
    subreddit: str
    by: str
    votes: int
    comments: int
    date: int


output_path = Path('output')
output_path.mkdir(exist_ok=True)

post_per_page = 10
number_of_pages = 10
for i in range(number_of_pages):
    posts = [
        Post(
            name=fake.sentence(),
            subreddit=random.choice(subreddits),
            by=fake.name(),
            votes=random.randint(0, 250),
            comments=random.randint(0, 100),
            date=random.randint(1, 24),
        )
        for _ in range(post_per_page)]

    with open(output_path.joinpath(f'{i+1}.html'), 'w') as f:
        f.write(template.render(posts=posts, current_page=i, total_pages=number_of_pages, subreddits=subreddits))
