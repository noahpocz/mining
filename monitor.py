from flask import Flask, request
import ouimeaux.environment as e
import threading

app = Flask(__name__)

env = e.Environment()
env.start()
env.discover(seconds=5)
switch = env.get_switch('Miner Switch')


class Counter:

    def __init__(self):
        self.count = 0
        self.mining = False

        self.prime()

    def power_cycle(self):
        print('shut down')
        switch.off()

        def on():
            switch.on()
            self.mining = False

        threading.Timer(5, on)

    def prime(self):
        threading.Timer(1, self.increment).start()

    def increment(self):
        self.count += 1

        if self.count > 10 and self.mining:
            self.power_cycle()

        self.prime()

    def reset(self):
        self.count = 0
        self.mining = True

        self.prime()


counter = Counter()


@app.route('/', methods=['POST'])
def declare_hashrate():

    data = request.json

    try:
        hashrate = float(data['hashrate'])
        threshold = float(data['threshold'])

        if hashrate < threshold:
            counter.power_cycle()

        else:
            print('reset')
            counter.reset()

    except:
        print('Invalid message!')

    return 'nice'


if __name__ == "__main__":
    app.run()
