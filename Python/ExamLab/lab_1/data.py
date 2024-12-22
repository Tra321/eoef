# 数据的批量输入、转换、统计操作（个数、均值、排序、最大值、最小值、中位数等）、随机数等
import numpy as np


def data_operations():
    # 批量输入数据
    print("请输入数据，每个数字用空格分隔，按回车结束：")
    data = list(map(float, input().split()))

    # 基本统计操作
    count = len(data)  # 个数
    mean_value = np.mean(data)  # 均值
    sorted_data = sorted(data)  # 排序
    max_value = max(data)  # 最大值
    min_value = min(data)  # 最小值
    median = np.median(data)  # 中位数

    # 输出结果
    print(f"\n统计结果:")
    print(f"数据个数: {count}")
    print("平均值: {:.2f}".format(mean_value))
    print(f"排序后: {sorted_data}")
    print("最大值：{}".format(max_value))
    print(f"最小值: {min_value}")
    print(f"中位数: {median}")

    # 生成随机数示例
    random_numbers = np.random.randint(1, 100, size=5)  # 生成5个1-100之间的随机整数
    print(f"\n随机生成的5个数: {random_numbers}")


if __name__ == "__main__":
    data_operations()
