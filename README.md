# twitch-stream-analysis

> This is a web-site that analysis the stream in twitch
>
> - Draw the dashboard for viewship using Highchart 
> - Recommend the similar streamer using word2vec.

**Web-site address** [link](http://twitch-stream-analysis.ml) 



**(1) Main Streamer info**

![webpage text](https://github.com/wjy5446/board-twitch-analysis/blob/master/img/main.PNG)



**(2) viewship**

![webpage text](https://github.com/wjy5446/board-twitch-analysis/blob/master/img/viewship.PNG)



**(3) Recommand streamer**

![webpage text](https://github.com/wjy5446/board-twitch-analysis/blob/master/img/recommand_streamer.PNG)



## 1. Code

##### skill

> - numpy, pandas, gensim
> - web : flask, bootstrap, MySQLdb, hghchart

##### Code

>flask : flask
>
>data : csv
>
>model : model(word2vec) 
>
>flask/util : function
>
>- db.py : Load the stream-info data from MysqlDB 
>- viewship.py : Crawling the data form twitch-metrics
>
