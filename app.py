from flask import Flask, render_template, jsonify, request
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
    try:
        W = Willy(left=(17,18), right=(22,23), speed=0.5, sonar=(4,15))
    except:
        print("Error: Error al cargar el objeto Willy")
    return render_template('Willy.html')
#    photos = get_photos()
#    return render_template('index.html', photos=photos)

@app.route('/FW/', methods=['POST'])
def FW():
    W.forwardClick()
    now = datetime.now()
    response = now.strftime("%H:%M:%S: ")+"Moving forward...<BR>"
    return jsonify({'data': response})


@app.route('/BW/', methods=['POST'])
def BW():
    W.backwardClick()
    now = datetime.now()
    response = now.strftime("%H:%M:%S: ")+"Moving backward...<BR>"
    return jsonify({'data': response})

@app.route('/right/', methods=['POST'])
def right():
    W.rightClick()
    now = datetime.now()
    response = now.strftime("%H:%M:%S: ")+"Moving right...<BR>"
    return jsonify({'data': response})

@app.route('/left/', methods=['POST'])
def left():
    W.leftClick()
    now = datetime.now()
    response = now.strftime("%H:%M:%S: ")+"Moving left...<BR>"
    return jsonify({'data': response})

@app.route('/stop/', methods=['POST'])
def stop():
    W.stopClick()
    now = datetime.now()
    response = now.strftime("%H:%M:%S: ")+"Stop!<BR>"
    return jsonify({'data': response})

@app.route('/distance', methods=['POST'])
def distance():
    x = request.form['x']
    y = request.form['y']
    W.goPosition(x,y)
    now = datetime.now()
    response = now.strftime("%H:%M:%S: ")+"Go position: x: "+x+", y:"+y+" <br>"
    if(W.isRecording() != 0):
        svgresponse = "<svg height=\"500\" width=\"500\"><line x1=\"0\" y1=\"0\" x2=\""+x*10+"\" y2=\""+y*10+"\" style=\"stroke:rgb(255,0,0);stroke-width:2\" /></svg>" 
    else:
        svgresponse = "<h3>Not recording...</h3>"
    return jsonify({'data': response, 'svgdata': svgresponse})

@app.route('/rotate', methods=['POST'])
def rotate():
    deg = request.form['deg']
    W.rotatebyDegrees(int(deg))
    now = datetime.now()
    response = now.strftime("%H:%M:%S: ")+"Rotate "+deg+"º<BR>"
    return jsonify({'data': response})

@app.route('/rotateleft/', methods=['POST'])
def rotateleft():
    W.rotatebyTime(direction="left",seconds=None)
    now = datetime.now()
    response = now.strftime("%H:%M:%S: ")+"Rotating left...<BR>"
    return jsonify({'data': response})

@app.route('/rotateright/', methods=['POST'])
def rotateright():
    W.rotatebyTime(direction="right",seconds=None)
    now = datetime.now()
    response = now.strftime("%H:%M:%S: ")+"Rotating right...<BR>"
    return jsonify({'data': response})

@app.route('/startJ/', methods=['POST'])
def startJ():
    title = request.form['title']
    response = W.recordJournal(title)
    now = datetime.now()
    if (response == 0):
        response = now.strftime("%H:%M:%S: ")+title+", Recording stated!<BR>"
    elif (response == 1):
        response = now.strftime("%H:%M:%S: ")+"Recording failed<BR>"
    else:
        response = now.strftime("%H:%M:%S: ")+"Journal exist! Try again!<BR>"
    return jsonify({'data': response})

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
    app.run(debug=True, port=5000, host='0.0.0.0')
