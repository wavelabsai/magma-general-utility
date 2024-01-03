Orc8rNotificationService

Pre-requisties
====================================
sudo apt install openjdk-8-jdk-headless
sudo apt install maven

Build Procedure
=====================================

cd Orc8rNotificationService/
$ mvn clean -Dmaven.clean.failOnError=false compile package


Generated Jar file path
=====================================
After compile and package command is executed jar file is generated under target folder 

1. Orc8rNotificationService-1.0-SNAPSHOT.jar
2. Orc8rNotificationService-1.0-SNAPSHOT-jar-with-dependencies.jar


Delete the "Orc8rNotificationService-1.0-SNAPSHOT.jar" 
$ rm Orc8rNotificationService-1.0-SNAPSHOT.jar

Rename the "Orc8rNotificationService-1.0-SNAPSHOT-jar-with-dependencies.jar" to "Orc8rNotificationService-1.0-SNAPSHOT.jar"
$ mv Orc8rNotificationService-1.0-SNAPSHOT-jar-with-dependencies.jar Orc8rNotificationService-1.0-SNAPSHOT.jar

Executing Orc8rNotificationService Jar file path
================================================
$ java -jar Orc8rNotificationService-1.0-SNAPSHOT.jar 4442 4443

Testing Orc8rNotificationService Jar file path
================================================

Usage registering subscribers for receiving subscriber updates
==============================================================
java -cp <JarName> com.orc8r.NotificationService.test,TestNotificationSubscriberClient  <NotificationServerAddress> <PublisherPort>
java -cp Orc8rNotificationService-1.0-SNAPSHOT.jar com.orc8r.NotificationService.test.TestNotificationSubscriberClient localhost 4443

Usage for publishing subscriber change
======================================
java -cp <JarName> com.orc8r.NotificationService.test,TestNotificationSubscriberClient  <NotificationServerAddress> <PublisherPort>
java -cp Orc8rNotificationService-1.0-SNAPSHOT.jar com.orc8r.NotificationService.test.TestPlainNotificationClient localhost 4442




