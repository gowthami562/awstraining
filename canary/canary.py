import boto3 

import os  

from datetime import datetime 

from urllib.request import urlopen 

 

SITE = os.environ['https://www.mphasis.com/'] 

EXPECTED = os.environ['Digital Transformation'] 

PHONE = os.environ['+917022161968']  # Must be in this format '+15556668888' 

 

sns = boto3.client('sns') 

 

def validate(res): 

    """Return false if the expected value isn't in the result""" 

    return EXPECTED in res 

 

def ping(event, context): 

    print('Checking {} at {}...'.format(SITE, event['time'])) 

    try: 

        if not validate(str(urlopen(SITE).read())): 

            sns.publish( 

                Message='This is not the site text you\'re looking for',  

                PhoneNumber=PHONE 

            ) 

            raise Exception('Validation failed') 

    except Exception as e: 

        print('Check failed!') 

        raise e 

    else: 

        print('Check passed!') 

        sns.publish(Message='Check passed', PhoneNumber=PHONE) 

        return event['time'] 

    finally: 

        print('Check complete at {}'.format(str(datetime.now()))) 

 

 

 