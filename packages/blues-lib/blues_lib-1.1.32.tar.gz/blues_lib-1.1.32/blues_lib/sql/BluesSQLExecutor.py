from .BluesMySQL import BluesMySQL
from .BluesSQLConvertor import BluesSQLConvertor

class BluesSQLExecutor():

  def __init__(self,account):
    sql_lang = account.get('sql_lang','mysql')
    if sql_lang=='mysql':
      self.sql_executor = BluesMySQL.get_instance(account)

  def get(self,table,fields="*",conditions=None,orders=None,pagination=None):
    '''
    @description 查询用户提交数据
    @param {dict[]} conditions : one or more conditions
      [
        {'operator':'and','field':'name','comparator':'=','value':'blues'},
        {'operator':'and','field':'name','comparator':'=','value':'blues'}
      ] 
    @param {dict[]} : orders
      [{'field':'id','sort':'asc'},{'field':'name','sort':'desc'}] 
    @param {dict} pagination : page info
      {'no':1,'size':10}
    @returns {SQLResult}
    '''
    condition_sql = BluesSQLConvertor.get_condition_sql(conditions)
    order_sql = BluesSQLConvertor.get_order_sql(orders)
    limit_sql = BluesSQLConvertor.get_limit_sql(pagination)
    field_sql = fields if isinstance(fields,str) else ','.join(fields)

    sql = 'select %s from %s %s %s %s' % (field_sql,table,condition_sql,order_sql,limit_sql)  
    return self.sql_executor.get(sql) 

  def insert(self,table,entities):
    '''
    @description : insert by sql
    @param {dict | dict[]} entities : the entity dict's key is the real table field
      [{'name':'blues','age':18}]
    @returns {SQLResult} 
    '''
    insert_sql = BluesSQLConvertor.get_insert_sql(entities)
    sql = 'insert into %s %s' % (table,insert_sql)
    return self.sql_executor.post(sql) 
 
  def post(self,table,fields,values):
    '''
    @description : insert by template sql
    @param {list|tuple} fields : the fields will be updated
      ['name','age']
    @param {list | list[]} values : one or multi row data values
      [['post01',1],['post02',2]]
    @returns {SQLResult} 
    '''
    insert_sql = BluesSQLConvertor.get_insert_template_sql(fields)
    sql = 'insert into %s %s' % (table,insert_sql)
    return self.sql_executor.post(sql,values) 
  
  def put(self,table,fields,values,conditions):
    '''
    @description : update row
    @param {list|tuple} fields : the fields will be updated
      ['name','age']
    @param {list|tuple} values : the values will be writed
      ['blues',18]
    @param {dict[]} conditions : one or more conditions
      [
        {'operator':'and','field':'name','comparator':'=','value':'blues'},
        {'operator':'and','field':'name','comparator':'=','value':'blues'}
      ] 
    @returns {SQLResult} 
    '''
    update_sql = BluesSQLConvertor.get_update_template_sql(fields,conditions)
    sql = 'update %s %s' % (table,update_sql)
    return self.sql_executor.put(sql,values) 

  def update(self,table,entity,conditions):
    '''
    @description : update row
    @param {dict} entity : the entity dict's key is the real table field
      {'name':'blues','age':18}
    @param {dict[]} conditions : one or more conditions
      [
        {'operator':'and','field':'name','comparator':'=','value':'blues'},
        {'operator':'and','field':'name','comparator':'=','value':'blues'}
      ] 
    @returns {SQLResult} 
    '''
    update_sql = BluesSQLConvertor.get_update_sql(entity,conditions)
    sql = 'update %s %s' % (table,update_sql)
    return self.sql_executor.put(sql) 
  
  def delete(self,table,conditions):
    '''
    @description : delete rows by conditon 
    @param {str} table 
    @param {dict[]} conditions : one or more conditions
      [
        {'operator':'and','field':'name','comparator':'=','value':'blues'},
        {'operator':'and','field':'name','comparator':'=','value':'blues'}
      ] 
    @returns {SQLResult}
    '''
    condition_sql = BluesSQLConvertor.get_condition_sql(conditions)
    sql = 'delete from %s %s' % (table,condition_sql)
    return self.sql_executor.delete(sql)   
