# CS50 Finance

### Overview

CS50 Finance is a stock trading simulator (implemented as a website) based on Flask framework that uses IEX API for stock quotes.

### Features implemented

- **Register:** allows a user to register for an account via a form, adds user information to database
- **Quote:** allows a user to look up a stock’s current price
- **Buy:** enables a user to buy stocks
- **Sell:** enables a user to sell stocks
- **Index:** displays an HTML table summarizing, for the user currently logged in, 
  which stocks the user owns, the numbers of shares owned, the current price of each stock, 
  the total value of each holding and user’s current cash balance along with a grand total
- **History:** displays an HTML table summarizing all of a user’s transactions
- **Top Up:** allows a user to add funds to his/her account

### Tech used

- **Backend:**
  - Python
  - Flask
  - CS50 library (for interacting with DB)
  - Werkzeug (for password hash generation, error handling)
  - SQLite
- **Frontend:**
  - HTML, CSS
  - Bootstrap
