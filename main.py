import os

import pkuseg  # https://github.com/lancopku/pkuseg-python, you can change it to any other word cutter
import io

path = input()
(base_name, dir_name) = os.path.split(path)

with open(path, encoding='utf-8') as f:
    text = f.read()


class Punctuation:
    from_ = '〈《「『【〔〖〝（．［｛、。〉》」』】〕〗〞！＂％＇），．：；？］｀｜｝～“”'
    to = '""""[[["(.[{,.""""]]]"!"%\'),.:;?]`|}~""'

    pause = ',.:;?!'

    trans_table = str.maketrans(from_, to)


result_writer = io.StringIO()

magic = '𗀀'  # 一般通过西夏字
text = text.replace('\n', '\n' + magic + '\n')  # workaround

seg = pkuseg.pkuseg(postag=True)
cut_result = seg.cut(text)

prev_is_pause = False  # ".", ","
prev_is_character = False

for seg in cut_result:
    if seg[0] == magic:
        prev_is_pause = False
        prev_is_character = False

        result_writer.write('\n')
    elif seg[1] == 'w':
        unified = seg[0].translate(Punctuation.trans_table)

        if unified in Punctuation.pause:
            prev_is_pause = True
        else:
            if prev_is_pause:
                result_writer.write(' ')
            prev_is_pause = False
        prev_is_character = False

        result_writer.write(unified)
    else:
        if prev_is_pause or prev_is_character:
            result_writer.write(' ')
        prev_is_pause = False
        prev_is_character = True

        result_writer.write(seg[0])

result = result_writer.getvalue()

result_path = os.path.join(base_name, 'separated_' + dir_name)

with open(result_path, 'w', encoding='utf-8') as f:
    f.write(result)
