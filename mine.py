import threading
import subprocess
import socket
import json
import datetime

INTERVAL = 1
THRESHOLD = 70

claymore_string = './claymore/ethdcrminer64 -epool eu1.ethermine.org:4444 -ewal 0x1C06239D043386275f219a5f307366b7c48709B2.dwight -epsw x -wd 0 -mode 1 -tt 65,62,65 -fanmin 50,50,50'

def run_process(cmd):
    subprocess.Popen(cmd, shell=True)

def monitor(reached):

    # query the status of claymore
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 3333)
    sock.connect(server_address)
    command = "{\"id\":0,\"jsonrpc\":\"2.0\",\"method\":\"miner_getstat1\"}"
    sock.sendall(command.encode('UTF-8'))
    data = sock.recv(1200).decode('UTF-8')
    data = json.loads(data)

    hashrate = sum([int(x) for x in data['result'][3].split(';')]) / 1000
    print('Effective hashrate: %s' % hashrate)

    gpu_stats = []
    values = [int(x) for x in data['result'][6].split(';')]
    temps = []
    fan_speeds = []
    for i in range(len(values)):
        if i % 2 == 0:
            temps.append(values[i])
        else:
            fan_speeds.append(values[i])

    for i in range(len(temps)):
        stat = {}
        stat['temp'] = temps[i]
        stat['fan_speed'] = fan_speeds[i]
        gpu_stats.append(stat)

    for index, value in enumerate(gpu_stats):
        print('GPU %s: temp = %s, fan = %s' % (index, value['temp'], value['fan_speed']))

    print('')  # newline

    if hashrate < THRESHOLD and reached:
        open('crash.log', 'a').write('Failed at %s \n' % str(datetime.datetime.now()))
        run_process('sudo shutdown now')

    if hashrate >= THRESHOLD:
        reached = True

    threading.Timer(INTERVAL, monitor, args=(reached,)).start()

# spawn a mining process
print('Initializing Claymore\'s miner...')
open('crash.log', 'a').write('Started mining at %s \n' % str(datetime.datetime.now()))
p = subprocess.Popen(claymore_string, shell=True, stdout=open('/dev/null', 'a'))

threading.Timer(20, monitor, args=(False,)).start()

