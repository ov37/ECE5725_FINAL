from flask import Flask, request, render_template

app = Flask(__name__)

msg_dict = {}

@app.route('/', methods=['POST', 'GET'])
def message_form_post():
    if request.method == 'GET':
        return render_template('html_example.html')
    
    message = request.form['message']
    print(message)
    #msg_dict[message] = message

    #templateData = {
    #        'msg_dict' : msg_dict
    #}

    #send message to the other server here, maybe via FIFO?

    #return render_template('page.html', **templateData)
    return render_template('html_example.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')


