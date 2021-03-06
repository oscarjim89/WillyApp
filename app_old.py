from flask import Flask, render_template, jsonify
from Willy import *
from datetime import datetime
import os

app = Flask(__name__)

path = os.path.dirname(os.path.realpath(__file__))

#W = Willy(left=(17,18), right=(22,23), speed=0.5)

#def get_photos():
#    photo_files = glob("%s/static/photos/*.jpg" % path)
#    photos = ["/static/photos/%s" % photo.split('/')[-1] for photo in photo_files]
#    return sorted(photos, reverse=True)

@app.route('/')
def index():
    global W
    W = Willy(left=(17,18), right=(22,23), speed=0.6)
    return render_template('index.html')
#    photos = get_photos()
#    return render_template('index.html', photos=photos)

@app.route('/FW/', methods=['POST'])
def FW():
    W.forwardClick()
    return render_template('index.html')


@app.route('/BW/', methods=['POST'])
def BW():
    W.backwardClick()
    return render_template('index.html')

@app.route('/right/', methods=['POST'])
def right():
    W.rightClick()
    return render_template('index.html')

@app.route('/left/', methods=['POST'])
def left():
    W.leftClick()
    return render_template('index.html')

@app.route('/stop/', methods=['POST'])
def stop():
    W.stopClick()
    return render_template('index.html')

##ejemplo para AJAX
#@app.route('/_get_data/', methods=['POST'])
#def _get_data():
#
#    #W = Willy(left=(17,18), right=(22,23), speed=0.5)
#    W.forward(0.1)
#    response = "Moving forward..."
#    return jsonify({'data': response})

#@app.route('/view/<photo>/')
#def view(photo):
#    return render_template('view.html', photo=photo)

#@app.route('/tweet/<photo>/')
#def tweet(photo):
#    photo_path = '%s/static/photos/%s.jpg' % (path, photo)
#    message = "I'm at the @Raspberry_Pi stand at #bett2015"
#    with open(photo_path, 'rb') as media:
#        twitter.update_status_with_media(status=message, media=media)
#    return render_template('view.html', photo=photo, tweeted=True)

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
