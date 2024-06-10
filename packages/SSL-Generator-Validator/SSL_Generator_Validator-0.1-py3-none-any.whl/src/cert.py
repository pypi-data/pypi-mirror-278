def create_cert(domain=None):
    import subprocess
    
    # If no domain is provided, prompt for user input
    if domain is None:
        domain = input("Enter the domain name: ")

    try:
        # Run the mkcert command for local development
        subprocess.run(["mkcert", "-key-file", "key.pem", "-cert-file", "cert.pem", domain], check=True)
        print(f"Local certificate created for {domain}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create local certificate for {domain}: {str(e)}")

    try:
        # Run the certbot command for production
        subprocess.run(["certbot", "certonly", "--standalone", "-d", domain], check=True)
        print(f"Production certificate created for {domain}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create production certificate for {domain}: {str(e)}")

if __name__ == "__main__":
    create_cert()
