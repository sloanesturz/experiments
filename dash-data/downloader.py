# This script scraped all of the video chunks (65 per encoding)

import requests

base_url = "http://dash.edgesuite.net/envivio/dashpr/clear/"
medias = ["audio"] + ["video%s" % (i+1,) for i in range(5)]

def download(media_name, id):
    url = base_url + m + "/" + id + ".m4s"
    r = requests.get(url)
    if r.status_code == 200:
        with open(media_name + "/" + id + ".m4s", "wb") as f:
            f.write(r.content)
            return True
    return False

for m in medias:
    url = base_url + m + "/"
    download(m, "Header")
    i = 0
    while download(m, str(i)):
        print "Downloaded %s %s" % (m, i)
        i += 1

