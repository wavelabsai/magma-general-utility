RUN apt-get update && apt-get -y install vim
RUN wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/6.5.0/openapi-generator-cli-6.5.0.jar -O openapi-generator-cli.jar
RUN wget https://download.java.net/java/GA/jdk13.0.1/cec27d702aa74d5a8630c65ae61e4305/9/GPL/openjdk-13.0.1_linux-x64_bin.tar.gz
RUN tar -xvf openjdk-13.0.1_linux-x64_bin.tar.gz
RUN mv jdk-13.0.1 /opt/
ENV JAVA_HOME='/opt/jdk-13.0.1'
ENV PATH="$JAVA_HOME/bin:$PATH"
RUN wget https://mirrors.estointernet.in/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz
RUN tar -xvf apache-maven-3.6.3-bin.tar.gz
RUN mv apache-maven-3.6.3 /opt/
ENV M2_HOME='/opt/apache-maven-3.6.3'
ENV PATH="$M2_HOME/bin:$PATH"

RUN npm install -g @apidevtools/swagger-cli
