
            # andrew: are these even used?
            # if msg['type'] == 'add_queue_back' and 'uuid' in msg:
            #     uuid = msg['uuid']
            #     effect_name = msg['effect']
            #     song_queue.append([effect_name, get_queue_salt(), uuid])
            #     if len(song_queue) == 1:
            #         song_time = 0
            #         add_effect(effect_name)
            #         broadcast_light = True
            #         play_song(effect_name)
            #         song_playing = True

            # elif msg['type'] == 'add_queue_front' and 'uuid' in msg:
            #     uuid = msg['uuid']
            #     effect_name = msg['effect']
            #     if len(song_queue) == 0:
            #         song_queue.append([effect_name, get_queue_salt(), uuid])
            #     else:
            #         song_queue.insert(1, [effect_name, get_queue_salt(), uuid])
            #     if len(song_queue) == 1:
            #         song_time = 0
            #         add_effect(effect_name)
            #         broadcast_light = True
            #         play_song(effect_name)
            #         song_playing = True



    # // andrew: are these even used?
    # // function addQueueBack(effect){
    # //     let msg = {
    # //         uuid: uuid,
    # //         type: "add_queue_back",
    # //         effect: effect
    # //     };
    # //     socket.send(JSON.stringify(msg));
    # //     console.log(msg);
    # // }

    # // function addQueueFront(effect){
    # //     let msg = {
    # //         uuid: uuid,
    # //         type: "add_queue_front",
    # //         effect: effect
    # //     };
    # //     socket.send(JSON.stringify(msg));
    # //     console.log(msg);
    # // }

