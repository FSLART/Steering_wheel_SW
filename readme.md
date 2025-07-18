# Steering-Wheel-LART

## Login Armbian
```
User: root
Password: root
```

---

## Colocar a interface de CAN a funcionar num Raspberry Pi/BananaPI

### 1. Fazer as conexões físicas

O pinout para ligar MCP2515 a um Raspberry Pi Zero:

![Raspberry Pi Image](https://forums.raspberrypi.com/download/file.php?id=13939&sid=9352ccfb77f2a6f527bc6fe32d9c964e)

### 2. Configurações no sistema

1. Atualizar o sistema:
   ```bash
   sudo apt update -y && sudo apt upgrade -y
   ```

2. Desativar serviços não essenciais (Reativar caso seja necessário fazer debug a problemas de sistema):
   ```bash
   sudo systemctl disable armbian-zram-config.service  # Desativa a configuração de zram do Armbian
   sudo systemctl disable systemd-random-seed.service  # Desativa a semente aleatória do systemd
   sudo systemctl disable rsyslog.service  # Desativa o logging do sistema
   sudo systemctl disable e2scrub_reap.service  # Desativa a limpeza do e2scrub
   sudo systemctl mask armbian-zram-config.service  # Mascara a configuração de zram do Armbian
   sudo systemctl mask systemd-random-seed.service  # Mascara a semente aleatória do systemd
   sudo systemctl mask armbian-ramlog.service  # Mascara o logging em RAM do Armbian
   sudo systemctl disable systemd-timesyncd.service
   ```

3. Desligar Servidor DNS e Configurar Estáticos (Resolução de Nomes):

   ```bash
   sudo systemctl disable systemd-resolved.service  # Desativa a resolução de nomes do systemd
   sudo nano /etc/resolv.conf
   ```
   - Adicionar ao ficheiro as seguintes linhas:
     ```ini
     nameserver 8.8.8.8
     nameserver 1.1.1.1
4. Atrasar arranque do serviço `systemd-logind`:
      ```bash
      sudo systemctl edit systemd-logind.service
      ```
      - Adicionar o seguinte texto no espaço aberto entre comentários:
        ```ini
        [Service]
        ExecStartPre=/bin/sleep 1
        ```
5. Configurar o arranque automático do user root e arranque automático do Xorg (com a interface do volante):
   ```bash
   sudo mkdir -p /etc/systemd/system/getty@tty1.service.d/
   sudo nano /etc/systemd/system/getty@tty1.service.d/override.conf
   ```
   - Adicionar ao ficheiro as seguintes linhas:
     ```ini
     [Service]
     ExecStart=
     ExecStart=-/sbin/agetty --autologin root --noclear %I $TERM
     ```
   - Executar os seguintes comandos:
     ```bash
     sudo systemctl daemon-reexec
     sudo systemctl restart getty@tty1.service
     sudo reboot
     ```
   - Verificar que está tudo ok após o reboot.

6. Instalar o pacote `can-utils`:
   ```bash
   sudo apt install can-utils
   ```

7. Reiniciar o sistema:
   ```bash
   sudo reboot
   ```

8. Configurar a interface CAN:
   ```bash
   sudo ip link set can0 up type can bitrate 1000000
   ```

9.  Verificar se a interface se encontra a funcionar. Deve ter o nome algo similar a `can0` ou `slcan0`:
   ```bash
   ip a
   ```

10. Testar a interface:
    - Enviar uma mensagem de teste:
      ```bash
      cansend can0 MENSAGEM
      ```
    - Fazer dump da interface:
      ```bash
      candump can0
      ```

---

## Ambiente Python & Apresentação Gráfica

Caso o sistema se encontre bem configurado, para arrancar com a interface gráfica do volante, apenas será necessário correr o comando:
```bash
startx
```

### 1º Setup do Ambiente Python

1. Instalar dependências necessárias:
   ```bash
   sudo apt install xserver-xorg xinit openbox python3 python3-pip python3-tk customtkinter
   ```

2. Clonar o repositório:
   ```bash
   sudo git clone https://github.com/pontefrancisco/Steering-Wheel-LART /root/Steering-Wheel-LART
   ```

3. Navegar até ao repositório:
   ```bash
   cd ~/Steering-Wheel-LART
   ```

4. Criar um ambiente virtual Python:
   ```bash
   python3 -m venv venv
   ```

5. Ativar o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```

6. Instalar as dependências do projeto:
   ```bash
   pip3 install -r requirements.txt
   ```

7. Configurar o arranque automático do script ao abrir a interface gráfica:
   ```bash
   sudo nano ~/.xinitrc
   ```
   - Adicionar ao ficheiro as seguintes linhas:
     ```bash
     openbox &
     source ~/Steering-Wheel-LART/venv/bin/activate
     export DISPLAY=:0
     echo $DISPLAY
     python3 ~/Steering-Wheel-LART/interface.py
     ```

8. Arrancar com a interface:
   ```bash
   startx

## Setup Após a Primeira Vez

Caso o sistema já tenha sido configurado previamente, basta seguir os passos abaixo para iniciar o ambiente:

1. Ativar o ambiente virtual Python:
   ```bash
   source ~/Steering-Wheel-LART/venv/bin/activate
   ```

2. Navegar para o diretório do projeto:
   ```bash
   cd ~/Steering-Wheel-LART
   ```

3. Iniciar a interface gráfica:
   ```bash
   startx
   ```





   