from app import create_server

port = 5000
app = create_server()

if __name__ == "__main__":
    app.run(debug=True, port=port)