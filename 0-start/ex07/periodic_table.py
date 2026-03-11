def read_file():
    data = None
    with open("periodic_table.txt", "r") as f:
        data = f.read()
    if not data:
        print("Could not open the file")
        return 

    table = []
    lines = filter(lambda e: e != "", data.split("\n"))
    for line in lines:
        name, vals = line.split("=")
        vals_dict = {}
        for val in vals.split(","):
            k, v = val.split(":")
            vals_dict[k.strip()] = v.strip()
        vals_dict["period"] = len(vals_dict["electron"].split(" "))
        if name.strip() == "Palladium":
            vals_dict["period"] += 1
        table.append((name.strip(), vals_dict))

    return table

def get_elem(data, i, j):
    for (name, vals) in data:
        if vals["period"] == i and vals["position"] == str(j):
            return (name, vals)
    return None

def elem_str(elem):
    name, vals = elem
    ret = "  " * 3 + '<td style="border:1px solid black; padding:5px">\n'
    ret += "  " * 4 + f"<h4>{name}</h4>\n"
    ret += "  " * 4 + "<ul>\n"
    ret += "  " * 5 + f'<li>No {vals["number"]}</li>\n'
    ret += "  " * 5 + f'<li>{vals["small"]}</li>\n'
    ret += "  " * 5 + f'<li>{vals["molar"]}</li>\n'
    ret += "  " * 5 + f'<li>{vals["electron"]}</li>\n'
    ret += "  " * 4 + "</ul>\n"
    ret += "  " * 3 + "</td>\n"
    return ret

def get_lanthanides():
    ret = "  " * 3 + '<td style="border:1px solid black; padding:5px">\n'
    ret += "  " * 4 + f"<h4>Lanthanides</h4>\n"
    ret += "  " * 4 + "<ul>\n"
    ret += "  " * 5 + f'<li>No 57-71</li>\n'
    ret += "  " * 4 + "</ul>\n"
    ret += "  " * 3 + "</td>\n"
    return ret

def get_actinides():
    ret = "  " * 3 + '<td style="border:1px solid black; padding:5px">\n'
    ret += "  " * 4 + f"<h4>Actinides</h4>\n"
    ret += "  " * 4 + "<ul>\n"
    ret += "  " * 5 + f'<li>No 89-103</li>\n'
    ret += "  " * 4 + "</ul>\n"
    ret += "  " * 3 + "</td>\n"
    return ret

def periodic_table():
    data = read_file()
    if not data:
        return

    html = "<!DOCTYPE html>\n"
    html += "<html>\n"
    html += "<title>\n"
    html += "  " + "Periodic table\n"
    html += "</title>\n"

    html += "<body>\n"
    html += "  " + "<table>\n"

    for i in range(1, 8):
        html += "  " * 2 + "<tr>\n"
        for j in range(0, 18):
            if i == 6 and j == 2:
                html += get_lanthanides()
                continue
            if i == 7 and j == 2:
                html += get_actinides()
                continue
            elem = get_elem(data, i, j)
            if elem:
                html += elem_str(elem)
            else:
                html += "  " * 3 + "<td></td>\n"
        html += "  " * 2 + "</tr>\n"

    html += "  " + "</table>\n"
    html += "</body>\n"
    html += "</html>"

    with open("periodic_table.html", "w") as f:
        f.write(html)


if __name__ == "__main__":
    periodic_table()
