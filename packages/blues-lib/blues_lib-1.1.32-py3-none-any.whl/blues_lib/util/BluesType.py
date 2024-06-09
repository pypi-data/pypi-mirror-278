class BluesType():
  @classmethod
  def last_index(cls,sequence,value):
    '''
    @description : get the last index of a value in a sequence
    @param {tuple|list} sequence
    @param {any} value
    @returns {init} : Returns -1 if there is no match
    '''
    try:
      return (len(sequence) - 1) - sequence[::-1].index(value)
    except ValueError:
      return -1 
 