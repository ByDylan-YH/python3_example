# coding=utf-8
# 导入requests库
import requests;
from bs4 import BeautifulSoup;
import re;
import mysql.connector;
import time;
import jieba;

mydb = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="By960122",  # 数据库密码
    database="bingo"
);

# 给请求指定一个请求头来模拟chrome浏览器,地址栏中输入  about:version
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'};
# 网址
addr = 'https://www.12306.cn/mormhweb/kyyyz';


# 计时器
def timer(func):
    def wrapper(*args, **kwds):
        t0 = time.time();
        func(*args, **kwds);
        t1 = time.time();
        print('耗时 %0.3f s' % (t1 - t0,));

    return wrapper;


# 获取12306网站所有集团下html
def get_html(addr):
    res = requests.get(addr, headers=headers);
    html = res.content;
    html_doc = str(html, 'utf8');
    # 使用自带的html.parser解析,获取首页
    homepage = BeautifulSoup(html_doc, 'html.parser');
    html_detail = homepage.find('table', id='mainTable').find_all('tbody');
    html_list = [];
    for htmls in html_detail:
        # print(html.get_text());
        # print(html);
        # print(html.get('title'));
        try:
            aa = htmls.find('td', class_='submenu_bg').find_all('a');
            # print(aa);
            for a in aa:
                html_list.append(a.get('href').replace("./", "/"));
        except Exception as e:
            pass;

    return html_list;


# 获取每个html下的车站信息
def get_station(station_addr):
    req = requests.get(url=station_addr);
    html = req.content;
    html_doc = str(html, 'utf8');
    bf = BeautifulSoup(html_doc, 'html.parser');
    station_list = [];
    try:
        texts = bf.find('tbody').find_all('tr');
        # print(texts);
        for text in texts:
            # 不要 √ 符号的内容,正则匹配之后为list,转成str存好.
            station_list.append(("".join(re.compile(r'[^√]').findall(text.get_text()))));
    except Exception as e:
        pass
    return station_list;


def parse_addr(station_result):
    station_list = [];
    for station in station_result:
        station_dict = {};
        result = jieba.cut(station['addr'], cut_all=False);
        station_dict['province'], station_dict['city'] = ",".join(result).split(",")[0:2];
        station_dict['station'] = station['station'];
        station_dict['addr'] = station['addr'];
        station_list.append(station_dict);

    # print(station_list);
    return station_list;


# 写入数据库
def write_mysql(station_list):
    sql = 'insert into trationstation values (%s,%s,%s,%s);';
    insert_list = [];
    for station_detail in station_list:
        detail_list = [];
        detail_list.append(station_detail['province']);
        detail_list.append(station_detail['city']);
        detail_list.append(station_detail['station']);
        detail_list.append(station_detail['addr']);
        insert_list.append(detail_list);
    # print(insert_list);
    mycursor = mydb.cursor();
    mycursor.executemany(sql, insert_list);
    mydb.commit();
    # print(mycursor.rowcount, ",Success");
    print('成功写入数据库: %s 行' % mycursor.rowcount);


# 主方法
@timer
def main():
    mycursor = mydb.cursor();
    mycursor.execute("truncate table trationstation;");
    html_list = get_html(addr);
    for html in html_list:
        station_result = [];
        station_addr = addr + html;
        station_list = get_station(station_addr);
        # print(station_list);
        for station in station_list[2:len(station_list)]:
            station_dict = {};
            aa = station.split("\n")[1:3];
            station_dict['station'], station_dict['addr'] = station.split("\n")[1:3];
            station_result.append(station_dict);
        station_result = parse_addr(station_result);
        print(station_result);
        write_mysql(station_result);


