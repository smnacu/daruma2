# Daruma Consulting SRL - Website

Sitio web corporativo para Daruma Consulting SRL, una consultora de servicios de TI. Este proyecto implementa una landing page moderna y responsive con soporte técnico integrado.

## 🚀 Características

- Landing page responsive y moderna
- Tema claro/oscuro con detección automática de preferencias del sistema
- Sección de soporte técnico con:
  - Detección automática del sistema operativo
  - Visualización de IP del cliente
  - Descarga directa de TeamViewer QuickSupport
- Arquitectura modular preparada para futuras expansiones
- Despliegue Dockerizado

## 🛠️ Tecnologías

- **Backend**: FastAPI
- **Frontend**: HTML5, CSS3, JavaScript Vanilla
- **Container**: Docker
- **Servidor**: Uvicorn

## 📋 Prerequisitos

- Python 3.8+
- pip (Python package manager)
- Docker (opcional, para despliegue containerizado)

## 🔧 Instalación y Desarrollo Local

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd daruma2
```

2. Crear y activar entorno virtual:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar el servidor de desarrollo:
```bash
uvicorn app.main:app --reload
```

El sitio estará disponible en `http://127.0.0.1:8000`

## 🚀 Despliegue en Producción

### Usando Docker

1. Construir la imagen:
```bash
docker build -t daruma-website .
```

2. Ejecutar el contenedor:
```bash
docker run -d -p 8000:8000 daruma-website
```

### Despliegue Manual en Servidor Linux

1. Instalar las dependencias del sistema:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

2. Crear y configurar el usuario del servicio:
```bash
sudo useradd -r -s /bin/false daruma
```

3. Clonar el repositorio y configurar la aplicación:
```bash
sudo mkdir /opt/daruma
sudo chown daruma:daruma /opt/daruma
git clone <url-del-repositorio> /opt/daruma
cd /opt/daruma
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Crear servicio systemd (/etc/systemd/system/daruma.service):
```ini
[Unit]
Description=Daruma Website
After=network.target

[Service]
User=daruma
Group=daruma
WorkingDirectory=/opt/daruma
Environment="PATH=/opt/daruma/.venv/bin"
ExecStart=/opt/daruma/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

5. Configurar Nginx (/etc/nginx/sites-available/daruma):
```nginx
server {
    listen 80;
    server_name tudominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

6. Activar y iniciar los servicios:
```bash
sudo ln -s /etc/nginx/sites-available/daruma /etc/nginx/sites-enabled/
sudo systemctl enable daruma
sudo systemctl start daruma
sudo systemctl restart nginx
```

## 🔒 Seguridad

El proyecto implementa las siguientes medidas de seguridad:

- CORS (Cross-Origin Resource Sharing) configurado
- Headers de seguridad HTTP
- Rate limiting para prevenir abusos
- Sanitización de inputs
- SSL/TLS en producción

## 📝 Mantenimiento

Para actualizar el sitio:

1. Hacer pull de los cambios:
```bash
git pull origin main
```

2. Reinstalar dependencias:
```bash
pip install -r requirements.txt
```

3. Reiniciar el servicio:
```bash
sudo systemctl restart daruma
```

## 🔍 Monitoreo

Para monitorear los logs:

```bash
# Logs del servicio
sudo journalctl -u daruma -f

# Logs de Nginx
sudo tail -f /var/log/nginx/error.log
```

## 🌐 Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
```

## 📞 Soporte

Para soporte técnico, contactar a:
- Email: soporte@darumaconsulting.com
- Teléfono: [Número de soporte]

## 🔄 Backup

Recomendaciones para backup:

1. Base de datos (cuando se implemente):
```bash
pg_dump -U usuario nombre_db > backup.sql
```

2. Archivos estáticos:
```bash
tar -czf static_backup.tar.gz app/static/
```

## 🚧 TODOs Futuros

- Implementación de base de datos para funcionalidades SaaS
- Panel de administración
- Sistema de tickets de soporte
- Integración con sistemas de monitoreo
- Analytics y tracking de usuarios

## 📄 Licencia

Este proyecto es propiedad de Daruma Consulting SRL. Todos los derechos reservados.
