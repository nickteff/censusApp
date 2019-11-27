from backend import server
from frontend import index, app1

from waitress import serve


debug = False

if __name__ == '__main__':
    app1.app.enable_dev_tools(debug=False)
    index.app.enable_dev_tools(debug=False)
    if debug:
        server.run(host='0.0.0.0', port=9990, debug=debug)
    else:
        serve(server, host='0.0.0.0', port=9990)