if __name__ == '__main__':
    # station_result = [{'station': '阿城', 'addr': '黑龙江省哈尔滨市阿城区会宁路61号'},
    #                   {'station': '阿尔山北', 'addr': '内蒙古自治区兴安盟阿尔山市伊尔施街道办事处新区社区'},
    #                   {'station': '阿里河', 'addr': '内蒙古自治区呼伦贝尔盟鄂伦春自治旗阿里河镇'},
    #                   {'station': '阿龙山', 'addr': '内蒙古自治区呼伦贝尔根河市阿龙山镇'}, {'station': '阿木尔', 'addr': '黑龙江省大兴安岭地区漠河县劲涛镇'},
    #                   {'station': '安达', 'addr': '黑龙江省安达市铁路街'}, {'station': '安家', 'addr': '黑龙江省五常市安家镇'},
    #                   {'station': '昂昂溪', 'addr': '黑龙江省齐齐哈尔市昂昂溪区陵园路23号'}, {'station': '八面通', 'addr': '黑龙江省穆棱市八面通镇'},
    #                   {'station': '巴林', 'addr': '内蒙古自治区牙克石市巴林镇巴林车站'}, {'station': '白奎堡', 'addr': '黑龙江省哈尔滨市呼兰区白奎镇'},
    #                   {'station': '宝林', 'addr': '黑龙江省林口县龙爪乡宝林村'}, {'station': '宝泉岭', 'addr': '黑龙江省鹤岗市萝北县宝泉岭镇哈萝公路西侧'},
    #                   {'station': '北安', 'addr': '黑龙江省北安市'}, {'station': '背荫河', 'addr': '黑龙江省五常市背荫河镇'},
    #                   {'station': '笔架山', 'addr': '黑龙江省双鸭山市集贤兴安乡'}, {'station': '滨江', 'addr': '黑龙江省哈尔滨市道外区滨江街28号'},
    #                   {'station': '勃利', 'addr': '黑龙江省勃利县城西街站前路84号'},
    #                   {'station': '博克图', 'addr': '内蒙古自治区牙克石市博克图镇大直街博克图站'}, {'station': '柴河', 'addr': '黑龙江省海林市柴河镇'},
    #                   {'station': '长汀镇', 'addr': '黑龙江省海林市'}, {'station': '辰清', 'addr': '黑龙江省黑河市孙吴县辰清镇\xa0\xa0'},
    #                   {'station': '晨明', 'addr': '黑龙江省伊春市南岔区晨明镇'}, {'station': '成高子', 'addr': '黑龙江省哈市香坊区哈成路158号'},
    #                   {'station': '成吉思汗', 'addr': '内蒙古自治区扎兰屯市成吉思汗镇大汗路成吉思汗车站'},
    #                   {'station': '楚山', 'addr': '黑龙江省林口县龙爪乡楚山村'},
    #                   {'station': '嵯岗', 'addr': '内蒙古自治区\xa0呼伦贝尔市新巴尔虎左旗嵯岗镇嵯岗火车站'},
    #                   {'station': '大庆', 'addr': '黑龙江省大庆市萨尔图区中桥路51号'}, {'station': '大庆东', 'addr': '大庆市龙凤区民安路88号'},
    #                   {'station': '大庆西', 'addr': '黑龙江省大庆市让湖路区西虹路40号'}, {'station': '大兴', 'addr': '黑龙江省泰来县大兴镇大兴车站'},
    #                   {'station': '大雁', 'addr': '内蒙古自治区鄂温克旗巴彦镇前卫街大雁站'},
    #                   {'station': '大杨树', 'addr': '内蒙古自治区呼伦贝尔盟鄂伦春自治旗大杨树镇'}, {'station': '带岭', 'addr': '黑龙江省伊春市带岭区'},
    #                   {'station': '得耳布尔', 'addr': '内蒙古呼伦贝尔根河市得耳布尔镇'}, {'station': '滴道', 'addr': '黑龙江省鸡西市滴道区白云委'},
    #                   {'station': '东边井', 'addr': '黑龙江省绥化市海伦市东风镇'}, {'station': '东二道河', 'addr': '黑龙江省抚远市'},
    #                   {'station': '东方红', 'addr': '黑龙江省东方红镇铁路委'}, {'station': '东海', 'addr': '黑龙江省鸡东县东海镇乡直委'},
    #                   {'station': '东津', 'addr': '黑龙江省绥化市北林区东津镇'}, {'station': '东京城', 'addr': '黑龙江省宁安市东京城镇'},
    #                   {'station': '东门', 'addr': '黑龙江省哈尔滨市香坊区铁东街8号（非客运营业站）'},
    #                   {'station': '对青山', 'addr': '黑龙江省哈尔滨市松北区对青山镇铁路街'}, {'station': '二道湾', 'addr': '黑龙江省富裕县友谊乡二道湾车站'},
    #                   {'station': '二龙山屯', 'addr': '黑龙江省黑河市五大连池市'}, {'station': '丰乐镇', 'addr': '黑龙江省双鸭山市集贤县丰乐镇南侧'},
    #                   {'station': '冯屯', 'addr': '黑龙江省富裕县塔哈乡冯屯车站'}, {'station': '福利屯', 'addr': '黑龙江省双鸭山市集贤县福双路立交桥头南侧'},
    #                   {'station': '抚远', 'addr': '黑龙江省抚远市'}, {'station': '富海', 'addr': '黑龙江省富裕县富海镇富海车站'},
    #                   {'station': '富锦', 'addr': '黑龙江省富锦市锦绣大街站前路'}, {'station': '富拉尔基', 'addr': '黑龙江省齐齐哈尔市富拉尔基区安全路84号'},
    #                   {'station': '富裕', 'addr': '黑龙江省富裕县站前街富裕车站'}, {'station': '甘河', 'addr': '内蒙古自治区呼伦贝尔盟鄂伦春自治旗甘河镇'},
    #                   {'station': '根河', 'addr': '内蒙古自治区呼伦贝尔盟根河市'}, {'station': '沟口', 'addr': '非客运营业站'},
    #                   {'station': '古城镇', 'addr': '黑龙江省牡丹江市林口县古城镇'}, {'station': '古莲', 'addr': '黑龙江省大兴安岭地区漠河县古莲镇'},
    #                   {'station': '哈尔滨', 'addr': '黑龙江省哈尔滨市南岗区铁路街1号'},
    #                   {'station': '哈尔滨北', 'addr': '哈尔滨市江北利民大道，外国语学院斜对面'}, {'station': '哈尔滨东', 'addr': '哈尔滨市道外区桦树街1号'},
    #                   {'station': '哈尔滨西', 'addr': '黑龙江省哈尔滨市南岗区哈尔滨大街501号'}, {'station': '哈克', 'addr': '非客运营业站'},
    #                   {'station': '哈拉苏', 'addr': '内蒙古自治区扎兰屯市哈拉苏镇哈拉苏车站'}, {'station': '海北', 'addr': '黑龙江省绥化市海伦市海北镇'},
    #                   {'station': '海拉尔', 'addr': '内蒙古自治区呼伦贝尔市海拉尔区靠山街60号'}, {'station': '海林', 'addr': '黑龙江省海林市海林镇'},
    #                   {'station': '海伦', 'addr': '黑龙江省绥化市海伦市\xa0海伦镇'}, {'station': '寒葱沟', 'addr': '黑龙江省抚远市'},
    #                   {'station': '浩良河', 'addr': '黑龙江省伊春市南岔区浩良河镇'}, {'station': '鹤北', 'addr': '黑龙江省鹤岗市萝北县鹤北镇'},
    #                   {'station': '鹤岗', 'addr': '黑龙江省鹤岗市向阳区老站路'}, {'station': '鹤立', 'addr': '黑龙江省佳木斯市汤原县鹤立镇忠诚街'},
    #                   {'station': '黑河', 'addr': '黑龙江省黑河市'}, {'station': '黑台', 'addr': '黑龙江省密山市黑台镇'},
    #                   {'station': '横道河子', 'addr': '黑龙江省海林市横道河子镇'}, {'station': '红山', 'addr': '黑龙江省伊春市'},
    #                   {'station': '红兴隆', 'addr': '黑龙江省双鸭山市友谊县兴隆镇'}, {'station': '红星', 'addr': '红星林业局锦绣小区环形道南侧'},
    #                   {'station': '红彦', 'addr': '内蒙古自治区呼伦贝尔盟莫力达瓦达乌尔族自治旗红彦镇'}, {'station': '洪河', 'addr': '黑龙江省抚远市'},
    #                   {'station': '呼兰', 'addr': '黑龙江省哈尔滨市呼兰区'},
    #                   {'station': '呼源', 'addr': '黑龙江省大兴安岭地区呼中区呼源镇（线路不达标临时停运）'},
    #                   {'station': '呼中', 'addr': '黑龙江省大兴安岭地区呼中区呼中镇（线路不达标临时停运）'},
    #                   {'station': '虎林', 'addr': '黑龙江省虎林市虎林镇站前街1号'}, {'station': '桦林', 'addr': '黑龙江省牡丹江市阳明区桦林镇'},
    #                   {'station': '桦南', 'addr': '黑龙江省佳木斯市桦南县铁西街北段'}, {'station': '换新天', 'addr': '黑龙江农垦总局建三江分局创业农场'},
    #                   {'station': '鸡东', 'addr': '黑龙江省鸡东县鸡东镇振兴大街100号'}, {'station': '鸡西', 'addr': '黑龙江省鸡西市鸡冠区兴国中路138号'},
    #                   {'station': '吉文', 'addr': '内蒙古自治区呼伦贝尔盟鄂伦春自治旗吉文镇'}, {'station': '加格达奇', 'addr': '黑龙江省大兴安岭地区加格达奇区'},
    #                   {'station': '佳木斯', 'addr': '黑龙江省佳木斯市站前路179号'}, {'station': '建三江', 'addr': '黑龙江农垦总局建三江分局站前路'},
    #                   {'station': '江桥', 'addr': '黑龙江省泰来县江桥镇江桥车站'}, {'station': '姜家', 'addr': '乘降点'},
    #                   {'station': '金河', 'addr': '内蒙古呼伦贝尔根河市金河镇'}, {'station': '金山屯', 'addr': '黑龙江省伊春市金山屯区铁路街'},
    #                   {'station': '锦河', 'addr': '黑龙江省黑河市锦河农场'}, {'station': '九三', 'addr': '黑龙江省嫩江县双山镇九三车站'},
    #                   {'station': '峻德', 'addr': '黑龙江省鹤岗市兴安区'}, {'station': '康金井', 'addr': '黑龙江省哈尔滨市呼兰区康金镇'},
    #                   {'station': '克东', 'addr': '黑龙江省齐齐哈尔市克东县宝泉镇'}, {'station': '克山', 'addr': '黑龙江省齐齐哈尔市克山县克山镇'},
    #                   {'station': '克一河', 'addr': '内蒙古自治区呼伦贝尔盟鄂伦春自治旗克一河镇'},
    #                   {'station': '库都尔', 'addr': '内蒙古呼伦贝尔牙克石市库都尔镇'}, {'station': '奎山', 'addr': '黑龙江省林口县奎山乡奎山村'},
    #                   {'station': '拉古', 'addr': '黑龙江省海林市横道河子镇'}, {'station': '拉哈', 'addr': '黑龙江省讷河市拉哈镇东岗街拉哈车站'},
    #                   {'station': '拉林', 'addr': '黑龙江省五常市拉林镇铁路街'}, {'station': '喇嘛甸', 'addr': '黑龙江省大庆市让湖路区喇嘛甸镇'},
    #                   {'station': '兰岗', 'addr': '黑龙江省宁安市兰岗乡'}, {'station': '兰棱', 'addr': '黑龙江省双城市兰棱镇'},
    #                   {'station': '朗乡', 'addr': '黑龙江省伊春市铁力市朗乡镇'}, {'station': '老莱', 'addr': '黑龙江省讷河市老莱镇老莱车站'},
    #                   {'station': '梨树镇', 'addr': '黑龙江省鸡西市梨树区'}, {'station': '李家', 'addr': '黑龙江省黑河市北安市李家村'},
    #                   {'station': '里木店', 'addr': '黑龙江省肇东市里木店镇'}, {'station': '莲江口', 'addr': '黑龙江省佳木斯市郊区莲江口镇镇北社区87委'},
    #                   {'station': '林海', 'addr': '黑龙江省大兴安岭地区新林区新林镇'}, {'station': '林口', 'addr': '黑龙江省林口县林口镇站前大街329号'},
    #                   {'station': '林源', 'addr': '黑龙江省大庆市大同区林源镇北街1号'}, {'station': '六合镇', 'addr': '黑龙江省讷河市六合镇六合镇车站'},
    #                   {'station': '龙江', 'addr': '黑龙江省龙江县正阳街8号'}, {'station': '龙镇', 'addr': '黑龙江省黑河市五大连池市龙镇镇'},
    #                   {'station': '麻山', 'addr': '黑龙江省鸡西市麻山区东麻山村'}, {'station': '马莲河', 'addr': '黑龙江省宁安市马河乡'},
    #                   {'station': '马桥河', 'addr': '已关闭'}, {'station': '满归', 'addr': '内蒙古自治区呼伦贝尔盟根河市满归镇'},
    #                   {'station': '满洲里', 'addr': '内蒙古自治区满洲里市南区一道街铁路车站'}, {'station': '帽儿山', 'addr': '黑龙江省尚志市帽儿山镇市场街'},
    #                   {'station': '美溪', 'addr': '黑龙江省伊春市美溪区曙光街426号'}, {'station': '孟家岗', 'addr': '黑龙江省佳木斯市桦南县孟家岗镇'},
    #                   {'station': '密山', 'addr': '黑龙江省密山市密山镇光复街'}, {'station': '免渡河', 'addr': '内蒙古自治区牙克石市免渡河镇站前路免渡河站'},
    #                   {'station': '庙台子', 'addr': '黑龙江省哈尔滨市松北区松浦镇（非客运营业站）'}, {'station': '磨刀石', 'addr': '黑龙江省穆棱市磨刀石镇'},
    #                   {'station': '莫尔道嘎', 'addr': '内蒙古自治区额尔古纳市莫尔道嘎镇'}, {'station': '漠河', 'addr': '黑龙江省大兴安岭地区漠河县'},
    #                   {'station': '牡丹江', 'addr': '黑龙江省牡丹江市光华街643号'}, {'station': '穆棱', 'addr': '黑龙江省穆棱市穆棱镇'},
    #                   {'station': '南岔', 'addr': '黑龙江省伊春市南岔区站前街'}, {'station': '南木', 'addr': '内蒙古自治区扎兰屯市南木乡南木车站'},
    #                   {'station': '讷河', 'addr': '黑龙江省讷河市铁路街讷河车站'}, {'station': '嫩江', 'addr': '黑龙江省嫩江县站前大街嫩江车站'},
    #                   {'station': '碾子山', 'addr': '黑龙江省齐齐哈尔市碾子山区沿河路53号'}, {'station': '宁安', 'addr': '黑龙江省宁安市宁安镇'},
    #                   {'station': '牛家', 'addr': '黑龙江省五常市牛家镇'}, {'station': '裴德', 'addr': '黑龙江省密山市裴德镇'},
    #                   {'station': '平房', 'addr': '黑龙江省哈尔滨市平房区联盟大街49号'}, {'station': '平山', 'addr': '黑龙江省哈尔滨市阿城区平山镇'},
    #                   {'station': '平洋', 'addr': '黑龙江省泰来县平洋镇平洋车站'}, {'station': '七台河', 'addr': '黑龙江省七台河市新兴区兴华街４９号'},
    #                   {'station': '齐齐哈尔', 'addr': '黑龙江省齐齐哈尔市站前大街130号'}, {'station': '齐齐哈尔南', 'addr': '齐齐哈尔市龙沙区嫩江环路1号'},
    #                   {'station': '前锋', 'addr': '黑龙江省抚远市'}, {'station': '前进镇', 'addr': '黑龙江省同江市前进农场'},
    #                   {'station': '秦家', 'addr': '黑龙江省绥化市北林区秦家镇'}, {'station': '青山', 'addr': '黑龙江省林口县青山乡青山村'},
    #                   {'station': '庆安', 'addr': '黑龙江省绥化市庆安县庆安镇'},
    #                   {'station': '三间房', 'addr': '黑龙江省齐齐哈尔市昂昂溪区榆树屯镇友谊社区三站街'}, {'station': '山市', 'addr': '黑龙江省海林市山市镇'},
    #                   {'station': '尚家', 'addr': '乘降点'}, {'station': '尚志', 'addr': '黑龙江省尚志市站前路'},
    #                   {'station': '神树', 'addr': '黑龙江省伊春市铁力市桃山镇神树村'}, {'station': '沈家', 'addr': '黑龙江省哈尔滨市呼兰区沈家镇'},
    #                   {'station': '石磷', 'addr': '鸡西市梨树区石场村'}, {'station': '石人城', 'addr': '黑龙江省哈尔滨市呼兰区石人镇'},
    #                   {'station': '石头', 'addr': '黑龙江省宁安市石岩镇'}, {'station': '双城堡', 'addr': '黑龙江省双城市车站街'},
    #                   {'station': '双城北站', 'addr': '黑龙江省哈尔滨市双城区双城镇光明村温家屯双城北站'},
    #                   {'station': '双丰', 'addr': '黑龙江省伊春市铁力市双丰镇'}, {'station': '双鸭山', 'addr': '黑龙江省双鸭山市尖山区站前路'},
    #                   {'station': '四方台', 'addr': '黑龙江省绥化市北林区四方台镇'}, {'station': '宋', 'addr': '黑龙江省肇东市宋站镇'},
    #                   {'station': '绥芬河', 'addr': '黑龙江省绥芬河市站前路36号'}, {'station': '绥化', 'addr': '黑龙江省绥化市北林区'},
    #                   {'station': '绥棱', 'addr': '黑龙江省绥化市绥棱县绥棱镇'}, {'station': '绥阳', 'addr': '黑龙江省东宁县绥阳镇'},
    #                   {'station': '孙家', 'addr': '黑龙江省哈尔滨市通乡街65号'}, {'station': '孙吴', 'addr': '黑龙江省黑河市孙吴县孙吴镇'},
    #                   {'station': '塔尔气', 'addr': '内蒙古自治区牙克石市塔尔气镇'}, {'station': '塔哈', 'addr': '黑龙江省富裕县塔哈乡塔哈车站'},
    #                   {'station': '塔河', 'addr': '黑龙江省大兴安岭地区塔河县'}, {'station': '苔青', 'addr': '乘降点'},
    #                   {'station': '太平镇', 'addr': '黑龙江省双鸭山市集贤县大平镇'}, {'station': '泰康', 'addr': '黑龙江省大庆市杜尔伯特蒙古族自治县向阳街'},
    #                   {'station': '泰来', 'addr': '黑龙江省泰来县铁东街泰来车站'}, {'station': '汤池', 'addr': '黑龙江省泰来县汤池镇汤池车站'},
    #                   {'station': '汤旺河', 'addr': '黑龙江省伊春市汤旺河区向阳街125号'}, {'station': '汤原', 'addr': '黑龙江省佳木斯市汤原县铁路街'},
    #                   {'station': '桃山', 'addr': '黑龙江省伊春市铁力市桃山镇'}, {'station': '铁力', 'addr': '黑龙江省伊春市铁力市铁力镇'},
    #                   {'station': '通北', 'addr': '黑龙江省黑河市、北安市通北镇'}, {'station': '同江', 'addr': '同江市同三路南路同江火车站同江地铁有限公司'},
    #                   {'station': '图里河', 'addr': '内蒙古自治区呼伦贝尔牙克石市图里镇'}, {'station': '图强', 'addr': '黑龙江省大兴安岭地区漠河县图强镇'},
    #                   {'station': '团结', 'addr': '黑龙江省讷河市兴旺乡团结车站'}, {'station': '完工', 'addr': '非客运营业站'},
    #                   {'station': '万发屯', 'addr': '黑龙江省绥化市北林区万发镇'}, {'station': '万乐', 'addr': '黑龙江省哈尔滨市松北区乐业乡（乘降所）'},
    #                   {'station': '王岗', 'addr': '黑龙江省哈尔滨市王岗镇'}, {'station': '王兆屯', 'addr': '黑龙江省哈尔滨市香坊区文政街99号'},
    #                   {'station': '苇河', 'addr': '黑龙江省尚志市苇河镇'}, {'station': '卫星', 'addr': '黑龙江省虎林市虎林镇850农场'},
    #                   {'station': '温春', 'addr': '黑龙江省牡丹江市西安区温春镇'}, {'station': '倭肯', 'addr': '黑龙江省七台河市勃利县倭肯镇'},
    #                   {'station': '卧里屯', 'addr': '黑龙江省大庆市龙凤区卧里屯大街1号'},
    #                   {'station': '乌尔旗汗', 'addr': '内蒙古自治区呼伦贝尔牙克石市乌尔旗汗镇'},
    #                   {'station': '乌奴耳', 'addr': '内蒙古自治区牙克石市乌奴耳镇道北乌奴耳站'},
    #                   {'station': '乌伊岭', 'addr': '黑龙江省伊春市乌伊岭林业局林铁街'}, {'station': '五常', 'addr': '黑龙江省五常市通达大街101号'},
    #                   {'station': '五大连池', 'addr': '黑龙江省黑河市五大连池市'}, {'station': '五家', 'addr': '黑龙江省双城市五家镇'},
    #                   {'station': '五营', 'addr': '黑龙江省伊春市五营区壮林街'}, {'station': '西岗子', 'addr': '黑龙江省黑河市爱辉区西岗镇'},
    #                   {'station': '西林', 'addr': '黑龙江省伊春市西林区繁荣街'}, {'station': '西麻山', 'addr': '黑龙江省鸡西市麻山区车站委'},
    #                   {'station': '下城子', 'addr': '黑龙江省穆棱市下城子镇'}, {'station': '香坊', 'addr': '黑龙江省哈尔滨市香坊区通站街118号'},
    #                   {'station': '香兰', 'addr': '黑龙江省佳木斯市汤原县香兰镇'}, {'station': '襄河', 'addr': '黑龙江省黑河市襄河农场'},
    #                   {'station': '向阳', 'addr': '黑龙江省林口县龙爪乡向阳村'}, {'station': '小岭', 'addr': '黑龙江省哈尔滨市阿城区小岭镇小岭街'},
    #                   {'station': '小扬气', 'addr': '黑龙江省大兴安岭地区松岭区小扬气镇'}, {'station': '新绰源', 'addr': '内蒙古自治区牙克石市绰尔镇'},
    #                   {'station': '新华', 'addr': '黑龙江省鹤岗市兴安区新华镇'}, {'station': '新华屯', 'addr': '乘降点'},
    #                   {'station': '新林', 'addr': '黑龙江省大兴安岭地区新林区新林镇'}, {'station': '新青', 'addr': '黑龙江省伊春市新青区新青大街'},
    #                   {'station': '新松浦', 'addr': '黑龙江省哈尔滨市松北区松浦镇'}, {'station': '新友谊', 'addr': '黑龙江省双鸭山市友谊县'},
    #                   {'station': '兴凯', 'addr': '黑龙江省密山市兴凯镇'}, {'station': '兴隆镇', 'addr': '黑龙江省绥化市巴彦县兴隆镇'},
    #                   {'station': '杏树', 'addr': '黑龙江省七台河市勃利县杏树乡'}, {'station': '徐家', 'addr': '黑龙江省哈尔滨市呼兰区利民镇松源村'},
    #                   {'station': '牙克石', 'addr': '内蒙古自治区牙克石市迎宾街1号牙克石站'}, {'station': '亚布力', 'addr': '黑龙江省尚志市亚布力镇'},
    #                   {'station': '亚布力南', 'addr': '黑龙江省尚志市亚布力镇'}, {'station': '烟筒屯', 'addr': '乘降点'},
    #                   {'station': '羊草', 'addr': '乘降点'}, {'station': '杨岗', 'addr': '黑龙江省虎林市杨岗镇杨岗村'},
    #                   {'station': '一面坡', 'addr': '黑龙江省尚志市一面坡镇'}, {'station': '伊春', 'addr': '黑龙江省伊春市伊春区新兴东大街4号'},
    #                   {'station': '伊拉哈', 'addr': '黑龙江省嫩江县伊拉哈镇伊拉哈车站'},
    #                   {'station': '伊林', 'addr': '非客运营业站，只有一个一节轨道车拉的摆渡车厢乘降旅客'},
    #                   {'station': '伊敏', 'addr': '内蒙古自治区呼伦贝尔市鄂温克族自治旗伊敏河镇五牧场'},
    #                   {'station': '伊图里河', 'addr': '内蒙古自治区呼伦贝尔牙克石市图里镇'}, {'station': '依安', 'addr': '黑龙江省依安县西南街依安车站'},
    #                   {'station': '银浪', 'addr': '黑龙江省大庆市红岗区乘南12街'}, {'station': '迎春', 'addr': '黑龙江省虎林市迎春镇'},
    #                   {'station': '永安乡', 'addr': '黑龙江省鸡东县永安镇农安委'}, {'station': '友好', 'addr': '黑龙江省伊春市友好区东升街'},
    #                   {'station': '榆树屯', 'addr': '黑龙江省齐齐哈尔市昂昂溪区榆树屯镇榆树屯车站'},
    #                   {'station': '玉泉', 'addr': '黑龙江省哈尔滨市阿城区玉泉街道办事处酒厂大街1号'}, {'station': '原林', 'addr': '非客运营业站'},
    #                   {'station': '扎赉诺尔', 'addr': '非客运营业站'}, {'station': '扎赉诺尔西', 'addr': '内蒙古自治区满洲里市扎赉诺尔矿区站前街'},
    #                   {'station': '扎兰屯', 'addr': '内蒙古自治区扎兰屯市铁西路22号'}, {'station': '扎罗木得', 'addr': '非客运营业站'},
    #                   {'station': '张维屯', 'addr': '黑龙江省绥化市北林区张维镇'}, {'station': '赵光', 'addr': '黑龙江省黑河市、北安市赵光镇'},
    #                   {'station': '肇东', 'addr': '黑龙江省肇东市铁东一道街'}, {'station': '周家', 'addr': '黑龙江省双城市周家镇'},
    #                   {'station': '朱家沟', 'addr': '黑龙江省牡丹江市林口县朱家镇'}];
    # parse_addr(station_result);
    main();
