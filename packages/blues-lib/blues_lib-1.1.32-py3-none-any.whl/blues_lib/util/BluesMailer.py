import smtplib,datetime
from email.message import EmailMessage
from email.header import Header

class __BluesMailer():

  config = {
    # pick a smtp server
    'server' : 'smtp.qq.com',
    'port' : 465,
    # debug level: 0 - no message; 1 - many messages
    'debug_level' : 0, 
    # the sender's address
    'addresser' : '1121557826@qq.com',
    'addresser_name' : 'BluesLiu QQ',
    # the qq's auth code (not the account's login password)
    'addresser_pwd' : 'ryqokljshrrlifae',
  }

  def __init__(self):
    self.connection = self.__get_connection()

  def __get_connection(self):
    connection = smtplib.SMTP_SSL(self.config['server'],self.config['port'])
    connection.set_debuglevel(self.config['debug_level'])
    connection.login(self.config['addresser'],self.config['addresser_pwd'])
    return connection

  def send(self,payload):
    '''
    @description : send the mail
    @param {MailPayload} payload : mail's required info
     - addressee ：list | str  ; required
     - addressee_name ：str , can't contains space
     - subject : str ; required
     - content : str 
    @returns {MailSentResult} : send result

    '''
    # the receiver's address
    if not payload.get('addressee'):
      return {
        'code':501,
        'message':'The addressee address is empty!'
      }
    
    if not payload.get('subject'):
      return {
        'code':502,
        'message':'The mail subject is empty!'
      }

    if not payload.get('content'):
      payload['content'] = payload['subject']
    
    try:
      message = self.__get_message(payload)
      self.connection.sendmail(self.config['addresser'],payload['addressee'],message)
      self.connection.quit()
    except Exception as e:
      return {
        'code':503,
        'message':'%s' % e
      }

    return {
      'code':200,
      'message':'success'
    }

  def __get_message(self,payload):

    message = EmailMessage()
    
    message['subject'] = payload['subject']
    # the last string must be from mail address
    from_with_nickname = '%s <%s>' % (self.config['addresser_name'],self.config['addresser']) 
    message['from'] = Header(from_with_nickname)

    if type(payload['addressee'])==str:
      message['to'] = Header(payload.get('addressee_name',payload['addressee']))
    else:
      message['to'] = Header(','.join(payload['addressee']))

    # support html document
    message.set_content(payload['content'],'html','utf-8')
    return message.as_string()

# singleton mode
BluesMailer = __BluesMailer()   
