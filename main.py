import sys
import getopt
import pypinyin
import bibtexparser


IN_CHINESE_MARK = "---"
IN_CHINESE_WITH_ENGLISH_ABSTRACT_MARK = "----"
AUTHOR_DELIMITERS = ["and", "，", ","]


def is_chinese(target_string):
    return any('\u4e00' <= c <= '\u9fff' for c in target_string)


def split_authors(authors):
    for delimiter in AUTHOR_DELIMITERS:
        if delimiter in authors:
            # 此处假设不存在此种可能：即作者名中有中文名和英文名，且英文名所用分隔符和作者之间分隔符相同。
            # 亦假设每个参考文献的各作者之间的分隔符相同。
            authors = authors.split(delimiter)
            break
    return authors


def chinese_name2pinyin(name):
    name_pinyin = ""
    pinyin_list = pypinyin.pinyin(name, pypinyin.NORMAL)
    for i, pinyin in enumerate(pinyin_list):
        pinyin = pinyin[0]
        if i < 2:
            pinyin_upper = pinyin[0].upper() + pinyin[1:]
        else:
            pinyin_upper = pinyin
        name_pinyin += pinyin_upper
        if i == 0:
            name_pinyin += ", "
        else:
            name_pinyin += ""
    return name_pinyin


def bib2str(bib_item):
    entry_type = bib_item["ENTRYTYPE"]
    id = bib_item["ID"]
    result = f"@{entry_type}{{{id},\n"
    for k, v in bib_item.items():
        if k == "ENTRYTYPE" or k == "ID":
            continue
        else:
            result += f"\t{k} = {{{v}}},\n"
    result += "}\n"
    return result


def process_mark(bib_entries):
    for bib_item in bib_entries:
        if bib_item["title"].endswith(IN_CHINESE_WITH_ENGLISH_ABSTRACT_MARK):
            bib_item["title"] = bib_item["title"].replace(
                IN_CHINESE_WITH_ENGLISH_ABSTRACT_MARK, "")
            bib_item["language"] = "zh"
            bib_item["short title"] = "mark"
        elif bib_item["title"].endswith(IN_CHINESE_MARK):
            bib_item["title"] = bib_item["title"].replace(
                IN_CHINESE_MARK, "")
            bib_item["language"] = "zh"
        elif "language" in bib_item:
            bib_item.pop("language")
    return bib_entries


def process_author(bib_entries):
    for bib_item in bib_entries:
        authors = bib_item["author"]
        bib_item["author"] = authors.replace("-", " ")
        if is_chinese(authors):
            authors = split_authors(authors)
            authors_pinyin = []
            if str(type(authors)) == "<class 'list'>":
                for author in authors:
                    if is_chinese(author):
                        author = chinese_name2pinyin(author.split())
                    authors_pinyin.append(author)
                bib_item["author"] = " and ".join(authors_pinyin)
            else:
                bib_item["author"] = chinese_name2pinyin(authors.split())
    return bib_entries


def bib_entries2str(bib_entries):
    for bib_item in bib_entries:
        result = bib2str(bib_item)
        yield result


def process_bib_file(path, path_output):
    with open(path, "r", encoding="utf8") as f:
        bib_data = bibtexparser.load(f)
    bib_entries = bib_data.entries
    bib_entries = process_mark(bib_entries)
    bib_entries = process_author(bib_entries)
    with open(path_output, "w", encoding="utf8") as f:
        for bib_str in bib_entries2str(bib_entries):
            f.write(bib_str)


def main(argv):
    """
        通过 getopt模块 来识别参数,
    """

    input = ""
    output = ""

    try:
        """
            options, args = getopt.getopt(args, shortopts, longopts=[])

            参数args：一般是sys.argv[1:]。过滤掉sys.argv[0]，它是执行脚本的名字，不算做命令行参数。
            参数shortopts：短格式分析串。例如："hi:o:"，h后面没有冒号，表示后面不带参数；i和o后面带有冒号，表示后面带参数。
            参数longopts：长格式分析串列表。例如：["help", "ip=", "port="]，help后面没有等号，表示后面不带参数；ip和port后面带冒号，表示后面带参数。

            返回值options是以元组为元素的列表，每个元组的形式为：(选项串, 附加参数)，如：('-i', '192.168.0.1')
            返回值args是个列表，其中的元素是那些不含'-'或'--'的参数。
        """
        opts, args = getopt.getopt(argv, "hi:o:", ["help", "input=", "output="])
    except getopt.GetoptError:
        print('Error: getReference.py -i <input> -o <output>')
        print('   or: getReference.py --input=<input> --output=<output>')
        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Error: getReference.py -i <input> -o <output>')
            print('   or: getReference.py --input=<input> --output=<output>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input = arg
        elif opt in ("-o", "--output"):
            output = arg
            
    try:
        process_bib_file(path=input, path_output=output)
    except:
        print('Error: getReference.py -i <input> -o <output>')
        print('   or: getReference.py --input=<input> --output=<output>')
        sys.exit()


if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    main(sys.argv[1:])