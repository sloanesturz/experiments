import requests
import re

URLS = [
    "http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/bus.ljansbakken-oslo",
    "http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/metro.kalbakken-jernbanetorget",
    "http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/tram.ljabru-jernbanetorget",
    "http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/tram.jernbanetorget-ljabru",
    "http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/tram.jernbanetorget-universitetssykehuset",
    "http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/ferry.nesoddtangen-oslo",
    "http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/car.aarnes-elverum",
    "http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/car.oslo-grimstad",
    "http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/car.snaroya-smestad",
    "http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/train.oslo-vestby",
    "http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/train.vestby-oslo"
]


needed = {}

for url in URLS:
    name = url.split('/')[-1]
    resp = requests.get(url)
    links = re.findall('href="([^"]+)"', resp.text)
    if links:
        needed[name] = [(url + "/" + u) for u in links if 'report' in u]


for name, urls in needed.iteritems():
    for url in urls:
        resp = requests.get(url)
        with open("traces/" + name + "." + url.split("/")[-1], 'w') as f:
            f.write(resp.text)
