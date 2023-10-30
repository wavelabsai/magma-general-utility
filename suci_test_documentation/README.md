**Basic information about SUCI**

![image](https://github.com/Rameshwar-Kanade/Magma-exp/assets/131740331/7843571b-657e-4063-babc-fa1b7c07e600)


* SUCI is a privacy-preserving identifier containing the concealed SUPI.
* SUCI is a one-time use subscription identifier, and a different SUCI is generated after SUCI has been used.
* The UE shall generate a SUCI using a protection scheme with the raw public key, i.e., the Home Network Public Key, that was securely provisioned in control of the home network.
* Both UE and Home Network can derive the SUPI from SUCI and vice versa.
* The UE shall construct a scheme-input from the subscription identifier part of the SUPI as follows:
  * For SUPIs containing IMSI, the subscription identifier part of the SUPI includes the MSIN of the IMSI as defined in TS 23.003.
  * For SUPIs taking the form of a NAI, the subscription identifier part of the SUPI includes the "username" portion of the NAI (Network Access Identifier) as defined in NAI RFC 7542.


**Generate the private key as below**

      openssl genpkey -algorithm x25519 -out x25519.key.pem 

**Private key can be viewed with the command**

      openssl pkey -in x25519.key.pem -text 

**Generate the public key as below**

     openssl pkey -in x25519.key.pem -pubout -outform PEM 

**Configuration SUCI Extensions** 

While creating the LTE network, SUCI Profiles can be established using the below swagger API. 

**Create SUCI Profile**

HTTP Method: POST

Endpoint: /lte

Body:
```
POST - /lte
{
  "ngc": {
    "suci_profiles": [
      {
        "home_network_private_key": "2S2YxQinTRiAYmkL+i3WW0TpJ+RHf83HC1JqWE1bxzs=",
        "home_network_public_key": "YHkGb8+c4KQYsWtz5pevQinvdHQyz1jkgq8vg1vMp08=",
        "home_network_public_key_identifier": 2,
        "protection_scheme": "ProfileA"    
      }
    ]
  }
}
```
 

**1. Add a SUCI Profile to an existing LTE network, we may do it with the swagger API listed below.**

 ![image](https://github.com/Rameshwar-Kanade/Magma-exp/assets/131740331/6be8bbde-021a-4548-9367-f05b3b86c780)

 

**2. Go to LTE Networks.** 

![image](https://github.com/Rameshwar-Kanade/Magma-exp/assets/131740331/cf6931e9-d51b-4eff-b886-6705eea4561f)


**3. Go to PUT - lte/{network_id}/cellular/ngc.**

  Add network_id(Add whatever added in orc8r) 

  ![image](https://github.com/Rameshwar-Kanade/Magma-exp/assets/131740331/7fc7836e-c99b-438d-ad5c-4fe28cb2c736)

