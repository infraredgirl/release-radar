import releaseradar

app = releaseradar.create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55555, debug=True)
