# opencv 라이브러리
import cv2
# numpy 리이브러리
import numpy as np
# 현재 시간 출력을 위한 datetime 라이브러리
from datetime import datetime

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

isDragging = False                      
x0, y0, w, h = -1,-1,-1,-1             
blue, green, red = (255,0,0), (0,255,0), (0,0,255)          

################################################################################## 
# 트랙바
def onChange(x):
    pass
################################################################################## 
################################################################################## 
#마우스 클릭 이벤트 핸들러
def Mouse_ROI(event,x,y,flags,param):     
    global isDragging, x0, y0, img      
    if event == cv2.EVENT_LBUTTONDOWN:  
        isDragging = True
        x0 = x
        y0 = y
    elif event == cv2.EVENT_MOUSEMOVE:  
        if isDragging:                  
            cv2.rectangle(camera, (x0, y0), (x, y), blue, 2)
            cv2.imshow('camera', camera)
    elif event == cv2.EVENT_LBUTTONUP:  
        if isDragging:                  
            isDragging = False          
            w = x - x0                  
            h = y - y0                  
            if w > 0 and h > 0:         
                cv2.rectangle(camera, (x0, y0), (x, y), blue, 2) 
                cv2.imshow('camera', camera)
                roi = camera[y0:y0+h, x0:x0+w]
                cv2.moveWindow('cropped', 0, 0)
                cv2.imshow('cropped', roi)

                faces = face_cascade.detectMultiScale(camera, 1.3, 5)
                for (x,y,w,h) in faces:
                    
                    now = datetime.now()
                    print("-----------------------------------------------------")
                    print("측정 날짜 시각 : " + str(now))
                    print("마스크 미착용 의심 사람 위치 : ",faces)
                    print("-----------------------------------------------------")
                    
                    cv2.rectangle(camera,(x,y),(x+w,y+h),green,2)
                    cv2.imshow('cropped', roi)
                    print("이미지가 저장되었습니다.")
                    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    cv2.imwrite('저장위치'+str(now)+'.jpg',roi)                   
            else:
                print("좌측 상단에서 우측 하단으로 영역을 드래그 하세요.")
################################################################################## 
################################################################################## 
# 실시간 웹캡
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#재생할 파일의 높이 얻기
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#재생할 파일의 프레임 레이트 얻기
fourcc = cv2.VideoWriter_fourcc(*'XVID')
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = '저장위치'+str(now)+'.avi'
out = cv2.VideoWriter(filename, fourcc, 10.0, (int(width), int(height)))

##################################################################################
# 트랙바
cv2.namedWindow('camera')
cv2.createTrackbar('NIGHT MODE', 'camera', 0, 1, onChange)
##################################################################################
if cap.isOpened() :
    while True:
        ret, camera = cap.read()
        ret, night_camera = cap.read()
        faces = face_cascade.detectMultiScale(camera, 1.3, 5)

        if ret:
################################################################################## 
# 어두운곳 얼굴 인식
##################################################################################
# 노말라이즈 정규화
            night_camera = cv2.normalize(night_camera, None, 0, 255, cv2.NORM_MINMAX)
##################################################################################
# 이퀄라이즈 평탄화
            img_yuv = cv2.cvtColor(night_camera, cv2.COLOR_BGR2YUV)
            img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
            night_camera = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
##################################################################################
# 얼굴 인식
            for (x,y,w,h) in faces:
                cv2.rectangle(night_camera,(x,y),(x+w,y+h),red,2)
                cv2.putText(night_camera,"No mask",(x-10,y-10),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,255))
            cv2.setMouseCallback('night_camera', Mouse_ROI) 
################################################################################## 
# 얼굴인식
##################################################################################
# 트랙바
            s = cv2.getTrackbarPos('NIGHT MODE','camera')
            if s == 0:
                pass
            else:
                camera = night_camera
##################################################################################
# 노말라이즈 정규화
            camera = cv2.normalize(camera, None, 0, 255, cv2.NORM_MINMAX)
##################################################################################
# 얼굴 인식
            for (x,y,w,h) in faces:
                cv2.rectangle(camera,(x,y),(x+w,y+h),red,2)
                cv2.putText(camera,"No mask",(x-10,y-10),cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,255)) 
            out.write(camera)
            cv2.imshow('camera',camera)
            cv2.setMouseCallback('camera', Mouse_ROI)
################################################################################## 
            if cv2.waitKey(1) != -1:
                break
        else:
            print('no camera!')
            break
else:
    print('no camera!')
################################################################################## 
cv2.waitKey()
cap.release()
out.release()
print(str(now)+" 웹캠 영상이 저장되었습니다.")
cv2.destroyAllWindows()
