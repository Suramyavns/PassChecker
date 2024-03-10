import requests
import hashlib
import sys


def requestApiData(queryChar):
    url = 'https://api.pwnedpasswords.com/range/'
    response = requests.get(url+queryChar)
    if response.status_code != 200:
        raise RuntimeError(f"Error fetching: {response.status_code}, check for API and try again!")
    return response
def pwnedApiCheck(password):
    #Check password if it exists in API response
    sha1passwd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5Chars, tail = sha1passwd[:5],sha1passwd[5:]
    response = requestApiData(first5Chars)
    return response,tail

def getPasswdLeaksCount(hashes,hashToCheck):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in  hashes:
        if h==hashToCheck:
            return count
    return 0
    

def main(args):
    for passwd in args:
        hashes,tail = pwnedApiCheck(passwd)
        count = getPasswdLeaksCount(hashes,tail)
        if count!=0:
            print(f'{passwd} has been pwned {count} times...better change it!')
        else:
            print(f"No pwnage found for {passwd}")

if __name__=="__main__":
    print("This program checks if your password has ever been pwned.\nThis program doesn't share your password over the internet without encrypting.")
    if sys.argv[1:]:
        main(sys.argv[1:])
    else:
        inputs = input("Enter space seperated list of passwords: ").split()
        main(inputs)
    
