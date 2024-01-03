package com.orc8r.NotificationService.Server;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class NotificationClients {

    public static final String Network_Default = "default";
    private Map<String, Map<String, ClientRequestHandler>> clientMap
            = new ConcurrentHashMap<String, Map<String, ClientRequestHandler>>();

    public NotificationClients() {
        Map<String, ClientRequestHandler> defaultMap = new ConcurrentHashMap<String, ClientRequestHandler>();
        clientMap.put("default",defaultMap);
    }


    public void addNewClient(ClientRequestHandler requestHandler) {
        Map<String, ClientRequestHandler> map =  clientMap.get(requestHandler.getNetwork());
        if (map == null) {
            map = new HashMap<String, ClientRequestHandler>();
        }
        map.put(requestHandler.getGateway(), requestHandler);
        System.out.println(map);
    }

    public void removeClient(ClientRequestHandler requestHandler) {
        Map<String, ClientRequestHandler> map = clientMap.get(requestHandler.getNetwork());
        ClientRequestHandler handler = map.get(requestHandler.getGateway());
        //map.put(requestHandler.getGateway(), null);
        handler = null;

    }

    public void postMessage(ClientRequestHandler requestHandler) {
        System.out.println("Forwarding the post to the registered Users");
        Map<String, ClientRequestHandler> map = clientMap.get(requestHandler.getNetwork());
        for (Map.Entry<String, ClientRequestHandler> entry : map.entrySet()) {
            ClientRequestHandler client = entry.getValue();
            if (client != null) {
                if (!client.isClosed())
                    client.sendNotification();
            }
        }
        //map.put(requestHandler.getGateway(), null);
    }

}
