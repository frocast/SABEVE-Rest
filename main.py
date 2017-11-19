#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# [START app]

# export SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:p3nt35t1ng@127.0.0.1/aula_virtual
""" Comentario"""
import logging
import datetime
import socket
import os
import jwt

from flask import Flask, render_template, request, redirect, session, url_for, jsonify, make_response
#from flask_talisman import Talisman
# from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import jinja2

from functools import wraps

#from dbconnect import connection, run_query           

app = Flask(__name__)
app.secret_key='Clave_secreta'
# csrf = SeaSurf(app)
#Talisman(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
print template_dir
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
    autoescape=False
)

db = SQLAlchemy(app)

class Usuarios(db.Model):
    Nombre = db.Column(db.String(30))
    Apellido = db.Column(db.String(30))
    email = db.Column(db.String(30), primary_key=True)
    knd = db.Column(db.String(20))
    fecha_na = db.Column(db.String(15))
    institucion = db.Column(db.String(200))
    genero = db.Column(db.String(10))
    pasw = db.Column(db.String(20)) 
    id_grupo = db.Column(db.Integer)      

    def __init__(self, nombre, apellido, email, knd, fecha_na, institucion, genero, pasw, id_grupo):
        self.Nombre = nombre
        self.Apellido = apellido   
        self.email = email   
        self.knd = knd   
        self.fecha_na = fecha_na
        self.institucion = institucion   
        self.genero = genero  
        self.pasw = pasw
        self.id_grupo = id_grupo

class Intereses(db.Model):
    id_intereses = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))    
    pais = db.Column(db.String(50))        
    habilidades = db.Column(db.String(1000))        
    nota = db.Column(db.String(1000))        
    institucion = db.Column(db.String(100))        

    def __init__(self, email, pais, habilidades, nota, institucion):                        
        self.email = email                                            
        self.pais = pais
        self.habihabilidades =habilidades
        self.nota = nota
        self.institucion = institucion

class Biblioteca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    autor = db.Column(db.String(50))
    ISSNISBN = db.Column(db.String(20))    
    tipo = db.Column(db.String(10))
    editorial = db.Column(db.String(100))
    fecha = db.Column(db.Integer)
    idioma = db.Column(db.String(20))
    resena = db.Column(db.String(5000))
    link = db.Column(db.String(500))
    portada = db.Column(db.String(5000))       

    def __init__(self, titulo="", autor="", ISSNISBN="", tipo="", editorial="", fecha=0, idioma="", resena="", link="", portada=""):
        self.titulo = titulo
        self.autor = autor   
        self.ISSNISBN = ISSNISBN   
        self.tipo = tipo
        self.editorial = editorial
        self.fecha = fecha
        self.idioma = idioma
        self.resena = resena  
        self.link = link    
        self.portada = portada

class Podcasts(db.Model):
    id_pod = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(5000))
    email = db.Column(db.String(50))    
    fecha_pu = db.Column(db.DateTime, default=db.func.current_timestamp())
    url = db.Column(db.String(500))
    portada = db.Column(db.String(500))
    tipo = db.Column(db.String(10))

    def __init__(self, titulo, descripcion, email, url, portada, tipo):
        self.titulo = titulo
        self.descripcion = descripcion   
        self.email = email           
        self.url = url
        self.portada = portada
        self.tipo = tipo        

class Foro(db.Model):
    id_tema = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String(50))
    titulo = db.Column(db.String(200))
    mensaje = db.Column(db.String(500))
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())  

    def __init__(self, autor, titulo, mensaje):                        
        self.autor = autor
        self.titulo = titulo 
        self.mensaje = mensaje   

class Mensajes(db.Model):
    id_mensaje = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    id_tema= db.Column(db.Integer)       
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())  
    mensaje = db.Column(db.String(500))

    def __init__(self, email, id_tema, mensaje):                        
        self.email = email
        self.id_tema = id_tema 
        self.mensaje = mensaje               

class Moocs(db.Model):
    id_mooc = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(500))
    titulo = db.Column(db.String(100))
    email = db.Column(db.String(50))    

    def __init__(self, descripcion, titulo, email):                
        self.descripcion = descripcion
        self.titulo = titulo 
        self.email = email

class Contenido_mooc(db.Model):
    id_contenido = db.Column(db.Integer, primary_key=True)
    id_mooc = db.Column(db.Integer)
    titulo = db.Column(db.String(200))
    url = db.Column(db.String(500))
    email = db.Column(db.String(50))    

    def __init__(self, id_mooc, titulo, url, email):                        
        self.id_mooc = id_mooc
        self.titulo = titulo 
        self.url = url
        self.email = email

