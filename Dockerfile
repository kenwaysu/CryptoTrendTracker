# 使用 Python 3 的官方基本映像作為基礎映像
FROM python:3.10.8-alpine

# 設置工作目錄
WORKDIR /app

# 將當前目錄中的所有文件複製到容器的 /app 目錄中
COPY . /app

# 安裝 Python 依賴項
RUN pip install -r requirements.txt

# 定義執行應用程序的命令
CMD ["python", "app.py"]
