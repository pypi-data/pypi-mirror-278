from argparse import ArgumentParser
from .gapp import GunicornApplication
from .server import app
import multiprocessing as mp


if __name__ == '__main__':
    # Argument parser
    ap = ArgumentParser()
    ap.add_argument("-l", "--log", default="EventLog.jsonl.gz",
                    help="path to where we should save event log file")
    ap.add_argument("-p", "--port", default="3939",
                    help="port to listen for connections")
    ap.add_argument("-H", "--host", default="127.0.0.1",
                    help="host to listen for connections")
    ap.add_argument("-d", "--debug", action="store_true", default=False,
                    help="host to listen for connections")

    args = ap.parse_args()
    app.config["event_log"] = args.log

    if args.debug:
        app.run(debug=True, host=args.host, port=args.port)
    else:
        cpu_count = mp.cpu_count()
        options = {
            'bind': '%s:%s' % (args.host, args.port),
            'workers': min(cpu_count+1, 4),
            'timeout': 120,
        }
        guni_app = GunicornApplication(app, options)
        guni_app.run()
