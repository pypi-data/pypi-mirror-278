import csv
import requests

def main(month, year, csv_url):
  """
  在CSV文件中查找指定月和年份的总访问量

  参数：
    month: 要查找的月份缩写
    year: 要查找的年份
    csv_url: CSV文件URL

  返回值：
    指定月和年份的总访问量，如果找不到则返回0
  """

  # 下载CSV文件内容
  response = requests.get(csv_url)
  csv_content = response.text

  total_visitors = 0
  # 使用 StringIO 类处理从URL下载的文本内容
  from io import StringIO
  csvfile = StringIO(csv_content)
  reader = csv.DictReader(csvfile)
  for row in reader:
      if row['Month (abbr)'] == month and row['Year'] == str(year):
        # Remove comma before converting to integer
        visitor_arrivals = int(row['Visitor Arrivals'].replace(",", ""))
        total_visitors += visitor_arrivals
  return total_visitors

# 获取用户输入的月份和年份
month = input("请输入要查找的月份缩写：")
year = int(input("请输入要查找的年份："))

# 设定CSV文件URL
csv_url = "https://public.tableau.com/views/3_1_Visitor_arrivals/CSV_1__2_3__3.csv?%3AshowVizHome=no&%E5%AF%BE%E8%B1%A1%E5%A4%96%EF%BC%88%E5%9B%BD%E3%83%BB%E5%9C%B0%E5%9F%9F%EF%BC%89=%E7%9C%9F&%E5%B9%B4%20=2019%2C2020%2C2021%2C2022%2C2023%2C2024&%E6%9A%AB%E5%AE%9A%E5%80%A4%E3%83%95%E3%83%A9%E3%82%B0=%E7%A2%BA%E5%AE%9A%E5%80%A4%2C%E6%9A%AB%E5%AE%9A%E5%80%A4"

# 计算总访问量
total_visitors = total_visitors(month, year, csv_url)

# 打印结果
if total_visitors > 0:
  print(f"{year}年{month}月的总访问量为：{total_visitors}")
else:
  print(f"未找到{year}年{month}月的访问量数据")

if __name__ == '__main__':
    main()