# **Plan de Distribución del MVP: AiMaze \- La Mazmorra Generativa**

Este documento describe los pasos para la distribución del Producto Mínimo Viable (MVP) de AiMaze, permitiendo que otros usuarios puedan jugar a través de una interfaz web.

## **Fase 1: Servicio Web Backend (FastAPI)**

### **Objetivo:**

Crear una API RESTful para exponer la lógica del juego, permitiendo la comunicación con el frontend web.

### **Pasos:**

1. **Configuración de FastAPI y Uvicorn:**  
   * **Acción:** Crear la estructura básica de una aplicación FastAPI.  
   * Prompt para la IA integrada en el IDE:  
     "Crea el archivo src/aimaze/api/main.py. Este archivo debe:  
     * Inicializar una aplicación FastAPI.  
     * Incluir un endpoint /health que devuelva {'status': 'ok'}.  
     * Configurar CORS para permitir peticiones desde cualquier origen (por ahora, para desarrollo)."  
2. **Exposición de Acciones del Juego:**  
   * **Acción:** Adaptar las funciones del juego (initialize\_game\_state, process\_player\_action, display\_scenario) para ser llamadas a través de la API.  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/api/main.py. Añade los siguientes endpoints:  
     * POST /game/start: Que llame a game\_state.initialize\_game\_state() y devuelva el estado inicial del juego, incluyendo la descripción de la primera ubicación y opciones.  
     * POST /game/action: Que reciba un player\_choice (entero o cadena) en el cuerpo de la petición. Este endpoint debe:  
       * Recuperar el estado del juego (por ahora, simulado o desde una variable global simple).  
       * Llamar a actions.process\_player\_action() con la elección del jugador.  
       * Devolver el nuevo estado del juego, incluyendo la nueva descripción, el ASCII art y las opciones."  
3. **Integración de la Lógica del Juego:**  
   * **Acción:** Asegurar que los módulos del juego (game\_state, display, actions, dungeon) puedan ser importados y utilizados correctamente por el api/main.py.  
   * **Consideración:** El estado del juego se manejará inicialmente en memoria en el servidor para el MVP, pero se preparará para persistencia en la Fase 2\.  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/api/main.py. Asegúrate de que las llamadas a las funciones de game\_state, display y actions usen un sistema de estado de juego simulado en memoria (ej. un diccionario global que se actualice) para que la API sea funcional para una sola sesión. Incluye comentarios que indiquen dónde se integrará la persistencia con Supabase."

### **Tests:**

1. **Tests de Endpoint API:**  
   * Prompt para la IA integrada en el IDE:  
     "Crea un archivo de test tests/api/test\_game\_api.py. Utiliza pytest y httpx para:  
     * Verificar que el endpoint /health devuelve un estado OK.  
     * Probar el endpoint /game/start y verificar que la respuesta contiene las claves esperadas para el estado inicial del juego.  
     * Probar el endpoint /game/action con una elección válida y una inválida. Verifica que el estado del juego se actualiza y la respuesta es la esperada. Utiliza unittest.mock para simular las llamadas a las funciones de lógica del juego si es necesario para aislar el test de la API."

## **Fase 2: Gestión de Usuarios y Persistencia (Supabase)**

### **Objetivo:**

Implementar la autenticación de usuarios y la persistencia del estado del juego en una base de datos PostgreSQL gestionada por Supabase.

### **Pasos:**

1. **Configuración de Proyecto Supabase:**  
   * **Acción:** Crear un nuevo proyecto en Supabase, habilitar Authentication y crear una tabla para almacenar los estados del juego (game\_sessions).  
   * Prompt para la IA integrada en el IDE:  
     "Crea un esquema SQL para una tabla game\_sessions en Supabase. Debe incluir: user\_id (UUID), session\_id (UUID, clave primaria), game\_state\_data (JSONB, para almacenar el diccionario game\_state), last\_updated\_at (timestamp con valor por defecto)."  
