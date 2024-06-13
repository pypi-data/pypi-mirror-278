import pyodbc

__version__ = "0.0.2"

class MSSQLSingleton(type):
  _instances = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(MSSQLSingleton, cls).__call__(*args, **kwargs)

    return cls._instances[cls]

class BetterMSSQL(metaclass=MSSQLSingleton):
  __conn=None

  @staticmethod
  def setup(name, user, pasw, host, port=1433, timeout=5):
    if (not BetterMSSQL.__conn):
      BetterMSSQL.__conn = pyodbc.connect(driver='{SQL Server}', host=host, database=name, port=port, user=user, password=pasw, timeout=timeout, autocommit=True)
    
  @staticmethod
  def connection():
    return BetterMSSQL.__conn
    
  @staticmethod
  def cursor():
    return BetterMSSQL.__conn.cursor()

  @staticmethod
  def cell(sql, data=None):
    curr = BetterMSSQL.cursor()

    curr.execute(BetterMSSQL.__query_sql(sql), BetterMSSQL.__query_data(data))

    return curr.fetchone()[0] if curr.rowcount else None

  @staticmethod
  def run(sql, data=None):
    curr = BetterMSSQL.cursor()

    curr.execute(BetterMSSQL.__query_sql(sql), BetterMSSQL.__query_data(data))

    return curr

  @staticmethod
  def sql_date():
    return "getdate()"

  @staticmethod
  def __query_sql(sql):
    return sql.replace('__NOW__', BetterMSSQL.sql_date())

  @staticmethod
  def __query_data(data):
    return data if (data) else []
  
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

  def insert(self, s = ""):
    self.__query = f"insert into {self._table} " + (f"({s})" if s else "")

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
        letter = BetterMSSQL.sql_date()
        
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

    self.__query += f"values ({s}) "

    return data

  def where(self, s):
    if (s):
      self.__query += f"where {s} "

    return self
    
  def top(self, count):
    self.__query = self.__query.replace('select', f'select top({count})')

    return self

  def order(self, s):
    self.__query += f"order by {s} "

    return self

  def group(self, s):
    self.__query += f"group by {s} "

    return self

  def row(self, data=None):
    return Model.__query_row(BetterMSSQL.run(self.query(), data))

  def cell(self, data=None):
    return BetterMSSQL.cell(self.query(), data)

  def run(self, data=None, last_id=False):
    is_insert = (self.query().lower().find("insert") != -1)
    last_inserted_id = 0

    if is_insert:
      data = self.__values(data)

    cursor = BetterMSSQL.run(self.query(), data)
    
    if (is_insert and last_id):
      cursor.execute("select scope_identity()")
      last_inserted_id = cursor.fetchone()[0]

    return Model.__query_all(cursor) if not (is_insert and last_id) else last_inserted_id

  @staticmethod
  def __query_all(cursor):
    rows = None
    
    try:
      columns = [col[0] for col in cursor.description]
      rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except:
      pass

    return rows

  @staticmethod
  def __query_row(cursor):
    row = None
    
    if (row := cursor.fetchone()):
      columns = [col[0] for col in cursor.description]  
      row = dict(zip(columns, row))

    return row