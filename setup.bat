@echo off
REM 创建并激活虚拟环境
python -m venv venv
call venv\Scripts\activate

REM 升级pip
python -m pip install --upgrade pip

REM 安装依赖库
pip install -r requirements.txt

echo Envirement Set up Successfully!
pause