2. **Integración de Cliente Supabase en FastAPI:**  
   * **Acción:** Instalar la librería supabase-py y configurar el cliente en el backend.  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/api/main.py y src/aimaze/config.py.  
     * En config.py, añade variables de entorno para SUPABASE\_URL y SUPABASE\_KEY.  
     * En api/main.py, configura el cliente Supabase al iniciar la aplicación.  
     * Implementa una función de utilidad get\_supabase\_client() que devuelva la instancia del cliente."  
3. **Endpoints de Registro/Login de Usuarios:**  
   * **Acción:** Añadir endpoints para que los usuarios puedan registrarse y autenticarse.  
   * Prompt para la IA integrada en el IDE:  
     "Añade los siguientes endpoints a src/aimaze/api/main.py:  
     * POST /auth/signup: Recibe email y password. Utiliza el cliente Supabase para registrar un nuevo usuario. Devuelve el token de sesión.  
     * POST /auth/login: Recibe email y password. Utiliza el cliente Supabase para autenticar un usuario existente. Devuelve el token de sesión.  
     * GET /auth/me: Recibe el token de sesión en los headers (Bearer Token). Utiliza el cliente Supabase para obtener la información del usuario autenticado."  
4. **Persistencia del Estado del Juego:**  
   * **Acción:** Modificar los endpoints de juego para guardar y cargar el estado de la sesión del usuario en Supabase.  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/api/main.py.  
     * Asegúrate de que los endpoints /game/start y /game/action requieran autenticación. Utiliza dependencias de FastAPI para extraer el user\_id del token de autenticación.  
     * Cuando un juego se inicia (/game/start), verifica si existe una sesión para ese user\_id. Si existe, cárgala; si no, crea una nueva en Supabase.  
     * Después de cada acción del jugador (/game/action), actualiza el game\_state\_data en la tabla game\_sessions para el session\_id y user\_id correspondiente.  
     * Asegúrate de que el game\_state se serialice/deserialice correctamente a JSONB."

### **Tests:**

1. **Tests de Autenticación:**  
   * Prompt para la IA integrada en el IDE:  
     "Actualiza tests/api/test\_game\_api.py. Añade tests para:  
     * POST /auth/signup y POST /auth/login (simulando registros y logeos).  
     * GET /auth/me con un token válido e inválido.  
     * Utiliza un cliente Supabase mockeado si no quieres depender de una instancia real de Supabase para los tests unitarios."  
2. **Tests de Persistencia de Datos:**  
   * Prompt para la IA integrada en el IDE:  
     "Actualiza tests/api/test\_game\_api.py.  
     * Añade un test de integración que: registre un usuario, inicie un juego, realice una acción, y luego simule una nueva sesión para el mismo usuario para verificar que el estado del juego se ha cargado correctamente desde Supabase. Mockea las llamadas a la base de datos Supabase."

## **Fase 3: Interfaz Web Frontend (HTML/CSS/JS)**

### **Objetivo:**

Crear una interfaz de usuario web que simule una terminal de texto retro, interactuando con el backend de FastAPI.

### **Pasos:**

1. **Estructura HTML Básica:**  
   * **Acción:** Crear un archivo index.html con elementos clave para la interfaz.  
   * Prompt para la IA integrada en el IDE:  
     "Crea el archivo frontend/index.html. Debe incluir:  
     * Un div principal para la 'terminal' donde se mostrará el texto del juego.  
     * Un campo de entrada de texto (input) para la elección del jugador.  
     * Un botón para enviar la elección (o manejar el Enter).  
     * Un área para mensajes de estado (ej. "Conectando...").  
     * Enlaces a un archivo CSS (style.css) y un archivo JS (script.js)."  
2. **Estilado CSS (Estilo Monocromo Retro):**  
   * **Acción:** Aplicar estilos para lograr la apariencia de terminal de fósforo verde.  
   * Prompt para la IA integrada en el IDE:  
     "Crea el archivo frontend/style.css. Aplica los siguientes estilos:  
     * Fondo negro, texto verde fluorescente (simulando fósforo verde).  
     * Fuente monoespaciada (ej. 'Press Start 2P', 'VT323', o 'Monospace' genérica).  
     * Bordes para la 'terminal' que simulen ASCII art (ej. con box-shadow o border-image para un efecto pixelado).  
     * Efectos de brillo o parpadeo para el cursor de entrada.  
     * Diseño responsive para que funcione bien en dispositivos móviles."  
