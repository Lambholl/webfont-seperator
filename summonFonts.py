import os, re, uuid

# 设置项  Settings
css_file = 'notosanssc.css'   # 对应的谷歌 Webfont css 文件
css_out  = 'sarasa-gothic-sc.css'  # 输出的 css 文件
font_file = 'sarasa-gothic-sc-regular.ttf'   #字体输入文件名
font_out  = 'sarasa-gothic-sc-regular-{0}.'  #字体输出文件名模板
dir_out = 'SarasaGothicSC'  # 字体输出文件夹
dir_url = 'https://www.example.com:443/Fonts/SarasaGothicSC/' # 存储字体文件的路径的访问地址 (记得允许跨域访问)
font_family = 'Sarasa Gothic TC'  # 字体名称

# 代码区  Codings

with open(css_file, 'r', encoding='utf-8') as fb:
    origin_css = fb.read()
    fb.close()

p = '(?<=unicode-range: ).+?(?=;)'
pp = re.compile(p)
ranges = pp.findall(origin_css)

os.makedirs(dir_out, exist_ok=True)

a = 0
for i in [i.replace(', ', ',') for i in ranges]:
    outfilename = font_out.format(str(uuid.uuid4()))
    for n in ['woff']:
        cmd = 'pyftsubset "'+font_file+'" --ignore-missing-glyphs "--unicodes='+i+'" --output-file="'+dir_out+'/'+outfilename+n+'"'
        os.system(cmd)
    with open(css_out, 'a', encoding='utf-8') as fb:
        for line in [
            '/*' + str(a) + '*/',
            '@font-face {',
            '  font-family: \''+font-family+'\';',
            '  font-style: normal;',
            '  src: url('+dir_url+outfilename+'woff) format(\'woff\');',
            '  unicode-range: '+i.replace(',', ', ')+';',
            '}'
        ]:
            fb.write(line+'\n')
        fb.close()
    a += 1
