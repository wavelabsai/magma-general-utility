package com.orc8r.NotificationService.Server;

public interface NotificationServerInterface extends Runnable{
    public void init();
    public void bind();

    public void listen();

    public void accept();

    public void addNotificationClient(NotificationClients clients);


}
