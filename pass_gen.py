def pass_gen(name, phone, email):
    file = open("template.html", "r")

    html = file.read()
    html = html.replace("{{name}}", name)
    html = html.replace("{{phone}}", phone)
    html = html.replace("{{email}}", email)

    file.close()

    return html
