**quick start:**
```
cd CK4TI/code
python main.py --mode online --pattern pipeline --sum
```

for server: ../../Python-3.11.0/python main.py --mode online --pattern pipeline --sum

## note: 
java version: openjdk 17.0.2
server java version openjdk 11.0.19

java -cp LuceneIndexer/LuceneIndexer.jar LuceneCodeIndexer -online ../data/Dataset_without_wrapperclasses/StatType-SO/hibernate/hibernate_class_1.java 10 ../Evaluation/Lucene_top10/

./python -m pip install re_gpt

gpu info: nvidia-smi

screen: https://zhuanlan.zhihu.com/p/622993407

## 错误日志：
### 2-24
StatType-SO jdk Class_16 Lucene index searching fault:
```
org.apache.lucene.queryparser.classic.ParseException: Cannot parse code: too many boolean clauses
        at org.apache.lucene.queryparser.classic.QueryParserBase.parse(QueryParserBase.java:145)
        at LuceneCodeIndexer.search(LuceneCodeIndexer.java:139)
        at LuceneCodeIndexer.main(LuceneCodeIndexer.java:269)
Caused by: org.apache.lucene.search.IndexSearcher$TooManyClauses: maxClauseCount is set to 1024
        at org.apache.lucene.search.BooleanQuery$Builder.add(BooleanQuery.java:115)
        at org.apache.lucene.search.BooleanQuery$Builder.add(BooleanQuery.java:129)
        at org.apache.lucene.util.QueryBuilder.add(QueryBuilder.java:409)
        at org.apache.lucene.util.QueryBuilder.analyzeMultiBoolean(QueryBuilder.java:428)
        at org.apache.lucene.util.QueryBuilder.createFieldQuery(QueryBuilder.java:365)
        at org.apache.lucene.util.QueryBuilder.createFieldQuery(QueryBuilder.java:258)
        at org.apache.lucene.queryparser.classic.QueryParserBase.newFieldQuery(QueryParserBase.java:
        at org.apache.lucene.queryparser.classic.QueryParserBase.getFieldQuery(QueryParserBase.java:
        at org.apache.lucene.queryparser.classic.QueryParser.MultiTerm(QueryParser.java:680)
        at org.apache.lucene.queryparser.classic.QueryParser.Query(QueryParser.java:233)
        at org.apache.lucene.queryparser.classic.QueryParser.TopLevelQuery(QueryParser.java:223)
        at org.apache.lucene.queryparser.classic.QueryParserBase.parse(QueryParserBase.java:137)
```