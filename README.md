<p align="center">
  <img src="https://user-images.githubusercontent.com/102455571/282228390-547fdde0-caf2-497e-bc40-0277cde82fea.png">
</p>
** 라즈베리파이 **
카메라, LTE 모듈 장착
- 0.5초마다 이미지를 촬영합니다.
- 오토인코더 모델을 사용해 벌을 감지합니다.
- 이미지에 컨투어를 적용해 개체 수를 예측합니다.
- 개체 수가 바뀌면 1)해당 프레임의 원본 이미지, 2)해당 프레임의 오토인코더 및 컨투어 적용 이미지, 3) 이전 프레임의 원본 이미지, 4) 이전 프레임의 오토인코더 및 컨투어 적용 이미지, 5) 해당 프레임의 개체 수, 6) 이전 프레임의 개체 수를 1개의 npy파일로 만들어 구글 드라이브에 업로드합니다.<br><br>

** 서버 **
- 라즈베리파이가 구글 드라이브에 업로드한 npy파일들을 다운로드 합니다.
- 4개의 이미지로 저장하고, 개체 수 정보는 txt파일에 저장합니다.
- 플라스크를 사용해 이미지들과 개체 수를 볼 수 있는 웹사이트를 구현했습니다. 검색 기능도 포함합니다.

**autoencoder**
- autoencoder.ipynb : 오토인코더 학습 코드
- autoencoder_16 : 인코더, 디코더 레이어 각각 2개, ephochs 50으로 학습한 오토인코더
- autoencoder_32 : 인코더, 디코더 레이어 각각 3개, ephochs 50으로 학습한 오토인코더
- autoencoder_64 : 인코더, 디코더 레이어 각각 4개, ephochs 50으로 학습한 오토인코더
- autoencoder3_200_32 : 인코더, 디코더 레이어 각각 3개, ephochs 200, batch size 32로 학습한 오토인코더
- autoencoder3_200_64 : 인코더, 디코더 레이어 각각 3개, ephochs 200, batch size 64로 학습한 오토인코더
- autoencoder3_200_128 : 인코더, 디코더 레이어 각각 3개, ephochs 200, batch size 128로 학습한 오토인코더

**client (raspberry pi)**
- client_capture.py : 이미지 촬영, 오토인코더 적용, 컨투어 적용, 개체 수 예측, 개체 수 변화 시 위에서 설명한 4개 이미지들과 2개 변수를 npy 파일로 저장
- client_uplaod.py : upload 폴더에 새로운 파일이 저장되면 구글 드라이브에 업로드
- shut_down.py : 버튼을 누르면 종료
- client.py : 위 3개 파일을 비 동기적으로 실행

**server**
- server.ipynb, server.py : 라즈베리파이가 구글 드라이브에 업로드한 파일들을 다운로드. 4개 이미지와 2개 변수로 나누어 저장

**flask (server)**
- flask_server.py : 서버에서 다운받은 이미지들을 웹사이트에서 볼 수 있게 하는 flask 코드

**images**
- 학습(original, mask)과 테스트(test)에 사용된 이미지들
