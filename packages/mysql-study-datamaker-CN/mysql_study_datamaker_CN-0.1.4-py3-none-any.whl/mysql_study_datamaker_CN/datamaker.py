import random
import random as r
from datetime import datetime


class DataMaker:
    """
    这个类的目的是为了在学习 MySQL 语言时，创建表结构后，需要很多插入的数据来进行学习测试；
    DataMaker会根据指定的数量生成指定多的随机项，且支持自定义顺序；
    当前的版本只会生成一个 txt 文本，注意最后一行的","要替换成";"才能够插入数据；
    xxx 是你的 MySQL 表名，需要替换，很傻瓜很简单的一个类
    """

    def __init__(self, N, args=("姓名", "性别", "年龄", "生日", "身份证", "部门", "手机", "城市"), left=1950,
                 right=2000,
                 department=None, gender="cn", a=0, b=150, phonehead=130, phone=0, IDCITY=('11000', '310101'),
                 work_head="员工", work_numwidth=3, work_start=1, file=None,
                 city=("北京", "上海", "天津", "重庆"), sep=","):
        """
        __information：数据字典
        | -- N：数据个数，这里需要传递一个大于0的整数，否则会报错！
        | -- args：字段列表，目前只支持："姓名,年龄,部门,生日,性别,分数,手机,身份证,工号,日期"；
                   默认值给了一个元组参数，如果传递不符合需求，则会自动报错，根据提示即可得知错误原因。
        | -- left:出生日期左边界，默认情况下不允许小于 1950 （如有需求可自行修改源代码中的判定）
        | -- right:出生日期有边界，默认情况下不允许小于当前年 （自动判定当前年份，拒绝未来人）
        | -- department：默认给了：‘销售部,技术部,售后部,企划部,咨询部,人事部,财务部’，如果需要重新定义部门，需要写字符串，用','分割；
        | -- gender：
            | -- cn：默认是中文类型，只有'男'或者'女'
            | -- int：0 和 1 代表不同性别，没有严格的去区分哪个数字代表男和女；
            | -- en：英文的 M F
            | -- english：英文的 Male  Female
        | -- a:考试分数的随机，最小值；
        | -- b:考试分数的随机，最大值；
               分数只要识别前两个字符是分数就可以，如果想创建多个分数的学生信息，可以写成：
               ("姓名", "年龄", "性别",  "分数1", "分数2", "分数3")
                考试分数默认是 ； 0~150 分，则 a 就是 0， b：就是 150，做了判定修改，支持 b < a
        | -- file：文件名，写入以 x 格式，所以创建后，再次生成会报文件已存在的错误，建议写入当前日期时间，使用'date'模式；
              模式为：None或者'date'，
              如果是None则使用 时刻 + "_mysql_date.txt" , 如果是 "date" 则以此刻时间为基准，也可以自定义名直接写；
              这样做的好处是避免覆盖掉之前生成的数据，date模式更方便，也可以自定义文件名；

        | -- phonehead(int)：前三位，默认是 '130' 这里只是模拟，不是很准确；
        | -- phone:手机号从 0 开始

        | -- IDCITY：最好元组格式，没有做限制，身份证城市ID头
        | -- work_num：工号标头
        | -- work_numwidth：工号编号，当前只支持数字牌号
        | -- work_start：工号开始的值，默认从 1 开始；
        | -- city：元组对象，里面都是字符串城市名
        | -- sep：每个元素的间隔符号
        """
        self.__informations = {}
        if not isinstance(N, int):
            raise TypeError("N must be an integer")
        elif N <= 0:
            raise ValueError("N > 0, N ∈ Z")
        self.__N = N
        self.__args = args
        self.__left = left
        self.__right = right
        self.__department = department
        self.__gender = gender
        self.__a = a
        self.__b = b
        self.__phonehead = phonehead
        self.__phone = phone
        self.__IDCITY = IDCITY

        self.__work_num = work_head
        self.__work_num_width = work_numwidth
        self.__work_start = work_start

        self.__city = city
        self.__sep = sep

        now = datetime.now()
        if file is None:
            self.file = f"{now.year}{now.month:>02}{now.day:>02} {now.hour:>02}.{now.minute:>02}.{now.second:>02}_mysql_date.txt"
        elif not isinstance(file, str):
            raise TypeError("'file' should be a str")
        elif file.lower() == "date":
            self.file = f"{now.year}{now.month:>02}{now.day:>02} {now.hour:>02}.{now.minute:>02}.{now.second:>02}.txt"
        else:
            self.file = file
        self.__get_info()

    def __get_name(self):
        """
        返回随机生成的姓名系统，总共有 300个姓氏，3579个名字；
        如果超过 1,073,700 个姓名，就一定会有重复的名字出现；
        因为没有做去重处理，所以就算生成 2 个随机姓名也有重复出现的概率！
        :param self.__N: 生成名字的个数；
        :return: 返回一个迭代器；
        """
        with open(__file__[:__file__.rfind("d")] + 'new_names.txt', encoding="utf-8") as f:
            names = f.read().splitlines()

        with open(__file__[:__file__.rfind("d")] + 'new_family.txt', encoding="utf-8") as f:
            familys = f.read().splitlines()

        return ("'" + r.choice(familys) + r.choice(names) + "'" for _ in range(self.__N))

    def __is_leapyear(self, year):
        """
        判断是不是闰年
        :param year: 传递来的年份
        :return: bool值
        """
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return True
        return False

    def __get_birthday_age_ID(self):
        """
        返回的是一个生成器, 根据types的类型来判断返回什么，默认返回的是生日类型；
        年龄具有时效性！如果是前一年生成的，那么下一年则需要变动；
        随机生成生日的函数，这里做了限定，不能低于 1950 生人；
        如果左右的限定不符合规则（如 年份超出当今年份）都会触发异常；
        因为每个人的身份证号也包含年龄，所以该方法也可以返回身份证号
        :param self.__N: 数量
        :param self.__left: 1950年起，今年；
        :param self.__right: 同 self.__left
        :param self.__types: 只能是 'birthday' 或者 'age' 或者 ‘ID’
        :return: 生成器
        """

        if not isinstance(self.__left, int) or not isinstance(self.__right, int):
            raise TypeError('left or right must be int')
        today = datetime.now()
        if self.__left < 1950 or self.__left > today.year:
            raise ValueError(f"left must be '1950 <= left <= {today.year}.'")
        if self.__right < 1950 or self.__right > today.year:
            raise ValueError(f"right must be '1950 <= right <= {today.year}.'")
        if self.__left > self.__right:
            self.__left, self.__right = self.__right, self.__left

        years = [year for year in range(self.__left, self.__right + 1)]
        months = [month for month in range(1, 13)]
        days1 = [day for day in range(1, 32)]
        days2 = [day for day in range(1, 31)]
        days3 = [day for day in range(1, 30)]
        days4 = [day for day in range(1, 29)]

        for i in range(self.__N):
            year = r.choice(years)
            month = r.choice(months)
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day = r.choice(days1)
            elif month in [4, 6, 9, 11]:
                day = r.choice(days2)
            else:
                if self.__is_leapyear(year):
                    day = r.choice(days3)
                else:
                    day = r.choice(days4)

            id_head = random.choice(self.__IDCITY)
            id_end = "".join([str(random.randint(0, 9)) for i in range(3)]) + random.choice("0123456789X")

            yield [f"\'{year:>02}-{month:>02}-{day:>02}\'",
                   str(today.year - year),
                   f"\'{id_head}{year:>02}{month:>02}{day:>02}{id_end}\'"]

    def __get_random_date(self):
        """
        返回一个随机日期，限制与生日相同，但是日期与生日无关！
        如果日期是入职日期，有入职日期大于生日日期的情况！这里并没有做逻辑判断！
        单纯生成一个随机日期！
        :return: 生成器
        """
        if not isinstance(self.__left, int) or not isinstance(self.__right, int):
            raise TypeError('left or right must be int')
        today = datetime.now()
        if self.__left < 1950 or self.__left > today.year:
            raise ValueError(f"left must be '1950 <= left <= {today.year}.'")
        if self.__right < 1950 or self.__right > today.year:
            raise ValueError(f"right must be '1950 <= right <= {today.year}.'")
        if self.__left > self.__right:
            self.__left, self.__right = self.__right, self.__left

        years = [year for year in range(self.__left, self.__right + 1)]
        months = [month for month in range(1, 13)]
        days1 = [day for day in range(1, 32)]
        days2 = [day for day in range(1, 31)]
        days3 = [day for day in range(1, 30)]
        days4 = [day for day in range(1, 29)]

        for i in range(self.__N):
            year = r.choice(years)
            month = r.choice(months)
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day = r.choice(days1)
            elif month in [4, 6, 9, 11]:
                day = r.choice(days2)
            else:
                if self.__is_leapyear(year):
                    day = r.choice(days3)
                else:
                    day = r.choice(days4)
            yield f"\'{year:>02}-{month:>02}-{day:>02}\'"

    def __get_gender(self, types="int"):
        """
        根据传递的类型不同，可以分别用，英文，中文，整数来表达性别；
        注意，英文如果是全拼的 'english' 返回 'Male' 'Female'；
        如果是 'en' 返回 'M' 'F'
        中文的'chinese' 'cn' 都是 ‘男’  ‘女’
        :param self.__N: 返回的数量
        :param self.__types: english, chinese, int, cn, en
        :return: 生成器
        """
        if types not in ["int", "english", "chinese", "en", "cn"]:
            raise ValueError('types can be "int"  "english"  "chinese" "cn" "en" .')
        if types == "int":
            return ("'" + r.choice("01") + "'" for _ in range(self.__N))
        elif types == "english":
            return ("'" + r.choice(["Male", "Female"]) + "'" for _ in range(self.__N))
        elif types == "en":
            return ("'" + r.choice("MF") + "'" for _ in range(self.__N))
        else:
            return ("'" + r.choice("男女") + "'" for _ in range(self.__N))

    def __get_department(self, department=None):
        """
        部门默认是："销售部,技术部,售后部,企划部,咨询部,人事部,财务部"
        可以自定义传递，传递必须是字符串，且用英文','分割
        :param self.__N: 生成个数
        :param self.__department:默认是None
        :return: 生成器
        """
        if department is None:
            department = "销售部,技术部,售后部,企划部,咨询部,人事部,财务部"
        department = department.split(",")
        return ("'" + r.choice(department) + "'" for _ in range(self.__N))

    def __get_phone(self):
        """
        模拟随机的手机号
        :return: 生成器
        """
        for i in range(self.__N):
            yield f'\'{self.__phonehead}{self.__phone:>08}\''
            self.__phone += 1
            if self.__phone == 99999999:
                self.__phonehead += 1
                self.__phone = 0

    def __get_score(self, a=0, b=150):
        """
        返回随机分数
        :param self.__N: 个数
        :param self.__a: 最低值
        :param self.__b: 最高值
        :return: 返回生成器
        """
        if a > b:
            a, b = b, a
        return (str(r.randint(a, b)) for _ in range(self.__N))

    def __get_worknum(self):
        return (f"\'{self.__work_num}{i:0>{self.__work_num_width}}\'" for i in
                range(self.__work_start, self.__N + self.__work_start))

    def __get_city(self):
        """
        返回随机的一个城市
        :return: 生成器
        """
        return (random.choice(self.__city) for _ in range(self.__N))

    def __get_info(self):
        infos = "姓名,年龄,部门,生日,性别,分数,手机,身份证,工号,日期,城市".split(",")
        for info in self.__args:
            if info not in infos:
                if info[:2] != "分数":
                    error_info = ','.join(infos)
                    raise ValueError(f"All must be in\n < {error_info} >, \n'{info}' not in.")

        for item in self.__args:
            if item == "姓名":
                self.__informations[item] = self.__get_name()
            elif item in ["年龄", "生日", "身份证"]:
                self.__informations["DATE"] = self.__get_birthday_age_ID()
            elif item == "部门":
                self.__informations[item] = self.__get_department(department=self.__department)
            elif item == "性别":
                self.__informations[item] = self.__get_gender(self.__gender)
            elif item[:2] == "分数":
                self.__informations[item] = self.__get_score(self.__a, self.__b)
            elif item == "手机":
                self.__informations[item] = self.__get_phone()
            elif item == "工号":
                self.__informations[item] = self.__get_worknum()
            elif item == "日期":
                self.__informations[item] = self.__get_random_date()
            elif item == "城市":
                self.__informations[item] = self.__get_city()

    def __iter__(self):
        return self

    def __next__(self):

        result = ""
        if "DATE" in self.__informations:
            temp = next(self.__informations["DATE"])

        for item in self.__args:
            if item == "生日":
                result += temp[0] + self.__sep
            elif item == "年龄":
                result += temp[1] + self.__sep
            elif item == "身份证":
                result += temp[2] + self.__sep
            else:
                result += next(self.__informations[item]) + self.__sep

        result = result[:-1]
        if not result:
            raise StopIteration
        return result

    def create_mysql(self, code="insert_into"):
        """
        需要先生成一个DataMaker对象，来创建指定数量和字段，再调用该方法，写入到一个txt文本中；
        :param code: 生成模式
        :return: None
        """
        if code == "insert_into":
            with open("insert_into_" + self.file, "x", encoding="utf-8") as f:
                f.write(f"insert into xxx values {('PRIMARYKEY_ID',) + self.__args} \n")
                id = 1
                for line in self:
                    comment = "(" + str(id) + self.__sep + line + "),\n"
                    id += 1
                    f.write(comment)
        elif code == "self":
            with open("insert_into_" + self.file, "x", encoding="utf-8") as f:
                f.write(f"self_data:\n{self.__args}\n")
                for line in self:
                    f.write(line + "\n")

    def get_data(self):
        self.create_mysql("self")


