import pandas as pd

# 从CSV文件读取数据
data = pd.read_csv('data.csv')

# 执行基本分析
mean = data['column_name'].mean()
print(f"Mean: {mean}")