🛠️ Dexter-DDoS

⚠️ Advertencia
💀 Esta herramienta debe utilizarse únicamente en entornos controlados y con permiso expreso del propietario del servidor.
🚨 El uso indebido puede tener consecuencias legales graves, incluyendo sanciones penales.

Dexter-DDoS es una herramienta para ataques tipo DDoS, TCP, UDP y HTTP con opciones configurables como número de hilos y duración.


🚀 Instalación
Requiere Python 3.x 
Tener pip instalado y actualizado

📦 Instalación de dependencias
Clona este repositorio y entra en la carpeta del proyecto:
cd DexterDDoS
pip install -r requirements.txt

🔧 Uso
Ejecuta el script con los siguientes parámetros:
python DexterDDoS.py target port {tcp,udp,http} --threads N --duration S

🔹 target: IP o dominio del objetivo.
🔹 port: Puerto del servidor objetivo.
🔹 tcp, udp, http: Tipo de ataque.
🔹 threads: Número de hilos concurrentes.
🔹 duration: Duración del ataque en segundos.

Ejemplo de uso:
python DexterDDoS.py example.com 80 tcp --threads 100 --duration 60

📜 Licencia
MIT License - Se puede modificar y distribuir libremente el código, siempre respetando los términos de la licencia.




