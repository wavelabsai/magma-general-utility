
# Test Suci Extension in Magma with spirent

**Basic information about SUCI**

![image](https://github.com/wavelabsai/magma-general-utility/assets/131740331/9a6dc735-5073-483d-b552-0e7c151fc172)



* SUCI is a privacy-preserving identifier containing the concealed SUPI.
* SUCI is a one-time use subscription identifier, and a different SUCI is generated after SUCI has been used.
* The UE shall generate a SUCI using a protection scheme with the raw public key, i.e., the Home Network Public Key, that was securely provisioned in control of the home network.
* Both UE and Home Network can derive the SUPI from SUCI and vice versa.
* The UE shall construct a scheme-input from the subscription identifier part of the SUPI as follows:
  * For SUPIs containing IMSI, the subscription identifier part of the SUPI includes the MSIN of the IMSI as defined in TS 23.003.
  * For SUPIs taking the form of a NAI, the subscription identifier part of the SUPI includes the "username" portion of the NAI (Network Access Identifier) as defined in NAI RFC 7542.
    

### I. Generate the keys
1. Generate the private key:
   ```
   openssl genpkey -algorithm x25519 -out x25519.key.pem
   ``` 
2. To view the keys:
   ```
   openssl pkey -in x25519.key.pem -text
   ``` 
   ![image](https://github.com/wavelabsai/magma-general-utility/assets/131740331/aaa513b9-5b42-4611-b4f0-9202e9c05d79)


3. Format Private Key:
   
    - Private key(hex): ```48:d4:6f:5a:89:db:04:7b:f5:c1:ea:dc:5a:1c:bf:b2:06:79:22:80:af:9b:db:87:77:c9:09:0a:74:86:db:78```
   
    - Remove Colons and add "0x"(hex): ```0x48d46f5a89db047bf5c1eadc5a1cbfb206792280af9bdb8777c9090a7486db78```

    - Convert to private key to base64:
      ```
      SNRvWonbBHv1wercWhy/sgZ5IoCvm9uHd8kJCnSG23g=
      ```
      
4. Format Public Key:
   
    - Public key(hex): ```a1:1b:f9:0a:da:a0:3a:0c:df:57:9a:1d:86:33:e0:2f:43:d8:f5:3e:f8:e1:52:63:07:81:df:1f:0d:15:ef:0c```
   
    - Remove Colons and add "0x"(hex): ```0xa11bf90adaa03a0cdf579a1d8633e02f43d8f53ef8e152630781df1f0d15ef0c```

    - Convert to public key to base64:
      ```
      oRv5CtqgOgzfV5odhjPgL0PY9T744VJjB4HfHw0V7ww=
      ```
### II. Configure the suci profiles through swagger:
- **Network ID:** Check NMS to get the network id to which the AGW is connected.
- **home_network_private_key** : (generated in step 3)
      ```
      SNRvWonbBHv1wercWhy/sgZ5IoCvm9uHd8kJCnSG23g=
      ```
- **home_network_public_key** : (generated in step 4)
      ```
      oRv5CtqgOgzfV5odhjPgL0PY9T744VJjB4HfHw0V7ww=
      ```
- **home_network_public_key_identifier**: 22 (Any number between 0-255)
- **protection_scheme**: ProfileA (X25519 algo,this profile has been used as an example in this guide) **OR**
                         ProfileB (ECDH_SECP256R1 algo)
  
![image](https://github.com/wavelabsai/magma-general-utility/assets/131740331/e5e81c2c-4da3-4505-a536-2a946264fb1b)


### III. Configure Spirent test case:
1. Session builder -> Amf nodal -> NAS-5G -> MM
   ![image](https://github.com/wavelabsai/magma-general-utility/assets/131740331/1ab7483d-9c44-4f0a-b5c3-51cbe032259f)


     ![image](https://github.com/wavelabsai/magma-general-utility/assets/131740331/d6f077bb-30c2-48fe-b87f-f21cacc62fdf)



### Working pcap and logs

[suci_extension.zip](https://github.com/wavelabsai/magma-general-utility/files/13246896/suci_extension.zip)

*** 
### References:
1. Magma Docs: https://magma.github.io/magma/docs/lte/suci_extensions
2. OpenSsl Output breakdown: https://stackoverflow.com/questions/60303561/how-do-i-pass-a-44-bytes-x25519-public-key-created-by-openssl-to-cryptokit-which
3. Hex to Base64 online converter: https://base64.guru/converter/encode/hex


