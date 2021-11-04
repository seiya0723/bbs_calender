from django.shortcuts import render,redirect

from django.views import View
from .models import Topic

import datetime

class BbsView(View):

    def get(self, request, *args, **kwargs):

        context = {}
        context["topics"]   = Topic.objects.all()


        #今月のカレンダーを表示させる。

        #今月の初日を手に入れる。
        dt  = datetime.datetime.now()
        dt  = dt.replace(day=1)

        #今月を手に入れる
        month       = dt.month

        #month_dateはweek_dateのリスト、week_dateは日付のリスト
        month_date  = []
        week_date   = []

        #最終的に作られるmonth_dateのイメージ。このように複数のweek_dateを含む。月の最初が日曜日ではない場合、必要な数だけ空欄をアペンドしておく
        """
        [ ['  ', '  ', '1 ', '2 ', '3 ', '4 ', '5 '],
          ['6 ', '7 ', '8 ', '9 ', '10', '11', '12'],
          ['13', '14', '15', '16', '17', '18', '19'],
          ['20', '21', '22', '23', '24', '25', '26'],
          ['27', '28', '29', '30']
          ]
        """

        #一日ずつずらしてweek_dateにアペンドする。
        #datetimeのオブジェクトは .weekday() で数値化した曜日が出力される(月曜日が0、日曜日が6)

        #日曜日以外の場合、空欄を追加する。
        if dt.weekday() != 6:
            for i in range(dt.weekday()+1):
                week_date.append("")

        #1日ずつ追加して月が変わったらループ終了
        while month == dt.month:
            week_date.append(dt.day)

            #1日追加する
            dt  = dt + datetime.timedelta(days=1)

            #週末になるたびに追加する。
            if dt.weekday() == 6:
                month_date.append(week_date)
                week_date   = []

        #一ヶ月の最終週を追加する。
        if dt.weekday() != 6:
            month_date.append(week_date)

        #print(month_date)
        context["month_date"]   = month_date

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        posted  = Topic( comment = request.POST["comment"] )
        posted.save()

        return redirect("bbs:index")

index   = BbsView.as_view()

