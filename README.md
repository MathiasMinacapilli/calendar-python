# Python app to see calendar tasks
A python app in order to see google calendar calendars tasks, and other usefull information.

# Requirements
It is required to install the following pip packages:
* google-api-python-client
* google-auth-httplib2
* google-auth-oauthlib
You can install them running the following command (if you have installed python2 and python3 at the same time you should run with pip3 instead of only pip):
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

# Add calendars to the program
If you wanna add another calendar to the program you have to open the file `calendars.json` and add another JSON object with the following structure:
```
{
    "name": "your_calendar_name",
    "key": "your_calendar_key"
}
```

# Run the program
You can run the program by executing the following command: (if you have installed python2 and python3 at the same time you should run with python3 instead of only python)
```
python main.py
```