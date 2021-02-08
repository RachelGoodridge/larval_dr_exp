import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("exp2_data.xlsx")
setup = pd.read_excel("exp2_setup.xlsx")

for col in data.columns:
    if col != "time":
        total = max([int(setup[setup["well_num"]==col]["worm_num"]), max(data[col])])
        if total != 0:
            data[col] = data[col]/total

times = [i.strftime("%H:%M") for i in data["time"]]            

for col in data.columns:
    if col != "time":
        plt.plot(times, data[col])
plt.xlabel("Time")
plt.ylabel("Fraction Glowing")
