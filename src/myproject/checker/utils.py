from django.conf import settings
import yaml
import re
import os
import cgi
import json

def _diff(out, ref):
    fout = open(out, 'r').read().strip()
    fref = open(ref, 'r').read().strip()

    print("fout = {}".format(fout))
    print("fref = {}".format(fref))
    

    lines_out = [line.rstrip() for line in fout.split('\n')]
    lines_ref = [line.rstrip() for line in fref.split('\n')]

    if (len(lines_out) != len(lines_ref)):
        return False

    for i in range(0, len(lines_out)):
        if lines_out[i] != lines_ref[i]:
            return False

    return True

def _read_config_file(problem):
    content = open(settings.APP_DIR + '/problems/{}/config.yml'.format(problem)).read()

    result = yaml.load(content, Loader=yaml.FullLoader)
    return result['time_limit'], result['mem_limit'], result['source_limit'], result['difficulty'], result['name']


def _format_problem_text(content):
    elements = json.loads(content)
    
    block = '<div class="row my-4"> <div class="col-lg-10"><strong><h4>{}</h4></strong><div>{}</div></div></div>'
    result = ''
    
    for key in elements.keys():
        result += block.format(key, elements[key])


    return result

    


# def syntax_highlight(content):
#     lines = [c + '\n' for c in content.split('\n')]
#     tags = []

#     state = 'initial'

#     data_types = r'[\(\{\[]?(int|float|double|char|bool|unsigned|long|short)'
#     paranth_statements = r'^(if|for|while|switch)(?=[^\w])'
#     space_statements   = r'^(return|do|break|continue|goto)(?=[^\w]+)'
#     bool_variables     = r'(?<=[^\w])(false|true)(?=[^\w]*)'
#     include            = r'#include.*'
#     comment = r'\/\/.*'
#     string = r'\".*\"'

#     for idx, line in enumerate(lines):
#         to_be_added = []
#         formatted = False

#         words = [c + ' ' for c in line.split(' ')]


#         for widx, word in enumerate(words):

#             if state == 'comment':
#                 tags.append((words[widx], 'gray'))
#                 state = 'comment' if '\n' not in words[widx] else 'initial'
#                 continue
#             elif state == 'include':
#                 tags.append((words[widx], 'green'))
#                 state = 'include' if '\n' not in words[widx] else 'initial'
#                 continue



#             m = re.search(comment, words[widx])
#             if m is not None:
#                 if m.start() == 0:
#                     tags.append((words[widx], 'gray'))
#                     state = 'comment' if '\n' not in words[widx] else state
#                     continue
#                 else:
#                     words.insert(widx + 1, words[widx][m.start():])
#                     words[widx] = words[widx][:m.start()]

#             m = re.search(include, words[widx])
#             if m is not None:
#                 tags.append((words[widx], 'green'))
#                 state = 'include' if '\n' not in words[widx] else state
#                 continue

#             m = re.search(data_types, words[widx])
#             if m is not None and m.start() == 0:
#                 non_alpha = ''
#                 for c in words[widx]:
#                     if not c.isalpha():
#                         non_alpha += c
#                     else:
#                         break

#                 tags.append((non_alpha, 'black'))                
#                 tags.append((words[widx].replace(non_alpha, ''), 'blue'))
#                 continue
            
#             m = re.search(paranth_statements, words[widx])
#             if m is not None:
#                 alpha = ''
#                 for c in words[widx]:
#                     if c.isalpha():
#                         alpha += c
#                     else:
#                         break

#                 tags.append((alpha, 'purple'))                
#                 words.insert(widx + 1, words[widx].replace(alpha, ''))
#                 continue

#             m = re.search(space_statements, words[widx])
#             if m is not None:
#                 if not m.group(0)[-1].isalpha():
#                     tags.append((m.group(0)[:-1], 'purple'))
#                     tags.append((words[widx][m.end() - 1:], 'black'))
#                 else:
#                     tags.append((words[widx], 'purple'))

#                 continue

#             m = re.search(string, words[widx])
#             if m is not None:
#                 if m.end() - m.start() == len(words[widx]):
#                     print('perf match {}'.format(words[widx]))
#                     tags.append((words[widx], '#BDB76B'))
#                     continue
#                 else:
#                     print('meh match {} in {}'.format(m.group(0), words[widx]))
#                     print('#0 {}'.format(words[widx]))
#                     words.insert(widx + 1, words[widx][m.start() : m.end()])
#                     print('#1 {}'.format(words[widx + 1]))
#                     words.insert(widx + 2, words[widx][m.end():])
#                     print('#2 {}'.format(words[widx + 2]))
#                     words[widx] = words[widx][:m.start()]


#             m = re.search(bool_variables, words[widx])
#             if m is not None:
#                 non_alpha = ''
#                 ended = 0
#                 leng = 0
#                 for c in words[widx]:
#                     if not c.isalpha():
#                         non_alpha += c
#                         ended += 1
#                     else:
#                         break
                
#                 for c in words[widx][ended:]:
#                     if c.isalpha():
#                         leng += 1
#                     else:
#                         break


#                 tags.append((non_alpha, 'black'))                
#                 tags.append((words[widx][ended : ended + leng], 'blue'))
#                 words.insert(widx + 1, words[widx][ended + leng:])
#                 continue
            

            
#             tags.append((words[widx], 'black'))

#     result = '<div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%">'
#     for tag in tags:
#         result += '<span style="color:{}">{}</span>'.format(tag[1], cgi.escape(tag[0]))

#     result += '</pre></div>'
#     return result



