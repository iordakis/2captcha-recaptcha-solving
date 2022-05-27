from time import sleep
import requests

SERVICEKEY = '' # 'your_api_service_key'
RECAPTCHAKEY = '' # 'google_recaptcha_key'
RECAPTCHAPAGE = '' # 'https://www.example.com/register'

s = requests.Session()
jobDone = False


# sending the captcha ID and waiting to receive the solution string
def recaptchaSolving():
    global finalRecaptcha, recaptchaAnswer

    captchaURL = 'http://2captcha.com/in.php?key=' + SERVICEKEY + '&method=userrecaptcha&googlekey=' + RECAPTCHAKEY + '&pageurl=' + RECAPTCHAPAGE
    print("[+] CAPTCHA URL:", captchaURL, "\n")
    try:
        resp = s.get(captchaURL, timeout=20)
        if resp.text[0:2] != 'OK':
            print("Service error. Error code:" + resp.text)
            jobDone = False
        else:
            captcha_id = resp.text[3:]
            print("[+] 2CAPTCHA ID :", captcha_id, "\n")
            fetch_url = 'http://2captcha.com/res.php?key=' + SERVICEKEY + '&action=get&id=' + captcha_id
            # looping 12 times with 7 seconds delay each, to make sure we allow enough time for receiving the solution
            for i in range(1, 12):
                sleep(7)
                resp = s.get(fetch_url, timeout=20)
                print("[+] RECAPTCHA response token:", resp.text, "\n")
                if resp.text[0:2] == 'OK':
                    break
            jobDone = True
            print("[+] FINAL RECAPTCHA response token:", resp.text[3:], "\n")
            finalRecaptcha = str(resp.text[3:])
    except requests.Timeout as err:
        print(err.message)
    except:
        print("[+] General exception thrown!", "\n")
        recaptchaAnswer = False
        jobDone = False

    if jobDone == True:
        print("Job done, verifying received content..")
        if finalRecaptcha == 'CHA_NOT_READY':
            print("Captcha solving was not ready...")
            recaptchaAnswer = False
        else:
            print("Captcha solving is READY...")
            recaptchaAnswer = True


# used to report a bat captcha solution, if this happens
def reportBadCaptcha():
    global captcha_id
    global SERVICEKEY

    print("[+] REPORTING bad captcha ID:", captcha_id, "\n")
    try:
        fetch_url = 'http://2captcha.com/res.php?key=' + SERVICEKEY + '&action=reportbad&id=' + captcha_id
        resp = s.get(fetch_url, timeout=20)
        time.sleep(2)
        print("[+] RECAPTCHA response token:", resp.text, "\n")
    except requests.Timeout as err:
        print(err.message)
    except:
        print("FAILED reporting bad captcha!")


if __name__ == '__main__':
    recaptchaSolving()
    # send the finalRecaptcha content in your POST request
    # if captcha wasn't solved use reportBadCaptcha() to save service credit