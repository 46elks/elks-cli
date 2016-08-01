# elks

*Real-time communication command line console powered by 46elks*

## Features

- Send and receive SMS
- Powerful voice call control
- Send and receive MMS (limited support)
- Allocate and de-allocate virtual phone numbers
- Debug your 46elks connections
- Create and modify subaccounts
- See balance and information about your 46elks account
- Display interactive graphs regarding your 46elks account

## Usage

### First time setup

1. Unless you have one already, sign up for a 46elks account at
[46elks.com](https://46elks.com/)
1. Log in on the [46elks Dashboard](https://www.46elks.com/login) and copy your
API id and secret
1. Run `elks setup` to start the interactive setup guide. Please enter your
API id and secret when prompted
1. Run `elks accounts` and ensure that your account is in the list

### Modules

Elks is build using modules which you can use to send, receive and debug your
46elks connections. The current modules are

- elkme
- elks accounts
- elks billing
- elks debug
- elks images
- elks interactive
- elks ivr
- elks mms
- elks numbers
- elks recordings
- elks setup
- elks sms
- elks status
- elks subaccounts
- elks voice

### Send your first SMS

#### Interactively

1. Open a terminal and enter `elks sms new`

#### Non-interactively

1. Open a terminal
1. Enter `elks sms new --to +46700000000 --from You --message
"Hello Ingvar"`

### Read incoming SMS

1. Open a terminal and enter `elks sms list`

### Debug a specific SMS

1. Open a terminal and enter `elks debug --sms <SMSID>`

