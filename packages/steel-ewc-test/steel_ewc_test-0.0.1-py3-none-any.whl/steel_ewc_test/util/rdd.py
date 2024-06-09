from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt


raw_data = pd.read_excel('../data/steel/TRain/Task1(拉速1.2)/板坯1_和/测试暴力.xlsx')
filter_columns = [ "castspeed_2","h10_ws_fix_ht_ext_2", "h10_ws_left_ht_ext_2", "h10_ws_los_ht_ext_2",
                      "h10_ws_right_ht_ext_2", "actual_gate_position_2", "castspeeddiff_2"]
X= raw_data[filter_columns]
Y= raw_data["mdleveldiff_2"]
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.005, random_state=42)

rfr_model = RandomForestRegressor(n_estimators=100)
rfr_model.fit(x_train, y_train)

y_pred = rfr_model.predict(x_test)

RMSE = np.sqrt(mean_squared_error(y_test,y_pred))
MAE = mean_absolute_error(y_test, y_pred)
R2 = r2_score(y_test,y_pred)

print("RMSE:",RMSE)
print("MAE:",MAE)
print("R2:",R2)

plt.figure(figsize=(12, 8), dpi=160)
font1 = {'family': 'Arial', 'weight': 'normal', 'size': 18}
prediction = np.asarray(y_pred)
observation = np.asfarray(y_test)
time_points = len(prediction)
t = np.arange(0, time_points)
plt.plot(t, prediction, label='prediction', color='black')
plt.plot(t, observation, label='observation', color='green')
plt.legend(prop=font1, loc='upper center', ncol=2)
plt.xlabel('Time (Second)', fontproperties='Times New Roman', fontsize=20)
plt.xticks(fontproperties='Arial', fontsize=16)
plt.ylabel('Value', fontproperties='Times New Roman', fontsize=20)
plt.yticks(fontproperties='Arial', fontsize=16)
plt.show()

