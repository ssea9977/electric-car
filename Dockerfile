FROM python:3.9.5

RUN pip3 install django bs4 requests selenium pyautogui datetime

WORKDIR /usr/src/app

COPY . .

WORKDIR ./electricCar
# manage.py를 실행할 수 있는 디렉토리로 이동합니다.

CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]
# 이동한 디렉토리에서 django를 가동시켜주는 코드를 작성합니다. 여기서 port는 80로 실행합니다. 

EXPOSE 80
# django 서버의 포트를 80로 지정하였으므로 Docker의 컨테이너 또한 80 포트를 열어줍니다.
