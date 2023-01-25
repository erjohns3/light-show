

### experimenting with fast tar
# tar czf - <files> | ssh user@host "cd /wherever && tar xvzf -"

from helpers import * 

this_file_directory = pathlib.Path(__file__).parent.resolve()
effects_dir = this_file_directory.joinpath('effects')
autogen_shows_dir = effects_dir.joinpath('autogen_shows')



remote_folder = pathlib.Path('/home/pi/light-show/effects/autogen_shows')
for filename, filepath in get_all_paths(autogen_shows_dir):
    scp_to_doorbell(filepath, remote_folder, keep_open=True)
close_connections_to_doorbell()

# this is so much faster
# tar czf - effects/autogen_shows | ssh -T pi@192.168.86.55 "cd light-show && tar xvzf -"