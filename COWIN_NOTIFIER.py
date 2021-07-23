import requests
from datetime import datetime, timedelta
import time
import config

age = config.age
pincodes = config.pincodes
CHAT_ID=config.CHAT_ID
print_flag = 'Y'
print("Starting search for Covid vaccine slots!")
print(pincodes)
NOTIFICATION_FLAG=1

def telegram_bot_sendtext(bot_message,bot_chatID):
    
    bot_token = config.bot_token
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


while True:
    counter = 0   

    for pincode in pincodes:   
        actual = datetime.today()
        given_date = actual.strftime("%d-%m-%Y")
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
        try:
            result = requests.get(URL, headers=header)
        except:
            print("NO/POOR INTERNET CONNECTION ON  ",datetime.now())
            continue
        #print(result,given_date) 
        if result.ok:
            response_json = result.json()
            if response_json["centers"]:
                if(print_flag.lower() =='y'):
                    for center in response_json["centers"]:
                        for session in center["sessions"]:
                            if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                                msg='FOR AGE {} :\n'.format(age)
                                print('Pincode: ' + pincode)
                                msg+='Pincode: ' + pincode+"\n"
                                print("Available on: {}".format(session['date']))
                                msg+="Available on: {} \n".format(session['date'])
                                print("\t", center["name"])
                                msg+=center["name"]+"\n"
                                print("\t", center["block_name"])
                                msg+=center["block_name"]+"\n"
                                print("\t Price: ", center["fee_type"])
                                msg+="Price: " + str(center["fee_type"])+"\n"
                                print("Availablity : ", session["available_capacity"])
                                msg+="Availablity : "+str(session["available_capacity"])+"\n"
                                print("\t DOSE_1: ", session["available_capacity_dose1"])
                                msg+="DOSE 1 : "+str(session["available_capacity_dose1"])+"\n"
                                print("\t DOSE_2 : ", session["available_capacity_dose2"])
                                msg+="DOSE 2 : "+str(session["available_capacity_dose2"])+"\n"
                                if(session["vaccine"] != ''):
                                    print("\t Vaccine type: ", session["vaccine"])
                                    msg+="Vaccine type: " + session["vaccine"]
                                print("\n")
                                msg+="\n\nAS CHECKED ON: "+str(datetime.now())
                                try:
                                    telegram_bot_sendtext(msg,CHAT_ID[0])
                                    #telegram_bot_sendtext(msg,CHAT_ID[1])
                                except:
                                    pass
                                counter = counter + 1
        else:
            print(result)
    if not counter:
        if not NOTIFICATION_FLAG:
            try:
                telegram_bot_sendtext(":( MISSED THIS TIME :( ",CHAT_ID[0])
                #telegram_bot_sendtext(":( MISSED THIS TIME :( ",CHAT_ID[1])
            except Exception as e:
                print("UNABLE TO NOTIFY DUE TO ERROR",e)
            NOTIFICATION_FLAG=1
        print("No Vaccination slot available! as checked on",datetime.now())
    else:
        try:
            telegram_bot_sendtext(":) VACCINE AVAILABLE, BOOK YOUR SLOT ASAP :)",CHAT_ID[0])
            #telegram_bot_sendtext(":) VACCINE AVAILABLE, BOOK YOUR SLOT ASAP :)",CHAT_ID[1])
        except Exception as e:
            print("UNABLE TO NOTIFY DUE TO ERROR",e)
        NOTIFICATION_FLAG=0
        print("Vaccination slot AVAILABLE AND NOTIFIED! on ",datetime.now())

    time.sleep(10)
