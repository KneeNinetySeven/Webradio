import time
import thread as t
import sys

from radio import Radio


def main():
    stations = ["https://wdr-1live-live.sslcast.addradio.de/wdr/1live/live/mp3/128/stream.mp3"]
    radio = Radio(stations)
    # try:
    # thread = t.start_new_thread(radio.switch_to(), 0,)
    # except:
    # print "Radio thread could not be started"
    radio.listen_to_station(0)
    # time.sleep(10)
    menue(radio)


def menue(radio):
    print "Radio running. \n>>Possible Commands:\n\t-> exit \n\t-> pause \n\t-> play\n\t-> next"
    input = ""
    while (input != "exit"):
        input = input.lower()
        if input == "pause":
            radio.pause_station()

        if input == "play":
            radio.listen_to_station(0)

        if input == "next":
            radio.next_station()


        time.sleep(0.1)
        input = raw_input("> ")

    radio.stop_listening()

if __name__ == '__main__':
    main()
