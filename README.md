# Orbital Viewer Project

This project is a full-stack application for visualizing orbital trajectories in 3D. It consists of a **backend** built with FastAPI and a **frontend** built with React and Three.js.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setting Up WSL with Docker](#setting-up-wsl-with-docker)
- [Creating an SSH Key and Adding it to GitHub](#creating-an-ssh-key-and-adding-it-to-github)
- [Cloning the Project via SSH](#cloning-the-project-via-ssh)
- [Running the Project](#running-the-project)

---

## Prerequisites

Before proceeding, ensure you have the following installed on your system:

- **Windows Subsystem for Linux (WSL)**: Install a WSL 2-compatible Linux distribution (e.g., Ubuntu).
- **Docker CLI**: Ensure Docker is installed and configured to work with WSL 2.
- **Git**: If not included with WSL distro Install Git for version control.

---

## Setting Up WSL with Docker

1. **Install WSL**:
   Open PowerShell as Administrator and run:

   ```powershell
   wsl --install
   ```

   Restart your system if prompted.

2. **Install a Linux Distro**:
   After restarting, open a terminal and set up your preferred Linux distribution (e.g., Ubuntu).

3. **Install Docker in WSL**:
   Inside your WSL terminal, run the following commands:

   ```bash
   sudo apt update
   sudo apt install -y docker.io
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

4. **Enable Docker with Systemd**:
   Edit the WSL configuration file to enable systemd:

   ```bash
   sudo nano /etc/wsl.conf
   ```

   Add the following lines:

   ```
   [boot]
   systemd=true
   ```

   Save and exit the file. Restart WSL:

   ```powershell
   wsl --shutdown
   wsl
   ```

5. **Verify Docker Installation**:
   Run the following command to verify Docker is running:
   ```bash
   sudo docker run hello-world
   ```

---

## Creating an SSH Key and Adding it to GitHub

1. **Generate an SSH Key**:
   In your WSL terminal, run:

   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

   Press Enter to accept the default file location and set a passphrase if desired.

2. **Add the SSH Key to the SSH Agent**:
   Start the SSH agent and add your key:

   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

3. **Copy the SSH Key**:
   Copy the public key to your clipboard:

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

   Copy the output.

4. **Add the SSH Key to GitHub**:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys).
   - Click **New SSH Key**.
   - Paste the key and save.

---

## Cloning the Project via SSH

1. **Clone the Repository**:
   In your WSL terminal, run:
   ```bash
   git clone git@github.com:your-username/orbital-viewer.git
   cd orbital-viewer
   ```

---

## Running the Project

1. **Open the Dev Container**:
   Open the project in Visual Studio Code. When prompted, reopen the project in the Dev Container.

2. **Install Dependencies**:
   The Dev Container will automatically install dependencies for both the backend and frontend.

3. **Start the Backend**:
   Open a terminal in the `backend` directory and run:

   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Start the Frontend**:
   Open a terminal in the `frontend` directory and run:
   `bash
    npm run dev
    `
   This command starts the frontend in development mode, allowing you to interact with the isolated frontend only.

To view the full application (frontend served by the FastAPI backend), use:
`bash
    npm run build
    `
This will serve the frontend through the backend at [http://localhost:8000](http://localhost:8000). If you still do not see the app at this address, try restarting the FastAPI server.

5. **Access the Application**:
   - Frontend: Open [http://localhost:5173](http://localhost:5173).
   - Backend: Open [http://localhost:8000/docs](http://localhost:8000/docs) for API documentation.

---

## Notes

- Ensure Docker is running and integrated with WSL.
- If you encounter issues, check the logs in the terminal or Dev Container output.

Happy coding!
