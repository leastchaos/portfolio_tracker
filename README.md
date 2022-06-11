# portfolio_tracker
very basic example on fetch total usd from exchange to spreadsheet
example: https://docs.google.com/spreadsheets/d/139B3755pzarPeCqWy-sketPhFShPof8_94NIyyZS2rY/edit?usp=sharing

1.  fork/clone this repository on your local drive
2.  pip install -r requirements.txt
3.  add account_cred.yml following account_cred.yml example
4.  add google_service_cred.json follow instruction for bots: using service account on https://docs.gspread.org/en/latest/oauth2.html 
    remember to share the spreadsheet on your google account with the bot email or the service account will not be able to detect your spread sheet
4.  update config.yml workbook name and worksheet name that you want to use
5.  run main.py
