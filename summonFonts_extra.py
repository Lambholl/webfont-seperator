import os, re, uuid, math
from fontTools.ttLib import TTFont

# 设置项  Settings
css_files = ['notosanshk.css','notosanstc.css','notosanssc.css']   # 对应的谷歌 Webfont css 文件
css_file = 'notosansjp.css'
css_out  = 'sarasa-gothic-j.css'  # 输出的 css 文件
font_file = 'sarasa-gothic-j-regular.ttf'   #字体输入文件名
font_out  = 'sarasa-gothic-j-regular-{0}.'  #字体输出文件名模板
dir_out = 'SarasaGothicJ'  # 字体输出文件夹
dir_url = '/fonts/SarasaGothicJ/' # 存储字体文件的路径的访问地址 (记得允许跨域访问)
font_family = 'Sarasa Gothic J'  # 字体名称
font_style  = 'normal'            # 字体样式名称 可选 normal, italic 等
font_weight = 'normal'

# 代码区  Codings
all_ranges = []
for i in css_files:
    with open(i, 'r', encoding='utf-8') as fb:
        origin_css = fb.read()
        fb.close()
    p = '(?<=unicode-range: ).+?(?=;)'
    pp = re.compile(p)
    ranges = pp.findall(origin_css)
    for range0 in ranges:
        for range1 in range0.split(', '):
            if not range1 in all_ranges:
                all_ranges.append(range1)
with open(css_file, 'r', encoding='utf-8') as fb:
    origin_css = fb.read()
    fb.close()
p = '(?<=unicode-range: ).+?(?=;)'
pp = re.compile(p)
ranges0 = pp.findall(origin_css)
ranges1 = []
for range0 in ranges0:
    for range1 in range0.split(', '):
        if not range1 in ranges1:
            ranges1.append(range1)
ranges_append = [i for i in all_ranges if not i in ranges1]

os.makedirs(dir_out, exist_ok=True)

a = -1

def produce(i):
    global a
    a += 1
    outfilename = font_out.format(str(uuid.uuid4()))
    cmd = 'pyftsubset "'+font_file+'" --ignore-missing-glyphs "--unicodes='+i+'" --output-file="'+outfilename+'ttf"'
    os.system(cmd)
    with TTFont(outfilename+'ttf') as f:
        for n in ['woff', 'woff2']:
            f.flavor = n
            f.save(dir_out+'/'+outfilename+n)
    os.remove(outfilename+'ttf')
    with open(css_out, 'a', encoding='utf-8') as fb:
        for line in [
            '/*E' + str(a) + '*/',
            '@font-face {',
            '  font-family: \''+font_family+'\';',
            '  font-style: '+font_style+';',
            '  font-weight: '+font_weight+';',
            '  src: url('+dir_url+outfilename+'woff2) format(\'woff2\'),',
            '       url('+dir_url+outfilename+'woff) format(\'woff\');',
            '  unicode-range: '+i.replace(',', ', ')+';',
            '}'
        ]:
            fb.write(line+'\n')
        fb.close()

ranges2 = []
for i in range(math.ceil(len(ranges_append)/125)):
    n = ranges_append[i*125:(i+1)*125]
    e = ''
    for b in n:
        e += b+','
    produce(e[:-1])

