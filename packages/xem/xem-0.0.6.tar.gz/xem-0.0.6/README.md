# XEM

XEM is a simple web analytics server written in Python and Flask.

"Xem" means "to see" or "to watch" in Vietnamese.

## Usage

Run this on a server host:

```
pip install xem
python -m xem
```

Add the following script tag to all pages on your website you want to track with `xem`:

```
<script async src="http://your.server.org:3939/xem.js?property=PROPERTYID" type="text/javascript" />
```

where `PROPERTYID` is a 10-character alphanumeric unique ID to identify your site.







