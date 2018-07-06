EXECUTABLE:
notation +    
sonic +
player +
split +    
music +
fun +-

FUTURE UPDATES:
    (add args)
        sonicwaves  --help
                    --gui
                    --file music.son
                                        --all
                                        --mark First
                                                        --post
                                                        --live
                                                        --todata music.dat
                                                        --towave music.wav
                   --data music.dat
                                       --post
                                       --towave music.wav
                   --wave music.wav
                   --scale Am
                   --keyboard
                   --commands
    (add sustain notes)
        sustain -> (A4*16)*4
        note    -> A4*4
        chord   -> (A4 A5)*4
    (add re in notation)    
    (add command-player)
    (add keyboard-player)
    (add noise generation)
        def make_noise(self, wavelength, time, amplitude)
    (parallel marks playing)
        when --all -> play marks parallel (sum of their waves)
    (add wave coefs in percents)
        imput  -> waves = 10.10.10.10
        output -> waves = (10, 10, 10, 10)
    (add scales)
    (add notification about out-of-scale notes)
    (add improvisation using licks and patterns)
    (write to .wav file)
    (write to .data file)
    (replace sonic fuctions in fun)
    (add pytests)


KNOWN BAD CASES:
@Test,
FOR, C4, FOR, D4, REP=0, REP=0, => EndlessLoop
@Test,
REP=1, REP=1, FOR, C4, FOR, D4, => IndexError