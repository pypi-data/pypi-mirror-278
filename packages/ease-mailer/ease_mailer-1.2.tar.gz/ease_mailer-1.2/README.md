<h2>Ease Mailer</h2>
<hr>
<p>Easy Mailer is a simple python package that allows you to send emails with ease.</p>
<h4>Usage</h4>
<ul>
<li><h4>Import the class</h4></li>

```
from ease_mailer import mailer
```

<li><h4>For Help Type</h4></li>

```
mailer.Mail.help() # Shows the help message
```

<li><h4>Create an instance of the class</h4></li>

```
mail_class = mailer.Mail("source@email.com", "youremailpassword") # Creates an instance of the class
```

<li><h4>Login to your email</h4></li>

```
mail_class.login() # Logs the user in returns True if successful, False otherwise
```

<li><h4>Send an email</h4></li>

```
mail_class.send_mail("dest@mail.com", "Subject", "Body") # Sends the email, throws an error if user is not logged in returns True if successful, False otherwise
```

<li><h4>Show the status of email wether it was sent or not</h4></li>

```
mail_class.show_status() # Shows the status of the email whether it was sent or not returns "Email sent successfully" if successful, "Email failed to send" otherwise
```

</ul>
