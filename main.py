from flask import Flask, request, render_template
import psycopg2


print("")
def getDataFromDB(limit = 0):
    conexion1 = psycopg2.connect(database="postgres",
                                 user="odoo",
                                 password="odoo",
                                 host="localhost",
                                 port="5432")
    cursor1 = conexion1.cursor()
    if limit == 0:
        sql = "SELECT * FROM puntuacion;"
    else:
        sql = f"SELECT * FROM puntuacion LIMIT{limit};"

    cursor1.execute(sql)
    row = 0
    data = []
    while row is not None:
        print(row)
        row = cursor1.fetchone()
        data.append(row)

    conexion1.commit()
    conexion1.close()
    return data
def getDataFromOdoo(limit = 0):
    conexion1 = psycopg2.connect(database="odoo",
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
    print(data)
    # while row is not None:
    #     print(row)
    #     row = cursor1.fetchone()
    #     print(row)
    #     row = list(row)
    #     # row.append("<br>")
    #     data.append(row)

    conexion1.commit()
    conexion1.close()
    return data

def addRow(datos):
    # < div class ="table" >
    a = '<div class="row">'
    for i in datos:
        a = a+ '<div class="cell">'
        a = a + str(i)
        print(a)
        a = a + '</div>'


    a = a+"</div>"
    return a

# < / div >

app = Flask(__name__)
@app.route('/recomendacion')
def my_route():
    idusuario = request.args.get('user', default=1, type=int)
    nombre = request.args.get('movie', default='*', type=str)
    puntuacion = request.args.get('rating', default='*', type=float)

    data = getDataFromOdoo(5)
    content = ""
    for i in data:
        content = content + (addRow(i))
    # content = addRow([1,2,3,4])

    return render_template('indextest.html',euclidiana=content,manhatan=content,pearson=content,cosine=content)

if __name__ == '__main__':
    app.run()