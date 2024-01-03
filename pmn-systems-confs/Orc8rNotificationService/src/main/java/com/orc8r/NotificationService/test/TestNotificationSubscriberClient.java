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

public class TestNotificationSubscriberClient {
    public static void main(String[] args) throws IOException {

        if (args.length == 0 || args.length != 2) {
            System.out.println("Usage registering subscribers");
            System.out.println("java -cp <JarName> com.orc8r.NotificationService.test,TestNotificationSubscriberClient  <NotificationServerAddress> <PublisherPort>");
            System.out.println("java -cp Orc8rNotificationService-1.0-SNAPSHOT.jar com.orc8r.NotificationService.test.TestNotificationSubscriberClient localhost 4443");
            System.exit(1);
        }
        String host = args[0];
        String portStr = args[1];
        Integer port = 4442;
        try {
            port = Integer.parseInt(portStr);
        } catch (NumberFormatException ne) {
            ne.printStackTrace();
            host = "localhost";
        }
        Socket s = null;
        try {
            s = new Socket(host, port);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        System.out.println(s);

        PrintWriter out = new PrintWriter(s.getOutputStream(), true);
        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
        String userInput = "register";
        out.println(userInput);
        out.flush();
        while ((userInput = in.readLine()) != null) {

            System.out.println("Received: " + userInput);
        }
    }

    public static void main1(String[] args) throws IOException {
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
