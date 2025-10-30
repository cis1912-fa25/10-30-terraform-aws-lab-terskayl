from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import socket
import os
import platform

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    hostname = socket.gethostname()

    # Try to get EC2 metadata, fallback if not available
    try:
        instance_id = os.popen('ec2-metadata --instance-id 2>/dev/null').read().split(': ')[1].strip()
        availability_zone = os.popen('ec2-metadata --availability-zone 2>/dev/null').read().split(': ')[1].strip()
    except:
        instance_id = "N/A (not on EC2)"
        availability_zone = "N/A (not on EC2)"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Terraform + Docker Web Server</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            .container {{
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }}
            h1 {{
                margin-top: 0;
            }}
            .info {{
                background: rgba(0, 0, 0, 0.2);
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
            }}
            code {{
                background: rgba(0, 0, 0, 0.3);
                padding: 2px 6px;
                border-radius: 3px;
            }}
            .badge {{
                display: inline-block;
                padding: 5px 10px;
                border-radius: 5px;
                margin: 5px 5px 5px 0;
            }}
            .terraform-badge {{
                background: #7B42BC;
            }}
            .docker-badge {{
                background: #2496ED;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Hello from Terraform + Docker!</h1>
            <p>This containerized application is running on infrastructure provisioned entirely through code.</p>

            <div class="info">
                <h3>Instance Information:</h3>
                <p><strong>Container Hostname:</strong> <code>{hostname}</code></p>
                <p><strong>Instance ID:</strong> <code>{instance_id}</code></p>
                <p><strong>Availability Zone:</strong> <code>{availability_zone}</code></p>
            </div>

            <div>
                <span class="badge terraform-badge">⚡ Provisioned with Terraform</span>
                <span class="badge docker-badge">🐳 Running in Docker</span>
            </div>

            <p>This entire infrastructure - ECR repository, EC2 instance, security group, and container orchestration - was created from declarative configuration files. No clicking required!</p>
        </div>
    </body>
    </html>
    """
    return html

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "terraform-docker-web-server",
        "hostname": socket.gethostname()
    }
