import cv2
import pymysql.cursors

cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def countFace():
    dem = 0
    conn = pymysql.connect(host='localhost',
                        user='root',
                        password='chuanh255',                             
                        db='Recognition',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute("select * from  People")
    for i in cursor:
        dem = dem+1
    conn.commit()
    conn.close()
    return dem

def insertData(name, age, gender):
    conn = pymysql.connect(host='localhost',
                        user='root',
                        password='chuanh255',                             
                        db='Recognition',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
    
    sql = "INSERT into People(name, age, gender) values(%s,%s,%s)"
    cursor = conn.cursor()
    cursor.execute(sql,(name,age,gender))
    conn.commit()
    conn.close()
    
name = input("Moi nhap ten : ")
age = int(input("Moi nhap tuoi : "))
gender = input("Moi nhap gioi tinh : ")
insertData(name, age, gender)
id = countFace()
sampleNum = 0
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('frame', img)
        sampleNum = sampleNum + 1
        cv2.imwrite("dataSet/user." + str(id) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    if sampleNum > 20:
        break
cam.release()
cv2.destroyAllWindows()

