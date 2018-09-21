import scrapy
import json

client_id = "luWcnwCEWokSADZxVeKLcyZXAuOPSjLC"
all_likes_request: str = "https://api-v2.soundcloud.com/users/317883075/track_likes?offset=1532751595251515&limit=2000&client_id=luWcnwCEWokSADZxVeKLcyZXAuOPSjLC&app_version=1537434439&app_locale=en"

class TakerSpider(scrapy.Spider):
    name = "taker"
    start_urls = [
        all_likes_request,
    ]

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        for song in jsonresponse["collection"]:
            print(song["track"]["id"])
