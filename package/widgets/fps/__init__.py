''' 
    fps [module] 
    
    - Provides access to fingerprint APIs under one configurable name
'''

# Custom classess can also be added here for other sensors
# [NOTE] They must have the same interface/functions as the default class
from .r307 import R307

# Set to the fingerprint sensor you want to use
FingerprintSensor = R307
