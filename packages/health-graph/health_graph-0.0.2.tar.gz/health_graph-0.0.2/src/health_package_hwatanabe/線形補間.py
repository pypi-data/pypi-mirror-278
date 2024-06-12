import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

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
        x = np.arange(len(self.weight_records))
        y = np.array(self.weight_records)
        f = interpolate.interp1d(x, y)
        xnew = np.arange(0, len(self.weight_records)-1, 0.1)
        ynew = f(xnew)
        # Calculate the slope of the interpolated line
        slope = (ynew[-1] - ynew[0]) / (xnew[-1] - xnew[0])
        if slope > 0:
            print("体重が増加しています。")
        elif slope < 0:
            print("体重が減少しています。")
        else:
            print("体重は安定しています。")

    def plot_weight_trend(self):
        # Create a linear interpolation of the weight records
        x = np.arange(len(self.weight_records))
        y = np.array(self.weight_records)
        f = interpolate.interp1d(x, y)
        xnew = np.arange(0, len(self.weight_records)-1, 0.1)
        ynew = f(xnew)
        # Plot the interpolated line
        plt.plot(xnew, ynew)
        plt.title('体重の傾向')
        plt.xlabel('日数')
        plt.ylabel('体重 (kg)')
        plt.show()

# HealthManagerのインスタンスを作成
health_manager = HealthManager()

# 体重を記録
for _ in range(3):
    health_manager.record_weight()

# 平均体重を計算
health_manager.calculate_average_weight()

# 体重の傾向を表示
health_manager.display_weight_trend()

# 体重の傾向をグラフに表示
health_manager.plot_weight_trend()
