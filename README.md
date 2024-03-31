1. Install `docker` and `docker compose`
2. In directory that `docker-compose.yml` exists run:
```shell
docker-compose up --build -d
```
3. For stopping server run: 
```shell
docker-compose down
```
install requirment : (pip install -r requirements.txt)
accountract : (uvicorn src.main:app --reload --port 8010)
gpt : (uvicorn gpt.main:app --reload --port 8011)


To import and export data in a PostgreSQL database running inside a Docker container, you can use various methods such as using `pg_dump` and `pg_restore` utilities, or you can directly execute SQL commands inside the container.

Here's how you can perform import and export operations:

### Export Data

1. **Using `pg_dump` from Host Machine:**

   ```bash
   docker exec -t accountract-db pg_dump -U postgres accountract > backup.sql
   ```

   This command exports the `accountract` database into a file named `backup.sql` on your host machine.

2. **Using `pg_dump` from Inside the Container:**

   ```bash
   docker exec -t accountract-db pg_dump -U postgres accountract > /path/on/container/backup.sql
   ```

   This command exports the `accountract` database into a file named `backup.sql` inside the container. You can then copy this file out of the container using `docker cp`.

### Import Data

1. **Using `psql` from Host Machine:**

   ```bash
   cat backup.sql | docker exec -i accountract-db psql -U postgres accountract
   ```

   This command imports data from `backup.sql` into the `accountract` database within the container.

2. **Using `psql` from Inside the Container:**

   ```bash
   docker exec -i accountract-db psql -U postgres accountract < /path/on/host/backup.sql
   ```

   This command imports data from `backup.sql` on the host machine into the `accountract` database within the container.

Remember to replace `accountract` with the appropriate database name if it's different in your setup.

These commands assume your PostgreSQL container is named `accountract-db`. Adjust the container name if it's different.

Ensure that the PostgreSQL server is running when you execute these commands. Additionally, if authentication is enabled for PostgreSQL, you may need to provide the password for the PostgreSQL user (`postgres` in your case) during these operations.




To set your local git repository to a specific commit and then push that commit to the remote repository, you can follow these steps:

First, make sure you're in the directory of your Git repository in your command line or terminal.

Use the following command to reset your local repository to the desired commit:

css
Copy code
git reset --hard 23a0b823f1ece3c705764f1edb72bff3bfefa912
This command will reset your working directory to the specified commit, discarding any changes you might have made after that commit.

Once you've reset to the desired commit, push that commit to the remote repository:

css
Copy code
git push --force origin HEAD
This command will forcefully push the specified commit to the remote repository. Be cautious when using --force, as it can overwrite history and potentially cause issues for collaborators who have pulled the repository.

After running these commands, your local repository will be set to the specified commit, and the remote repository will be updated accordingly. Make sure to communicate any changes like this with your collaborators to avoid confusion.