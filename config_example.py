#IMPORTANT: RENAME THIS FILE TO config.py AFTER CLONING THE REPOSITORY

#######################
#Wordpress config
#######################
#Id of the user input html element in wordpress login page
wp_user_id = "user_login"
#Id of the password input html element in wordpress login page
wp_pswd_id = "user_pass"
#Id of login button html element in wordpress login page
wp_submit_id = "wp-submit"
#Login page of your Wordpress site
login_url = "https://example.com/wp-admin"
#Url of the Wordpress blog draft that you would like to convert to PDF
post_url = "https://example.com/?p=1234"
#Wordpress username
user = "admin"
#Wordpress passwword
pswd = "wpPassword123"

#######################
#General configuration
#######################
#How many times to check if login was succesfull
max_retries = 5
#How many seconds to wait more after each retry
timeout_factor = 10
#Directory to export screenshots, html and pdf
export_dir = "export/"
