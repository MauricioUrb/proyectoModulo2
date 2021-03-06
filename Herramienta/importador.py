#!/usr/bin/env python3

import os
import subprocess
import socket
import threading
import time
import re
import sys
    
def importSiteConf():
    print("Esperando importacion de archivo", end = '', flush=True)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 1331))
    s.listen(1)
    conn, addr = s.accept()

    nombre = conn.recv(1024)
    print("\nNombre del sitio: " + nombre.decode("utf-8"))
    conn.sendall(bytes('Nombre recibido', 'UTF-8'))
    
    contenido = conn.recv(1000000)
    f = open(nombre.decode("utf-8"), 'w+b')
    f.write(contenido)
    f.close()
    conn.sendall(bytes('Archivo recibido', 'UTF-8'))

    responder = conn.recv(1024)
    print("Archivo creado.")
    conn.sendall(bytes('Archivo creado sitio1', 'UTF-8'))

    nombre2 = conn.recv(1024)
    print("Nombre del sitio: " + nombre2.decode("utf-8"))
    conn.sendall(bytes('Nombre recibido', 'UTF-8'))
    
    contenido = conn.recv(1000000)
    f = open(nombre2.decode("utf-8"), 'w+b')
    f.write(contenido)
    f.close()
    conn.sendall(bytes('Archivo recibido', 'UTF-8'))

    responder = conn.recv(1024)
    print("Archivo creado.")
    conn.sendall(bytes('Archivo creado sitio2', 'UTF-8'))
    conn.close()

    return nombre.decode("utf-8"),nombre2.decode("utf-8")

