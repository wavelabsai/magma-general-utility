package com.orc8r.NotificationService.Server;

import java.io.IOException;

public class PlainServer {

    public static void main(String[] args) throws IOException {
        NotificationServer server = new NotificationServer(4442);
        server.init();
        Thread th = new Thread(server);
        th.start();


    }
}
