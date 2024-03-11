# Odoo ExamenSXE

En este readme explico como hacer .

## Docker Compose
### Odoo
```
version: '3.1'
services:
  web:
    image: odoo:16.0
    depends_on:
      - mydb
    volumes:
      - ./extra-addons:/mnt/extra-addons
    ports:
      - "8069:8069"
    environment:
      - HOST=mydb
      - USER=odoo
      - PASSWORD=myodoo
```
### PostgresSQL
```
  mydb:
    image: postgres:15
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=myodoo
      - POSTGRES_USER=odoo
    ports:
      - "5433:5432"
```

## Conectarse a la Base de Datos desde PyCharm
Para poder conectarse con la base de datos desde el IDE, debemos darle al + > Data Source > PostgresSQL.
Seleccionaremos como puerto 5433, como usuario: odoo y como contraseña: myodoo que son las credenciales que pusimos en el código.



Tal y como se aprecia en la imagen siguiente la conexión se ha esteblecido con éxito:



## Lanzamiento del docker compose
Para esto empezaremos ejecutando en la consola del IDE el comando `docker-compose up -d` para así activar los servicios del archivo `docker-compose.yml`.

Tras este proceso ya podríamos ir al nuestro navegador, entrar en `localhost:8069` donde desde Odoo podremos crear nuestra base de datos.
Para crearla simplemente pondremos los datos que pide y una vez tengamos todo puesto pulsaremos el botón `create database`.

A continuación nos aparecerá una pestaña para iniciar sesión tal y como se puede ver en la imagen siguiente:



Las credenciales serían las que hemos seleccionado en el proceso previo



## Creación del Modulo
Para poder instalar el módulo crearemos en nuestro proyecto un carpeta llamada `entra-addons` si no se ha creado sola. 

Posteriormente ejecutaremos los comandos siguientes en la terminal del IDE:

* `docker exec -u root -it "Nombre de tu proyecto (sin comillas)"-web-1 /bin/bash` para acceder al contenedor de Odoo.
* `cd /mnt/extra-addons` para acceder a la carpeta extra-addons.
* `odoo scaffold openacademy` para crear la estructura y archivos del módulo.
* `chmod -R 777 openacademy` para cederle todos los permisos a la carpeta del módulo.
* `exit` 
* `docker restart modulo_odoo-web-1` para reiniciarlo y que se apliquen los cambios realizados.

Tras reiniciarlo para que se actualicen los cambios que hicimos debería quedarnos una estructura de proyecto como la que se ve a continuación (ignorando la carpeta imgs):




## Configuración del Módulo y creación de la Tabla
El primer paso será instalar el módulo desde Odoo, para ello iremos en la web de odoo a el icono de la esquina, ajustes, bajamos abajo de todo y activamos el modo de desarrollador.

Posteriormente buscaremos OpenAcademy en el buscador de Odoo y lo instalaremos. Cuando lo tengamos podemos ir a los 3 putnos > Más Información para ver más datos o actualizar datos (esos datos se pueden modificar desde el archivo `manifest.py`).



Para crear una _Tabla_, nos dirigiremos a la carpeta `models` > `models.py` y agregamos el código siguiente:
```
# -*- coding: utf-8 -*-

from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Modelo de prueba"

    producto = fields.Char(string="Producto")
    viabilidad = fields.Float(string="Viabilidad")
```

Cuando acabemos de hacer los cambios reinciamos el contenedor y refrescamos la base de datos.
También en Odoo en el módulo de OpenAcademy le damos a los `3 puntos > Más Información > Actualizar` para que se apliquen todos los cambios.

A continuación vamos a la base de datos, seleccionamos el apartado `public > tables` bajamos y en la parte de abajo deberíamos encontrar la tabla `test_model`.



Ahora necesitamos poder introducir datos a nuestra tabla, para ello crearemos una carpeta llamada `data` y dentro un archivo llamado `datos.xml` y escribimos el código siguiente para que encaje con nuestro `models.py`.
```
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <data>
        <!-- Producto 1 -->
        <record id="producto_1" model="test_model">
            <field name="producto">Producto A</field>
            <field name="viabilidad">0.75</field>
        </record>
        
        <!-- Producto 2 -->
        <record id="producto_2" model="test_model">
            <field name="producto">Producto B</field>
            <field name="viabilidad">0.85</field>
        </record>
        
        <!-- Producto 3 -->
        <record id="producto_3" model="test_model">
            <field name="producto">Producto C</field>
            <field name="viabilidad">0.95</field>
        </record>
        
        <!-- Producto 4 -->
        <record id="producto_4" model="test_model">
            <field name="producto">Producto D</field>
            <field name="viabilidad">0.65</field>
        </record>
        
        <!-- Producto 5 -->
        <record id="producto_5" model="test_model">
            <field name="producto">Producto E</field>
            <field name="viabilidad">0.55</field>
        </record>
    </data>
</odoo>

```

Cuando ya tengamos el archivo xml lo añadimos al archivo `__manifest __.py` en la sección `data` poniendo el nombre de nuestro nuevo archivo.
```
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/datos.xml'
    ],
```

Tras eso, reiniciamos el contenedor y refrescamos la base de datos para aplicar los últimos cambios. Ahora ya podemos ver la tabla con los datos que introdujimos.

![2_1.png](imgs%2F2_1.png)

En último lugar tendremos que modificar dos archivos para que así se nos permita visualizar la tabla en desde nuestro modulo en Odoo.
Primero editaremos el archivo `views.xml` que está en el fichero `views`. 
```
<odoo>
  <data>
    <!-- explicit list view definition -->
    <record model="ir.ui.view" id="test_model_list_view">
      <field name="name">test.model.list</field>
      <field name="model">test_model</field>
      <field name="arch" type="xml">
        <tree>
          <field name="producto"/>
          <field name="viabilidad"/>
        </tree>
      </field>
    </record>

    <!-- actions opening views on models -->
    <record model="ir.actions.act_window" id="test_model_action_window">
      <field name="name">Test Model</field>
      <field name="res_model">test_model</field>
      <field name="view_mode">tree,form</field>
    </record>

    <!-- Top menu item -->
    <menuitem name="Test Model" id="test_model_menu_root"/>

    <!-- menu categories -->
    <menuitem name="Test Model" id="test_model_menu" parent="test_model_menu_root"/>

    <!-- actions -->
    <menuitem name="View Products" id="test_model_menu_view_products" parent="test_model_menu"
              action="test_model_action_window"/>
  </data>
</odoo>

```

A posteriori entraremos a nuestro archivo `__manifest __.py` a el apartado `data` y descomentaremos el apartado `security/ir.model.access.csv` para así poder ver la tabla.
```
 # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/datos.xml'
    ],
```

Por último nos situaremos en la carpeta `security` para editar el archivo `ir.model.access.csv`, cambiando el nombre y grupo al que pertence, quedaría así:
```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_openacademy_openacademy,openacademy.openacademy,model_test_model,base.group_user,1,1,1,1
```

Tras un reinicio del contenedor y refresco de la base de datos iremos a Odoo, actualizaremos como antes el módulo OpenAcademy y si todo ha salido correctamente debería aparecernos como 2ª opción al presionar el icono de la esquina izquierda de la web de Odoo.



Ahora desde el propio Odoo puedes añadir más datos a la tabla, presionando `Nuevo` y agregando, en mi caso nombre y nacionalidad de quien quieras añadir.



Tras agregar datos desde Odoo, esos mismos deberían aparecer en la tabla de nuestra base de datos si todo el proceso se ha hecho correctamente.



Hasta aquí ha llegado la guía.

By _Lucas Feliu_.