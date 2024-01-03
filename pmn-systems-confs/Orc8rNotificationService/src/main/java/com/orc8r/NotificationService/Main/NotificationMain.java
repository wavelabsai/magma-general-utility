package com.orc8r.NotificationService.Main;

import com.orc8r.NotificationService.Server.NotificationClients;
import com.orc8r.NotificationService.Server.NotificationServer;
import com.orc8r.NotificationService.Server.NotificationServerInterface;
import nl.altindag.ssl.SSLFactory;
import nl.altindag.ssl.pem.util.PemUtils;


import javax.net.ssl.*;
import java.io.*;
import java.net.Socket;
import java.nio.file.Path;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.nio.file.Paths;
import java.util.List;


    public class NotificationMain {
    private static final int SERVER_PORT = 8444;
    private static final String TLS_VERSION = "TLSv1.2";
    private static final int SERVER_COUNT = 1;
    private static final String SERVER_HOST_NAME = "127.0.0.1";
    private static final String TRUST_STORE_NAME = "servercert.p12";
    private static final char[] TRUST_STORE_PWD = new char[] {'a', 'b', 'c', '1',
            '2', '3'};
    private static final String KEY_STORE_NAME = "servercert.p12";
    private static final char[] KEY_STORE_PWD = new char[] {'a', 'b', 'c', '1',
            '2', '3'};

    /*public static void main1(String[] args) throws Exception {
        TLSServer server = new TLSServer();

        System.setProperty("javax.net.debug", "ssl");
        ExecutorService serverExecutor = Executors.newFixedThreadPool(SERVER_COUNT);
        serverExecutor.submit(() -> {
            try {
                server.serve(SERVER_PORT, TLS_VERSION, TRUST_STORE_NAME,
                        TRUST_STORE_PWD, KEY_STORE_NAME, KEY_STORE_PWD);
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }*/
    public static void main2(String[] args) throws IOException, NoSuchAlgorithmException, KeyManagementException {

        String basePath = Paths.get("").toAbsolutePath().toString();
        String cacert = basePath + "/certs/cacert.pem";
        Path cacertPath = Paths.get(cacert);
        String key = basePath + "/certs/key.pem";
        Path keyPath = Paths.get(key);
        String certicate = basePath + "/certs/cert.pem";
        Path certPath = Paths.get(certicate);
        System.setProperty("javax.net.debug", "ssl");


        KeyManager  keyManager = PemUtils.loadIdentityMaterial(certPath,keyPath);
        TrustManager trustManager = PemUtils.loadTrustMaterial(cacertPath);
        List<?> list = PemUtils.loadCertificate(certPath);


        SSLFactory factory = SSLFactory.builder()
                .withIdentityMaterial((X509KeyManager) keyManager)
                .withTrustMaterial((X509TrustManager) trustManager)
                .build();
        System.out.println(factory);

        SSLContext context = SSLContext.getInstance("TLS");
        context.init(new KeyManager[]{keyManager}, new TrustManager[]{trustManager},
                SecureRandom.getInstanceStrong());
        SSLServerSocketFactory socketFactory = context.getServerSocketFactory();
        SSLServerSocket serverSocket =  (SSLServerSocket) socketFactory.createServerSocket(4443);
        System.out.println(serverSocket.getEnabledCipherSuites());

        serverSocket.setNeedClientAuth(true);
        serverSocket.setEnabledProtocols(new String[] {"TLSv1.2"});

        byte[] buffer = new byte[512];
        while(true) {
            Socket socket = serverSocket.accept();
            System.out.println(socket);
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            out.println("Hello World!");

        }
    }

    public static void main(String[] args) {
        if (args.length >= 0 && args.length != 2) {
            if (args.length == 1 && "test".equalsIgnoreCase(args[0])) {
                System.out.println("Usage registering subscribers");
                System.out.println("java -cp <JarName> com.orc8r.NotificationService.test,TestNotificationSubscriberClient  <NotificationServerAddress> <PublisherPort>");
                System.out.println("java -cp Orc8rNotificationService-1.0-SNAPSHOT.jar com.orc8r.NotificationService.test.TestNotificationSubscriberClient localhost 4443");
                System.out.println("Usage for publishing subscriber change");
                System.out.println("java -cp <JarName> com.orc8r.NotificationService.test,TestNotificationSubscriberClient  <NotificationServerAddress> <PublisherPort>");
                System.out.println("java -cp Orc8rNotificationService-1.0-SNAPSHOT.jar com.orc8r.NotificationService.test.TestPlainNotificationClient localhost 4442");
                System.exit(1);
            }
            System.out.println("Usage");
            System.out.println("java -jar <JarName> <PublisherPort> <SubscriberPort>");
            System.out.println("java -jar Orc8rNotificationService-1.0-SNAPSHOT.jar 4442 4443");
            System.exit(1);
        }
        Integer pubPort = 4442;
        Integer subPort = 4443;
        try {
            String pubportStr = args[0];
            String subPortStr = args[1];
            pubPort = Integer.parseInt(pubportStr);
            subPort = Integer.parseInt(subPortStr);
        }catch (NumberFormatException ne) {
            ne.printStackTrace();
        }

        System.out.println(pubPort);
        System.out.println(subPort);
        //System.exit(1);
        NotificationClients clients = new NotificationClients();
        NotificationServerInterface plainSeverSocket = new NotificationServer(pubPort);
        plainSeverSocket.addNotificationClient(clients);
        plainSeverSocket.init();
        NotificationServerInterface sslServerSocket = new NotificationServer(subPort);
        sslServerSocket.addNotificationClient(clients);
        sslServerSocket.init();
        Thread plainThread = new Thread(plainSeverSocket);
        plainThread.setName("Plain Socket");
        plainThread.start();
        Thread sslThread = new Thread(sslServerSocket);
        sslThread.setName("SSL Socket");
        sslThread.start();

    }
}
