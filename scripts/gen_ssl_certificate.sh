#!/bin/bash

cert_path="ssl_certificate"

# Generate SSL certificate and key if not present
if [ ! -d "$cert_path" ]; then
    mkdir "$cert_path"
    echo "Created ${cert_path} directory"
fi

if [ -f "$cert_path/key.pem" ] && [ -f "$cert_path/cert.pem" ]; then
    read -r -p "SSL certificate and key already exist. Do you want to overwrite them? (y/n): " choice
    choice=${choice:-n}  # Default to "n" if no input
    case "$choice" in
        y|Y ) echo "Overwriting SSL certificate and key...";;
        * ) echo "Skipping SSL certificate and key generation"; exit 0;;
    esac
fi

echo "Generating self-signed SSL certificate and key..."

openssl genpkey -algorithm RSA -out "${cert_path}/key.pem"
openssl req -new -x509 -key "${cert_path}/key.pem" -out "${cert_path}/cert.pem" -days 365 \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"

echo "SSL certificate and key generated successfully."

# Add SSL certificate and key to environment variables
./scripts/update_env.sh SSL_CERT_FILE "${cert_path}/cert.pem"
./scripts/update_env.sh SSL_KEY_FILE "${cert_path}/key.pem"

echo "SSL certificate and key added to .env file"

# Determine the OS type
OS_TYPE=$(uname)

# Add the certificate based on OS
if [[ "$OS_TYPE" == "Linux" ]]; then
    # Try to detect the distro using /etc/os-release (works on most Linux distros)
    if [[ -f "/etc/os-release" ]]; then
      DISTRO=$(grep -i '^id=' /etc/os-release | cut -d= -f2 | tr -d '"')
    else
      echo "Unable to determine Linux distribution. Please install lsb_release or check your OS."
      exit 1
    fi

    # Add the certificate based on the detected distribution
    case "$DISTRO" in
      ubuntu|debian)
        sudo cp "${cert_path}/cert.pem" /usr/local/share/ca-certificates/
        sudo update-ca-certificates;;
      redhat|centos|fedora)
        sudo cp "${cert_path}/cert.pem" /etc/pki/ca-trust/source/anchors/
        sudo update-ca-trust;;
      *)
        echo "Unsupported Linux distribution: $DISTRO"
        exit 1;;
    esac
elif [[ "$OS_TYPE" == "Darwin" ]]; then
    # macOS: Add to system keychain
    sudo security add-certificates -k /Library/Keychains/System.keychain "${cert_path}/cert.pem"
    echo "Certificate added to macOS Keychain"
else
    echo "Unsupported OS"
    exit 1
fi

echo "Certificate added successfully to trusted store."
