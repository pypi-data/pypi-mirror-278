
# Publix Passport API

API to interact with publix passport. Still under development, features are still being added.

# WARNING

Publix requires mutlifactor authentification on login. Currently the API will prompt you for the factors sent to you via SMS in the terminal.

I recomend editing the init() function in 'publix.py' file to fit your needs.

# Usage

```python
from publixPassportAPI.publix import User

user = User('username', 'password')

schedule = user.getSchedule() # returns hashmap
payStatements = user.payStatementHistory() # returns list

```


