from databasehandler import data_henter, lat_long
from matplotlib.figure import Figure 
import base64
from io import BytesIO

def plotter1(adresse):
    try:
        fig = Figure()
        ax = fig.subplots()
        y = data_henter(adresse)
        categories = ['Rest', 'Mad', 'Plast', 'Pap']
        ax.bar(categories, y)
        buf = BytesIO()
        fig.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        data_img = f"<img style='img-fluid' src='data:image/png;base64,{data}'/>"
        return  data_img
    except:
        return """<h1 style="color:red;">Indtast venligst en gyldig adresse</h1> <img src=static/bobby-hill-bicycle.gif>"""


def mapper(type1):
    waypoints = []
    rest,mad,plast,pap = lat_long()
    temp = "&origin=55.688170,12.561280&destination=55.688170,12.561280&waypoints="
    try:
        if type1 == "rest":
            for i in rest:
                waypoints.append(i[0])
            if len(waypoints) > 18:
                for n in range(0,18):
                        if n == 0:
                            temp += str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
                        else:
                            temp += "|"+ str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
            else:
                for n in range(0,len(waypoints)):
                    if n == 0:
                        temp += str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
                    else:
                        temp += "|"+ str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
        if type1 == "mad":
            for i in mad:
                waypoints.append(i[0])
            if len(waypoints) > 18:
                for n in range(0,18):
                    if n == 0:
                        temp += str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
                    else:
                        temp += "|"+ str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
            else:
                for n in range(0,len(waypoints)):
                    if n == 0:
                        temp += str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
                    else:
                        temp += "|"+ str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
        if type1 == "plast":
            for i in plast:
                waypoints.append(i[0])
            if len(waypoints) > 18:
                for n in range(0,18):
                    if n == 0:
                        temp += str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
                    else:
                        temp += "|"+ str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
            else:
                for n in range(0,len(waypoints)):
                    if n == 0:
                        temp += str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
                    else:
                        temp += "|"+ str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
        if type1 == "pap":
            for i in pap:
                waypoints.append(i[0])
            if len(waypoints) > 18:
                for n in range(0,18):
                    if n == 0:
                        temp += str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
                    else:
                        temp += "|"+ str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
            else:
                for n in range(0,len(waypoints)):
                    if n == 0:
                        temp += str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
                    else:
                        temp += "|"+ str(waypoints[n]).replace("(","").replace(")","").replace(" ","")
        return temp
    except Exception as e:
        print(e)

mapper("rest")