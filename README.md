# days-app

This is a basic python app.

with this you can mark the days and count the days on your journey towards something

the below is the structure of the project which helps in containerize the python app.

flask-nginx-app/
├── Dockerfile
├── requirements.txt
├── app.py
├── templates/
│   └── index.html
└── checked_days.json  (optional, this can be created automatically)

# for this just close the repo into your linix VM with docker in it.

# build the docker image 

docker build -t YOUR_DOCKER-HUB_USERNAME/days_checker:v1.0 .

# run the conatiner with that image

docker run -d --name=days_app -p 81:5000 YOUR_DOCKER-HUB_USERNAME/days_checker:v1.0

# then browse the app from your local with public ip of the ec2 instance

http://PUBLIC_IP_OF_EC2:81

# ###########################################################################################

OR 

# you can simply pull the image from my docker-hub then run it.

docker pull gowtham454/days_checker:v1.0

# then run it 

docker run -d --name=days_app -p 81:5000 gowtham454/days_checker:v1.0 

# Thank you.
