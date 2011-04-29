'''
Control aspects of the grains data
'''

def items():
    '''
    Return the grains data

    CLI Example:
    salt '*' grains.items
    '''
    return __grains__

def item(key):
    '''
    Return a singe component of the facter data

    CLI Example:
    salt '*' grains.item operatingsystem
    '''
    if __grains__.has_key(key):
        return __grains__[key]
    return ''
