import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from sklearn.linear_model import LinearRegression

class HealthManager:
    def __init__(self):
        self.weight_records = []

    def record_weight(self):
        weight = float(input("体重をkg単位で入力してください: "))
        self.weight_records.append(weight)
        print(f"体重を記録しました: {weight} kg")

    def calculate_average_weight(self):
        if len(self.weight_records) == 0:
            print("体重の記録が見つかりません。")
            return
        average_weight = sum(self.weight_records) / len(self.weight_records)
        print(f"平均体重: {average_weight} kg")

    def display_weight_trend(self):
        if len(self.weight_records) < 2:
            print("体重の傾向を表示するためのデータが十分ではありません。")
            return
        # Create a linear interpolation of the weight records
        x = np.array(range(len(self.weight_records))).reshape(-1, 1)
        y = np.array(self.weight_records)
        model = LinearRegression()
        model.fit(x, y)
        y_pred = model.predict(x)

        slope = (y_pred[-1] - y_pred[0])
        if slope > 0:
            print("体重が増加しています。")
        elif slope < 0:
            print("体重が減少しています。")
        else:
            print("体重は安定しています。")

    def plot_weight_trend(self):
        # Create a linear interpolation of the weight records
        x = np.array(range(len(self.weight_records))).reshape(-1, 1)
        y = np.array(self.weight_records)
        model = LinearRegression()
        model.fit(x, y)
        y_pred = model.predict(x)
        
        plt.scatter(x, y, color='blue')
        plt.plot(x, y_pred, color='red')
        plt.title('体重の傾向')
        plt.xlabel('日数')
        plt.ylabel('体重 (kg)')
        plt.show()

# HealthManagerのインスタンスを作成
health_manager = HealthManager()

# 体重を記録
for _ in range(7):
    health_manager.record_weight()

# 平均体重を計算
health_manager.calculate_average_weight()

# 体重の傾向を表示
health_manager.display_weight_trend()

# 体重の傾向をグラフに表示
health_manager.plot_weight_trend()
