## Automated CodeForces Registration

This is a python script that uses the selenium module and chromedriver to register on the CodeForces website for you.

## Usage
### run the python script in your terminal: 
`python auto_register.py`

You should be greeted with this page
![](https://i.imgur.com/47kE3E8.png)

### Input your handle, email and password
Make sure you input a valid email and your passwords are >5 characters in length and contain lowercase, uppercase, numbers and special characters!

### Browser session starts
After inputting the necessary credentials, a chrome browser session should be started and credentials filled into the form inputs and submitted.

After submission, you'll be brought to the registration completion page and a screenshot will be taken and stored in your current directory.

The driver then closes and you've successfully registered for CodeForce!

![](https://i.imgur.com/lwJiY8o.png)


__Note: If the handle you've chosen has already been taken, you will not be taken to the registration completion page and the driver will timeout, resulting in an unsuccessful registration and you'll have to try again with a different handle.__

![](https://i.imgur.com/nr5BelU.png)

