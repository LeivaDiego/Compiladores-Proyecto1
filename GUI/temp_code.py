## Proyecto 1 - Redes
### CHAT XMPP
#### Jos� Pablo Orellana - 21970

---

## Descripci�n del Proyecto

Este proyecto es un cliente de chat basado en el protocolo XMPP, desarrollado utilizando Python y la librer�a `slixmpp`. La aplicaci�n permite a los usuarios conectarse a un servidor XMPP, gestionar su lista de contactos, intercambiar mensajes y realizar varias operaciones de gesti�n de cuentas como la eliminaci�n de cuentas. La interfaz gr�fica (GUI) est� implementada utilizando `tkinter`, lo que ofrece una experiencia de usuario sencilla y directa.

---

## Funcionalidades Implementadas

### 1) **Inicio de Sesi�n**

#### Descripci�n:
El usuario puede iniciar sesi�n utilizando su `JID` (Jabber ID) y contrase�a. La autenticaci�n se realiza contra un servidor XMPP.

#### Detalles T�cnicos:
- **Entrada:** Usuario ingresa su `JID` y `contrase�a`.
- **Proceso:** Se crea una instancia de `XMPPClient`, que maneja la autenticaci�n y la conexi�n con el servidor XMPP.
- **Salida:** Si la autenticaci�n es exitosa, se habilitan las funciones de la aplicaci�n como la lista de contactos, la opci�n de agregar contactos y m�s.

#### C�mo se utiliza:
1. Al iniciar la aplicaci�n, se presenta una pantalla de inicio de sesi�n.
2. Ingrese su `JID` y `contrase�a`.
3. Haga clic en el bot�n "Iniciar Sesi�n".

---

### 2) **Cierre de Sesi�n**

#### Descripci�n:
El usuario puede cerrar la sesi�n actual, lo que desconecta la cuenta del servidor XMPP y lo redirige a la pantalla de inicio de sesi�n.

#### Detalles T�cnicos:
- **Proceso:** Al cerrar sesi�n, la conexi�n XMPP se desconecta limpiamente y la interfaz vuelve a la pantalla de inicio de sesi�n.
- **Salida:** El usuario es desconectado del servidor XMPP y se deshabilitan las opciones del men� que requieren autenticaci�n.

#### C�mo se utiliza:
1. Despu�s de iniciar sesi�n, en la barra de men�, haga clic en "Cerrar Sesi�n".
2. La aplicaci�n volver� a la pantalla de inicio de sesi�n.

---

### 3) **Mostrar Listado de Contactos**

#### Descripci�n:
Una vez autenticado, el usuario puede ver su lista de contactos, excluy�ndose a s� mismo.

#### Detalles T�cnicos:
- **Proceso:** Despu�s de la autenticaci�n, la lista de contactos se recupera del servidor y se muestra en la interfaz gr�fica.
- **Salida:** Se muestra una lista de contactos en la interfaz, que permite seleccionar y ver m�s detalles o iniciar una conversaci�n.

#### C�mo se utiliza:
1. Inicie sesi�n en la aplicaci�n.
2. La lista de contactos aparecer� autom�ticamente en la parte izquierda de la interfaz.

---

### 4) **Agregar Contacto**

#### Descripci�n:
El usuario puede agregar nuevos contactos a su lista.

#### Detalles T�cnicos:
- **Entrada:** `JID` del contacto que se desea agregar.
- **Proceso:** Se env�a una solicitud de suscripci�n al `JID` ingresado. Si la solicitud es aceptada, el contacto se agrega a la lista.
- **Salida:** El nuevo contacto se agrega y se muestra en la lista de contactos.

#### C�mo se utiliza:
1. Despu�s de iniciar sesi�n, en la barra de men�, seleccione "Agregar Contacto".
2. Ingrese el `JID` del contacto que desea agregar y haga clic en "Agregar".

---

### 5) **Mostrar Informaci�n de Contacto**

#### Descripci�n:
El usuario puede ver el estado de presencia de un contacto espec�fico.

#### Detalles T�cnicos:
- **Entrada:** `JID` del contacto del cual se desea ver la informaci�n.
- **Proceso:** Se consulta el estado de presencia del contacto y se muestra al usuario.
- **Salida:** Se muestra el estado de presencia del contacto en una ventana emergente.

#### C�mo se utiliza:
1. Despu�s de iniciar sesi�n, en la barra de men�, seleccione "Detalle Contacto".
2. Ingrese el `JID` del contacto y haga clic en "Consultar".

---

### 6) **Eliminar Mi Usuario**

#### Descripci�n:
El usuario puede eliminar su cuenta del servidor XMPP. Esta acci�n es irreversible y elimina la cuenta permanentemente.

#### Detalles T�cnicos:
- **Entrada:** Confirmaci�n del usuario para eliminar su cuenta.
- **Proceso:** Se env�a una solicitud de eliminaci�n de cuenta al servidor. Si la operaci�n es exitosa, la cuenta se elimina y el usuario es desconectado.
- **Salida:** La cuenta del usuario se elimina del servidor XMPP.

#### C�mo se utiliza:
1. Despu�s de iniciar sesi�n, en la barra de men�, seleccione "Eliminar Cuenta".
2. Confirme que desea eliminar su cuenta cuando se le solicite.

---

## Requisitos

- **Python 3.11.9**
- **Bibliotecas:** 
  - `slixmpp`
  - `tkinter` (incluido con Python)
- **Servidor XMPP:** Debe tener acceso a un servidor XMPP para utilizar la aplicaci�n.
- Si no tienes la versi�n de python y te crea conflicto. Crea un entorno virutal con esa versi�n para ejecutarlo.

---

## Instalaci�n

1. Clone este repositorio en su m�quina local.
2. Instale las dependencias necesarias utilizando `pip`:
   ```bash
   pip install slixmpp

## Para ejecutar el programa ir a consola. Ingresar a la direcci�n de la carpeta GUI y ejecutar el siguiente c�digo
   ```bash
   python principal.py

