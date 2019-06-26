# classfy-photo-by-location
classfy photos from mobile phone by location in China which generated with GPS data from the EXIF information.  Put it into different directory.

按照手机照片里的EXIF中的GPS数据对照片，按日期（一般是月）和地点进行分类。

采用中国国家地理中心的数据对行政区进行分类。精确到县，并针对长名称进行一定简化。

map_data_new.json是数据文件
findlocation.py是个测试，根据输入的GPS数据反查地名。

对不同地区的招牌采取不同的分类方式。

类型一：非本省区域，连续日期在同一城市，以月+市（含直辖市、港澳）为分类名称，比如“201812上海”，“201808辽宁大连”等。

类型二：非本省区域，连续日期在不同城市，以月+市+市...+市分类，比如“201709昆明大理丽江”，简称可以手工微调。

类型三：本省区域，非本市区域，连续时间内相同或不同城市，以月+地级市+县+县...+县分类。如县级名称为区，则只保留地级市名。如“201902自贡泸州”

类型四：本市区域，按每日进行分类，以月+行政区分类。

暂不处理类型：
连续日期内的本省和邻省的跨省分类，用手工合并
无GPS数据的照片，如微信传入图，手工分类

