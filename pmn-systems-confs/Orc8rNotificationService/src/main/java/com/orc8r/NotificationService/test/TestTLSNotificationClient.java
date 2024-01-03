package com.orc8r.NotificationService.test;

import nl.altindag.ssl.SSLFactory;
import nl.altindag.ssl.pem.util.PemUtils;

import javax.net.ssl.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;

public class TestTLSNotificationClient {
    public static void main1(String[] args) throws NoSuchAlgorithmException, KeyManagementException, IOException {
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

            System.out.println("Received: " + userInput);
        }
    }

    public static void main(String[] args) throws IOException {
        try {
            Socket echoSocket = new Socket("localhost", 4222);
            System.out.println(echoSocket);
            PrintWriter out = new PrintWriter(echoSocket.getOutputStream(), true);
            String userInput = "Register";
            out.println(userInput);
            out.flush();
            echoSocket.close();
        }catch (UnknownHostException e) {
            System.err.println("Don't know about host ");
            System.exit(1);
        }catch (IOException e) {
            System.err.println("Couldn't get I/O for the connection to ");
            System.exit(1);
        }
    }
}
