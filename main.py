from flask import Flask, request, render_template
import psycopg2

from getSQL import *
from knn import *

print("")

def getDataFromOdoo(limit = 0):
    conexion1 = psycopg2.connect(database="odoo2",
                                 user="odoo",
                                 password="odoo",
                                 host="localhost",
                                 port="5432")
    cursor1 = conexion1.cursor()
    sql = ""

    if limit == 0:
        sql = "select sale_order.name,create_date,amount_total from sale_order ORDER BY sale_order.name;"
    else:
        sql = f"select sale_order.name,create_date,amount_total from sale_order ORDER BY sale_order.name LIMIT {limit};"

    cursor1.execute(sql)
    row = 0
    data = []
    row = cursor1.fetchall()
    for i in row:
        temp = list(i)
        temp[len(temp)-1] = str(temp[len(temp)-1]) + "<br>"
        data.append(temp)

    conexion1.commit()
    conexion1.close()
    return data




def addRow(datos):
    # < div class ="table" >
    a = '<div class="row">'
    for i in datos:
        a = a+ '<div class="cell">'
        a = a + str(i)
        a = a + '</div>'


    a = a+"</div>"
    return a
# < / div >




app = Flask(__name__)
@app.route('/recomendacion')
def my_route():
    idusuario = request.args.get('user', default=1, type=int)
    nombre = request.args.get('neighbours', default='3', type=int)


    data = getDataFromOdoo(5)
    content = ""
    for i in data:
        content = content + (addRow(i))
    # content = addRow([1,2,3,4])

    users = (getUser())
    movies = (getMovie())
    puntuacion = (getPuntuacion())
    res = getRecomendations(idusuario,nombre)
    print(res)
    content = []
    x = 0
    for i in res:

        row = ""
        for j in i:
            temp = []

            for k in users:
                if (j in k):
                    name = k[1]
                    temp.append(name)
                    break
            maxmovie = -10000
            idmovie = 1
            for k in puntuacion:
                if (j in k):
                    if k[2]> maxmovie:
                        idmovie = k[1]

            for k in movies:
                if (idmovie in k):
                    moviename = k[1]
                    temp.append(moviename)
                    break
            # print(j,i[j])
            temp.append(round(i[j],4))
            row = row + addRow(temp)
            print(temp)
        content.append(row)
        val = j
        # print(val)
    return render_template('indextest.html',euclidiana=content[0],manhatan=content[1],pearson=content[2],cosine=content[3])

if __name__ == '__main__':
    app.run()