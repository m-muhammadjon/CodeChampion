from urllib.request import urlopen

from django.core.files.temp import NamedTemporaryFile


def set_avatar(backend, user, response, *args, **kwargs):
    if backend.name == "github":
        avatar_url = response.get("avatar_url", None)

        if avatar_url:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(avatar_url).read())
            img_temp.flush()
            user.avatar.save(f"avatar_{user.pk}.webp", img_temp)
