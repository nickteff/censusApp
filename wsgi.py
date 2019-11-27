from backend import server
from frontend import index, app1, app2

from waitress import serve


debug = True

if __name__ == '__main__':
    app1.app.enable_dev_tools(debug=False)
    app2.app.enable_dev_tools(debug=False)
    index.app.enable_dev_tools(debug=False)
    if debug:
        server.run(host='0.0.0.0', port=8080, debug=debug)
    else:
        serve(server, host='0.0.0.0', port=8080)

