package com.orc8r.NotificationService.test;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class TestPlainNotificationClient {

    public static void main(String[] args) throws IOException {
        if (args.length == 0 || args.length != 2) {
            System.out.println("Usage for publishing subscriber change");
            System.out.println("java -cp <JarName> com.orc8r.NotificationService.test,TestNotificationSubscriberClient  <NotificationServerAddress> <PublisherPort>");
            System.out.println("java -cp Orc8rNotificationService-1.0-SNAPSHOT.jar com.orc8r.NotificationService.test.TestPlainNotificationClient localhost 4442");
            System.exit(1);
        }
        String host = args[0];
        String portStr = args[1];
        Integer port = 4443;
        try {
            port = Integer.parseInt(portStr);
        } catch (NumberFormatException ne) {
            ne.printStackTrace();
            host = "localhost";
        }

        try {
            Socket echoSocket = new Socket(host, port);
            System.out.println(echoSocket);
            PrintWriter out = new PrintWriter(echoSocket.getOutputStream(), true);
            String userInput = "subscriber_change";
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
