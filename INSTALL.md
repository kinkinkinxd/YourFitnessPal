## Getting Started
| Name | Required version(s) | Description |
|------|---------------------| ------------|
| Python | 3.7 or higher | An interpreted, high-level and general-purpose programming language.|
| Django | 3.1 or higher | A Python-based free and open-source web framework. |
| Requests | 2.24.0 or higher | A module that allows you to send HTTP requests using Python. |

* Note that for Linux/MacOS the commands are usually python3 and pip3 instead of python and pip respectively.

1. Clone this project to your machine(computers).
``` 
git clone https://github.com/kinkinkinxd/YourFitnessPal.git
```
2. Go to the directory where you clone the project.
```
cd YourFitnessPal
```
3. Generate new virtual enviroment. (For Window OS)
```
virtualenv env
```
(For MacOS/Linux)
```
virtualenv venv
```
4. Activate virtualenv

go to env directory and then activate it

For Window OS
```
cd env
Scripts\activate
```
after you did this section you should see (env) in your terminal
```
(env) C:\user\YourFitnessPal\env>
```
for MacOs and Linux
```
source venv/bin/activate
```
5. Go out from the env directory
```
(env) C:\user\YourFitnessPal\env>cd..	
# we should see terminal like below
(env) C:\user\YourFitnessPal>
```
6. Enter this command to install all require packages.
``` 
pip install -r requirements.txt 
```
7. Enter this command to migrate the database.
``` 
python manage.py migrate 
```
8. Enter this command to start running the server.
``` 
python manage.py runserver 
```