3. **Lógica JavaScript (Interacción con Backend):**  
   * **Acción:** Escribir el JavaScript para manejar la UI, la comunicación con la API y el renderizado del contenido del juego.  
   * Prompt para la IA integrada en el IDE:  
     "Crea el archivo frontend/script.js. Este script debe:  
     * Al cargar la página, llamar al endpoint POST /game/start del backend.  
     * Mostrar la descripción de la ubicación y el ASCII art recibidos en el div de la terminal.  
     * Mostrar las opciones al usuario.  
     * Al enviar la entrada del usuario (botón o Enter), llamar al endpoint POST /game/action con la elección.  
     * Actualizar la interfaz de usuario con el nuevo estado del juego recibido del backend.  
     * Implementar un sistema de autenticación básico (guardar token en localStorage y adjuntarlo a las peticiones)."  
4. **Renderizado de ASCII Art y Texto:**  
   * **Acción:** Asegurar que el contenido recibido de la API (descripción y ASCII art) se muestre correctamente.  
   * **Consideración:** El ASCII art a menudo requiere etiquetas \<pre\> para mantener el formato.  
   * Prompt para la IA integrada en el IDE:  
     "Modifica frontend/script.js. Al renderizar el contenido, asegúrate de que el ASCII art se coloque dentro de una etiqueta \<pre\> para preservar el espaciado. Haz que el texto de la descripción sea legible y formateado correctamente."

### **Tests:**

1. **Tests de UI Frontend:**  
   * **Acción:** Pruebas manuales en el navegador para verificar la apariencia y el flujo.  
   * **Tests de Integración API en Frontend:**  
     * Prompt para la IA integrada en el IDE:  
       "Sugiere cómo podríamos simular pruebas automatizadas para el frontend que interactúen con el backend (ej. usando Cypress o Playwright). Por ahora, solo necesitamos la estructura de cómo se harían, no la implementación completa."

## **Fase 4: Contenerización (Docker)**

### **Objetivo:**

Empaquetar el backend de FastAPI y el frontend estático en contenedores Docker para un despliegue consistente.

### **Pasos:**

1. **Dockerfile para el Backend (FastAPI):**  
   * **Acción:** Crear un Dockerfile para la aplicación FastAPI.  
   * Prompt para la IA integrada en el IDE:  
     "Crea el archivo Dockerfile.backend en la raíz del proyecto. Este Dockerfile debe:  
     * Usar una imagen base de Python.  
     * Copiar el código de la aplicación FastAPI.  
     * Instalar las dependencias de requirements.txt.  
     * Exponer el puerto donde corre Uvicorn.  
     * Definir el comando para iniciar Uvicorn."  
2. **Dockerfile para el Frontend (Nginx o FastAPI como servidor de estáticos):**  
   * **Acción:** Servir los archivos estáticos del frontend. Opción 1: Nginx. Opción 2: FastAPI. Para simplificar el MVP, FastAPI sirviendo estáticos es más fácil.  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/api/main.py. Añade código para servir los archivos estáticos desde la carpeta frontend cuando la aplicación se ejecute. Esto eliminará la necesidad de un servidor web separado para el frontend en el MVP. Asegúrate de que los archivos como index.html, style.css y script.js sean accesibles."  
3. **Generación de docker-compose.yml (Opcional para desarrollo local):**  
   * **Acción:** Un archivo docker-compose.yml para levantar el backend y, si fuera el caso, un frontend separado, para desarrollo local. Para el MVP con FastAPI sirviendo estáticos, sería más sencillo.  
   * Prompt para la IA integrada en el IDE:  
     "Crea un archivo docker-compose.yml simple para levantar el servicio de backend con Uvicorn. Expón el puerto necesario para que el frontend (servido por el mismo backend) sea accesible."

### **Tests:**

