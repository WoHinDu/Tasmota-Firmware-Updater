import requests
import json
import time

def readSettings():
	try:
		settings = json.load(open('settings.json'))
		return settings["credentials"]
	except FileNotFoundError:
		raise FileNotFoundError(
			"Could not found the settings.json file.")


def printStatus(credentials):
	print("Host\t\t\tName\tVersion")

	for sonoff in credentials:
		status = getStatus(sonoff)

		if status:
			print("%s\t%s\t%s" % (
				sonoff["host"],
				status["Status"]["FriendlyName"],
				status["StatusFWR"]["Version"]
			))
		else:
			print("%s\t%s\t%s" % (
				sonoff["host"],
				'-',
				'-'
			))


def getStatus(credential):
	host = 'http://' + credential["host"] + '/cm'
	payload = {
		'user'    : credential["user"],
		'password': credential["password"],
		'cmnd'    : "status 0"
	}

	for attempt in range(5):
		try:
			r = requests.get(host, params=payload)
			return r.json()
		except:
			print("Something went wrong with device %s. Retry. Attempt %s/5" % (credential["host"], attempt))
	else:
		print("Something went completely wrong with device %s" % credential["host"])
		print("It was not possible to etablish a connection to the device. Please check the settings.json and your firewall.")
		return False


def bulkUpdate(credentials, firmware):
	for credential in credentials:
		sendUpdate(credential["host"], firmware)


def sendUpdate(host, firmware):
	url = 'http://' + host + '/u2'

	try:
		files = {'file': open(firmware + '.bin', 'rb')}
	except FileNotFoundError:
		raise FileNotFoundError(
			"Please make sure that {0} is in the same folder next to this "
			"script.".format(firmware))

	for attempt in range(5):
		try:
			r = requests.post(url, files=files)
		except:
			print("Something went wrong with device %s. Retry. Attempt %s/5" % (host, attempt))
		else:
			break
	else:
		raise (ConnectionError, "Something went wrong with device {0}!".format(host))


## Load Settings
credentials = readSettings()

## Show Status
printStatus(credentials)
input("Is everything correct? If you want to continue press ENTER.")

## Flash Minimal Version
print("Let's start with the minimal firmware. This may take a few minutes.")
bulkUpdate(credentials, 'firmware-minimal')

## Show Status
time.sleep(10)
printStatus(credentials)
input("Is everything correct? If you want to continue press ENTER.")

## Flash Regular Version
print("Let's start with the regular firmware. This may take a few minutes.")
bulkUpdate(credentials, 'firmware')

## Show Status
time.sleep(10)
printStatus(credentials)
input("Press Enter to finish...")