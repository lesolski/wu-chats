## SS 2021 - Corporate IT 1 - final project

My project is available online at address: codeasap.pythonanywhere.com - not anymore
I suggest that you inspec webapp from there to ensure everything is working, it's a free hosting so it might be a bit slow.
Demo login: demo@s.wu.ac.at pw: 1234

Things I implemented:
- Register/Login System
- Protected views
- Email confirmation within set timer (30minutes)
- Only @s.wu.ac.at emails can register
- Reset password, resend email confirmation token
- Success, Info and Error Messages
- QR code generator with WU Logo
- Form checks, course ID has to be 4 integers, anonymous posting, only valid telegram and wa links allowed
- reCaptcha
- Basic DB CRUD (Create, Read, Update, Delete)
- Like/unlike button
- Pagination
- HTTP Error pages, click on "Need Help?"

Remarks:

- This project is written in Flask Python Web Framework that uses Jinja 2 Templating Engine for HTML.
- I used inline JavaScript in couple pages therefore there is no .js files.
- sitemap.xml and robots.txt are in `static` folder

If you want to run project locally you would have to change database path in `config.py` and run following commands from this directory:
`pip3 install -p requirements.txt`
`python3 run.py`
and open localhost:5000/ in your preferred browser. *Email confirmation and registration won't work due to lack of password