def installPre():
    print("Update")
    info = subprocess.Popen(['apt-get','update', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo hacer update")
    else:
        print("Se logro hacer update")
    print("Upgrade")
    info = subprocess.Popen(['apt-get','upgrade', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo hacer upgrade")
    else:
        print("Se logro hacer upgrade")
    print("Instalando/verificando apache")
    info = subprocess.Popen(['apt-get','install', 'apache2', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo instalar apache")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Apache instalado")
    print("Instalando/verificando php")
    info = subprocess.Popen(['apt-get', 'install', 'php7.3', 'libapache2-mod-php7.3', 'php7.3-cli', 'php7.3-pgsql', 'php7.3-intl', 
        'php7.3-mysql', 'php7.3-curl', 'php7.3-gd', 'php7.3-soap', 'php7.3-xml', 'php7.3-zip','php7.3-ldap', 
        '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo instalar php")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Php instalado")

    print("Configurando php")
    cmd = "sed -i -e 's/;extension=ldap/extension=ldap/' \
           -i -e 's/;extension=openssl/extension=openssl/' \
           -i -e 's/;extension=pgsql/extension=pgsql/' -i -e 's/upload_max_filesize = 2M/upload_max_filesize = 2G/'\
           -i -e 's/post_max_size = 8M/post_max_size = 8G/' /etc/php/7.3/apache2/php.ini"
    info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo configurar php")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Php configurado")

    print("Instalando git")
    info = subprocess.Popen(['apt-get','install','git','-y']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se puede instalar git")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Git instalado")

    print("Instalando/verificando drush")
    info = subprocess.Popen(['wget','https://github.com/drush-ops/drush/releases/download/8.3.2/drush.phar', '-q','--show-progress']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo descaragr drush")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Drush descargado")
    info = subprocess.Popen(['chmod','+x','drush.phar'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo cambiar permisos a drush")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Permisos asignados a drush")
    info = subprocess.Popen(['mv','drush.phar','/usr/bin/drush'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo agragar drush al path")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Drush agregado al path")
    print("Instalando cliente de postgresql")
    info = subprocess.Popen(['apt-get','install','postgresql-client-11','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se puede instalar cliente de postgresql")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Cliente de postgresql instalado")

    print("Instalando OpenSSL")
    info = subprocess.Popen(['apt-get','install','openssl','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se puede instalar OpenSSL")
        print("Abortando operacion")
        sys.exit()
    else:
        print("OpenSSL instalado")
    print("Descargando Drupal")
    info = subprocess.Popen(['drush', 'dl', 'drupal-8.8.3', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se descarger drupal 8.8.3")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Drupal descargado")
    """"
    print("Instalando composer")
    info = subprocess.Popen(['apt-get','install','composer','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se puede instalar composer")
        print("Abortando operacion")
        sys.exit()
    else:
        print("composer instalado")
    """

def installDrupal(nombreSitio):
    s1 = ""
    f = open(nombreSitio, "r")
    for linea in f:
        if linea.lower().find("documentroot") != -1:
            pat = re.compile(".*#.*documentroot.*")
            result = pat.match(linea.lower())
            if(result == None):
                l1 = linea.split()
                for j in l1[1:]:
                    s1+=j+' '
                s = s1.split('#')
                cad = s[0].rstrip().lstrip()
                print(cad)
                break
    f.close()
    print("Moviendo Drupal al sitio")
    info = subprocess.Popen(['cp', '-r', 'drupal-8.8.3/', cad],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo mover drupal")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Drupal ha sido movido")
    """
    user = input("Ingrese el usuario de la base de datos.\n")
    ip = input("Direccion de la base de datos.\n")
    port = input("Puerto de la base de datos.\n")
    bd = input("Base de datos a la conectarse.\n")
    password = input("Ingrese la coontraseña de acceso.\n")
   """
    user='drupal'
    ip='192.168.216.148'
    port='5432'
    bd = user
    password = 'hola123.,'
    print("Relizando instalacion de drupal")
    url = "--db-url=pgsql://"+ user +":"+password+"@"+ip+":"+port+"/"+bd
    info = subprocess.Popen(['drush', 'si','standard',url, '-r', cad, '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    l = info.stdout.read().decode()
    l1 = l.find("Installation complete.")
    if l1 == -1:
        print("Problemas con la instalaciion")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Drupal instalado")
        print("[!] " + l[l1:l1+70])
    s1 = nombreSitio.split('/')
    print("Activando modulos y sitio.")
    info = subprocess.Popen(['a2ensite', s1[-1]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo activar la pagina")
        print("Abortando operacion")
        sys.exit()
    info = subprocess.Popen(['a2enmod', 'rewrite'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Error de activacion del modulo rewrite")
        sys.exit()
    info = subprocess.Popen(['a2enmod', 'ssl'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Error de activacion del modulo ssl")
        sys.exit()
    info = subprocess.Popen(['a2enmod', 'headers'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Error de activacion del modulo headers")
        sys.exit()
    print("Reiniciando pagina.")
    info = subprocess.Popen(['/etc/init.d/apache2', 'restart']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Error Reiniciando apache")
        sys.exit()
    f = open(nombreSitio, "r")
    s1 = ""
    for linea in f:
        if linea.lower().find("servername") != -1:
            pat = re.compile(".*#.*servername.*")
            result = pat.match(linea.lower())
            if(result == None):
                l1 = linea.split()
                for j in l1[1:]:
                    s1+=j+' '
                s = s1.split('#')
                cad = s[0].rstrip().lstrip()
                break
    print("Actualizando /etc/hosts.")
    cmd = "echo '127.0.0.1 "+cad+"' >> /etc/hosts"
    info = subprocess.Popen(cmd,shell=True).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Error al actualizar hosts")
        sys.exit()
    f.close()


def deleteDL():
    print("Eliminando descargable")
    info = subprocess.Popen(['rm', '-r', 'drupal-8.8.3/']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Problemas al quitar el descargable")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Descargable eliminado")

installPre()
nombreSitio1, nombreSitio2 = importSiteConf()
installDrupal(nombreSitio1)
#installDrupal(nombreSitio2)
deleteDL()