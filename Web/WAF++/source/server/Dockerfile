FROM ubuntu:18.04

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN useradd -p "M.hkK9LJs8uGU" mote  #Mote_have_fun!

RUN set -ex \
  && DEBIAN_FRONTEND=noninteractive apt-get update \ 
  && apt-get install sudo=1.8.21p2-3ubuntu1 \
  && apt-get install --allow-unauthenticated -y openssh-server

RUN echo 'mote ALL=(ALL,!root) ALL' >> /etc/sudoers


EXPOSE 22

COPY setup.sh /root/setup.sh
CMD ["sh","/root/setup.sh"]