class Evaluaciones(db.Model):
    id_evaluaciones = db.Column(db.Integer, primary_key=True)
    id_mooc = db.Column(db.Integer)
    pregunta = db.Column(db.String(200))
    respuesta_1 = db.Column(db.String(500))
    respuesta_2 = db.Column(db.String(500))    
    respuesta_3 = db.Column(db.String(500))    

    def __init__(self, id_mooc, pregunta, respuesta_1, respuesta_2, respuesta_3):                        
        self.id_mooc = id_mooc
        self.pregunta = pregunta 
        self.respuesta_1 =respuesta_1
        self.respuesta_2 = respuesta_2        
        self.respuesta_3 = respuesta_3

class Resultados(db.Model):
    id_resultados = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    id_mooc = db.Column(db.Integer)
    calificacion = db.Column(db.String(500))    

    def __init__(self, email, id_mooc, calificacion):                        
        self.email = email
        self.id_mooc = id_mooc
        self.calificacion = calificacion   

class Sitios(db.Model):
    id_sitios = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    titulo = db.Column(db.String(100))
    link = db.Column(db.String(500))    

    def __init__(self, email, titulo, link):                        
        self.email = email
        self.titulo = titulo
        self.link = link
              
class Grupos(db.Model):
    id_grupo = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50)) 
    nombre = db.Column(db.String(100))        

    def __init__(self, email, nombre):                        
        self.email = email                   
        self.nombre = nombre                   

class Temas(db.Model):
    
    id_tema = db.Column(db.Integer, primary_key=True)
    id_grupo = db.Column(db.Integer) 
    tema = db.Column(db.String(100))  
    email = db.Column(db.String(50))        

    def __init__(self, id_grupo, tema, email):                        
        self.id_grupo = id_grupo                   
        self.tema = tema
        self.email = email

class Contenidos_tema(db.Model):
    id_contenido = db.Column(db.Integer, primary_key=True)
    id_tema = db.Column(db.Integer)    
    subtema = db.Column(db.String(100))        
    pdf_link = db.Column(db.String(1000))        
    habilitar = db.Column(db.String(10))        

    def __init__(self, id_tema, subtema, pdf_link, habilitar):                        
        self.id_tema = id_tema                                             
        self.subtema = subtema
        self.pdf_link = pdf_link
        self.habilitar = habilitar
        
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensaje': 'token perdido'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Usuarios.query.filter_by(email=data['email']).first()
        except:
            return jsonify({'mensaje': 'token invalido'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/api/v1.0', methods=['GET'])
@token_required
def inicio_api(current_user):
    return  jsonify({"":""})

@app.route('/api/v1.0/login/')
def login_api():
    auth = request.get_json()
    
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response('sin verificar', 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})
    
    usuario = Usuarios.query.filter_by(email=auth.get('email')).first()
    if not usuario:
        return make_response('sin verificar', 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})
        
    if usuario.pasw == auth.get('password'):
        token = jwt.encode({'email':usuario.email, 'nombre':usuario.Nombre ,'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})        

    return make_response('sin verificar', 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})

@app.route('/api/v1.0/usuarios/')
@token_required
def usuarios_api(current_user):
        
    usuarios = Usuarios.query.all()
    return jsonify({"usuarios": [{ "email": usuario.email, 
                                   "nombre": usuario.Nombre, 
                                   "apellido": usuario.Apellido, 
                                   "tipo": usuario.knd,
                                   "fecha_na": usuario.fecha_na,
                                   "insititucion": usuario.institucion,
                                   "genero": usuario.genero,
                                   "password": usuario.pasw,                                   
                                   "id_grupo": usuario.id_grupo
                                   } for usuario in usuarios]})

@app.route('/api/v1.0/usuarios/<email>')
@token_required
def usuarios_by_id_api(current_user, email):
    usuarios = Usuarios.query.filter_by(email=email).all()
    return jsonify({"usuario": [{ "email": usuario.email, 
                                   "nombre": usuario.Nombre, 
                                   "apellido": usuario.Apellido, 
                                   "tipo": usuario.knd,
                                   "fecha_na": usuario.fecha_na,
                                   "insititucion": usuario.institucion,
                                   "genero": usuario.genero,
                                   "password": usuario.pasw,                                   
                                   "id_grupo": usuario.id_grupo
                                   } for usuario in usuarios]})

@app.route('/api/v1.0/usuarios/', methods=['POST'])
@token_required
def nuevo_usuario_api(current_user):
    datos = request.get_json()
    email = datos.get('email')
    nombre = datos.get('nombre')
    apellido = datos.get('apellido')
    tipo = datos.get('tipo')
    fecha_na = datos.get('fecha_na')
    institucion = datos.get('institucion')
    genero = datos.get('genero')
    password = datos.get('password')
    id_grupo = datos.get('id_grupo')

    usuario = Usuarios(nombre,apellido,email,tipo,fecha_na,institucion,genero,password,id_grupo)        
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'email':usuario.email}), 201  

