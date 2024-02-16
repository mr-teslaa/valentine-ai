from application import create_app

app = create_app()

# production = False
production = True

if production is False:
    if __name__ == '__main__':
        app.run(debug=True)
else:
    if __name__ == '__main__':
        app.run()