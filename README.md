# Algorithmic-Sciences-Standardized-Introductory-Task-Osman
Standardized Introductory Task for Software Engineers at Algorithmic Sciences

Installation
Clone the repository:
    git clone https://github.com/your-repo/Algorithmic-Sciences-Standardized-Introductory-Task-Osman.git

Change directory:
    cd Algorithmic-Sciences-Standardized-Introductory-Task-Osman

Install Python dependencies:
    pip install -r requirements.txt

Download and install NSSM:
    Download NSSM from the official website: https://nssm.cc/download
    Extract the downloaded zip file.
    Move nssm.exe to a directory included in your system PATH or provide the full path when running NSSM commands.

Running the Server:
    python Server/server.py

Running the server as a Windows Service (*linux/daemon or service requirement from project instuctions*)
    Open an Administrator Command Prompt:

    Right-click on Command Prompt and select "Run as administrator".
    Navigate to the project directory:
        cd path\to\your\Algorithmic-Sciences-Standardized-Introductory-Task-Osman

    Install the service using NSSM:
        nssm install StringSearchServer "C:\path\to\python.exe" "path\to\your\Algorithmic-Sciences-Standardized-Introductory-Task-Osman\Server\server.py"


    Start the service:
        nssm start StringSearchServer
    Start the service:
        nssm stop StringSearchServer
    Remove the service:
        nssm remove StringSearchServer

    Running the Client
    To interact with the server, use the client script:
        python client.py

    To run the unit tests:
        python -m unittest discover tests

    To run the speed test:
        python tests/speed_test.py


```
```
Algorithmic-Sciences-Standardized-Introductory-Task-Osman
├─ .vscode
│  └─ settings.json
├─ client
│  ├─ client.py
│  ├─ test_client.py
│  └─ __pycache__
├─ config
│  └─ server_config.ini
├─ data
│  └─ 200k.txt
├─ logs
│  └─ server.log
├─ nssm.exe
├─ README.md
├─ requirements.txt
├─ Server
│  ├─ server.py
│  ├─ test_server.py
│  └─ __pycache__
│     └─ server.cpython-312.pyc
├─ Speed_test_results.pdf
├─ speed_test_results.txt
├─ tests
│  ├─ speed_test.py
│  └─ test_ssl.py
├─ test_cert.csr
├─ test_cert.pem
└─ test_key.pem

```