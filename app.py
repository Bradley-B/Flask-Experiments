from Main import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4567, threaded=True)

application = app
