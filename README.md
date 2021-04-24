# Python app to see calendar tasks
A python app in order to see google calendar calendars tasks, and other usefull information.

# Docs/API
Using the [google calendar API](https://developers.google.com/calendar/quickstart/python)

# Get started
1. Create virtual env: `python3 -m venv env`
1. Activate virtual env: `source env/bin/activate`
1. Install requirements: `pip install -r requirements.txt`
1. Add calendars if required (see sections "Add calendars to the program")
1. Run the program: `python main.py`

# Add calendars to the program
If you wanna add another calendar to the program you have to open the file `calendars.json` and add another JSON object with the following structure:
```
{
    "name": "your_calendar_name",
    "key": "your_calendar_key"
}
```
