from pathlib import Path
import os
import glob

md_path = 'content/'
htm_path = 'out/site/'
templates_path = 'templates/'
outfile = ''
generatedContent = ''
blogdirectory = 'content/blog/'
md_files = glob.glob(os.path.join(blogdirectory, '*.md'))


use_default_boilerplate = False
title = ''


metalines = False

def saveHTML():
    Path(htm_path).mkdir(parents=True, exist_ok=True)
    file = open(htm_path + "index.html", "w")
    file.write(outfile)
    file.close()
    
def injectContent(content):
    content.strip()
    if '{{ content }}' in content:
        x = content.replace('{{ content }}', generatedContent + '\n')
    return x

def createTag(content, htmltag):
    return '<' + htmltag + '>' + content + '</' + htmltag + '>'+ '\n'
    # print('<' + tag + '>' + content + '</' + tag + '>')

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
                generatedContent += createTag(i.strip(), "p")

f.close()

basefile = open(templates_path + 'base.blu', 'r')
for line in basefile:
    if '{{' in line:
        tag = line.replace(' ', '').replace('}', '').replace('{', '').strip()
        tag = tag.split('|')
        print(tag)

        # add a way to get the title of file paths and create functions per result
        if tag[0] == 'title':
            outfile = outfile + title

        if tag[0] == 'content':
            if len(tag) > 1:
                if tag[1] == 'list':
                    for file_path in md_files:
                        # print(f'Contents of {file_path}:')
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            # print(content)
                            outfile = outfile + content
                            # print('-' * 40)  # Separator for readability
                            outfile = outfile + '\n' + ('-' * 40) + '\n'
            else: 
                outfile = outfile + generatedContent
        else: outfile = outfile + generatedContent

    else:
        outfile = outfile + line
        # pass

f



# print(outfile)
# print(outfile)
saveHTML()

