import scrapy
import json
from scTaker.items import Track 


client_id = "luWcnwCEWokSADZxVeKLcyZXAuOPSjLC"
all_likes_request: str = "https://api-v2.soundcloud.com/users/317883075/track_likes?offset=1532751595251515&limit=2&client_id=luWcnwCEWokSADZxVeKLcyZXAuOPSjLC&app_version=1537434439&app_locale=en"

def track_links_request(track_id: int) -> str:
    return f"https://api.soundcloud.com/i1/tracks/{track_id}/streams?client_id=luWcnwCEWokSADZxVeKLcyZXAuOPSjLC"

class TakerSpider(scrapy.Spider):
    name = "taker"

    def start_requests(self):
        yield scrapy.Request(all_likes_request, self.take_track_ids)

    def take_track_ids(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        for song in jsonresponse["collection"]:
            print(song["track"]["title"])
            request = scrapy.Request(
                track_links_request(song["track"]["id"]),
                self.take_track_links
            )
            request.meta['title'] = song["track"]["title"].replace(" ", "")
            yield request

    def take_track_links(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        print(jsonresponse['hls_mp3_128_url'])
        yield Track(file_url=jsonresponse['hls_mp3_128_url'], title=response.meta['title'])

