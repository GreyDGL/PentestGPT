FROM ubuntu:22.04

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        net-tools python3 python3-pip \
        curl gnupg nmap bandit locales \
        cloc sloccount less iputils-ping

# # Install Metasploit
# RUN curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > /tmp/msfinstall \
#     && chmod 755 /tmp/msfinstall \
#     && /tmp/msfinstall

# # [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# #  alternatively, this also helps avoid having to pull requirements from the internet every single time
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp
RUN pip3 install bandit trufflehog3

RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
