# HueLightsPlay

This is a script for accessing my Hue hub at home to play with.

references:

Python Requests
https://realpython.com/python-requests/

Hue Developer Get Started
https://developers.meethue.com/develop/get-started-2/

Python dotenv
https://pypi.org/project/python-dotenv/

Python's time.sleep()
https://www.pythoncentral.io/pythons-time-sleep-pause-wait-sleep-stop-your-code/

Flask
https://flask.palletsprojects.com/en/1.1.x/

Jinja
https://jinja.palletsprojects.com/en/2.10.x/api/#basics

The Flask Mega-Tutorial Part III: Web Forms
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

A tutorial on creating basic API in Flask
https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#implementing-our-api

## k8s Deployment

I was working on trying to host an API in k8s at work and I found some answers.
The dilemma was that I had a Flask app and wanted to host it using nginx.

After searching for answers, I found and tutorial on how to do this without k8s. Then, I used docker to create images and then deploy to k8s

I learned that you can host more than 1 container in a pod and that internetworking between the containers in a pod was only localhost.

If you look in [the nginx folder](https://github.com/fearlessfreap24/HueLightsPlay/tree/master/nginx) you will see that I made a config file to proxy the requests from port 80 to localhost:5001.

I made the containers separately. The [deployment](https://github.com/fearlessfreap24/HueLightsPlay/blob/master/dep.huelights.yaml) put the 2 containers together and then I created a [service](https://github.com/fearlessfreap24/HueLightsPlay/blob/master/serv.lb.huelights.yaml) to expose port 80.

