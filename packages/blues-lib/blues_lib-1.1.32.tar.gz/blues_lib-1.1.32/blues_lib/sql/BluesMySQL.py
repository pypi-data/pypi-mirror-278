import pymysql,traceback

# using the singleton to make sure using the only one cursor
class BluesMySQL():

  mysql = None
  
  @classmethod
  def get_instance(cls,account):
    if not cls.mysql:
      cls.mysql = BluesMySQL(account)
    return cls.mysql

  def __init__(self,account):
    '''
    @description : connect and execute sql
    @param {dict} account : MySQL account
    '''
    self.connector = self.__get_connector(account)
    self.cursor = self.connector.cursor() 
  
  def get(self,sql):
    # always fetch all rows, even only one row
    return self.__fetchall(sql)

  def post(self,sql,values=None):
    return self.__execute(sql,values)

  def put(self,sql,values=None):
    return self.__execute(sql,values)
  
  def delete(self,sql):
    return self.__execute(sql)

  def __get_connector(self,account):
    return  pymysql.connect(
      host=account['host'],
      user=account['user'],
      password=account['password'],
      database=account['database'],
      cursorclass=pymysql.cursors.DictCursor,  # 返回数组类型数据
      )

  def __execute(self,sql,values=None):
    '''
    @description : insert/update/delete 
    @prams {str} sql : sql statement (with or without template)
    @params {tuple[]} values : multi real values
    @demo use placeholder
      - sql="insert into ics_test (name,age) values (%s,%s)"
      - execute: cursor.execute(sql,[('blues',18),('liu',12)])
    '''
    try:
      invoker_info = traceback.extract_stack()
      invoker = invoker_info[-2][2]
      
      # use executemany only when values is two-dimensional array
      if values and self.__is_series(values[0]):
        count=self.cursor.executemany(sql,values)
      else:
        count=self.cursor.execute(sql,values)

      self.connector.commit()

      result = {
        'code':200,
        'count':count,
        'sql': sql,
      }
      if invoker=='post':
        # if insert many rows, the row_id is the first inserted row's id (not the last inserted one)
        result['row_id'] = self.cursor.lastrowid

      return result

    except Exception as e:
      return {
        'code':500,
        'exception':e,
        'sql': sql,
      }

  def __is_series(self,value):
    return isinstance(value, (list, tuple))

  def __fetchall(self,sql):
    '''
    @description Query rows of data
    @param {str} sql : Complete sql statement
    @returns {SQLResult} 
    '''
    try:
      self.cursor.execute(sql)
      rows=self.cursor.fetchall()
      # 立即提交，否则轮询会有缓存
      self.connector.commit()
      return {
        'code':200,
        'count':len(rows),
        'data':rows if rows else None, # 无数据返回空元组转为None
        'sql': sql,
      }
    except Exception as e:
      return {
        'code':500,
        'exception':e,
        'sql': sql,
      }



