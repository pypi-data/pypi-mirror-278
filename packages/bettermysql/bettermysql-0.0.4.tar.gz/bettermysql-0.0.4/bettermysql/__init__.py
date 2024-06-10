import pymysql

__version__ = "0.0.4"

class MYSQLSingleton(type):
  _instances = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(MYSQLSingleton, cls).__call__(*args, **kwargs)

    return cls._instances[cls]

class BetterMYSQL(metaclass=MYSQLSingleton):
  __conn=None

  @staticmethod
  def setup(name, user, pasw, host, port=3306, timeout=5):
    if (not BetterMYSQL.__conn):
      BetterMYSQL.__conn = pymysql.connect(host=host, user=user, passwd=pasw, database=name, port=port, connect_timeout=timeout, autocommit=True)
    
  @staticmethod
  def connection():
    return BetterMYSQL.__conn
    
  @staticmethod
  def cursor(arg=pymysql.cursors.DictCursor):
    return BetterMYSQL.__conn.cursor(arg)

  @staticmethod
  def cell(sql, data=None):
    curr = BetterMYSQL.cursor(pymysql.cursors.Cursor)

    curr.execute(BetterMYSQL.__query_sql(sql), data)

    return curr.fetchone()[0] if curr.rowcount else None

  @staticmethod
  def run(sql, data=None):
    curr = BetterMYSQL.cursor(pymysql.cursors.DictCursor)

    curr.execute(BetterMYSQL.__query_sql(sql), data)

    return curr

  @staticmethod
  def sql_date():
    return "now()"

  @staticmethod
  def __query_sql(sql):
    return sql.replace('__NOW__', BetterMYSQL.sql_date()).replace('?', '%s')

class Model:
  __query=""
  _table=""
  
  def table(self):
    return self._table

  def query(self):
    return self.__query

  def select(self, s):
    self.__query = f"select {s} from {self._table} "

    return self

  def insert(self, s):
    self.__query = f"insert into {self._table} ({s}) "

    return self

  def update(self, s):
    self.__query = f"update {self._table} set {s} "

    return self

  def delete(self, s : any = None):
    self.__query = f"delete from {self._table} "
    self.where(s)

    return self

  def __values(self, data):
    s = ""

    i = 0
    while i < len(data):
      if (data[i] == '__NOW__'):
        letter = BetterMYSQL.sql_date()
        
        temp_data = list(data)
        temp_data.pop(i)
        data = tuple(temp_data)
      else:
        letter = "?"
      
      if i == 0:
        s += letter
      else:
        s += f",{letter}"
      
      if (letter == '?'):
        i += 1

    dt = BetterMYSQL.sql_date()

    self.__query += f"values ({s}) "

    return data

  def where(self, s):
    if (s):
      self.__query += f"where {s} "

    return self
    
  def order(self, s):
    self.__query += f"order by {s} "

    return self

  def group(self, s):
    self.__query += f"group by {s} "

    return self

  def limit(self, s):
    self.__query += f"limit {s} "

    return self

  def row(self, data=None):
    return Model.__query_row(BetterMYSQL.run(self.query(), data))

  def cell(self, data=None):
    return BetterMYSQL.cell(self.query(), data)

  def run(self, data=None, last_id=True):
    is_insert = (self.query().lower().find("insert") != -1)

    if is_insert:
      data = self.__values(data)

    cursor = BetterMYSQL.run(self.query(), data)

    return Model.__query_all(cursor) if not (is_insert and last_id) else BetterMYSQL.connection().insert_id()

  @staticmethod
  def __query_all(cursor):
    return cursor.fetchall()

  @staticmethod
  def __query_row(cursor):
    return cursor.fetchone()