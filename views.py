def index():
    with open('templates/index.html') as template:
        return template.read()


def custom():
    with open('templates/custom.html') as template:
        return template.read()
