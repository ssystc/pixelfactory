import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from webserver import app
import config

config.Log = app.logger
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=config.WEB_SERVER_PORT)
