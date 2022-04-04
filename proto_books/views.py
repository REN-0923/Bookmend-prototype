
from django.shortcuts import redirect, render, get_object_or_404

from .forms import BookmarkForm, BookmarkEditForm, TagForm
from .models import BookmarkModel
import requests
from bs4 import BeautifulSoup
import MeCab
import json
from collections import Counter
from pytrends.request import TrendReq
# Create your views here.



def create(request):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            #BeautifulSoupでタイトル取得
            r = requests.get(bookmark.site_url)
            soup = BeautifulSoup(r.text, 'html.parser')
            title=soup.find("title")
            bookmark.site_title = title.text

            #MeCabでキーワード取得
            m = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/ipadic")
            nouns_with_symbols = [line.split()[0] for line in m.parse(title.text).splitlines()
               if "名詞" in line.split()[-1]]
            symbol_list = ['-', ',', '.', '|', ';', ':', '_', '*', '(', ')', '/','#']
            nouns_list = [n for n in nouns_with_symbols if n not in symbol_list]
            bookmark.site_keyword = json.dumps(nouns_list, ensure_ascii=False)
                                                        #TODO:jsonで日本語が/uXXXXX/になるのを防ぐ。必要？
            
            bookmark.save()
            return redirect('create')
    else:
        bookmark_list = BookmarkModel.objects.order_by('site_color')
        form = BookmarkForm()
        return render(request, 'create.html', {'bookmarkform':form, 'bookmark_list':bookmark_list})

def statistic(request):
    keyword_list = []
    bookmark_list = BookmarkModel.objects.all()
    for bm in bookmark_list:
        keywords_A_a = json.loads(bm.site_keyword)
        keywords_a = [x.lower() for x in keywords_A_a]
        keyword_list.extend(keywords_a)
    c = Counter(keyword_list)
    keyword_top3 = c.most_common()[:3]

    pytrend = TrendReq(hl='ja-jp',tz=540)
    related_topics = []
    for kw in keyword_top3:
        search_word = [kw[0]]
        pytrend.build_payload(kw_list=search_word, timeframe='today 3-m', geo="JP")
        topics = pytrend.related_queries()
        kw_related_topics = topics[search_word[0]]['rising']['query'].head(10)
        print(kw_related_topics.to_list)
        related_topics.append(kw_related_topics.to_list)
    return render(request, 'statistic.html', {'keyword_top3':keyword_top3, 'related_topics':related_topics})


def description(request, pk):
    bookmark = get_object_or_404(BookmarkModel, pk=pk)
    if request.method == 'POST':
        form = BookmarkEditForm(request.POST, instance=bookmark)
        if form.is_valid():
            bookmark = form.save(commit=False)
            tags_list = request.POST['hashtag'].split()
            bookmark.site_keyword = json.dumps(tags_list)
            bookmark.save()
            return redirect('create')
    else:
        bookmark_keyword_list = json.loads(bookmark.site_keyword)
        bookmark_edit_form = BookmarkEditForm(instance=bookmark)
        bookmark_keyword = ' '.join(bookmark_keyword_list)
        tag_form = TagForm(initial={'hashtag':bookmark_keyword})
        print(bookmark_keyword)
        return render(request, 'description.html', {'bookmark':bookmark, 'bookmark_keyword_list':bookmark_keyword_list, 
                                                    'bookmark_form':bookmark_edit_form, 'tag_form':tag_form})