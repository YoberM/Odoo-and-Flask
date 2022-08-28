import psycopg2
# from knn import *

import csv


def getPuntuacion(limit = 0):
    conexion1 = psycopg2.connect(database="odoo2",
                                 user="odoo",
                                 password="odoo",
                                 host="localhost",
                                 port="5432")
    cursor1 = conexion1.cursor()
    sql = ""

    if limit == 0:
        sql = f"""
        select res_partner.id,product_product.product_tmpl_id, sale_report.product_uom_qty
        from res_partner 
        INNER JOIN sale_report ON res_partner.id = sale_report.partner_id 
        INNER JOIN product_product ON product_id = product_product.id 
        INNER JOIN product_template ON product_product.product_tmpl_id = product_template.id;
        """
    else:
        sql = f"""
        select res_partner.id,product_product.product_tmpl_id, sale_report.product_uom_qty
        from res_partner 
        INNER JOIN sale_report ON res_partner.id = sale_report.partner_id 
        INNER JOIN product_product ON product_id = product_product.id 
        INNER JOIN product_template ON product_product.product_tmpl_id = product_template.id
        LIMIT {limit};
        """
    cursor1.execute(sql)
    data = []
    row = cursor1.fetchall()
    for i in row:
        temp = list(i)
        temp[0] = int(temp[0])
        temp[1] = int(temp[1])
        temp[2] = float(temp[2])
        data.append(temp)
    conexion1.commit()
    conexion1.close()
    return data



def getUser(limit = 0):
    conexion1 = psycopg2.connect(database="odoo2",
                                 user="odoo",
                                 password="odoo",
                                 host="localhost",
                                 port="5432")
    cursor1 = conexion1.cursor()
    sql = ""

    if limit == 0:
        sql = f"""
        select res_partner.id,res_partner.name from res_partner 
        INNER JOIN sale_report ON res_partner.id = sale_report.partner_id 
        INNER JOIN product_product ON product_id = product_product.id 
        INNER JOIN product_template ON product_product.product_tmpl_id = product_template.id;
        """
    else:
        sql = f"""
        select res_partner.id,res_partner.name from res_partner 
        INNER JOIN sale_report ON res_partner.id = sale_report.partner_id 
        INNER JOIN product_product ON product_id = product_product.id 
        INNER JOIN product_template ON product_product.product_tmpl_id = product_template.id
        LIMIT {limit};
        """
    cursor1.execute(sql)
    data = []
    row = cursor1.fetchall()
    for i in row:
        temp = list(i)
        temp[0] = int(temp[0])
        temp[1] = str(temp[1])
        data.append(temp)
    conexion1.commit()
    conexion1.close()
    return data

def getMovie(limit = 0):
    conexion1 = psycopg2.connect(database="odoo2",
                                 user="odoo",
                                 password="odoo",
                                 host="localhost",
                                 port="5432")
    cursor1 = conexion1.cursor()
    sql = ""

    if limit == 0:
        sql = f"""
        select product_product.product_tmpl_id, product_template.name from res_partner 
        INNER JOIN sale_report ON res_partner.id = sale_report.partner_id 
        INNER JOIN product_product ON product_id = product_product.id 
        INNER JOIN product_template ON product_product.product_tmpl_id = product_template.id;
        """
    else:
        sql = f"""
        select product_product.product_tmpl_id, product_template.name from res_partner 
        INNER JOIN sale_report ON res_partner.id = sale_report.partner_id 
        INNER JOIN product_product ON product_id = product_product.id 
        INNER JOIN product_template ON product_product.product_tmpl_id = product_template.id
        LIMIT {limit};
        """
    cursor1.execute(sql)
    data = []
    row = cursor1.fetchall()
    for i in row:
        temp = list(i)
        temp[0] = int(temp[0])
        temp[1] = str(temp[1])
        data.append(temp)
    conexion1.commit()
    conexion1.close()
    return data


def WriteData():
    # open the file in the write mode
    f = open('tempRating.csv', 'w')
    f2 = open('tempUser.csv', 'w')
    f3 = open('tempMovie.csv', 'w')

    writer = csv.writer(f)
    writer.writerow(["userid","movieid","puntuacion"])
    for i in getPuntuacion():
        writer.writerow(i)

    writer = csv.writer(f2)
    writer.writerow(["userid", "username"])
    for i in getUser():
        writer.writerow(i)

    writer = csv.writer(f3)

    writer.writerow(["movieid", "moviename"])

    for i in getMovie():
        writer.writerow(i)

    # close the file
    f.close()
    f2.close()
    f3.close()

    f4 = open('tempNewUser.csv', 'w')
    writer = csv.writer(f4)
    writer.writerow(["userid","movieid","puntuacion"])
    writer.writerow(["1000","2","35"])

    f4.close()


# def test():
#     print("test")
#     print(getUser(5))
#     print(getMovie(5))
#     print(getPuntuacion(5))
#
# test()