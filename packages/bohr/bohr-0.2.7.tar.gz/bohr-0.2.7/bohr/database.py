import os
import psycopg2
import pandas as pd
from psycopg2 import extras



class Database(object):
    def __init__(self, user,password,host,port,database,multiple=False):
        """
        Initializes the Database object with connection details.

        Args:
            user (str): The username for the database connection.
            password (str): The password for the database connection.
            host (str): The hostname of the database server.
            port (int): The port number of the database server.
            database (str): The name of the database to connect to.
            multiple (bool): Flag indicating if operations should be performed on multiple databases.
        """
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.multiple = multiple

    def connect(self,db):
        """
        Connects to the specified database.

        Args:
            db (str): The name of the database to connect to.

        Returns:
            tuple: A tuple containing the connection object and cursor object, or (None, None) if the connection fails.

        Example:
            >>> conn, cur = Database(user, password, host, port, database).connect('my_database')
        """
        try:
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=db
            )
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            return conn, cur
        except Exception as e:
            print(f'Error connecting to {db}: {e}')
            return None, None

    def get_sql(self, sql, params=None):
        """
        Executes a SELECT SQL query and returns the result as a DataFrame.

        Args:
            sql (str): The SQL query to execute.
            params (tuple, optional): Parameters to include in the SQL query.

        Returns:
            pd.DataFrame: A DataFrame containing the result of the SQL query, or None if the query fails.

        Example:
            >>> df = Database(user, password, host, port, database).get_sql('SELECT * FROM my_table')
        """
        conn, cur = self.connect(self.database)
        if conn is None or cur is None:
            return None

        try:
            cur.execute(sql, params)
            result = cur.fetchall()
            df = pd.DataFrame(result)
            return df
        finally:
            conn.close()

    def commit_sql(self, sql, params=None):
        """
        Executes a SQL command that modifies the database and commits the changes.

        Args:
            sql (str): The SQL command to execute.
            params (tuple, optional): Parameters to include in the SQL command.

        Example:
            >>> Database(user, password, host, port, database).commit_sql('INSERT INTO my_table (column) VALUES (%s)', (value,))
        """

        conn, cur = self.connect(self.database)
        if conn is None or cur is None:
            return
        try:
            if params is None:
                cur.execute(sql)
            else:
                cur.execute(sql, params)
            conn.commit()
        except Exception as e:
            print(f"SQL execution error: {e}")
        finally:
            conn.close()



    def insert(self, table, df, onConflict=''):
        """
        Inserts data from a DataFrame into a specified table, handling conflicts if specified.

        Args:
            table (str): The name of the table to insert data into.
            df (pd.DataFrame): The DataFrame containing the data to insert.
            onConflict (str, optional): Conflict resolution clause for the SQL query.

        Example:
            >>> Database(user, password, host, port, database).insert('my_table', df, 'ON CONFLICT (id) DO NOTHING')
        """
        if self.multiple:

            if "research_dev" in self.database or 'trading_dev' in self.database:
                for db in ['research_dev', 'trading_dev']:
                    self.batch_insert(db, table, df, onConflict)
            elif self.database=="research" or self.database=='trading':
                for db in ['research', 'trading']:
                    self.batch_insert(db, table, df, onConflict)
            else:
                self.batch_insert(self.database, table, df, onConflict)
        else:
            self.batch_insert(self.database, table, df, onConflict)


    def batch_insert(self,db,table, df,onConflict=''):
        """
        Inserts data from a DataFrame into a specified table in batch mode, handling conflicts if specified.

        Args:
            db (str): The name of the database to insert data into.
            table (str): The name of the table to insert data into.
            df (pd.DataFrame): The DataFrame containing the data to insert.
            onConflict (str, optional): Conflict resolution clause for the SQL query.

        Example:
            >>> Database(user, password, host, port, database).batch_insert('my_database', 'my_table', df, 'ON CONFLICT (id) DO NOTHING')
        """
        try:
            conn, cur = self.connect(db)
            if conn is None or cur is None:
                return

            tuples = [tuple(x) for x in df.to_numpy()]
            cols = ','.join(list(df.columns))
            query = f"INSERT INTO {table}({cols}) VALUES %s {onConflict}"
            extras.execute_values(cur, query, tuples)
            conn.commit()
            print("Data inserted",db)
        except Exception as error:
            print(f"Data Error: {error,db}")
            conn.rollback()
        finally:
            if conn is not None:
                conn.close()
    
