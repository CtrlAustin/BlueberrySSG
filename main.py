from pathlib import Path

md_path = 'content/'
htm_path = 'out/site/'
templates_path = 'templates/'
outfile = ''
generatedContent = ''

use_default_boilerplate = False
title = ''


metalines = False

def saveHTML():
    Path(htm_path).mkdir(parents=True, exist_ok=True)
    file = open(htm_path + "index.html", "w")
    file.write(outfile)
    file.close()
    
def injectContent(content):
    # for i in content.split():
    content.strip()
    if '{{ content }}' in content:
        x = content.replace('{{ content }}', generatedContent + '\n')
    return x



f = open(md_path + 'index.md', 'r')
# print(f.read())
for i in f:
    if i == '---\n':
        if metalines:
            metalines=False
        else:
            metalines=True
    else:
        if metalines:
            if 'title' in i:
                title = i.strip().split(':'[0])
                title = (str(title[1]))
        else:
            if '<' in i:
                generatedContent += i #+ '\n'
            elif '</' in i:
                generatedContent += i+ '\n'
            elif i == "\n":
                generatedContent += i
            else:
                tag = "p"
                print('<' + tag + '>' + i.strip() + '</' + tag + '>')
                generatedContent += '<' + tag + '>' + i.strip() + '</' + tag + '>'+ '\n'

f.close()

f = open(templates_path + 'base.blu', 'r')
for i in f:
    if '{{' in i:
        print("found variable")
        # var = i.strip().split('{{ '[0])
        # var = (str(var[2]))
        # print(var)

        if 'content' in i:
            outfile = outfile + injectContent(i)
        if 'title' in i:
            outfile = outfile + title
    else:
        outfile = outfile + i


print(outfile)
saveHTML()

