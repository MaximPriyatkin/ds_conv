import json
import re


def load_dict(fname: str) -> list:
    with open(fname, encoding='utf-8') as fptr:
        dt = json.load(fptr)
        return dt


def print_title(dt: list) -> str:
    err = ''
    for num, conv in enumerate(dt):
        ftitle = conv["title"].replace(' ', "_")
        ftitle = re.sub(r'[^\w\s\-\.]', '', ftitle, flags=re.UNICODE)
        # if ftitle != "Обзор_инструмента_управления_проектами_Jira":
        #    continue
        fdate = conv["inserted_at"].split("T")[0]
        fdate = fdate.replace("-", "")
        fname = f'./out/{ftitle}-{fdate}.md'
        content, error = print_content(conv["mapping"])
        if error != '' or content == '':
            err += error + '\n'
            err += ftitle + '\n'
        with open(fname, 'w+', encoding='utf-8') as fptr:
            content = f'# {conv["title"]}\n\n{content}'
            fptr.write(content)
            fptr.flush()
    return err


def print_content(dt: dict) -> str:
    out: str = ''
    error: str = ''
    for key, conv in dt.items():
        if key == 'root':
            continue
        try:
            for content in conv['message']['fragments']:
                type = content["type"]
                out += f'## {type}-{key}\n\n'
                if type == "SEARCH":
                    for search in content['results']:
                        out += search['url'] + '\n\n'
                else:
                    out += content['content'] + '\n\n'
        except Exception:
            error += f'ошибка в {key}'
    return out, error


if __name__ == '__main__':
    err = print_title(load_dict('conversations.json'))
    with open('error.log', 'w+', encoding='utf-8') as fptr:
        fptr.write(err)
