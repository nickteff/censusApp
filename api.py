from backend import api

from waitress import serve

debug = True

if __name__ == '__main__':
    if debug:
        api.run(host='0.0.0.0', port='9999', debug=debug)
    else:
        serve(api, host='0.0.0.0', port='9999')
