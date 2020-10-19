import boto3
import requests
import datetime
import time
import cv2

# Connect to AWS
client=boto3.client('rekognition',
                    aws_access_key_id="Your access key id",
                    aws_secret_access_key="Yor secret access id",
                    aws_session_token="Your session token",
                    region_name='us-east-1')

# Loop for 5 hours to capture and compare
for hr in range(0, 5):
    # capture current image through webcam
    current_time = datetime.datetime.now().strftime("%d-%m-%y  %H-%M-%S ")
    print(current_time)
    cam = cv2.VideoCapture(0)
    for i in range(20):
        value, image = cam.read()
        if (i == 19):
            cv2.imwrite('images/' + current_time + '.jpg', image)
    del (cam)

    # uploading in AWS S3 Bucket
    clients3 = boto3.client('s3', region_name='us-east-1')
    clients3.upload_file("images/"+current_time+'.jpg', 'count-attendance', current_time+'.jpg')

    # open current image to compare
    with open(r'images/'+current_time+'.jpg','rb') as source_image:
        source_bytes = source_image.read()
    print(type(source_bytes))

    # comparing byte codes
    print("Recognition Service")
    response = client.detect_custom_labels(
        ProjectVersionArn='arn:aws:rekognition:us-east-1:906855307936:project/HourlyAttendanceCapturingSystem/version/HourlyAttendanceCapturingSystem.2020-10-10T19.06.48/1602337008460',
       
        Image={
            'Bytes':source_bytes

        },
       
    )

    print(response)
    # Not identified
    if not len(response['CustomLabels']):
        print('Person not identified')

    # Calls API to update the attendance
    else:
        str=response['CustomLabels'][0]['Name']
        url="https://zdjdrlb439.execute-api.us-east-1.amazonaws.com/test?rollNo="+str
        resp = requests.get(url)
        print(resp)

        # Sleeps for 1 hour
        time.sleep(3600)