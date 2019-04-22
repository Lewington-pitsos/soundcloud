import scrapy
import json
from scTaker.items import Track 


client_id = "luWcnwCEWokSADZxVeKLcyZXAuOPSjLC"


def liked_tracks_request(offset: int) -> str:
    return f"https://api-v2.soundcloud.com/users/317883075/track_likes?offset={offset}&limit=2000&client_id=luWcnwCEWokSADZxVeKLcyZXAuOPSjLC&app_version=1537434439&app_locale=en"

def track_links_request(track_id: int) -> str:
    return f"https://api.soundcloud.com/i1/tracks/{track_id}/streams?client_id=luWcnwCEWokSADZxVeKLcyZXAuOPSjLC"

class TakerSpider(scrapy.Spider):
    name = "taker"

    def start_requests(self):
        yield scrapy.Request(
            liked_tracks_request(1532751595251515), 
            self.take_track_ids,
        )

    def take_track_ids(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        for song in jsonresponse["collection"]:
            request = scrapy.Request(
                track_links_request(song["track"]["id"]),
                self.take_track_links
            )
            request.meta['title'] = song["track"]["title"].replace(" ", "").replace("/", "-").replace("|", "-")
            yield request

        try:
            next_link = jsonresponse["next_href"]
        except KeyError:
            pass
        
        if next_link is not None:
            yield scrapy.Request(
                liked_tracks_request(next_link.split("=")[1].split("&")[0]), 
                self.take_track_ids,
            )
        else:
            print(">>>>>>>>>>> Retrived ID's of all Liked Tracks <<<<<<<<<<<<<<<<")


    def take_track_links(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        yield Track(file_url=jsonresponse['hls_mp3_128_url'], title=response.meta['title'])

