"""
Written by:
    Ilya Bushuev @scorpthe
Date:
    22.03.2018
Description:
    Version 0.3R [regular]:
        file   -> string,
        string -> names, commands
        names, commands -> riffs.
"""

import re

# CONSTANTS

AG1 = 1
AG2 = 2
AG3 = 3

COMMENT = r'@.*[\n$]?'

BEG_TEXT = r'^'
NAME = r'"(.*)"'
BEG_SEQ = r':'
COMMAND = r'([^\.]*)'
END_SEQ = r'\.'

MB_SPACES = r'\s*'
MB_TAB_SP = r'[\t ]*'

SEQ = (BEG_TEXT + MB_SPACES + NAME + MB_TAB_SP +
        BEG_SEQ + MB_SPACES + COMMAND +
        MB_SPACES + END_SEQ + MB_SPACES)

BPM = r'(bpm)=(\d{1,3})'
DIV = r'(div)=(\d{1,2})'

SOUND = r'([CDEFGAH][#b]?[2-9])'
MB_VAL = r'(:\d{1,2})?'
MB_DUR = r'(\*\d)?'
NOTE = r'^' + SOUND + MB_VAL + MB_DUR + r'$'

def parseFileToRiffs(name):
    # file into text
    orig_text = ''
    with open(name,'r') as file:
        orig_text = file.read()
    # reduce all comments
    nocom_text = re.sub(COMMENT, r'\n', orig_text)
    # define reg exps
    seq = re.compile(SEQ) # Args 1 name, 2 command
    bpm = re.compile(BPM) # Args 1 bpm, 2 value
    div = re.compile(DIV) # Args 1 div, 2 value
    note = re.compile(NOTE) # Args 1 sound, 2 value, 3 duration
    # common circle - split names and commands
    names = []
    commands = []
    print('Your file\n===\n',orig_text,'\n===')
    print('Without comments\n===\n',nocom_text,'\n===')
    print('Searching...')
    sliced_text = nocom_text
    found = seq.search(sliced_text)
    if found:
        while found:
            names.append(found[AG1])
            commands.append(found[AG2])
            sliced_text = sliced_text[found.end():]           
            print('Found',found[AG1])
            found = seq.search(sliced_text)
        else:
            print('Sequence stoped.\n===')
    else:
        print('No sequences.\n===')
    # commands circle - converting string to list of tuples
    i = 0
    failed = False
    while i < len(commands) and not failed:
        cmds = commands[i]
        cmds = re.sub(r' ', r'', cmds)
        cmds = re.split(r'[,\n]+', cmds)
        j = 0
        while j < len(cmds) and not failed:
            s = cmds[j]
            tp = None
            if bpm.search(s):
                found = bpm.search(s)
                tp = (found[1], int(found[AG2]))
            elif div.search(s):
                found = div.search(s)
                tp = (found[1], int(found[AG2]))
            elif note.search(s):
                found = note.search(s)
                snd = found[1]
                val = int(found[AG2][1:]) if found[AG2] else None
                dur = int(found[AG3][1:]) if found[AG3] else None
                dc = {'snd':snd, 'val':val, 'dur':dur}
                tp = ('note', dc)
            else:
                failed = True
            if not failed:
                cmds[j] = tp
            j += 1
        if not failed:
            commands[i] = cmds
        i += 1
    if failed:
        print('COMMAND FAIL')
    # temp riffs output
    riffs = {}
    riffs = dict(zip(names,commands))
    for name, value in riffs.items():
        print(name)
        print(value,'\n')
    return riffs
