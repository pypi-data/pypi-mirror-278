import json
import gzip
from . import models
import pathlib
import flask
from flask import Flask, render_template, make_response, request
from base64 import b64decode
from datetime import datetime, timezone


# Setup
# http://probablyprogramming.com/2009/03/15/the-tiniest-gif-ever
# pixelGifBase64 = "R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs="
pixelGifBase64 = "R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
pixelGif = b64decode(pixelGifBase64)
tracking_script = \
    """
    class Xem {

        constructor(siteId, xemUrl){
            this.xemUrl = xemUrl;
            this.siteId = siteId;
            this.currentUrl = "";
        }

        emit(event) {
            // encode data as base64 json string
            const payloadJSON = JSON.stringify(event);
            const payloadBase64 = btoa(payloadJSON);

            // build url
            const notificationUrl = this.xemUrl + "?" +
                "data=" + payloadBase64;

            console.log(notificationUrl)

            // send notificaiton to server
            let image = new Image();
            image.src = notificationUrl;
        }

        emitPageView() {
            const pageUrl = window.location.toString();
            const referrer = document.referrer;
            const event = {
                "name": "PageView",
                "siteId": this.siteId,
                "referrer": referrer,
                "pageUrl": pageUrl,
                "prevUrl": this.currentUrl
            }
            this.emit(event);
        }

        async start() {
            let newURL = window.location.toString();
            if (newURL !== this.currentURL) {
                this.emitPageView();
                this.currentURL = newURL;
            }
            setTimeout(() => {
                this.start()
            }, 1000);
        }
    }
    const xem = new Xem("%(siteId)s", "%(tracking_url)s");
    xem.start();
    """


# Flask App
template_folder = pathlib.Path(__file__)\
                         .expanduser()\
                         .parent\
                         .joinpath("templates")\
                         .resolve()
app = Flask(__name__, template_folder=template_folder)


# ======
# Routes
# ======

def home():
    return render_template('index.html')


def script():
    prop = request.args.get("siteId")
    root_url = request.url_root
    tracking_url = root_url + "tk"
    if prop is None:
        return ""

    params = {
        "tracking_url": tracking_url,
        "siteId": prop
    }
    response = make_response(tracking_script % params)
    response.headers['Content-Type'] = 'text/javascript'
    return response


def tracker():
    response = make_response(pixelGif)
    response.headers['Content-Type'] = 'image/gif'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    response.headers['Cache-Control'] = (
        'no-store, no-cache, must-revalidate,'
        ' post-check=0, pre-check=0,'
        ' max-age=0'
    )

    # begin tracking code
    event_data = read_event_data(request)
    event_source_ip = get_source_ip(request)
    event_time = datetime.now(timezone.utc)
    event_time_str = event_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    # augment event data with time and ip
    event_data["time"] = event_time_str
    event_data["sourceIp"] = event_source_ip

    # validate event
    event = validate_event_data(event_data)

    # write to event log
    event_log = app.config["event_log"]
    with gzip.GzipFile(event_log, "a") as fh:
        event_json = event.model_dump_json()
        fh.write(bytes(event_json, "utf-8"))
        fh.write(bytes("\n", "utf-8"))

    return response


# =========
# Utilities
# =========

def read_event_data(req: flask.Request):
    event_base64 = req.args.get("data")
    if event_base64 is None:
        flask.abort(400, "no data sent")
    event_json = b64decode(event_base64.encode("ascii"))
    event_data = json.loads(event_json)
    return event_data


def get_source_ip(request: flask.Request):
    """
    Get source IP Address from request
    """
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr


def validate_event_data(event_data: dict):
    """
    Validate user sent event data
    """
    etype = models.Event
    if event_data.get("name") == "PageView":
        etype = models.PageViewEvent
    return etype.model_validate(event_data)


# ===============
# Register routes
# ===============

app.route('/')(home)
app.route('/xem.js')(script)
app.route('/tk')(tracker)
# app.route('/test')(test)