1. **Tests de Construcción/Ejecución de Docker:**  
   * **Acción:** Construir y ejecutar las imágenes de Docker localmente.  
   * Prompt para la IA integrada en el IDE:  
     "Proporciona los comandos de terminal necesarios para construir la imagen Docker del backend y luego ejecutarla localmente. Verifica que la aplicación es accesible en el puerto expuesto."

## **Fase 5: Despliegue en Google Cloud Platform (GCP)**

### **Objetivo:**

Desplegar la aplicación contenerizada en un entorno escalable y accesible en GCP.

### **Pasos:**

1. **Configuración del Proyecto Google Cloud:**  
   * **Acción:** Crear un nuevo proyecto en GCP y habilitar las APIs necesarias (Cloud Run, Artifact Registry, Cloud Build).  
   * Prompt para la IA integrada en el IDE:  
     "Enumera los comandos gcloud necesarios para:  
     * Crear un nuevo proyecto GCP (si no existe).  
     * Establecer el proyecto por defecto.  
     * Habilitar las APIs de Cloud Run, Artifact Registry y Cloud Build."  
2. **Configuración de gcloud CLI:**  
   * **Acción:** Autenticarse y configurar el CLI localmente.  
   * **Consideración:** Se asume que el usuario ya tiene el CLI instalado.  
3. **Subida de Imagen Docker a Artifact Registry:**  
   * **Acción:** Construir la imagen Docker y subirla al registro de contenedores de GCP.  
   * Prompt para la IA integrada en el IDE:  
     "Proporciona los comandos gcloud para:  
     * Configurar Docker para autenticarse en Artifact Registry.  
     * Construir la imagen Docker (Dockerfile.backend) y taggearla con el nombre del registro de Artifact Registry.  
     * Subir la imagen al Artifact Registry."  
4. **Despliegue en Cloud Run:**  
   * **Acción:** Crear y desplegar un servicio Cloud Run utilizando la imagen Docker del backend.  
   * **Consideración:** Configurar variables de entorno (Supabase URL, Key) en Cloud Run.  
   * Prompt para la IA integrada en el IDE:  
     "Proporciona el comando gcloud run deploy para desplegar el servicio. Este comando debe:  
     * Especificar el nombre del servicio (ej. aimaze-game).  
     * Apuntar a la imagen Docker en Artifact Registry.  
     * Configurar las variables de entorno SUPABASE\_URL y SUPABASE\_KEY.  
     * Permitir acceso no autenticado (para MVP público).  
     * Especificar la región de despliegue."

### **Tests:**

1. **Test de Despliegue End-to-End:**  
   * **Acción:** Verificar que la aplicación desplegada es accesible a través de la URL de Cloud Run y que el juego funciona correctamente (inicio de sesión, juego, persistencia).  
   * **Consideración:** Esta es una prueba manual crucial después del despliegue.

## **Conclusión y Próximos Pasos**

Este plan de distribución proporciona una hoja de ruta para hacer que AiMaze sea accesible como una aplicación web. Una vez que la API esté desplegada en Cloud Run con Supabase, los usuarios podrán acceder al juego a través de su navegador web y disfrutar de la experiencia de la mazmorra generada por IA.

Los siguientes pasos después de la implementación de este plan de distribución podrían incluir la monitorización, la mejora continua de la interfaz de usuario, la adición de más funcionalidades de juego, y la optimización del rendimiento y los costes en GCP.

## Siguientes Incrementos

**Incremento 2**: Más Niveles y Objetivo: Permitir la progresión a través de múltiples niveles simulados hasta el objetivo final (salir).
**Incremento 3**: Monstruos y Encuentros Azarosos: Introducir la posibilidad de encuentros con criaturas, con mensajes placeholder para el combate.
**Incremento 4**: Puzzles y Obstáculos Simples: Implementar puertas cerradas, trampas simples que requieran una elección específica (ej. "saltar el foso" vs "buscar un puente").
**Incremento 5**: Características del Jugador y Sistema de Enfrentamiento: Definir atributos (Fuerza, Destreza, etc.) y un sistema básico de "tirada de dados" para resolver desafíos y combates.