def get_help():
    content = """
    --- ver 0.1.4 ---
    更改内容：
        | -- 增加 sep 属性，默认为","，可以对生成的连续属性间隔符进行自定义
        | -- 增加“城市”属性，城市与身份证并无对应关系！不符合逻辑！工作地址和出生地址不是捆绑关系！
        | -- create() 方法 更名为 create_mysql()方法，code增加"self"模式
        | -- 增加 get_data()方法，可以生成自己想要的数据，与create_mysql(code="self")相同！
        | -- 但是数据只能是下面所列
            | -- 姓名,年龄,部门,生日,性别,分数,手机,身份证,工号,日期,城市
    bug修复：
        | -- 修复了版本描述问题
    
    --- ver 0.1.3 ---
    更改内容：
        | -- create_insertinto() 方法 更名为 create方法，需要传递 code 参数来生成指定的 Mysql语法信息，默认”insert_into“；
    bug修复：
        | -- 修复了 年龄、身份证、生日与其他字段顺序不统一的录入问题
        
        
    --- ver 0.1.2 ---
    增加内容：
        | -- 增加了 get_demo() 函数，查看详细的案例演示；
    
    bug修复：
        | -- 修复了 电话/手机 的不统一问题，只能用 手机；
        
        
    --- ver 0.1.1 ---
    增加内容：
        | -- 增加了 随机日期 的方法；
    
    bug修复：
        | -- 修复了 工号 的字符串格式；
    
    
    --- ver 0.1.0 ---
    该版本支持‘身份证’，‘手机’，‘工号’，及修复了年龄显示 不正确的 bug，
    如果要使用身份证，需要输入大写 ‘ID’，构造函数IDCITY参数要传递城市开头代码，这里默认给了北京和上海的，
    如果需要更多的城市可以自己对该参数进行修改，后四位为随机生成，不符合性别及正规规律，单纯模拟，
    如果有需要末尾是按照需求的可自行修改代码。
    """
    print(content)


