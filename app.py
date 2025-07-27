from flask import Flask, request, render_template_string
import socket
import subprocess

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Web Recon Scanner</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light text-dark">
    <div class="container mt-4">
        <h2 class="text-center mb-4">🌐 Web Recon Scanner</h2>
        <form method="POST">
            <div class="mb-3">
                <label for="target" class="form-label">Website URL (with http://)</label>
                <input type="text" class="form-control" name="target" placeholder="http://example.com" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Scan Type</label>
                <select name="scan_type" class="form-select">
                    <option value="quick">Quick Scan</option>
                    <option value="full">Full Scan (no root)</option>
                    <option value="os">OS Detection (root)</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary w-100">🚀 Start Scan</button>
        </form>

        <div class="text-center mt-4">
            <button class="btn btn-dark" onclick="document.body.classList.toggle('bg-dark'); document.body.classList.toggle('text-light')">🌓 Toggle Dark Mode</button>
        </div>

        {% if result %}
        <div class="mt-4 alert alert-secondary">
            <pre>{{ result }}</pre>
        </div>

        {% if show_button %}
        <div class="text-center">
            <a href="http://{{ ip_address }}" target="_blank">
                <button class="btn btn-success mt-2">🌐 Open IP in Browser</button>
            </a>
        </div>
        {% endif %}
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    show_button = False
    ip_address = None

    if request.method == 'POST':
        target = request.form['target'].strip()
        scan_type = request.form['scan_type']

        try:
            ip_address = socket.gethostbyname(target.replace('http://', '').replace('https://', '').split('/')[0])
            result += f"🔍 Scanning: {target}\n📍 IP Address: {ip_address}\n\n"
        except Exception as e:
            result = f"❌ Error resolving domain: {e}"
            return render_template_string(TEMPLATE, result=result)

        if scan_type == "quick":
            cmd = ['nmap', '-F', ip_address]
        elif scan_type == "full":
            cmd = ['nmap',  ip_address]
        elif scan_type == "os":
            cmd = ['nmap', '-O', ip_address]
        else:
            result += "⚠️ Invalid scan type selected."
            return render_template_string(TEMPLATE, result=result)

        try:
            output = subprocess.check_output(cmd, text=True)
            result += f"🧪 Nmap Output:\n{output}"
            if scan_type != "os":
                show_button = True
        except Exception as e:
            result += f"⚠️ Error running scan: {e}"

    return render_template_string(TEMPLATE, result=result, show_button=show_button, ip_address=ip_address)

if __name__ == '__main__':
    import os
    # For Termux: Automatically open browser
    try:
        os.system("termux-open-url http://localhost:5000")
    except:
        pass
    app.run(host='0.0.0.0', port=5000)
