
性能测试结果：


队列个数, 优先级调整刷新时间间隔, 是否序列化, 消息个数

10, 0.1, True/False, 1000
test_performance usedtime: 0.0934798717499s
test_performance usedtime: 0.0452258586884s

10, 0.1, True/False, 10000
test_performance usedtime: 1.29951786995s
test_performance usedtime: 0.641245126724s

10, 0.1, True/False, 100000
test_performance usedtime: 13.4946079254s
test_performance usedtime: 6.77674794197s

10, 0.1, True/False, 1000000
test_performance usedtime: 139.334857941s
test_performance usedtime: 69.0894129276s


--------------------------------------------

10, 1, True/False, 1000
test_performance usedtime: 0.0986461639404s
test_performance usedtime: 0.0494980812073s
10, 1, True/False, 10000
test_performance usedtime: 0.978669881821s
test_performance usedtime: 0.459939002991s
10, 1, True/False, 100000
test_performance usedtime: 13.9127328396s
test_performance usedtime: 6.41927099228s
10, 1, True/False, 1000000
test_performance usedtime: 144.799054146s



上述依次测试了消息个数 10000， 100000， 1000000的耗时，单位（秒）

结果表示非序列化效率更快近一倍
