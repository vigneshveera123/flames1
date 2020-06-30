from flask import Flask,render_template,request



app=Flask(__name__)

@app.route('/flames')

def flames():
    return render_template("flames.html")


@app.route('/login',methods=['post'])


def Flames():

    your_name = request.form["YOUR NAME"]
    caple_name= request.form["YOUR CAPLE NAME"]


    c = set(your_name)
    d = set(caple_name)

    c.intersection_update(d)

    g = len(c)

    if your_name != " ":
        return render_template('hello.html',name=g)















if __name__=="__main__":
    app.debug=True
    app.run()
