# Films_actors Flask Restful Api 
**(Swagger, Sqlalchemy, SQLite, flask, pipenv, pytest, flask_migrate, jwt authentication 
, Marshmallow, Docker, Bs4, threads)**
### This is a simple application can insert/select/update/delete data in the database using sqlalchemy and flask rest framework.
### Git https://github.com/Aleshichev/Flask_films_Api

## Database has 4 tables:

- **Actors**
- **Films**
- **Movies-actors**
- **Users**

## Swagger:
- **/swagger** - users can interactively view the project documentation.

## The application accepts the following requests:

- **/register** - To register a new user you need to enter your username and password and get a token, then create a new user with json data.

- **/login** - Enter your login to sign in (igor 123).

- **/films** - list of all films.

- **/films/uuid** -  **GET** method has an optional parameter "uuid", it returns films equal to parameter's value. In the **POST** method and **DELETE** method you can add new film or remove existing film. In the **PUT** and **PATCH** methods you can change an existing film.

- **/actors** - list of all actors.

- **/actors/id** - **GET** method has an optional parameter "id", it returns actor who has this parameter's value . In the **POST** method and **DELETE** method you can add new actor or remove existing actor. In the **PUT** and **PATCH** methods you can change an existing actor.

- **/populate_db/** -  **GET** method with **bs4** parse site https://www.imdb.com/ and download films data in db

- **/populate_db_threaded/** -  **GET** method method with **bs4**  and **threads** parse site https://www.imdb.com/ and download films data in db

- **/populate_db_executor/** -  **GET** method method with **bs4** and **ThreadPoolExecutor** or **ProcessPoolExecutor** parse site https://www.imdb.com/ and download films data in db

Results 100 films :
PopulateDB ------------ Done in 139.63 sec.
PopulateDBThreaded ---- Done in 17.49 sec.
ThreadPoolExecutor ---- Done in 21.35 sec.
ProcessPoolExecutor --- Done in 36.87 sec.

## Pytests :
- **test_actors.py** - checks response actors api with mock.
- **test_films.py** - checks response films api with mock.
- **test_auth.py** - checks response users api with mock.

## Dockerfile :
With Dockerfile builds new image
