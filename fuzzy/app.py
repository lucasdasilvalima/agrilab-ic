from fuzzy_api import server

app = server.app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
