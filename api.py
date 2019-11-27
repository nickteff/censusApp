from backend import api

from waitress import serve

debug = True

if __name__ == '__main__':
    if debug:
        api.run(port=9999, debug=debug)
    else:
        serve(api, port=9999, debug=debug)
