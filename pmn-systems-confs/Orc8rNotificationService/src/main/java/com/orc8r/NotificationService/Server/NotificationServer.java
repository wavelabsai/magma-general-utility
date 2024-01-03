package com.orc8r.NotificationService.Server;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class NotificationServer implements NotificationServerInterface{


    private ServerSocket serverSocket = null;
    private String host;
    private Integer port;

    private NotificationClients clients = null;

    private boolean serverRunning;
    public NotificationServer(String host, Integer port) {
        this.host = host;
        this.port = port;
    }

    public NotificationServer(Integer port) {
        this.host = "localhost";
        this.port = port;
    }

    @Override
    public void init() {
        try {
            serverSocket = new ServerSocket(this.port);
            System.out.println("Server Started on  " + serverSocket );
            serverRunning = true;
        } catch (IOException e) {
            e.printStackTrace();
        }

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
        //System.out.println("New client connected... " );
        System.out.println("Waiting for client to be connected " );
        while (serverRunning) {
            try {
                Socket clientSocket = serverSocket.accept();
                System.out.println("New client connected... " + clientSocket);
                ClientRequestHandler handler = new ClientRequestHandler(clientSocket);
                handler.addNotificationClient(this.clients);
                Thread th = new Thread(handler);
                th.setName("Plain socket Client");
                th.start();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
}
