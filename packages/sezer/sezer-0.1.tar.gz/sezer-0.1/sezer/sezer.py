me_as_ascii = """
MMMMMMMMMNXOdc;'......';lodk0XWMMMMMMMMM
MMMMMMWKOdl:'...........,:clox0XNWMMMMMM
MMMMWXkdoddl,...'........;oxxkOkO0XWMMMM
MMWXOxdddxxl'';;;::cclol,;oddddkO0KXWMMM
MW0dllllllo:'''',:c:;;cdl;clc:lkXXXXXWMM
WOo:clllllol,....;:...'lxdodlccxXXXXXNWM
KxkdokOkxxkxc'...;ol::lxOkoloocdXXKXNXXW
KOX0OKXOxxOOkoc;,;ldxxxkOdc:oo:o0K00XNNN
KKNKOO0kdoolc:;;,';loollxkdcc:;lOXXXNNNN
KKNXkodo:,;,'....,;::cllodkxc'.':dKNNNNN
XKXXkl:,.........;;:::cloxOkl'...,oKNNNW
XKKXOc...........;:::cloodkkxl'...,dXNNW
NXXNO:..........,;:clooc:cdO0kl,..';xKNW
WWNN0:.........,;:codo;...;okOOx:,'':xXW
MWNKd,.......';clll:;'......;oxkkdo:;xNM
MMWO:.......,;ldl;...........,coxxOO0NMM
MMMNk:....',;cdl,.............,cox0NWMMM
MMMMMNkl;,,;coc'...............:xKWMMMMM
MMMMMMMWXOdddc.............';lxKWMMMMMMM
MMMMMMMMMMWNKd:'........':okXWMMMMMMMMMM

"""

tr = """
Merhaba ben Sezer Bozkır,
Kendimi bildim bileli bilgisayar denilen kutunun başında, teknolojiyi takip edip “daha fazla ne olabilir?” sorusu üzerine çalışıyorum. Özellikle GNU/Linux ve python ile uğraşıyorum. Şu an Python ve GNU/Linux server üzerine kendimi geliştiriyorum. Photoshop ile yıllarımı geçirdiğimden derdimi anlatabilecek kadar Photoshop biliyorum. Yalova Üniversitesi’nde Bilgisayar mühendisliği okudum. Huawei Turkiye, Umraniye ofisinde R&D  ekibinde, backend developer olarak python geliştiricisi unvaniyla gorev aliyorum.

Motosiklet tutkunuyum. Sancak chopper motosiklet kulubune uye ve Meclisinde gorev aliyorum. Uzun surusler yapip yollarin tadini cikariyorum. Ekstra olarak teknoloji hakkında döküman okuyorum, ilgimi çeken her konuda sorularıma ağız dolusu cevap verebilene kadar araştırıp öğrenmeye gayret ediyorum, bunlardan paylaşmaya değer bulduklarımı döküman haline getirip paylaşıyorum.

iletişim için: admin@sezerbozkir.com
website: https://sezerbozkir.com
"""

en = """
Hello, I'm Sezer Bozkir,
Ever since I can remember, I have been working on the box called computer, following the technology and working on the question of "what can be more?" I am especially interested in GNU/Linux and python. I am currently developing myself on Python and GNU/Linux server. I know enough Photoshop to explain my problem since I spent years with Photoshop. I studied Computer Engineering at Yalova University. Huawei Turkey, Umraniye office in the R&D team, backend developer in the title of python developer.

I am a motorcycle enthusiast. I am a member of Sancak chopper motorcycle club and I take part in its council. I make long rides and enjoy the roads. In addition, I read documents about technology, I try to research and learn until I can answer my questions on every subject that interests me, I document and share the ones I find worth sharing.

contact: admin@sezerbozkir.com
website: https://sezerbozkir.com
"""


def whoami(lang="tr"):
    print(me_as_ascii)
    if lang == "tr":
        print(tr)
    else:
        print(en)