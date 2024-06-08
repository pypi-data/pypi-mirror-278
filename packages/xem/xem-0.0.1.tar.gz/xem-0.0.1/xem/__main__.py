import json
import time
import pathlib
from argparse import ArgumentParser
from base64 import b64decode
from flask import Flask, render_template, make_response, request
from .gcontainer import GunicornApplication

# Argument parser
ap = ArgumentParser()
ap.add_argument("-l", "--log", default="EventLog.jsonl",
                help="path to where we should save event log file")
ap.add_argument("-p", "--port", default="3939",
                help="port to listen for connections")
ap.add_argument("-H", "--host", default="0.0.0.0",
                help="host to listen for connections")
args = ap.parse_args()

event_log = args.log

# Setup
# http://probablyprogramming.com/2009/03/15/the-tiniest-gif-ever
pixelGifBase64 = "R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
# pixelGifBase64 = "R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs="
pixelGif = b64decode(pixelGifBase64)
tracking_script = \
    """
    async function _run_xem_now() {
        var currentURL = window.location.toString()
        function xem(property) {
            console.log(window.location.toString());
            const url = window.location.toString();
            const referrer = document.referrer;
            const xemURL = "%(utm_gif_url)s" + "?" +
                           "url=" +
                           encodeURIComponent(url) +
                           "&property=" +
                           encodeURIComponent(property) +
                           "&referrer=" +
                           encodeURIComponent(referrer);
            image = new Image();
            image.src = xemURL;
        }
        setInterval(function(){
            let newURL = window.location.toString();
            if (newURL !== currentURL) {
                xem("%(property)s")
                currentURL = newURL;
            }
        }, 1000);
        xem("%(property)s")
    }
    _run_xem_now()
    """


# Flask App
template_folder = pathlib.Path(__file__)\
                         .expanduser()\
                         .parent\
                         .joinpath("templates")\
                         .resolve()
app = Flask(__name__, template_folder=template_folder)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/xem.js')
def script():
    prop = request.args.get("property")
    root_url = request.url_root
    utm_gif_url = root_url + "utm.gif"
    if prop is None:
        return ""

    params = {
        "utm_gif_url": utm_gif_url,
        "property": prop
    }
    response = make_response(tracking_script % params)
    response.headers['Content-Type'] = "text/javascript"
    response.headers['Cache-Control'] = ('no-store, no-cache, must-revalidate,'
                                         ' post-check=0, pre-check=0,'
                                         ' max-age=0')
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route('/utm.gif')
def tracker():
    response = make_response(pixelGif)
    response.headers['Content-Type'] = 'image/gif'
    response.headers['Cache-Control'] = ('no-store, no-cache, must-revalidate,'
                                         ' post-check=0, pre-check=0,'
                                         ' max-age=0')
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'

    # begin tracking code
    visitor_arrival_time = time.time()
    visitor_referrer = request.args.get("referrer", "")
    visitor_property = request.args.get("property", "")
    visitor_url = request.args.get("url")
    visitor_ip = request.remote_addr

    # don't write logs if property is none
    if visitor_property == "":
        return response

    with open(event_log, "a") as fh:
        event = {
            "name": "PageView",
            "property": visitor_property,
            "url": visitor_url,
            "referrer": visitor_referrer,
            "arrival_time": visitor_arrival_time,
            "ip": visitor_ip,
        }
        fh.write(json.dumps(event))
        fh.write("\n")

    return response


if __name__ == '__main__':
    import multiprocessing as mp
    cpu_count = mp.cpu_count()
    options = {
        'bind': '%s:%s' % (args.host, args.port),
        'workers': min(cpu_count+1, 4),
        'timeout': 120,
    }
    guni_app = GunicornApplication(app, options)
    guni_app.run()
