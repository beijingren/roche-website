# coding=utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import TextAnnotationForm


INITIAL_TEXT = u"""歐陽修，字永叔，廬陵人。四歲而孤，母鄭，守節自誓，親誨之學，家貧，至以荻畫地學書。幼敏悟過人，讀書輒成誦。及冠，嶷然有聲。

宋興且百年，而文章體裁，猶仍五季余習。鎪刻駢偶，淟涊弗振，士因陋守舊，論卑氣弱。蘇舜元、舜欽、柳開、穆修輩，咸有意作而張之，而力不足。修游隨，得唐韓愈遺稿於廢書簏中，讀而心慕焉。苦志探賾，至忘寢食，必欲並轡絕馳而追與之並。
"""

def index(request):
    
    if request.method == 'POST':
        pass
    else:
        form = TextAnnotationForm(initial={'text': INITIAL_TEXT})

    data = {'form': form }
    return render_to_response('annotate/index.html', data, context_instance=RequestContext(request))
