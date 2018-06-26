"""
Split (part of Sonic Waves)

started 22.03.18
by Bushuev Ilya

updated 03.07.18

function: file => splitted
"""

import re

AG1 = 1
AG2 = 2
AG3 = 3

COMMENT = r'@.*[\n$]?'
BEG_TEXT = r'^'
END_TEXT = r'$'
NAME = r'"(.*)"'
BEG_SEQ = r':'
COMMAND = r'([^\.]*)'
END_SEQ = r'\.'
MB_SPACES = r'\s*'
MB_TAB_SP = r'[\t ]*'
PHRASE = (BEG_TEXT + MB_SPACES + NAME + MB_TAB_SP +
          BEG_SEQ + MB_SPACES + COMMAND +
          MB_SPACES + END_SEQ + MB_SPACES)

TEMPO = BEG_TEXT + r'(tempo)=(\d{1,3})' + END_TEXT
VALUE = BEG_TEXT + r'(value)=(\d{1,2})' + END_TEXT
SOUND = r'([CDEFGAH][#b]?[0-9])'
MB_VAL = r'(:\d{1,2})?'
MB_DUR = r'(\*\d)?'
NOTE = BEG_TEXT + SOUND + MB_VAL + MB_DUR + END_TEXT


def split_file(name, echo=True):
    # file into text
    with open(name, 'r') as file:
        orig_text = file.read()

    # reduce all comments
    no_comment_text = re.sub(COMMENT, r'\n', orig_text)

    # define reg exps
    re_phrase = re.compile(PHRASE)  # Args 1 name, 2 command
    re_tempo = re.compile(TEMPO)  # Args 1 re_tempo, 2 value
    re_value = re.compile(VALUE)  # Args 1 re_value, 2 value
    re_note = re.compile(NOTE)  # Args 1 sound, 2 value, 3 duration

    # common circle - split names and commands
    names = []
    commands = []
    if echo:
        print('Your file\n===\n', orig_text, '\n===')
        print('Without comments\n===\n', no_comment_text, '\n===')
        print('Searching...')
    sliced_text = no_comment_text
    found = re_phrase.search(sliced_text)
    if found:
        while found:
            names.append(found.group(AG1))
            commands.append(found.group(AG2))
            sliced_text = sliced_text[found.end():]
            print('Found', found.group(AG1))
            found = re_phrase.search(sliced_text)
        else:
            print('No more phrases.\n===')
    else:
        print('No phrases.\n===')

    # commands circle - converting string to list of tuples
    i = 0
    failed = False
    while i < len(commands) and not failed:
        commands_i = commands[i]
        commands_i = re.sub(r' ', r'', commands_i)
        commands_i = re.split(r'[,\n]+', commands_i)
        j = 0
        while j < len(commands_i) and not failed:
            s = commands_i[j]
            tp = None
            if re_tempo.search(s):
                found = re_tempo.search(s)
                tp = (found.group(AG1), int(found.group(AG2)))
            elif re_value.search(s):
                found = re_value.search(s)
                tp = (found.group(AG1), int(found.group(AG2)))
            elif re_note.search(s):
                found = re_note.search(s)
                snd = found.group(AG1)
                val = int(found.group(AG2)[1:]) if found.group(AG2) else None
                dur = int(found.group(AG3)[1:]) if found.group(AG3) else None
                dc = {'snd': snd, 'val': val, 'dur': dur}
                tp = ('note', dc)
            else:
                failed = True
            if not failed:
                commands_i[j] = tp
            j += 1
        if not failed:
            commands[i] = commands_i
        i += 1
    if failed:
        print('COMMAND FAIL')

    # temp riffs output
    riffs = dict(zip(names, commands))
    for name, value in riffs.items():
        print(name)
        print(value, '\n')
    return riffs
