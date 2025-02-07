import os
from uuid import uuid1

def upload_post_photo(instance, filename: str) -> str:
    ext = filename.split('.')[-1]
    return os.path.join(f"posts/{instance.author.id}", f"{uuid1()}.{ext}")

