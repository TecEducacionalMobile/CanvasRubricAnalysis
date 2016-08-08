Canvas Rubric Analysis
=============================

This repo contains the code for Canvas Rubric Analysis tool at Escola Móbile. 

<img src="http://i.giphy.com/x8JTy9Zp1jtPq.gif" width='500px'>

Running the app
---------------


This application is built on top of [Google App Engine](https://cloud.google.com/appengine/). 

In order to run the app, you must supply a `Handlers/secrets.py` file with the appropriate Canvas credentials. An example file is provided. Be mindful that in order for the tool to work properly an auth token with high-level admin privileges is required. Therefore, never commit any file which has the credentials.

In `dist/scripts/****.scripts.js`, find `app.constant` and make sure the URL corresponds to the address being served by your App Engine endpoint.

To deploy, simply change the name of your app in `app.yaml`


Developing
----------

<img src="http://i.giphy.com/13HgwGsXF0aiGY.gif" width='300px'>

###Set-up

The application is a small AngularJS app which consumes a basic API that is served by App Engine. 

All communication with the Canvas API happens on the backend. All routes are defined in `main.py` and all relevant code is in `Handlers/Home.py`. 

To develop the front-end app, you will need [Grunt](https://www.gruntjs.com) for build tasks and [Bower](https://bower.io) for dependency management. The snippet below should be able to get you on your way:

```
cd frontend
npm install -g bower grunt-cli
bower install
```

At this point, you should be able to run `grunt serve` to serve your app with live-reload and `grunt build` to build your work. The build task should generate a `dist` folder. Simply place this folder at the root to have App Engine serve it.

Caveats
-------
<img src="http://i.giphy.com/fgR5ghGSXWpuU.gif" width='300px'>

+ Endpoints

   There are two sets of endpoints that you have to be mindful app: The GAE endpoint that the frontend app will use and the Canvas API endpoints that you will consume. As of right now, there is no automatic build task to help sort any of this out. Therefore, always be careful that you are routing each of these apps correctly, especially as you are about transition between development and production environments.

+ Security

   This was built as a proof-of-concept application. As such, there are  NO SECURITY considerations taken into account. The app exposes enrollment, assignment, and assignment result data to anyone who hits the endpoints.





