package com.vletris.NotificationService.test;

import nl.altindag.ssl.SSLFactory;
import nl.altindag.ssl.pem.util.PemUtils;

import javax.net.ssl.*;
import java.io.*;
import java.net.InetAddress;
import java.net.Socket;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;

public class NotificationClient {

    private static final int SERVER_PORT = 4443;
    private static final String TLS_VERSION = "TLSv1.2";
    private static final int SERVER_COUNT = 1;
    private static final String SERVER_HOST_NAME = "127.0.0.1";
    private static final String TRUST_STORE_NAME = "servercert.p12";
    private static final char[] TRUST_STORE_PWD = new char[] {'a', 'b', 'c', '1',
            '2', '3'};
    private static final String KEY_STORE_NAME = "servercert.p12";
    private static final char[] KEY_STORE_PWD = new char[] {'a', 'b', 'c', '1',
            '2', '3'};

    public static void main1(String[] args) throws Exception {
        TLSClient client = new TLSClient();
        System.setProperty("javax.net.debug", "ssl");
        String returnedValue = client.request(
                InetAddress.getByName(SERVER_HOST_NAME), SERVER_PORT, TLS_VERSION,
                TRUST_STORE_NAME, TRUST_STORE_PWD, KEY_STORE_NAME, KEY_STORE_PWD);
    }

    public static void main(String[] args) throws NoSuchAlgorithmException, KeyManagementException, IOException {
        String basePath = Paths.get("").toAbsolutePath().toString();
        String cacert = basePath + "/certs/cacert.pem";
        Path cacertPath = Paths.get(cacert);
        String key = basePath + "/certs/key.pem";
        Path keyPath = Paths.get(key);
        String certicate = basePath + "/certs/cert.pem";
        Path certPath = Paths.get(certicate);


        KeyManager keyManager = PemUtils.loadIdentityMaterial(certPath,keyPath);
        TrustManager trustManager = PemUtils.loadTrustMaterial(cacertPath);
        //List<?> list = PemUtils.loadCertificate(certPath);

        SSLFactory factory1 = SSLFactory.builder()
                .withIdentityMaterial((X509KeyManager) keyManager)
                .withTrustMaterial((X509TrustManager) trustManager)
                .build();

        SSLContext context = SSLContext.getInstance("TLS");
        context.init(new KeyManager[]{keyManager},new TrustManager[]{trustManager}, SecureRandom.getInstanceStrong());
        SSLSocketFactory socketFactory = context.getSocketFactory();

        Socket s = null;

        s = socketFactory.createSocket("localhost", 4443);
        System.out.println(s);

        PrintWriter out = new PrintWriter(s.getOutputStream(), true);
        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
        BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
            String userInput = "register";
            out.println(userInput);
            out.flush();
            while ((userInput = in.readLine()) != null) {

                System.out.println("Received: " + in.readLine());
            }
        }


}
