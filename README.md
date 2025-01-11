# Descripción
El presente código utiliza el Framework de FastApi en conjunto de AlchemySQL para generar de manera automática una base de datos en base a los modelos de tablas creadas para la API. Además, FastApi genera de manera automática el FrontEnd de la Api en base a los end points de cada controller realizado. Además, se utilizó AlchemySQL para generar una base de datos SQL lite.

# Objetivo de la API
La razón tras la creación de esta API es con el fin de estandarizar de forma numérica la valoración de las habilidades blandas y duras dentro de una empresa. Existe don consideraciones importantes, las habilidades que cada departamento considera de gran importancia serán diferentes y tendrán un peso distinto. En este caso las habilidades priorizadas por departamentos son valoradas en base a un número decimal de 0 a 1, tal que representa el procentaje del valor total del peso de la habilidadad del empleado. Es decir, si la habilidad del empleado tiene un peso de 90 y dicha habilidad tiene un prioridad de 0.1, siendo el resultado final un peso de 9, significa que dicho resultado es el peso de esa habilidad en la empresa en base al departamento del empleado. Por otro lado, tambien se toma en cuenta que la importancia de las habilidades de un empleado pueden variar en base a su dominio y experiencio, por dicha razón, el peso final se múltiplica por el dominio (de 1 a 10) para obtener un peso real de una habilidad. 


## Arquitectura

El código se divide en application, core y entities.
- <b>core:</b> contiene la lógica tras el funcionamiento del código incluyendo los datos de la bases de datos, la manipulación de la base de datos y los servicios.
- <b>application:</b> contiene los controladores necesarios que aplican los routers de FastApi.
- <b>entities:</b> contiene todos los modelos necesarios que se utilizará en la aplicación.

## Tablas
Esta API administra 5 diferentes tablas presentes en la base de datos y 6 usadas para mostrar la respuesta de la API ante las peticiones del usuario o para manejar las entradas (ingreso de información) por parte del usuario. <br>
Las tablas almacenadas en la base de datos son las siguientes:
- <b>Employee:</b> Almacena la información personal y profesional del empleado.
- <b>Department:</b> Enlista los departamentos de la empresa, incluye una opción para el empleado cuyo departamento no ha sido asignado.
- <b>Position:</b> Enlista las posiciones de la empresa, incluye una opción para el empleado cuya posición no ha sido asignada.
- <b>Hard Skills:</b> Enlista las habilidades duras que la empresa necesita. Incluye una ponderación que representa su importancia dentro de la empresa.
- <b>Soft Skills:</b> Enlista las habilidades blandas que la empresa necesita. Incluye una ponderación que representa su importancia dentro de la empresa.
- <b>Employee Hard Skills:</b> Enlista las habilidades duras que posee un empleado, junto con su dominio de aquella habilidad.
- <b>Employee Soft Skills:</b> Enlista las habilidades duras que posee un empleado, junto con su dominio de aquella habilidad.

## Implementación
Los requisitos para la implementación son los siguientes:
1. Tener instalado python 3.9 o superior, y declararlo en las variables del sistema
2. Clonar o descargar el proyecto y ejecutar la siguiente línea de código en la línea de comandos:


```
    pip install pipreqs
    pipreqs /path/to/project
    ./Scripts/activate
```
3. Para ejecutar al API se utiliza el siguiente comando (asegúrese de que el terminal se encuentre en la posicion correcta)
```
    fastapi dev src/main.py
```
4. Se puede acceder a la página por este link: http://127.0.0.1:8000/docs 