import time
import thread as t
import sys

from radio import Radio, Station


def main():
    stations = [Station("https://wdr-1live-live.sslcast.addradio.de/wdr/1live/live/mp3/128/stream.mp3", "1Live"),
                Station("http://www.ndr.de/resources/metadaten/audio/m3u/ndr2_hh.m3u", "Ndr2"),
                Station("https://swr-dasding-live.sslcast.addradio.de/swr/dasding/live/aac/96/stream.aac", "Das Ding")]
    radio_inst = Radio(stations)
    # try:
    # thread = t.start_new_thread(radio.switch_to(), 0,)
    # except:
    # print "Radio thread could not be started"
    radio_inst.listen_to_station(0)
    # time.sleep(10)
    menue(radio_inst)


def menue(radio):
    print "Radio running. \n>>Possible Commands:\n\t-> exit \n\t-> pause \n\t-> play\n\t-> next"
    usr_input = ""
    while (usr_input != "exit"):
        usr_input = usr_input.lower()
        if usr_input == "":
            print "> "
        elif usr_input == "pause":
            radio.pause_station()
        elif usr_input == "play":
            radio.listen_to_station(0)
        elif usr_input == "next":
            radio.next_station()
            print "Now Playing: ", radio.stations[radio.current_station].name
        elif usr_input == "vol+":
            radio.turn_vol_up()
            print "Volume: ", radio.current_vol
        elif usr_input == "vol-":
            radio.turn_vol_down()
            print "Volume: ", radio.current_vol
        elif usr_input == "setvol":
            vol = raw_input("to? ")
            try:
                int(vol)
            except:
                print 'Enter a Number pls!'
                break
            radio.turn_vol_to(int(vol))
        else:
            print 'Unkown command'
            time.sleep(0.1)

        usr_input = raw_input("> ")

    radio.stop_listening()

if __name__ == '__main__':
    main()
