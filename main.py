import vlc
from urllib2 import urlopen
import pyaudio
import pymedia.audio.acodec as acodec
import pymedia.muxer as muxer
import time


def main():
    player = vlc.MediaPlayer()
    media_list_player = vlc.MediaListPlayer()
    media_list_player.set_media_player(player)

    def cb(event):
        print "cb:", event.type, event.u

    media_list_player_event_manager = media_list_player.event_manager()
    media_list_player_event_manager.event_attach(vlc.EventType.MediaListPlayerNextItemSet, cb)

    media_list_player_event_manager = player.event_manager()
    media_list_player_event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, cb)
    media_list_player_event_manager.event_attach(vlc.EventType.MediaPlayerMediaChanged, cb)

    media_list = vlc.MediaList()

    media_list.add_media("https://wdr-1live-live.sslcast.addradio.de/wdr/1live/live/mp3/128/stream.mp3")
    media_list_player.set_media_list(media_list)

    media_list_player.play()

    time.sleep(10)

    #radio = RadioPyMedia()
    #radio.streamwithpyMedia()



class RadioPyMedia():

    running = False;

    def streamwithpyMedia(self):
        self.running = True;
        url = "http://mp3.ffh.de/radioffh/livestream.mp3"
        url = "http://www.bensound.org/bensound-music/bensound-dubstep.mp3"
        url = "https://wdr-1live-live.sslcast.addradio.de/wdr/1live/live/mp3/128/stream.mp3"

        dm = muxer.Demuxer('mp3')

        pyaud = pyaudio.PyAudio()

        srate = 44100

        stream = pyaud.open(format=pyaud.get_format_from_width(2),
                            channels=2,
                            rate=srate,
                            output=True)
        print "Latency: ", stream.get_output_latency()

        u = urlopen(url)
        sleeptime = 0.1
        data = u.read(8192/2)
        time.sleep(1)

        while data:
            """while stream.get_write_available() < 8192:
                print "Available: ", stream.get_write_available()
                time.sleep(sleeptime)
                sleeptime += 0.1
            sleeptime = 0.1"""
            # Start Decode using pymedia
            dec = None
            s = " "
            while len(s):
                s = data
                if len(s):
                    frames = dm.parse(s)
                    for fr in frames:
                        if dec == None:
                            # Open decoder
                            dec = acodec.Decoder(dm.streams[0])
                        r = dec.decode(fr[1])
                        if r and r.data:
                            din = r.data;
                    s = ""

            # decode ended

            stream.write(din)
            data = u.read(8192/2)

        self.running = False;

if __name__ == '__main__':
    main()

