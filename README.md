--- Instruction on how to implement our project.

Step1. Go to our github: https://github.com/spark1216/551_Project_Team17
Step2. Download all the file in the folder "pages", arrange in the correct order: client_pages.py, manager_pages.py
Step3. Download the airbnb_ds_clean.csv in the folder "database creation", and its directory path will be used in the dsci551_project_mysql_setup.py
Step4. Pip installs necessary modules: streamlit, datetime, pymysql, sqlalchemy, pgeocode
Step5. Download the local MySQL database, set the password for the localhost (we suggest the password to be dsci551 so you do not need to modify the code). You can verify the password by typing into the terminal and starting MySQL.
Step6. Using dsci551_project_mysql_setup.py to set up our database. You can verify the setup by login to SQL and check the database and tables
Step7. Streamlit connection: make sure you place the folder in the right directory. 
Step8. Go to the main.py and run it. Paste this line into the terminal and it will direct you to our database UI. We recommend using the following command to give permission for file upload:  streamlit run /Users/winniecai/PycharmProjects/551/venv/project2/main.py --server.enableXsrfProtection false 
After you paste the command line, it will redirect you to our database website. Now you can just use our UI to manage the database!



