from django.shortcuts import render

# Create your views here.
def shades(request):
    shading_table = []
    for i in range(0, 50):
        gs = (i * 5)
        s = 255 - gs
        shading_table.append({"red": f"#{s:02x}0000",
                              "green": f"#00{s:02x}00",
                              "blue": f"#0000{s:02x}",
                              "black": f"#{gs:02x}{gs:02x}{gs:02x}"})
    return render(request, "ex03/shades.html", {"table": shading_table})