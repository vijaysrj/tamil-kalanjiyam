import glob, re, sys, subprocess
import os
R = os.path.dirname(os.path.abspath(__file__)) + '/'
cat = lambda d: ''.join(open(p, encoding='utf-8').read() for p in sorted(glob.glob(R + d + '/*.html')))
html = cat('parts')
anchors = [
 ("மிகப் பழைய மனிதத் தடங்களில் இதுவும் ஒன்று.", "pappu"),
 ("ஆய்வுலகில் இதன் மீதான மதிப்பாய்வு தொடர்கிறது.", "iron"),
 ("வாழ்வுக்கு இது தொல்லியல் சான்று.", "keeladi"),
 ("அண்டை நாடுகளாகக் குறிப்பிடுகின்றன.", "sastri"),
 ("குவியல் குவியலாகக் கிடைத்துள்ளன.", "karashima"),
 ("கிடைத்துள்ள சங்க இலக்கியம் வரலாற்று உண்மை.", "lemuria"),
 ("தோன்றியதும் இக்காலத்தை ஒட்டியே.", "mayilai"),
 ("விதிகளைப் பதிவு செய்கிறது.", "sastri"),
 ("(கடாரம்) மீது படையெடுத்தான்.", "sastri"),
 ("இந்திய எழுத்தில் அச்சான முதல் நூல் அது.", "blackburn"),
 ("பதிப்பித்ததால் சங்க இலக்கியம் மீண்டது.", "uvesa"),
 ("1937இல் முதல் இந்தித் திணிப்பு எதிர்ப்புப் போராட்டம்.", "geetha"),
 ("தொழில் வளர்ச்சி ஆகியவை இக்காலத்தின் அடையாளம்.", "dravmodel"),
 ("இரு கட்சி மாற்று ஆட்சி முறை முடிவுக்கு வந்தது.", "election"),
 ("வரை யாழ்ப்பாண அரசு நிலவியது.", "indrapala"),
 ("யாழ்ப்பாணப் பொது நூலகம் எரிக்கப்பட்டது.", "knuth"),
 ("லட்சக்கணக்கானோர் புலம்பெயர்ந்தனர்.", "unpanel"),
 ("பிராகுயி மொழியும் இக்குடும்பமே.", "krishnamurti"),
 ("எட்டுக் கோடிக்கும் மேற்பட்டோர் தமிழ் பேசுகின்றனர்.", "census"),
 ("பானை ஓடுகளிலும் காணப்படுகிறது.", "mahadevan"),
 ("சேர்ந்து ஐந்திலக்கணம் ஆயிற்று.", "tolk"),
 ("சங்கப் பாடலைப் புரிந்துகொள்ள இதுவே திறவுகோல்.", "ramanujan"),
 ("'நமஸ்காரம்' வணக்கம் ஆனதும் இதன் விளைவு.", "ramaswamy"),
 ("1856இல் கால்டுவெல் திராவிட மொழிக் குடும்பத்தை நிறுவினார்.", "caldwell"),
]
for a, k in anchors:
    if html.count(a) != 1:
        sys.exit('anchor count %d: %s' % (html.count(a), a))
    html = html.replace(a, a + '<sup data-s="%s"></sup>' % k)
i = html.index('<main>') + len('<main>'); j = html.index('</main>')
ta = html[i:j]; en = cat('parts-en')
html = html[:i - len('<main>')] + '<main id="main"></main>\n<template id="tpl-ta">' + ta + '</template>\n<template id="tpl-en">' + en + '</template>\n' + html[j + len('</main>'):]

src = set(l.split('|')[0] for l in html.split('id="srcdata">')[1].split('</script>')[0].strip().split('\n'))
ids = set(re.findall(r'data-s="([^"]+)"', html))
print('missing sources:', ids - src, 'unused:', src - ids)
rows = lambda t: t.split('id="litdata">')[1].split('</script>')[0].strip().split('\n')
lt, le = rows(ta), rows(en)
print('works ta/en:', len(lt), len(le), 'bad:', [l for l in lt + le if l.count('|') != 5][:3],
      'order mismatch:', [(n, a.split('|')[0], b.split('|')[0]) for n, (a, b) in enumerate(zip(lt, le)) if a.split('|')[0] != b.split('|')[0] or a[-1] != b[-1]][:5])
def shape(t):
    return [(v, len(re.findall('<h2', body)), len(re.findall('data-s=', body))) for v, body in re.findall(r'<section class="view" id="v-(\w+)">(.*?)</section>', t, re.S)]
st, se = shape(ta), shape(en)
print('views ta:', st); print('views en:', se)
open(R + '../index.html', 'w', encoding='utf-8').write(html)
print('bytes', len(html.encode()))
for n, blk in enumerate(re.findall(r'<script>(.*?)</script>', html, re.S)):
    open('/tmp/s%d.js' % n, 'w').write(blk)
    print('script', n, subprocess.run(['node', '--check', '/tmp/s%d.js' % n], capture_output=True, text=True).stderr[:400] or 'ok')
