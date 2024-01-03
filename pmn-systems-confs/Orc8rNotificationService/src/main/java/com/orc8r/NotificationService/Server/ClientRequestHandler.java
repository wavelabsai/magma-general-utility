package com.orc8r.NotificationService.Server;

import java.io.*;
import java.net.Socket;

public class ClientRequestHandler implements Runnable{
    private Socket clientSocket;
    private boolean running = true;
    private String network = NotificationClients.Network_Default;
    private String gateway = NotificationClients.Network_Default;

    private PrintWriter writer = null;

    private NotificationClients notificationClients = null;

    private boolean isTLS = false;

    private boolean closed = false;


    public ClientRequestHandler(final Socket socket) {
        this.clientSocket = socket;
    }

    public ClientRequestHandler(final Socket socket, NotificationClients clients) {
        this.clientSocket = socket;
        this.notificationClients = clients;
    }

    @Override
    public void run() {
        InputStream stream = null;
        System.out.println("Starting stream thread for the client connected");
        try {
            stream = this.clientSocket.getInputStream();
        } catch (IOException e) {
            running = false;
        }
        BufferedReader reader = new BufferedReader(new InputStreamReader(stream));

        OutputStream outputStream = null;

        try {
            outputStream = this.clientSocket.getOutputStream();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        writer = new PrintWriter(outputStream);

        while (running) {
            try {
                String line = reader.readLine();

                if ("subscriber_change".equalsIgnoreCase(line)) {
                    System.out.println("Received a Change in subscriber post");
                    notificationClients.postMessage(this);
                } else if ("register".equalsIgnoreCase(line)) {
                    System.out.println("Received a registration request from AGW");
                    writer.println("subscriber_change");
                    writer.flush();
                    notificationClients.addNewClient(this);
                }
                //System.out.println("Received " +line);
                //writer.println(line);
                //writer.flush();

            } catch (IOException e) {
                System.err.println("Error occurred in connection..  Closing connection");
                if (isTLS()) {
                    notificationClients.removeClient(this);
                }
                closed = true;
                running = false;
                //throw new RuntimeException(e);

            }
        }
    }

    public void sendNotification(){
        writer.println("subscriber_change");
        writer.flush();
    }

    public String getGateway() {
        return gateway;
    }

    public String getNetwork() {
        return network;
    }

    public void setTLS(boolean TLS) {
        isTLS = TLS;
    }

    public boolean isTLS() {
        return isTLS;
    }

    public void addNotificationClient(NotificationClients clients) {
        this.notificationClients = clients;
    }

    public boolean isClosed() {
        return closed;
    }
}
