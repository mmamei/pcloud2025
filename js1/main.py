
data = '''sensor1, 10
sensor2, 40
sensor3, 70
sensor1, 100'''

d = {}
for line in data.split('\n'):
    sensor, value = line.split(', ')
    if sensor not in d:
        d[sensor] = []
    d[sensor].append(int(value))

print('sensor1')
for v in d['sensor1']:
    print(v)

def media(d):
    v = []
    for sensor in d:
        v += d[sensor]
    return sum(v) / len(v)

print('media:', media(d))
