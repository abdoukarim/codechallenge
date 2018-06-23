# Installation
Install docker and docker compose

Clone the project and build the project by running
```bash
$ git clone https://github.com/abdoukarim/codechallenge
$ docker-compose up -d
```

After completing the installation, access the app by clicking the following link (http://localhost:8888)

## Note:
The app is not immediately available on port 8888 because the containers 
are still being initialized and may take a couple of minutes before the first load.

# Best way to safely store and manage the keys
To safely store and manage the keys, we can you use docker vault [vault](https://hub.docker.com/_/vault/)
Vault is a tool for securely accessing secrets. 
A secret is anything that you want to tightly control access to, such as API keys, passwords, certificates, and more. 
Vault provides a unified interface to any secret, while providing tight access control and recording a detailed audit log.
