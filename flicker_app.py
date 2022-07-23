# import statements
import requests_with_caching
from flicker_creds import api_key
from timer import Timer

# import webbrowser  # allows the url to be opened in a browser.

flickr_key = api_key


@Timer(text="Downloaded the 5 flickr urls in {:.2f} seconds")
def get_flickr_data(tags_string):
    baseurl = "https://api.flickr.com/services/rest/"
    params_diction = {"api_key": flickr_key, "tags": tags_string, "tag_mode": "all",
                      "method": "flickr.photos.search", "per_page": 5, "media": "photos",
                      "format": "json", "nojsoncallback": 1}
    flickr_resp = requests_with_caching.get(baseurl, params=params_diction)
    # Useful for debugging: print the url! Uncomment the below line to do so.
    # print(flickr_resp.url)  # Paste the result into the browser to check it out...

    if type(flickr_resp) is dict:
        return flickr_resp
    return flickr_resp.json()


img_query = input("What type of flickr image would you like to search: Separate different words with a comma(,)\n")
results = get_flickr_data(img_query)

# Some code to open up a few photos that are tagged with the mountains and river tags...

photos = results['photos']['photo']
for photo in photos:
    owner = photo['owner']
    photo_id = photo['id']
    url = 'https://www.flickr.com/photos/{}/{}'.format(owner, photo_id)
    print(url)
    # webbrowser.open(url)
