# Recent Activity Extractor for Strava Clubs

This is a small Python 3.8 script to extract data from the __Recent Activity__ tab in Strava Clubs.

## Installation

```bash
git clone
cd strava
```

Create a virtual environment to install the required packages ([See link](https://docs.python.org/3/library/venv.html)).

```bash
pip install -r requirements.txt
```

## Usage

1. Login into your Strava account.
2. Go to https://www.strava.com/clubs/617821/recent_activity
3. Scroll at the end of the page
4. Right-click and __Save as__
5. Save the page in the project directory and make sure its name is `index.htm`
6. Execute the following command:

```bash
python main.py
```
You now have a `data.json` file in the project directory with the updated data.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Unlicense](https://choosealicense.com/licenses/unlicense/)