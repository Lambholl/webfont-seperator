import os, re, uuid
from fontTools.ttLib import TTFont

# 设置项  Settings
css_file = 'notosanssc.css'   # 对应的谷歌 Webfont css 文件
css_out  = 'sarasa-gothic-sc.css'  # 输出的 css 文件
font_file = 'sarasa-gothic-sc-regular.ttf'   #字体输入文件名
font_out  = 'sarasa-gothic-sc-regular-{0}.'  #字体输出文件名模板
dir_out = 'SarasaGothicSC'  # 字体输出文件夹
dir_url = '/fonts/SarasaGothicSC/' # 存储字体文件的路径的访问地址 (记得允许跨域访问)
font_family = 'Sarasa Gothic SC'  # 字体名称
font_style  = 'normal'            # 字体样式名称 可选 normal, italic 等
font_weight = 'normal'

# 代码区  Codings

with open(css_file, 'r', encoding='utf-8') as fb:
    origin_css = fb.read()
    fb.close()

p = '(?<=unicode-range: ).+?(?=;)'
pp = re.compile(p)
ranges = pp.findall(origin_css)

os.makedirs(dir_out, exist_ok=True)

a = -1
thread_processing = 0

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
            '/*' + str(a) + '*/',
            '@font-face {',
            '  font-family: \''+font_family+'\';',
            '  font-style: '+font_style+';',
            '  font-weight: '+font_weight+';',
            '  src: url('+dir_url+outfilename+'woff) format(\'woff\'),',
            '       url('+dir_url+outfilename+'woff2) format(\'woff2\');',
            '  unicode-range: '+i.replace(',', ', ')+';',
            '}'
        ]:
            fb.write(line+'\n')
        fb.close()

for i in [i.replace(', ', ',') for i in ranges]:
    produce(i)
    
