good in basement
    Supernova/Stars/PieturP - HSL-tunnelvisions_morphing3.milk
    Reaction/Liquid Blobby/$$$ Royal - Mashup (236).milk
    Dancer/Glowsticks Mirror/203.milk
    Dancer/Murky/mrt ei cynical engineers working for a backward system unite in circle jerk oink.milk
    Dancer/Glowsticks Mirror/389.milk
    Fractal/Lattice/EoS - skylight a3 [trip colors flux2]_phat_Multi_shaped2_zoe_colours3.milk
    Dancer/Whirl/Adam Fx 2 Zylot -  FierceFX Glowworld 7.milk

    Waveform/Spectrum/suksma - negative infinity for not flinching - thr.milk
    Waveform/Wire Mirror/Serge + Jc - Neon Star Formation003.milk
    Sparkle/Mass Circles/suksma - dotes hostile undertake - fake rivals real2.milk
    Drawing/Trails Mirror/fiShbRaiN - witchcraft (metropolish remix) - test - tillex  - bob boyce' 'the cell', pulstar, singh grooves, motor up, pre-filter cyclone.milk

    ./presets/presets-cream-of-the-crop/Waveform/Wire Mirror/suksma - ignore butte des mortes prayer heap.milk

    Drawing/Liquid/suksma - satanic teleprompter - sth shd - salientanic FLE.milk

    Dancer/Glowsticks Mirror/200.milk
    Dancer/Glowsticks Mirror/207 mrt get out to where the shooting's going on.milk
    ./presets/presets-cream-of-the-crop/Waveform/Wire Circular/Geiss - Skin Dots 6 (Jelly).milk

    talking:
        Dancer/Glowsticks Mirror/drugsincombat - liquifried squid i.milk



fix audio:
    echo "set-default-sink alsa_output.platform-bcm2835_audio.analog-stereo" | pacmd



git submodule update --init --recursive
    for eval


other frontend
    https://github.com/kblaschke/frontend-sdl2



cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_SDL_UI=ON
cmake --build . -- -j

ON RASP PI:
    cmake --build .



rm CMakeCache.txt; cmake CMakeLists.txt && cmake --build . && ./test_sdl2


headless x:
    https://stackoverflow.com/questions/75680223/glx-offscreen-rendering-in-headless-system


https://gist.github.com/n8allan/4cd46396c86cb00fd35cb399515d31df
https://github.com/matusnovak/rpi-opengl-without-x


https://wiki.libsdl.org/SDL2/README/raspberrypi


https://stackoverflow.com/questions/57672568/sdl2-on-raspberry-pi-without-x
    FOR TEST PROGRAM:
        maybe this instead: ./configure --enable-video-kmsdrm --enable-video-rpi
        g++ main.cpp `pkg-config --cflags --libs sdl2` -o real_sdl2.out && ./real_sdl2.out


        g++ main.cpp -I/home/pi/random/sdl_install/SDL/include/ -D_REENTRANT -L/home/pi/random/sdl_install/SDL/build/.libs -Wl,-rpath,/home/pi/random/sdl_install/SDL/build/.libs -Wl,--enable-new-dtags -lSDL2 -o my_sdl2.out && LD_LIBRARY_PATH=build ./my_sdl2.out

        default include:
            /usr/include/SDL

        default lib:
            /lib/aarch64-linux-gnu/libSDL2-2.0.so.0

    FOR REAL:
        rm CMakeCache.txt; cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_SDL_UI=ON -DSDL2_INCLUDE_DIR=/home/pi/random/sdl_install/SDL/include/ -DSDL2_LIBRARY=/home/pi/random/sdl_install/SDL/build/.libs/libSDL2.so -DSDL2_DIR=/home/pi/random/sdl_install/SDL/


        LD_LIBRARY_PATH=/home/pi/random/sdl_install/SDL/build/.libs/ 
        





real:
    doorbell SDL-release-2.28.4$ sdl2-config --cflags
    -I/usr/include/SDL2 -D_REENTRANT
    doorbell SDL-release-2.28.4$ sdl2-config --libs  
    -lSDL2

built:
    doorbell SDL$ ./sdl2-config --cflags                           
    -I/home/pi/random/sdl_install/include/SDL2 -D_REENTRANT
    doorbell SDL$ ./sdl2-config --libs         
    -L/home/pi/random/sdl_install/lib -Wl,-rpath,/home/pi/random/sdl_install/lib -Wl,--enable-new-dtags -lSDL2


building sdl2:
    ./configure --enable-video-kmsdrm

    cp -r include SDL2



src/sdl-test-ui/projectM-Test-UI




-Wl,-rpath, /usr/lib/libGLESv2.so /usr/lib/libgomp.so /usr/lib/libpthread.a 



rm CMakeCache.txt; cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_SDL_UI=ON && cmake --build . -- -j && src/sdl-test-ui/projectM-Test-UI

static:
    rm CMakeCache.txt; cmake -DCMAKE_BUILD_TYPE=Debug -DBUILD_SHARED_LIBS=OFF -DENABLE_SDL_UI=ON && cmake --build . -- -j && src/sdl-test-ui/projectM-Test-UI



INFO: Displaying preset: ./presets/presets-cream-of-the-crop/Waveform/Wire Tunnel/stahlregen + geiss + martin - the origin of galaxies.milk


milkdroppreset.cpp
lBlitFramebuffer(0, 0, renderContext.viewportSizeX, renderContext.vie

    int width = initialWindowBounds.w;
    int height = initialWindowBounds.h;

SDL_Log("Found audio capture device %d: %s", i, SDL_GetAudioDeviceName(i, true));


winners;
INFO: Displaying preset: ./presets/presets-cream-of-the-crop/Reaction/Liquid Ripples/suksma - satanic teleprompter - nothing has will, stop pretending.milk

INFO: Displaying preset: ./presets/presets-cream-of-the-crop/Supernova/Stars/324.milk

INFO: Displaying preset: ./presets/presets-cream-of-the-crop/Supernova/Radiate/$$$ Royal - Mashup (355).milk




benchmarking
perf record -g src/sdl-test-ui/projectM-Test-UI
perf report -g 'graph,0.5,caller'