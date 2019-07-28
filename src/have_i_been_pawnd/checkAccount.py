import hashlib
import requests
import json
from src.exceptions.errors import ApiNotAvailableException

###VARS###
have_i_been_pwned_url_password = "https://api.pwnedpasswords.com/range/"
have_i_been_pwned_url_account = "https://haveibeenpwned.com/api/v2/breachedaccount/"


def check_password(password):
    """
    :param password:
    :return: True when password was found, False when nothing was found
    """

    hashed_password = hashlib.sha1(password.encode()).hexdigest()

    sha1_prefix = hashed_password[:5]
    sh1_suffix = hashed_password[-35:]

    response = requests.get(have_i_been_pwned_url_password + sha1_prefix)

    if response.status_code == 200:

        hash_list = response.text.splitlines()
        hash_list_formatted = []

        for line in hash_list:
            hash_list_formatted.append(line.split(":")[0].lower())

        if sh1_suffix in hash_list_formatted:
            return True
        else:
            return False
    else:
        raise ApiNotAvailableException("Have i been Pawned Api error! Could not check password! Status code: " + response.status_code )


def check_email(e_mail):
    """
    :param e_mail
    :return: dict of breached sites and infos
             if nothing is found, None is returned

             Format: Name, Title, Domain, BreachDate, AddedDate, ModifiedDate, PwnCount, Description,
             LogoPath, DataClasses as List, IsVerified, IsFabricated, IsSensitive, IsRetired, IsSpamList
    """

    response = requests.get(have_i_been_pwned_url_account + e_mail)
    if response.status_code == 200:
        breaches = json.loads(response.text)
        return breaches
    elif response.status_code != 400:
        raise ApiNotAvailableException("Have i been Pawned Api error! Could not check account! Status code: " + response.status_code)
    return False


    # TODO Check if Internet Connection is avaible