@app.route('/api/v1.0/usuarios/<email>', methods=['PUT'])
@token_required
def actualizar_usuarios(current_user, email):
    usuario = Usuarios.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({'mensaje':'no se encontro al usuario'})
    datos_actualizados = request.get_json()
    
    usuario.institucion = datos_actualizados['institucion']
    usuario.pasw = datos_actualizados['password']    
    usuario.pasw = datos_actualizados['password']        
    db.session.commit()

    return jsonify({'mensaje': 'Datos de Usuario actualizados'})

@app.route('/api/v1.0/usuarios/<email>', methods=['DELETE'])
@token_required
def eliminar_usuarios(current_user, email):
    usuario = Usuarios.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({'mensaje':'no se encontro al usuario'})
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensaje':'Usuario Eliminado'})

@app.route('/api/v1.0/biblioteca/')
def biblioteca_api():
        
    libros = Biblioteca.query.all()
    return jsonify({"Libros": [{ "id": libro.id, 
                                   "titulo": libro.titulo, 
                                   "autor": libro.autor, 
                                   "ISSNISBN": libro.ISSNISBN,
                                   "tipo": libro.tipo,
                                   "editorial": libro.editorial,
                                   "fecha": libro.fecha,
                                   "idioma": libro.idioma,                                   
                                   "resena": libro.resena,
                                   "link": libro.link,
                                   "portada": libro.portada                                   
                                   } for libro in libros]})

@app.route('/api/v1.0/biblioteca/<clave>/<idioma>/<fecha_inferior>/<fecha_superior>/')
def biblioteca_by_id_api(clave,idioma,fecha_inferior,fecha_superior):
    libros = Biblioteca.query.filter((Biblioteca.titulo==clave) | (Biblioteca.autor==clave) | (Biblioteca.ISSNISBN==clave) | (Biblioteca.idioma==idioma) | (Biblioteca.fecha.between(int(fecha_inferior), int(fecha_superior)))).order_by(Biblioteca.titulo.desc()).all()
    return jsonify({"Libros": [{ "id": libro.id, 
                                   "titulo": libro.titulo, 
                                   "autor": libro.autor, 
                                   "ISSNISBN": libro.ISSNISBN,
                                   "tipo": libro.tipo,
                                   "editorial": libro.editorial,
                                   "fecha": libro.fecha,
                                   "idioma": libro.idioma,                                   
                                   "resena": libro.resena,
                                   "link": libro.link,
                                   "portada": libro.portada                                   
                                   } for libro in libros]})                                 

@app.route('/api/v1.0/biblioteca/', methods=['POST'])
def nuevo_libro_api():
    datos = request.get_json()

    titulo = datos.get('titulo') # o titulo = dato['titulo']
    autor = datos.get('autor')
    ISSNIBSN = datos.get('ISSNISBN')
    tipo = datos.get('tipo')
    editorial = datos.get('editorial')
    fecha = datos.get('fecha')
    idioma = datos.get('idioma')
    resena = datos.get('resena')
    link = datos.get('link')
    portada = datos.get('portada')    

    libro = Biblioteca(titulo,autor,ISSNIBSN,tipo,editorial,fecha,idioma,resena,link,portada)        
    db.session.add(libro)
    db.session.commit()
    return jsonify({'libro':libro.titulo}), 201  

@app.errorhandler(404)
def page_not_found(e):
    response = make_response(jsonify({'mensaje':'{}'.format(e)}), 404)
    response.headers['Content-type'] = 'application/json'    
    return response

@app.errorhandler(400)
def bad_request(e):
    response = make_response(jsonify({'mensaje':'{}'.format(e)}), 400)
    response.headers['Content-type'] = 'application/json'    
    return response

@app.errorhandler(500)
def server_error(e):
    response = make_response(jsonify({'mensaje':'{}'.format(e)}), 500)
    response.headers['Content-type'] = 'application/json'    
    return response

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)
# [END app]

# curl -XPOST -H "Content-type: application/json" -d '{"nombre": "timbona", "apellido": "sin dato", "email":"urodoz@gmail.com", "tipo": "Alumno", "fecha_na":"01/01/1990", "institucion":"IPN", "genero":"perro", "password":"abc", "id_grupo":"0"}' 'http://localhost:8080/api/v1.0/usuarios/'