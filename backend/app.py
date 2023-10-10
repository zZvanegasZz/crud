from flask import Flask
from flask_cors import CORS
from flask import jsonify,request
import pymysql

app=Flask(__name__)

CORS(app)

def conectar( vhost, vuser,vpass,vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset = 'utf8mb4')
    return conn

@app.route("/")

def consulta_general():
    try:
        conn=conectar ('localhost','root','1234','gestor_contrasena')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM  Baul """)
        datos=cur.fetchall()
        data=[]
        for row in datos:
            dato= {'id_Baul':row[0], 'plataforma':row[1], 'usuario':row[2],'clave':row[3]}
            data.append(dato)
        cur.close()
        conn.close()
        return jsonify({'Baul': data, 'mensaje':'Baul decontraseñas'})
    except Exception as ex:
        return jsonify({'mensaje':'Error'})
    
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    try:
        conn=conectar ('localhost','root','1234','gestor_contrasena')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM  Baul where id_baul='{0}'""", format (codigo))
        datos=cur.fetchone()
        cur.close()
        conn.close()
    if datos is not None:
        dato = {'id_baul': datos[0], 'Plataforma': datos[1], 'usuario': datos[2], 'clave': datos[3]}
    return jsonify({"baul": dato, 'mensaje': 'Registro encontrado'})
else:
    return jsonify({'mensaje': 'Registro no encontrado'})
except Exception as ex:
    return jsonify({'mensaje': 'Error'})

@app.route("/registro/", methods=['POST'])
def registro():
    try:
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()

        x = cur.execute("""INSERT INTO baul (plataforma, usuario, clave) VALUES \
                        ('{0}','{1}', '{2}')""".format(request.json['plataforma'], \
                        request.json['usuario'], request.json['clave']))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'mensaje': 'Registro agregado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    try:
        conn = conectar('localhost', 'root', '1234', 'gestor_contrasena')
        cur = conn.cursor()

        x = cur.execute("""DELETE FROM baul WHERE id_baul = {0}""".format(codigo))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'mensaje': 'Eliminado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@app.route("/actualizar/<codigo>", methods=['PUT'])
