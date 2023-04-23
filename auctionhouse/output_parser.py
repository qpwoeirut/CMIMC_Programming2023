import json
with open("auctionhouse/outputs/243a4d77-8539-4ce3-924b-2a0c96abd3d4.json","r") as x:
    Data=json.load(x)
x=Data["history"]
mx = 0
clown = []
z = [0] * 101
p = [0] * 10
for item in x:
    for i in item:
        cnt = 0
        ind = 0
        loss = 0
        if len(i[2]) < 5:
            continue
        for j in i[2]:
            ind += 1
            if (ind == 7):
                break;
            if (ind > 4 and ind <= 7):
                z[j[0]] += 1
                break

            if j[1] == False:
                loss += 1
        p[loss] += 1
print("\n\n")
for count in z:
    print(count)
print("\n\n")
for count in p:
    print(count)