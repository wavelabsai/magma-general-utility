import subprocess

def setup():
    vmip = input("Enter the VM IP address (xxx.xx.xx.x format only): ")
    user = input("Enter the username: ")
    swagger_url = input("Enter the Swagger URL: ")
    return vmip, user, swagger_url

def generate_key_pair():
    subprocess.run(["openssl", "genpkey", "-algorithm", "x25519", "-out", "x25519.key.pem"])
    print("Key has been generated")

def get_private_key():
    private_key_result = subprocess.run(["openssl", "pkey", "-in", "x25519.key.pem", "-text"], capture_output=True, text=True)
    private_key = private_key_result.stdout
    return private_key

def get_public_key():
    subprocess.run(["openssl", "pkey", "-in", "x25519.key.pem", "-pubout", "-outform", "PEM"])
    public_key_result = subprocess.run(["openssl", "pkey", "-in", "x25519.key.pem", "-pubout", "-outform", "PEM"], capture_output=True, text=True)
    public_key = public_key_result.stdout
    return public_key

def swagger(private_key, public_key):
    request_data = {
        "ngc": {
            "suci_profiles": [
                {
                    "home_network_private_key": private_key.strip(),
                    "home_network_public_key": public_key.strip(),
                    "home_network_public_key_identifier": 2,
                    "protection_scheme": "ProfileA"
                }
            ]
        }
    }


    rPut = requests.put(url=(swagger_url} + f"/lte/{network}/cellular/feg_network_id"), cert=({cert_path}, {key_path}),
                                   verify=False)
        print(str(rPut.text))

        if rPut.status_code == 204:
            print("\nPut  Network NGC Configuration Test passed. The response code is:\n")
            print(str(rPut.status_code))

        else:
            print("Put Network NGC Configuration Test failed. The response code  is:\n")
            print(str(rPut.status_code))



if __name__ == "__main__":
    vmip, user, swagger_url = setup()
    generate_key_pair()
    private_key = get_private_key()
    public_key = get_public_key()
    swagger_example(private_key, public_key)
