## 参考文献处理工具

### 1. 人名处理
本工具主要用于需要参考中文文献的情况，推荐搭配Endnote或Zotero等工具使用。工具将检测bib文件中的作者，并将其转换为拼音。
使用方法：
```
git clone https://github.com/dp0qb/ReferencesTool.git
cd ./ReferencesTool
pip install -r ./requirements.txt
python ./main.py -i <输入文件名> -o <输出文件名>
```
例如：
```
python ./main.py -i ./ref.bib -o output.bib
```
### 2. in Chinese 和 in Chinese with English Abstract 自动添加
由于部分老文献没有英文摘要，只能手动翻译。处理完成后还需添加**in Chinese**等信息，颇为繁琐。所以推荐在翻译时在手动翻译的论文名字后加上三个减号，即"---"，在使用英文摘要翻译而来的论文名字后面加上四个减号，即"----"。脚本将自动识别，去除标记后添加必要信息。

使用脚本处理得到输出后，在Zotero的csl（Citation Style Language）文件末尾"</layout>"标签前添加如下标签，即可完成in Chinese 和 in Chinese with English Abstract 的自动添加。
```
<choose>
	<if variable="language" match="any">
		<choose>
			<if variable="title-short">
				<text value=" (in Chinese with English Abstract)" suffix="."/>
			</if>
			<else>
				<text value=" (in Chinese)" suffix="."/>
			</else>
		</choose>
	</if>
</choose>
```