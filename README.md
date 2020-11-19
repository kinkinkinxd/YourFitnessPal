# YourFitnessPal
[![Build Status](https://travis-ci.com/kinkinkinxd/YourFitnessPal.svg?branch=main)](https://travis-ci.com/kinkinkinxd/YourFitnessPal)
[![codecov](https://codecov.io/gh/kinkinkinxd/YourFitnessPal/branch/main/graph/badge.svg?token=B3T7C774FS)](undefined)

YourFitnessPal web application is a website for help you to have a better life and stay healthy. We will advise you what to eat
to do for each day. You can tell us which exercise you like and we will make a schedule for you. The other things are Diets, which foods you should eat or shouldn’t eat, which day is your free day and you can save your information by creating a user to login to our website.

## Getting Started
| Name | Required version(s) |
|------|---------------------|
| Python | 3.7 or higher |
| Django | 3.1 or higher |

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
4. Activate virtualenc

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

## Project Documents
- [Vision Statement](https://github.com/kinkinkinxd/YourFitnessPal/wiki/Vision-Statement)
- [Requirement](https://github.com/kinkinkinxd/YourFitnessPal/wiki/Requirements)
- [Code Review Procedure](https://github.com/kinkinkinxd/YourFitnessPal/wiki/Procedure)
- [Code Checklist](https://github.com/kinkinkinxd/YourFitnessPal/wiki/Checklist)
- [Iteration 1 Plan](https://github.com/kinkinkinxd/YourFitnessPal/wiki/Iteration-1-Plan) and [Task Board](https://github.com/kinkinkinxd/YourFitnessPal/projects/1)
- [Iteration 2 Plan](https://github.com/kinkinkinxd/YourFitnessPal/wiki/Iteration-2-Plan) and [Task Board](https://github.com/kinkinkinxd/YourFitnessPal/projects/2)
- [Iteration 3 Plan](https://github.com/kinkinkinxd/YourFitnessPal/wiki/Iteration-3-Plan) and [Task Board](https://github.com/kinkinkinxd/YourFitnessPal/projects/3)
- [Iteration 4 Plan](https://github.com/kinkinkinxd/YourFitnessPal/wiki/Iteration-4-Plan) and [Task Board](https://github.com/kinkinkinxd/YourFitnessPal/projects/4)

## Licensing
Contact our team members to license.
* @jeanyjean
* @kinkinkinxd
* @BellBoyZz
* @PanitanPlengkham
