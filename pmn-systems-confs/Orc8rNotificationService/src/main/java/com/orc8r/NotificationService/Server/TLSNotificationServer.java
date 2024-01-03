package com.orc8r.NotificationService.Server;

import nl.altindag.ssl.SSLFactory;
import nl.altindag.ssl.pem.util.PemUtils;

import javax.net.ssl.*;
import java.io.IOException;
import java.net.Socket;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;

public class TLSNotificationServer implements NotificationServerInterface {


    SSLServerSocket serverSocket = null;
    private boolean serverRunning;
    private String host;
    private Integer port;

    private KeyManager keyManager = null;
    private TrustManager trustManager = null;

    private NotificationClients clients = null;

    public TLSNotificationServer(Integer port) {
        this.port = port;
    }

    public TLSNotificationServer(String host,Integer port) {
        this.port = port;
        this.host = host;
    }


    public void initializeCertificates(String cacert, String key, String cert) {
        String basePath = Paths.get("").toAbsolutePath().toString();
        //String cacert = basePath + "/certs/cacert.pem";
        Path cacertPath = Paths.get(cacert);
        //String key = basePath + "/certs/key.pem";
        Path keyPath = Paths.get(key);
       // String certicate = basePath + "/certs/cert.pem";
        Path certPath = Paths.get(cert);
        //System.setProperty("javax.net.debug", "ssl");

        this.keyManager = PemUtils.loadIdentityMaterial(certPath,keyPath);
        this.trustManager = PemUtils.loadTrustMaterial(cacertPath);
    }

    private void initializeCertificates() {
        String basePath = Paths.get("").toAbsolutePath().toString();
        String cacert = basePath + "/certs/cacert.pem";
        Path cacertPath = Paths.get(cacert);
        String key = basePath + "/certs/key.pem";
        Path keyPath = Paths.get(key);
        String certicate = basePath + "/certs/cert.pem";
        Path certPath = Paths.get(certicate);
        System.setProperty("javax.net.debug", "ssl");

        this.keyManager = PemUtils.loadIdentityMaterial(certPath,keyPath);
        this.trustManager = PemUtils.loadTrustMaterial(cacertPath);
    }


    @Override
    public void init() {
        initializeCertificates();
        SSLFactory factory = SSLFactory.builder()
                .withIdentityMaterial((X509KeyManager) keyManager)
                .withTrustMaterial((X509TrustManager) trustManager)
                .build();
        SSLContext context = null;
        try {
            context = SSLContext.getInstance("TLS");
            context.init(new KeyManager[]{keyManager}, new TrustManager[]{trustManager},
                    SecureRandom.getInstanceStrong());
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        } catch (KeyManagementException e) {
            throw new RuntimeException(e);
        }

        SSLServerSocketFactory socketFactory = context.getServerSocketFactory();


        try {
            this.serverSocket = (SSLServerSocket) socketFactory.createServerSocket(this.port);
            serverRunning = true;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        System.out.println(serverSocket.getEnabledCipherSuites());

        serverSocket.setNeedClientAuth(true);
        serverSocket.setEnabledProtocols(new String[] {"TLSv1.2"});
    }

    @Override
    public void bind() {

    }

    @Override
    public void listen() {

    }

    @Override
    public void accept() {

    }

    @Override
    public void addNotificationClient(NotificationClients clients) {
        this.clients = clients;
    }

    @Override
    public void run() {
        System.out.println("New client connected... " );
        while (serverRunning) {
            try {
                System.out.println("Waiting for client to be connected " );
                Socket clientSocket = serverSocket.accept();

                System.out.println("New client connected... " + clientSocket);
                ClientRequestHandler handler = new ClientRequestHandler(clientSocket);
                handler.setTLS(true);
                handler.addNotificationClient(this.clients);
                Thread th = new Thread(handler);
                th.setName("SSL socket Client");
                th.start();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

}
