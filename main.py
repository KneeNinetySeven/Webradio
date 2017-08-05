import vlc
from urllib2 import urlopen
import pyaudio
import pymedia.audio.acodec as acodec
import pymedia.muxer as muxer
import time


def main():
    print('Hello World')
    # p = vlc.MediaPlayer('https://wdr-1live-live.icecastssl.wdr.de/wdr/1live/live/mp3/128/stream.mp3')
    # p.play()
    streamwithpyMedia()
    # while pyaudio.paStreamIsNotStopped:
    # do nothing


def streamwithpyMedia():
    url = "http://mp3.ffh.de/radioffh/livestream.mp3"
    url = "https://wdr-1live-live.sslcast.addradio.de/wdr/1live/live/mp3/128/stream.mp3"

    dm = muxer.Demuxer('mp3')

    pyaud = pyaudio.PyAudio()

    srate = 44100

    stream = pyaud.open(format=pyaud.get_format_from_width(2),
                        channels=2,
                        rate=srate,
                        output=True)

    u = urlopen(url)

    data = u.read(8192)

    while data:
        # Start Decode using pymedia
        dec = None
        s = " "
        sinal = []
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
        data = u.read(8192)


if __name__ == '__main__':
    main()
