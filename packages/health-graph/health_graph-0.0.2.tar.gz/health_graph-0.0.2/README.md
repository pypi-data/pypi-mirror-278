# 健康管理ソフト
直近一週間分の体重を入力すると、平均体重と体重の傾向を算出します。<br>
傾向は線形補間または線形回帰により算出されます。<br>
ソフトを起動する前に以下のコマンドでライブラリをインストールしてください。
```python
pip install numpy
pip install scipy
pip install matplotlib.pyplot
pip install scikit-learn
```