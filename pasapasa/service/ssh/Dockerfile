FROM ubuntu:latest
RUN apt update && apt install -y openssh-server

# Create user
RUN useradd -m shaktale && echo "shaktale:fortrash" | chpasswd

# Configure SSH
RUN mkdir /var/run/sshd

# Start SSH server
CMD ["/usr/sbin/sshd", "-D"]