import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone

from extensions import mongo
from main import main
print("Start")

#def create_app(config_object='settings'):
print("create_app")
app = Flask(__name__)
Bootstrap(app)

app.config.from_object('settings')

mongo.init_app(app)

Dropzone(app)

app.register_blueprint(main)

app.debug = True
        
    #return app
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)