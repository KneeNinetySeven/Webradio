import vlc

class Radio:
    def __init__(self, stations):
        self._media_list_player = None
        self.stations = stations
        self.running = False
        self.current_station = None
        self.current_vol = 30;

    def listen_to_station(self, station_number=0):
        if self._media_list_player is not None:
            self._media_list_player.stop()

        self._prepare(self.stations[station_number].url)
        self.current_station = station_number
        self.play_station()

    def stop_listening(self):
        self._media_list_player.stop()
        self._media_list_player = None

    def next_station(self):
        if self.current_station < len(self.stations) - 1:
            next_stat = self.current_station + 1
        else:
            next_stat = 0

        self.listen_to_station(next_stat)

    def pause_station(self):
        self._media_list_player.pause()

    def play_station(self):
        self._media_list_player.play()

    def _prepare(self, url):
        def _cb(event):
            print "Event: ", event.type, event.u

        self._media_list_player = vlc.MediaListPlayer()
        self.player = vlc.MediaPlayer()
        self._media_list_player.set_media_player(self.player)

        media_list_player_event_manager = self._media_list_player.event_manager()
        media_list_player_event_manager.event_attach(vlc.EventType.MediaListPlayerNextItemSet, _cb)

        media_list_player_event_manager = self.player.event_manager()
        media_list_player_event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, _cb)
        media_list_player_event_manager.event_attach(vlc.EventType.MediaPlayerMediaChanged, _cb)

        media_list = vlc.MediaList()

        media_list.add_media(url)
        self._media_list_player.set_media_list(media_list)
        self.player.audio_set_volume(self.current_vol)

    def turn_vol_up(self):
        if self.current_vol + 10 <= 150:
            self.current_vol += 10
            self.player.audio_set_volume(self.current_vol)

    def turn_vol_down(self):
        if self.current_vol - 10 >= 0:
            self.current_vol -= 10
            self.player.audio_set_volume(self.current_vol)

    def turn_vol_to(self, volume):
        if volume > 0 & volume <= 150:
            self.player.audio_set_volume(volume)
            self.current_vol = volume

class Station:
    def __init__(self, link, name):
        self.url = link
        self.name = name
