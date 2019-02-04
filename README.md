# MM-demo

See [backlog](https://docs.google.com/spreadsheets/d/1uTqkZLnjPkgGWoH3Vkg3unEWrG3S-EqRwAIhGvOchUg/edit?usp=sharing) 

<img src="notes/boadr1.jpg" alt="Boadr1">

# Running RabbitMQ with Docker
```
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

# CURL examples

For text sending:
```
curl -H "Content-Type: application/json" -X POST -d '{"text": ["abc erty", "sent2", "cba dfd"]}' http://0.0.0.0:8080/text
```
```
curl -H "Content-Type: application/json" -X POST -d '{"text": "The United States of America is a federal republic consisting of 50 states, a federal district (Washington, D.C., the capital city of the United States), five major territories, and various minor islands. The 48 contiguous states and Washington, D.C., are in central North America between Canada and Mexico; the two other states, Alaska and Hawaii, are in the northwestern part of North America and an archipelago in the mid-Pacific, respectively, while the territories are scattered throughout the Pacific Ocean and the Caribbean Sea."}' http://localhost:8080/text
```
For result receiving:
```
curl http://localhost:8080/result
```
