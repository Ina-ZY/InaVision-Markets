import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 设置字体
plt.rcParams['axes.unicode_minus'] = False

# 定义加密货币名称与对应的 yfinance ticker
crypto_dict = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Binance Coin (BNB)": "BNB-USD",
    "XRP (XRP)": "XRP-USD",
    "Cardano (ADA)": "ADA-USD",
    "Dogecoin (DOGE)": "DOGE-USD",
    "Solana (SOL)": "SOL-USD",
    "STETH (STETH)": "STETH-USD"
}

# 创建2×4的子图网格（8个子图）
fig, axs = plt.subplots(2, 4, figsize=(20, 10))
axs = axs.flatten()

# 指定要显示的年份（x轴刻度）
years = pd.to_datetime(['2020-01-01', '2021-01-01', '2022-01-01', '2023-01-01', '2024-01-01', '2025-01-01'])
year_labels = ['2020', '2021', '2022', '2023', '2024', '2025']

# 存储最高和次高点的信息
peak_info = {}

# 循环下载数据并绘图
for ax, (name, ticker) in zip(axs, crypto_dict.items()):
    try:
        data = yf.download(ticker, period='5y', interval='1d', progress=False)
        
        # 对于 STETH，仅显示2021年之后的数据
        if ticker == "STETH-USD":
            data = data[data.index >= '2021-01-01']
        
        if data.empty:
            ax.text(0.5, 0.5, f'No data for\n{name}', 
                    horizontalalignment='center', verticalalignment='center', fontsize=12)
        else:
            ax.plot(data.index, data['Close'], label=name, linewidth=2)
            
            # 计算最高和次高点
            sorted_prices = data['Close'].sort_values(ascending=False)
            highest_price = sorted_prices.iloc[0]
            second_highest_price = sorted_prices.iloc[1]
            highest_date = sorted_prices.index[0]
            second_highest_date = sorted_prices.index[1]

            # 标注最高点和次高点
            ax.scatter(highest_date, highest_price, color='red', marker='o', s=80, label="Highest")
            ax.scatter(second_highest_date, second_highest_price, color='blue', marker='o', s=80, label="Second Highest")

            # 显示标注
            ax.text(highest_date, highest_price, f"{highest_price:.2f}", fontsize=10, color='red', verticalalignment='bottom')
            ax.text(second_highest_date, second_highest_price, f"{second_highest_price:.2f}", fontsize=10, color='blue', verticalalignment='bottom')

            # 记录信息（包含月份）
            peak_info[name] = {
                "Highest Price": highest_price,
                "Highest Date": highest_date.strftime("%Y-%m"),
                "Second Highest Price": second_highest_price,
                "Second Highest Date": second_highest_date.strftime("%Y-%m")
            }
            
            ax.legend(loc='upper right', fontsize=10)
    
    except Exception as e:
        ax.text(0.5, 0.5, f'Error for\n{name}', 
                horizontalalignment='center', verticalalignment='center', fontsize=12)
    
    # 设置 x 轴仅显示指定年份
    ax.set_xticks(years)
    ax.set_xticklabels(year_labels)
    
    # 移除背景网格
    ax.grid(False)
    
    # 设置刻度参数
    ax.tick_params(axis='both', labelsize=10, direction='in', length=4, width=1.5)
    
    # 加粗四周边框
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)

# 设置seaborn样式为白色背景
sns.set_style('white')

# 为整体图形添加大标题
plt.suptitle('Cryptocurrency Prices (Last 5 Years)', fontsize=20, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("crypto_prices.svg", format="svg", dpi=500)
plt.show()

# 打印最高和次高价格信息（包含月份）
peak_info_df = pd.DataFrame(peak_info).T
