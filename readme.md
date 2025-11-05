# Online Judge API

> API hệ thống chấm code tự động cho các trang web lập trình thi đấu, sử dụng FastAPI, PostgreSQL và Isolate (IOI Sandbox)

## 📋 Mục lục

- [Giới thiệu](#giới-thiệu)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
  - [1. Cài đặt Isolate](#1-cài-đặt-isolate)
  - [2. Cài đặt các ngôn ngữ lập trình](#2-cài-đặt-các-ngôn-ngữ-lập-trình)
  - [3. Cài đặt PostgreSQL](#3-cài-đặt-postgresql)
  - [4. Cài đặt Python và dependencies](#4-cài-đặt-python-và-dependencies)
  - [5. Cấu hình môi trường](#5-cấu-hình-môi-trường)
- [Chạy ứng dụng](#chạy-ứng-dụng)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🎯 Giới thiệu

Online Judge API là một hệ thống backend mạnh mẽ cho phép:
- Thực thi code an toàn trong môi trường sandbox (Isolate)
- Chấm điểm tự động với test cases
- Hỗ trợ nhiều ngôn ngữ lập trình (C, C++, Python, Java, etc.)
- Quản lý bài tập và submissions
- Giao diện frontend đơn giản với HTML/CSS/JS

## 🛠 Công nghệ sử dụng

- **Backend Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Sandbox**: Isolate (IOI Sandbox)
- **Frontend**: HTML, CSS, JavaScript
- **ORM**: SQLAlchemy

## 💻 Yêu cầu hệ thống

- **OS**: Linux (Ubuntu 20.04+ hoặc Debian-based distros khuyến nghị)
- **Python**: 3.8+
- **PostgreSQL**: 12+
- **RAM**: Tối thiểu 2GB
- **Disk**: Tối thiểu 5GB trống
- **Permissions**: Root access để cài đặt Isolate

## 🚀 Cài đặt

### 1. Cài đặt Isolate

Isolate là sandbox được sử dụng trong các kỳ thi IOI (International Olympiad in Informatics) để thực thi code an toàn.

#### Bước 1.1: Cài đặt dependencies

```bash
# Update package list
sudo apt update

# Cài đặt các công cụ cần thiết
sudo apt install -y build-essential git libcap-dev pkg-config asciidoc
```

#### Bước 1.2: Clone và build Isolate

```bash
# Clone repository
cd /tmp
git clone https://github.com/ioi/isolate.git
cd isolate

# Build isolate
make isolate

# Cài đặt (yêu cầu quyền root)
sudo make install

# Verify installation
isolate --version
```

#### Bước 1.3: Cấu hình Isolate

```bash
# Tạo sandbox directories
sudo isolate --init

# Set permissions (quan trọng để FastAPI có thể sử dụng)
sudo chmod 755 /var/local/lib/isolate/
```

#### Bước 1.4: Test Isolate

```bash
# Tạo sandbox
isolate --init

# Tạo file test
echo 'print("Hello from Isolate!")' > /tmp/test.py

# Copy vào sandbox (giả sử sandbox ID = 0)
cp /tmp/test.py /var/local/lib/isolate/0/box/

# Chạy code
isolate --run -- /usr/bin/python3 test.py

# Cleanup
isolate --cleanup
```

### 2. Cài đặt các ngôn ngữ lập trình

#### 2.1. C & C++

```bash
# GCC/G++ compiler
sudo apt install -y gcc g++

# Verify
gcc --version
g++ --version
```

#### 2.2. Python

```bash
# Python 3 (thường đã cài sẵn trên Ubuntu)
sudo apt install -y python3 python3-pip

# Verify
python3 --version
```

#### 2.3. Java

```bash
# OpenJDK
sudo apt install -y openjdk-11-jdk openjdk-11-jre

# Verify
java -version
javac -version
```

#### 2.4. Node.js (JavaScript)

```bash
# Node.js và npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify
node --version
npm --version
```

### 3. Cài đặt PostgreSQL

```bash
# Cài đặt PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Tạo database và user
sudo -u postgres psql

# Trong psql prompt:
```

```sql
CREATE DATABASE online_judge;
CREATE USER postgres WITH PASSWORD 'root';
GRANT ALL PRIVILEGES ON DATABASE online_judge TO postgres;
\q
```

### 4. Cài đặt Python và dependencies

```bash
# Clone repository
git clone https://github.com/Zaphong11/OnlineJudgeApi.git
cd OnlineJudgeApi

# Tạo virtual environment (khuyến nghị)
python3 -m venv venv
source venv/bin/activate

# Cài đặt requirements
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Cấu hình môi trường

#### Bước 5.1: Tạo file `.env`

```bash
# Tạo file .env trong thư mục root của project
touch .env
```

#### Bước 5.2: Thêm cấu hình vào `.env`

```properties
# Database Configuration
DATABASE_URL=postgresql://postgres:root@localhost:5432/online_judge
```

## 🎮 Chạy ứng dụng

### Chạy Backend (FastAPI)

```bash
# Activate virtual environment (nếu dùng)
source venv/bin/activate

# Chạy với Uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Hoặc nếu file chính có tên khác:
# uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Truy cập ứng dụng

- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Frontend**: `public/index.html`

## 📁 Cấu trúc thư mục

```
OnlineJudgeApi/
├── main.py                 # Entry point của FastAPI
├── app.py                  # Có thể là entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (không commit)
├── .env.example           # Template cho .env
├── .gitignore
├── README.md
│
├── models/                 # Database models
│   ├── __init__.py
│   ├── problem.py
│   ├── submission.py
│   └── user.py
│
├── routes/                 # API endpoints
│   ├── __init__.py
│   ├── problems.py
│   ├── submissions.py
│   └── users.py
│
├── services/               # Business logic
│   ├── __init__.py
│   ├── judge.py           # Isolate integration
│   └── compiler.py
│
├── database/               # Database configuration
│   ├── __init__.py
│   └── connection.py
│
├── schemas/                # Pydantic schemas
│   ├── __init__.py
│   └── submission.py
│
└── public/                 # Frontend files
    ├── index.html
    ├── css/
    │   └── style.css
    ├── js/
    │   ├── main.js
    │   └── api.js
    └── assets/
        └── images/
```

## 📚 API Documentation

### Endpoints chính

#### 1. Submit Code

```http
POST /api/submit
Content-Type: application/json

{
  "language": "python",
  "source_code": "print('Hello World')",
  "problem_id": 1,
  "test_cases": [
    {"input": "", "expected_output": "Hello World\n"}
  ]
}
```

#### 2. Get results

```http
GET /api/results/{submission_id}
```

## 🔧 Troubleshooting

### Lỗi thường gặp

#### 1. Isolate: Permission denied

```bash
# Solution: Chạy với sudo hoặc cấu hình capabilities
sudo setcap cap_sys_admin+ep /usr/local/bin/isolate
```

#### 2. Database connection error

```bash
# Kiểm tra PostgreSQL đang chạy
sudo systemctl status postgresql

# Kiểm tra credentials trong .env
# Đảm bảo database đã được tạo
```

#### 3. Module not found

```bash
# Activate virtual environment
source venv/bin/activate

# Cài lại dependencies
pip install -r requirements.txt
```

#### 4. Port already in use

```bash
# Tìm process đang dùng port 8000
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>

# Hoặc dùng port khác
uvicorn main:app --port 8001
```

#### 5. Isolate không tạo được sandbox

```bash
# Kiểm tra cgroups
mount | grep cgroup

# Cleanup các sandbox cũ
sudo isolate --cleanup

# Init lại sandbox
sudo isolate --init
```

### Debug mode

Để debug chi tiết hơn:

```bash
# Chạy với log level debug
uvicorn main:app --reload --log-level debug

# Kiểm tra logs của Isolate
isolate --verbose --run -- /usr/bin/python3 test.py
```

## 🔐 Security Notes

- **Không commit file `.env`** vào git
- Cấu hình firewall cho production:
  ```bash
  sudo ufw allow 8000/tcp
  ```
- Sử dụng HTTPS trong production
- Giới hạn resource usage trong Isolate để tránh DOS

## 📝 License

[MIT License](LICENSE)

## 👨‍💻 Contributors

- Zaphong11 - Initial work

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For issues and questions, please open an issue on GitHub. Or contact me by email: phongnguyengia82@gmail.com

---

**Happy Coding! 🎉**