def get_demo():
    content = """
    def __init__(self, N, args=("姓名", "性别", "年龄", "生日", "身份证", "部门", "手机"), left=1950, right=2000,
             department=None, gender="cn", a=0, b=150, phonehead=130, phone=0, IDCITY=('11000', '310101'),
             work_num="员工", work_numwidth=3, work_start=1, file=None): --> None
    构造函数当中的参数：
        | -- N：数据个数，这里需要传递一个大于0的整数，否则会报错！
        | -- args：字段列表，目前只支持："姓名,年龄,部门,生日,性别,分数,手机,身份证,工号,日期"；
                   默认值给了一个元组参数，如果传递不符合需求，则会自动报错，根据提示即可得知错误原因。
        | -- left:出生日期左边界，默认情况下不允许小于 1950 （如有需求可自行修改源代码中的判定）
        | -- right:出生日期有边界，默认情况下不允许小于当前年 （自动判定当前年份，拒绝未来人）
        | -- department：默认给了：‘销售部,技术部,售后部,企划部,咨询部,人事部,财务部’，如果需要重新定义部门，需要写字符串，用','分割；
        | -- gender：
            | -- cn：默认是中文类型，只有'男'或者'女' 
            | -- int：0 和 1 代表不同性别，没有严格的去区分哪个数字代表男和女；
            | -- en：英文的 M F
            | -- english：英文的 Male  Female
        | -- a:考试分数的随机，最小值；
        | -- b:考试分数的随机，最大值；
               分数只要识别前两个字符是分数就可以，如果想创建多个分数的学生信息，可以写成：
               ("姓名", "年龄", "性别",  "分数1", "分数2", "分数3")
                考试分数默认是 ； 0~150 分，则 a 就是 0， b：就是 150，做了判定修改，支持 b < a
        | -- file：文件名，写入以 x 格式，所以创建后，再次生成会报文件已存在的错误，建议写入当前日期时间，使用'date'模式；
              模式为：None或者'date'，
              如果是None则使用 时刻 + "_mysql_date.txt" , 如果是 "date" 则以此刻时间为基准，也可以自定义名直接写；
              这样做的好处是避免覆盖掉之前生成的数据，date模式更方便，也可以自定义文件名；

        | -- phonehead(int)：前三位，默认是 '130' 这里只是模拟，不是很准确；
        | -- phone:手机号从 0 开始

        | -- IDCITY：最好元组格式，没有做限制，身份证城市ID头
        | -- work_head：工号标头
        | -- work_numwidth：工号编号，当前只支持数字牌号
        | -- work_start：工号开始的值，默认从 1 开始；
        | -- city：元组对象，里面都是字符串城市名
        | -- sep：每个元素的间隔符号
        
        示例演示：
        示例1，学生信息，
        姓名，性别，学号，语文、数学、英语三科成绩，50人；
        one = DataMaker(50, ("姓名", "性别", "工号", "分数语文", "分数数学", "分数英语"), work_head="2024.三班", work_numwidth=2)
        one.create_mysql(code="insert_into")
        
        示例2，员工信息
        姓名，性别，生日，年龄，身份证，部门，手机，100人
        one = DataMaker(100, ("姓名", "性别", "生日", "年龄", "身份证", "部门", "手机"))
        one.create_mysql(code="insert_into")
        
        实例3，生成单一数据
        姓名，性别，年龄，城市
        one = DataMaker(20, ("姓名", "性别",  "年龄", "城市"))
        one.get_dataself()
    """
    print(content)


if __name__ == '__main__':
    """
    下面是案例，直接运行可以获得测试代码，生成50个随机数据；
    """
    one = DataMaker(20, ("姓名", "性别", "年龄", "城市"))
    one.get_data()
