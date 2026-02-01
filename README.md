# Discord Faucet 脚本服务器部署指南

## 方法一：使用 systemd（推荐）

### 1. 上传代码到服务器
```bash
# 在本地执行，将代码上传到服务器
scp -r /Users/dongmac/hashgame user@your-server:/home/user/hashgame
```

### 2. 在服务器上安装依赖
```bash
ssh user@your-server

cd /home/user/hashgame
python3 -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv
```

### 3. 确认 .env 配置
```bash
cat .env  # 确认配置正确
```

### 4. 安装 systemd 服务
```bash
# 复制服务文件
sudo cp discord-faucet.service /etc/systemd/system/

# 重新加载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start discord-faucet

# 设置开机自启
sudo systemctl enable discord-faucet
```

### 5. 查看运行状态
```bash
# 查看服务状态
sudo systemctl status discord-faucet

# 查看实时日志
sudo journalctl -u discord-faucet -f
```

### 6. 常用命令
```bash
sudo systemctl stop discord-faucet    # 停止
sudo systemctl restart discord-faucet # 重启
sudo systemctl disable discord-faucet # 取消开机自启
```

---

## 方法二：使用 screen（临时方案）

```bash
# 安装 screen
sudo apt install screen  # Ubuntu/Debian
# 或
sudo yum install screen  # CentOS

# 创建新会话
screen -S faucet

# 运行脚本
cd /home/user/hashgame
source .venv/bin/activate
python3 main.py

# 按 Ctrl+A 然后按 D 分离会话（脚本继续后台运行）

# 重新连接会话
screen -r faucet
```

---

## 方法三：使用 Docker

```bash
# 构建镜像
docker build -t discord-faucet .

# 运行容器
docker run -d --name faucet --restart=always discord-faucet
```
