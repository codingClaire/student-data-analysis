import pandas as pd
import numpy  as np
import seaborn as sns
import matplotlib.pyplot as plt

fig, axes =plt.subplots(7, 1)
timetable=["开馆前","第一节","第二节","第三节","第四节",
           "中午","第五节","第六节","第七节","第八节","第九节",
           "晚上","第十节","第十节","第十一节","闭馆后"]
data =pd.Series(np.random.rand(16), index=timetable)
data.plot.bar(ax=axes[0], color='k', alpha=0.7)
data.plot.bar(ax=axes[1], color='k', alpha=0.7)
data.plot.bar(ax=axes[2], color='k', alpha=0.7)
data.plot.bar(ax=axes[3], color='k', alpha=0.7)
data.plot.bar(ax=axes[4], color='k', alpha=0.7)
data.plot.bar(ax=axes[5], color='k', alpha=0.7)
data.plot.bar(ax=axes[6], color='k', alpha=0.7)
plt.show()
plt.savefig("A.png")
plt.clf()