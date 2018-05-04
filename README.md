#### about the project:
- users can create and handle tasks 
 each task can be in 3 cases (NEW, PROGRESS, DONE)
- Progress state tasks could be linked to another task, I handled it like a doubly linked list, from this task, client can reach to its linked task **or**  if from the linked, the client can reach to the former task(outer task) 

-------

#### to run in the terminal inside repo folder write :
```shell
virtualenv env 
pip install -r requirments.txt
python manage collectstatic
python mange migrate
python mange runsever 
```
make your that **python3 & virtualenv** were installed in your machine


------------------
run tests :
```shell
./manage.py test
```
-----
to try the API you have to make user first , write in your terminal
```shell
python manage.py createsuperuser
```
-----
request and response for individual task:

[![http://www8.0zz0.com/2018/05/04/05/666922892.jpeg](http://www8.0zz0.com/2018/05/04/05/666922892.jpeg "http://www8.0zz0.com/2018/05/04/05/666922892.jpeg")](http://www8.0zz0.com/2018/05/04/05/666922892.jpeg "http://www8.0zz0.com/2018/05/04/05/666922892.jpeg")
