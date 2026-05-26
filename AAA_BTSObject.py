# coding=utf-8

#Author: zhaoshiheng
#version: 1.00
#date: 2019/02/25


# 通用研发特殊字段封装，便于高层编程
try:
    MODEL = MODEL
except: pass
APPEND_MODE=APPEND_MODE
OVERWRITE_MODE=OVERWRITE_MODE
MOD=MOD
WHERE=WHERE
ExcelRow=ExcelRow
BIT=BIT
re=re
copy=copy
math=math
NETYPE=NETYPE
# json=json
# FOr JSON to CME Decoding
data_into_xml = {"SRN":[],
                 "SN": [],
                 "ANTN": [],
                 "ANTTYPE": [],
                 "TXBKPMODE": [],
                 "SECTOREQMID": [],
                 "SECTORID" : [],
                 "ANTCFGMODE": []
                 }
# load 加载数据到内存 dump 内存保存到文件
@API_RECORD
def load_Excel_Data(excel_name, sheet_name, title_row=1, filter_func=None,
                        group_title=None, title_name_mapping=None, **kwargs):
    return LOAD_EXCEL_DATA(excel_name, sheet_name, title_row, filter_func, group_title, title_name_mapping, **kwargs)

@API_RECORD
def load_Excel_File(excel_name, sheet_name, title_row, group_title, **kwargs):
    return LOAD_EXCEL_FILE(excel_name, sheet_name, title_row, group_title, **kwargs)

@API_RECORD
def load_CSV_File(csv_name, delimiter_symbols=";",encoding="utf-8"):
    return LOAD_CSV_FILE(csv_name,delimiter_symbols,encoding)

@API_RECORD
def load_TXT_File(filename, encoding="GBK"):
    return READ_TXT_FILE(filename, encoding)

@API_RECORD
def get_data_from_summary(summary_name, moc_name, *filter_list, **kwargs):
    return LOAD_SUMMARY_DATA(summary_name, moc_name, *filter_list, **kwargs)

@API_RECORD
def load_Object(filename, init_value):
    return LOAD_OBJ(filename, init_value)

@API_RECORD
def dump_Object(filename, obj):
    return DUMP_OBJ(filename, obj)

@API_RECORD
def load_WSD_File(ne_name, with_raw=False):
    return LOAD_WSD_FILE(ne_name, with_raw)

@API_RECORD
def load_Json_File(filename):
    return LOAD_JSON_FILE(filename)

@API_RECORD
def dump_TXT_File(filename, rows, encoding='GBK'):
    return WRITE_TXT_FILE(filename, rows, encoding)

@API_RECORD
def write_Excel_Sheet(excel_name, sheet_name, title_row, rows, start_row=None, with_clear=False, **kwargs):
    return WRITE_EXCEL_SHEET(excel_name, sheet_name, title_row, rows, start_row, with_clear, **kwargs)

@API_RECORD
def convert_Str2Ip(string):
    return MODEL.IPV4.fromString(string)

@API_RECORD
def convert_Ip2Str(ip):
    return MODEL.IPV4.toString(ip)

@API_RECORD
def convert_Str2Int_Ipv6(ipstr):
    '''
    cme导出DB中ipv6地址转换
    ipstr必须为字符串类型
    '''
    if ipstr == None:
        return 0

    # 双冒号只能存在一次
    if ipstr.count("::") > 1:
        return 0

    # ipv6地址共8组128位
    ipv6_group_len = 8

    # 是否内嵌ipv4
    if ipstr.find('.') != -1:
        ip_v4_str = ipstr.split(":")[-1]
        if ip_v4_str.count(".") == 3:
            try:
                v4_int = ipv4_int(ip_v4_str)
            except:
                return 0
            v4_int_pre = "%04x" % (v4_int >> 16)
            v4_int_post = "%04x" % (v4_int & 0xffff)
            ipv4_to_ipv6 = "%s%s%s" % (v4_int_pre, ":", v4_int_post)
            ipstr = ipstr.replace(ip_v4_str, ipv4_to_ipv6)
        else:
            return 0
    try:
        if ipstr.find("::") != -1:
            double_colon_lst = ipstr.split("::")
            if double_colon_lst[0] == "":
                before_colon_lst = ["0"]
            else:
                before_colon_lst = double_colon_lst[0].split(":")
            if double_colon_lst[-1] == "":
                after_colon_lst = ["0"]
            else:
                after_colon_lst = double_colon_lst[-1].split(":")
            # 补全双冒号
            double_colon_count =  ipv6_group_len - len(before_colon_lst) - len(after_colon_lst)
            if double_colon_count <= 0:
                return 0

            elements = before_colon_lst + ["0"] * double_colon_count + after_colon_lst
        else:
            elements = ipstr.split(":")
            if len(elements) != ipv6_group_len:
                return 0
    except:
        return 0

    ret_value = 0
    for element in elements:
        try:
            element = int(element, 16)
            error = not (0 <= element <= 0xffff)
        except ValueError:
            error = True
        if error:
            return 0
        ret_value = (ret_value << 16) + element
    return ret_value
    '''
    cme导出DB中ipv6地址转换
    ipstr必须为字符串类型
    '''
    if ipstr == None:
        return 0

    # 双冒号只能存在一次
    if ipstr.count("::") > 1:
        return 0

    # ipv6地址共8组128位
    ipv6_group_len = 8

    # 是否内嵌ipv4
    if ipstr.find('.') != -1:
        ip_v4_str = ipstr.split(":")[-1]
        if ip_v4_str.count(".") == 3:
            try:
                v4_int = ipv4_int(ip_v4_str)
            except:
                return 0
            v4_int_pre = "%04x" % (v4_int >> 16)
            v4_int_post = "%04x" % (v4_int & 0xffff)
            ipv4_to_ipv6 = "%s%s%s" % (v4_int_pre, ":", v4_int_post)
            ipstr = ipstr.replace(ip_v4_str, ipv4_to_ipv6)
        else:
            return 0
    try:
        if ipstr.find("::") != -1:
            double_colon_lst = ipstr.split("::")
            if double_colon_lst[0] == "":
                before_colon_lst = ["0"]
            else:
                before_colon_lst = double_colon_lst[0].split(":")
            if double_colon_lst[-1] == "":
                after_colon_lst = ["0"]
            else:
                after_colon_lst = double_colon_lst[-1].split(":")
            # 补全双冒号
            double_colon_count =  ipv6_group_len - len(before_colon_lst) - len(after_colon_lst)
            if double_colon_count <= 0:
                return 0

            elements = before_colon_lst + ["0"] * double_colon_count + after_colon_lst
        else:
            elements = ipstr.split(":")
            if len(elements) != ipv6_group_len:
                return 0
    except:
        return 0

    ret_value = 0
    for element in elements:
        try:
            element = int(element, 16)
            error = not (0 <= element <= 0xffff)
        except ValueError:
            error = True
        if error:
            return 0
        ret_value = (ret_value << 16) + element
    return ret_value

@API_RECORD
def convert_Int2Str_Ipv6(ipint):
    '''
    Ipv6地址转换
    '''
    s = []
    for i in range(8):
        s.append(hex(ipint % 65536).replace('0x', '').replace('L', '').zfill(4))
        ipint //= 65536
    return ':'.join(s[::-1])

@API_RECORD
def convert_Pfx2Mask_Ipv6(pfx_len):
    '''
    ipv6路由前缀
    '''
    pfx = ['1' for i in range(pfx_len)] + ['0' for i in range(128 - pfx_len)]
    return int(''.join(pfx), 2)

@API_RECORD
def check_ip_net_segment(ip1, ip2, mask):
    """
    判断2个IP是否同网段，针对网段包含，与当前OCL校验不同，
    只有2个IP分别与掩码相与的结果相等时，才能判定2个IP同网段，
    在网段包含下，如果仅仅是与网段大的掩码相与相等，不能判定2个IP同网段。
    :param ip1:
    :param mask:
    :param ip2:
    :return: True or False
    """
    if ip1 & mask == ip2 & mask:
        return True
    return False

@API_RECORD
def convert_Object(table_name, select_table, filter_func=None, fill_default=False, with_upper=False):
    return CVT_OBJ(table_name, select_table, filter_func, fill_default, with_upper)

@API_RECORD
def search_Files(filter_name, extensions=EXCEL_EXT_NAME):
    return SEARCH_FILES(filter_name, extensions)

@API_RECORD
def convert_Second2Degree(second):
    y = second.split(":", 3)
    return int(float(float(y[0]) + float(y[1]) / 60 + float(y[2]) / 3600) * 1000000)

@API_RECORD
def convert_Num2MaskStr(num):
    return MODEL.IPV4.toString( 4294967295 << (32-int(num)))

@API_RECORD
def convert_Num2Mask(num):
    return 4294967295 << (32-int(num))

@API_RECORD
def convert_moc_name(name):
    """Convert moc name to correct
    convert_moc_name("CELL")   ->   Cell
    convert_moc_name("CELLALGOSWITCH")    -> CellAlgoSwitch
    """
    r = CVT_CLASS_NAME(name)
    if not r:
        return None
    return r

@API_RECORD
def get_para_class(moc_name, para_name):
    """Return Para Class"""
    moc_class = CVT_CLASS(moc_name)
    if moc_class is None:
        return None
    para_name = convert_moc_para_name(moc_name, para_name)
    if para_name is None: return None
    para_class = getattr(moc_class, para_name)
    return para_class

@API_RECORD
def get_moc_para_type(moc_name, para_name):
    """Return Parameter Type：BitDomain, Enum, UnsignedLong, String, IpV4, IpV6, List, DateTime
    get_moc_para_type("RRU", "RS")   -> "Enum"
    """
    para_class = get_para_class(moc_name, para_name)
    if para_class is None: return None
    return para_class.typeName

@API_RECORD
def convert_moc_para_name(moc_name, para_name):
    """Convert parameter name to correct
    convert_moc_para_name("CELL", "DLBANDWIDTH")   ->   DlBandWidth
    convert_moc_para_name("CELLALGOSWITCH", ""RACHALGOSWITCH)    ->  RachAlgoSwitch
    """
    moc_class = CVT_CLASS(moc_name)
    if moc_class is None:
        return None
    all_para_list = moc_class._field_names_
    big_all_para_list = [s.upper() for s in all_para_list]
    para_name = para_name.upper()
    if para_name in big_all_para_list:
        return all_para_list[big_all_para_list.index(para_name)]
    return None

@API_RECORD
def convert_moc_value_name(moc_name, para_name, value_name):
    """Convert value name to correct
    convert_moc_value_name("cell", "DLBANDWIDTH", "cell_bw_n50")    ->  CELL_BW_N50
    convert_moc_value_name("CELLALGOSWITCH", "RACHALGOSWITCH", "RACHADJSWITCH")  ->  RachAdjSwitch
    """
    para_class = get_para_class(moc_name, para_name)
    if para_class is None: return None
    if para_class.typeName not in ["Enum", "BitDomain"]:  # Not Enum, Not Bit
        return None
    all_value_list = para_class._field_names_
    big_all_value_list = [s.upper() for s in all_value_list]
    value_name = value_name.upper()
    if value_name in big_all_value_list:
        return all_value_list[big_all_value_list.index(value_name)]
    return None

class BitObject: # Get/Set Bit Value
    """ Usage:
    bit = BitObject("BBP", "BBWS", "NBIOT")
    support_nb = bit.get(bbp_obj)  # get bit value
    bit.set(bbp_obj, 1)  # set bit value
    """
    @API_RECORD
    def __init__(self, moc_name, para_name, bit_name):
        self.moc_name = CVT_CLASS_NAME(moc_name)
        self.para_name = para_name
        self.bit_name = bit_name
        self.bit_pos = getattr(getattr(getattr(MODEL, moc_name), para_name), bit_name)
        pass

    @API_RECORD
    def get(self, moc_obj):
        para_value = getattr(moc_obj, self.para_name)
        bit_value = para_value & (1 << self.bit_pos)
        return 1 if bit_value else 0

    @API_RECORD
    def set(self, moc_obj, bit_value):
        para_value = getattr(moc_obj, self.para_name)
        if bit_value:
            para_value = para_value | (1 << self.bit_pos)
        else:
            para_value = para_value & (~(1 << self.bit_pos))
        setattr(moc_obj, self.para_name, para_value)
    pass

class BaseObject:
    cache_dict = {}

    """数据操作基类"""
    def get_moc(self, table_name, *filter_list, **kwargs):
        return LOAD_DATA(table_name, *filter_list, **kwargs)

    @API_RECORD
    def check_moc(self, table_name, *filter_list, **kwargs):
        return len(LOAD_DATA(table_name, *filter_list, **kwargs))

    @API_RECORD
    def get_MocCount(self, moc):
        return len(self.get_moc(moc))

    def save_moc(self, table_name, select_table, mode=OVERWRITE_MODE, **kwargs):
        return COMMIT_DATA(table_name, select_table, mode, **kwargs)

    @API_RECORD
    def save_all_mocs(self, doc, mode=OVERWRITE_MODE, include_mocs=None, exclude_mocs=None,with_clone=False, **kwargs):
        if with_clone is True:
            for moc_name in doc:
                doc[moc_name] = [x.clone(True) for x in doc[moc_name]]
        return COMMIT_DOC(doc, mode, include_mocs, exclude_mocs, **kwargs)

    def get_moc_list_by_del(self, select_table, *filter_list):
        return DELETE_DATA(select_table, *filter_list)

    def get_moc_list_by_mod(self, select_table, *updater_list, **kwargs):
        return UPDATE_DATA(select_table, *updater_list, **kwargs)

    def get_para_list_from_moc(self, select_table, para_name_list, *filter_list, **kwargs):
        return LOAD_PARA_LIST(select_table, para_name_list, *filter_list, **kwargs)

    @API_RECORD
    def get_para2_list_from_moc(self, select_table, para_name1,para_name2, *filter_list, **kwargs):
        para_name1_list = self.get_para_list_from_moc(select_table, para_name1, *filter_list, **kwargs)
        para2_list = []
        for para_name1_table in para_name1_list:
            para_name2_list = self.get_para_list_from_moc(para_name1_table, para_name2, *filter_list, **kwargs)
            for para2 in para_name2_list:
                para2_list.append(para2)
        return para2_list

    @API_RECORD
    def get_para_list_from_ne_tree(self,ne_tree,select_table, para_name_list, **kwargs):
        moc_list = ne_tree[select_table]
        para_list = []
        for moc in moc_list:
            mark = True
            for key,value in kwargs.items():
                if moc[key] != value:
                    mark = False
            if not mark:
                continue
            temp_list = []
            for para_name in para_name_list:
                temp_list.append(moc[para_name])
            para_list.append(temp_list)
        return para_list

    @API_RECORD
    def get_data_from_template(self, template_doc, table_name, *filter_list, **kwargs):
        return LOAD_TEMPLATE_DATA(template_doc, table_name, *filter_list, **kwargs)

    @API_RECORD
    def get_doc_from_template(self, template_name, with_raw=False, biz_mode=None):
        return LOAD_TEMPLATE(template_name, with_raw, biz_mode)

    @API_RECORD
    def save_data_with_template(self, select_table, template_item, filter_func=None, filter_child_func=None):
        return APPLY_TEMPLATE(select_table, template_item, filter_func, filter_child_func)

    @API_RECORD
    def get_data_from_ref(self, ref_doc, table_name, *filter_list, **kwargs):
        return LOAD_REF_DATA(ref_doc, table_name, *filter_list, **kwargs)

    @API_RECORD
    def get_all_moc_from_ref(self, ne_name, with_clone=False):
        return LOAD_REF_NE(ne_name, with_clone)

    @API_RECORD
    def modify_id_from_ne_tree(self, ne_tree, moc, para_list, id_replace_map):
        if "." in moc:
            moc, up_para = moc.split(".")
        else:
            up_para = None
        obj_list = getattr(ne_tree, moc, []) if ne_tree else LOAD_DATA(moc)
        for obj in obj_list:
            if up_para:
                for sub_obj in getattr(obj, up_para, []):
                    para_val_list = [getattr(sub_obj, para) for para in para_list]
                    # para_val = tuple(para_val_list)
                    temp = []
                    for ch in para_val_list:
                        if ch is None:
                            temp.append(ch)
                            continue
                        temp.append(int(ch))
                    para_val = tuple(temp)
                    if para_val in id_replace_map:
                        new_val_list = id_replace_map[para_val]
                        for (para, new_val) in zip(para_list, new_val_list):
                            setattr(sub_obj, para, new_val)
            else:
                if hasattr(obj, para_list[0]) is False: continue
                para_val_list = [getattr(obj, para, None) for para in para_list]
                # para_val = tuple(para_val_list)
                temp = []
                for ch in para_val_list:
                    if ch is None:
                        temp.append(ch)
                        continue
                    temp.append(int(ch))
                para_val = tuple(temp)
                if para_val in id_replace_map:
                    new_val_list = id_replace_map[para_val]
                    for (para, new_val) in zip(para_list, new_val_list):
                        setattr(obj, para, new_val)
        if not ne_tree:
            COMMIT_DATA(moc, obj_list, OVERWRITE_MODE)
        pass

    @API_RECORD
    def compare_site_by_moc(self, ne_tree, moc_name):
        moc_different_list = []
        para_name_list, primary_key_list, no_primary_key_list = self.get_para_name_list_from_model(moc_name)
        para_value_orig_list = self.get_para_list_from_ne_tree(ne_tree, moc_name, para_name_list)
        para_value_target_list = self.get_para_list_from_ne_tree(ne_tree, moc_name, para_name_list)
        if len(para_value_orig_list) != len (para_value_target_list):
            if moc_name not in moc_different_list:
                moc_different_list.append(moc_name)
        primary_value_list = self.get_para_list_from_ne_tree(ne_tree, moc_name, primary_key_list)
        if len(primary_key_list)==0 or len(no_primary_key_list)==0 or len(primary_value_list) == 0:
            data_target_list = self.get_para_list_from_moc(moc_name, para_name_list)
            if len(no_primary_key_list) == 1:
                data_target_list = [[tartget_data] for tartget_data in data_target_list]
            data_orig_list = self.get_para_list_from_ne_tree(ne_tree, moc_name,para_name_list)
            if data_target_list != data_orig_list:
                if not self.is_equal_obj(data_target_list, data_orig_list):
                    if moc_name not in moc_different_list:
                        moc_different_list.append(moc_name)
        else:
            for primary_value_dic in primary_value_list:
                primary_key_value_dic = {}
                for i, primary_key_value in enumerate(primary_value_dic):
                    primary_key_value_dic[primary_key_list[i]] = primary_key_value
                data_target_list = self.get_para_list_from_moc(moc_name, no_primary_key_list,WHERE(**primary_key_value_dic))
                if len(no_primary_key_list) == 1:
                    data_target_list = [[tartget_data] for tartget_data in data_target_list]
                data_orig_list = self.get_para_list_from_ne_tree(ne_tree, moc_name, no_primary_key_list,**primary_key_value_dic)
                if data_target_list != data_orig_list:
                    if not self.is_equal_obj(data_target_list, data_orig_list):
                        if moc_name not in moc_different_list:
                            moc_different_list.append(moc_name)
        if moc_name in moc_different_list:
            return False,para_name_list,para_value_orig_list,para_value_target_list
        else:
            return True,para_name_list,para_value_orig_list,para_value_target_list

    @API_RECORD
    def is_equal_obj(self, data_target_list, data_orig_list):
        if len(data_target_list) != len(data_orig_list):
            return False
        for _index, target_attrs in enumerate(data_target_list):
            origin_attrs = data_orig_list[_index]
            if len(target_attrs) != len(origin_attrs):
                return False
            for _attr_index, target_attr_value in enumerate(target_attrs):
                origin_attr_value = origin_attrs[_attr_index]
                if isinstance(target_attr_value, list) and isinstance(origin_attr_value, list):
                    if len(target_attr_value) != len(origin_attr_value):
                        return False
                    else:
                        for _child_index, tartget_child_moi in enumerate(target_attr_value):
                            origin_child_moi = origin_attr_value[_child_index]
                            for target_child_attr in tartget_child_moi["BasicAttr"]:
                                child_attr_name = target_child_attr._Name
                                if tartget_child_moi[child_attr_name] != origin_child_moi[child_attr_name]:
                                    return False
                else:
                    if target_attr_value != origin_attr_value:
                        return False
        return True

    @API_RECORD
    def get_product_type(self):
        product_type_dict = {
            "1": "DBS3900_LTE", "2": "BTS3900_LTE", "3": "BTS3900A_LTE", "4": "BTS3900L_LTE", "5": "BTS3900AL_LTE",
            "7": "DBS3900_LampSite_LTE", "8": "DBS5900_LTE", "9": "BTS5900_LTE",
            "10": "BTS5900A_LTE", "11": "BTS5900L_LTE", "12": "BTS5900AL_LTE", "13": "DBS5900_LampSite_LTE",
            "14": "DBS3900_WCDMA", "15": "BTS3900_WCDMA", "16": "BTS3900A_WCDMA", "17": "BTS3900L_WCDMA",
            "18": "BTS3900AL_WCDMA", "23": "DBS3900_LampSite_WCDMA", "24": "DBS5900_WCDMA", "25": "BTS5900_WCDMA",
            "26": "BTS5900A_WCDMA", "27": "BTS5900L_WCDMA", "28": "BTS5900AL_WCDMA", "29": "DBS5900_LampSite_WCDMA",
            "100": "BTS3202E",
            "117": "DBS3900", "118": "BTS3900", "119": "BTS3900A", "120": "BTS3900L",
            "121": "BTS3900AL", "123": "DBS3900_LampSite", "125": "DBS5900", "135": "DBS5900_LampSite",
            "122": "BTS3911E", "124": "BTS3912E",
            "212": "DBS5900_5G", "217": "DBS3900_5G",
            "221": "DBS3900_LampSite_5G", "222": "DBS5900_LampSite_5G",
            "256": "DBS5900A", "257": "DBS5900E",
            "320": "DBS5900A_WCDMA", "321": "DBS5900E_WCDMA",
            "384": "DBS5900A_LTE", "385": "DBS5900E_LTE",
            "448": "DBS5900A_5G", "449": "DBS5900E_5G",
        }
        return product_type_dict

    @API_RECORD
    def exit_Info(self, cause='Please fill description for this error!'):
        return EXIT(code=1, cause="Error: %s" % cause)

    @API_RECORD
    def finish(self, msg=""):
        msg = "".join(["\nNE=", NENAME, " Done.\n", msg])
        self.print_msg(msg)

    @API_RECORD
    def print_msg(self, string):
        print(string)

    @API_RECORD
    def warning_Info(self, msg="Please Fill description for this warning!"):
        msg = "Warning: %s" % msg
        self.print_msg(msg)

    @API_RECORD
    def inner_load_Summary_SHEET_DEF_sheet(self):
        sheet_list = GET_SHEET_NAMES(self.summary_file_name)
        if "SHEET DEF" not in sheet_list:
            msg = "Error: No SHEET DEF sheet. File=%s is not a valid Summary file." % self.summary_file_name
            raise Exception(msg)
        data_dict = LOAD_EXCEL_FILE(self.summary_file_name, "SHEET DEF", title_row=1, group_title="Sheet Name")
        for (sheet_name, row_list) in data_dict.items():
            row = row_list[0]
            self.summary_sheet_define_dict[sheet_name] = (row["Sheet Type"], row["Mapping Type"])
            if row["Sheet Type"] == "COMMON":
                self.summary_common_sheet_name = sheet_name
            if row["Sheet Type"] == "MAIN":
                self.summary_base_station_sheet_name = sheet_name
            pass
        return True

    @API_RECORD
    def inner_load_Summary_MAPPING_DEF_sheet(self):
        sheet_list = GET_SHEET_NAMES(self.summary_file_name)
        if "MAPPING DEF" not in sheet_list:
            msg = "Error: No MAPPING DEF sheet. File=%s is not a valid Summary file." % self.summary_file_name
            raise Exception(msg)
        self.summary_sheet_mapping_dict = LOAD_EXCEL_FILE(self.summary_file_name, "MAPPING DEF", title_row=1, group_title="Sheet Name")
        return True

    @API_RECORD
    def inner_load_Summary_Common_Data_sheet(self):
        row_list = self.summary_sheet_mapping_dict[self.summary_common_sheet_name]
        group_name_list = []
        for row in row_list:
            group_name = row["Group Name"]
            if group_name not in group_name_list:
                group_name_list.append(group_name)
            pass
        for group_name in group_name_list:
            print("Info: Parse Common Data Group=%s...." % group_name)
            row, col = SEARCH_IN_EXCEL_FILE(group_name, self.summary_file_name, self.summary_common_sheet_name, 1, 9999, 1, 1)
            group_data_list = LOAD_EXCEL_DATA(self.summary_file_name, self.summary_common_sheet_name, row+1, empty_break=True, empty_break_row=1)
            self.summary_common_group_data_dict[group_name] = group_data_list
        return True

    @API_RECORD
    def innner_load_Summary_Pattern_sheet(self, is_controller=False):
        for (sheet_name, (sheet_type, mapping_type)) in self.summary_sheet_define_dict.items():
            if sheet_type != "Pattern": continue
            print("Info: Parse Sheet=%s...." % sheet_name)
            if is_controller is True and "CONTROLLER" not in mapping_type: continue
            if is_controller is False and "CONTROLLER" in mapping_type: continue
            row_list = self.summary_sheet_mapping_dict[sheet_name]
            key_row_list = [row for row in row_list if row["Is Key"] == "TRUE"]
            key_title = key_row_list[0]["Group Name"] + key_row_list[0]["Column Name"]
            moc_data_list = LOAD_EXCEL_DATA(self.summary_file_name, sheet_name, title_start_row=1, group_title=key_title,
                                            title_row=2, empty_break=True, empty_break_row=100)
            self.summary_moc_data_dict[sheet_name] = moc_data_list
        return True

    @API_RECORD
    def inner_parse_Summary_Base_Station_sheet(self):
        data_list = LOAD_EXCEL_DATA(self.summary_file_name, self.summary_base_station_sheet_name, title_start_row=1, title_row=2)
        for row in self.summary_sheet_mapping_dict[self.summary_base_station_sheet_name]:
            group_name = row["Group Name"]
            column_name = row["Column Name"]
            value = data_list[0][group_name + column_name]
            if row["MOC Name"] == "Customization_CME" and row["Attribute Name"] == "Scenario":
                self.summary_customize_dict[group_name + "\\" + column_name] = []
            key = "\\".join([self.summary_base_station_sheet_name, group_name, column_name])
            self.summary_base_station_dict[key] = value
        return True

    @API_RECORD
    def inner_parse_Summary_Common_moc_data(self, doc_tree, is_controller):
        common_data_row_list = self.summary_sheet_mapping_dict["Common Data"]
        for (group_name, data_row_list) in self.summary_common_group_data_dict.items():
            group_attribute_row_list = [row for row in common_data_row_list if row["Group Name"] == group_name]
            moc_list = [row["MOC Name"] for row in group_attribute_row_list if row["MOC Name"]]
            moc_list = list(set(moc_list))
            if len(moc_list) == 0:
                doc_tree[group_name] = []
                for data_row in data_row_list:
                    tmp_data_dict = {}
                    for attr_row in group_attribute_row_list:
                        column_name = attr_row["Column Name"]
                        tmp_data_dict[column_name] = data_row[column_name]
                    doc_tree[group_name].append(tmp_data_dict)
            else:
                for moc in moc_list:
                    ne_type_list = [attr_row["Ne Type"] for attr_row in group_attribute_row_list if attr_row["Ne Type"]]
                    ne_type = ne_type_list[0].upper()
                    if is_controller is True and "CONTROLLER" not in ne_type: continue
                    if is_controller is False and "CONTROLLER" in ne_type: continue
                    if hasattr(MODEL, moc) is False: continue
                    doc_tree[moc] = []
                    for data_row in data_row_list:
                        moc_class = getattr(MODEL, moc)
                        moc_obj = moc_class()
                        for attr_row in group_attribute_row_list:
                            ne_type = attr_row["Ne Type"]
                            column_name = attr_row["Column Name"]
                            para_name = attr_row["Attribute Name"]
                            value = data_row[column_name]
                            if attr_row["MOC Name"]:
                                if attr_row["MOC Name"] != moc: continue
                                setattr(moc_obj, para_name, value)
                            else:
                                setattr(moc_obj, column_name, value)
                        doc_tree[moc].append(moc_obj)
        return doc_tree

    @API_RECORD
    def inner_parse_Summary_Pattern_moc_data(self, doc_tree):
        for (sheet_name, row_list) in self.summary_moc_data_dict.items():
            moc_list = [row["MOC Name"] for row in self.summary_sheet_mapping_dict[sheet_name] if row["MOC Name"]]
            moc_list = list(set(moc_list))
            for moc_name in moc_list:
                if moc_name == "Customization_CME": continue
                doc_tree[moc_name] = []
                if hasattr(MODEL, moc_name) is False: continue
                moc_class = getattr(MODEL, moc_name)
                for data_row in row_list:
                    moc_obj = moc_class()
                    for attr_row in self.summary_sheet_mapping_dict[sheet_name]:
                        attr_moc_name = attr_row["MOC Name"]
                        if attr_moc_name not in [None, moc_name, "Customization_CME"]: continue
                        group_name = attr_row["Group Name"]
                        column_name = attr_row["Column Name"]
                        para_name = attr_row["Attribute Name"]
                        value = data_row[group_name + column_name]
                        if attr_moc_name == moc_name:
                            if not value: continue
                            if "\\" in value and value[-1] == "]":
                                tmp_str, idx = value[:-1].split("[")
                                tmp, tmp_group_name, tmp_column_name = tmp_str.split("\\")
                                value = self.summary_common_group_data_dict[tmp_group_name][int(idx)][tmp_column_name]
                            elif "\\" in value:
                                value = self.summary_base_station_dict[value]
                            setattr(moc_obj, para_name, value)
                        else:
                            setattr(moc_obj, group_name + "\\" + column_name, value)
                        if attr_moc_name == "Customization_CME":
                            self.summary_customize_dict[group_name + "\\" + column_name].append(moc_name)
                    doc_tree[moc_name].append(moc_obj)
            pass
        return doc_tree

    @API_RECORD
    def inner_parse_Summary(self, summary_file_name, is_controller=False):
        # initilize
        cache_key = "Inner Summary=%s.%s" % (summary_file_name, is_controller)
        if cache_key in self.cache_dict:
            return self.cache_dict[cache_key]
        self.summary_file_name = summary_file_name
        self.summary_base_station_dict = {}
        self.summary_customize_dict = {}
        self.summary_common_sheet_name = None
        self.summary_base_station_sheet_name = None
        self.summary_sheet_define_dict = {}
        self.summary_common_group_data_dict = {}
        self.summary_moc_data_dict = {}
        # Parse Summary
        self.inner_load_Summary_SHEET_DEF_sheet()
        self.inner_load_Summary_MAPPING_DEF_sheet()
        self.inner_parse_Summary_Base_Station_sheet()
        self.inner_load_Summary_Common_Data_sheet()
        self.innner_load_Summary_Pattern_sheet(is_controller)
        doc_tree = CREATE_DOC()
        self.inner_parse_Summary_Common_moc_data(doc_tree, is_controller)
        self.inner_parse_Summary_Pattern_moc_data(doc_tree)
        self.cache_dict[cache_key] = doc_tree
        return doc_tree

    @API_RECORD
    def inner_Summary_replace_variable(self, doc_tree, variable_dict):
        moc_tree = COPY_DOC(doc_tree)
        result_tree = CREATE_DOC()
        for moc_name in moc_tree._fields_:
            if not hasattr(moc_tree, moc_name): continue  # 避免二次调用报错
            obj_list = getattr(moc_tree, moc_name)
            if type(obj_list) is not list: continue
            if len(obj_list) == 0: continue
            if not hasattr(MODEL, moc_name):
                result_tree[moc_name] = obj_list
                continue
            new_obj_list = []
            for obj in obj_list:
                if "metaclass.NE" in str(type(obj)) and moc_name != "NE":
                    continue
                for para_name in obj._type_._field_names_:
                    if hasattr(obj, para_name):
                        value = getattr(obj, para_name)
                        if type(value) == str and value.startswith("$"):
                            if value[1:] in variable_dict:
                                real_value = variable_dict[value[1:]]
                                setattr(obj, para_name, real_value)
                            else:
                                msg = "   Value not set for Variable=%s (MOC=%s Para=%s)\n" % (value, moc_name, para_name)
                                if msg not in self.failure_reason_list:
                                    self.failure_reason_list.append(msg)
                    pass
                new_obj_list.append(obj)
            new_obj_list = CVT_OBJ(moc_name, new_obj_list)
            result_tree[moc_name] = new_obj_list
        return result_tree

    @API_RECORD
    def inner_Summary_filter_by_customize_scenario(self, doc_tree, customer_scenario_dict):
        for (customize_scenario, moc_list) in self.summary_customize_dict.items():
            scenario_variable = self.summary_base_station_dict[self.summary_base_station_sheet_name + "\\" + customize_scenario]
            if scenario_variable is None:  # 表格中场景字段没有填写内容
                msg = "   Cannot filter by Customize Scenario=%s because NO Variable input in Summary file.\n" % (customize_scenario)
                self.failure_reason_list.append(msg)
                continue
            elif scenario_variable.startswith("$"):  # 填写的变量
                if scenario_variable[1:] not in customer_scenario_dict:
                    msg = "   Value not set for variable=%s for Customize Scenario=%s.\n" % (scenario_variable, customize_scenario)
                    self.failure_reason_list.append(msg)
                    continue
                scenario_value = customer_scenario_dict[scenario_variable[1:]]
            else:  # 填写的固定值
                scenario_value = scenario_variable
            if scenario_value is None:
                scenario_list = []
            else:
                scenario_list = scenario_value.split(",")
                scenario_list = [s.strip() for s in scenario_list if len(s.strip()) > 0]
            moc_list = list(set(moc_list))
            for moc_name in moc_list:
                obj_list = getattr(doc_tree, moc_name)
                new_obj_list = []
                for obj in obj_list:
                    value = getattr(obj, customize_scenario)
                    if value is None or value in scenario_list:
                        new_obj_list.append(obj)
                setattr(doc_tree, moc_name, new_obj_list)
        pass

    @API_RECORD
    def inner_load_Summary_file(self, summary_file_name, variable_dict, is_controller=False):
        """Load Data from Summary File. Return moc tree"""
        self.failure_reason_list = []
        doc_tree = self.inner_parse_Summary(summary_file_name, is_controller)
        result_tree = self.inner_Summary_replace_variable(doc_tree, variable_dict)
        self.inner_Summary_filter_by_customize_scenario(result_tree, variable_dict)

        if len(self.failure_reason_list) > 0:
            raise Exception("Error\n" + "".join(self.failure_reason_list))
        return result_tree

    @API_RECORD
    def get_para_name_list_from_model(self,moc_name):
        para_name_list = getattr(MODEL, moc_name)._field_names_
        primary_key_list = []
        no_primary_key_list = []
        para_list = getattr(MODEL, moc_name)._fields_
        for para in para_list:
            if para[3] is True:
                primary_key_list.append(para[0])
            else:
                no_primary_key_list.append(para[0])
        return para_name_list,primary_key_list,no_primary_key_list

    def add_moc(self, select_table, **kwargs):
        obj = getattr(MODEL, select_table)(**kwargs)
        self.save_moc(select_table, [obj], APPEND_MODE, with_child=True, with_merge=True)

    @API_RECORD
    def set_moc(self, select_table, **kwargs):
        obj = getattr(MODEL, select_table)(**kwargs)
        self.save_moc(select_table, [obj], OVERWRITE_MODE)

    def mod_moc(self, select_table, *updater_list, **kwargs):
        obj_list = self.get_moc_list_by_mod(select_table, *updater_list, **kwargs)
        self.save_moc(select_table, obj_list, OVERWRITE_MODE)

    @API_RECORD
    def mod_SubParaInMoc(self, select_table, *updater_list, **kwargs):
        if "/" not in select_table and "\\" not in select_table:
            msg = "no Sub Para in the Moc"
            self.exit_Info(msg)
        else:
            ne_trees = []
            select_table.replace("\\", "/")
            select_moc_table, select_para_table = select_table.split("/")
            if len(updater_list) == 2:
                children_updater_list = updater_list[0]
                parent_updater_list = updater_list[1]
                ne_trees = self.get_moc(select_moc_table, parent_updater_list, with_child=True)
            elif len(updater_list) == 1:
                ne_trees = self.get_moc(select_moc_table, with_child=True)
                children_updater_list = updater_list[0]
            else:
                self.exit_Info("The input parameter of the mod_SubParaInMoc method is incorrect")
            for ne_tree in ne_trees:
                mod_para_table = self.get_moc_list_by_mod(ne_tree[select_para_table], children_updater_list, **kwargs, is_new=True)
                ne_tree[select_para_table] = mod_para_table
            self.save_moc(select_moc_table, ne_trees, APPEND_MODE, with_child=True, with_merge=True)


    @API_RECORD
    def mod_moc_Ex(self, select_table, *updater_list, **kwargs):
        obj_list = self.get_moc_list_by_mod(select_table, *updater_list, **kwargs)
        self.save_moc(select_table, obj_list, OVERWRITE_MODE, with_child=True, with_assoc=True)

    def del_moc(self, select_table, *filter_list):
        obj_list = self.get_moc_list_by_del(select_table, *filter_list)
        self.save_moc(select_table, obj_list, OVERWRITE_MODE)

    @API_RECORD
    def del_moc_Ex(self, select_table, *filter_list):
        obj_list = self.get_moc_list_by_del(select_table, *filter_list)
        self.save_moc(select_table, obj_list, OVERWRITE_MODE, with_child=True, with_assoc=True)

    @API_RECORD
    def add_moc_into_moc_tree(self, ne_tree, select_table, **kwargs):
        obj = getattr(MODEL, select_table)(**kwargs)
        ne_tree[select_table] = ne_tree[select_table].append(obj)

    @API_RECORD
    def mod_moc_in_moc_tree(self, ne_tree, select_table, *updater_list, **kwargs):
        obj_list = self.get_moc_list_by_mod(ne_tree[select_table], *updater_list, **kwargs)
        ne_tree[select_table] = obj_list

    @API_RECORD
    def set_moc_in_moc_tree(self, ne_tree, select_table, **kwargs):
        obj = getattr(MODEL, select_table)(**kwargs)
        ne_tree[select_table] = [obj]

    @API_RECORD
    def del_moc_from_moc_tree(self, ne_tree, select_table):
        del ne_tree[select_table]

    @API_RECORD
    def get_free_id_list(self,moc,para, id_start=0, id_end=65535, *filter_list, **kwargs):
        for x in range(int(id_start), id_end):
            if x not in self.get_para_list_from_moc(moc, para, *filter_list, **kwargs):
                return [x]

    # 查找合适ID的函数，如果perfer_id已经存在，则分配一个新ID
    @API_RECORD
    def get_Available_ID(self, moc, para_name, prefer_id=None, max_value=1000, step=1, *filter_list, **kwargs):
        prefer_id = int(prefer_id)
        existing_id_list = self.get_para_list_from_moc(moc, para_name, *filter_list, **kwargs)
        if prefer_id not in existing_id_list and prefer_id is not None:
            return prefer_id
        if prefer_id is None :
            prefer_id = 1
        for idx in range(prefer_id, max_value + 1, step):
            if idx not in existing_id_list:
                self.print_msg("%s=%d is already occupied. set to %d" % (para_name, prefer_id, idx))
                return idx
        self.print_msg("Error: No Available ID for %s" % (para_name))
        return None

    @API_RECORD
    def del_Duplicate(self, moc, para_list):
        obj_list = self.get_moc(moc)
        if len(obj_list) < 2: return
        obj_list = CVT_OBJ(moc, obj_list)
        new_value_list = []
        new_obj_list = []
        for obj in obj_list:
            value = [getattr(obj, para) for para in para_list]
            if value not in new_value_list:
                new_value_list.append(value)
                new_obj_list.append(obj)
            pass
        self.save_moc(moc, new_obj_list, OVERWRITE_MODE)

    # 从项目配置页签，或者指定 item的设置。标题默认在第二列
    @API_RECORD
    def get_Project_Setting(self, excel_file, sheet_name, item_name, area=None, row_title=2, value_title="ITEM_Value"):
        setting_map = load_Excel_File(excel_file, sheet_name, row_title, "ITEM_Name")
        if item_name not in setting_map:
            self.exit_Info("%s is found in sheet=%s, file=%s" % (item_name, sheet_name, excel_file))
        if area is not None:
            value = None
            for item_info in setting_map[item_name]:
                if not item_info.exist_attr("Area"):
                    self.exit_Info("title=Area is not exist in sheet=%s file=%s" % (sheet_name, excel_file))
                if item_info["Area"] == area:
                    value = item_info.attr(value_title)
                    break
            if value is None:
                self.exit_Info("Aear=%s Item=%s is not found in sheet=%s file=%s" % (area, item_name, sheet_name, excel_file))
        else:
            value = setting_map[item_name][0].attr(value_title)
        return value

    # id_replace_map存在了 需要ID更改的对应关系。本函数返回正确的修改顺序，避免出现前一个赋值把后一个覆盖的情况
    # 举例，需要修改1->2, 2->3; 则需要先执行 2->3, 再执行 1->2
    @API_RECORD
    def get_ID_Replace_List(self, id_replace_map):
        replace_list = []
        oldid_list = list(id_replace_map.keys())
        newid_list = list(id_replace_map.values())
        while len(oldid_list) > 0:
            tempid = None
            if oldid_list == newid_list:  # 两者完全相同
                newid = newid_list[0]
            elif set(oldid_list) == set(newid_list):
                tempid = (100, 100, 100, 100)
                newid = newid_list[0]
            else:
                diff_list = list(set(newid_list).difference(set(oldid_list)))
                if len(diff_list) == 0:
                    self.print_msg("Error: Cannot Modify ID as inter-modify" + id_replace_map)
                    return None
                newid = diff_list[0]
            oldid = oldid_list[newid_list.index(newid)]
            if oldid != newid and tempid is not None:
                replace_list.append((newid, tempid))
                replace_list.append((oldid, newid))
                replace_list.append((tempid, oldid))
                oldid_list.remove(newid)
                newid_list.remove(oldid)
            elif oldid != newid:
                replace_list.append((oldid, newid))
            else:
                pass

            oldid_list.remove(oldid)
            newid_list.remove(newid)

        return replace_list

    @API_RECORD
    def read_RF_Para(self, excel_filename, sheet_name, output_title_list, default_value_row,
                     title_row=1, mo_title="MO", key_para_title="KeyPara", parameter_title="Parameter", switch_title="Switch",
                     value_title="Config Value", default_value_title="Default Value", **kwargs):
        """读取RF参数表，返回一个字典"""
        para_setting_map = load_Excel_File(excel_filename, sheet_name, title_row=title_row, group_title=mo_title, **kwargs)
        rf_para_setting_dict = {}
        for (mo, row_list) in para_setting_map.items():
            for excel_row in row_list:
                if "DO" in excel_row and excel_row["DO"] == "NO": continue
                if key_para_title is not None:
                    key_para_name = excel_row[key_para_title]
                else:
                    key_para_name = None
                parameter = excel_row[parameter_title]
                if switch_title is not None:  # 如果输入了开关名称，则和Parameter合并起来，用:间隔
                    switch_name = excel_row[switch_title]
                    if switch_name is not None:
                        parameter = "%s: %s" % (parameter, switch_name)
                default_value = excel_row[default_value_title]
                if default_value is not None and default_value.upper() in ["N/A", "NONE"]:
                    default_value = None
                config_value = excel_row[value_title]
                if config_value is not None and config_value.upper() in ["N/A", "NONE"]:
                    config_value = None
                if config_value is None:
                    config_value = default_value
                if default_value is None and config_value is None: continue
                if default_value and "(" in default_value:
                    default_value = default_value.split("(")[0].strip()
                if config_value and "(" in config_value:
                    config_value = config_value.split("(")[0].strip()
                if mo not in rf_para_setting_dict:
                    rf_para_setting_dict[mo] = []
                rf_para_setting_dict[mo].append([parameter, config_value, default_value, key_para_name])
                if key_para_name:
                    new_title = "%s\n%s\n(%s)" % (mo, parameter, key_para_name)
                else:
                    new_title = "%s\n%s" % (mo, parameter)
                if new_title not in output_title_list:
                    output_title_list.append(new_title)
                    default_value_row[new_title] = default_value
            pass
        return rf_para_setting_dict

    @API_RECORD
    def save_RF_Para_result(self, excel_filename, sheetname, output_title_list, result_excel_row, default_value_row, transpose=False):
        """把RF参数修改结果写入Excel文件"""
        default_value_row["Detail"] = "Default Value"
        target_filename = "RF_Para_Result"
        COPY_EXCEL_FILE(source_name=excel_filename, target_name=target_filename)
        RF_para_dump_map = LOAD_OBJ("RF_Para_Result", {})
        if sheetname not in RF_para_dump_map:
            RF_para_dump_map[sheetname] = {"ROW": 4, "COL": 0}

        # 写入标题
        start_col = RF_para_dump_map[sheetname]["COL"]
        for col in range(start_col, len(output_title_list)):
            title = output_title_list[col]
            if "\n" in title:
                mo, parameter = title.split("\n", 1)
                if transpose is True:
                    WRITE_EXCEL_CELL(excel_name=target_filename, sheet_name=sheetname, col_no=1, row_no=col + 1, cell_value=mo)
                    WRITE_EXCEL_CELL(excel_name=target_filename, sheet_name=sheetname, col_no=2, row_no=col + 1, cell_value=parameter)
                else:
                    WRITE_EXCEL_CELL(excel_name=target_filename, sheet_name=sheetname, row_no=1, col_no=col + 1, cell_value=mo)
                    WRITE_EXCEL_CELL(excel_name=target_filename, sheet_name=sheetname, row_no=2, col_no=col + 1, cell_value=parameter)
            else:
                if transpose is True:
                    WRITE_EXCEL_CELL(excel_name=target_filename, sheet_name=sheetname, col_no=2, row_no=col + 1, cell_value=title)
                else:
                    WRITE_EXCEL_CELL(excel_name=target_filename, sheet_name=sheetname, row_no=2, col_no=col + 1, cell_value=title)
            if title in default_value_row:
                value = default_value_row[title]
                if transpose is True:
                    WRITE_EXCEL_CELL(excel_name=target_filename, sheet_name=sheetname, col_no=3, row_no=col + 1, cell_value=value)
                else:
                    WRITE_EXCEL_CELL(excel_name=target_filename, sheet_name=sheetname, row_no=3, col_no=col + 1, cell_value=value)
        pass
        # 写入本小区的参数修改结果
        row_no = RF_para_dump_map[sheetname]["ROW"]
        for (col, title) in enumerate(output_title_list):
            if title in result_excel_row:
                value = result_excel_row[title]
                if transpose is True:
                    WRITE_EXCEL_CELL(excel_name=target_filename, sheet_name=sheetname, col_no=row_no, row_no=col + 1, cell_value=value)
                else:
                    WRITE_EXCEL_CELL(excel_name=target_filename, sheet_name=sheetname, row_no=row_no, col_no=col + 1, cell_value=value)
            pass
        RF_para_dump_map[sheetname] = {"ROW": row_no + 1, "COL": len(output_title_list)}
        DUMP_OBJ("RF_Para_Result", RF_para_dump_map)
        pass

    pass


# 基站对象
class BTSObject(BaseObject):
    rat_list = []
    short_rat_list = []
    WSD_Info_Cache = {}
    BOM_dict = {}
    CONFIG_dict = {}
    Rat_BBP_Cache = {"G": [], "U": [], "L": [], "F": [], "T": [], "N": []}
    ID_Plan_Cache = {}
    Com_Plan_Cache= {}
    UMTS_Cell_Count = 0
    BaseBandEqm_Cache = {"G": [], "U": {"DL":[],"UL":[]}, "L": [], "F": [], "T": [], "N": []}
    Tree_Dict = {'G': [], 'U':[], 'L': [], 'NR': [], 'COMPT': []}
    # For JSON to CME Decoding
    rat_map = {"GO": "GSM",
               "UO": "UMTS",
               "LO": "LTE",
               "MO": "NB",
               "TO": "TDD",
               "NO":"NO"}
    @API_RECORD
    def __init__(self):
        self.NEName = None
        self.BTSName = None
        self.NodeBName = None
        self.eNodeBName = None
        self.gNodeBName = None
        self.NEVERSION = None
        self.ProductType = None
        self.RRULIST = None
        self.RFULIST = None
        self.BBPLIST = None
        self.MPTLIST = None
        self.Analyze_Cache = {"Band_Sector_To_LocalCellId": {},
                              "Band_Sector_To_ULOCELLID":{},
                              "Band_Sector_To_GLOCELLID":{},
                              "Band_Sector_To_SectorEqmId": {},
                              "Band_Sector_To_GTRXGROUPID": {},
                              "Band_Sector_To_SectorId": {},
                              "Band_Sector_To_RXU": {},
                              "Band_Sector_To_RruChain": {},
                              "Band_Sector_To_Bbp_Port": {}}
        self.ratStr = ""
        self.start()

    # 方法操作动作定义
    # get 获取
    # add 添加
    # del 删除
    # mod 修改
    # set 如果存量没有则添加，有则覆盖

    @API_RECORD
    def start(self):
        self.NEName = self.get_moc("NE")[0].NENAME
        self.print_msg("Process NE=" + self.NEName)
        self.NEVERSION = self.get_moc("NE")[0].PRODUCTVERSION
        if len(self.get_moc("NODE")) > 0:
            self.ProductType = self.get_moc("NODE")[0].PRODUCTTYPE
        if len(self.get_moc("GBTSFUNCTION")) > 0:
            self.BTSName = self.get_moc("GBTSFUNCTION")[0].GBTSFUNCTIONNAME
            self.ratStr += "G"
        if len(self.get_moc("NODEBFUNCTION")) > 0:
            self.NodeBName = self.get_moc("NODEBFUNCTION")[0].NODEBFUNCTIONNAME
            self.ratStr += "U"
        if len(self.get_moc("eNodeBFunction")) > 0:
            self.eNodeBName = self.get_moc("eNodeBFunction")[0].eNodeBFunctionName
            self.ratStr += "L"
        if len(self.get_moc("gNodeBFunction")) > 0:
            self.gNodeBName = self.get_moc("gNodeBFunction")[0].gNodeBFunctionName
            self.ratStr += "N"

    @API_RECORD
    def load_Summary_file(self, summary_file_name, variable_dict):
        """从Summary文件创建数据，variable_dict为变量字典"""
        doc_tree = BaseObject.inner_load_Summary_file(self, summary_file_name, variable_dict, is_controller=False)
        return doc_tree

    @API_RECORD
    def get_data_from_excel(self, excel_name, sheet_name, title_row, group_title, ne_name=None, **kwargs):
        if ne_name is None:
            ne_name = self.NEName
        data_map = load_Excel_File(excel_name, sheet_name, title_row, group_title, **kwargs)
        if ne_name not in data_map:
            self.print_msg('%s is not in the %s file %s sheet' %(ne_name, excel_name, sheet_name))
            return []
        return data_map[ne_name]

    @API_RECORD
    def get_data_from_csv(self, csv_name, ne_title_name=None, ne_name=None):
        csv_data = LOAD_CSV_FILE(csv_name)

        if ne_title_name == None or ne_name == None:
            return csv_data

        for row in csv_data:
            if row[ne_title_name] == ne_name:
                return row

    @API_RECORD
    def get_parameter_name_value(self, Common_Parameter_map, parameter_name):
        for k, v in Common_Parameter_map.items():
            if parameter_name == k:
                count = 1
                for excel_row in v:
                    if count > 1:
                        msg = "Error: {} map multi row".format(k)
                        self.exit_Info(msg)
                        break
                    count += 1
                    return excel_row.Values

    @API_RECORD
    def get_parameter_name(self, Common_Parameter_map, parameter_name):
        for k, v in Common_Parameter_map.items():
            if parameter_name == k:
                count = 1
                for excel_row in v:
                    if count > 1:
                        msg = "Error: {} map multi row".format(k)
                        self.exit_Info(msg)
                        break
                    count += 1
                    return excel_row

    @API_RECORD
    def get_SiteInfo(self, site_info_excel_name, site_name_title="*Name", site_info_sheet_name="Base Station Transport Data", ne_name=None, title_row=2, **kwargs):
        site_info_list = self.get_data_from_excel(excel_name=site_info_excel_name, sheet_name=site_info_sheet_name, group_title=site_name_title, title_row=title_row, ne_name=ne_name, **kwargs)
        if len(site_info_list) == 0:
            if ne_name is None:
                ne_name = self.NEName
            msg = "Error: NE=%s is not found in file %s sheet %s" % (ne_name, site_info_excel_name,site_info_sheet_name)
            self.exit_Info(msg)
        elif len(site_info_list) > 1:
            msg = "NE=%s has %d duplicate data in file %s sheet %s" % (ne_name, len(site_info_list), site_info_excel_name,site_info_sheet_name)
            self.exit_Info(msg)

        if "*DO" in site_info_list[0]:
            do = site_info_list[0].attr("*DO")
            if do == None or do.upper() != "YES":
                msg = "Skip NE=%s because DO != YES" % ne_name
                self.exit_Info(msg)
        if "*BTS Name" in site_info_list[0] and site_info_list[0].attr("*BTS Name") not in [None, ""] and "G" not in self.ratStr:
            self.ratStr += "G"
        if "*NodeB Name"in site_info_list[0] and site_info_list[0].attr("*NodeB Name") not in [None, ""] and "U" not in self.ratStr:
            self.ratStr += "U"
        if "*eNodeB Name"in site_info_list[0] and site_info_list[0].attr("*eNodeB Name") not in [None, ""] and "L" not in self.ratStr:
            self.ratStr += "L"
        if "*gNodeB Name"in site_info_list[0] and site_info_list[0].attr("*gNodeB Name") not in [None, ""] and "N" not in self.ratStr:
            self.ratStr += "N"
        return site_info_list[0]

    @API_RECORD
    def get_CellInfoList(self, cell_info_excel_name, cell_info_sheet_name, site_name_title, ne_name=None, title_row=2,  **kwargs):
        cell_info_list = self.get_data_from_excel(excel_name=cell_info_excel_name, sheet_name=cell_info_sheet_name, group_title=site_name_title, title_row=title_row, ne_name=ne_name, **kwargs)
        if len(cell_info_list) == 0:
            msg = "Error: NE=%s No Cell info in file %s sheet %s" % (ne_name, cell_info_excel_name, cell_info_sheet_name)
            self.exit_Info(msg)
        return cell_info_list

    @API_RECORD
    def get_IPInfo(self, ip_info_excel_name, ip_info_sheet_name="IP Data", site_name_title="*NE Name", ne_name=None, title_row=2, **kwargs):
        ip_info_list = self.get_data_from_excel(excel_name=ip_info_excel_name, sheet_name=ip_info_sheet_name, group_title=site_name_title, title_row=title_row, ne_name=ne_name, **kwargs)
        if len(ip_info_list) != 1:
            msg = "Error: NE=%s No or More than one IP info in file %s sheet %s" % (ne_name, ip_info_excel_name, ip_info_sheet_name)
            self.exit_Info(msg)
        return ip_info_list[0]

    @API_RECORD
    def get_MME_SGW_pool(self, pool_name, pool_excel_file_name, pool_sheet_name, pool_title, title_row=2):
        if pool_name in [None, ""]:
            self.warning_Info("POOL Name is empty, return empty list")
            return []
        pool_dict = load_Excel_File(excel_name=pool_excel_file_name, sheet_name=pool_sheet_name,
                                    title_row=title_row, group_title=pool_title)
        if pool_name not in pool_dict:
            msg = "Error: Not found Pool Name=%s in file=%s, sheet=%s" % (pool_name, pool_excel_file_name, pool_sheet_name)
            self.exit_Info(msg)
        return pool_dict[pool_name]
    load_MME_SGW_pool=get_MME_SGW_pool

    @API_RECORD
    def convert_product_type(self, ne_tree, product_type):
        NE_SITETYPE_CONVERT(ne_tree, product_type)

    @API_RECORD
    def get_SectorEqm_Info(self):
        # Create a dict for sectoreqmid and TX/RX antenna port
        sectoreqm_txrxnum_map = {}
        sectoreqm_obj_list = self.get_moc("SECTOREQM")
        for sectoreqm_obj in sectoreqm_obj_list:
            tx_num = 0
            rx_num = 0
            tx_port_list = []
            if sectoreqm_obj.ANTCFGMODE in ["ANTENNAPORT", MODEL.SECTOREQM.ANTCFGMODE.ANTENNAPORT]:
                for ant_obj in sectoreqm_obj.SECTOREQMANTENNA:
                    if ant_obj.ANTTYPE in ["RXTX_MODE", MODEL.SECTOREQM.SECTOREQMANTENNA.ANTTYPE.RXTX_MODE]:
                        tx_num += 1
                        rx_num += 1
                        tx_port_list.append(ant_obj.ANTN)
                    elif ant_obj.ANTTYPE in ["RX_MODE", MODEL.SECTOREQM.SECTOREQMANTENNA.ANTTYPE.RX_MODE]:
                        rx_num += 1
                    else:
                        tx_num += 1
                        tx_port_list.append(ant_obj.ANTN)
            sectoreqmid = sectoreqm_obj.SECTOREQMID
            sectoreqm_txrxnum_map[sectoreqmid] = (tx_num, rx_num, tx_port_list)
        return sectoreqm_txrxnum_map

    @API_RECORD
    def get_Bom(self, moc, cn, srn, sn):
        bom = None
        mocname = MODEL.EQMTOINVENTORYUNITHW.MOCNAME.fromString(moc)
        obj_list = self.get_moc("EQMTOINVENTORYUNITHW", WHERE(MOCNAME=mocname, CN=cn, SRN=srn, SN=sn))
        if len(obj_list) > 0:
            serial_no = obj_list[0].INVENTORYUNITHWID
            inv_obj = self.get_moc("INVENTORYUNITHW", WHERE(INVENTORYUNITHWID=serial_no))[0]
            bom = inv_obj.ProductNumber
        return bom

    # 对配置数据进行检查和纠错
    @API_RECORD
    def check_and_correct_Data(self):
        # Check if RFU has subrack. If not, Create RFU subrack
        existing_rfu_cn_srn_list = self.get_para_list_from_moc("SUBRACK", ["CN", "SRN"], WHERE(TYPE=MODEL.SUBRACK.TYPE.RFU))
        rfu_cn_srn_list = self.get_para_list_from_moc("RFU", ["CN", "SRN"])
        if len(rfu_cn_srn_list) > 0:
            for (cn, srn) in rfu_cn_srn_list:
                if [cn, srn] not in existing_rfu_cn_srn_list:
                    obj = MODEL.SUBRACK(CN=cn, SRN=srn, TYPE=MODEL.SUBRACK.TYPE.RFU)
                    self.save_moc("SUBRACK", [obj], APPEND_MODE, with_merge=True)
                    existing_rfu_cn_srn_list.append([cn, srn])

        # Delete RFU Subrack if no RFU in this cabinet
        # exixting_mpt_list = self.get_moc("MPT")
        # exixting_bbp_list = self.get_moc("BBP")
        subrack_obj_list = self.get_moc_list_by_del("SUBRACK", WHERE(lambda o: [o.CN, o.SRN] not in rfu_cn_srn_list
                                                                               and o.TYPE == MODEL.SUBRACK.TYPE.RFU))
        self.save_moc("SUBRACK", subrack_obj_list, OVERWRITE_MODE)
        # self.save_moc("BBP", exixting_bbp_list, OVERWRITE_MODE)
        # self.save_moc("MPT", exixting_mpt_list,OVERWRITE_MODE)

        # Delete DLFLOWCTRLPARA (SBT=E1_COVERBOARD)
        dlflowctrlpara_obj_list= self.get_moc_list_by_del("DLFLOWCTRLPARA", WHERE(SBT=MODEL.DLFLOWCTRLPARA.SBT.E1_COVERBOARD))
        self.save_moc("DLFLOWCTRLPARA", dlflowctrlpara_obj_list, OVERWRITE_MODE)

        # Check and modify SNDMD, RCVMD parameter for GTRXGROUP to match SectorEqm TX/RX port num
        sectoreqm_txrxnum_map = self.get_SectorEqm_Info()
        gtrxgroup_obj_list = self.get_moc("GTRXGROUP")
        for obj in gtrxgroup_obj_list:
            gtrxgroupid = obj.GTRXGROUPID
            sectoreqmid_list = self.get_para_list_from_moc("GTRXGROUPSECTOREQM", "SECTOREQMID", WHERE(GTRXGROUPID=gtrxgroupid))
            if len(sectoreqmid_list) > 0:
                sectoreqmid = sectoreqmid_list[0]
                if sectoreqmid not in sectoreqm_txrxnum_map:
                    self.print_msg( "Info: GTRXGROUPID=%r has no SECTOREQM config. Delete it" % gtrxgroupid)
                    obj_list = self.get_moc_list_by_del("GTRXGROUP", WHERE(GTRXGROUPID=gtrxgroupid))
                    self.save_moc("GTRXGROUP", obj_list, OVERWRITE_MODE)
                    obj_list = self.get_moc_list_by_del("GTRXGROUPSECTOREQM", WHERE(GTRXGROUPID=gtrxgroupid))
                    self.save_moc("GTRXGROUPSECTOREQM", obj_list, OVERWRITE_MODE)
                else:
                    tx_num, rx_num, tx_port_list = sectoreqm_txrxnum_map[sectoreqmid]
                    send_mode = "SINGLESND" if tx_num<2 else "DIVERSITY"
                    if rx_num == 1:
                        recv_mode = "SINGLERECV"
                    elif rx_num == 4:
                        recv_mode = "FOURDIVERSITY"
                    else:
                        recv_mode = "MAINDIVERSITY"

                    obj_list = self.get_moc_list_by_mod("GTRXGROUP", MOD(SNDMD=send_mode, RCVMD=recv_mode).WHERE(GTRXGROUPID=gtrxgroupid))
                    self.save_moc("GTRXGROUP", obj_list, OVERWRITE_MODE)
            else:
                self.print_msg( "Info: GTRXGROUPID=%r has no GTRXGROUPSECTOREQM config. Delete it" % gtrxgroupid)
                obj_list = self.get_moc_list_by_del("GTRXGROUP", WHERE(GTRXGROUPID=gtrxgroupid))
                self.save_moc("GTRXGROUP", obj_list, OVERWRITE_MODE)
            pass

        #检查是否存在UPEU单板，如果存在，则删除对应槽位的UEIU单板
        cn_srn_sn_list = self.get_para_list_from_moc("PEU", ["CN", "SRN", "SN"])
        ueiu_obj_list = self.get_moc_list_by_del("UEIU", WHERE(lambda o: [o.CN, o.SRN, o.SN] in cn_srn_sn_list))
        self.save_moc("UEIU", ueiu_obj_list, OVERWRITE_MODE)

        # 检查BRI单板所在槽位是否存在BBP单板，如果存在，则删除BRI单板
        bbp_sn_list = self.get_para_list_from_moc("BBP", ["CN", "SRN", "SN"])
        bri_sn_list = self.get_para_list_from_moc("BRI", ["CN", "SRN", "SN"])
        for (cn, srn, sn) in bri_sn_list:
            if [cn, srn, sn] in bbp_sn_list:
                bri_obj_list = self.get_moc_list_by_del("BRI", WHERE(CN=cn, SRN=srn, SN=sn))
                self.save_moc("BRI", bri_obj_list, OVERWRITE_MODE)
            pass

        # 解决TCU/FMU/PMU/EMU的管理端口号冲突的问题
        moc_address_list = [
            ("TCU", ["0-0-0-7", "0-0-0-23", "0-0-1-7", "0-0-1-23"]),
            ("FMU", ["0-0-0-14", "0-0-0-15", "0-0-1-14", "0-0-1-15"]),
            ("PMU", ["0-0-0-3", "0-0-1-3"]),
            ("EMU", ["0-0-0-2", "0-0-1-2"]) ]
        for (moc, monitor_port_list) in moc_address_list:
            obj_list = self.get_moc(moc)
            for obj in obj_list:
                port_str = "%d-%d-%d-%d" % (obj.MCN, obj.MSRN, obj.MPN, obj.ADDR)
                if port_str not in monitor_port_list:
                    port_str = monitor_port_list[0]
                    tmp_list = [int(s) for s in port_str.split("-")]
                    obj.MCN, obj.MSRN, obj.MPN, obj.ADDR = tmp_list
                monitor_port_list.remove(port_str)
            self.save_moc(moc, obj_list, OVERWRITE_MODE)
        pass

    # 通过正则表达式，小区名称通配符，来计算小区所在的扇区id，扇区id从0开始
    @API_RECORD
    def calculate_SectorNo_For_Cell(self, rat_name, cellname, sector_format_map, band_cell_qty=0):
        sector_no = None
        for i in range(12):
            sector_str = "SECTOR_%s" % chr(ord("A") + i)
            if sector_str not in sector_format_map: continue
            if len(sector_format_map[sector_str]) == 0: continue

            fmt = sector_format_map[sector_str][0]
            if len(fmt) == 0: continue
            p = re.compile(fmt)
            match = p.match(cellname)
            if match:
                sector_no = sector_str[-1]
                break
        if sector_no is None:
            if band_cell_qty == 1:
                sector_no = "A"
            else:
                self.print_msg("Error: cellname=%s cannot match any %s CELLNAME_FORMAT. Cannot calculate SectorNo." % (
                cellname, rat_name))
        return sector_no

    ###############################################################################################
    @API_RECORD
    def common_data_from_template(self, moc_names, **kwargs):
        if not isinstance(moc_names, list):
            moc_names = [moc_names]
        TemplateName = kwargs["TemplateName"]
        for moc_name in moc_names:
            data_from_template = self.get_data_from_template(TemplateName, moc_name, **kwargs)[0]
            for field_name in data_from_template.get_field_names():
                if field_name not in kwargs:
                    kwargs[field_name] = data_from_template.get(field_name)
        return kwargs

    # Create Node by use Site Template
    # 引用基站模板，创建NODE对象
    @API_RECORD
    def create_NODE(self,  product_type, ne_name=None, node_template_name=None, exclude_moc_list=None, template_only=False):
        """
        product_type: DBS3900, DBS3900_LTE, DBS5900_5G, etc
        exclude_moc_list: unnecessary moc list, such as ["UEIU", "RFU", "RRU", "RRUCHAIN", "SECTOREQM", "SECTOR", "BBP", BASEBANDEQM", "BRI"]
        """
        fix_exclude_moc_list = ["SUBRACK", "RFU", "RRU", "RRUCHAIN", "SECTOREQM", "SECTOR", "BBP", "BASEBANDEQM", "BRI",
                                "UEIU","GBTSFUNCTION", "NODEBFUNCTION", "eNodeBFunction", "gNodeBFunction", "RET",
                                "RETSUBUNIT","TMASUBUNIT", "TMA", "NTPCP","RSCGRP", "ETHPORT"]

        if ne_name is None:
            ne_name = self.NEName
        if not node_template_name:
            if "5900" in product_type:
                node_template_name = "DBS5900_5G_BBU5900_VIRTUAL_NR_3SEC_SIMPTRANSMODE"
            else:
                node_template_name = "BTS3900_SRAN_BBU3910_BTS3900_FEGE_GUL_G_3SEC_U_3SEC_L_3SEC"
        if exclude_moc_list is None:
            exclude_moc_list = fix_exclude_moc_list
        else:
            exclude_moc_list.extend(fix_exclude_moc_list)
        if template_only is True:
            exclude_moc_list = None
        # To Delete RAT info because some NODE template include RAT info
        exclude_moc_list.extend(["GBTSFUNCTION", "NODEBFUNCTION", "eNodeBFunction", "gNodeBFunction"])
        # Load Template and Commit all MOC
        node_doc = self.get_doc_from_template(node_template_name)
        self.save_all_mocs(node_doc, APPEND_MODE, with_merge=True, exclude_mocs=exclude_moc_list)
        # Correct invalid value in XML Template
        if hasattr(MODEL.SECTOREQM, "ANTCFGMODE"):
            self.mod_moc("SECTOREQM", MOD(BEAMAZIMUTHOFFSET=None, BEAMLAYERSPLIT=None, BEAMSHAPE=None).WHERE(
                         ANTCFGMODE=MODEL.SECTOREQM.ANTCFGMODE.ANTENNAPORT))

        # Decide if the product is ConCurrent or not
        wm = MODEL.NODE.WM.fromString("CONCURRENT")
        if "WCDMA" in product_type or "LTE" in product_type or "5G" in product_type:
            wm = MODEL.NODE.WM.fromString("NON-CONCURRENT")
        # Create and Commit NODE
        self.set_moc("NODE",NODENAME=ne_name, PRODUCTTYPE=product_type, NODEID=1, WM=wm)
        self.mod_moc("EQUIPMENT",MOD(EQUIPMENTTY=product_type))
        # Create and Commit NE
        self.set_moc("NE", NENAME=ne_name)
        pass

    # Example
    # template_name = "DBS3900_SRAN_VIRTUAL_FEGE_GULT_G_3SEC_U_3SEC_L_3SEC_T_3SEC"
    # ne_name = "test"
    # API_Create_NODE(template_name, ne_name, "DBS3900")
    ####################################################################################################
    # Create GSM Radio by template
    # 创建GSM Radio对象
    @API_RECORD
    def create_GSM_Radio(self,  egbts_name, gsm_radio_template_name=None, app_ref=1):
        if not gsm_radio_template_name:
            gsm_radio_template_name = "GBTS_Radio"
        radio_template = self.get_data_from_template(gsm_radio_template_name, "GBTSFUNCTION", with_child=True)[0]
        gbts_function_obj = MODEL.GBTSFUNCTION(GBTSFUNCTIONNAME=egbts_name, APPLICATIONREF=app_ref)
        gbts_function_obj_list = self.save_data_with_template([gbts_function_obj], radio_template)
        self.save_moc("GBTSFUNCTION", gbts_function_obj_list, OVERWRITE_MODE, with_child=True)
        pass

    @API_RECORD
    def create_GSM_Radio_Ex(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["GBTSFUNCTIONNAME"])
        if "TemplateName" not in kwargs or kwargs["TemplateName"] in [None, ""]:
            kwargs["TemplateName"] = "GBTS_Radio"
        radio_template = self.get_data_from_template(kwargs["TemplateName"], "GBTSFUNCTION", with_child=True)[0]
        for field_name in radio_template.get_field_names():
            if field_name not in kwargs:
                kwargs[field_name] = radio_template.get(field_name)
        if "APPLICATIONREF" not in kwargs:
            kwargs["APPLICATIONREF"] = 1

        gbts_function_obj = MODEL.GBTSFUNCTION(**kwargs)
        gbts_function_obj_list = self.save_data_with_template([gbts_function_obj], radio_template)
        self.save_moc("GBTSFUNCTION", gbts_function_obj_list, OVERWRITE_MODE, with_child=True)
        return error_count

    # example
    # gsm_radio_template_name = "GBTS_Radio"
    # API_Create_GSM_Radio(gsm_radio_template_name, "GBTS_Site1")

    ####################################################################################################
    # Create GSM Locell by template
    # 创建GSM本地小区对象
    @API_RECORD
    def create_GSM_Local_Cell(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["TemplateName", "GLOCELLID"])
        if "TemplateName" not in kwargs or kwargs["TemplateName"] in [None, ""]:
            kwargs["TemplateName"] = "GBTS_Cell"
        glocell_template = self.get_data_from_template(kwargs["TemplateName"], "GLOCELL", with_child=True)[0]
        for field_name in glocell_template.get_field_names():
            if field_name not in kwargs:
                kwargs[field_name] = glocell_template.get(field_name)
        glocell_obj = MODEL.GLOCELL(**kwargs)
        glocell_obj_list = self.save_data_with_template([glocell_obj], glocell_template)
        self.save_moc('GLOCELL', glocell_obj_list, APPEND_MODE, with_child=True, with_merge=True)  # APPEND
        pass

    @API_RECORD
    def create_GSM_Local_Cell_Ex(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["TemplateName", "GLOCELLID", "GTRXGROUPID", "SECTOREQMID"])
        if "TemplateName" not in kwargs or kwargs["TemplateName"] in [None, ""]:
            kwargs["TemplateName"] = "GBTS_Cell"
        glocell_template = self.get_data_from_template(kwargs["TemplateName"], "GLOCELL", with_child=True)[0]
        glocell_obj = MODEL.GLOCELL(**kwargs)
        glocell_obj_list = self.save_data_with_template([glocell_obj], glocell_template)
        self.save_moc('GLOCELL', glocell_obj_list, APPEND_MODE, with_child=True, with_merge=True)  # APPEND
        # Create GTRXGROUP
        gtrxgroupid_list = str(kwargs["GTRXGROUPID"]).split(",")
        sectoreqmid_list = str(kwargs["SECTOREQMID"]).split(",")
        for gtrxgroupid in gtrxgroupid_list:
            sectoreqmid_str = sectoreqmid_list[gtrxgroupid_list.index(gtrxgroupid)]
            sectoreqmid_str_list = sectoreqmid_str.split(";")
            self.add_moc("GTRXGROUP", GTRXGROUPID=gtrxgroupid, GLOCELLID=kwargs["GLOCELLID"])
            for sectoreqmid in sectoreqmid_str_list:
                self.add_moc("GTRXGROUPSECTOREQM", GTRXGROUPID=gtrxgroupid, SECTOREQMID=sectoreqmid)

        return error_count

    # example
    # glocell_template_name = "GBTS_Cell"
    # for glocellid in [1,2,3]:
    #     API_Create_GSM_Local_Cell(glocell_template_name, glocellid)

    ####################################################################################################
    # Create UMTS Radio by template
    @API_RECORD
    def create_UMTS_Radio(self, nodeb_name, umts_radio_template_name=None, nodeb_id=0, app_ref=2):
        if not umts_radio_template_name:
            umts_radio_template_name = "NodeB_Radio"
        radio_template = self.get_data_from_template(umts_radio_template_name, "NODEBFUNCTION", with_child=True)[0]
        nodeb_function_obj = MODEL.NODEBFUNCTION(NODEBFUNCTIONNAME=nodeb_name, NODEBID=nodeb_id, APPLICATIONREF=app_ref)
        nodeb_function_list = self.save_data_with_template([nodeb_function_obj], radio_template)
        self.save_moc('NODEBFUNCTION', nodeb_function_list, OVERWRITE_MODE, with_child=True)  # APPEND/OVERWRITE
        pass

    @API_RECORD
    def create_UMTS_Radio_Ex(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["NODEBFUNCTIONNAME"])
        if "TemplateName" not in kwargs or kwargs["TemplateName"] in [None, ""]:
            kwargs["TemplateName"] = "NodeB_Radio"
        radio_template = self.get_data_from_template(kwargs["TemplateName"], "NODEBFUNCTION", with_child=True)[0]
        for field_name in radio_template.get_field_names():
            if field_name not in kwargs:
                kwargs[field_name] = radio_template.get(field_name)
        if "NODEBID" not in kwargs:
            kwargs["NODEBID"] = 0
        if "APPLICATIONREF" not in kwargs:
            kwargs["APPLICATIONREF"] = 2

        nodeb_function_obj = MODEL.NODEBFUNCTION(**kwargs)
        nodeb_function_list = self.save_data_with_template([nodeb_function_obj], radio_template)
        self.save_moc('NODEBFUNCTION', nodeb_function_list, OVERWRITE_MODE, with_child=True)  # APPEND/OVERWRITE
        return error_count
    # example
    # umts_radio_template_name = "NodeB_Radio"
    # API_Create_UMTS_Radio(umts_radio_template_name, "NodeB_Site1")

    ####################################################################################################

    # Create UMTS local cell by template
    @API_RECORD
    def create_UMTS_Local_Cell(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["ULOCELLID", "DLFREQ", "MAXPWR"])
        if "TemplateName" not in kwargs or kwargs["TemplateName"] in [None, ""]:
            kwargs["TemplateName"] = "NodeB_Cell_Transmitter Non-diversity_Default"
        ulocell_template = self.get_data_from_template(kwargs["TemplateName"], "ULOCELL", with_child=True)[0]
        for field_name in ulocell_template.get_field_names():
            if field_name not in kwargs:
                kwargs[field_name] = ulocell_template.get(field_name)
        ulocell_obj = MODEL.ULOCELL(**kwargs)
        ulocell_obj_list = self.save_data_with_template([ulocell_obj], ulocell_template)
        self.save_moc('ULOCELL', ulocell_obj_list, APPEND_MODE, with_child=True, with_merge=True)  # APPEND/OVERWRITE
        # Create ULOCELLSECTOREQM
        if "SECTOREQMID" in kwargs:
            kwargs["MAXPWR"] = 65535
            ulocellsectoreqm_obj = MODEL.ULOCELLSECTOREQM(**kwargs)
            self.save_moc('ULOCELLSECTOREQM', [ulocellsectoreqm_obj], APPEND_MODE, with_child=True, with_merge=True)
        return error_count

    # example
    # ulocell_radio_template_name = "NodeB_Cell_Transmitter Non-diversity_Default"
    # API_Create_UMTS_Local_Cell(TemplateName=ulocell_template_name, ULOCELLID=ulocellid,
    #                            ULFREQ=ulfreq, DLFREQ=dlfreq, MAXPWR=max_pwr, DL64QAM=dl64qam, RADIUS=radius)

    ####################################################################################################
    # Create LTE Radio by template
    @API_RECORD
    def create_LTE_Radio_Ex(self, **kwargs):
        error_count = self.inner_check_para(kwargs,
                                       ["eNodeBName", "eNodeBId", "CnOperatorName", "Mcc", "Mnc"])
        if "TemplateName" not in kwargs or kwargs["TemplateName"] in [None, ""]:
            kwargs["TemplateName"] = "LTE_Radio"
        radio_template = self.get_data_from_template(kwargs["TemplateName"], "eNodeBFunction", with_child=True)[0]
        function_obj = MODEL.eNodeBFunction(eNodeBFunctionName=kwargs["eNodeBName"], eNodeBId=kwargs["eNodeBId"])
        enodeb_function_obj = self.save_data_with_template([function_obj], radio_template)[0]
        enodeb_function_obj.CnOperator[0].CnOperatorName = kwargs["CnOperatorName"]
        enodeb_function_obj.CnOperator[0].CnOperatorType = 'CNOPERATOR_PRIMARY'
        enodeb_function_obj.CnOperator[0].Mcc = kwargs["Mcc"]
        enodeb_function_obj.CnOperator[0].Mnc = kwargs["Mnc"]
        enodeb_function_obj.ApplicationRef = None
        if "APPLICATIONREF" not in kwargs:
            kwargs["APPLICATIONREF"] = 3
        if len(enodeb_function_obj["CnOperator"]) > 1:
            for x in range(1,len(enodeb_function_obj["CnOperator"])):
                del enodeb_function_obj["CnOperator"][x]  # Not create CnOperator
        del enodeb_function_obj["CnOperatorTa"]  # Not create CnOperatorTa
        self.save_moc('eNodeBFunction', [enodeb_function_obj], OVERWRITE_MODE, with_child=True)
        return error_count

    @API_RECORD
    def create_LTE_Radio(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["eNodeBFunctionName", "eNodeBId"])
        if "TemplateName" not in kwargs or kwargs["TemplateName"] in [None, ""]:
            kwargs["TemplateName"] = "LTE_Radio"
        radio_template = self.get_data_from_template(kwargs["TemplateName"], "eNodeBFunction", with_child=True)[0]
        for field_name in radio_template.get_field_names():
            if field_name not in kwargs:
                kwargs[field_name] = radio_template.get(field_name)
        function_obj = MODEL.eNodeBFunction(**kwargs)
        enodeb_function_obj = self.save_data_with_template([function_obj], radio_template)[0]
        if "ApplicationRef" not in kwargs:
            kwargs["ApplicationRef"] = 3
        enodeb_function_obj.ApplicationRef = kwargs["ApplicationRef"]
        self.save_moc('eNodeBFunction', [enodeb_function_obj], OVERWRITE_MODE, with_child=True)
        return error_count

    @API_RECORD
    def create_LTE_FDD_Cell(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["RootSequenceIdx", "DlBandWidth", "UlBandWidth"])
        kwargs["FddTddInd"] = MODEL.Cell.FddTddInd.CELL_FDD
        if "TemplateName" not in kwargs or kwargs["TemplateName"] in [None, ""]:
            kwargs["TemplateName"] = "LTE_Cell_FDD_20M_2T2R"
        error_count += self.inner_create_lte_cell(**kwargs)
        return error_count

    @API_RECORD
    def create_LTE_TDD_Cell(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["RootSequenceIdx", "DlBandWidth", "UlBandWidth", "SubframeAssignment",
                                                "SpecialSubframePatterns"])
        kwargs["FddTddInd"] = MODEL.Cell.FddTddInd.CELL_TDD
        if "TemplateName" not in kwargs or kwargs["TemplateName"] in [None, ""]:
            kwargs["TemplateName"] = "LTE_CELL_TDD_20M_SA1_S1_2T2R"
        error_count += self.inner_create_lte_cell(**kwargs)
        return error_count

    @API_RECORD
    def create_LTE_Cell(self, **kwargs):
        error_count = 0
        cell_template = self.get_data_from_template(kwargs["TemplateName"], "Cell", with_child=True)[0]
        kwargs["cell_template"] = cell_template
        if cell_template["FddTddInd"] == MODEL.Cell.FddTddInd.CELL_TDD or cell_template["FddTddInd"] == "CELL_TDD":
            error_count += self.create_LTE_TDD_Cell(**kwargs)
        else:
            error_count += self.create_LTE_FDD_Cell(**kwargs)
        return error_count

    @API_RECORD
    def create_Prb_Cell(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["LocalCellId","PrbId"])
        if "TemplateName" not in kwargs or kwargs["TemplateName"] in [None, ""]:
            kwargs["TemplateName"] = "LTE_CELL_TDD_20M_SA1_S1_2T2R"
        prb_template = self.get_data_from_template(kwargs["TemplateName"], "Prb", with_child=True, **kwargs)[0]
        for field_name in prb_template.get_field_names():
            if field_name not in kwargs:
                kwargs[field_name] = prb_template.get(field_name)
        prb_obj = MODEL.Prb(**kwargs)
        nb_prb_obj = self.save_data_with_template([prb_obj], prb_template)
        self.save_moc("Prb", nb_prb_obj, APPEND_MODE, with_child=True, with_merge=True)
        return error_count

    @API_RECORD
    def create_NB_Cell(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["PrbId"])
        if "NbCellFlag" not in kwargs:
            kwargs["NbCellFlag"] = MODEL.Cell.NbCellFlag.TRUE
        if "NbIotTaFlag" not in kwargs:
            kwargs["NbIotTaFlag"] = MODEL.CnOperatorTa.NbIotTaFlag.BOOLEAN_TRUE
        if "CoverageLevelType" not in kwargs:
            kwargs["CoverageLevelType"] = 7
        if "FddTddInd" not in kwargs:
            kwargs["FddTddInd"] = MODEL.Cell.FddTddInd.CELL_FDD
        # kwargs["PrbIdList"] = [MODEL.eUCellSectorEqm.PrbIdList(PrbId=kwargs["PrbId"])]

        # Create NB Cell
        error_count += self.inner_create_lte_cell(**kwargs)
        # Create Prb
        prb_obj = MODEL.Prb(**kwargs)
        self.save_moc('Prb', [prb_obj], APPEND_MODE, with_child=True, with_merge=True)
        # Create CellRachCECfg
        obj_list = []
        for level in ["COVERAGE_LEVEL_0", "COVERAGE_LEVEL_1", "COVERAGE_LEVEL_2"]:
            kwargs["CoverageLevel"] = MODEL.CellRachCECfg.CoverageLevel.field(level)
            obj = MODEL.CellRachCECfg(**kwargs)
            obj_list.append(obj)
        self.save_moc('CellRachCECfg', obj_list, APPEND_MODE, with_child=True, with_merge=True)
        return error_count

    @API_RECORD
    def create_5G_Radio(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["gNodeBFunctionName", "gNBId"])
        if "TemplateName" not in kwargs:
            kwargs["TemplateName"] = "NR_RADIO"
        radio_template = self.get_data_from_template(kwargs["TemplateName"], "gNodeBFunction", with_child=True)[0]
        for field_name in radio_template.get_field_names():
            if field_name not in kwargs:
                kwargs[field_name] = radio_template.get(field_name)
        if "gNBIdLength" not in kwargs:
            kwargs['gNBIdLength'] = 22
        kwargs["gNBId"] = int(kwargs["gNBId"])

        gnodeb_function_obj = MODEL.gNodeBFunction(**kwargs)
        gnodeb_function_obj = self.save_data_with_template([gnodeb_function_obj], radio_template)[0]
        self.save_moc('gNodeBFunction', [gnodeb_function_obj], OVERWRITE_MODE, with_child=True)
        return error_count

    @API_RECORD
    def create_5G_Radio_Ex(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["gNodeBFunctionName", "gNBId", "OperatorName", "Mcc", "Mnc"])
        if "TemplateName" not in kwargs:
            kwargs["TemplateName"] = "NR_RADIO"
        if "gNBIdLength" not in kwargs:
            kwargs['gNBIdLength'] = 22
        kwargs['"gNBId"'] = int(kwargs['gNBId'])
        radio_template = self.get_data_from_template(kwargs["TemplateName"], "gNodeBFunction", with_child=True)[0]
        gnodeb_function_obj = MODEL.gNodeBFunction(**kwargs)
        gnodeb_function_obj = self.save_data_with_template([gnodeb_function_obj], radio_template)[0]
        gnodeb_function_obj.gNBOperator[0].OperatorName = kwargs["OperatorName"]
        gnodeb_function_obj.gNBOperator[0].Mcc = kwargs["Mcc"]
        gnodeb_function_obj.gNBOperator[0].Mnc = kwargs["Mnc"]
        if "NrNetworkingOption" in kwargs:
            gnodeb_function_obj.gNBOperator[0].NrNetworkingOption = kwargs["NrNetworkingOption"]
        gnodeb_function_obj.ReferencedApplicationId = None
        if "APPLICATIONREF" not in kwargs:
            kwargs["APPLICATIONREF"] = 4
        self.save_moc('gNodeBFunction', [gnodeb_function_obj], OVERWRITE_MODE, with_child=True)
        return error_count

    @API_RECORD
    def create_5G_NrCell(self, **kwargs):
        error_count = self.inner_check_para(kwargs,
                                            ["NrCellId", "CellName", "Tac", "CellId", "FrequencyBand","TrackingAreaId"])

        if "TemplateName" not in kwargs or kwargs["TemplateName"] is None:
            kwargs["TemplateName"] = "NR_CELL_SUB6G_TDD_100M_64T64R"
        cell_template = self.get_data_from_template(kwargs["TemplateName"], "NRCell", with_child=True)[0]
        for field_name in cell_template.get_field_names():
            if field_name not in kwargs:
                kwargs[field_name] = cell_template.get(field_name)
        if "DuplexMode" not in kwargs:
            kwargs["DuplexMode"] = "CELL_TDD"
        self.create_gNBTAC(kwargs["Tac"], kwargs["TrackingAreaId"])

        # Create NRCell
        cell_obj = MODEL.NRCell(**kwargs)
        new_cell_obj = self.save_data_with_template([cell_obj], cell_template)[0]
        # new_cell_obj.CellOp[0].TrackingAreaId = tai
        self.save_moc("NRCell", [new_cell_obj], APPEND_MODE, with_child=True, with_merge=True)
        return error_count

    @API_RECORD
    def create_5G_NrDuCell(self,**kwargs):
        error_count = self.inner_check_para(kwargs,
                                            ['NrDuCellId', 'NrDuCellName', 'CellId', 'PhysicalCellId', 'FrequencyBand',
                                             'DlNarfcn', 'UlBandwidth', 'DlBandwidth', 'MaxTransmitPower', 'SectorEqmId'])
        if "TemplateName" not in kwargs or kwargs["TemplateName"] is None:
            kwargs["TemplateName"] = "NR_DUCELL_SUB6G_TDD_100M_64T64R"
        cell_template = self.get_data_from_template(kwargs["TemplateName"], "NRDUCell", with_child=True, with_raw=True)[0]
        for field_name in cell_template.get_field_names():
            if field_name not in kwargs:
                kwargs[field_name] = cell_template.get(field_name)
        if "DuplexMode" not in kwargs:
            kwargs["DuplexMode"] = "CELL_TDD"
        if "UlNarfcnConfigInd" not in kwargs:
            kwargs['UlNarfcnConfigInd'] = "NOT_CONFIG"
        if "SlotAssignment" not in kwargs:
            kwargs['SlotAssignment'] = "4_1_DDDSU"
        if "SlotStructure" not in kwargs:
            kwargs['SlotStructure'] = "SS2"
        if "TxRxMode" not in kwargs:
            kwargs['TxRxMode'] = "64T64R"
        if "PowerConfigMode" not in kwargs:
            kwargs['PowerConfigMode'] = "TRANSMIT_POWER"
        if "TrpType" not in kwargs:
            kwargs['TrpType'] = "DEFAULT"
        if "CpriCompression" not in kwargs:
            kwargs['CpriCompression'] = "3DOT2_COMPRESSION"
        if 'NrDuCellTrpId' not in kwargs:
            kwargs['NrDuCellTrpId'] = kwargs['NrDuCellId']
        if 'NrDuCellCoverageId' not in kwargs:
            kwargs['NrDuCellCoverageId'] = kwargs['NrDuCellTrpId']
        if 'SsbFreqPos' not in kwargs:
            if kwargs['FrequencyBand'] in ["N3", "N28"]:
                kwargs['SsbFreqPos'] = str(int(kwargs['DlNarfcn'])-18) if kwargs['DlBandwidth'].split("_")[-1] in ['15M'] else kwargs['DlNarfcn']
            elif kwargs['FrequencyBand'] in ["N41"]:
                kwargs['SsbFreqPos'] = str(int(kwargs['DlNarfcn'])-36) if kwargs['DlBandwidth'].split("_")[-1] in ['20M', '50M', '70M', '80M', '90M', '100M'] else kwargs['DlNarfcn']
            elif kwargs['FrequencyBand'] in ["N77", "N78", "N79"]:
                kwargs['SsbFreqPos'] = str(int(kwargs['DlNarfcn'])-12) if kwargs['DlBandwidth'].split("_")[-1] in ['20M', '50M', '70M', '80M', '90M', '100M'] else kwargs['DlNarfcn']
            else:
                kwargs['SsbFreqPos'] = kwargs['DlNarfcn']

        if 'SubcarrierSpacing' not in kwargs:
            spacing = self.get_NrDuCell_SubcarrierSpacing(kwargs)
            kwargs['SubcarrierSpacing'] =spacing

        # Create NRDUCell
        cell_obj = MODEL.NRDUCell(**kwargs)
        new_cell_obj = self.save_data_with_template([cell_obj], cell_template)[0]
        self.save_moc("NRDUCell", [new_cell_obj], APPEND_MODE, with_child=True, with_merge=True)
        self.add_moc("NRDUCellTrp",**kwargs)
        if "LampSiteCellFlag" not in kwargs or kwargs['LampSiteCellFlag'] == 0:
            kwargs['MaxTransmitPower'] = 65535
        self.add_moc("NRDUCellCoverage", **kwargs)
        self.add_moc("NRDUCellPrach", **kwargs)
        return error_count

    @API_RECORD
    def get_NrDuCell_SubcarrierSpacing(self, kwargs):
        if kwargs['FrequencyBand'] in ["N3", "N28", "N80", "N82", "N83", "N84"]:
            spacing = "15KHZ"
        elif kwargs['FrequencyBand'] in ["N41", "N77", "N78", "N79"]:
            spacing = "30KHZ"
        elif kwargs['FrequencyBand'] in ["N257", "N258", "N260"]:
            spacing = "120KHZ"
        else:
            spacing = "30KHZ"
        return spacing

    @API_RECORD
    def create_X2_for_LTE(self, **kwargs):
        error_count = self.inner_check_para(kwargs,['SIGIP1V4', 'PN', 'LOCIPV4'])
        if 'IPVERSION' not in kwargs:
            kwargs['IPVERSION'] = 'IPv4'
        if 'SCTPTEMPLATEID' not in kwargs:
            kwargs['SCTPTEMPLATEID'] = 0
        if 'USERLABEL' not in kwargs:
            kwargs['USERLABEL'] = "to_NR_NSA_X2"
        if 'gNBCuX2Id' not in kwargs:
            kwargs['gNBCuX2Id'] = self.get_free_id_list("gNBCUX2",'gNBCuX2Id').pop(0)
        if 'EPGROUPID' not in kwargs:
            kwargs['EPGROUPID'] = self.get_free_id_list("EPGROUP",'EPGROUPID').pop(0)
        if 'SCTPHOSTID' not in kwargs:
            kwargs['SCTPHOSTID'] = self.get_free_id_list("SCTPHOST",'SCTPHOSTID').pop(0)
        if 'UPHOSTID' not in kwargs:
            kwargs['UPHOSTID'] = self.get_free_id_list("USERPLANEHOST",'UPHOSTID').pop(0)
        kwargs['CpEpGroupId'] = kwargs['EPGROUPID']
        kwargs['UpEpGroupId'] = kwargs['EPGROUPID']
        kwargs['SCTPHOSTREFS'] = [MODEL.EPGROUP.SCTPHOSTREFS(SCTPHOSTID=kwargs['SCTPHOSTID'])]
        kwargs['USERPLANEHOSTREFS'] = [MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=kwargs['UPHOSTID'])]
        self.add_moc("EPGROUP",**kwargs)
        self.add_moc("SCTPHOST", **kwargs)
        self.add_moc("USERPLANEHOST", **kwargs)
        self.add_moc("gNBCUX2", **kwargs)
        self.add_moc("GNBX2SONCONFIG", X2SonConfigSwitch=BIT(X2SON_SETUP_SWITCH=1))

        return error_count

    create_X2_for_NSA = create_X2_for_LTE

    @API_RECORD
    def create_S1_for_SGW(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ['LOCIPV4', "PEERIPV4_LIST"])
        if 'UPPEERID_LIST' in kwargs:
            if len(kwargs['UPPEERID_LIST']) < len(kwargs['PEERIPV4_LIST']):
                self.exit_Info("create_S1_for_SGW: len(kwargs['UPPEERID_LIST']) < len(kwargs['PEERIPV4_LIST'])")
        else:
            free_id_list = self.get_free_id_list("USERPLANEPEER", 'UPPEERID')
            kwargs['UPPEERID_LIST'] = [x for x in free_id_list if free_id_list.index(x) < len(kwargs['PEERIPV4_LIST'])]
        if 'IPVERSION' not in kwargs:
            kwargs['IPVERSION'] = 'IPv4'
        if 'USERLABEL' not in kwargs:
            kwargs['USERLABEL'] = "to_NR_NSA_S1"
        if 'gNBCuS1Id' not in kwargs:
            kwargs['gNBCuS1Id'] = self.get_free_id_list("gNBCUS1", 'gNBCuS1Id').pop(0)
        if 'EPGROUPID' not in kwargs:
            kwargs['EPGROUPID'] = self.get_free_id_list("EPGROUP", 'EPGROUPID').pop(0)
        if 'UPHOSTID' not in kwargs:
            kwargs['UPHOSTID'] = self.get_free_id_list("USERPLANEHOST", 'UPHOSTID').pop(0)
        kwargs['UpEpGroupId'] = kwargs['EPGROUPID']#必须EPGroupID
        kwargs['USERPLANEHOSTREFS'] = [MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=kwargs['UPHOSTID'])]
        kwargs['USERPLANEPEERREFS'] = [MODEL.EPGROUP.USERPLANEPEERREFS(UPPEERID=id) for id in kwargs['UPPEERID_LIST']]
        self.add_moc("EPGROUP", **kwargs)
        self.add_moc("USERPLANEHOST", **kwargs)
        self.add_moc("gNBCUS1", **kwargs)
        for (kwargs['PEERIPV4'], kwargs['UPPEERID']) in [(x,y) for x in kwargs['PEERIPV4_LIST'] for y in kwargs['UPPEERID_LIST'] if kwargs['PEERIPV4_LIST'].index(x) == kwargs['UPPEERID_LIST'].index(y)]:
            self.add_moc("USERPLANEPEER", **kwargs)

        return error_count

    #S1自建立
    @API_RECORD
    def create_S1_for_NSA(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ['LOCIPV4'])
        if 'IPVERSION' not in kwargs:
            kwargs['IPVERSION'] = 'IPv4'
        if 'USERLABEL' not in kwargs:
            kwargs['USERLABEL'] = "to_NR_NSA_S1"
        if 'gNBCuS1Id' not in kwargs:
            kwargs['gNBCuS1Id'] = self.get_free_id_list("gNBCUS1", 'gNBCuS1Id').pop(0)
        if 'EPGROUPID' not in kwargs:
            kwargs['EPGROUPID'] = self.get_free_id_list("EPGROUP", 'EPGROUPID').pop(0)
        if 'UPHOSTID' not in kwargs:
            kwargs['UPHOSTID'] = self.get_free_id_list("USERPLANEHOST", 'UPHOSTID').pop(0)
        kwargs['UpEpGroupId'] = kwargs['EPGROUPID']
        kwargs['USERPLANEHOSTREFS'] = [MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=kwargs['UPHOSTID'])]
        self.add_moc("EPGROUP", **kwargs)
        self.add_moc("USERPLANEHOST", **kwargs)
        self.add_moc("gNBCUS1", **kwargs)

        return error_count

    #create S1 and X2 with one IP
    @API_RECORD
    def create_S1_X2_for_NSA(self, **kwargs):
        error_count = self.inner_check_para(kwargs,['SIGIP1V4', 'PN', 'LOCIPV4'])
        if 'IPVERSION' not in kwargs:
            kwargs['IPVERSION'] = 'IPv4'
        if 'SCTPTEMPLATEID' not in kwargs:
            kwargs['SCTPTEMPLATEID'] = 0
        #S1
        if 'gNBCuS1Id' not in kwargs:
            kwargs['gNBCuS1Id'] = self.get_free_id_list("gNBCUS1", 'gNBCuS1Id').pop(0)
        if 'EPGROUPID' not in kwargs:
            kwargs['EPGROUPID'] = self.get_free_id_list("EPGROUP", 'EPGROUPID').pop(0)
        if 'UPHOSTID' not in kwargs:
            kwargs['UPHOSTID'] = self.get_free_id_list("USERPLANEHOST", 'UPHOSTID').pop(0)
        kwargs['UpEpGroupId'] = kwargs['EPGROUPID']
        kwargs['USERPLANEHOSTREFS'] = [MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=kwargs['UPHOSTID'])]
        kwargs['USERLABEL'] = "to_NR_NSA_S1"
        self.add_moc("EPGROUP", **kwargs)
        kwargs['USERLABEL'] = "to_NR_NSA_S1_X2"
        self.add_moc("USERPLANEHOST", **kwargs)
        self.add_moc("gNBCUS1", **kwargs)
        #X2
        if 'gNBCuX2Id' not in kwargs:
            kwargs['gNBCuX2Id'] = self.get_free_id_list("gNBCUX2",'gNBCuX2Id').pop(0)
        if 'SCTPHOSTID' not in kwargs:
            kwargs['SCTPHOSTID'] = self.get_free_id_list("SCTPHOST",'SCTPHOSTID').pop(0)
        kwargs['EPGROUPID'] = self.get_free_id_list("EPGROUP", 'EPGROUPID').pop(0)
        kwargs['USERLABEL'] = "to_NR_NSA_X2"
        kwargs['CpEpGroupId'] = kwargs['EPGROUPID']
        kwargs['UpEpGroupId'] = kwargs['EPGROUPID']
        kwargs['SCTPHOSTREFS'] = [MODEL.EPGROUP.SCTPHOSTREFS(SCTPHOSTID=kwargs['SCTPHOSTID'])]
        self.add_moc("EPGROUP",**kwargs)
        self.add_moc("SCTPHOST", **kwargs)
        self.add_moc("gNBCUX2", **kwargs)
        self.add_moc("GNBX2SONCONFIG", X2SonConfigSwitch=BIT(X2SON_SETUP_SWITCH=1))
        return error_count

    @API_RECORD
    def create_IPSEC(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ['SIP', 'LOCALIP', 'REMOTEIP'])
        if 'ACLDESC' not in kwargs:
            kwargs['ACLDESC'] = 'IPSEC'
        if 'ACLID' not in kwargs:
            kwargs['ACLID'] = 3001
        if 'RULEID' not in kwargs:
            kwargs['RULEID'] = 1
        if 'DWC' not in kwargs:
            kwargs['DWC'] = '255.255.255.255'
        if 'DIP' not in kwargs:
            kwargs['DIP'] = '0.0.0.0'
        if 'SWC' not in kwargs:
            kwargs['SWC'] = '0.0.0.0'
        if 'PT' not in kwargs:
            kwargs['PT'] = 'IP'
        if 'DSCP' not in kwargs:
            kwargs['DSCP'] = 48
        if 'NATKLI' not in kwargs:
            kwargs['NATKLI'] = 20
        if 'IDTYPE' not in kwargs:
            kwargs['IDTYPE'] = 1
        if 'PEERNAME' not in kwargs:
            kwargs['PEERNAME'] = 'SeGW_IKEPEER'
        if 'PROPID' not in kwargs:
            kwargs['PROPID'] = 1
        if 'REDUNDANCYFLAG' not in kwargs:
            if 'REMOTEIP2' not in kwargs:
                kwargs['REDUNDANCYFLAG'] = 0
            else:
                kwargs['REDUNDANCYFLAG'] = 1
                kwargs['IPSECSBWAITTIME'] = 2
                kwargs['IPSECSWITCHBACK'] = 1
        if 'AUTHALG' not in kwargs:
            kwargs['AUTHALG'] = 5
        if 'SPGN' not in kwargs:
            kwargs['SPGN'] = 'IPSECPOLICY_GRP'
        if 'SPSN' not in kwargs:
            kwargs['SPSN'] = 1
        if 'PROPNAME' not in kwargs:
            kwargs['PROPNAME'] = 'IPSEC_PROPOSAL'
        if 'IPSECBINDITFID' not in kwargs:
            kwargs['IPSECBINDITFID'] = 0
        if 'ITFID' not in kwargs:
            kwargs['ITFID'] = 0

        self.add_moc("ACL", **kwargs)
        self.add_moc("ACLRULE", **kwargs)
        self.add_moc("IKECFG", **kwargs)
        self.add_moc("IKEPEER", **kwargs)
        self.add_moc("IPSECPOLICY", **kwargs)
        if 'REMOTEIP2' in kwargs:
            kwargs['REDUNDANCYFLAG'] = 2
            kwargs['PRIORITY'] = 1
            kwargs['REMOTEIP'] = kwargs['REMOTEIP2']
            kwargs['MASTERPEERNAME'] = kwargs['PEERNAME']
            kwargs['PEERNAME'] = 'SeGW_IKEPEER_2'
            self.add_moc("IKEPEER", **kwargs)
            kwargs['SPSN'] = 2
            self.add_moc("IPSECPOLICY", **kwargs)
        self.add_moc("IKEPROPOSAL", **kwargs)
        self.add_moc("IPSECPROPOSAL", **kwargs)
        self.add_moc("IPSECBINDITF", **kwargs)
        return error_count

    @API_RECORD
    def create_CA(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ['LOCALIP', 'URL'])
        if 'CANAME' not in kwargs:
            kwargs['CANAME'] = 'CANAME'
        if 'COUNTRY' not in kwargs:
            kwargs['COUNTRY'] = 'CN'
        if 'ORG' not in kwargs:
            kwargs['ORG'] = 'huawei'
        if 'USERADDINFO' not in kwargs:
            kwargs['USERADDINFO'] = '.huawei.com'
        self.add_moc("CA", **kwargs)
        self.add_moc("CERTREQ", **kwargs)
        return error_count

    @API_RECORD
    def create_OMCH(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ['IP', "PEERIP"])
        if 'FLAG' not in kwargs:
            kwargs['FLAG'] = "MASTER"
        if 'BEAR' not in kwargs:
            kwargs['BEAR'] = "IPV4"
        if 'PEERMASK' not in kwargs:
            kwargs['PEERMASK'] = "255.255.255.0"
        if 'MASK' not in kwargs:
            kwargs['MASK'] = "255.255.255.255"
        self.add_moc("OMCH",**kwargs)
        return error_count

    @API_RECORD
    def create_IP_OldTXMode(self, **kwargs):
        """Create OldTXMode IP (include DEVIP/SRCIPRT/VLANMAP"""
        error_count = self.inner_check_para(kwargs, ["SN", "IP"])
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        if 'PN' not in kwargs:
            kwargs['PN'] = 0
        if 'SBT' not in kwargs:
            kwargs['SBT'] = "BASE_BOARD"
        if "VRFIDX" not in kwargs:
            kwargs["VRFIDX"] = 0
        if int(kwargs['PN']) == 0:
            kwargs['PA'] = "COPPER"
        else:
            kwargs['PA'] = "FIBER"
        if 'SPEED' not in kwargs:
            kwargs['SPEED'] = "AUTO"
        if 'DUPLEX' not in kwargs:
            kwargs['DUPLEX'] = "AUTO"
        if 'PT' not in kwargs:
            kwargs['PT'] = "ETH"
        if 'MASK' not in kwargs:
            kwargs['MASK'] = "255.255.255.0"
        if kwargs['MASK'] == "255.255.255.255":
            kwargs['PT'] = "LOOPINT"
        if 'NEXTHOP' in kwargs:
            if kwargs['SRCRTIDX'] not in kwargs:
                kwargs['SRCRTIDX'] = self.get_free_id_list("SRCIPRT", 'SRCRTIDX').pop(0)
            kwargs['SRCIP'] = kwargs['IP']
            kwargs['RTTYPE'] = "NEXTHOP"
            self.add_moc("SRCIPRT", **kwargs)
            if "VLANID" in kwargs:
                kwargs['NEXTHOPIP'] = kwargs['NEXTHOP']
                if 'VLANMODE' not in kwargs:
                    kwargs['VLANMODE'] = "SINGLEVLAN"
                if 'SETPRIO' not in kwargs:
                    kwargs['SETPRIO'] = "DISABLE"
                self.add_moc("VLANMAP", **kwargs)

        if len(self.get_moc("ETHPORT", WHERE(CN=kwargs['CN'],SRN=kwargs['SRN'],SN=kwargs['SN'],PN=kwargs['PN']))) < 1 and kwargs['PT']=="ETH":
            self.add_moc("ETHPORT", **kwargs)
        self.add_moc("DEVIP", **kwargs)
        return error_count

    @API_RECORD
    def create_GBTSABISCP(self,id_start=0,**kwargs):
        error_count = self.inner_check_para(kwargs, ["SN", "LOCIP", "LOCPORT", "PEERIP", "PEERPORT"])
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        if "SCTPNO" not in kwargs:
            kwargs["SCTPNO"] = self.get_free_id_list("SCTPLNK", "SCTPNO",id_start=id_start).pop(0)
        if "DESCRI" not in kwargs:
            kwargs["DESCRI"] = "To BSC(ABIS)"
        self.add_moc('SCTPLNK', **kwargs)
        kwargs["LINKNO"] = kwargs["SCTPNO"]
        if "CPBEARID" not in kwargs:
            kwargs["CPBEARID"] = kwargs["SCTPNO"]
        if "BEARTYPE" not in kwargs:
            kwargs["BEARTYPE"] = 1
        if "FLAG" not in kwargs:
            kwargs["FLAG"] = 0
        # Create CPBEARER
        self.add_moc('CPBEARER', **kwargs)
        if "ABISCPID" not in kwargs:
            kwargs["ABISCPID"] = kwargs["CPBEARID"]
        # Create GBTSABISCP
        self.add_moc('GBTSABISCP', **kwargs)
        return error_count

    @API_RECORD
    def create_GBTSPATH(self,id_start=0, **kwargs):
        error_count = self.inner_check_para(kwargs, ["SN", "LOCALIP", "PEERIP"])
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        if 'SBT' not in kwargs:
            kwargs['SBT'] = "BASE_BOARD"
        if 'PT' not in kwargs:
            kwargs['PT'] = "ETH"
        if 'PN' not in kwargs:
            kwargs['PN'] = 0
        if "PATHID" not in kwargs:
            kwargs["PATHID"] = self.get_free_id_list("IPPATH", "PATHID",id_start=id_start).pop(0)
        if "DESCRI" not in kwargs:
            kwargs["DESCRI"] = "To BSC"
        if "DSCPLIST" not in kwargs:
            kwargs["PATHTYPE"] = "ANY"
            self.add_moc('IPPATH', **kwargs)
            self.add_moc('GBTSPATH', **kwargs)
        else:
            kwargs["PATHTYPE"] = "FIXED"
            for kwargs["DSCP"] in kwargs["DSCPLIST"]:
                kwargs["PATHID"] = self.get_free_id_list("IPPATH", "PATHID",id_start=id_start).pop(0)
                self.add_moc('IPPATH', **kwargs)
                self.add_moc('GBTSPATH', **kwargs)
        return error_count

    @API_RECORD
    def create_IUBCP_NCP(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["SN", "LOCIP", "LOCPORT", "PEERIP", "PEERPORT"])
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        if "SCTPNO" not in kwargs:
            kwargs["SCTPNO"] = self.get_free_id_list("SCTPLNK", "SCTPNO").pop(0)
        if "DESCRI" not in kwargs:
            kwargs["DESCRI"] = "To RNC(IUB) NCP"
        self.add_moc('SCTPLNK', **kwargs)

        # Create CPBEARER
        kwargs["LINKNO"] = kwargs["SCTPNO"]
        if "CPBEARID" not in kwargs:
            kwargs["CPBEARID"] = kwargs["SCTPNO"]
        if "BEARTYPE" not in kwargs:
            kwargs["BEARTYPE"] = 1
        if "FLAG" not in kwargs:
            kwargs["FLAG"] = 0
        self.add_moc('CPBEARER', **kwargs)

        # Create IUBCP
        if "CPPT" not in kwargs:
            kwargs["CPPT"] = "NCP"
        self.add_moc('IUBCP', **kwargs)
        return error_count

    @API_RECORD
    def create_IUBCP_CCP(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["SN", "LOCIP", "LOCPORT", "PEERIP", "PEERPORT"])
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        if "SCTPNO" not in kwargs:
            kwargs["SCTPNO"] = self.get_free_id_list("SCTPLNK", "SCTPNO").pop(0)
        if "DESCRI" not in kwargs:
            kwargs["DESCRI"] = "To RNC(IUB) CCP"
        self.add_moc('SCTPLNK', **kwargs)

        # Create CPBEARER
        kwargs["LINKNO"] = kwargs["SCTPNO"]
        if "CPBEARID" not in kwargs:
            kwargs["CPBEARID"] = kwargs["SCTPNO"]
        if "BEARTYPE" not in kwargs:
            kwargs["BEARTYPE"] = 1
        if "FLAG" not in kwargs:
            kwargs["FLAG"] = 0
        self.add_moc('CPBEARER', **kwargs)

        # Create IUBCP
        if "CPPT" not in kwargs:
            kwargs["CPPT"] = "CCP"
        self.add_moc('IUBCP', **kwargs)
        return error_count

    @API_RECORD
    def create_IUBCP(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["SN", "LOCIP", "LOCPORT", "PEERIP", "PEERPORT", "CPPT"])
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        if "SCTPNO" not in kwargs:
            kwargs["SCTPNO"] = self.get_free_id_list("SCTPLNK", "SCTPNO").pop(0)
        if "DESCRI" not in kwargs:
            kwargs["DESCRI"] = "To RNC(IUB)"
        self.add_moc('SCTPLNK', **kwargs)

        # Create CPBEARER
        kwargs["LINKNO"] = kwargs["SCTPNO"]
        if "CPBEARID" not in kwargs:
            kwargs["CPBEARID"] = kwargs["SCTPNO"]
        if "BEARTYPE" not in kwargs:
            kwargs["BEARTYPE"] = 1
        if "FLAG" not in kwargs:
            kwargs["FLAG"] = 0
        self.add_moc('CPBEARER', **kwargs)

        # Create IUBCP
        self.add_moc('IUBCP', **kwargs)
        return error_count

    @API_RECORD
    def create_IUB(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["LOCIPV4", "PEERIPV4"])
        if 'UPHOSTID' not in kwargs:
            kwargs['UPHOSTID'] = self.get_free_id_list('USERPLANEHOST', 'UPHOSTID').pop(0)
        if 'VRFIDX' not in kwargs:
            kwargs['VRFIDX'] = 0
        if 'IPVERSION' not in kwargs:
            kwargs['IPVERSION'] = 'IPv4'
        if 'IPSECSWITCH' not in kwargs:
            kwargs['IPSECSWITCH'] = 'DISABLE'
        if 'USERLABEL' not in kwargs:
            kwargs['USERLABEL'] = 'UMTS_U'
        if 'UPPEERID' not in kwargs:
            kwargs['UPPEERID'] = self.get_free_id_list('USERPLANEPEER', 'UPPEERID').pop(0)
        if 'EPGROUPID' not in kwargs:
            kwargs['EPGROUPID'] = self.get_free_id_list('EPGROUP', 'EPGROUPID').pop(0)
        if 'PACKETFILTERSWITCH' not in kwargs:
            kwargs['PACKETFILTERSWITCH'] = 'DISABLE'
        if 'TYPEFLAG' not in kwargs:
            kwargs['TYPEFLAG'] = 'COMMON'
        if 'IUBID' not in kwargs:
            kwargs['IUBID'] = self.get_free_id_list('IUB', 'IUBID').pop(0)
        kwargs['UPEPGROUPID'] = kwargs['EPGROUPID']
        if 'STATICCHKWS' not in kwargs:
            kwargs['STATICCHKWS'] = 'OFF'
        kwargs['USERPLANEHOSTREFS'] = [MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=kwargs['UPHOSTID'])]
        kwargs['USERPLANEPEERREFS'] = [MODEL.EPGROUP.USERPLANEPEERREFS(UPPEERID=kwargs['UPPEERID'])]
        self.add_moc('USERPLANEHOST', **kwargs)
        self.add_moc('USERPLANEPEER', **kwargs)
        self.add_moc('EPGROUP', **kwargs)
        self.add_moc('IUB', **kwargs)
        return error_count

    @API_RECORD
    def create_NODEBPATH(self,with_ippm=False,id_start=0,id_end=100,**kwargs):
        error_count = self.inner_check_para(kwargs, ["SN", "LOCALIP", "PEERIP"])
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        if 'SBT' not in kwargs:
            kwargs['SBT'] = "BASE_BOARD"
        if 'PT' not in kwargs:
            kwargs['PT'] = "ETH"
        if 'PN' not in kwargs:
            kwargs['PN'] = 0
        if "PATHID" not in kwargs:
            kwargs["PATHID"] = self.get_free_id_list("IPPATH", "PATHID",id_start, id_end).pop(0)
        if "DESCRI" not in kwargs:
            kwargs["DESCRI"] = "To BSC"
        if "DSCPLIST" not in kwargs:
            kwargs["PATHTYPE"] = "ANY"
            self.add_moc('IPPATH', **kwargs)
            self.add_moc('NODEBPATH', **kwargs)
        else:
            kwargs["PATHTYPE"] = "FIXED"
            for kwargs["DSCP"] in kwargs["DSCPLIST"]:
                kwargs["PATHID"] = self.get_free_id_list("IPPATH", "PATHID",id_start, id_end).pop(0)
                self.add_moc('IPPATH', **kwargs)
                self.add_moc('NODEBPATH', **kwargs)
                if with_ippm is True:
                    kwargs["IPPMSN"] = kwargs["PATHID"]
                    if "BINDPATH" not in kwargs:
                        kwargs["BINDPATH"] = "YES"
                    if "IPPMTYPE" not in kwargs:
                        kwargs["IPPMTYPE"] = "FOUR_TUPLE"
                    kwargs["IPPMDSCP"] = kwargs["DSCP"]
                    self.add_moc("IPPMSESSION", **kwargs)
        return error_count

    @API_RECORD
    def create_SCTPHOST(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["SIGIP1V4", "PN"])
        if 'SCTPTEMPLATEID' not in kwargs:
            kwargs['SCTPTEMPLATEID'] = 0
        self.add_moc('SCTPTEMPLATE', **kwargs)
        if 'VRFIDX' not in kwargs:
            kwargs['VRFIDX'] = 0
        if 'SIGIP2V4' not in kwargs:
            kwargs['SIGIP2V4'] = "0.0.0.0"
        if 'IPVERSION' not in kwargs:
            kwargs['IPVERSION'] = "IPv4"
        if 'SIMPLEMODESWITCH' not in kwargs:
            kwargs['SIMPLEMODESWITCH'] = "SIMPLE_MODE_OFF"
        if 'USERLABEL' not in kwargs:
            kwargs['USERLABEL'] = "SCTPHOST"
        if 'SCTPHOSTID' not in kwargs:
            kwargs['SCTPHOSTID'] = self.get_free_id_list("SCTPHOST", "SCTPHOSTID").pop(0)
        self.add_moc('SCTPHOST', **kwargs)
        return kwargs['SCTPHOSTID']

    @API_RECORD
    def create_USERPLANEHOST(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["LOCIPV4"])
        if 'VRFIDX' not in kwargs:
            kwargs['VRFIDX'] = 0
        if 'IPVERSION' not in kwargs:
            kwargs['IPVERSION'] = "IPv4"
        if 'USERLABEL' not in kwargs:
            kwargs['USERLABEL'] = "USERPLANEHOST"
        if 'UPHOSTID' not in kwargs:
            kwargs['UPHOSTID'] = self.get_free_id_list("USERPLANEHOST", "UPHOSTID").pop(0)
        self.add_moc('USERPLANEHOST', **kwargs)
        return kwargs['UPHOSTID']

    @API_RECORD
    def create_SCTPPEER(self, mme_pool_list=[], **kwargs):
        if 'VRFIDX' not in kwargs:
            kwargs['VRFIDX'] = 0
        if 'IPVERSION' not in kwargs:
            kwargs['IPVERSION'] = "IPv4"
        # Create SCTPPEER
        if not mme_pool_list:
            error_count = self.inner_check_para(kwargs, ["SIGIP1V4", "PN"])
            if 'SCTPPEERID' not in kwargs:
                kwargs['SCTPPEERID'] = self.get_free_id_list("SCTPPEER", 'SCTPPEERID').pop(0)
            self.add_moc("SCTPPEER", **kwargs)
        dstipList = []
        for mme_info in mme_pool_list:
            kwargs["SIGIP1V4"] = mme_info["SIGIP1V4"]
            kwargs["SIGIP2V4"] = mme_info["SIGIP2V4"]
            kwargs["USERLABEL"] = mme_info["USERLABEL"]
            kwargs["SCTPPEERID"] = mme_pool_list.index(mme_info) if mme_info.attr("SCTPPEERID") in [None, ""] else mme_info["SCTPPEERID"]
            kwargs["PN"] = mme_info["PN"]
            self.add_moc('SCTPPEER', **kwargs)
            dstipList.append({"SCTPPEERID": kwargs["SCTPPEERID"],
                              "IP": kwargs["SIGIP1V4"],
                              "USERLABEL": "To " + kwargs["USERLABEL"]})
            if kwargs["SIGIP2V4"] not in [None, ""]:
                dstipList.append({"SCTPPEERID": kwargs["SCTPPEERID"],
                                  "IP":kwargs["SIGIP2V4"],
                                  "USERLABEL": "To " + kwargs["USERLABEL"]})
        return dstipList

    @API_RECORD
    def create_USERPLANEPEER(self, ugw_pool_list=[], **kwargs):
        if 'VRFIDX' not in kwargs:
            kwargs['VRFIDX'] = 0
        if 'IPVERSION' not in kwargs:
            kwargs['IPVERSION'] = "IPv4"
        # Create USERPLANEPEER
        dstipList = []
        for ugw_info in ugw_pool_list:
            kwargs["PEERIPV4"] = ugw_info["PEERIPV4"]
            kwargs["UPPEERID"] = ugw_pool_list.index(ugw_info) if ugw_info["UPPEERID"] in [None, ""] else ugw_info[
                "UPPEERID"]
            kwargs["USERLABEL"] = ugw_info["USERLABEL"]
            self.add_moc("USERPLANEPEER", **kwargs)
            dstipList.append({"UPPEERID": kwargs["UPPEERID"],
                              "IP": kwargs["PEERIPV4"],
                              "USERLABEL": "To " + kwargs["USERLABEL"]})
        # Create USERPLANEPEER
        if not ugw_pool_list:
            error_count = self.inner_check_para(kwargs, ["PEERIPV4"])
            if 'UPPEERID' not in kwargs:
                kwargs['UPPEERID'] = self.get_free_id_list("USERPLANEPEER", 'UPPEERID').pop(0)
            self.add_moc("USERPLANEPEER", **kwargs)

        return dstipList

    @API_RECORD
    def create_S1(self, sctphostIDList=None, userplanehostIDList=None, sctppeerIDList=None, userplanepeerIDList=None, **kwargs):
        error_count = 0
        if sctphostIDList is None or userplanehostIDList is None:
            error_count += 1
            return error_count
        kwargs["SCTPHOSTREFS"] = [MODEL.EPGROUP.SCTPHOSTREFS(SCTPHOSTID=x) for x in sctphostIDList]
        kwargs["USERPLANEHOSTREFS"] = [MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=x) for x in userplanehostIDList]
        kwargs["SCTPPEERREFS"] = [MODEL.EPGROUP.SCTPPEERREFS(SCTPPEERID=x) for x in sctppeerIDList]
        if userplanepeerIDList != None:
            kwargs["USERPLANEPEERREFS"] = [MODEL.EPGROUP.USERPLANEPEERREFS(UPPEERID=x) for x in userplanepeerIDList]
        kwargs["USERLABEL"] = kwargs["UserLabel"] = "for S1"
        if "EPGROUPID" not in kwargs:
            kwargs["EPGROUPID"] = self.get_free_id_list("EPGROUP", "EPGROUPID").pop(0)
        self.add_moc('EPGROUP', **kwargs)

        kwargs["S1Id"] = self.get_free_id_list("S1", "S1Id").pop(0)
        if "CnOperatorId" not in kwargs:
            kwargs["CnOperatorId"] = 0
        if "MmeRelease" not in kwargs:
            kwargs["MmeRelease"] = "Release_R13"
        if "Priority" not in kwargs:
            kwargs["Priority"] = 255
        if "EpGroupCfgFlag" not in kwargs:
            kwargs["EpGroupCfgFlag"] = ""
            if sctphostIDList not in [None, []]:
                kwargs["EpGroupCfgFlag"] += "CP_"
            if userplanehostIDList not in [None, []]:
                kwargs["EpGroupCfgFlag"] += "UP_"
            kwargs["EpGroupCfgFlag"] += "CFG"
        kwargs["CpEpGroupId"] = kwargs["UpEpGroupId"] = kwargs["EPGROUPID"]
        self.add_moc('S1', **kwargs)
        return error_count

    @API_RECORD
    def create_X2(self, sctphostIDList=None, userplanehostIDList=None, sctppeerIDList=None, userplanepeerIDList=None, **kwargs):
        error_count = 0
        if sctphostIDList is None or userplanehostIDList is None:
            error_count += 1
            return error_count
        kwargs["SCTPHOSTREFS"] = [MODEL.EPGROUP.SCTPHOSTREFS(SCTPHOSTID=x) for x in sctphostIDList]
        kwargs["USERPLANEHOSTREFS"] = [MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=x) for x in userplanehostIDList]
        if "EPGROUPID" not in kwargs:
            kwargs["EPGROUPID"] = self.get_free_id_list("EPGROUP", "EPGROUPID").pop(0)
        kwargs["USERLABEL"] = kwargs["UserLabel"] = "for X2"
        self.add_moc('EPGROUP', **kwargs)

        # Create X2
        kwargs["X2Id"] = self.get_free_id_list("X2", "X2Id").pop(0)
        if "CnOperatorId" not in kwargs:
            kwargs["CnOperatorId"] = 0
        if "TargetENodeBRelease" not in kwargs:
            kwargs["TargetENodeBRelease"] = "Release_R13"
        if "EpGroupCfgFlag" not in kwargs:
            kwargs["EpGroupCfgFlag"] = ""
            if sctphostIDList not in [None, []]:
                kwargs["EpGroupCfgFlag"] += "CP_"
            if userplanehostIDList not in [None, []]:
                kwargs["EpGroupCfgFlag"] += "UP_"
            kwargs["EpGroupCfgFlag"] += "CFG"
        kwargs["CpEpGroupId"] = kwargs["UpEpGroupId"] = kwargs["EPGROUPID"]
        self.add_moc('X2', **kwargs)
        return error_count

    @API_RECORD
    def create_Router(self, **kwargs):
        """Create Router(include IPRT/VLANMAP"""
        error_count = self.inner_check_para(kwargs, ["SN", "DSTIP", "NEXTHOP"])
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        if 'SBT' not in kwargs:
            kwargs['SBT'] = "BASE_BOARD"
        if 'PT' not in kwargs:
            kwargs['PT'] = "ETH"
        if 'DESCRI' not in kwargs:
            kwargs['DESCRI'] = "To PEER"
        if 'PN' not in kwargs:
            kwargs['PN'] = 0
        if 'MASK' not in kwargs:
            kwargs['MASK'] = "255.255.255.255"
        if "DSTMASK" not in kwargs:
            kwargs["DSTMASK"] = kwargs['MASK']
        kwargs['DSTIP'] = self.get_network_by_ip(ip=kwargs["DSTIP"], mask=kwargs["DSTMASK"])
        if 'RTTYPE' not in kwargs:
            kwargs['RTTYPE'] = "NEXTHOP"
        if 'RTIDX' not in kwargs:
            kwargs['RTIDX'] = self.get_free_id_list("IPRT", "RTIDX").pop(0)
        if kwargs['DSTIP'] == '0.0.0.0' and kwargs['DSTMASK'] == '0.0.0.0':
            self.add_moc('GTRANSPARA', FORWARDMODE='HOST')
        self.add_moc('IPRT', **kwargs)
        if 'SETPRIO' not in kwargs:
            kwargs['SETPRIO'] = "DISABLE"
        if 'VLANID' in kwargs:
            kwargs["VLANID"] = int(kwargs["VLANID"])
            kwargs['VLANMODE'] = "SINGLEVLAN"
            if len(self.get_moc("VLANMAP", WHERE(VLANID=kwargs['VLANID']))) < 1:
                kwargs["NEXTHOPIP"] = kwargs["NEXTHOP"]
                self.add_moc('VLANMAP', **kwargs)
        if "VLANGROUPNO" in kwargs:
            kwargs['VLANMODE'] = "VLANGROUP"
            if len(self.get_moc("VLANMAP", WHERE(VLANGROUPNO=int(kwargs['VLANGROUPNO'])))) < 1:
                self.add_moc('VLANMAP', **kwargs)
        return error_count

    @API_RECORD
    def create_IP(self, **kwargs):
        """Create IP (include ETHPORT/INTERFACE/IPADDR4/SRCIPROUTE4/VLAN"""
        error_count = self.inner_check_para(kwargs, ["SN", "PN", "IP"])
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        if 'SBT' not in kwargs:
            kwargs['SBT'] = "BASE_BOARD"
        if int(kwargs['PN']) == 0:
            kwargs['PA'] = "COPPER"
        else:
            kwargs['PA'] = "FIBER"
        if 'SPEED' not in kwargs:
            kwargs['SPEED'] = "AUTO"
        if 'DUPLEX' not in kwargs:
            kwargs['DUPLEX'] = "AUTO"
        if 'ITFID' not in kwargs:
            kwargs['ITFID'] = self.get_free_id_list("INTERFACE", 'ITFID').pop(0)
        if 'ITFTYPE' not in kwargs:
            kwargs['ITFTYPE'] = "NORMAL"
        if 'PT' not in kwargs:
            kwargs['PT'] = "ETH"
        if 'TAGGED' not in kwargs:
            kwargs['TAGGED'] = "ENABLE"
        if 'MASK' not in kwargs:
            kwargs['MASK'] = "255.255.255.0"
        if 'SRCRTIDX' not in kwargs:
            kwargs['SRCRTIDX'] = self.get_free_id_list("SRCIPROUTE4", 'SRCRTIDX').pop(0)
        kwargs['SRCIP'] = kwargs['IP']
        if kwargs['PT'] == "ETH":
            kwargs['RTTYPE'] = "NEXTHOP"
            kwargs['NEXTHOPIP'] = kwargs['NEXTHOP']
        if 'VLANMODE' not in kwargs:
            kwargs['VLANMODE'] = "SINGLEVLAN"
        if 'SETPRIO' not in kwargs:
            kwargs['SETPRIO'] = "DISABLE"
        if len(self.get_para_list_from_moc("ETHPORT", "PORTID", WHERE(SN=int(kwargs['SN']), PN=int(kwargs['PN'])))) == 0:
            kwargs['PORTID'] = kwargs['ITFID']
            self.add_moc("ETHPORT", **kwargs)
        else:
            kwargs['PORTID'] =self.get_para_list_from_moc("ETHPORT", "PORTID", WHERE(SN=int(kwargs['SN']), PN=int(kwargs['PN'])))[0]
        if 'VLANID' not in kwargs:
            kwargs['ITFTYPE'] = "NORMAL"
            if len(self.get_para_list_from_moc("INTERFACE", "ITFID", WHERE(SN=int(kwargs['SN']), PN=int(kwargs['PN'])))) == 0:
                self.add_moc("INTERFACE", **kwargs)
            else:
                kwargs['ITFID'] = self.get_para_list_from_moc("INTERFACE", "ITFID", WHERE(SN=int(kwargs['SN']), PN=int(kwargs['PN'])))[0]
        else:
            vlan_id_list = self.get_para_list_from_moc("INTERFACE", "VLANID")
            if kwargs['VLANID'] not in vlan_id_list:
                kwargs['ITFTYPE'] = "VLAN"
                self.add_moc("INTERFACE", **kwargs)
            else:
                kwargs['ITFID'] = self.get_para_list_from_moc("INTERFACE", "ITFID", WHERE(SN=int(kwargs['SN']), PN=int(kwargs['PN'])))[0]

        self.add_moc("IPADDR4", **kwargs)

        if kwargs['PT'] == "ETH":
            kwargs['PT'] = "TUNNEL"
            self.add_moc("SRCIPROUTE4", **kwargs)
        elif kwargs['PT'] == "LOOPINT":
            self.add_moc("LOOPBACK", **kwargs)

        # if 'VLANID' in kwargs:
        #     self.add_moc("VLANMAP",**kwargs)
        # self.add_moc("GTRANSPARA",TRANSCFGMODE="NEW" )
        return error_count

    @API_RECORD
    def create_IP_NewTXMode(self,**kwargs):
        """Create IP (include ETHPORT/INTERFACE/IPADDR4"""
        error_count = self.inner_check_para(kwargs, ["SN", "PN", "IP"])
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        if 'SBT' not in kwargs:
            kwargs['SBT'] = "BASE_BOARD"
        if int(kwargs['PN']) == 0:
            kwargs['PA'] = "COPPER"
        else:
            kwargs['PA'] = "FIBER"
        if 'SPEED' not in kwargs:
            kwargs['SPEED'] = "AUTO"
        if 'DUPLEX' not in kwargs:
            kwargs['DUPLEX'] = "AUTO"
        if 'ITFID' not in kwargs:
            kwargs['ITFID'] = self.get_free_id_list("INTERFACE", 'ITFID').pop(0)
        if 'ITFTYPE' not in kwargs:
            kwargs['ITFTYPE'] = "NORMAL"
        if 'PT' not in kwargs:
            kwargs['PT'] = "ETH"
        if 'TAGGED' not in kwargs:
            kwargs['TAGGED'] = "ENABLE"
        if 'MASK' not in kwargs:
            kwargs['MASK'] = "255.255.255.0"
        if len(self.get_para_list_from_moc("ETHPORT", "PORTID", WHERE(SN=int(kwargs['SN']), PN=int(kwargs['PN'])))) == 0:
            self.add_moc("ETHPORT", **kwargs)
        if 'VLANID' not in kwargs:
            kwargs['ITFTYPE'] = "NORMAL"
            if len(self.get_para_list_from_moc("INTERFACE", "ITFID", WHERE(SN=int(kwargs['SN']), PN=int(kwargs['PN'])))) == 0:
                self.add_moc("INTERFACE", **kwargs)
            else:
                kwargs['ITFID'] = self.get_para_list_from_moc("INTERFACE", "ITFID", WHERE(SN=int(kwargs['SN']), PN=int(kwargs['PN'])))[0]
        else:
            vlan_id_list = self.get_para_list_from_moc("INTERFACE", "VLANID")
            if kwargs['VLANID'] not in vlan_id_list:
                kwargs['ITFTYPE'] = "VLAN"
                self.add_moc("INTERFACE", **kwargs)
            else:
                kwargs['ITFID'] = self.get_para_list_from_moc("INTERFACE", "ITFID", WHERE(SN=int(kwargs['SN']), PN=int(kwargs['PN'])))[0]

        self.add_moc("IPADDR4", **kwargs)

    @API_RECORD
    def create_IPROUTE4(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["DSTIP", "DSTMASK","NEXTHOP"])
        if 'RTIDX' not in kwargs:
            kwargs['RTIDX'] = self.get_free_id_list("IPROUTE4", 'RTIDX').pop(0)
        if 'RTTYPE' not in kwargs:
            kwargs['RTTYPE'] = 0
        self.add_moc("IPROUTE4", **kwargs)

    @API_RECORD
    def create_EPGROUP(self,sctphostid_list=[],sctppeerid_list=[],uphostid_list=[],uppeerid_list=[],**kwargs):
        if 'EPGROUPID' not in kwargs:
            kwargs['EPGROUPID'] = self.get_free_id_list("EPGROUP", 'EPGROUPID').pop(0)
        if 'USERLABEL' not in kwargs:
            kwargs['USERLABEL'] = ""
        ep_sctphostid_list = [MODEL.EPGROUP.SCTPHOSTREFS(SCTPHOSTID=idx) for idx in sctphostid_list] if sctphostid_list else None
        ep_sctppeerid_list = [MODEL.EPGROUP.SCTPPEERREFS(SCTPPEERID=idx) for idx in sctppeerid_list] if sctppeerid_list else None
        ep_uphostid_list = [MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=idx) for idx in uphostid_list] if uphostid_list else None
        ep_uppeerid_list = [MODEL.EPGROUP.USERPLANEPEERREFS(UPPEERID=idx) for idx in uppeerid_list] if uppeerid_list else None
        epgroup_obj = MODEL.EPGROUP(EPGROUPID=kwargs['EPGROUPID'],USERLABEL=kwargs['USERLABEL'],SCTPHOSTREFS=ep_sctphostid_list,SCTPPEERREFS=ep_sctppeerid_list,USERPLANEHOSTREFS=ep_uphostid_list,USERPLANEPEERREFS=ep_uppeerid_list)
        self.save_moc("EPGROUP", [epgroup_obj], APPEND_MODE, with_merge=True, **kwargs)

    @API_RECORD
    def create_NTP_Time(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["IP"])
        if 'ZONET' not in kwargs:
            kwargs['ZONET'] = 'GMT+0800'
        if 'DST' not in kwargs:
            kwargs['DST'] = 'NO'
        if 'TIMESRC' not in kwargs:
            kwargs['TIMESRC'] = 'NTP'
        if 'MODE' not in kwargs:
            kwargs['MODE'] = 'IPV4'
        if 'SYNCCYCLE' not in kwargs:
            kwargs['SYNCCYCLE'] = 60
        if 'MASTERFLAG' not in kwargs:
            kwargs['MASTERFLAG'] = 'Master'
        self.add_moc("TZ", **kwargs)
        self.add_moc("TIMESRC", **kwargs)
        self.add_moc("NTPCP", **kwargs)
        if 'IP2' in kwargs:
            kwargs['MASTERFLAG'] = 'Slave'
            kwargs['IP'] = kwargs['IP2']
            self.add_moc('NTPCP', **kwargs)
        return error_count

    @API_RECORD
    def create_GPS_Time(self, **kwargs):
        if 'ZONET' not in kwargs:
            kwargs['ZONET'] = 'GMT+0800'
        if 'DST' not in kwargs:
            kwargs['DST'] = 'NO'
        if 'TIMESRC' not in kwargs:
            kwargs['TIMESRC'] = 'GPS'
        self.add_moc("TZ", **kwargs)
        self.add_moc("TIMESRC", **kwargs)
        return

    @API_RECORD
    def create_GPS_Clock(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["SN"])
        if 'CLKSYNCMODE' not in kwargs:
            kwargs['CLKSYNCMODE'] = 'TIME'
        if 'MODE' not in kwargs:
            kwargs['MODE'] = 'GPS'
        if 'GN' not in kwargs:
            kwargs['GN'] = 0
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        self.add_moc("GPS", **kwargs)
        kwargs['MODE'] = 'AUTO'
        self.add_moc("TASM", **kwargs)
        return error_count

    @API_RECORD
    def create_eCPRI_IPCLK(self, **kwargs):
        error_count = 0
        self.add_moc("SYNCETH", LN=1)
        self.add_moc("IPCLKLNK", LN=2, ICPT='PTP', DEVTYPE='OC_MASTER', CNM='L2_MULTICAST', DELAYTYPE='E2E', PROFILETYPE='1588V2')
        return error_count

    @API_RECORD
    def create_SYNCETH(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["SN"])
        if 'CN' not in kwargs:
            kwargs['CN'] = 0
        if 'SRN' not in kwargs:
            kwargs['SRN'] = 0
        if 'PN' not in kwargs:
            kwargs['PN'] = 0
        if 'LN' not in kwargs:
            kwargs['LN'] = self.get_free_id_list("SYNCETH", "LN").pop(0)
        self.add_moc("SYNCETH", **kwargs)
        return error_count

    ####################################################################################################
    # Create TAC, return corresponding TAI
    # Usage: tai = API_Create_Tac("123")
    # Usage: tai = API_Create_Tac("123", TrackingAreaId=10, NbIotTaFlag=1)
    @API_RECORD
    def create_TAC(self, Tac, CnOperatorId=0, TrackingAreaId=0, NbIotTaFlag=0):
        Tac = int(Tac)
        tai = TrackingAreaId
        tai_list = self.get_para_list_from_moc("CnOperatorTa", "TrackingAreaId", WHERE(lambda obj: (int(obj.Tac) == Tac) and int(obj.CnOperatorId) == CnOperatorId))
        if len(tai_list) == 0:  # this TAC is not configured
            existing_tai_list = self.get_para_list_from_moc("CnOperatorTa", "TrackingAreaId")
            if tai in existing_tai_list:  # But TAI is used. Modify TAI to new value
                tai = max(existing_tai_list) + 1
            self.add_moc("CnOperatorTa", TrackingAreaId=tai, Tac=Tac, CnOperatorId=CnOperatorId, NbIotTaFlag=NbIotTaFlag)
        else:  # This TAC is configured,
            tai = tai_list[0]
        return tai

    @API_RECORD
    def create_TAC_MoMOCN(self, Tac, CnOperatorId=0, TrackingAreaId=0, NbIotTaFlag=0):
        Tac = int(Tac)
        tai = TrackingAreaId
        tai_list = self.get_para_list_from_moc("CnOperatorTa", "TrackingAreaId", WHERE(lambda obj: int(obj.Tac) == Tac))
        if len(tai_list) == 0:  # this TAC is not configured
            # existing_tai_list = self.get_para_list_from_moc("CnOperatorTa", "TrackingAreaId")
            # if tai in existing_tai_list:  # But TAI is used. Modify TAI to new value
            #     tai = max(existing_tai_list) + 1
            self.set_moc("CnOperatorTa", TrackingAreaId=tai, Tac=Tac, CnOperatorId=CnOperatorId, NbIotTaFlag=NbIotTaFlag)
        else:  # This TAC is configured,
            tai = tai_list[0]
        return tai

    @API_RECORD
    def create_Second_CnOperator_RANSharing(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["CnOperatorName", "Mcc", "Mnc", "Tac", "TrackingAreaId"])
        if 'CnOperatorId' not in kwargs:
            kwargs['CnOperatorId'] = self.get_free_id_list('CnOperator','CnOperatorId').pop(0)
        if 'CnOperatorType' not in kwargs:
            kwargs['CnOperatorType'] = 'CNOPERATOR_SECONDARY'
        self.add_moc('CnOperator', **kwargs)
        if 'TrackingAreaId' not in kwargs:
            kwargs['TrackingAreaId'] = self.get_free_id_list('CnOperatorTa','TrackingAreaId').pop(0)
        if 'NbIotTaFlag' not in kwargs:
            kwargs['NbIotTaFlag'] = 0
        self.add_moc("CnOperatorTa", **kwargs)
        self.mod_moc('ENodeBSharingMode', ENodeBSharingMode='SHARED_FREQ')
        return error_count

    @API_RECORD
    def update_ANR_in_RANSharing(self, **kwargs):
        kwargs["RanSharingAnrSwitch"] = 'NBSLTEPLMNRoundSwitch-0&NBSLTERANSharingSwitch-0&NBSUTRANRANSharingSwitch-1&NBSGERANRANSharingSwitch-0'
        self.add_moc('ENodeBAlgoSwitch', **kwargs)
        return

    @API_RECORD
    def create_CellOp(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["LocalCellId", "TrackingAreaId"])
        if 'MMECfgNum' not in kwargs:
            kwargs['MMECfgNum'] = 'CELL_MME_CFG_NUM_0'
        self.add_moc('CellOp', **kwargs)
        return error_count

    @API_RECORD
    def create_gNBTAC(self, Tac, TrackingAreaId=0):
        Tac = int(Tac)
        tai = TrackingAreaId
        tai_list = self.get_para_list_from_moc("gNBTrackingArea", "TrackingAreaId", WHERE(lambda obj: int(obj.Tac) == Tac))
        if len(tai_list) == 0:  # this TAC is not configured
            existing_tai_list = self.get_para_list_from_moc("gNBTrackingArea", "TrackingAreaId")
            if tai in existing_tai_list:  # But TAI is used. Modify TAI to new value
                tai = max(existing_tai_list) + 1
            self.add_moc("gNBTrackingArea",TrackingAreaId=tai, Tac=Tac)
        else:  # This TAC is configured,
            tai = tai_list[0]
        return tai

    ####################################################################################################
    # Create one BBP board.
    # Usage: API_Create_One_BBP(0, 0, 3, "UBBPd4", "FM")   #U/L/F/T/M/N
    # Usage: API_Create_One_BBP(0, 0, 3, "UBBP", "T+")  # TDD_Enhance
    # Usage: API_Create_One_BBP(0, 0, 3, "WBBPf4", "")  #
    @API_RECORD
    def create_One_BBP(self, cn, srn, sn, bbp_brd, rat):
        cn, srn, sn = int(cn), int(srn), int(sn)
        error_count = 0
        if bbp_brd[:4] == "UBBP":
            bbp_char_rat_map = {"G": "GSM", "U": "UMTS", "F": "LTE_FDD", "L": "LTE_FDD", "T": "LTE_TDD", "M": "NBIOT", "N": "NR"}
            if rat is None or len(rat) == 0:
                print("Error: UBBP slot=%d, %s, no RAT info. Please set: %r" % (sn, bbp_brd, bbp_char_rat_map.keys()))
            bbws_value = 0
            srt = MODEL.BBP.SRT.DEFAULT
            bbresallocmode = "MANUAL"
            for i in range(len(rat)):
                if rat[i] in ["O"]: continue
                if rat[i] in bbp_char_rat_map:
                    tech_bit = MODEL.BBP.BBWS.field(bbp_char_rat_map[rat[i]])
                    bbws_value |= (1 << tech_bit)
                elif rat[i] == "+" and i > 0:  # + Mean Enhance
                    if rat[i - 1] == "T":
                        srt = MODEL.BBP.SRT.TDD_ENHANCE
                    elif rat[i - 1] == "F":
                        srt = MODEL.BBP.SRT.FDD_ENHANCE
                    elif rat[i - 1] == "M":
                        srt = MODEL.BBP.SRT.NBIOT_ENHANCE
                else:
                    print("Error: BBP slot=%d, %s, RAT=%s is invalid. Must be one of %r" % (
                    sn, bbp_brd, rat, bbp_char_rat_map.keys()))
                    error_count += 1
            if "UBBPfw1" in bbp_brd or "UBBPfw2" in bbp_brd:  # 5G full-width BBP
                ubbp_type = MODEL.BBP.TYPE.field("UBBP-W")
            else:  # Normal UBBP
                ubbp_type = MODEL.BBP.TYPE.UBBP
            bbp_obj = MODEL.BBP(CN=cn, SRN=srn, SN=sn, TYPE=ubbp_type, BBWS=bbws_value, SRT=srt,BRDSPEC=bbp_brd[:6],BBRESALLOCMODE=bbresallocmode,WM=MODEL.BBP.WM.NORMAL)
            pass
        elif bbp_brd[:4] == "WBBP":
            bbp_obj = MODEL.BBP(CN=cn, SRN=srn, SN=sn, TYPE=MODEL.BBP.TYPE.WBBP, WM=MODEL.BBP.WM.FDD)
        elif bbp_brd[:4] == "LBBP":
            lbbp_wm_map = {"T": "TDD", "T+": "TDD_ENHANCE", "TS": "TDD_TL",
                           "F": "FDD", "M": "NBIOT", "FM": "FDD_NBIOT", "FM+": "FDD_NBIOT_ENHANCE"}
            if rat is None or len(rat) == 0:
                print("Error: UBBP slot=%d, %s, no RAT info. Please set: %r" % (sn, bbp_brd, lbbp_wm_map.keys()))
            if rat in lbbp_wm_map:
                wm = lbbp_wm_map[rat]
                bbp_obj = MODEL.BBP(CN=cn, SRN=srn, SN=sn, TYPE=MODEL.BBP.TYPE.LBBP, WM=MODEL.BBP.WM.field(wm))
            else:
                print("Error: LBBP slot=%s, %s, RAT=%s is invalid. Must be one of %r" % (
                sn, bbp_brd, rat, lbbp_wm_map.keys()))
                error_count += 1
            pass
        else:
            print("Error: BBP slot=%d, BBP type=%s is invalid. Please check" % (sn, bbp_brd))
            error_count += 1

        if error_count == 0:
            self.save_moc("BBP", [bbp_obj], APPEND_MODE, with_merge=True)

        return error_count

    ####################################################################################################
    # Create S1/EPGROUP/SCTPPEER/IPRT to MME
    @API_RECORD
    def create_MME(self, excel_fn, mme_pool_name, sctphost_id, uphost_id, lte_gateway, cn_operator_id, sctppeer_id=0,
                       epgroup_id=0, s1_id=0,
                       one_mme_one_s1=False, support_nbiot=False, key_title_name="MME_POOL_NAME"):
        # Read MME Pool setting file, sheet name must be 'MME Pool', and title_row=3
        mme_pool_info_map = load_Excel_File(excel_fn, "MME Pool", 3, key_title_name)
        if mme_pool_name not in mme_pool_info_map:
            self.exit_Info("MME_POOL_NAME=%s is not exist in 'MME Pool' sheet" % mme_pool_name)
        mme_pool_list = mme_pool_info_map[mme_pool_name]

        # Config SCTPPEER
        sctppeerid_list = []
        for mme_info in mme_pool_list:
            mme_ip1 = mme_info["IP1"]
            mme_ip2 = mme_info["IP2"] if len(mme_info["IP2"]) > 0 else "0.0.0.0"
            mme_name = mme_info["MME_NAME"]
            mme_port = mme_info["PORT"]
            mme_release = mme_info["RELEASE"]

            sctppeer_id = self.get_Available_ID("SCTPPEER", "SCTPPEERID", sctppeer_id)
            sctppeer_obj = MODEL.SCTPPEER(SCTPPEERID=sctppeer_id, SIGIP1V4=mme_ip1, SIGIP2V4=mme_ip2, PN=mme_port,
                                          USERLABEL=mme_name,
                                          VRFIDX=0, IPVERSION="IPv4")
            self.save_moc("SCTPPEER", [sctppeer_obj], APPEND_MODE, with_merge=True)
            sctppeerid_list.append(sctppeer_id)
            sctppeer_id += 1
            pass

        # Config EPGROUP
        epgroup_id = self.get_Available_ID("EPGROUP", "EPGROUPID", epgroup_id)
        if one_mme_one_s1:
            ep_sctphost_obj = MODEL.EPGROUP.SCTPHOSTREFS(SCTPHOSTID=sctphost_id)
            ep_sctppeer_obj_list = [MODEL.EPGROUP.SCTPPEERREFS(SCTPPEERID=idx) for idx in sctppeerid_list]
            ep_uphost_obj = MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=uphost_id)
            epgroup_obj = MODEL.EPGROUP(EPGROUPID=epgroup_id, SCTPHOSTREFS=[ep_sctphost_obj],
                                        SCTPPEERREFS=ep_sctppeer_obj_list,
                                        USERPLANEHOSTREFS=[ep_uphost_obj], USERLABEL="MME")
            self.save_moc("EPGROUP", [epgroup_obj], APPEND_MODE, with_merge=True)
        else:
            pass

        # Config S1
        s1_id = self.get_Available_ID("S1", "S1Id", s1_id)
        if one_mme_one_s1:
            s1_obj = MODEL.S1(S1Id=s1_id, CnOperatorId=cn_operator_id, CpEpGroupId=epgroup_id, UpEpGroupId=epgroup_id,
                              MmeRelease=mme_release, Priority=255, UserLabel="MME",
                              EpGroupCfgFlag=MODEL.S1.EpGroupCfgFlag.CP_UP_CFG)
            self.save_moc("S1", [s1_obj], APPEND_MODE, with_merge=True)
        else:
            pass

        if support_nbiot:
            # Config MmeCapInfo
            if one_mme_one_s1:
                mme_capinfo_id = self.get_Available_ID("MmeCapInfo", "MmeCapCfgId", 0)
                mmecapinfo_obj = MODEL.MmeCapInfo(MmeCapCfgId=mme_capinfo_id, S1Id=s1_id,
                                                  S1CfgType=MODEL.MmeCapInfo.S1CfgType.S1_CFG,
                                                  NbCiotEpsOptCap="CP", NbLteSupportCap="NOT_SUPPORT",
                                                  MmeSupportEmtcDedEpcCap="NOT_SUPPORT")
                self.save_moc("MmeCapInfo", [mmecapinfo_obj], APPEND_MODE, with_merge=True)
            else:
                pass

        # Config IPRT to MME
        mtp_cn, mpt_srn, mpt_sn = self.get_para_list_from_moc("MPT", ["CN", "SRN", "SN"])[0]  # Find MPT slot
        mme_dstmask = "255.255.255.0"  # 到NB MME的IPRT的路由掩码
        added_dstip_list = []
        for mme_info in mme_pool_list:
            for mme_ip in [mme_info["IP1"], mme_info["IP2"]]:
                if mme_ip in ["0.0.0.0", None]: continue  # Skip if MME IP is 0.0.0.0 or None
                dstip = ".".join([str(int(a) & int(b)) for (a, b) in zip(mme_ip.split("."), mme_dstmask.split("."))])
                if dstip in added_dstip_list: continue
                added_dstip_list.append(dstip)
                iprt_id = self.get_Available_ID("IPRT", "RTIDX", 0)
                iprt_obj = MODEL.IPRT(RTIDX=iprt_id, CN=mtp_cn, SRN=mpt_srn, SN=mpt_sn, SBT="BASE_BOARD",
                                      RTTYPE="NEXTHOP",
                                      DSTIP=dstip, DSTMASK=mme_dstmask, NEXTHOP=lte_gateway, DESCRI="TO MME")
                self.save_moc("IPRT", [iprt_obj], APPEND_MODE, with_merge=True)
                iprt_id += 1
        pass

    ####################################################################################################
    # Use Excel Template to create Data
    # Please refer to: http://3ms.huawei.com/hi/group/2030315/thread_6885841.html?mapId=8575419
    @API_RECORD
    def load_TX_Excel_Template(self, excel_fn, sheet_name, ne_type, filter_map, replace_map, include_moc_list=None,
                                 exclude_moc_list=None):
        MAX_PARA_QTY = 100  # 最大参数个数

        moc_title_map = {}  # 保存moc的参数名称
        moc_data_map = {}  # 保存moc的数据行

        # 读取Excel传输模板
        tx_moc_list = self.get_list_from_excel(excel_fn, sheet_name, 2)
        if len(tx_moc_list) == 0:
            self.exit_Info("Error: NO data was found in excel file=%s sheet=%s!" % (excel_fn, sheet_name))

        # 检查过滤条件
        filter_title_list = []
        for (filter_title, filter_list) in filter_map.items():
            if tx_moc_list[0].exist_attr(filter_title):
                filter_title_list.append(filter_title)
            else:
                self.print_msg( "Error: title=%s not found in excel file=%s sheet=%s row=2" % (filter_title, excel_fn, sheet_name))
                has_error = True

        for tx_moc in tx_moc_list:
            if tx_moc.attr("MOC") is None: continue  # 没有MOC名称的行，跳过
            if tx_moc.attr("NETYPE") != ne_type: continue  # 按照NETYPE类型过滤
            moc = tx_moc.attr("MOC")
            if include_moc_list is not None and moc not in include_moc_list: continue  # 不在指定的moc列表中,跳过
            if exclude_moc_list is not None and moc in exclude_moc_list: continue  # 在排除的moc列表中，跳过

            if tx_moc.attr("ROWTYPE") == "title":  # 标题行
                if moc not in moc_title_map:
                    moc_title_map[moc] = tx_moc
            else:
                no_need_row = False
                for filter_title in filter_title_list:  # 对过滤条件进行检查
                    if tx_moc.attr(filter_title) not in filter_map[filter_title]:
                        no_need_row = True
                        break
                if no_need_row == False:  # 需要的数据行
                    if moc not in moc_data_map:
                        moc_data_map[moc] = []
                    moc_data_map[moc].append(tx_moc)
            pass

        # 开始创建对象
        result_table_map = {}  # 保存创建的对象列表
        has_error = False
        no_value_list = []  # 保存没有在replace_map中提供值的变量列表
        for (moc, moc_data_list) in moc_data_map.items():
            if not hasattr(MODEL, moc):
                self.print_msg("Error：moc=%s not exist in MODEL. Please check." % moc)
                has_error = True
            title_row = moc_title_map[moc]
            obj_class = getattr(MODEL, moc)

            # 检查参数名
            for i in range(1, MAX_PARA_QTY + 1):  # 最多100个参数
                col_name = "PARA%d" % i
                if not title_row.exist_attr(col_name): break  # 表格中没有这一列，表示全部参数读取完成
                if title_row.attr(col_name) is None: break  # 遇到空格，表示全部参数读取完成
                para_name = title_row.attr(col_name)
                if hasattr(obj_class, para_name) == False:
                    self.print_msg("Warning: moc=%s has no attr=%s. Please check" % (moc, para_name))

            # 创建对象
            obj_list = []
            for moc_data in moc_data_list:
                obj = obj_class()
                for i in range(1, MAX_PARA_QTY + 1):  # 最多100个参数
                    col_name = "PARA%d" % i
                    if not title_row.exist_attr(col_name): break  # 表格中没有这一列，表示全部参数读取完成
                    if title_row.attr(col_name) is None: break  # 遇到空格，表示全部参数读取完成
                    para_name = title_row.attr(col_name)
                    value = moc_data.attr(col_name)
                    if value is None: continue  # 表示该参数的值为空，跳过

                    if "{" in value:  # 存在变量，进行变量替换
                        pos = 0
                        tmp_replace_map = {}  # 查找和记录变量的值
                        while pos < len(value) - 1:
                            r_start = value.find("{", pos)
                            r_end = value.find("}", r_start + 1)
                            r_str = value[r_start + 1: r_end]
                            if r_str in replace_map:
                                tmp_replace_map[value[r_start: r_end + 1]] = replace_map[r_str]
                            else:
                                if r_str not in no_value_list:
                                    no_value_list.append(r_str)
                                    self.print_msg("Error: no value for {%s}" % r_str)
                                    has_error = True
                            pos = r_end + 1
                        # 替换变量
                        for (r, t) in tmp_replace_map.items():
                            if t is None:  # 变量的值=None，增加告警信息输出
                                self.print_msg("Warning: %s is empty" % r)
                                t = ""
                            elif type(t) != str or type(t) != type(u""):  # 变量的值不是字符串，需要转换为字符串后，再进行替换
                                t = str(t)  # 把非字符串替换为字符串

                            value = value.replace(r, t)
                        pass

                    # 判断参数的类型：枚举值、列表、字符串/整数,
                    para_class = getattr(obj_class, para_name)
                    if para_class.typeName == "Enum" and len(value) > 0:  # 如果是枚举值
                        if value in para_class._field_names_:  # 判断输入的是否是有效的值。对无效值报错
                            value = para_class.field(value)
                        elif value.isdigit() == False:  # 非数值
                            self.print_msg("Error: MOC=%s, PARA=%s: %s is invalid, should be %r" % (
                            moc, para_name, value, para_class._field_names_))
                            has_error = True
                            continue
                    elif para_class.typeName == "List":  # 如果是列表
                        v_list = value.split(";")  # 多个值用;分割
                        v_list = [s.strip() for s in v_list if len(s.strip()) > 0]
                        sub_obj_list = []
                        for v in v_list:
                            sub_obj = para_class()
                            setattr(sub_obj, para_class._field_names_[0], v)
                            sub_obj_list.append(sub_obj)
                        value = sub_obj_list

                    # 设置参数的值
                    if value == "": value = None  # 把空字符串转换为None
                    setattr(obj, para_name, value)
                obj_list.append(obj)

            if moc == "IPRT":  # Correct IPRT
                for obj in obj_list:
                    obj.DSTIP = MODEL.IPV4.fromString(obj.DSTIP) & MODEL.IPV4.fromString(obj.DSTMASK)
            if has_error == False:
                obj_list = convert_Object(moc, obj_list)
            result_table_map[moc] = obj_list  # 保存创建的对象列表

        if has_error:
            self.exit_Info("Error: Failed to create objects!")

        return result_table_map  # 返回创建的对象列表


    @API_RECORD
    def get_Dict_From_List_By_Title(self, info_list, title):
        result_dict = {}
        if title not in info_list[0]:
            return None
        for x in info_list:
            if x.attr(title) not in result_dict:
                result_dict[x.attr(title)] = []
            result_dict[x.attr(title)].append(x)
        return result_dict

    ###########################################################################
    # Read ID Plan Table, Return a dict which include Plan ID for each sector each band
    # Excel Must include "ID Plan" sheet, and title must be in first line.
    # Please refer to: http://3ms.huawei.com/hi/group/2030315/thread_6898423.html?mapId=8589265
    @API_RECORD
    def get_ID_Plan(self, excel_file, id_type):
        id_plan_map = load_Excel_File(excel_file, "ID Plan", 1, "ID_TYPE")
        if len(id_plan_map) == 0:
            raise Exception("Error: No ID Plan was found in ID Plan sheet")
        if id_type not in id_plan_map:
            raise Exception("Error: %s plan is not exist in ID Plan sheet" % id_type)

        plan_list = id_plan_map[id_type]
        result_map = {}
        for plan_info in plan_list:
            band = plan_info.attr(u"FREQ_BAND")
            if band not in result_map:
                result_map[band] = {}

            for i in range(12):  # 最大支持12个扇区
                sector_name = "SECTOR_%s" % (chr(ord("A") + i))
                if not hasattr(plan_info, sector_name): continue
                if plan_info.attr(sector_name):
                    string_list = plan_info.attr(sector_name).replace(",", ";").split(";")
                    result_map[band][sector_name] = [s.strip() for s in string_list if len(s.strip()) > 0]
                else:
                    result_map[band][sector_name] = []
        return result_map

    @API_RECORD
    def get_ID_Plan_Ex(self, excel_file):
        id_plan_map = load_Excel_File(excel_file, "ID Plan", 1, "ID_TYPE")
        if len(id_plan_map) == 0:
            raise Exception("Error: No ID Plan was found in ID Plan sheet")
        for id_type, plan_list in id_plan_map.items():
            result_map = {}
            for plan_info in plan_list:
                band = plan_info.attr(u"FREQ_BAND")
                if band not in result_map:
                    result_map[band] = {}

                for i in range(12):  # 最大支持12个扇区
                    sector_name = "SECTOR_%s" % (chr(ord("A") + i))
                    if not hasattr(plan_info, sector_name): continue
                    if plan_info.attr(sector_name):
                        string_list = plan_info.attr(sector_name).replace(",", ";").split(";")
                        result_map[band][sector_name] = [s.strip() for s in string_list if len(s.strip()) > 0]
                    else:
                        result_map[band][sector_name] = []
            self.ID_Plan_Cache[id_type] = result_map
        self.print_msg("NE=%s Get ID Plan and Save to Cache!" % self.NEName)
        return self.ID_Plan_Cache

    # 从RXU的工作制式字符串，获得对应的整数值
    # example: rs = API_Get_RXU_WorkModeValue_From_String("GULM")
    @API_RECORD
    def get_RXU_WorkMode_From_String(self, work_mode_str):
        work_mode_value = 0
        if "G" in work_mode_str:
            work_mode_value += MODEL.RRU.RS.GO
        if "U" in work_mode_str:
            work_mode_value += MODEL.RRU.RS.UO
        if "L" in work_mode_str:
            work_mode_value += MODEL.RRU.RS.LO
        if "M" in work_mode_str:
            work_mode_value += MODEL.RRU.RS.MO
        if "T" in work_mode_str:  # TDD-LTE
            work_mode_value += MODEL.RRU.RS.TDL
        if "N" in work_mode_str:  # 5G NR
            work_mode_value += MODEL.RRU.RS.NO
        return work_mode_value

    # get work mode list from workmode rxu For JSON to CME Decoding
    # eg GUM = ['GSM', 'UMTS','NBIOT']
    @API_RECORD
    def get_RXU_WorkMode_List_From_String(self, work_mode_str):
        work_mode_value = []
        if "G" in work_mode_str:
            work_mode_value.append('GSM')
        if "U" in work_mode_str:
            work_mode_value.append('UMTS')
        if "L" in work_mode_str:
            work_mode_value.append('LTE')
        if "M" in work_mode_str:
            work_mode_value.append('NBIOT')
        if "T" in work_mode_str:  # TDD-LTE
            work_mode_value.append('TDD')
        # if "N" in work_mode_str:  # 5G NR
        #     work_mode_value.append('GSM')
        return work_mode_value
    # 读取WSD的设计数据(Excel/Json)，创建RXU硬件设备
    # rruchain_obj_list, rru_obj_list, rfu_obj_list, sectoreqm_obj_list, sector_obj_list =
    #                                                  API_Create_RXU_WSD("Site1", site_list_filename)

    # 从WSD获取硬件信息, 支持Json、Excel两种方式
    @API_RECORD
    def get_RXU_Info_From_WSD(self, ne_name, wsd_cme_docking_filename="*WSD-CME Docking*"):
        rxu_info_list = []
        wsd_filename_list = search_Files(wsd_cme_docking_filename)
        if len(wsd_filename_list) > 0:  # Get RXU info from WSD-CME Docking Excel file
            rxu_info_list = self.get_RXU_Info_By_Scenario(wsd_filename_list[0], [ne_name], "NE_NAME")
        else:  # Get RXU info from WSD Server by Json
            json = load_WSD_File(ne_name)
            self.print_msg( json)
            json_rxu_list = []
            for tmp in json.rxuScenarios:
                if tmp.nEName == ne_name:
                    json_rxu_list = tmp.rxuInfos
                    break
            if len(json_rxu_list) == 0:
                self.exit_Info("Not found RXU for BTS=%s in WSD JSON file" % ne_name)

            self.print_msg( "RXU Info fro ")
            for rxu in json_rxu_list:
                row = ExcelRow()
                row["SECTOR_NO"] = rxu.physiNos
                row["BAND"] = rxu.rxuBand
                row["RXUSPEC"] = rxu.rxuType
                row["CN-SRN-SN"] = rxu.cNSrnSn
                row["CN-SRN-SN_Orgin"] = rxu.orgCNSrnSn
                row["WORK_MODE"] = rxu.workMode
                row["RCN"] = rxu.rxuToBbpInfos[0].rxuChainRcn
                row["CPRI_BBP_PORT1"] = rxu.rxuToBbpInfos[0].rxuToBbpPort0
                row["CPRI_BBP_PORT2"] = rxu.rxuToBbpInfos[0].rxuToBbpPort1
                row["PS"] = rxu.rxuToBbpInfos[0].rxuPs
                row["GSM_PORT_ASSIGN"] = rxu.rxuToAntInfos[0].gsmPortAssign
                row["UMTS_PORT_ASSIGN"] = rxu.rxuToAntInfos[0].umtsPortAssign
                row["LTE_PORT_ASSIGN"] = rxu.rxuToAntInfos[0].ltePortAssign
                row["NB_PORT_ASSIGN"] = rxu.rxuToAntInfos[0].nbiotPortAssign
                row["5G_PORT_ASSIGN"] = rxu.rxuToAntInfos[0].nrPortAssign
                rxu_info_list.append(row)
            pass
        if len(rxu_info_list) == 0:
            self.exit_Info("Not found RXU for BTS%s in WSD file" % ne_name)
        return rxu_info_list

    @API_RECORD
    def create_RXU_From_WSD_aux(self, rxu_info_list, site_list_filename):
        # 读取RXU规格表
        rxu_spec_map = load_Excel_File(site_list_filename, "RXU Spec", 2, "RXUSPEC")
        if len(rxu_spec_map) == 0:
            raise Exception("Error: No RXU_Spec was found in RXU Spec sheet")
        pass

        # 读取并获得SECTOREQMID的规划表
        sectoreqmid_plan_map = self.get_ID_Plan(site_list_filename, "SECTOREQMID")
        # 获得扇区ID
        sectorid_plan_map = self.get_ID_Plan(site_list_filename, "SECTORID")

        # 创建扇区设备对象
        sectoreqm_obj_list = []
        rxu_interconnectino_sector_band_map = {}  # 记录射频互连的RXU对应关系
        for rxu_info in rxu_info_list:
            if "SECTOR_NO" not in rxu_info: continue  # 对于没有扇区的RXU，不生成扇区设备
            band = rxu_info["BAND"]
            if band is None: continue
            sector = rxu_info["SECTOR_NO"]
            work_mode = rxu_info["WORK_MODE"]
            gm = rxu_info["GSM_PORT_ASSIGN"]
            um = rxu_info["UMTS_PORT_ASSIGN"]
            lm = rxu_info["LTE_PORT_ASSIGN"]
            nm = rxu_info["NB_PORT_ASSIGN"]
            g5m = rxu_info["5G_PORT_ASSIGN"]

            if "&" in sector:  # RRU用于两个扇区，如扇区劈裂
                sector1, sector2 = sector.split("&")
                mode1, mode2 = work_mode.split("&")
                assign_list1 = []
                assign_list2 = []
                for tmp in [gm, um, lm, nm, g5m]:
                    if tmp is None:
                        assign_list1.append(None)
                        assign_list2.append(None)
                    else:
                        assign_list1.append(tmp.split("&")[0])
                        assign_list2.append(tmp.split("&")[1])
                self.inner_create_sectoreqm_WSD(sectoreqm_obj_list, sectoreqmid_plan_map, sectorid_plan_map, sector1, band,
                                           mode1,
                                           assign_list1, [rxu_info])
                self.inner_create_sectoreqm_WSD(sectoreqm_obj_list, sectoreqmid_plan_map, sectorid_plan_map, sector2, band,
                                           mode2,
                                           assign_list2, [rxu_info])
            elif "&" in band:  # RRU支持两个频段,
                band1, band2 = band.split("&")
                mode1, mode2 = work_mode.split("&")
                assign_list1 = []
                assign_list2 = []
                for tmp in [gm, um, lm, nm, g5m]:
                    if tmp is None:
                        assign_list1.append(None)
                        assign_list2.append(None)
                    else:
                        assign_list1.append(tmp.split("&")[0])
                        assign_list2.append(tmp.split("&")[1])
                self.inner_create_sectoreqm_WSD(sectoreqm_obj_list, sectoreqmid_plan_map, sectorid_plan_map, sector, band1,
                                           mode1, assign_list1, [rxu_info])
                self.inner_create_sectoreqm_WSD(sectoreqm_obj_list, sectoreqmid_plan_map, sectorid_plan_map, sector, band2,
                                           mode2, assign_list2, [rxu_info])
            else:
                assign_list = [gm, um, lm, nm, g5m]
                tmp_str = "".join([s for s in assign_list if s is not None])  #
                if "a" in tmp_str or "b" in tmp_str:  # 如果在端口分配模式中，存在小写的a,b(即第二个RXU的端口)，在认为是射频互连
                    if sector not in rxu_interconnectino_sector_band_map:
                        rxu_interconnectino_sector_band_map[sector] = {}
                    if band not in rxu_interconnectino_sector_band_map[sector]:
                        rxu_interconnectino_sector_band_map[sector][band] = []
                    rxu_interconnectino_sector_band_map[sector][band].append(rxu_info)
                else:
                    self.inner_create_sectoreqm_WSD(sectoreqm_obj_list, sectoreqmid_plan_map, sectorid_plan_map, sector,
                                               band, work_mode, assign_list, [rxu_info])
            pass

        # 为射频互连的RXU创建扇区设备对象
        for (sector, rxu_band_map) in rxu_interconnectino_sector_band_map.items():
            for (band, tmp_rxu_info_list) in rxu_band_map.items():
                mode = tmp_rxu_info_list[0]["WORK_MODE"]
                assign_list = [gm, um, lm, nm, g5m]
                while len(tmp_rxu_info_list) > 0:
                    rxu_info = tmp_rxu_info_list.pop(0)
                    if len(tmp_rxu_info_list) == 0:
                        self.inner_create_sectoreqm_WSD(sectoreqm_obj_list, sectoreqmid_plan_map, sectorid_plan_map, sector,
                                                   band, mode, assign_list, [rxu_info])
                    else:
                        rxu_info2 = tmp_rxu_info_list.pop(0)
                        self.inner_create_sectoreqm_WSD(sectoreqm_obj_list, sectoreqmid_plan_map, sectorid_plan_map, sector,
                                                   band, mode, assign_list, [rxu_info, rxu_info2])
                        if "G" in mode:  # 含G的制式才互联，UMTS/LTE双拼，不需要配置射频互连
                            rxu_info["inter_connect_rxu"] = rxu_info2
                            rxu_info2["inter_connect_rxu"] = rxu_info
            pass

        # 创建RXU
        rru_obj_list = []
        rfu_obj_list = []
        aaru_obj_list = []
        aamu_obj_list = []
        aas_obj_list = []
        rruchain_info_map = {}
        for rxu_info in rxu_info_list:
            if "RXU_TYPE" not in rxu_info:  # from RXU Name(such as RRU3953) to get RXU_TYPE(such as MRRU) and TX_NUM, RX_NUM
                rxu_spec = rxu_info[u"RXUSPEC"]
                if rxu_spec not in rxu_spec_map:
                    raise Exception("Error: RXU_SPEC=%s not exist in RXUSpec sheet. Please define" % rxu_spec)
                xTxR = rxu_spec_map[rxu_spec][0].attr(u"xTxR")
                txnum, rxnum = xTxR.split("T")
                if int(txnum) > 8:  # 发射端口大于8，只支持BEAM，设置发射端口号为0
                    txnum, rxnum = 0, 0
                else:
                    txnum = int(txnum)
                    rxnum = int(rxnum[:-1])  # 去掉尾部的R字符

                title = "RXU_TYPE" if "RXU_TYPE" in rxu_spec_map[rxu_spec][0] else "RRU_TYPE"  # Title in RXU Spec sheet
                rxu_type = rxu_spec_map[rxu_spec][0][title]
            else:
                rxu_type = rxu_info["RXU_TYPE"]
                txnum, rxnum = rxu_info["TX_RX_NUM"]

            rcn = int(rxu_info[u"RCN"])
            if rcn not in rruchain_info_map:
                rruchain_info_map[rcn] = []
            if rxu_info[u"CPRI_BBP_PORT1"] and rxu_info[u"CPRI_BBP_PORT1"] not in rruchain_info_map[rcn]:
                rruchain_info_map[rcn].append(rxu_info[u"CPRI_BBP_PORT1"])
            if rxu_info[u"CPRI_BBP_PORT2"] and rxu_info[u"CPRI_BBP_PORT2"] not in rruchain_info_map[rcn]:
                rruchain_info_map[rcn].append(rxu_info[u"CPRI_BBP_PORT2"])

            # 计算RRU工作制式的值
            work_mode = rxu_info[u"WORK_MODE"]
            work_mode_value = self.get_RXU_WorkMode_From_String(work_mode)

            cn, srn, sn = self.inner_get_cn_srn_sn_from_rxu_info(rxu_info)
            if rxu_type[1:4] in ["RRU", "IRU"]:
                rxu_obj = MODEL.RRU(CN=cn, SRN=srn, SN=sn, RCN=rcn, PS=rxu_info[u"PS"], TXNUM=txnum, RXNUM=rxnum,
                                    RS=work_mode_value, RT=MODEL.RRU.RT.field(rxu_type),
                                    RUSPEC=rxu_info["RXUSPEC"],
                                    TP=MODEL.RRU.TP.TRUNK,
                                    ADMSTATE=MODEL.RRU.ADMSTATE.UNBLOCKED)
                rru_obj_list.append(rxu_obj)
            elif rxu_type[1:4] in ["AMU"]:
                rxu_obj = MODEL.AARU(CN=cn, SRN=srn, SN=sn,TXNUM=txnum, RXNUM=rxnum,
                                    RS=work_mode_value,
                                    VRETNO=(str((int(str(srn)[0]))-2))+str((sn+int(str(srn)[-1]))),
                                    ADMSTATE=MODEL.RRU.ADMSTATE.UNBLOCKED)
                aaru_obj_list.append(rxu_obj)
                temp=[]
                if srn not in temp:
                    aamu_obj = MODEL.AAMU(CN=0, SRN=srn,SN=0,TP=MODEL.AAMU.TP.TRUNK,
                                        RCN=rcn,PS=rxu_info[u"PS"])
                    aamu_obj_list.append(aamu_obj)
                    aas_obj = MODEL.AAS(CN=0, SRN=srn, AN="AAU_"+str(srn)[-1])
                    aas_obj_list.append(aas_obj)
            else:
                rxu_obj = MODEL.RFU(CN=cn, SRN=srn, SN=sn, RCN=rcn, PS=rxu_info[u"PS"], TXNUM=txnum, RXNUM=rxnum,
                                    RS=work_mode_value, RT=MODEL.RFU.RT.field(rxu_type),
                                    RUSPEC=rxu_info["RXUSPEC"],
                                    TP=MODEL.RFU.TP.TRUNK,
                                    ADMSTATE=MODEL.RFU.ADMSTATE.UNBLOCKED)
                rfu_obj_list.append(rxu_obj)
                exsiting_subrack_cn_srn_list = self.get_para_list_from_moc("SUBRACK", ["CN", "SRN"])
                if [cn,srn] not in exsiting_subrack_cn_srn_list:
                    self.add_moc("SUBRACK",CN=cn, SRN=srn, TYPE = MODEL.SUBRACK.TYPE.RFU)
            # 配置射频互连
            if "inter_connect_rxu" in rxu_info:
                cn, srn, sn = self.inner_get_cn_srn_sn_from_rxu_info(rxu_info["inter_connect_rxu"])
                rxu_obj.RFCONNTYPE = MODEL.RRU.RFCONNTYPE.INTRA_SYS_INTERCONN
                rxu_obj.RFCONNCN2 = cn
                rxu_obj.RFCONNSRN2 = srn
                rxu_obj.RFCONNSN2 = sn

            # 设置VSWR告警门限
            rxu_obj.ALMPROCSW = None if "VSWR_THD_LV1" not in rxu_info else MODEL.RFU.ALMPROCSW.ON
            rxu_obj.ALMTHRHLD = None if "VSWR_THD_LV1" not in rxu_info else rxu_info["VSWR_THD_LV1"]
            rxu_obj.ALMPROCTHRHLD = None if "VSWR_THD_LV2" not in rxu_info else rxu_info["VSWR_THD_LV2"]

            # RXU用于UMTS且频段为850/900时，设置RXU带宽为4.2M
            if "U" in work_mode:
                if "900" in rxu_info[u"BAND"]:
                    rxu_obj.FMBWH = MODEL.RFU.FMBWH.field("4200")
                elif "850" in rxu_info[u"BAND"]:
                    rxu_obj.FMBWH = MODEL.RFU.FMBWH.field("4200")
                else:
                    pass

            # 增加辅助信息
            if "SECTOR_NO" in rxu_info:
                rxu_obj.info_sector = rxu_info[u"SECTOR_NO"]
                rxu_obj.info_band = rxu_info[u"BAND"]
            pass

        # 创建RRUCHAIN
        rruchain_obj_list = []
        for (rcn, cpri_port_list) in rruchain_info_map.items():
            hcn, hsrn, hsn, hpn = cpri_port_list[0].split("-")
            rruchain_obj = MODEL.RRUCHAIN(RCN=int(rcn), HCN=hcn, HSRN=hsrn, HSN=hsn, HPN=hpn)

            #eCPRI配置
            for rxu_tmp_obj in rru_obj_list:
                if rxu_tmp_obj.RCN == rruchain_obj.RCN:
                    if rxu_tmp_obj.TXNUM == 0 or rxu_tmp_obj.TXNUM == 16 or rxu_tmp_obj.TXNUM == 32 or rxu_tmp_obj.TXNUM == 64:
                        rruchain_obj.PROTOCOL = "eCPRI"
                    else:
                        rruchain_obj.PROTOCOL = "CPRI"

            if len(cpri_port_list) == 1:  # 一根光纤
                rruchain_obj.TT = MODEL.RRUCHAIN.TT.CHAIN
                rruchain_obj.BM = MODEL.RRUCHAIN.BM.COLD
                rruchain_obj.AT = MODEL.RRUCHAIN.AT.LOCALPORT
            else:  # 两根光纤
                rruchain_obj.TT = MODEL.RRUCHAIN.TT.LOADBALANCE
                rruchain_obj.TCN, rruchain_obj.TSRN, rruchain_obj.TSN, rruchain_obj.TPN = cpri_port_list[1].split("-")
            rruchain_obj_list.append(rruchain_obj)

        # 根据扇区设备对象，创建扇区对象
        sector_obj_list = self.inner_create_sector_by_sectoreqm(sectoreqm_obj_list)
        self.save_moc("AAMU", aamu_obj_list, OVERWRITE_MODE)
        self.save_moc("AARU", aaru_obj_list, OVERWRITE_MODE)
        self.save_moc("AAS", aas_obj_list, OVERWRITE_MODE)

        return rruchain_obj_list, rru_obj_list, rfu_obj_list, sectoreqm_obj_list, sector_obj_list

    # 从WSD获取RXU硬件信息，创建RRU/RFU/RRUCHAIN/SectorEqm/Secor
    @API_RECORD
    def create_RXU_From_WSD(self, ne_name, site_list_filename, wsd_cme_docking_filename="*WSD-CME Docking*"):
        rxu_info_list = self.get_RXU_Info_From_WSD(ne_name, wsd_cme_docking_filename)
        return self.create_RXU_From_WSD_aux(rxu_info_list, site_list_filename)

    # 当找不到对应的NE时就用common的配置，这样的话如果所有站点硬件配置都一样就不用每个站点去添加硬件配置，同时也兼容差异配置
    @API_RECORD
    def set_Docking_Info(self, id_planing_file, ne_name=None, with_common=False, wsd_cme_docking_filename="*WSD-CME Docking*"):
        if ne_name is None:
            ne_name = self.NEName

        if with_common == True:
            wsd_filename_list = search_Files(id_planing_file)
            bbp_info_map = load_Excel_File(wsd_filename_list[0], "BBP", 2, "NE_NAME")
            if ne_name not in bbp_info_map:
                ne_name = "COMMON"

        lte_bbp_list, umts_bbp_list,nr_bbp_list = self.create_BBP_From_WSD(ne_name, wsd_cme_docking_filename)
        rruchain_obj_list, rru_obj_list, rfu_obj_list, sectoreqm_obj_list, sector_obj_list= self.create_RXU_From_WSD(ne_name, id_planing_file)
        self.Rat_BBP_Cache["F"] = lte_bbp_list
        self.Rat_BBP_Cache["U"] = umts_bbp_list
        self.Rat_BBP_Cache["N"] = nr_bbp_list
        self.save_moc("RRUCHAIN", rruchain_obj_list, APPEND_MODE, with_merge=True)
        self.save_moc("RRU", rru_obj_list, APPEND_MODE, with_merge=True)
        self.save_moc("RFU", rfu_obj_list, APPEND_MODE, with_merge=True)
        self.save_moc("SECTOREQM", sectoreqm_obj_list, APPEND_MODE, with_merge=True)
        self.save_moc("SECTOR", sector_obj_list, APPEND_MODE, with_merge=True)
        return lte_bbp_list, umts_bbp_list,nr_bbp_list, rruchain_obj_list, rru_obj_list, rfu_obj_list, sectoreqm_obj_list, sector_obj_list

    @API_RECORD
    def create_RXU_From_LLD(self,ne_name,id_key_lld, rcn_list, srn_list, wsd_cme_docking_filename, **kwargs):
        if ne_name:
              ne_name = self.NEName
        rxu_spec_map = {}
        # 读取RXU规格表
        rxu_spec_list = load_Excel_File(wsd_cme_docking_filename, "CELL_RRUTYPE", 2, "NE_NAME").get(ne_name,[])
        if rxu_spec_list:
            for rxu_spec in rxu_spec_list:
                if rxu_spec["RXUSPEC"] not in rxu_spec_map:
                    rxu_spec_map[rxu_spec["RXUSPEC"]] = []
                rxu_spec_map[rxu_spec["RXUSPEC"]].append(rxu_spec)

        if len(rxu_spec_map) == 0:
            raise Exception("Error: No RXU_Spec was found in RXU Spec sheet")
        pass
        # 创建RXU
        rru_obj_list = []
        rfu_obj_list = []
        aaru_obj_list = []
        aamu_obj_list = []
        aas_obj_list = []
        rruchain_obj_list = []
        rruchain_info_map = {}
        rxu_scenario_map = {}
        # 读取RXU场景表
        cell_rrutype_cell_row_list = load_Excel_File(wsd_cme_docking_filename, "CELL_RRUTYPE", 2, group_title="NE_NAME").get(ne_name, [])
        if cell_rrutype_cell_row_list:
            for cell_rrutype_cell_row in cell_rrutype_cell_row_list:
                if cell_rrutype_cell_row["Parameter Name"] not in rxu_scenario_map:
                    rxu_scenario_map[cell_rrutype_cell_row["Parameter Name"]] = []
                rxu_scenario_map[cell_rrutype_cell_row["Parameter Name"]].append(cell_rrutype_cell_row)

        rxu_info_list = []
        for rxu_scenario in [id_key_lld]:
              if rxu_scenario not in rxu_scenario_map:
                  raise Exception("Error: RXU Scenario=%s not exist" % rxu_scenario)
              rxu_info_list.extend(rxu_scenario_map[rxu_scenario])
        for rxu_info in rxu_info_list:
            rxu_spec_str = rxu_info[u"RXUSPEC"]
            if rxu_spec_str not in rxu_spec_map:
                raise Exception("Error: RXU_SPEC=%s not exist in RXUSpec sheet. Please define" % rxu_spec)
            xTxR = rxu_spec_map[rxu_spec_str][0].attr(u"xTxR")
            rxu_specs = rxu_spec_str.split(";")
            xTxRs = xTxR.split(";")
            cpri_bbp_port1s = rxu_info[u"CPRI_BBP_PORT1"].split(";")
            if rxu_info[u"CPRI_BBP_PORT2"]:
                cpri_bbp_port2s = rxu_info[u"CPRI_BBP_PORT2"].split(";")
            else:
                cpri_bbp_port2s = []
            work_modes = rxu_info[u"WORK_MODE"].split(";")
            rxuspeces = rxu_info["RXUSPEC"].split(";")
            pses = rxu_info[u"PS"].split(";")
            protocol = rxu_info[u"PROTOCOL"].split(";")

            title = "RXU_TYPE" if "RXU_TYPE" in rxu_spec_map[rxu_spec_str][0] else "RRU_TYPE"  # Title in RXU Spec sheet
            rxu_types = rxu_spec_map[rxu_spec_str][0][title].split(";")

            max_len = min(len(rxu_specs), len(xTxRs))
            self.create_RXU_From_LLD_verify_data(wsd_cme_docking_filename, "CELL_RRUTYPE", id_key_lld,
                                                 xTxRs=xTxRs,
                                                 rxu_specs=rxu_specs,
                                                 cpri_bbp_port1s=cpri_bbp_port1s,
                                                 work_modes=cpri_bbp_port1s,
                                                 rxu_types=rxu_types,
                                                 rcn_list=rcn_list,
                                                 srn_list=srn_list)
            for i in range(max_len):
                xTxR = xTxRs[i]
                rxu_spec = rxu_specs[i]
                cpri_bbp_port1 = cpri_bbp_port1s[i]
                if len(cpri_bbp_port2s) > i:
                    cpri_bbp_port2 = cpri_bbp_port2s[i]
                else:
                    cpri_bbp_port2 = None
                work_mode = work_modes[i]
                txnum, rxnum = xTxR.split("T")
                txnum = int(txnum)
                rxnum = int(rxnum[:-1])  # 去掉尾部的R字符
                rxu_type = rxu_types[i]

                # cn, srn, sn = cn_srn_rn.split("-")
                cn = 0
                rcn = rcn_list[i]
                sn = 0
                srn = srn_list[i]
                if rcn not in rruchain_info_map:
                    rruchain_info_map[rcn] = []
                if cpri_bbp_port1 and cpri_bbp_port1 not in rruchain_info_map[rcn]:
                    rruchain_info_map[rcn].append(cpri_bbp_port1)
                if cpri_bbp_port2 and cpri_bbp_port2 not in rruchain_info_map[rcn]:
                    rruchain_info_map[rcn].append(cpri_bbp_port2)

                # 计算RRU工作制式的值
                work_mode_value = self.get_RXU_WorkMode_From_String(work_mode)
                if rxu_type[1:4] in ["RRU", "IRU"]:
                    rxu_obj = MODEL.RRU(CN=cn, SRN=srn, SN=sn, RCN=rcn, PS=pses[i], TXNUM=txnum, RXNUM=rxnum,
                                        RS=work_mode_value, RT=MODEL.RRU.RT.field(rxu_type),
                                        RUSPEC=rxuspeces[i],
                                        TP=MODEL.RRU.TP.TRUNK,
                                        ADMSTATE=MODEL.RRU.ADMSTATE.UNBLOCKED)
                    rru_obj_list.append(rxu_obj)
                elif rxu_type[1:4] in ["AMU"]:
                    rxu_obj = MODEL.AARU(CN=cn, SRN=srn, SN=sn,TXNUM=txnum, RXNUM=rxnum,
                                        RS=work_mode_value,
                                        VRETNO=(str((int(str(srn)[0]))-2))+str((sn+int(str(srn)[-1]))),
                                        ADMSTATE=MODEL.RRU.ADMSTATE.UNBLOCKED)
                    aaru_obj_list.append(rxu_obj)
                    temp=[]
                    if srn not in temp:
                        aamu_obj = MODEL.AAMU(CN=0, SRN=srn,SN=0,TP=MODEL.AAMU.TP.TRUNK,
                                            RCN=rcn,PS=pses[i])
                        aamu_obj_list.append(aamu_obj)
                        aas_obj = MODEL.AAS(CN=0, SRN=srn, AN="AAU_"+str(srn)[-1])
                        aas_obj_list.append(aas_obj)
                else:
                    rxu_obj = MODEL.RFU(CN=cn, SRN=srn, SN=sn, RCN=rcn, PS=pses[i], TXNUM=txnum, RXNUM=rxnum,
                                        RS=work_mode_value, RT=MODEL.RFU.RT.field(rxu_type),
                                        RUSPEC=rxuspeces[i],
                                        TP=MODEL.RFU.TP.TRUNK,
                                        ADMSTATE=MODEL.RFU.ADMSTATE.UNBLOCKED)
                    rfu_obj_list.append(rxu_obj)
            # 创建RRUCHAIN
            for (rcn, cpri_port_list) in rruchain_info_map.items():
                hcn, hsrn, hsn, hpn = cpri_port_list[0].split("-")
                rruchain_obj = MODEL.RRUCHAIN(RCN=int(rcn), HCN=hcn, HSRN=hsrn, HSN=hsn, HPN=hpn)

                #eCPRI配置
                rruchain_obj.PROTOCOL = protocol[i]

                if len(cpri_port_list) == 1:  # 一根光纤
                    rruchain_obj.TT = MODEL.RRUCHAIN.TT.CHAIN
                    rruchain_obj.BM = MODEL.RRUCHAIN.BM.COLD
                    rruchain_obj.AT = MODEL.RRUCHAIN.AT.LOCALPORT
                else:  # 两根光纤
                    rruchain_obj.TT = MODEL.RRUCHAIN.TT.LOADBALANCE
                    rruchain_obj.TCN, rruchain_obj.TSRN, rruchain_obj.TSN, rruchain_obj.TPN = cpri_port_list[1].split("-")
                rruchain_obj_list.append(rruchain_obj)
        return rru_obj_list,rfu_obj_list,rruchain_obj_list

    def create_RXU_From_LLD_verify_data(self, wsd_cme_docking_filename, sheet_name, id_key_lld, **kwargs):
        attr_name_map = {
            "xTxRs": "xTxR",
            "rxu_specs": "RXUSPEC",
            "cpri_bbp_port1s": "CPRI_BBP_PORT1",
            "work_modes": "WORK_MODE",
            "rxu_types": "RRU_TYPE",

        }
        sector_attr_name_map = {
            "rcn_list": "RRU Chain",
            "srn_list": "RRU Subrack"
        }
        verify_data_len_map = {}
        error_keys = []
        for verify_key, verify_data in kwargs.items():
            data_len = len(verify_data)
            verify_data_len_map[verify_key] = data_len
        max_verify_data_len = max(verify_data_len_map.values())
        for verify_key, verify_data_len in verify_data_len_map.items():
            if verify_data_len != max_verify_data_len:
                error_keys.append(verify_key)
        if error_keys:
            error_info = ""
            for error_key in error_keys:
                error_attr_key = attr_name_map.get(error_key, '')
                if error_attr_key:
                    tmp_error_info = ("The length of attribute %s of %s in the %s sheet in the %s excel file is not %s."
                                      " Please check the data.\n") % (error_attr_key, id_key_lld, sheet_name,
                                                                      wsd_cme_docking_filename, max_verify_data_len)

                else:
                    sector_attr_name = sector_attr_name_map.get(error_key, '')
                    tmp_error_info = "Check whether the fields starting with %s in the Sector table do not contain %s." % (id_key_lld ,sector_attr_name)
                error_info += tmp_error_info
            self.exit_Info(error_info)

    @API_RECORD
    def create_RRU(self,**kwargs):
        error_count = self.inner_check_para(kwargs, ["RCN", "HSN", "HPN","CN","SRN","SN","PS","RT","RN","RS","RXNUM","TXNUM"])
        if 'TT' not in kwargs:
            kwargs['TT'] = "CHAIN"
        if 'BM' not in kwargs:
            kwargs['BM'] = "COLD"
        if "AT" not in kwargs:
            kwargs["AT"] = "LOCALPORT"
        if "TP" not in kwargs:
            kwargs["TP"] = "TRUNK"
        self.add_moc("RRUCHAIN", **kwargs)
        self.add_moc("RRU", **kwargs)

    @API_RECORD
    def mod_SectorEqmId_to_LocalCellId_LTE(self,excel_file,ne_tree=None):
        id_planing_map = self.get_ID_Plan(excel_file, id_type="SECTOREQMID")
        if ne_tree:
            lte_local_cell_id_list = self.get_para_list_from_ne_tree(ne_tree, "Cell", ["LocalCellId", "FreqBand", "NbCellFlag"])
            lte_local_prb_id_list = self.get_para_list_from_ne_tree(ne_tree, "Prb", ["LocalCellId", "FreqBand"])
        else:
            lte_local_cell_id_list = self.get_para_list_from_moc("Cell", ["LocalCellId", "FreqBand", "NbCellFlag"])
            lte_local_prb_id_list = self.get_para_list_from_moc("Prb", ["LocalCellId", "FreqBand"])
        for lte_local_cell_id in lte_local_cell_id_list:
            LocalCellId = lte_local_cell_id[0]
            if lte_local_cell_id[1] is None and lte_local_cell_id[2] == 1:
                for obj in lte_local_prb_id_list:
                    if obj[0] == LocalCellId:
                        band = "MO" + str(self.get_LTE_Common_Str_From_Band(obj[1]))
            else:
                band = "LO" + str(self.get_LTE_Common_Str_From_Band(lte_local_cell_id[1]))
            Sector_To_LocalCellId_dic = self.Analyze_Cache["Band_Sector_To_LocalCellId"][band]
            for sector,localcellid_list in Sector_To_LocalCellId_dic.items():
                for i,id in enumerate(localcellid_list):
                    if id == LocalCellId:
                        sector_old = sector
                        localcellid_index = i
            SectorEqmId_list = self.Analyze_Cache["Band_Sector_To_SectorEqmId"][band][sector_old]
            SectorEqmId_orig = SectorEqmId_list[localcellid_index]
            SectorEqmId_list = sorted(set(SectorEqmId_list), key=SectorEqmId_list.index)
            if SectorEqmId_list.index(SectorEqmId_orig) > len(id_planing_map[band]["SECTOR_" + sector_old])-1:
                SectorEqmId_index = 0
            else:
                SectorEqmId_index = SectorEqmId_list.index(SectorEqmId_orig)
            SectorEqmId = int(id_planing_map[band]["SECTOR_" + sector_old][SectorEqmId_index])
            if ne_tree:
                eUCellSectorEqm_list = ne_tree["eUCellSectorEqm"]
                for eUCellSectorEqm in eUCellSectorEqm_list:
                    if eUCellSectorEqm.LocalCellId == LocalCellId:
                        eUCellSectorEqm["SectorEqmId"] = SectorEqmId
                EuPrbSectorEqm_list = ne_tree["EuPrbSectorEqm"]
                for EuPrbSectorEqm in EuPrbSectorEqm_list:
                    if EuPrbSectorEqm.LocalCellId == LocalCellId:
                        EuPrbSectorEqm["SectorEqmId"] = SectorEqmId
            else:
                self.mod_moc("eUCellSectorEqm", MOD(SectorEqmId=SectorEqmId).WHERE(LocalCellId=LocalCellId))
                self.mod_moc("EuPrbSectorEqm", MOD(SectorEqmId=SectorEqmId).WHERE(LocalCellId=LocalCellId))

    @API_RECORD
    def mod_SectorEqmId_to_ULOCELLID_UMTS(self,excel_file,ne_tree=None,with_averge=False):
        id_planing_map = self.get_ID_Plan(excel_file, id_type="SECTOREQMID")
        if ne_tree:
            umts_local_cell_id_list = self.get_para_list_from_ne_tree(ne_tree, "ULOCELL", ["ULOCELLID", "DLFREQ"])
        else:
            umts_local_cell_id_list = self.get_para_list_from_moc("ULOCELL", ["ULOCELLID", "DLFREQ"])
        for umts_local_cell_id in umts_local_cell_id_list:
            ULOCELLID = umts_local_cell_id[0]
            band = "UO" + str(self.get_UMTS_Common_Str_From_Dlfreq(int(umts_local_cell_id[1])))
            Sector_To_ULOCELLID_dic = self.Analyze_Cache["Band_Sector_To_ULOCELLID"][band]
            for sector,ulocellid_list in Sector_To_ULOCELLID_dic.items():
                for i,id in enumerate(ulocellid_list):
                    if id == ULOCELLID:
                        sector_old = sector
                        ulocellid_index = i
            SectorEqmId_list = self.Analyze_Cache["Band_Sector_To_SectorEqmId"][band][sector_old]
            id_planing_band_sector_list = id_planing_map[band]["SECTOR_" + sector_old]
            if with_averge and abs(len(SectorEqmId_list)-2*SectorEqmId_list.count(SectorEqmId_list[ulocellid_index]))>1 and len(id_planing_band_sector_list)==2:
                SectorEqmId_index = ulocellid_index % 2
            else:
                SectorEqmId_orig = SectorEqmId_list[ulocellid_index]
                SectorEqmId_list = sorted(set(SectorEqmId_list), key=SectorEqmId_list.index)
                SectorEqmId_index = SectorEqmId_list.index(SectorEqmId_orig)
            SectorEqmId = int(id_planing_band_sector_list[SectorEqmId_index])
            if ne_tree:
                ULOCELLSECTOREQM_list = ne_tree["ULOCELLSECTOREQM"]
                for ULOCELLSECTOREQM in ULOCELLSECTOREQM_list:
                    if ULOCELLSECTOREQM.ULOCELLID == ULOCELLID:
                        ULOCELLSECTOREQM["SECTOREQMID"] = SectorEqmId
            else:
                self.mod_moc("ULOCELLSECTOREQM", MOD(SECTOREQMID=SectorEqmId).WHERE(ULOCELLID=ULOCELLID))

    @API_RECORD
    def mod_SectorEqmId_to_GtrxGroupId_GSM(self,excel_file,ne_tree=None):
        id_planing_map = self.get_ID_Plan(excel_file, id_type="SECTOREQMID")
        if ne_tree:
            gsm_gtrxgroup_id_list = self.get_para_list_from_ne_tree(ne_tree, "GTRXGROUP", ["GTRXGROUPID", "GLOCELLID"])
        else:
            gsm_gtrxgroup_id_list = self.get_para_list_from_moc("GTRXGROUP", ["GTRXGROUPID", "GLOCELLID"])
        for gsm_gtrxgroup_id in gsm_gtrxgroup_id_list:
            gtrxgroupid = gsm_gtrxgroup_id[0]
            for gsm_band,Sector_GtrxGroupId in self.Analyze_Cache["Band_Sector_To_GtrxGroupId"].items():
                for sector,GtrxGroupId_list in Sector_GtrxGroupId.items():
                    if gtrxgroupid in GtrxGroupId_list:
                        band = gsm_band
            Sector_To_GtrxGroupId_dic = self.Analyze_Cache["Band_Sector_To_GtrxGroupId"][band]
            for sector,gtrxgroupid_list in Sector_To_GtrxGroupId_dic.items():
                for i,id in enumerate(gtrxgroupid_list):
                    if id == gtrxgroupid:
                        sector_old = sector
                        gtrxgroupId_index = i
            SectorEqmId_list = self.Analyze_Cache["Band_Sector_To_SectorEqmId"][band][sector_old]
            SectorEqmId_orig = SectorEqmId_list[gtrxgroupId_index]
            SectorEqmId_list = sorted(set(SectorEqmId_list), key=SectorEqmId_list.index)
            if SectorEqmId_list.index(SectorEqmId_orig) > len(id_planing_map[band]["SECTOR_" + sector_old])-1:
                SectorEqmId_index = 0
            else:
                SectorEqmId_index = SectorEqmId_list.index(SectorEqmId_orig)
            SectorEqmId = int(id_planing_map[band]["SECTOR_" + sector_old][SectorEqmId_index])
            if ne_tree:
                GtrxGroupSectorEqm_list = ne_tree["GTRXGROUPSECTOREQM"]
                for GtrxGroupSectorEqm in GtrxGroupSectorEqm_list:
                    if GtrxGroupSectorEqm.GTRXGROUPID == gtrxgroupid:
                        GtrxGroupSectorEqm["SECTOREQMID"] = SectorEqmId
            else:
                self.mod_moc("GTRXGROUPSECTOREQM", MOD(SECTOREQMID=SectorEqmId).WHERE(GTRXGROUPID=gsm_gtrxgroup_id))

    @API_RECORD
    def get_UMTS_Common_Str_From_Dlfreq(self, dlfreq):
        if 10562 <= dlfreq <= 10838:
            return "2100"
        elif 9662 <= dlfreq <= 9938 or dlfreq in [412, 437, 462, 487, 512, 537, 562, 587, 612, 637, 662, 687]:
            return "1900"
        elif 1162 <= dlfreq <= 1513:
            return "1800"
        elif 1537 <= dlfreq <= 1738 or dlfreq in [1887, 1912, 1937, 1962, 1987, 2012, 2037, 2062, 2087]:
            return "1700"
        elif 4357 <= dlfreq <= 4458 or dlfreq in [1007, 1012, 1032, 1037, 1062, 1087]:
            return "850"
        elif 4387 <= dlfreq <= 4413 or dlfreq in [1037, 1062]:
            return "800"
        elif 2237 <= dlfreq <= 2563 or dlfreq in [2587, 2612, 2637, 2662, 2687, 2712, 2737, 2762, 2787, 2812, 2837, 2862, 2887, 2912]:
            return "2600"
        elif 2937 <= dlfreq <= 3088:
            return "900"
        elif 9237 <= dlfreq <= 9387:
            return "1700"
        else:
            return None

    @API_RECORD
    def get_LTE_Common_Str_From_Band(self, band):
        lteband_map = {1: "2100", 2: "1900", 3: "1800", 4: "AWS", 5: "850", 6: "800", 7: "2600", 8: "900", 9: "1700",
                       10: "", 11: "", 12: "", 13: "", 14: "", 17: "", 18: "", 19: "", 20: "800", 28: "700",
                       33: "", 34: "", 35: "", 36: "", 37: "", 38: "2600", 39: "1900", 40: "2300", 41: "2600",
                       42: "3500",
                       43: "3600", 64: "2600"}
        if band in lteband_map.keys():
            return lteband_map[band]
        else:
            return None

    @API_RECORD
    def get_LTE_Common_FreqBand_From_DlEarfcn(self, DlEarfcn):
        DlEarfcn_FreqBand_map = {"0-599":1,"600-1199":2,"1200-1949":3,"1950-2399":4,"2400-2649":5,"2650-2749":6,"2750-3449":7,
                                 "3450-3799":8,"3800-4149":9,"4150-4749":10,"4750-4949":11,"5000-5179":12,"5180-5279":13,"5280-5379":14,
                                 "5730-5849":17,"5850-5999":18,"6000-6149":19,"6150-6449":20,"7050-7199":21,"9210-9659":28,"36000-36199":33,"36200-36349":34,
                                 "36350-36949":35,"36950-37549":36,"37550-37749":37,"37750-38249":38,"38250-38649":39,"38650-39649":40,"39650-41589":41}
        FreqBand = None
        for DlEarfcn_range in DlEarfcn_FreqBand_map:
            DlEarfcn_start,DlEarfcn_end = DlEarfcn_range.split("-")
            if int(DlEarfcn_start)<=int(DlEarfcn)<=int(DlEarfcn_end):
                FreqBand = DlEarfcn_FreqBand_map[DlEarfcn_range]
                break
        return FreqBand

    @API_RECORD
    def get_PhysicalSectorFromIDPlan(self, sectoreqmid, idplanexcel_file="*WSD-CME Docking Form*" ):
        idplandata = self.get_ID_Plan(idplanexcel_file, "SECTOREQMID")
        # for key, item in idplandata:
        for key in idplandata.keys():
            item = idplandata[key]
            # for sector, datalist in item:
            for sector in item.keys():
                datalist=item[sector]
                if int(sectoreqmid) in [int(x )for x in datalist]:
                    return key, sector
        return "", ""

    @API_RECORD
    def create_NodeMultiGrp(self, dict, type):
        for item in dict.values():
            mutilegrpid = self.get_free_id_list("NODEBMULTICELLGRP","MULTICELLGRPID")[0]
            ULOCELLREF_List = [MODEL.NODEBMULTICELLGRP.ULOCELLREF(ULOCELLID=x) for x in item]
            self.add_moc("NODEBMULTICELLGRP",MULTICELLGRPID=mutilegrpid,MULTICELLGRPTYPE=type,ULOCELLREF=ULOCELLREF_List)
        pass


    # 读取WSD的设计数据(Excel/Json)，创建BBP和MPT主控板. 生成的moc数据直接提交，没有返回值
    # API_Create_RXU_WSD("Site1")
    @API_RECORD
    def create_BBP_From_WSD(self, ne_name, wsd_cme_docking_filename="*WSD-CME Docking*",with_clear=True):
        if with_clear is True:
            moc_hardware_del_list = ["MPT", "BBP", "BRI", "UEIU", "BBUFAN", "PEU", "RRU", "RFU"]
            for moc_hardware_del in moc_hardware_del_list:
                self.del_moc(moc_hardware_del)
        wsd_filename_list = search_Files(wsd_cme_docking_filename)
        if len(wsd_filename_list) == 0:
            json = load_WSD_File(ne_name)
            bbp_info_list = []
            for tmp in json.bbpInfos:
                if tmp.nEName == ne_name:
                    row = ExcelRow()
                    row["NE_NAME"] = tmp.nEName
                    row["BBU_TYPE"] = tmp.bbuType
                    row["CN-SRN"] = tmp.bbuSubrackNo
                    total_sn_list = [0, 1, 2, 3, 4, 5, 6, 7, 16, 18, 19]
                    for bbpinfo in tmp.bbpBoardInfos:
                        sn = int(bbpinfo.slot)
                        row["SLOT%d" % sn] = bbpinfo.targetBbp
                        row["SLOT%d_Orgin" % sn] = bbpinfo.originBbp
                        total_sn_list.remove(sn)
                    for sn in total_sn_list:
                        row["SLOT%d" % sn] = None
                        row["SLOT%d_Orgin" % sn] = None
                    bbp_info_list.append(row)
        else:
            bbp_info_map = load_Excel_File(wsd_filename_list[0], "BBP", 2, "NE_NAME")
            if ne_name not in bbp_info_map:
                self.exit_Info("Error: No BBP was found for BTS=%s in WSD-CME Docking file" % ne_name)
            bbp_info_list = bbp_info_map[ne_name]
        umts_bbp_list = []
        lte_bbp_list = []
        nr_bbp_list = []
        for bbp_info in bbp_info_list:
            cn, srn = bbp_info.attr("CN-SRN").split("-")
            cn, srn = int(cn), int(srn)
            for sn in range(8):
                bbp_str = bbp_info.attr("SLOT%d" % sn)
                if bbp_str is None: continue
                if "_" in bbp_str:
                    bbp_brd, rat = bbp_str.rsplit("_", 1)
                else:
                    bbp_brd, rat = bbp_str, ""

                if bbp_brd[1:4] == "MPT":  # Create MPT Board  UMPT/LMPT/WMPT
                    bbp_obj = MODEL.MPT(CN=cn, SRN=srn, SN=sn, TYPE=bbp_brd[:4])
                    self.save_moc("MPT", [bbp_obj], APPEND_MODE, with_merge=True)
                elif bbp_brd[1:4] == "BRI":  # Create UBRI
                    bbp_obj = MODEL.BRI(CN=cn, SRN=srn, SN=sn, TYPE=bbp_brd[:4])
                    self.save_moc("BRI", [bbp_obj], APPEND_MODE, with_merge=True)
                else:
                    if "F" in rat or 'L' in rat or "T" in rat:
                        lte_bbp_list.append((bbp_brd[:4], int(cn), int(srn), int(sn)))
                    if "U" in rat:
                        umts_bbp_list.append((bbp_brd[:4], int(cn), int(srn), int(sn)))
                    if "N" in rat:
                        nr_bbp_list.append((bbp_brd[:4], int(cn), int(srn), int(sn)))
                    self.create_One_BBP(cn, srn, sn, bbp_brd, rat)
                self.print_msg("Info: Create %s: slot=%d, %s" % (bbp_brd, sn, rat))
            for slot in [16]:
                slot_str = "SLOT%d" % slot
                if slot_str not in bbp_info: continue
                if bbp_info[slot_str] is None: continue
                brd = bbp_info[slot_str]
                if brd[:3] == "FAN":
                    fan_obj = MODEL.BBUFAN(CN=cn, SRN=srn, SN=slot)
                    self.save_moc("BBUFAN", [fan_obj], APPEND_MODE, with_merge=True)
                    self.print_msg("Info: Create %s: slot=%d" % (brd[:3],slot))

            for slot in [18, 19]:
                slot_str = "SLOT%d" % slot
                if slot_str not in bbp_info: continue
                if bbp_info[slot_str] is None: continue
                brd = bbp_info[slot_str]
                if brd[:4] == "UPEU":
                    peu_obj = MODEL.PEU(CN=cn, SRN=srn, SN=slot)
                    self.save_moc("PEU", [peu_obj], APPEND_MODE, with_merge=True)
                if brd[:4] == "UEIU":
                    ueiu_obj = MODEL.UEIU(CN=cn, SRN=srn, SN=slot)
                    self.save_moc("UEIU", [ueiu_obj], APPEND_MODE, with_merge=True)
            # 创建机柜
            subrack_type = bbp_info["BBU_TYPE"]
            obj = MODEL.SUBRACK(CN=cn, SRN=srn, TYPE=MODEL.SUBRACK.TYPE.fromString(subrack_type), DESC="")
            self.save_moc("SUBRACK", [obj], APPEND_MODE, with_merge=True)
        return lte_bbp_list, umts_bbp_list, nr_bbp_list

    ###########################################################################
    # Create RRU/RFU, RRUCHAIN, SECTOREQM, Sector
    # Please refer to: http://3ms.huawei.com/hi/group/2030315/thread_6898423.html?mapId=8589265
    # Usage:
    #  rxu_scenario_list = ["Tsel_900", "Tsel_1800_4T4R", "Tsel_2100"]
    #  rxu_info_list = API_Get_RXU_Info_By_Scenario(site_list_filename, rxu_scenario_list)
    #  rruchain_obj_list, rru_obj_list, rfu_obj_list, sectoreqm_obj_list, sector_obj_list = API_Create_RXU(site_list_filename, rxu_info_list)
    @API_RECORD
    def create_RXU(self, excel_file, rxu_info_list):
        # 读取端口分配模式表
        port_assign_mode_map = load_Excel_File(excel_file, "Ant Port Assign Mode", 2, "PORT_ASSIGN_MODE_NAME")
        if len(port_assign_mode_map) == 0:
            raise Exception("Error: No Port_Assign_Mode was found in Ant_Port_Assign_Mode sheet")
        # 读取RXU规格表
        rxu_spec_map = load_Excel_File(excel_file, "RXU Spec", 2, "RXUSPEC")
        if len(rxu_spec_map) == 0:
            raise Exception("Error: No RXU_Spec was found in RXU Spec sheet")

        # 读取并获得SECTOREQMID的规划表
        sectoreqmid_plan_map = self.get_ID_Plan(excel_file, "SECTOREQMID")

        # 创建扇区设备对象
        sectoreqm_obj_list = []
        rxu_interconnectino_sector_band_map = {}  # 记录射频互连的RXU对应关系
        for rxu_info in rxu_info_list:
            if "SECTOR_NO" not in rxu_info: continue  # 对于没有扇区的RXU，不生成扇区设备

            sector = rxu_info[u"SECTOR_NO"]
            band = rxu_info[u"BAND"]
            work_mode = rxu_info[u"WORK_MODE"]
            assign_mode = rxu_info[u"PORT_ASSIGN_MODE"]

            if "&" in sector:  # RRU用于两个扇区，如扇区劈裂
                sector1, sector2 = sector.split("&")
                mode1, mode2 = work_mode.split("&")
                assign1, assign2 = assign_mode.split("&")
                self.inner_create_sectoreqm(sectoreqm_obj_list, sectoreqmid_plan_map, excel_file, sector1, band, mode1,
                                       assign1,
                                       [rxu_info])
                self.inner_create_sectoreqm(sectoreqm_obj_list, sectoreqmid_plan_map, excel_file, sector2, band, mode2,
                                       assign2,
                                       [rxu_info])
            elif "&" in band:  # RRU支持两个频段
                band1, band2 = band.split("&")
                mode1, mode2 = work_mode.split("&")
                assign1, assign2 = assign_mode.split("&")
                self.inner_create_sectoreqm(sectoreqm_obj_list, sectoreqmid_plan_map, excel_file, sector, band1, mode1,
                                       assign1,
                                       [rxu_info])
                self.inner_create_sectoreqm(sectoreqm_obj_list, sectoreqmid_plan_map, excel_file, sector, band2, mode2,
                                       assign2,
                                       [rxu_info])
            else:
                ##判断是否为两个RXU射频互连,双拼
                if assign_mode not in port_assign_mode_map:
                    raise Exception("Error: Port_Assign_Mode=%s not exist" % assign_mode)
                assign_info = port_assign_mode_map[assign_mode][0]

                tmp_str = ""
                for name in ["GSM", "UMTS", "LTE", "NB", "5G"]:
                    rat_title = "%s_PORT_ASSIGN" % name
                    if hasattr(assign_info, rat_title) and assign_info.attr(rat_title):
                        tmp_str += assign_info.attr(rat_title)

                if "a" in tmp_str or "b" in tmp_str:  # 如果在端口分配模式中，存在小写的a,b(即第二个RXU的端口)，在认为是射频互连
                    if sector not in rxu_interconnectino_sector_band_map:
                        rxu_interconnectino_sector_band_map[sector] = {}
                    if band not in rxu_interconnectino_sector_band_map[sector]:
                        rxu_interconnectino_sector_band_map[sector][band] = []
                    rxu_interconnectino_sector_band_map[sector][band].append(rxu_info)
                else:
                   self.inner_create_sectoreqm(sectoreqm_obj_list, sectoreqmid_plan_map, excel_file, sector, band,
                                           work_mode,
                                           assign_mode, [rxu_info])

        # 为射频互连的RXU创建扇区设备对象
        for (sector, rxu_band_map) in rxu_interconnectino_sector_band_map.items():
            for (band, tmp_rxu_info_list) in rxu_band_map.items():
                mode = tmp_rxu_info_list[0]["WORK_MODE"]
                assign = tmp_rxu_info_list[0]["PORT_ASSIGN_MODE"]
                while len(tmp_rxu_info_list) > 0:
                    rxu_info = tmp_rxu_info_list.pop(0)
                    if len(tmp_rxu_info_list) == 0:
                        self.inner_create_sectoreqm(sectoreqm_obj_list, sectoreqmid_plan_map, excel_file, sector, band, mode,
                                               assign, [rxu_info])
                    else:
                        rxu_info2 = tmp_rxu_info_list.pop(0)
                        self.inner_create_sectoreqm(sectoreqm_obj_list, sectoreqmid_plan_map, excel_file, sector, band, mode,
                                               assign, [rxu_info, rxu_info2])
                        if "G" in mode:  # 含G的制式才互联，UMTS/LTE双拼，不需要配置射频互连
                            rxu_info["inter_connect_rxu"] = rxu_info2
                            rxu_info2["inter_connect_rxu"] = rxu_info
            pass

        # 创建RXU
        rru_obj_list = []
        rfu_obj_list = []
        rruchain_info_map = {}
        for rxu_info in rxu_info_list:
            if "RXU_TYPE" not in rxu_info:  # from RXU Name(such as RRU3953) to get RXU_TYPE(such as MRRU) and TX_NUM, RX_NUM
                rxu_spec = rxu_info[u"RXUSPEC"]
                if rxu_spec not in rxu_spec_map:
                    raise Exception("Error: RXU_SPEC=%s not exist in RXUSpec sheet. Please define" % rxu_spec)
                xTxR = rxu_spec_map[rxu_spec][0].attr(u"xTxR")
                txnum, rxnum = xTxR.split("T")
                if int(txnum) > 8:  # 发射端口大于8，只支持BEAM，设置发射端口号为0
                    txnum, rxnum = 0, 0
                else:
                    txnum = int(txnum)
                    rxnum = int(rxnum[:-1])  # 去掉尾部的R字符

                title = "RXU_TYPE" if "RXU_TYPE" in rxu_spec_map[rxu_spec][0] else "RRU_TYPE"  # Title in RXU Spec sheet
                rxu_type = rxu_spec_map[rxu_spec][0][title]
            else:
                rxu_type = rxu_info["RXU_TYPE"]
                txnum, rxnum = rxu_info["TX_RX_NUM"]

            rcn = int(rxu_info[u"RCN"])
            if rcn not in rruchain_info_map:
                rruchain_info_map[rcn] = []
            if rxu_info[u"CPRI_BBP_PORT1"] and rxu_info[u"CPRI_BBP_PORT1"] not in rruchain_info_map[rcn]:
                rruchain_info_map[rcn].append(rxu_info[u"CPRI_BBP_PORT1"])
            if rxu_info[u"CPRI_BBP_PORT2"] and rxu_info[u"CPRI_BBP_PORT2"] not in rruchain_info_map[rcn]:
                rruchain_info_map[rcn].append(rxu_info[u"CPRI_BBP_PORT2"])

            # 计算RRU工作制式的值
            work_mode = rxu_info[u"WORK_MODE"]
            work_mode_value = self.get_RXU_WorkMode_From_String(work_mode)

            cn, srn, sn = self.inner_get_cn_srn_sn_from_rxu_info(rxu_info)
            if rxu_type[1:4] in ["RRU", "IRU"]:
                rxu_obj = MODEL.RRU(CN=cn, SRN=srn, SN=sn, RCN=rcn, PS=rxu_info[u"PS"], TXNUM=txnum, RXNUM=rxnum,
                                    RS=work_mode_value, RT=MODEL.RRU.RT.field(rxu_type),
                                    RUSPEC=rxu_info["RXUSPEC"],
                                    TP=MODEL.RRU.TP.TRUNK,
                                    ADMSTATE=MODEL.RRU.ADMSTATE.UNBLOCKED)
                rru_obj_list.append(rxu_obj)
            else:
                rxu_obj = MODEL.RFU(CN=cn, SRN=srn, SN=sn, RCN=rcn, PS=rxu_info[u"PS"], TXNUM=txnum, RXNUM=rxnum,
                                    RS=work_mode_value, RT=MODEL.RFU.RT.field(rxu_type),
                                    RUSPEC=rxu_info["RXUSPEC"],
                                    TP=MODEL.RFU.TP.TRUNK,
                                    ADMSTATE=MODEL.RFU.ADMSTATE.UNBLOCKED)
                rfu_obj_list.append(rxu_obj)
            # 配置射频互连
            if "inter_connect_rxu" in rxu_info:
                cn, srn, sn =self.inner_get_cn_srn_sn_from_rxu_info(rxu_info["inter_connect_rxu"])
                rxu_obj.RFCONNTYPE = MODEL.RRU.RFCONNTYPE.INTRA_SYS_INTERCONN
                rxu_obj.RFCONNCN2 = cn
                rxu_obj.RFCONNSRN2 = srn
                rxu_obj.RFCONNSN2 = sn

            # 设置VSWR告警门限
            rxu_obj.ALMPROCSW = MODEL.RFU.ALMPROCSW.ON
            rxu_obj.ALMTHRHLD = 15 if "VSWR_THD_LV1" not in rxu_info else rxu_info["VSWR_THD_LV1"]
            rxu_obj.ALMPROCTHRHLD = 18 if "VSWR_THD_LV2" not in rxu_info else rxu_info["VSWR_THD_LV2"]

            # RXU用于UMTS且频段为850/900时，设置RXU带宽为4.2M
            if "U" in work_mode:
                if "900" in rxu_info[u"BAND"]:
                    rxu_obj.FMBWH = MODEL.RFU.FMBWH.field("4200")
                elif "850" in rxu_info[u"BAND"]:
                    rxu_obj.FMBWH = MODEL.RFU.FMBWH.field("4200")
                else:
                    pass

            # 增加辅助信息
            if "SECTOR_NO" in rxu_info:
                rxu_obj.info_sector = rxu_info[u"SECTOR_NO"]
                rxu_obj.info_band = rxu_info[u"BAND"]
            pass

        # 创建RRUCHAIN
        rruchain_obj_list = []
        for (rcn, cpri_port_list) in rruchain_info_map.items():
            hcn, hsrn, hsn, hpn = cpri_port_list[0].split("-")
            rruchain_obj = MODEL.RRUCHAIN(RCN=int(rcn), HCN=hcn, HSRN=hsrn, HSN=hsn, HPN=hpn)

            if len(cpri_port_list) == 1:  # 一根光纤
                rruchain_obj.TT = MODEL.RRUCHAIN.TT.CHAIN
                rruchain_obj.BM = MODEL.RRUCHAIN.BM.COLD
                rruchain_obj.AT = MODEL.RRUCHAIN.AT.LOCALPORT
            else:  # 两根光纤
                rruchain_obj.TT = MODEL.RRUCHAIN.TT.LOADBALANCE
                rruchain_obj.TCN, rruchain_obj.TSRN, rruchain_obj.TSN, rruchain_obj.TPN = cpri_port_list[1].split("-")
            rruchain_obj_list.append(rruchain_obj)

        # 根据扇区设备对象，创建扇区对象
        sector_obj_list = self.inner_create_sector_by_sectoreqm(sectoreqm_obj_list)

        return rruchain_obj_list, rru_obj_list, rfu_obj_list, sectoreqm_obj_list, sector_obj_list

    # Get RXU Info list by Scenario Name which in Excel file sheet=RXU Scenario
    @API_RECORD
    def get_RXU_Info_By_Scenario(self, excel_file, rxu_scenario_list, title):
        # 读取RXU场景表
        rxu_scenario_map = load_Excel_File(excel_file, "RXU Scenario", 2, title)
        if len(rxu_scenario_map) == 0:
            raise Exception("Error: No RXU Scenario was found in RXU Scenario sheet")

        rxu_info_list = []
        for rxu_scenario in rxu_scenario_list:
            if rxu_scenario not in rxu_scenario_map:
                raise Exception("Error: RXU Scenario=%s not exist" % rxu_scenario)
            rxu_info_list.extend(rxu_scenario_map[rxu_scenario])

        return copy.deepcopy(rxu_info_list)

    # Get RXU Info from BTS XML File
    @API_RECORD
    def get_TRX_Info(self, ne_name):
        rxu_info_map = {}
        for mo in ["RRU", "RFU"]:
            rxu_obj_list = self.get_data_from_ref(ne_name, mo)
            for rxu_obj in rxu_obj_list:
                cn, srn, sn = rxu_obj.CN, rxu_obj.SRN, rxu_obj.SN
                if (cn, srn, sn) not in rxu_info_map:
                    rxu_info_map[(cn, srn, sn)] = {}

                rxu_info_map[(cn, srn, sn)]["CN-SRN-SN"] = "%d-%d-%d" % (cn, srn, sn)
                rxu_info_map[(cn, srn, sn)]["RXU_TYPE"] = rxu_obj._type_.RT.toString(rxu_obj.RT)
                rxu_info_map[(cn, srn, sn)]["TX_RX_NUM"] = (rxu_obj.TXNUM, rxu_obj.RXNUM)
                rxu_info_map[(cn, srn, sn)]["RCN"] = rxu_obj.RCN
                rxu_info_map[(cn, srn, sn)]["PS"] = rxu_obj.PS

                work_mode = rxu_obj._type_.RS.toString(rxu_obj.RS)  # 工作模式
                rxu_info_map[(cn, srn, sn)]["WORK_MODE"] = work_mode.replace("O", "")  # 去掉O

                # 找到CPRI的位置
                rcn_obj = self.get_data_from_ref(ne_name, "RRUCHAIN", WHERE(RCN=rxu_obj.RCN))[0]
                rxu_info_map[(cn, srn, sn)]["CPRI_BBP_PORT1"] = "%d-%d-%d-%d" % (
                rcn_obj.HCN, rcn_obj.HSRN, rcn_obj.HSN, rcn_obj.HPN)
                if rcn_obj.TT in [1, 2]:  # 1: RING, 2:LOADBALANCE
                    rxu_info_map[(cn, srn, sn)]["CPRI_BBP_PORT2"] = "%d-%d-%d-%d" % (
                    rcn_obj.TCN, rcn_obj.TSRN, rcn_obj.TSN, rcn_obj.TPN)
                else:
                    rxu_info_map[(cn, srn, sn)]["CPRI_BBP_PORT2"] = None

                # 为了打印，补充临时字段
                rxu_info_map[(cn, srn, sn)]["SECTOR_NO"] = None
                rxu_info_map[(cn, srn, sn)]["BAND"] = None
                rxu_info_map[(cn, srn, sn)]["PORT_ASSIGN_MODE"] = ""
            pass

        # 读取扇区设备数据？
        sectoreqm_obj_list = self.get_data_from_ref(ne_name, "SECTOREQM")
        for sectoreqm_obj in sectoreqm_obj_list:
            sectorid = sectoreqm_obj.SECTORID
            sectoreqmid = sectoreqm_obj.SECTOREQMID
            ant_mode = sectoreqm_obj.ANTCFGMODE
            if ant_mode == 0:  # ANTENNAPORT
                for ant_obj in sectoreqm_obj.SECTOREQMANTENNA:
                    cn, srn, sn, antn, anttype, txbkpmode = ant_obj.CN, ant_obj.SRN, ant_obj.SN, ant_obj.ANTN, ant_obj.ANTTYPE, ant_obj.TXBKPMODE

                    pass
            elif ant_mode == 1:  # BEAM
                cn, srn, sn = sectoreqm_obj.RRUCN, sectoreqm_obj.RRUSRN, sectoreqm_obj.RRUSN
                beam_shape = sectoreqm_obj._type_.BEAMSHAPE.toString(sectoreqm_obj.BEAMSHAPE)
                beam_layer_split = sectoreqm_obj._type_.BEAMLAYERSPLIT.toString(sectoreqm_obj.BEAMLAYERSPLIT)
                beam_azimuth = sectoreqm_obj._type_.BEAMAZIMUTHOFFSET.toString(sectoreqm_obj.BEAMAZIMUTHOFFSET)
                self.print_msg("BEAM:" + beam_shape + beam_layer_split +  beam_azimuth)
                ant_mode_name = "BEAM(%s,%s,%s)" % (beam_shape, beam_layer_split, beam_layer_split)
                rxu_info_map[(cn, srn, sn)]["PORT_ASSIGN_MODE"] += ant_mode_name
        return rxu_info_map

    @API_RECORD
    def create_BBP_by_FormalFile(self, ne_name, filename):
        bbp_info_map = load_Excel_File(filename, "BBP", 2, "NE_NAME")
        if ne_name not in bbp_info_map:
            self.exit_Info("Error: No BBP was found for BTS=%s in WSD-CME Docking file" % ne_name)
        bbp_info_list = bbp_info_map[ne_name]
        umts_bbp_list = []
        lte_bbp_list = []
        for bbp_info in bbp_info_list:
            cn, srn = bbp_info.attr("CN-SRN").split("-")
            cn, srn = int(cn), int(srn)
            for sn in range(8):
                bbp_str = bbp_info.attr("SLOT%d" % sn)
                if bbp_str is None: continue
                if "_" in bbp_str:
                    bbp_brd, rat = bbp_str.rsplit("_", 1)
                else:
                    bbp_brd, rat = bbp_str, ""

                if bbp_brd[1:4] == "MPT":  # Create MPT Board  UMPT/LMPT/WMPT
                    bbp_obj = MODEL.MPT(CN=cn, SRN=srn, SN=sn, TYPE=bbp_brd[:4])
                    self.save_moc("MPT", [bbp_obj], APPEND_MODE, with_merge=True)
                else:
                    if rat in ["F"]:
                        lte_bbp_list.append(int(sn))
                    else:
                        umts_bbp_list.append(int(sn))
                    self.create_One_BBP(cn, srn, sn, bbp_brd, rat)
                self.print_msg("Info: Create %s: slot=%d, %s" % (bbp_brd, sn, rat))
            for slot in [18, 19]:
                slot_str = "SLOT%d" % slot
                if slot_str not in bbp_info: continue
                if bbp_info[slot_str] is None: continue
                brd = bbp_info[slot_str]
                if brd[:4] == "UPEU":
                    peu_obj = MODEL.PEU(CN=cn, SRN=srn, SN=slot)
                    self.save_moc("PEU", [peu_obj], APPEND_MODE, with_merge=True)
                if brd[:4] == "UEIU":
                    ueiu_obj = MODEL.UEIU(CN=cn, SRN=srn, SN=slot)
                    self.save_moc("UEIU", [ueiu_obj], APPEND_MODE, with_merge=True)
            # 创建机柜
            subrack_type = bbp_info["BBU_TYPE"]
            obj = MODEL.SUBRACK(CN=cn, SRN=srn, TYPE=MODEL.SUBRACK.TYPE.fromString(subrack_type), DESC="")
            self.save_moc("SUBRACK", [obj], APPEND_MODE, with_merge=True)

        return lte_bbp_list, umts_bbp_list

    # Print RXU Info
    @API_RECORD
    def get_RXU_Info(self, rxu_info_list):
        band_rxu_info_map = {}
        for rxu_info in rxu_info_list:
            band = rxu_info["BAND"] if "BAND" in rxu_info else "Unknown"
            if band not in band_rxu_info_map:
                band_rxu_info_map[band] = []
            band_rxu_info_map[band].append(rxu_info)

        # 打印标题
        print(
        "SECTOR_NO	BAND	RXUSPEC	CN-SRN-SN	WORK_MODE	PORT_ASSIGN_MODE	RCN	CPRI_BBP_PORT1	CPRI_BBP_PORT2	PS TRX_NUM")

        # 按照扇区顺序排序
        @API_RECORD
        def cmp_fun(a):
            if "SECTOR_NO" not in a: return -1
            return ord(a["SECTOR_NO"])

        for (band, band_rxu_info_list) in band_rxu_info_map.items():
            band_rxu_info_list.sort(key=cmp_fun)  # 按照扇区排序
            for rxu_info in band_rxu_info_list:
                rxuspec = rxu_info["RXUSPEC"] if "RXUSPEC" in rxu_info else rxu_info["RXUTYPE"]
                trx_num = rxu_info["TRX_NUM"] if "TRX_NUM" in rxu_info else ""
                sector = rxu_info["SECTOR_NO"] if "SECTOR_NO" in rxu_info else "Unknown"
                print(sector, band, rxuspec, rxu_info["CN-SRN-SN"],
                      rxu_info["WORK_MODE"], rxu_info["PORT_ASSIGN_MODE"], rxu_info["RCN"], rxu_info["CPRI_BBP_PORT1"],
                      rxu_info["CPRI_BBP_PORT2"],
                      rxu_info["PS"], trx_num)
        pass

    ##########################################################################################################
    # Below is inner function for below API
    #
    # port_assign_mode: 端口分配模式，如 ABTABR, ABTABCDR, BEAM(SEC_120DEG,OUTER_LAYER)等
    # rxu_list: RRU/RFU对象列表
    def inner_create_one_sectoreqm(self, sectoreqmid, sectorid, port_assign_mode, rxu_list):
        sectoreqmid = int(sectoreqmid)
        sectorid = int(sectorid)
        port_assign_modes = port_assign_mode.split(";")
        ant_list = []
        for i, port_assign_mode in enumerate(port_assign_modes):
            if "BEAM" in port_assign_mode:
                port_assign_list = port_assign_mode[port_assign_mode.find("(") + 1: -1].split(",")
                if len(port_assign_list) == 2:
                    shape, split = port_assign_list
                    offset = split
                elif len(port_assign_list) == 3:
                    shape, split, offset = port_assign_list
                else:
                    raise ValueError("The Beam parameter under port_assign_mode in the Sector standard Conso table is incorrectly added. Please modify it.")

                shape = shape.strip()  # 输入为字符串，如何转化为参数值？
                split = split.strip()
                offset = offset.strip()
                cn, srn, sn = self.inner_get_cn_srn_sn_from_rxu_info(rxu_list[i])
                sectoreqm_obj = MODEL.SECTOREQM(SECTOREQMID=sectoreqmid,
                                                SECTORID=sectorid,
                                                ANTCFGMODE=MODEL.SECTOREQM.ANTCFGMODE.BEAM,
                                                RRUCN=cn,
                                                RRUSRN=srn,
                                                RRUSN=sn,
                                                BEAMSHAPE=MODEL.SECTOREQM.BEAMSHAPE.field(shape),
                                                BEAMLAYERSPLIT=MODEL.SECTOREQM.BEAMLAYERSPLIT.field(split),
                                                BEAMAZIMUTHOFFSET=MODEL.SECTOREQM.BEAMAZIMUTHOFFSET.field(offset),
                                                )
                return sectoreqm_obj

            elif "T" in port_assign_mode and "R" in port_assign_mode:
                tx_ports = port_assign_mode[:port_assign_mode.find("T")]
                rx_ports = port_assign_mode[port_assign_mode.find("T") + 1: port_assign_mode.find("R")]
                salve_port = ""
                if port_assign_mode[-1] not in ["T", "R"]:
                    salve_port = port_assign_mode[-1]
                for t in tx_ports:  # 遍历发射端口
                    if t.isupper():  # 大写字母, 代表第一个模块的端口
                        rxu = rxu_list[i]
                        port = ord(t) - ord("A")
                    else:  # 小写字母，射频互连的第二个模块的端口
                        rxu = rxu_list[-1]
                        port = ord(t) - ord('a')

                    if t in rx_ports:
                        anttype = MODEL.SECTOREQM.SECTOREQMANTENNA.ANTTYPE.RXTX_MODE
                    else:
                        anttype = MODEL.SECTOREQM.SECTOREQMANTENNA.ANTTYPE.TX_MODE
                    if salve_port == t:
                        txbkpmode = MODEL.SECTOREQM.SECTOREQMANTENNA.TXBKPMODE.SLAVE
                    else:
                        txbkpmode = MODEL.SECTOREQM.SECTOREQMANTENNA.TXBKPMODE.MASTER

                    cn, srn, sn = self.inner_get_cn_srn_sn_from_rxu_info(rxu)
                    tmp = MODEL.SECTOREQM.SECTOREQMANTENNA(CN=cn, SRN=srn, SN=sn, ANTN=port, ANTTYPE=anttype,
                                                           TXBKPMODE=txbkpmode)
                    ant_list.append(tmp)

                for t in rx_ports:  # 遍历接收端口
                    if t in tx_ports: continue  # 如果该端口在发射端口中，则上面已输出过，无需处理

                    if t.isupper():  # 大写字母, 代表第一个模块的端口
                        rxu = rxu_list[i]
                        port = ord(t) - ord("A")
                    else:  # 小写字母，射频互连的第二个模块的端口
                        rxu = rxu_list[-1]
                        port = ord(t) - ord('a')

                    cn, srn, sn = self.inner_get_cn_srn_sn_from_rxu_info(rxu)
                    tmp = MODEL.SECTOREQM.SECTOREQMANTENNA(CN=cn, SRN=srn, SN=sn, ANTN=port,  # 发射端口号
                                                           ANTTYPE=MODEL.SECTOREQM.SECTOREQMANTENNA.ANTTYPE.RX_MODE)
                    ant_list.append(tmp)
        if len(ant_list) > 0:
            sectoreqm_obj = MODEL.SECTOREQM(SECTOREQMID=sectoreqmid, SECTORID=sectorid,
                                            ANTCFGMODE=MODEL.SECTOREQM.ANTCFGMODE.ANTENNAPORT,
                                            SECTOREQMANTENNA=ant_list
                                            )
        else:
            raise Exception("Error: Invalid port_assign_mode: %s" % port_assign_modes)
        return sectoreqm_obj

    @API_RECORD
    def inner_get_sectoreqmid_plan(self, sectoreqmid_plan_map, rat, sector_name, band, need_qty=1):
        rat_band = "%s%s" % (rat, band) if rat not in band else band
        if rat_band not in sectoreqmid_plan_map:
            self.exit_Info("Error: No SECTOREQMID plan for %s, band=%s" % (rat, band))
        if sector_name not in sectoreqmid_plan_map[rat_band]:
            self.exit_Info("Error: No SECTOREQMID plan for %s, band=%s, %s" % (rat, band, sector_name))
        if len(sectoreqmid_plan_map[rat_band][sector_name]) < need_qty:
            self.exit_Info("Error: No enough SECTOREQMID plan for  %s, band=%s, %s. need_qty=%d, remaining=%r" %
                           (rat, band, sector_name, need_qty, sectoreqmid_plan_map[rat_band][sector_name]))
        return sectoreqmid_plan_map[rat_band][sector_name]

    # 为一个PORT_ASSIGN创建扇区设备
    @API_RECORD
    def inner_create_sectoreqm(self, sectoreqm_obj_list, sectoreqmid_plan_map, excel_file, sector, band, work_mode,
                               assign_mode, rxu_info_list):
        sector_name = "SECTOR_%s" % (sector.strip()[0])
        band = band.strip()
        work_mode = work_mode.strip()

        # 获得扇区ID
        sectorid_plan_map = self.get_ID_Plan(excel_file, "SECTORID")
        if band not in sectorid_plan_map:
            self.exit_Info("Error: No SECTORID plan for band=%s" % band)
        if sector_name not in sectorid_plan_map[band] or len(sectorid_plan_map[band][sector_name]) == 0:
            self.exit_Info("Error: No SECTORID plan for band=%s %s" % (band, sector_name))
        sectorid = sectorid_plan_map[band][sector_name][0]

        port_assign_mode_map = load_Excel_File(excel_file, "Ant Port Assign Mode", 2, "PORT_ASSIGN_MODE_NAME")
        if assign_mode not in port_assign_mode_map:
            raise Exception("Error: Port_Assign_Mode=%s not exist" % assign_mode)
        assign_info = port_assign_mode_map[assign_mode][0]

        for (rat, rat_port_assign_name) in [("G", "GSM_PORT_ASSIGN"), ("U", "UMTS_PORT_ASSIGN"),
                                            ("L", "LTE_PORT_ASSIGN"), ("T", "LTE_PORT_ASSIGN"),
                                            ("M", "NB_PORT_ASSIGN"), ("N", "5G_PORT_ASSIGN")]:
            if rat in work_mode:
                rat_assign_info = assign_info.attr(rat_port_assign_name)
                if rat_assign_info is None: continue  # 该制式没有扇区设备设置
                if rat_assign_info.startswith("BEAM") == False:
                    rat_assign_info = rat_assign_info.replace(",", ";")
                rat_assign_list = rat_assign_info.split(";")
                rat_assign_list = [s.strip() for s in rat_assign_list if len(s.strip()) > 0]
                sectoreqmid_list = self.inner_get_sectoreqmid_plan(sectoreqmid_plan_map, rat+"O", sector_name, band,
                                                              len(rat_assign_list))
                for port_assign_mode in rat_assign_list:
                    sectoreqmid = sectoreqmid_list.pop(0)
                    sectoreqm_obj = self.inner_create_one_sectoreqm(sectoreqmid, sectorid, port_assign_mode, rxu_info_list)
                    sectoreqm_obj_list.append(sectoreqm_obj)
        pass

    @API_RECORD
    def inner_create_sectoreqm_WSD(self, sectoreqm_obj_list, sectoreqmid_plan_map, sectorid_plan_map, sector, band, work_mode,
                                   assign_mode_list, rxu_info_list):
        sector_name = "SECTOR_%s" % (sector.strip()[0])
        band = band.strip()
        work_mode = work_mode.strip()

        if band not in sectorid_plan_map:
            self.exit_Info("Error: No SECTORID plan for band=%s" % band)
        if sector_name not in sectorid_plan_map[band] or len(sectorid_plan_map[band][sector_name]) == 0:
            self.exit_Info("Error: No SECTORID plan for band=%s %s" % (band, sector_name))
        sectorid = sectorid_plan_map[band][sector_name][0]

        for (rat, rat_fullname, rat_port_assign_idx) in [("G", "GO", 0),
                                                         ("U", "UO", 1),
                                                         ("L", "LO", 2),
                                                         ("T", "TO", 2),
                                                         ("M", "MO", 3),
                                                         ("N", "NO", 4)]:
            if rat in work_mode:
                rat_assign_info = assign_mode_list[rat_port_assign_idx]
                if rat_assign_info is None: continue  # 该制式没有扇区设备设置
                if rat_assign_info.startswith("BEAM") == False:
                    rat_assign_info = rat_assign_info.replace(",", ";")
                rat_assign_list = rat_assign_info.split(";")
                rat_assign_list = [s.strip() for s in rat_assign_list if len(s.strip()) > 0]
                sectoreqmid_list = self.inner_get_sectoreqmid_plan(sectoreqmid_plan_map, rat_fullname, sector_name, band,
                                                              len(rat_assign_list))
                for port_assign_mode in rat_assign_list:
                    sectoreqmid = sectoreqmid_list.pop(0)
                    sectoreqm_obj = self.inner_create_one_sectoreqm(sectoreqmid, sectorid, port_assign_mode, rxu_info_list)
                    if sectoreqm_obj is None: continue
                    sectoreqm_obj_list.append(sectoreqm_obj)
        pass

    @API_RECORD
    def inner_create_sector_by_sectoreqm(self, sectoreqm_obj_list):
        sectorid_to_ant_map = {}
        ant_to_sectorid_map = {}
        for sectoreqm_obj in sectoreqm_obj_list:
            sectorid = int(sectoreqm_obj.SECTORID)
            if sectorid not in sectorid_to_ant_map:
                sectorid_to_ant_map[sectorid] = []
            if sectoreqm_obj.ANTCFGMODE == MODEL.SECTOREQM.ANTCFGMODE.ANTENNAPORT:
                for ant_obj in sectoreqm_obj.SECTOREQMANTENNA:
                    ant = (ant_obj.CN, ant_obj.SRN, ant_obj.SN, ant_obj.ANTN)
                    ant_to_sectorid_map[ant] = sectorid
            pass

        for (ant, sectorid) in ant_to_sectorid_map.items():
            sectorid_to_ant_map[sectorid].append(ant)

        used_sectorid_list = self.get_para_list_from_moc(sectoreqm_obj_list, "SECTORID")

        sector_obj_list = []
        for (sectorid, ant_list) in sectorid_to_ant_map.items():
            if sectorid not in used_sectorid_list: continue  # 没有被SectorEqm引用的SectorID，不创建
            ant_obj_list = []
            for (cn, srn, sn, antn) in ant_list:
                ant_obj = MODEL.SECTOR.SECTORANTENNA(CN=cn, SRN=srn, SN=sn, ANTN=antn)
                ant_obj_list.append(ant_obj)
            sector_obj = MODEL.SECTOR(SECTORID=int(sectorid), SECNAME="S%d" % sectorid, SECTORANTENNA=ant_obj_list)
            sector_obj_list.append(sector_obj)
        return sector_obj_list

    def inner_get_cn_srn_sn_from_rxu_info(self, rxu_info):
        if "CN-SRN-SN" in rxu_info:
            cn_srn_sn = rxu_info[u"CN-SRN-SN"]
        elif "-" in rxu_info: #For JSON to CME Decoding
            cn, srn, sn = rxu_info.split("-")
            return cn, srn, sn
        else:
            cn_srn_sn = rxu_info.cNSrnSn
        if "-" in cn_srn_sn:  # RRU只输入框号，这里为RRU补充CN, SN
            cn, srn, sn = cn_srn_sn.split("-")
            return int(cn), int(srn), int(sn)
        else:
            return 0, int(cn_srn_sn), 0

    @API_RECORD
    def get_Sub_Para_List(self,moc, para, subpara):
        result = []
        obj_list = self.get_moc(moc)
        for obj in obj_list:
            sub_obj_list = getattr(obj, para, [])
            for sub_obj in sub_obj_list:
                value = getattr(sub_obj, subpara, None)
                result.append(value)
        return result

    def inner_check_para(self, kwargs, para_list):
        error_count = 0
        for para in para_list:
            if para not in kwargs:
                print("Error: para=%s must provide" % para)
            elif kwargs[para] in [None, "", u""]:
                print("Error: para=%s is None" % para)
                error_count += 1
            else:
                continue
        return error_count

    @API_RECORD
    def inner_create_lte_cell(self, **kwargs):
        error_count = self.inner_check_para(kwargs,
                                       ["TemplateName", "LocalCellId", "CellName", "CellId", "FreqBand", "DlEarfcn",
                                        "PhyCellId", "TxRxMode", "TrackingAreaId", "Tac", "SectorEqmId"])
        # cell_template = kwargs.get("cell_template")
        # for field_name in cell_template.get_field_names():
        #     if field_name not in kwargs:
        #         kwargs[field_name] = cell_template.get(field_name)
        # Create Tac
        if "CnOperatorId" not in kwargs: kwargs["CnOperatorId"] = 0
        if "NbIotTaFlag" not in kwargs: kwargs["NbIotTaFlag"] = 0
        tai = self.create_TAC(kwargs["Tac"], kwargs["CnOperatorId"], kwargs["TrackingAreaId"], kwargs["NbIotTaFlag"])
        # Create LTE Cell

        cell_obj = MODEL.Cell(**kwargs)
        cell_template = self.get_data_from_template(kwargs["TemplateName"], "Cell", with_child=True)[0]
        new_cell_obj = self.save_data_with_template([cell_obj], cell_template)[0]
        # Setting Other Parameters
        if "ReferenceSignalPwr" in kwargs:
            new_cell_obj.PDSCHCfg[0].ReferenceSignalPwr = kwargs["ReferenceSignalPwr"]
        new_cell_obj.CellOp[0].TrackingAreaId = tai
        if len(new_cell_obj["eNBCellOpRsvdPara"]) > 1:
            for x in range(len(new_cell_obj["eNBCellOpRsvdPara"])-1, 0, -1):
                del new_cell_obj["eNBCellOpRsvdPara"][x]
        new_cell_obj.eNBCellOpRsvdPara[0].TrackingAreaId = tai
        if len(new_cell_obj["CellOp"]) > 1:
            new_cell_obj["CellOp"] = [new_cell_obj["CellOp"][0]]

        if "Pb" in kwargs:
            new_cell_obj.PDSCHCfg[0].Pb = kwargs["Pb"]
        if "PaPcOff" in kwargs:
            new_cell_obj.CellDlpcPdschPa[0].PaPcOff = kwargs["PaPcOff"]
        if "MMECfgNum" in kwargs:
            new_cell_obj.CellOp[0].MMECfgNum = MODEL.CellOp.MMECfgNum.field(kwargs["MMECfgNum"])
        self.save_moc("Cell", [new_cell_obj], APPEND_MODE, with_child=True, with_merge=True)

        # Create eUCellSectorEqm
        kwargs["ReferenceSignalPwr"] = 32767
        eUCellSectorEqm_obj = MODEL.eUCellSectorEqm(**kwargs)
        necell_flag = kwargs.get("NbCellFlag")
        if not necell_flag or MODEL.Cell.NbCellFlag.toString(necell_flag) == "FALSE":
            self.save_moc('eUCellSectorEqm', [eUCellSectorEqm_obj], APPEND_MODE, with_child=True, with_merge=True)
        return error_count

    @API_RECORD
    def inner_create_one_devip(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["CN", "SRN", "SN", "IP"])
        # default para value
        if "PN" not in kwargs or kwargs["PN"] in [None, "", u""]:
            kwargs["PN"] = 0
        if "MASK" not in kwargs or kwargs["MASK"] in [None, "", u""]:
            kwargs["MASK"] = MODEL.IPV4.fromString("255.255.255.0")
        if "SBT" not in kwargs or kwargs["SBT"] in [None, "", u""]:
            kwargs["SBT"] = MODEL.DEVIP.SBT.BASE_BOARD
        if "PT" not in kwargs or kwargs["PT"] in [None, "", u""]:
            kwargs["PT"] = MODEL.DEVIP.PT.ETH
        if "VRFIDX" not in kwargs or kwargs["VRFIDX"] in [None, "", u""]:
            kwargs["VRFIDX"] = 0
        # Create DEVIP
        devip_obj = MODEL.DEVIP(**kwargs)
        self.save_moc("DEVIP", [devip_obj], APPEND_MODE, with_merge=True)
        return error_count

    @API_RECORD
    def inner_create_one_omch(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["IP", "PEERIP"])
        # default para value
        if "FLAG" not in kwargs or kwargs["FLAG"] in [None, "", u""]:
            kwargs["FLAG"] = MODEL.OMCH.FLAG.MASTER
        if "MASK" not in kwargs or kwargs["MASK"] in [None, "", u""]:
            kwargs["MASK"] = MODEL.IPV4.fromString("255.255.255.0")
        if "PEERMASK" not in kwargs or kwargs["PEERMASK"] in [None, "", u""]:
            kwargs["PEERMASK"] = MODEL.IPV4.fromString("255.255.255.0")
        if "BEAR" not in kwargs or kwargs["BEAR"] in [None, "", u""]:
            kwargs["BEAR"] = MODEL.OMCH.BEAR.IPV4
        # Create OMCH
        omch_obj = MODEL.OMCH(**kwargs)
        self.save_moc("OMCH", [omch_obj], OVERWRITE_MODE, with_merge=True)
        return error_count

    @API_RECORD
    def inner_create_one_vlanmap(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["NEXTHOPIP", "VLANID"])
        # default para value
        if "MASK" not in kwargs or kwargs["MASK"] in [None, "", u""]:
            kwargs["MASK"] = MODEL.IPV4.fromString("255.255.255.255")
        if "VLANMODE" not in kwargs or kwargs["VLANMODE"] in [None, "", u""]:
            kwargs["VLANMODE"] = MODEL.VLANMAP.VLANMODE.SINGLEVLAN
        if "SETPRIO" not in kwargs or kwargs["SETPRIO"] in [None, "", u""]:
            kwargs["SETPRIO"] = MODEL.VLANMAP.SETPRIO.DISABLE
        if "VRFIDX" not in kwargs or kwargs["VRFIDX"] in [None, "", u""]:
            kwargs["VRFIDX"] = 0
        # Create VLANMAP
        vlanmap_obj = MODEL.VLANMAP(**kwargs)
        self.save_moc("VLANMAP", [vlanmap_obj], APPEND_MODE, with_merge=True)
        return error_count

    @API_RECORD
    def inner_Create_One_IPRT(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["CN", "SRN", "SN", "DSTIP", "IP", "NEXTHOP"])
        # default para value
        if "VRFIDX" not in kwargs or kwargs["VRFIDX"] in [None, "", u""]:
            kwargs["VRFIDX"] = 0
        if "SBT" not in kwargs or kwargs["SBT"] in [None, "", u""]:
            kwargs["SBT"] = MODEL.IPRT.SBT.BASE_BOARD
        if "RTTYPE" not in kwargs or kwargs["RTTYPE"] in [None, "", u""]:
            kwargs["RTTYPE"] = MODEL.IPRT.RTTYPE.NEXTHOP
        # Create IPRT
        used_iprtidx_list = self.get_para_list_from_moc("IPRT", "RTIDX")
        iprtidx_list = [idx for idx in range(150) if idx not in used_iprtidx_list]
        kwargs["RTIDX"] = iprtidx_list.pop(0)
        iprt_obj = MODEL.IPRT(**kwargs)
        self.save_moc("IPRT", [iprt_obj], APPEND_MODE, with_merge=True)
        return error_count

    @API_RECORD
    def inner_get_int_from_ipv4_str(self, **kwargs):
        for key_item in kwargs:
            if isinstance(kwargs[key_item], list):
                kwargs[key_item] = [MODEL.IPV4.fromString(x) for x in kwargs[key_item] if len(x.split(".")) == 4]
            elif isinstance(kwargs[key_item], str):
                kwargs[key_item] = MODEL.IPV4.fromString(kwargs[key_item]) if len(kwargs[key_item].split(".")) == 4 else \
                kwargs[key_item]
            else:
                pass
        pass

    @API_RECORD
    def inner_Create_One_NTP(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["IP"])
        # default para value
        if "MODE" not in kwargs or kwargs["MODE"] in [None, "", u""]:
            kwargs["MODE"] = MODEL.NTPCP.MODE.IPV4
        if "SYNCCYCLE" not in kwargs or kwargs["SYNCCYCLE"] in [None, "", u""]:
            kwargs["SYNCCYCLE"] = 360
        if "PORT" not in kwargs or kwargs["PORT"] in [None, "", u""]:
            kwargs["PORT"] = 123
        if "AUTHMODE" not in kwargs or kwargs["AUTHMODE"] in [None, "", u""]:
            kwargs["AUTHMODE"] = MODEL.NTPCP.AUTHMODE.PLAIN
        if "MASTERFLAG" not in kwargs or kwargs["MASTERFLAG"] in [None, "", u""]:
            kwargs["MASTERFLAG"] = MODEL.NTPCP.MASTERFLAG.field("Master")
        # Create NTPCP
        ntp_obj = MODEL.NTPCP(**kwargs)
        self.save_moc("NTPCP", [ntp_obj], OVERWRITE_MODE)
        timesrc_obj = MODEL.TIMESRC(TIMESRC=MODEL.TIMESRC.TIMESRC.NTP, AUTOSWITCH=MODEL.TIMESRC.AUTOSWITCH.ON)
        self.save_moc("TIMESRC", [timesrc_obj], OVERWRITE_MODE)
        return error_count

    @API_RECORD
    def create_TX_OMCH(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["SN", "PEERIP", "HOSTIP", "VLANID"])
        kwargs["IP"] = kwargs["HOSTIP"]
        self.inner_get_int_from_ipv4_str(**kwargs)
        if "CN" not in kwargs or kwargs["CN"] in [None, "", u""]:
            kwargs["CN"] = 0
        if "SRN" not in kwargs or kwargs["SRN"] in [None, "", u""]:
            kwargs["SRN"] = 0
        if "USERLABEL" not in kwargs or kwargs["USERLABEL"] in [None, "", u""]:
            kwargs["USERLABEL"] = "FOR OMCH"
        error_count += self.inner_create_one_devip(**kwargs)
        error_count += self.inner_create_one_omch(**kwargs)
        if "DESCRI" not in kwargs or kwargs["DESCRI"] in [None, "", u""]:
            kwargs["DESCRI"] = "FOR OMCH"
        if "DSTIP" not in kwargs or kwargs["DSTIP"] in [None, "", u""]:
            kwargs["DSTIP"] = kwargs["PEERIP"] & kwargs["PEERMASK"]
        if "DSTMASK" not in kwargs or kwargs["DSTMASK"] in [None, "", u""]:
            kwargs["DSTMASK"] = kwargs["PEERMASK"]
        if "NEXTHOP" not in kwargs or kwargs["NEXTHOP"] in [None, "", u""]:
            kwargs["NEXTHOP"] = kwargs["IP"] & kwargs["MASK"] | 0x01
        error_count += self.inner_Create_One_IPRT(**kwargs)
        if "NEXTHOPIP" not in kwargs or kwargs["NEXTHOPIP"] in [None, "", u""]:
            kwargs["NEXTHOPIP"] = kwargs["NEXTHOP"]
        error_count += self.inner_create_one_vlanmap(**kwargs)
        if "with_U2KNTP" in kwargs and kwargs["with_U2KNTP"] == True:
            kwargs["IP"] = kwargs["PEERIP"]
            error_count += self.inner_Create_One_NTP(**kwargs)
        return error_count

    @API_RECORD
    def create_DIFPRI(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["SIGPRI", "OMHIGHPRI", "OMLOWPRI", "IPCLKPRI"])
        if "PRIRULE" not in kwargs or kwargs["PRIRULE"] in [None, "", u""]:
            kwargs["PRIRULE"] = MODEL.DIFPRI.PRIRULE.DSCP
        difpri_obj = MODEL.NTPCP(**kwargs)
        self.save_moc("DIFPRI", [difpri_obj], OVERWRITE_MODE)
        return error_count

    @API_RECORD
    def create_UDT_Only(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["QCIUDTMAP"])
        udt_list = []
        for key, item  in kwargs["QCIUDTMAP"]:
            kwargs["UDTNO"] = key
            kwargs["UDTPARAGRPID"] = item
            udt_obj = MODEL.UDT(**kwargs)
            udt_list.append(udt_obj)
        self.save_moc("UDT", udt_list, OVERWRITE_MODE)
        return error_count

    @API_RECORD
    def create_UDTPARAGRP_Only(self,**kwargs):
        error_count = self.inner_check_para(kwargs, ["UDTPARAGOUPPRIMAP", "UDTUSEIDLIST"])
        # Create UDTPARAGRP
        udtparagrp_list = []
        count = 0
        if "PRIRULE" not in kwargs or kwargs["PRIRULE"] in [None, "", u""]:
            kwargs["PRIRULE"] = MODEL.UDTPARAGRP.PRIRULE.DSCP
        for udtparagroupid in kwargs["UDTPARAGOUPPRIMAP"].keys():
            if udtparagroupid not in kwargs["UDTUSEIDLIST"]: continue
            kwargs["UDTPARAGRPID"] = udtparagroupid
            kwargs["PRI"] = kwargs["UDTPARAGOUPPRIMAP"][udtparagroupid]
            kwargs["ACTFACTOR"] = 100 if count < 4 else 0
            kwargs[
                "PRIMTRANRSCTYPE"] = MODEL.UDTPARAGRP.PRIMTRANRSCTYPE.HQ if count < 5 else MODEL.UDTPARAGRP.PRIMTRANRSCTYPE.LQ
            kwargs["PRIMPTLOADTH"] = 100 if count < 5 else 30
            kwargs["PRIM2SECPTLOADRATH"] = 0 if count < 5 else 100
            udtparagrp_obj = MODEL.UDTPARAGRP(**kwargs)
            udtparagrp_list.append(udtparagrp_obj)
            count += 1
        self.save_moc("UDTPARAGRP", udtparagrp_list, OVERWRITE_MODE)
        return error_count

    @API_RECORD
    def create_LOCATION(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["LOCATIONNAME"])
        if "MODE" not in kwargs:
            kwargs["MODE"] = MODEL.LOCATION.MODE.AUTO
        if "GCDF" not in kwargs and "LATITUDEDEGFORMAT" in kwargs and "LONGITUDEDEGFORMAT" in kwargs:
            kwargs["GCDF"] = MODEL.LOCATION.GCDF.Degree
        elif "GCDF" not in kwargs and "LATITUDESECFORMAT" in kwargs and "LONGITUDESECFORMAT" in kwargs:
            kwargs["GCDF"] = MODEL.LOCATION.GCDF.Second
        else:
            error_count += 1
        location_obj = MODEL.LOCATION(**kwargs)
        self.save_moc('LOCATION', [location_obj], APPEND_MODE, with_merge=True, with_child=True)
        return error_count

    @API_RECORD
    def create_UDT(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["QCIUDTMAP", "UDTPARAGOUPPRIMAP"])
        error_count += self.create_UDT_Only(**kwargs)
        kwargs["UDTUSEIDLIST"] = self.get_para_list_from_moc("UDT", "UDTPARAGROUPID")
        error_count += self.create_UDTPARAGRP_Only(**kwargs)
        return error_count

    @API_RECORD
    def inner_Create_One_IPCLK(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["SN", "SIP", "CIP"])
        if "ICPT" not in kwargs or kwargs["ICPT"] in [None, "", u""]:
            kwargs["ICPT"] = MODEL.IPCLKLNK.ICPT.PTP
        if "IPMODE" not in kwargs or kwargs["IPMODE"] in [None, "", u""]:
            kwargs["IPMODE"] = MODEL.IPCLKLNK.IPMODE.IPV4
        if "CNM" not in kwargs or kwargs["CNM"] in [None, "", u""]:
            kwargs["CNM"] = MODEL.IPCLKLNK.CNM.UNICAST
        if "CN" not in kwargs or kwargs["CN"] in [None, "", u""]:
            kwargs["CN"] = 0
        if "SRN" not in kwargs or kwargs["SRN"] in [None, "", u""]:
            kwargs["SRN"] = 0
        if "PROFILETYPE" not in kwargs or kwargs["PROFILETYPE"] in [None, "", u""]:
            kwargs["PROFILETYPE"] = MODEL.IPCLKLNK.PROFILETYPE.field("1588V2")
        if "LN" not in kwargs or kwargs["LN"] in [None, "", u""]:
            kwargs["LN"] = self.get_free_id_list("IPCLKLNK", "LN").pop(0)
        ipclklnk_obj = MODEL.IPCLKLNK(**kwargs)
        self.save_moc('IPCLKLNK', [ipclklnk_obj], APPEND_MODE, with_child=True, fill_default=True)
        return error_count

    @API_RECORD
    def create_IPCLK(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["SN", "IPCLKIPLIST"])
        for item in kwargs["IPCLKIPLIST"]:
            if len(item) != 2:
                error_count += 1
                return error_count
            kwargs["CIP"], kwargs["SIP"] = item[0], item[1]
            self.inner_Create_One_IPCLK(**kwargs)

        return error_count

    @API_RECORD
    def get_LTE_Cell_by_LTE_band(self, band, report_error=False):
        """获得指定频段的LTE小区对象"""
        band = int(band)
        cell_obj_list = []
        for cell_obj in self.get_moc("Cell"):
            if cell_obj.NbCellFlag == MODEL.Cell.NbCellFlag.TRUE:
                cell_band = self.get_para_list_from_moc("Prb", "FreqBand", WHERE(LocalCellId=cell_obj.LocalCellId))[0]
            else:
                cell_band = cell_obj.FreqBand
            if cell_band == band:
                cell_obj_list.append(cell_obj)

        if len(cell_obj_list) == 0:
            msg = "Warning: LTE Cell Band=%d not exist" % band
            if report_error is True:
                self.exit_Info(msg)

        return cell_obj_list

    @API_RECORD
    def get_RXU_pos_by_LTE_LocalCellId(self, locellid, only_tx=True):
        """根据LTE LocalCellId获得RXU柜框槽号. Only_tx: 只获得发射的RXU，纯接收的RXU不返回"""
        locellid = int(locellid)
        cell_obj_list = self.get_moc("Cell", WHERE(LocalCellId=locellid))
        if len(cell_obj_list) == 0:
            print("Warning: LocalCellId=%s not exist." % locellid)
            return []
        cell_obj = cell_obj_list[0]
        if cell_obj.NbCellFlag == MODEL.Cell.NbCellFlag.TRUE and hasattr(MODEL, "EuPrbSectorEqm"):
            sectoreqmid_list = self.get_para_list_from_moc("EuPrbSectorEqm", "SectorEqmId", WHERE(LocalCellId=locellid))
        else:
            sectoreqmid_list = self.get_para_list_from_moc("eUCellSectorEqm", "SectorEqmId", WHERE(LocalCellId=locellid))

        rxu_pos_list = []
        for sectoreqmid in sectoreqmid_list:
            sectoreqm_obj = self.get_moc("SECTOREQM", WHERE(SECTOREQMID=sectoreqmid))[0]
            if getattr(sectoreqm_obj, "ANTCFGMODE") == "BEAM":
                rxu_pos_list.append((sectoreqm_obj.RRUCN, sectoreqm_obj.RRUSRN, sectoreqm_obj.RRUSN))
            else:
                for ant_obj in sectoreqm_obj.SECTOREQMANTENNA:
                    if only_tx is True and MODEL.SECTOREQM.SECTOREQMANTENNA.ANTTYPE.toString(ant_obj.ANTTYPE) == "RX_MODE":
                        continue
                    rxu_pos_list.append((ant_obj.CN, ant_obj.SRN, ant_obj.SN))
        if len(rxu_pos_list) == 0:
            print("Warning: LocalCellId=%s, not RXU for it." % locellid)
            return []
        rxu_pos_list = list(set(rxu_pos_list))
        rxu_pos_list.sort()
        return rxu_pos_list

    @API_RECORD
    def get_RXU_pos_by_LTE_band(self, band, report_error=False):
        """获得指定频段的RXU的柜框槽号"""
        cell_obj_list = self.get_LTE_Cell_by_LTE_band(band, report_error)
        rxu_pos_list = []
        for cell_obj in cell_obj_list:
            one_list = self.get_RXU_pos_by_LTE_LocalCellId(cell_obj.LocalCellId)
            rxu_pos_list.extend(one_list)
        rxu_pos_list = list(set(rxu_pos_list))
        rxu_pos_list.sort()
        return rxu_pos_list

    @API_RECORD
    def get_Antenna_List_By_Port_Assign_Str(self, cn, srn, sn, port_assign_str):
        tx_ports = port_assign_str[:port_assign_str.find("T")]
        rx_ports = port_assign_str[port_assign_str.find("T") + 1: port_assign_str.find("R")]

        ant_list = []
        for t in tx_ports:  # 遍历发射端口
            if t.isupper():  # 大写字母, 代表第一个模块的端口
                port = ord(t) - ord("A")
            else:  # 小写字母，射频互连的第二个模块的端口
                port = ord(t) - ord('a')

            if t in rx_ports:
                anttype = MODEL.SECTOREQM.SECTOREQMANTENNA.ANTTYPE.RXTX_MODE
            else:
                anttype = MODEL.SECTOREQM.SECTOREQMANTENNA.ANTTYPE.TX_MODE

            tmp = MODEL.SECTOREQM.SECTOREQMANTENNA(CN=cn, SRN=srn, SN=sn, ANTN=port, ANTTYPE=anttype,
                                                   TXBKPMODE=MODEL.SECTOREQM.SECTOREQMANTENNA.TXBKPMODE.MASTER)
            ant_list.append(tmp)

        for t in rx_ports:  # 遍历接收端口
            if t in tx_ports: continue  # 如果该端口在发射端口中，则上面已输出过，无需处理

            if t.isupper():  # 大写字母, 代表第一个模块的端口
                port = ord(t) - ord("A")
            else:  # 小写字母，射频互连的第二个模块的端口
                port = ord(t) - ord('a')

            tmp = MODEL.SECTOREQM.SECTOREQMANTENNA(CN=cn, SRN=srn, SN=sn, ANTN=port,  # 发射端口号
                                                   ANTTYPE=MODEL.SECTOREQM.SECTOREQMANTENNA.ANTTYPE.RX_MODE)
            ant_list.append(tmp)
        return ant_list

    # 封装函数，对NodeB进行共主控改造，已经规划纳入API基线库
    # 读取NodeB配置，并转换为共主控配置，然后返回配置对象树，对象树包含所有moc数据
    @API_RECORD
    def convert_UO_To_COMPT(self, nodeb_name, ne_tree=None, node_template=None):
        # 加载NodeB网元
        if ne_tree is None:
            ne_tree = self.get_all_moc_from_ref(nodeb_name)
        self.print_msg('Info: Convert UO to COMPT!')
        # 前后网元类型对照表，根据改造之前的类型，或者改造之后的类型
        nodeb_product_type_map = {
            14: 117,  # DBS3900 WCDMA
            15: 118,  # BTS3900 WCDMA
            16: 119,  # BTS3900A WCDMA
            17: 120,  # BTS3900L WCDMA
            18: 121,  # BTS3900AL WCDMA
            23: 123,  # DBS3900 LampSite WCDMA
            24: 125,  # DBS5900_WCDMA
            25: 126,  # BTS5900_WCDMA
            26: 127,  # BTS5900A_WCDMA
            27: 128,  # BTS5900L_WCDMA
            28: 129,  # BTS5900AL_WCDMA
            29: 135,  # DBS5900_LampSite_WCDMA
        }
        old_product_type = ne_tree.NODE[0].PRODUCTTYPE
        if old_product_type in nodeb_product_type_map:
            pass
        elif old_product_type in nodeb_product_type_map.values():
            self.print_msg("NE=%s is already CoMPT. no need do CoMPT Convert" % nodeb_name)
            return ne_tree
        elif old_product_type not in nodeb_product_type_map:
            self.exit_Info("Error: NodeB ProductType=%d is invalid, cannot do CoMPT Convert" % old_product_type)
            return None
        new_product_type = nodeb_product_type_map[old_product_type]

        # 新建共主控的NODE (不继承原来的NODE，目的是去掉原来的版本信息)
        obj = ne_tree["NODE"][0]
        node_obj = MODEL.NODE(NODENAME=nodeb_name, PRODUCTTYPE=new_product_type, WM=MODEL.NODE.WM.CONCURRENT,
                              USERLABEL=obj.USERLABEL, NODEID=obj.NODEID)
        ne_tree.NODE = [node_obj]

        # 新建NODEBFUNCTION, 同时设置APPLICATIONREF
        obj = ne_tree["NODEBFUNCTION"][0]
        nodeb_function_obj = MODEL.NODEBFUNCTION(NODEBFUNCTIONNAME=nodeb_name, USERLABEL=obj.USERLABEL,
                                                 NODEBID=obj.NODEBID)
        ne_tree.NODEBFUNCTION = [nodeb_function_obj]

        # #修改ApplicationRef
        # ne_tree["APPLICATION"] = [ MODEL.APPLICATION(AID=AppRef, AT="NodeB", AN="NodeB", APPMNTMODE="NORMAL") ]
        # ne_tree["RSCGRP"] = self.get_moc_list_by_mod(ne_tree["RSCGRP"],MOD(RSCGRPID=0).WHERE(RSCGRPID=MODEL.RSCGRP.RSCGRPID.AUTOPORT))
        # 修改WMPT为UMPT
        ne_tree.MPT[0].TYPE = MODEL.MPT.TYPE.UMPT

        # 修改LOCALIP
        ne_tree.LOCALIP[0].IP = "192.168.0.49"
        ne_tree.LOCALIP[0].MASK = "255.255.255.0"

        if len(ne_tree.EQUIPMENT) == 1:  # 修改EQUIPMENT的protocol字段
            ne_tree.EQUIPMENT[0].PROTOCOL = MODEL.EQUIPMENT.PROTOCOL.CPRI

        # 修正ETHPORT的设置
        ethport_obj_list = self.get_moc_list_by_mod(ne_tree.ETHPORT, MOD(DUPLEX=2).WHERE(SPEED=3))
        ne_tree.ETHPORT = ethport_obj_list

        # 从版本自带的默认NODE模板，拷贝需要新增的对象
        if node_template == None:
            if "5900" in self.ProductType:
                node_template = "BTS5900_SRAN_BBU5900_BTS5900_FEGE_GUL_G_3SEC_U_3SEC_L_3SEC"
            else:
                node_template = "BTS3900_SRAN_BTS3900_FEGE_GUL_G_3SEC_U_3SEC_L_3SEC"

        for moc in ["GTPU", "PMTUCFG", "TACALG", "TCPACKLIMITALG", "TLDRALG", "TOLCALG", "UDT", "UDTPARAGRP",
                    "LOCALIP6",
                    "CERTCFG", "GTRANSPARAGW", "INGCHKTSK", "LANSW", "MANRESALMRPT", "NEMNT", "UDPPING", "GEPMODELPARA",
                    "TRANSFUNCTIONSW",
                    "CPSWITCH", "SINGLEIPSWITCH"]:
            if hasattr(ne_tree, moc) == True: continue  # NodeB模型中已有这些参数，则不用增加，跳过
            if hasattr(MODEL, moc) == False: continue  # 共主控模型中没有这些参数，跳过
            obj_list = self.get_data_from_template(node_template, moc)
            ne_tree[moc] = obj_list

        # 删除一些不需要的数据，方便多制式合并
        self.inner_delete_unnecessary_data_during_convert(ne_tree)

        return ne_tree

    ##############################################################################
    #Reads gNodeB configurations, converts them to co-MPT configurations, and returns to the configuration object tree, which contains all MOC data
    @API_RECORD
    def convert_NO_To_COMPT(self, gnodeb_name, ne_tree=None):
        # 加载eNodeB网元
        if ne_tree is None:
            ne_tree = self.get_all_moc_from_ref(gnodeb_name)
        self.print_msg('Info: Convert NO to COMPT')
        # 前后网元类型对照表，根据改造之前的类型，或者改造之后的类型
        nr_product_type_map = {
            212: 125,  # DBS5900_5G
            213: 126,  # BTS5900_5G
            214: 127,  # BTS5900A_5G
            215: 128,  # BTS5900L_5G
            216: 129,  # BTS5900AL_5G
            217: 135,  # DBS5900_LampSite_5G
        }
        old_product_type = ne_tree.NODE[0].PRODUCTTYPE
        if old_product_type in nr_product_type_map.values():
            self.print_msg("NE=%s is already CoMPT. no need do CoMPT Convert" % gnodeb_name)
            return ne_tree
        elif old_product_type not in nr_product_type_map:
            self.exit_Info("Error: gNodeB ProductType=%d is invalid, cannot do CoMPT Convert" % old_product_type)
        new_product_type = nr_product_type_map[old_product_type]

        # 新建共主控的NODE (不继承原来的NODE，目的是去掉原来的版本信息)
        obj = ne_tree["NODE"][0]
        node_obj = MODEL.NODE(NODENAME=gnodeb_name, PRODUCTTYPE=new_product_type, WM=MODEL.NODE.WM.CONCURRENT,
                              USERLABEL=obj.USERLABEL, NODEID=obj.NODEID)
        ne_tree.NODE = [node_obj]

        # 新建eNodeBFunction
        obj = ne_tree["gNodeBFunction"][0]
        gnodeb_function_obj = MODEL.gNodeBFunction(gNodeBFunctionName=gnodeb_name, gNBId=obj.gNBId)
        ne_tree.gNodeBFunction = [gnodeb_function_obj]

        # 修改LMPT为UMPT
        ne_tree.MPT[0].TYPE = MODEL.MPT.TYPE.UMPT

        if len(ne_tree.EQUIPMENT) == 1:  # 修改EQUIPMENT的protocol字段
            ne_tree.EQUIPMENT[0].PROTOCOL = MODEL.EQUIPMENT.PROTOCOL.CPRI

        # 从版本自带的默认NODE模板，拷贝需要新增的MOC
        tmpl_filename = "DBS5900_SRAN_BBU5900_VIRTUAL_GULN_G_3SEC_U_3SEC_L_3SEC_NR_3SEC"
        for moc in ["GTPU", "PMTUCFG", "TACALG", "TCPACKLIMITALG", "TLDRALG", "TOLCALG","LOCALIP6",
                    "CERTCFG", "GTRANSPARAGW", "INGCHKTSK", "LANSW", "MANRESALMRPT", "NEMNT", "UDPPING", "GEPMODELPARA",
                    "TRANSFUNCTIONSW",
                    "CPSWITCH", "SINGLEIPSWITCH"]:
            if hasattr(ne_tree, moc) == True: continue  # NodeB模型中已有这些参数，则不用增加，跳过
            if hasattr(MODEL, moc) == False: continue  # 共主控模型中没有这些参数，跳过
            obj_list = self.get_data_from_template(tmpl_filename, moc)
            ne_tree[moc] = obj_list

        # 删除一些不需要的数据，方便多制式合并
        self.inner_delete_unnecessary_data_during_convert(ne_tree)

        return ne_tree
    # 封装函数，对eNodeB进行共主控改造，已经规划纳入API基线库
    # 读取eNodeB配置，并转换为共主控配置，然后返回配置对象树，对象树包含所有moc数据
    @API_RECORD
    def convert_LO_To_COMPT(self, enodeb_name, ne_tree=None):
        # 加载eNodeB网元
        if ne_tree is None:
            ne_tree = self.get_all_moc_from_ref(enodeb_name)
        self.print_msg('Info: Convert LO to COMPT')
        # 前后网元类型对照表，根据改造之前的类型，或者改造之后的类型
        lte_product_type_map = {
            1: 117,  # DBS3900 LTE
            2: 118,  # BTS3900 LTE
            3: 119,  # BTS3900A LTE
            4: 120,  # BTS3900L LTE
            5: 121,  # BTS3900AL LTE
            6: 117,  # DBS3900A LTE
            7: 123,  # DBS3900 LampSite LTE
            8: 125,  # DBS5900_LTE
            9: 126,  # BTS5900_LTE
            10: 127,  # BTS5900A_LTE
            11: 128,  # BTS5900L_LTE
            12: 129,  # BTS5900AL_LTE
            13: 135,  # DBS5900_LampSite_LTE
        }
        old_product_type = ne_tree.NODE[0].PRODUCTTYPE
        if old_product_type in lte_product_type_map.values():
            self.print_msg("NE=%s is already CoMPT. no need do CoMPT Convert" % enodeb_name)
            return ne_tree
        elif old_product_type not in lte_product_type_map:
            self.exit_Info("Error: eNodeB ProductType=%d is invalid, cannot do CoMPT Convert" % old_product_type)
        new_product_type = lte_product_type_map[old_product_type]

        # 新建共主控的NODE (不继承原来的NODE，目的是去掉原来的版本信息)
        obj = ne_tree["NODE"][0]
        node_obj = MODEL.NODE(NODENAME=enodeb_name, PRODUCTTYPE=new_product_type, WM=MODEL.NODE.WM.CONCURRENT,
                              USERLABEL=obj.USERLABEL, NODEID=obj.NODEID)
        ne_tree.NODE = [node_obj]

        # 新建eNodeBFunction
        obj = ne_tree["eNodeBFunction"][0]
        enodeb_function_obj = MODEL.eNodeBFunction(eNodeBFunctionName=enodeb_name, eNodeBId=obj.eNodeBId)
        ne_tree.eNodeBFunction = [enodeb_function_obj]

        # 修改LMPT为UMPT
        ne_tree.MPT[0].TYPE = MODEL.MPT.TYPE.UMPT

        if len(ne_tree.EQUIPMENT) == 1:  # 修改EQUIPMENT的protocol字段
            ne_tree.EQUIPMENT[0].PROTOCOL = MODEL.EQUIPMENT.PROTOCOL.CPRI

        # 从版本自带的默认NODE模板，拷贝需要新增的MOC
        if "5900" in self.ProductType:
            tmpl_filename = "BTS5900_SRAN_BBU5900_BTS5900_FEGE_GUL_G_3SEC_U_3SEC_L_3SEC"
        else:
            tmpl_filename = "BTS3900_SRAN_BTS3900_FEGE_GUL_G_3SEC_U_3SEC_L_3SEC"
        for moc in ["GTPU", "PMTUCFG", "TACALG", "TCPACKLIMITALG", "TLDRALG", "TOLCALG", "UDT", "UDTPARAGRP",
                    "LOCALIP6",
                    "CERTCFG", "GTRANSPARAGW", "INGCHKTSK", "LANSW", "MANRESALMRPT", "NEMNT", "UDPPING", "GEPMODELPARA",
                    "TRANSFUNCTIONSW",
                    "CPSWITCH", "SINGLEIPSWITCH"]:
            if hasattr(ne_tree, moc) == True: continue  # NodeB模型中已有这些参数，则不用增加，跳过
            if hasattr(MODEL, moc) == False: continue  # 共主控模型中没有这些参数，跳过
            obj_list = self.get_data_from_template(tmpl_filename, moc)
            ne_tree[moc] = obj_list

        # 删除一些不需要的数据，方便多制式合并
        self.inner_delete_unnecessary_data_during_convert(ne_tree)

        return ne_tree

    ##############################################################################
    # 封装函数，对GBTS进行共主控改造，
    # 把GBTS的配置，转换为共主控配置，然后返回配置对象树，对象树包含所有moc数据
    @API_RECORD
    def convert_GO_To_COMPT(self, btsinfo, node_template=None, radio_template=None, cell_template=None):
        if btsinfo["BTSTYPE"] == "EGBTS":
            self.print_msg("Error: BTS=%s is already EGBTS, cannot convert" % btsinfo["BTSNAME"])
            return None
        self.print_msg('Info: Convert GO to COMPT')
        if btsinfo["BTSTYPE"] not in ["DBS3900_GSM", "BTS3900_GSM", "BTS3900A_GSM", "BTS3900L_GSM", "BTS3900AL_GSM"]:
            btsinfo["NOT_SUPPORT_BTS"] = True
            product_type = btsinfo["BTSTYPE"].split("_")[0]
        else:
            btsinfo["NOT_SUPPORT_BTS"] = False
            product_type = "DBS3900"

        # 从版本包自带的基站模板中，创建NODE对象
        btsname = btsinfo["NEW_BTSNAME"] if "NEW_BTSNAME" in btsinfo else btsinfo["BTSNAME"]
        if node_template == None:
            if "5900" in self.ProductType:
                node_template = "BTS5900_SRAN_BBU5900_BTS5900_FEGE_GUL_G_3SEC_U_3SEC_L_3SEC"
            else:
                node_template = "BTS3900_SRAN_BTS3900_FEGE_GUL_G_3SEC_U_3SEC_L_3SEC"
        egbts_tree = self.get_doc_from_template(node_template)
        egbts_tree["NODE"] = [MODEL.NODE(NODENAME=btsname, PRODUCTTYPE=product_type, NODEID=1, WM="CONCURRENT")]
        egbts_tree["NE"] = [MODEL.NE(NENAME=btsname)]
        egbts_tree["GTMU"] = [MODEL.GTMU(CN=0, SRN=0, SN=6, TYPE="GTMU", ADMSTATE="UNBLOCKED")]

        # 删除默认基站模板中不需要的对象
        unselect_moc_list = ["RFU", "RRU", "RRUCHAIN", "SECTOREQM", "SECTOR", "BBP", "BASEBANDEQM", "UEIU", "BRI",
                             "TRP",
                             "DEVIP", "SCTPLNK", "IPPATH", "VLANMAP", "IPRT", "NTPCP", "CPBEARER",
                             "ALMPORT", "CPRIPORT", "SFP", "RETPORT", "TXBRANCH", "RXBRANCH", "CASCADEPORT"]
        for moc in unselect_moc_list:
            if moc in egbts_tree:
                del egbts_tree[moc]

        # 创建GBTSFunction
        if radio_template == None:
            radio_template = "GBTS_Radio"
        radio_template_data = self.get_data_from_template(radio_template, "GBTSFUNCTION", with_child=True)[0]
        gbts_function_obj = MODEL.GBTSFUNCTION(GBTSFUNCTIONNAME=btsname)
        egbts_tree["GBTSFUNCTION"] = self.save_data_with_template([gbts_function_obj], radio_template_data)

        # 从BSC的配置文件中，生成基站配置对象
        self.inner_GO_To_COMPT_create_GLOCELL(egbts_tree, btsinfo, cell_template)
        GTRXGROUP_obj_list, GTRXGROUPSECTOREQM_obj_list = self.create_GTRXGROUP(btsinfo)
        egbts_tree["GTRXGROUP"] = GTRXGROUP_obj_list
        egbts_tree["GTRXGROUPSECTOREQM"] = GTRXGROUPSECTOREQM_obj_list
        try:
            self.inner_GO_To_COMPT_create_CABINET(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_BRD(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_EMU(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_TCU(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_CCU(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_FMU(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_PMU(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_BATTERY(egbts_tree, btsinfo)

            self.inner_GO_To_COMPT_create_TMA(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_RET(egbts_tree, btsinfo)

            self.inner_GO_To_COMPT_create_ALMPORT(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_ALMCURCFG(egbts_tree, btsinfo)

            self.inner_GO_To_COMPT_create_DEVIP_SRCIPRT(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_VLAN(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_SCTPLNK(egbts_tree, btsinfo)
            self.inner_GO_To_COMPT_create_for_UserPlane(egbts_tree, btsinfo)
        except:
            pass

        # 删除一些不需要的数据，方便多制式合并
        self.inner_delete_unnecessary_data_during_convert(egbts_tree)
        return egbts_tree

    # Move BBP Board
    # 挪BBP单板
    @API_RECORD
    def move_BBP(self, ne_tree, old_sn, new_sn, old_srn=0, new_srn=0, old_cn=0, new_cn=0):
        old_cn, old_srn, old_sn = int(old_cn), int(old_srn), int(old_sn)
        new_cn, new_srn, new_sn = int(new_cn), int(new_srn), int(new_sn)
        for moc in ["BBP", "CASCADEPORT", "SFP", "CPRIPORT"]:
            if hasattr(ne_tree, moc) == False: continue
            ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc],
                                                    MOD(CN=new_cn, SRN=new_srn, SN=new_sn).WHERE(CN=old_cn, SRN=old_srn, SN=old_sn))

        if hasattr(ne_tree, "BASEBANDEQM"):
            for obj in ne_tree.BASEBANDEQM:
                if hasattr(obj, "BASEBANDEQMBOARD") == False: continue
                obj.BASEBANDEQMBOARD = self.get_moc_list_by_mod(obj.BASEBANDEQMBOARD,
                                                                MOD(CN=new_cn, SRN=new_srn, SN=new_sn).WHERE(CN=old_cn, SRN=old_srn,
                                                                                                SN=old_sn))

        if hasattr(ne_tree, "RRUCHAIN"):
            for obj in ne_tree.RRUCHAIN:
                if (obj.HCN, obj.HSRN, obj.HSN) == (old_cn, old_srn, old_sn):
                    obj.HCN, obj.HSRN, obj.HSN = new_cn, new_srn, new_sn
                if (obj.TCN, obj.TSRN, obj.TSN) == (old_cn, old_srn, old_sn):
                    obj.TCN, obj.TSRN, obj.TSN = new_cn, new_srn, new_sn
                if obj.AT == MODEL.RRUCHAIN.AT.PEERPORT and (obj.HCN, obj.HSRN, obj.LSN) == (
                old_cn, old_srn, old_sn):  # CPRI MUX
                    obj.HCN, obj.HSRN, obj.LSN = new_cn, new_srn, new_sn
            pass

        self.print_msg("Info: Move BBP from slot %d-%d-%d to slot %d-%d-%d" % (old_cn, old_srn, old_sn, new_cn, new_srn, new_sn))
        pass

    # Move BBP Board with Priority
    # 优先级挪BBP单板，按new_sn_list顺序检测每个单板是否存在，如果存在，则挪, 否则不挪
    @API_RECORD
    def move_BBP_Ex(self, ne_tree, old_sn, new_sn_list, srn=0, cn=0):
        cn, srn, old_sn = int(cn), int(srn), int(old_sn)

        existing_sn_list = self.get_para_list_from_moc(ne_tree.BBP, "SN")
        if old_sn not in existing_sn_list:  return True

        new_sn = None
        for sn in new_sn_list:
            if int(sn) not in existing_sn_list:  # 找到备选槽位
                new_sn = int(sn)
                break

        if new_sn is None:
            self.print_msg("Error: Move BBP Failed. No available slot")
            return False

        self.move_BBP(ne_tree, old_sn, new_sn, old_srn=srn, new_srn=srn, old_cn=cn, new_cn=cn)
        return True

    # Delete BBP Board
    @API_RECORD
    def delete_BBP(self, ne_tree, sn, srn=0, cn=0):
        cn, srn, sn = int(cn), int(srn), int(sn)
        for moc in ["BBP", "CASCADEPORT", "SFP", "CPRIPORT", "BRI"]:
            if hasattr(ne_tree, moc) == False: continue
            ne_tree[moc] = self.get_moc_list_by_del(ne_tree[moc], WHERE(CN=cn, SRN=srn, SN=sn))

        if hasattr(ne_tree, "BASEBANDEQM"):
            new_basebandeqm_obj_list = []
            for obj in ne_tree.BASEBANDEQM:
                if hasattr(obj, "BASEBANDEQMBOARD") == False: continue
                obj.BASEBANDEQMBOARD = self.get_moc_list_by_del(obj.BASEBANDEQMBOARD, WHERE(CN=cn, SRN=srn, SN=sn))
                if len(obj.BASEBANDEQMBOARD) > 0:  # ALL BBP of this BasebandEqm was deleted, delete this BasebandEqm
                    new_basebandeqm_obj_list.append(obj)
            ne_tree["BASEBANDEQM"] = new_basebandeqm_obj_list
        pass

    # Modify Subrack No
    @API_RECORD
    def modify_Subrack_No(self, ne_tree, old_cn, old_srn, new_cn, new_srn):
        if (old_cn, old_srn) == (new_cn, new_srn): return

        if new_srn in [0, 1]:  # BBU subrack
            bbp_pos_list = self.get_para_list_from_moc(ne_tree["BBP"], ["CN", "SRN", "SN"])
            for (cn, srn, sn) in bbp_pos_list:
                self.move_BBP(ne_tree, sn, sn, old_srn=srn, new_srn=new_srn, old_cn=cn, new_cn=new_cn)
            ne_tree["SUBRACK"] = self.get_moc_list_by_mod(ne_tree["SUBRACK"],
                                                          MOD(CN=new_cn, SRN=new_srn).WHERE(CN=old_cn, SRN=old_srn))
            ne_tree["RRUCHAIN"] = self.get_moc_list_by_mod(ne_tree["RRUCHAIN"],
                                                           MOD(HCN=new_cn, HSRN=new_srn).WHERE(HCN=old_cn, HSRN=old_srn))
            ne_tree["RRUCHAIN"] = self.get_moc_list_by_mod(ne_tree["RRUCHAIN"],
                                                           MOD(TCN=new_cn, TSRN=new_srn).WHERE(TCN=old_cn, TSRN=old_srn))
        elif new_srn in [4, 5]:  # RFU subrack
            rfu_pos_list = self.get_para_list_from_moc(ne_tree["RFU"], ["CN", "SRN", "SN"])
            for (cn, srn, sn) in rfu_pos_list:
                self.move_RXU(ne_tree, (cn, srn, sn), (new_cn, new_srn, sn))
            rfu_subrack_obj_list = self.get_moc("SUBRACK", WHERE(TYPE=MODEL.SUBRACK.TYPE.RFU, CN=new_cn, SRN=new_srn))
            if len(rfu_subrack_obj_list) > 0:  # new RFU subrack already exist, just delete old RFU subrack
                ne_tree["SUBRACK"] = self.get_moc_list_by_del("SUBRACK", WHERE(TYPE=MODEL.SUBRACK.TYPE.RFU, CN=old_cn, SRN=old_srn))
            else:
                ne_tree["SUBRACK"] = self.get_moc_list_by_mod(ne_tree["SUBRACK"],
                                                              MOD(CN=new_cn, SRN=new_srn).WHERE(CN=old_cn, SRN=old_srn))

        for moc in ne_tree._fields_:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            if hasattr(ne_tree[moc][0], "_type_") == False: continue
            if moc == "SUBRACK" and new_srn in [0, 1, 4, 5]: continue  # already processed above for BBU and RFU subrack
            if hasattr(ne_tree[moc][0]._type_, "CN") and hasattr(ne_tree[moc][0]._type_, "SRN"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(CN=new_cn, SRN=new_srn).WHERE(CN=old_cn, SRN=old_srn))
            if hasattr(ne_tree[moc][0]._type_, "MCN") and hasattr(ne_tree[moc][0]._type_, "MSRN"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(MCN=new_cn, MSRN=new_srn).WHERE(MCN=old_cn, MSRN=old_srn))
        pass

    @API_RECORD
    def modify_BBU_Board_slot(self, ne_tree, old_cn, old_srn, old_sn, new_cn, new_srn, new_sn):
        if old_sn == new_sn: return
        bbp_pos_list = self.get_para_list_from_moc(ne_tree["BBP"], ["CN", "SRN", "SN"])
        for (cn, srn, sn) in bbp_pos_list:
            if (cn, srn, sn) == (old_cn, old_srn, old_sn):
                if 0 <= sn <= 5:
                    self.move_BBP(ne_tree, sn, new_sn, old_srn=srn, new_srn=new_srn, old_cn=cn, new_cn=new_cn)
        for moc in ne_tree._fields_:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            if hasattr(ne_tree[moc][0], "_type_") == False: continue
            if hasattr(ne_tree[moc][0]._type_, "CN") and hasattr(ne_tree[moc][0]._type_, "SRN") and hasattr(ne_tree[moc][0]._type_, "SN"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(CN=new_cn, SRN=new_srn, SN=new_sn).WHERE(CN=old_cn, SRN=old_srn, SN=old_sn))
            if hasattr(ne_tree[moc][0]._type_, "MCN") and hasattr(ne_tree[moc][0]._type_, "MSRN") and hasattr(ne_tree[moc][0]._type_, "MSN"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(MCN=new_cn, MSRN=new_srn, MSN=new_sn).WHERE(MCN=old_cn, MSRN=old_srn, MSN=old_sn))
        pass

    # Modify Cabint No
    @API_RECORD
    def modify_Cabinet_No(self, ne_tree, old_cn, new_cn):
        subrack_list = self.get_para_list_from_moc(ne_tree["SUBRACK"], ["CN", "SRN"], WHERE(CN=old_cn))
        for (old_cn, srn) in subrack_list:
            self.modify_Subrack_No(ne_tree, old_cn, srn, new_cn, srn)
        for moc in ne_tree:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            if hasattr(ne_tree[moc][0], "_type_") == False: continue
            if hasattr(ne_tree[moc][0]._type_, "CN") == False: continue
            ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(CN=new_cn).WHERE(CN=old_cn))
        pass

    # Delete Tunnel
    @API_RECORD
    def delete_Tunnel(self, ne_tree):
        if hasattr(ne_tree, "TUNNEL"):
            del ne_tree["TUNNEL"]
        if hasattr(ne_tree, "IPRT"):
            ne_tree["IPRT"] = self.get_moc_list_by_del("IPRT", WHERE(IFT=MODEL.IPRT.IFT.TUNNEL))
        if hasattr(ne_tree, "RSCGRP"):
            ne_tree["RSCGRP"] = self.get_moc_list_by_del("RSCGRP", WHERE(PT=MODEL.RSCGRP.PT.TUNNEL))
        pass

    @API_RECORD
    def modify_TX_Port(self, ne_tree, new_port, cn=0, srn=0, sn=7):
        # Get Current TX Port
        new_port = int(new_port)
        old_tx_port_list = self.get_para_list_from_moc(ne_tree["DEVIP"], ["CN", "SRN", "SN", "PN", "SBT"],
                                          WHERE(PT=MODEL.DEVIP.PT.ETH))
        old_cn, old_srn, old_sn, old_pn, old_sbt = old_tx_port_list[0]

        for moc in ["SCTPLNK", "IPPATH", "IPRT", "SRCIPRT"]:
            ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc],
                                                    MOD(CN=cn, SRN=srn, SN=sn).WHERE(CN=old_cn, SRN=old_srn, SN=old_sn))

        moc_list = MODEL.NODE.get_child_names(True)
        for moc in moc_list:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            moc_class = getattr(MODEL, moc)
            if hasattr(moc_class, "SBT") == False: continue
            if hasattr(moc_class, "PN") == False: continue
            if hasattr(moc_class, "SN") == False: continue
            if hasattr(moc_class, "SRN") == False: continue
            if hasattr(moc_class, "CN") == False: continue
            if new_port != old_pn and moc != "ETHPORT":
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc],
                                                        MOD(CN=cn, SRN=srn, SN=sn, SBT=0, PN=0).WHERE(CN=old_cn, SRN=old_srn,
                                                                                         SN=old_sn, SBT=old_sbt, PN=1),
                                                        MOD(CN=cn, SRN=srn, SN=sn, SBT=0, PN=1).WHERE(CN=old_cn, SRN=old_srn,
                                                                                         SN=old_sn, SBT=old_sbt, PN=0))
            else:
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc],
                                                        MOD(CN=cn, SRN=srn, SN=sn, SBT=0).WHERE(CN=old_cn, SRN=old_srn, SN=old_sn,
                                                                                   SBT=old_sbt, ))
        pass

    @API_RECORD
    def modify_GSM_LocellID(self, ne_tree, old_id, new_id):
        if int(old_id) == int(new_id): return
        self.print_msg("Info: Modify GLOCELLID from %d to %d" % (int(old_id), int(new_id)))
        moc_list = MODEL.GBTSFUNCTION.get_child_names(True) + MODEL.GLOCELL.get_child_names(True)
        for moc in moc_list:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            moc_class = getattr(MODEL, moc)
            if hasattr(moc_class, "GLOCELLID"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(GLOCELLID=new_id).WHERE(GLOCELLID=old_id),is_new=True)
        pass

    @API_RECORD
    def modify_UMTS_LocellID(self, ne_tree, old_id, new_id):
        moc_list = MODEL.NODEBFUNCTION.get_child_names(True) + MODEL.ULOCELL.get_child_names(True)
        for moc in moc_list:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            moc_class = getattr(MODEL, moc)
            if hasattr(moc_class, "ULOCELLID"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(ULOCELLID=new_id).WHERE(ULOCELLID=old_id),is_new=True)
        if hasattr(ne_tree, "NODEBMULTICELLGRP") and len(ne_tree["NODEBMULTICELLGRP"]) > 0:
            for grp_obj in ne_tree["NODEBMULTICELLGRP"]:
                grp_obj.ULOCELLREF = self.get_moc_list_by_mod(grp_obj.ULOCELLREF, MOD(ULOCELLID=new_id).WHERE(ULOCELLID=old_id),is_new=True)
        pass

    @API_RECORD
    def modify_LTE_LocellID(self, ne_tree, old_id, new_id):
        nodebid = ne_tree[""]
        self.print_msg("Info: Modify LTE LocalCellID from %d to %d" % (old_id, new_id))
        moc_list = MODEL.eNodeBFunction.get_child_names(True) + MODEL.Cell.get_child_names(True)
        for moc in moc_list:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            moc_class = getattr(MODEL, moc)
            if hasattr(moc_class, "LocalCellId"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(LocalCellId=new_id).WHERE(LocalCellId=old_id),is_new=True)
        if hasattr(ne_tree, "CaGroupSCellCfg") and len(ne_tree["CaGroupSCellCfg"]) > 0:
            ne_tree["CaGroupSCellCfg"] = self.get_moc_list_by_mod(ne_tree["CaGroupSCellCfg"],
                                                                  MOD(SCellLocalCellId=new_id).WHERE(SCellLocalCellId=old_id),is_new=True)
        if hasattr(ne_tree, "SsrdCellGroup") and len(ne_tree["SsrdCellGroup"]) > 0:
            ne_tree["SsrdCellGroup"] = self.get_moc_list_by_mod(ne_tree["SsrdCellGroup"],
                                                                MOD(PrimaryLocalCellID=new_id).WHERE(PrimaryLocalCellID=old_id),is_new=True)
            ne_tree["SsrdCellGroup"] = self.get_moc_list_by_mod(ne_tree["SsrdCellGroup"],
                                                                MOD(SsrdLocalCellID=new_id).WHERE(SsrdLocalCellID=old_id),is_new=True)
        pass

    @API_RECORD
    def modify_Prb_PrbID(self, ne_tree, old_id, new_id):
        self.print_msg("Info: Modify Prb PrbID from %d to %d" % (old_id, new_id))
        moc_list = MODEL.Prb.get_child_names(True)
        for moc in moc_list:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            moc_class = getattr(MODEL, moc)
            if hasattr(moc_class, "PrbId"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(PrbId=new_id).WHERE(PrbId=old_id), is_new=True)


    @API_RECORD
    def modify_NR_NrCellId(self, ne_tree, old_id, new_id):
        nodebid = ne_tree[""]
        self.print_msg("Info: Modify NR NrCellId from %d to %d" % (old_id, new_id))
        moc_list = MODEL.gNodeBFunction.get_child_names(True) + MODEL.NRCell.get_child_names(True)
        for moc in moc_list:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            moc_class = getattr(MODEL, moc)
            if hasattr(moc_class, "NrCellId"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(NrCellId=new_id).WHERE(NrCellId=old_id),is_new=True)

    @API_RECORD
    def modify_NR_NrDuCellId(self, ne_tree, old_id, new_id):
        nodebid = ne_tree[""]
        self.print_msg("Info: Modify NR NRDUCell from %d to %d" % (old_id, new_id))
        moc_list = MODEL.gNodeBFunction.get_child_names(True) + MODEL.NRDUCell.get_child_names(True)
        for moc in moc_list:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            moc_class = getattr(MODEL, moc)
            if hasattr(moc_class, "NrDuCellId"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(NrDuCellId=new_id).WHERE(NrDuCellId=old_id),is_new=True)

    @API_RECORD
    def modify_NR_NrDuCellTrpId(self, ne_tree, old_id, new_id):
        nodebid = ne_tree[""]
        self.print_msg("Info: Modify NR NrDuCellTrpId from %d to %d" % (old_id, new_id))
        moc_list = MODEL.gNodeBFunction.get_child_names(True) + MODEL.NRDUCellTrp.get_child_names(True)
        for moc in moc_list:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            moc_class = getattr(MODEL, moc)
            if hasattr(moc_class, "NrDuCellTrpId"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(NrDuCellTrpId=new_id).WHERE(NrDuCellTrpId=old_id),is_new=True)

    @API_RECORD
    def modify_NR_NrDuCellTrpId(self, ne_tree, old_id, new_id):
        nodebid = ne_tree[""]
        self.print_msg("Info: Modify NR NrDuCellTrpId from %d to %d" % (old_id, new_id))
        moc_list = MODEL.gNodeBFunction.get_child_names(True) + MODEL.NRDUCellTrp.get_child_names(True)
        for moc in moc_list:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            moc_class = getattr(MODEL, moc)
            if hasattr(moc_class, "NrDuCellTrpId"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(NrDuCellTrpId=new_id).WHERE(NrDuCellTrpId=old_id),is_new=True)

    @API_RECORD
    def modify_LTE_CellID(self, ne_tree, old_id, new_id):
        eNodebid = ne_tree["eNodeBFunction"][0].eNodeBId
        ne_tree["Cell"] = self.get_moc_list_by_mod(ne_tree["Cell"], MOD(CellId=new_id).WHERE(CellId=old_id))
        ne_tree["EutranIntraFreqNCell"] = self.get_moc_list_by_mod(ne_tree["EutranIntraFreqNCell"],
                              MOD(CellId=new_id).WHERE(CellId=old_id, eNodeBId=eNodebid))

    # Move RRUCHAIN_POS
    @API_RECORD
    def move_RRUCHAIN_Pos(self, ne_tree, old_pos, new_pos):
        old_hcn, old_hsrn, old_hsn, old_hpn = int(old_pos[0]), int(old_pos[1]), int(old_pos[2]), int(old_pos[3])
        new_hcn, new_hsrn, new_hsn, new_hpn = int(new_pos[0]), int(new_pos[1]), int(new_pos[2]), int(new_pos[3])
        if (old_hcn, old_hsrn, old_hsn, old_hpn) == (new_hcn, new_hsrn, new_hsn, new_hpn): return

        for moc in ["RRUCHAIN"]:
            if hasattr(ne_tree, moc) == False: continue
            ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc],
                                                    MOD(HCN=new_hcn, HSRN=new_hsrn, HSN=new_hsn, HPN=new_hpn).WHERE(
                                                        HCN=old_hcn,
                                                        HSRN=old_hsrn,
                                                        HSN=old_hsn,
                                                        HPN=old_hpn))
        pass

    # Move RXU Board
    @API_RECORD
    def move_RXU(self, ne_tree, old_pos, new_pos):
        old_cn, old_srn, old_sn = int(old_pos[0]), int(old_pos[1]), int(old_pos[2])
        new_cn, new_srn, new_sn = int(new_pos[0]), int(new_pos[1]), int(new_pos[2])
        if (old_cn, old_srn, old_sn) == (new_cn, new_srn, new_sn): return

        if old_srn >= 60 and new_srn < 60:
            # print "API_Move_RXU: Old RRU(%r), New Pos is for RFU(%r). Skip" % (old_pos, new_pos)
            return
        elif old_srn < 60 and new_srn >= 60:
            # print "API_Move_RXU: Old RFU(%r), New Pos is for RRU(%r). Skip" % (old_pos, new_pos)
            return

        for moc in ["RRU", "RFU", "AAS", "AAMU", "AARU", "ANTENNAPORT", "CPRIPORT", "SFP", "RETPORT", "RXBRANCH",
                    "TXBRANCH", "ALMPORT"]:
            if hasattr(ne_tree, moc) == False: continue
            ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc],
                                                    MOD(CN=new_cn, SRN=new_srn, SN=new_sn).WHERE(CN=old_cn, SRN=old_srn, SN=old_sn))

        for moc in ["TMA", "RET"]:
            if hasattr(ne_tree, moc) == False: continue
            ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc],
                                                    MOD(CTRLCN=new_cn, CTRLSRN=new_srn, CTRLSN=new_sn).WHERE(CTRLCN=old_cn,
                                                                                                CTRLSRN=old_srn,
                                                                                                CTRLSN=old_sn))

        if hasattr(ne_tree, "RETSUBUNIT"):
            ne_tree["RETSUBUNIT"] = self.get_moc_list_by_mod(ne_tree["RETSUBUNIT"],
                                                             MOD(CONNCN1=new_cn, CONNSRN1=new_srn, CONNSN1=new_sn).WHERE(
                                                    CONNCN1=old_cn, CONNSRN1=old_srn, CONNSN1=old_sn))
            ne_tree["RETSUBUNIT"] = self.get_moc_list_by_mod(ne_tree["RETSUBUNIT"],
                                                             MOD(CONNCN2=new_cn, CONNSRN2=new_srn, CONNSN2=new_sn).WHERE(
                                                    CONNCN2=old_cn, CONNSRN2=old_srn, CONNSN2=old_sn))

        for moc in ["TMASUBUNIT", "VANTENNAPORT", "VRET", "VRETSUBUNIT"]:
            if hasattr(ne_tree, moc) == False: continue
            ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc],
                                                    MOD(CONNCN=new_cn, CONNSRN=new_srn, CONNSN=new_sn).WHERE(CONNCN=old_cn,
                                                                                                CONNSRN=old_srn,
                                                                                                CONNSN=old_sn))

        if hasattr(ne_tree, "SECTOREQM"):
            ne_tree.SECTOREQM = self.get_moc_list_by_mod(ne_tree.SECTOREQM,
                                                         MOD(RRUCN=new_cn, RRUSRN=new_srn, RRUSN=new_sn).WHERE(RRUCN=old_cn,
                                                                                                  RRUSRN=old_srn,
                                                                                                  RRUSN=old_sn))
            for obj in ne_tree.SECTOREQM:
                if hasattr(obj, "SECTOREQMANTENNA") == False: continue
                obj.SECTOREQMANTENNA = self.get_moc_list_by_mod(obj.SECTOREQMANTENNA,
                                                                MOD(CN=new_cn, SRN=new_srn, SN=new_sn).WHERE(CN=old_cn, SRN=old_srn,
                                                                                                SN=old_sn))

        if hasattr(ne_tree, "SECTOR"):
            for obj in ne_tree.SECTOR:
                if hasattr(obj, "SECTORANTENNA") == False: continue
                obj.SECTORANTENNA = self.get_moc_list_by_mod(obj.SECTORANTENNA,
                                                             MOD(CN=new_cn, SRN=new_srn, SN=new_sn).WHERE(CN=old_cn, SRN=old_srn,
                                                                                             SN=old_sn))

        self.print_msg("Info: Move RXU from %d-%d-%d to %d-%d-%d" % (old_cn, old_srn, old_sn, new_cn, new_srn, new_sn))
        pass

    # Modify RRU Subrack
    @API_RECORD
    def modify_RRU_Subrack(self, ne_tree, old_srn, new_srn):
        self.move_RXU(ne_tree, (0, old_srn, 0), (0, new_srn, 0))
        pass

    @API_RECORD
    def modify_SectorEqmID(self, ne_tree, old_id, new_id):
        if ne_tree is None: return
        ne_name = ne_tree["NE"][0].NENAME if "NE" in ne_tree else ""
        self.print_msg("Info: Modify SECTOREQMID from %d to %d for NE=%s" % (old_id, new_id, ne_name))
        ne_tree.SECTOREQM = self.get_moc_list_by_mod(ne_tree.SECTOREQM, MOD(SECTOREQMID=new_id).WHERE(SECTOREQMID=old_id))
        for mo in ["eUCellSectorEqm", "EuPrbSectorEqm", "NRDUCellTrp", "NRDUCellCoverage", "RFACellSectorEqm", "PrbSectorEqmGrpItem"]:
            if hasattr(ne_tree, mo) is False: continue
            if len(ne_tree[mo]) == 0: continue
            ne_tree[mo] = self.get_moc_list_by_mod(ne_tree[mo], MOD(SectorEqmId=new_id).WHERE(SectorEqmId=old_id))
        for mo in ["ULOCELLSECTOREQM", "GTRXGROUPSECTOREQM"]:
            if hasattr(ne_tree, mo) is False: continue
            if len(ne_tree[mo]) == 0: continue
            ne_tree[mo] = self.get_moc_list_by_mod(ne_tree[mo], MOD(SECTOREQMID=new_id).WHERE(SECTOREQMID=old_id))
        pass

    @API_RECORD
    def modify_SectorID(self, ne_tree, old_id, new_id):
        self.print_msg("Info: Modify SECTORID from %d to %d" % (old_id, new_id))
        ne_tree.SECTOR = self.get_moc_list_by_mod(ne_tree.SECTOR, MOD(SECTORID=new_id).WHERE(SECTORID=old_id))
        ne_tree.SECTOREQM = self.get_moc_list_by_mod(ne_tree.SECTOREQM, MOD(SECTORID=new_id).WHERE(SECTORID=old_id))
        pass

    @API_RECORD
    def modify_RRUChainNo(self, ne_tree, old_id, new_id):
        self.print_msg( "Info: Modify RRUCHAIN NO from %d to %d" % (old_id, new_id))
        for moc in ["RRUCHAIN", "RRU", "RFU", "RHUB", "AAMU", "CXU"]:
            ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(RCN=new_id).WHERE(RCN=old_id))
        pass

    @API_RECORD
    def modify_BaseBandEqmID(self, ne_tree, old_id, new_id):
        self.print_msg( "Info: Modify BASEBANDEQMID(MOC=BASEBANDEQM) from %d to %d" % (old_id, new_id))
        ne_tree.BASEBANDEQM = self.get_moc_list_by_mod(ne_tree.BASEBANDEQM, MOD(BASEBANDEQMID=new_id).WHERE(BASEBANDEQMID=old_id))
        if hasattr(ne_tree, "GLOCELL"):
            ne_tree.GLOCELL = self.get_moc_list_by_mod(ne_tree.GLOCELL, MOD(BASEBANDEQMID=new_id).WHERE(BASEBANDEQMID=old_id))
        if hasattr(ne_tree, "ULOCELL"):
            ne_tree.ULOCELL = self.get_moc_list_by_mod(ne_tree.ULOCELL, MOD(ULBASEBANDEQMID=new_id).WHERE(ULBASEBANDEQMID=old_id))
            ne_tree.ULOCELL = self.get_moc_list_by_mod(ne_tree.ULOCELL, MOD(DLBASEBANDEQMID=new_id).WHERE(DLBASEBANDEQMID=old_id))
        if hasattr(ne_tree, "NODEBBASEBANDEQMPARA"):
            ne_tree.NODEBBASEBANDEQMPARA = self.get_moc_list_by_mod(ne_tree.NODEBBASEBANDEQMPARA,
                                                                    MOD(BASEBANDEQMID=new_id).WHERE(BASEBANDEQMID=old_id))
        for moc in ["eUCellSectorEqm", "EuSectorEqmGroup", "SfnAuxResBind", "SfnAuxResGrpBind", "BbpCollaborateGrp",
                    "BbpCollaborationGrp"]:
            if hasattr(ne_tree, moc) == False: continue
            ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(BASEBANDEQMID=new_id).WHERE(BASEBANDEQMID=old_id))
        if hasattr(ne_tree, "EuCellPriBBEqm"):
            ne_tree.EuCellPriBBEqm = self.get_moc_list_by_mod(ne_tree.EuCellPriBBEqm,
                                                              MOD(PriBaseBandEqmId=new_id).WHERE(PriBaseBandEqmId=old_id))
        pass

    @API_RECORD
    def modify_EPGroupID(self, ne_tree, old_id, new_id):
        self.print_msg("Info: Modify EPGROUPID(MOC=EPGROUP) from %d to %d" % (old_id, new_id))
        ne_tree.EPGROUP = self.get_moc_list_by_mod(ne_tree.EPGROUP, MOD(EPGROUPID=new_id).WHERE(EPGROUPID=old_id))
        if hasattr(ne_tree, "gNBCUXn"):
            ne_tree.gNBCUXn = self.get_moc_list_by_mod(ne_tree.gNBCUXn, MOD(CpEpGroupId=new_id).WHERE(CpEpGroupId=old_id))
            ne_tree.gNBCUXn = self.get_moc_list_by_mod(ne_tree.gNBCUXn, MOD(UpEpGroupId=new_id).WHERE(UpEpGroupId=old_id))
        if hasattr(ne_tree, "gNBCUS1"):
            ne_tree.gNBCUS1 = self.get_moc_list_by_mod(ne_tree.gNBCUS1, MOD(CpEpGroupId=new_id).WHERE(CpEpGroupId=old_id))
            ne_tree.gNBCUS1 = self.get_moc_list_by_mod(ne_tree.gNBCUS1, MOD(UpEpGroupId=new_id).WHERE(UpEpGroupId=old_id))
        if hasattr(ne_tree, "gNBCUX2"):
            ne_tree.gNBCUX2 = self.get_moc_list_by_mod(ne_tree.gNBCUX2, MOD(CpEpGroupId=new_id).WHERE(CpEpGroupId=old_id))
            ne_tree.gNBCUX2 = self.get_moc_list_by_mod(ne_tree.gNBCUX2, MOD(UpEpGroupId=new_id).WHERE(UpEpGroupId=old_id))
        if hasattr(ne_tree, "S1"):
            ne_tree.S1 = self.get_moc_list_by_mod(ne_tree.S1, MOD(CpEpGroupId=new_id).WHERE(CpEpGroupId=old_id))
            ne_tree.S1 = self.get_moc_list_by_mod(ne_tree.S1, MOD(UpEpGroupId=new_id).WHERE(UpEpGroupId=old_id))
        if hasattr(ne_tree, "X2"):
            ne_tree.X2 = self.get_moc_list_by_mod(ne_tree.X2, MOD(CpEpGroupId=new_id).WHERE(CpEpGroupId=old_id))
            ne_tree.X2 = self.get_moc_list_by_mod(ne_tree.X2, MOD(UpEpGroupId=new_id).WHERE(UpEpGroupId=old_id))
        if hasattr(ne_tree, "SCTPHOST"):
            for sctphost_obj in ne_tree.SCTPHOST:
                if sctphost_obj.SIMPLEMODESWITCH == 0: continue
                if sctphost_obj.CPEPGROUPID1 == old_id: sctphost_obj.CPEPGROUPID1 = new_id
                if sctphost_obj.UPEPGROUPID1 == old_id: sctphost_obj.UPEPGROUPID1 = new_id
                if sctphost_obj.CPEPGROUPID2 == old_id: sctphost_obj.CPEPGROUPID1 = new_id
                if sctphost_obj.UPEPGROUPID2 == old_id: sctphost_obj.UPEPGROUPID1 = new_id
        if hasattr(ne_tree, "SCTPPEER"):
            ne_tree.SCTPPEER = self.get_moc_list_by_mod(ne_tree.SCTPPEER, MOD(EPGROUPID=new_id).WHERE(EPGROUPID=old_id))
        if hasattr(ne_tree, "IUB"):
            ne_tree.IUB = self.get_moc_list_by_mod(ne_tree.IUB, MOD(UPEPGROUPID=new_id).WHERE(UPEPGROUPID=old_id))
        if hasattr(ne_tree, "ABIS"):
            ne_tree.ABIS = self.get_moc_list_by_mod(ne_tree.ABIS, MOD(UPEPGRPID=new_id).WHERE(UPEPGRPID=old_id))
        pass

    # 解决多个NE之间ID冲突
    @API_RECORD
    def solve_ID_Conflict_Before_Merge(self, ne_tree=None, ne_tree2=None, ne_tree3=None, ne_tree4=None):
        # 对传入的ne_tree_list的第一个tree，进行ID冲突检测
        @API_RECORD
        def inner_get_conflict_id_list(ne_tree_list, moc, id_para):
            list1 = self.get_para_list_from_moc(ne_tree_list[0][moc], id_para) if moc in ne_tree_list[0] else []
            list2 = []
            for ne_tree in ne_tree_list[1:]:
                if ne_tree:
                    tmp_list = self.get_para_list_from_moc(ne_tree[moc], id_para) if moc in ne_tree else []
                    list2.extend(tmp_list)

            if type(id_para) == list and len(id_para) > 1:  # 当传入的是多个参数，把结果转换为tuple，方便下面set操作
                list1 = [tuple(s) for s in list1]
                list2 = [tuple(s) for s in list2]
            all_id_list = set(list1).union(set(list2))
            same_id_list = set(list1).intersection(set(list2))
            return all_id_list, same_id_list

        # 对传入的ne_tree_list的第一个tree, 检查ID冲突，并修改ID解决冲突
        @API_RECORD
        def inner_solve_id_conflict_for_1st_tree(ne_tree_list):
            ne_tree = ne_tree_list[0]
            if ne_tree is None: return
            ne_name = ne_tree["NE"][0].NENAME if "NE" in ne_tree else ""
            # SCTP
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "SCTPLNK", "SCTPNO")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.print_msg("Info: Modify SCTPNO(MOC=SCTPLNK) from %d to %d for NE=%s" % (old_id, new_id, ne_name))
                    ne_tree.SCTPLNK = self.get_moc_list_by_mod(ne_tree.SCTPLNK, MOD(SCTPNO=new_id).WHERE(SCTPNO=old_id))
                    if hasattr(ne_tree, "CPBEARER"):
                        ne_tree.CPBEARER = self.get_moc_list_by_mod(ne_tree.CPBEARER, MOD(LINKNO=new_id).WHERE(LINKNO=old_id))
                    if len(need_modify_id_list) == 0: break
                pass

            # CPBEARER
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "CPBEARER", "CPBEARID")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.print_msg("Info: Modify CPBEARID(MOC=CPBEARER) from %d to %d for NE=%s" % (old_id, new_id, ne_name))
                    ne_tree.CPBEARER = self.get_moc_list_by_mod(ne_tree.CPBEARER, MOD(CPBEARID=new_id).WHERE(CPBEARID=old_id))
                    if hasattr(ne_tree, "IUBCP"):
                        ne_tree.IUBCP = self.get_moc_list_by_mod(ne_tree.IUBCP, MOD(CPBEARID=new_id).WHERE(CPBEARID=old_id))
                    if hasattr(ne_tree, "GBTSABISCP"):
                        ne_tree.GBTSABISCP = self.get_moc_list_by_mod(ne_tree.GBTSABISCP,
                                                                      MOD(CPBEARID=new_id).WHERE(CPBEARID=old_id))
                    if hasattr(ne_tree, "S1Interface"):
                        ne_tree.S1Interface = self.get_moc_list_by_mod(ne_tree.S1Interface,
                                                                       MOD(S1CpBearerId=new_id).WHERE(S1CpBearerId=old_id))
                    if hasattr(ne_tree, "X2Interface"):
                        ne_tree.X2Interface = self.get_moc_list_by_mod(ne_tree.X2Interface,
                                                                       MOD(X2CpBearerId=new_id).WHERE(X2CpBearerId=old_id))
                    if len(need_modify_id_list) == 0: break

            # IPPATH
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "IPPATH", "PATHID")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.print_msg("Info: Modify IPPATHID(MOC=IPPATH) from %d to %d for NE=%s" % (old_id, new_id, ne_name))
                    ne_tree.IPPATH = self.get_moc_list_by_mod(ne_tree.IPPATH, MOD(PATHID=new_id).WHERE(PATHID=old_id))
                    if hasattr(ne_tree, "eNodeBPath"):
                        ne_tree.eNodeBPath = self.get_moc_list_by_mod(ne_tree.eNodeBPath,
                                                                      MOD(IpPathId=new_id).WHERE(IpPathId=old_id))
                    if hasattr(ne_tree, "CnOperatorIpPath"):
                        ne_tree.CnOperatorIpPath = self.get_moc_list_by_mod(ne_tree.CnOperatorIpPath,
                                                                            MOD(IpPathId=new_id).WHERE(IpPathId=old_id))
                    if hasattr(ne_tree, "NODEBPATH"):
                        ne_tree.NODEBPATH = self.get_moc_list_by_mod(ne_tree.NODEBPATH, MOD(PATHID=new_id).WHERE(PATHID=old_id))
                    if hasattr(ne_tree, "GBTSPATH"):
                        ne_tree.GBTSPATH = self.get_moc_list_by_mod(ne_tree.GBTSPATH, MOD(PATHID=new_id).WHERE(PATHID=old_id))
                    if hasattr(ne_tree, "IPPMSESSION"):
                        ne_tree.IPPMSESSION = self.get_moc_list_by_mod(ne_tree.IPPMSESSION, MOD(PATHID=new_id).WHERE(PATHID=old_id))
                    if len(need_modify_id_list) == 0: break
                pass

            # EPGROUP
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "EPGROUP", "EPGROUPID")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.modify_EPGroupID(ne_tree, old_id, new_id)
                    if len(need_modify_id_list) == 0: break
                pass

            # USERPLANEHOST
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "USERPLANEHOST",
                                                                               "UPHOSTID")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.print_msg("Info: Modify UPHOSTID(MOC=USERPLANEHOST) from %d to %d for NE=%s" % (old_id, new_id, ne_name))
                    ne_tree.USERPLANEHOST = self.get_moc_list_by_mod(ne_tree.USERPLANEHOST,
                                                                     MOD(UPHOSTID=new_id).WHERE(UPHOSTID=old_id))
                    for epgroup_obj in ne_tree.EPGROUP:
                        epgroup_obj.USERPLANEHOSTREFS = self.get_moc_list_by_mod(epgroup_obj.USERPLANEHOSTREFS,
                                                                                 MOD(UPHOSTID=new_id).WHERE(UPHOSTID=old_id))
                    if len(need_modify_id_list) == 0: break
                pass

            # USERPLANEPEER
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "USERPLANEPEER",
                                                                               "UPPEERID")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.print_msg("Info: Modify UPPEERID(MOC=USERPLANEPEER) from %d to %d for NE=%s" % (old_id, new_id, ne_name))
                    ne_tree.USERPLANEPEER = self.get_moc_list_by_mod(ne_tree.USERPLANEPEER,
                                                                     MOD(UPPEERID=new_id).WHERE(UPPEERID=old_id))
                    for epgroup_obj in ne_tree.EPGROUP:
                        epgroup_obj.USERPLANEPEERREFS = self.get_moc_list_by_mod(epgroup_obj.USERPLANEPEERREFS,
                                                                                 MOD(UPPEERID=new_id).WHERE(UPPEERID=old_id))
                    if len(need_modify_id_list) == 0: break
                pass

            # IPRT
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "IPRT", "RTIDX")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.print_msg("Info: Modify RTIDX(IPRT) from %d to %d for NE=%s" % (old_id, new_id, ne_name))
                    ne_tree.IPRT = self.get_moc_list_by_mod(ne_tree.IPRT, MOD(RTIDX=new_id).WHERE(RTIDX=old_id))
                    if hasattr(ne_tree, "OMCH"):
                        ne_tree.OMCH = self.get_moc_list_by_mod(ne_tree.OMCH, MOD(RTIDX=new_id).WHERE(RTIDX=old_id))
                    if len(need_modify_id_list) == 0: break
                pass

            # SRCIPRT
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "SRCIPRT", "SRCRTIDX")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.print_msg("Info: Modify SRCRTIDX(MOC=SRCIPRT) from %d to %d for NE=%s" % (old_id, new_id, ne_name))
                    ne_tree.SRCIPRT = self.get_moc_list_by_mod(ne_tree.SRCIPRT, MOD(SRCRTIDX=new_id).WHERE(SRCRTIDX=old_id))
                    if len(need_modify_id_list) == 0: break
                pass

            # SECTORID
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "SECTOR", "SECTORID")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.print_msg("Info: Modify SECTORID(MOC=SECTOR) from %d to %d for NE=%s" % (old_id, new_id, ne_name))
                    ne_tree.SECTOR = self.get_moc_list_by_mod(ne_tree.SECTOR, MOD(SECTORID=new_id).WHERE(SECTORID=old_id))
                    ne_tree.SECTOREQM = self.get_moc_list_by_mod(ne_tree.SECTOREQM, MOD(SECTORID=new_id).WHERE(SECTORID=old_id))
                    if len(need_modify_id_list) == 0: break
                pass

            # SECTOREQMID
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "SECTOREQM", "SECTOREQMID")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.modify_SectorEqmID(ne_tree, old_id, new_id)
                    if len(need_modify_id_list) == 0: break
                pass

            # BASEBANDEQM
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "BASEBANDEQM",
                                                                               "BASEBANDEQMID")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.modify_BaseBandEqmID(ne_tree, old_id, new_id)
                    if len(need_modify_id_list) == 0: break
                pass

            # RRUCHAIN
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "RRUCHAIN", "RCN")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.print_msg("Info: Modify RCN(MOC=RRUCHAIN) from %d to %d for NE=%s" % (old_id, new_id, ne_name))
                    for moc in ["RRUCHAIN", "RRU", "RFU", "RHUB", "AAMU", "CXU"]:
                        ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(RCN=new_id).WHERE(RCN=old_id))
                    if len(need_modify_id_list) == 0: break
                pass

            # RET
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "RET", "DEVICENO")
            if need_modify_id_list:
                for new_id in range(65535):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.print_msg("Info: Modify DEVICENO(MOC=RET) from %d to %d for NE=%s" % (old_id, new_id, ne_name))
                    for moc in ["RET", "RETDEVICEDATA", "RETSUBUNIT"]:
                        ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(DEVICENO=new_id).WHERE(DEVICENO=old_id))
                    if len(need_modify_id_list) == 0: break
                pass

            # VLANCLASS
            existing_id_list, need_modify_id_list = inner_get_conflict_id_list(ne_tree_list, "VLANCLASS", "VLANGROUPNO")
            if need_modify_id_list:
                for new_id in range(4):
                    if new_id in existing_id_list: continue
                    old_id = need_modify_id_list.pop()
                    self.print_msg( "Info: Modify VLANGROUPNO(MOC=VLANCLASS) from %d to %d for NE=%s" % (old_id, new_id, ne_name))
                    ne_tree["VLANCLASS"] = self.get_moc_list_by_mod(ne_tree["VLANCLASS"],
                                                                    MOD(VLANGROUPNO=new_id).WHERE(VLANGROUPNO=old_id))
                    ne_tree["VLANMAP"] = self.get_moc_list_by_mod(ne_tree["VLANMAP"],
                                                                  MOD(VLANGROUPNO=new_id).WHERE(VLANGROUPNO=old_id))
                    if len(need_modify_id_list) == 0: break
            pass

        # 解决多个tree之前的ID冲突
        ne_tree_list = []
        if ne_tree is None and ne_tree2 is None and ne_tree3 is None and ne_tree4 is None:
            for rat, tree_list in self.Tree_Dict.items():
                ne_tree_list.extend(tree_list)
        else:
            ne_tree_list.extend([ne_tree, ne_tree2, ne_tree3, ne_tree4])
        for i in range(len(ne_tree_list) - 1):
            tmp_ne_tree_list = [ne_tree_list[i]] + ne_tree_list[:i] + ne_tree_list[i + 1:]
            inner_solve_id_conflict_for_1st_tree(tmp_ne_tree_list)
        pass 

    # 对多个Tree进行SDR RXU的合并
    @API_RECORD
    def modify_SDR_RXU(self, ne_tree, ne_tree2=None, ne_tree3=None, ne_tree4=None):
        @API_RECORD
        def inner_modify_sdr_rxu(ne_tree, ne_tree2):
            ne1_name, ne2_name = ne_tree.NE[0].NENAME, ne_tree2.NE[0].NENAME
            for moc in ["RRU", "RFU", "AARU"]:
                sdr_rruchain_list = []
                all_rxu_pos, same_rxu_pos = self.inner_get_id_list(ne_tree, ne_tree2, moc, ["CN", "SRN", "SN"])
                for (cn, srn, sn) in same_rxu_pos:  # RXU框号相同
                    # rs1, rcn1 = self.get_para_list_from_moc(ne_tree[moc], [moc, "RCN"], WHERE(CN=cn, SRN=srn, SN=sn))[0]
                    # rs2, rcn2 = self.get_para_list_from_moc(ne_tree2[moc], [moc, "RCN"], WHERE(CN=cn, SRN=srn, SN=sn))[0]
                    rs1, rcn1 = self.get_para_list_from_moc(ne_tree[moc], ["RS", "RCN"], WHERE(CN=cn, SRN=srn, SN=sn))[0]
                    rs2, rcn2 = self.get_para_list_from_moc(ne_tree2[moc], ["RS", "RCN"], WHERE(CN=cn, SRN=srn, SN=sn))[0]
                    if rs1 == rs2:  # 柜框槽号相同，且工作制式相同，认为是同一块单板
                        sdr_rruchain_list.append((cn, srn, sn, rcn1, rcn2))
                    else:
                        work_mode1 = MODEL.RRU.RS.toString(rs1)
                        work_mode2 = MODEL.RRU.RS.toString(rs2)
                        print(
                        "Error: RXU=%d-%d-%d Same Subrack but Work_Mode different(%s, %s). Please modify subrack first"
                        % (cn, srn, sn, work_mode1, work_mode2))

                # 修改SDR模块的RRUCHAIN
                for (cn, srn, sn, rcn1, rcn2) in sdr_rruchain_list:
                    at1, bbp_cn1, bbp_srn1, bbp_sn1, bbp_pn1 = \
                    self.get_para_list_from_moc(ne_tree.RRUCHAIN, ["AT", "HCN", "HSRN", "HSN", "HPN"], WHERE(RCN=rcn1))[0]
                    at2, bbp_cn2, bbp_srn2, bbp_sn2, bbp_pn2 = \
                    self.get_para_list_from_moc(ne_tree2.RRUCHAIN, ["AT", "HCN", "HSRN", "HSN", "HPN"], WHERE(RCN=rcn2))[0]
                    if at1 == 1:  # PEERPORT
                        self.print_msg("Info: Delete RCN=%d RXU=%d-%d-%d for NE=%s" % (rcn1, cn, srn, sn, ne1_name))
                        ne_tree.RRUCHAIN = self.get_moc_list_by_del(ne_tree.RRUCHAIN, WHERE(RCN=rcn1))
                        ne_tree[moc] = self.get_moc_list_by_del(ne_tree[moc], WHERE(CN=cn, SRN=srn, SN=sn))
                        ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(RCN=rcn2).WHERE(RCN=rcn1))
                    elif at2 == 1:  # PEERPORT
                        self.print_msg( "Info: Delete RCN=%d RXU=%d-%d-%d for NE=%s" % (rcn2, cn, srn, sn, ne2_name))
                        ne_tree2.RRUCHAIN = self.get_moc_list_by_del(ne_tree2.RRUCHAIN, WHERE(RCN=rcn2))
                        ne_tree2[moc] = self.get_moc_list_by_del(ne_tree2[moc], WHERE(CN=cn, SRN=srn, SN=sn))
                        ne_tree2[moc] = self.get_moc_list_by_mod(ne_tree2[moc], MOD(RCN=rcn1).WHERE(RCN=rcn2))
                    elif (bbp_cn1, bbp_srn1, bbp_sn1) == (bbp_cn2, bbp_srn2, bbp_sn2):  # 端口相同
                        self.print_msg( "Info: Delete RCN=%d RXU=%d-%d-%d for NE=%s" % (rcn2, cn, srn, sn, ne2_name))
                        ne_tree2.RRUCHAIN = self.get_moc_list_by_del(ne_tree2.RRUCHAIN, WHERE(RCN=rcn2))
                        ne_tree2[moc] = self.get_moc_list_by_del(ne_tree2[moc], WHERE(CN=cn, SRN=srn, SN=sn))
                        ne_tree2[moc] = self.get_moc_list_by_mod(ne_tree2[moc], MOD(RCN=rcn1).WHERE(RCN=rcn2))
                    else:  # 修改为LOADBALANCE
                        self.print_msg( "Info: Delete RCN=%d RXU=%d-%d-%d for NE=%s" % (rcn1, cn, srn, sn, ne1_name))
                        self.print_msg( "Info: Modify RCN=%d to Load-Balance for NE=%s" % (rcn2, ne2_name))
                        ne_tree.RRUCHAIN = self.get_moc_list_by_del(ne_tree.RRUCHAIN, WHERE(RCN=rcn1))
                        ne_tree[moc] = self.get_moc_list_by_del(ne_tree[moc], WHERE(CN=cn, SRN=srn, SN=sn))
                        ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(RCN=rcn2).WHERE(RCN=rcn1))
                        ne_tree2.RRUCHAIN = self.get_moc_list_by_mod(ne_tree2.RRUCHAIN,
                                                                     MOD(TT=2, TCN=bbp_cn1, TSRN=bbp_srn1, TSN=bbp_sn1,
                                                            TPN=bbp_pn1).WHERE(RCN=rcn2))
            pass

        ne_tree_list = [ne_tree, ne_tree2, ne_tree3, ne_tree4]
        for i in range(len(ne_tree_list) - 1):
            for j in range(i + 1, len(ne_tree_list)):
                ne_tree = ne_tree_list[i]
                ne_tree2 = ne_tree_list[j]
                if ne_tree and ne_tree2:
                    inner_modify_sdr_rxu(ne_tree, ne_tree2)
        pass

    # 检查是否同时存在于两个tree的RXU，如果存在，进行Sector配置的合并
    @API_RECORD
    def modify_Sector(self, ne_tree, ne_tree2=None, ne_tree3=None, ne_tree4=None):
        @API_RECORD
        def inner_get_rxuport_sector_map(sector_obj_list):
            rxuport_sector_map = {}
            for sector_obj in sector_obj_list:
                sector_id = sector_obj.SECTORID
                for ant_obj in sector_obj.SECTORANTENNA:
                    rxuport_sector_map[(ant_obj.CN, ant_obj.SRN, ant_obj.SN, ant_obj.ANTN)] = sector_id
            return rxuport_sector_map

        @API_RECORD
        def inner_merge_sector(ne_tree, ne_tree2, sector_id, sector_id2):  # 合并Sector的填写数据
            ant_list1 = self.get_para_list_from_moc(ne_tree.SECTOR, "SECTORANTENNA", WHERE(SECTORID=sector_id))[0]
            ant_list2 = self.get_para_list_from_moc(ne_tree2.SECTOR, "SECTORANTENNA", WHERE(SECTORID=sector_id2))[0]
            ant_obj_list = []
            added_ant_list = []
            for ant_obj in ant_list1 + ant_list2:
                ant_info = ant_obj.CN, ant_obj.SRN, ant_obj.SN, ant_obj.ANTN
                if ant_info in added_ant_list: continue
                added_ant_list.append(ant_info)
                ant_obj_list.append(ant_obj)
            ne_tree2.SECTOR = self.get_moc_list_by_mod(ne_tree2.SECTOR, MOD(SECTORANTENNA=ant_obj_list).WHERE(SECTORID=sector_id2))
            ne_tree.SECTOR = self.get_moc_list_by_del(ne_tree.SECTOR, WHERE(SECTORID=sector_id))
            ne_tree.SECTOREQM = self.get_moc_list_by_mod(ne_tree.SECTOREQM, MOD(SECTORID=sector_id2).WHERE(SECTORID=sector_id))

        @API_RECORD
        def inner_modify_sector(ne_tree, ne_tree2):
            # 建立RXU端口和扇区ID的对应关系
            sectorid_map = {}
            rxuport_sector_map1 = inner_get_rxuport_sector_map(ne_tree.SECTOR)
            rxuport_sector_map2 = inner_get_rxuport_sector_map(ne_tree2.SECTOR)
            for ((cn, srn, sn, antn), sector_id) in rxuport_sector_map1.items():
                if (cn, srn, sn, antn) in rxuport_sector_map2:  # RXU模块相同的，认为是同一扇区
                    sector_id2 = rxuport_sector_map2[(cn, srn, sn, antn)]
                    if sector_id != sector_id2:  # 同RRU模块，SECTORID不同
                        sectorid_map[sector_id] = sector_id2

            while len(sectorid_map) > 0:
                old_sectorid_list = list(sectorid_map.keys())
                new_sectorid_list = list(sectorid_map.values())
                non_conflict_list = list(set(new_sectorid_list).difference(set(old_sectorid_list)))
                if len(non_conflict_list) == 0: break  # 剩下的，无法再挪
                new_sectorid = non_conflict_list[0]
                old_sectorid = old_sectorid_list[new_sectorid_list.index(new_sectorid)]
                if "NODE" in ne_tree:
                    self.print_msg("Info: Modify SECTORID from %s to %s for %s" % (
                    old_sectorid, new_sectorid, ne_tree.NODE[0].NODENAME))
                inner_merge_sector(ne_tree, ne_tree2, old_sectorid, new_sectorid)
                del sectorid_map[old_sectorid]

            # 对相同的SectorID，进行合并
            sectorid_list1 = self.get_para_list_from_moc(ne_tree["SECTOR"], "SECTORID")
            sectorid_list2 = self.get_para_list_from_moc(ne_tree2["SECTOR"], "SECTORID")
            same_sectorid_list = list(set(sectorid_list1).intersection(set(sectorid_list2)))
            for sectorid in same_sectorid_list:
                inner_merge_sector(ne_tree, ne_tree2, sectorid, sectorid)
            pass

        ne_tree_list = [ne_tree, ne_tree2, ne_tree3, ne_tree4]
        for i in range(len(ne_tree_list) - 1):
            for j in range(i + 1, len(ne_tree_list)):
                t_ne_tree = ne_tree_list[i]
                t_ne_tree2 = ne_tree_list[j]
                if t_ne_tree and t_ne_tree2:
                    if hasattr(t_ne_tree, "SECTOR") == False: continue
                    if hasattr(t_ne_tree2, "SECTOR") == False: continue
                    inner_modify_sector(t_ne_tree, t_ne_tree2)
        pass

    @API_RECORD
    def modify_SectorID_Based_On_Plan(self, ne_tree, Band_Sector_To_SectorId_map, sector_id_plan_map):
        id_replace_map = {}
        reverse_id_map = {}
        for band_str in Band_Sector_To_SectorId_map:
            for (sector_str, id_list) in Band_Sector_To_SectorId_map[band_str].items():
                id_list = list(set(id_list))
                id_list.sort()
                plan_id_list = sector_id_plan_map[band_str]["SECTOR_%s" % sector_str]
                for (i, id) in enumerate(id_list):
                    new_id = int(plan_id_list[i])
                    id_replace_map[id] = new_id
                    if new_id not in reverse_id_map:
                        reverse_id_map[new_id] = []
                    reverse_id_map[new_id].append(id)

        get_new_sectorid = lambda sector_obj: id_replace_map[sector_obj.SECTORID]
        ne_tree["SECTOR"] = self.get_moc_list_by_mod(ne_tree["SECTOR"],
                                                     MOD(SECTORID=get_new_sectorid).WHERE(lambda o: o.SECTORID in id_replace_map))
        ne_tree["SECTOREQM"] = self.get_moc_list_by_mod(ne_tree["SECTOREQM"],
                                                        MOD(SECTORID=get_new_sectorid).WHERE(lambda o: o.SECTORID in id_replace_map))

        # 检查是否存在相同的SectorID，如果存在，进行合并
        sector_obj_list = []
        for sector_obj in ne_tree["SECTOR"]:
            sectorid = sector_obj.SECTORID
            if sectorid not in reverse_id_map: continue
            id_list = reverse_id_map[sectorid]
            if len(id_list) >= 2:
                ant_obj_list = []
                sector_obj_temp_list = filter(lambda obj: obj.SECTORID == sectorid, ne_tree["SECTOR"])
                for obj in sector_obj_temp_list:
                    ant_list1 = obj.SECTORANTENNA
                    ant_list2 = sector_obj.SECTORANTENNA
                    ant_obj_list = []
                    added_ant_list = []
                    for ant_obj in ant_list1 + ant_list2:
                        ant_info = ant_obj.CN, ant_obj.SRN, ant_obj.SN, ant_obj.ANTN
                        if ant_info in added_ant_list: continue
                        added_ant_list.append(ant_info)
                        ant_obj_list.append(ant_obj)
                sector_obj.SECTORANTENNA = ant_obj_list
                pass
            sector_obj_list.append(sector_obj)
            del reverse_id_map[sectorid]
        pass

    # 按照中国移动的规范修改RRU框号
    @API_RECORD
    def modify_RRU_Subrack_Custom_For_China_Mobile(self, ne_tree):
        @API_RECORD
        def get_rru_subrack_by_cpri_port(bbp_slot, bbp_port, ps):
            if bbp_slot == 0:
                srn = 150 + ps * 6 + bbp_port
            elif bbp_slot == 1:
                srn = 174 + ps * 6 + bbp_port
            elif bbp_slot == 2:
                if bbp_port < 3:
                    srn = 60 + ps * 3 + bbp_port
                else:
                    srn = 81 + ps * 3 + bbp_port - 3
            elif bbp_slot == 3:
                if int(bbp_port) < 3:
                    srn = 90 + ps * 3 + bbp_port
                else:
                    srn = 111 + ps * 3 + bbp_port - 3
            elif bbp_slot == 4:
                srn = 200 + ps * 6 + bbp_port
            elif bbp_slot == 5:
                srn = 224 + ps * 6 + bbp_port
            else:
                pass
            return srn

        replace_rru_subrack_map = {}  # 建立RRU框号修改的前后对应关系
        for rru_obj in ne_tree.RRU:
            cn, srn, sn = rru_obj.CN, rru_obj.SRN, rru_obj.SN
            rcn = rru_obj.RCN
            bbp_slot_port_list = self.get_para_list_from_moc(ne_tree.RRUCHAIN, ["HSN", "HPN"], WHERE(RCN=rcn))
            if len(bbp_slot_port_list) == 0:
                self.print_msg("Error: NO RRU with RCN=%d" % rcn)
                continue
            bbp_slot, bbp_port = bbp_slot_port_list[0]
            ps = rru_obj.PS
            new_srn = get_rru_subrack_by_cpri_port(bbp_slot, bbp_port, ps)
            if new_srn != srn:
                replace_rru_subrack_map[srn] = new_srn

        # 替换框号
        srn_update_list = []
        while len(replace_rru_subrack_map) > 0:
            old_srn_list = replace_rru_subrack_map.keys()
            new_srn_list = replace_rru_subrack_map.values()
            non_conflict_list = list(set(new_srn_list).difference(set(old_srn_list)))
            if len(non_conflict_list) == 0: break  # 剩下的，无法再挪
            new_srn = non_conflict_list[0]
            old_srn = old_srn_list[new_srn_list.index(new_srn)]
            self.modify_RRU_Subrack(ne_tree, old_srn, new_srn)
            if new_srn not in srn_update_list:
                srn_update_list.append(new_srn)
            self.print_msg("Info: Change RRU subrack from %s to %s" % (old_srn, new_srn))
            del replace_rru_subrack_map[old_srn]
        pass

    # 从BSC获得基站的RXU Info信息
    ##cellname_to_sector_map保存小区名和所在物理扇区对应关系，如{"test-1":"A", "test-2":"B", "test-3":"C"}
    @API_RECORD
    def get_GBTS_RXU_Info(self, btsinfo):
        if btsinfo["BTSTYPE"] not in ["DBS3900_GSM", "BTS3900_GSM", "BTS3900A_GSM", "BTS3900L_GSM", "BTS3900AL_GSM"]:
            print("Error: GBTS=%s is not 3900 site. Cannot get RXU Info" % btsinfo["BTSNAME"])
            return None

        for ((cn, srn, sn), rxuinfo) in btsinfo["RXU_INFO"].items():
            rxuinfo["CN-SRN-SN"] = "%s-%s-%s" % (cn, srn, sn)
            if "RXUSPEC" not in rxuinfo:
                pass
            else:
                rxuspec = rxuinfo["RXUSPEC"]
                if rxuspec == "BYNAME":
                    rxuinfo["RXUSPEC"] = rxuinfo["RXUSPECNAME"][1:-1]
                elif rxuspec == "BYVALUE":  # 怎么获取???
                    pass
                elif "Reserved" not in rxuspec:
                    rxuinfo["RXUSPEC"] = rxuspec
                else:  # Reserve，无法识别
                    pass

            rxuinfo["RCN"] = rxuinfo["RXUCHAINNO"]
            rcn_paras = btsinfo["RCN_INFO"][rxuinfo["RXUCHAINNO"]]
            rxuinfo["CPRI_BBP_PORT1"] = "%s-%s-%s-%s" % (
            rcn_paras["HCN"], rcn_paras["HSRN"], rcn_paras["HSN"], rcn_paras["HPN"])
            if rcn_paras["TT"] == 1:  # RING
                rxuinfo["CPRI_BBP_PORT2"] = "%s-%s-%s-%s" % (
                rcn_paras["TCN"], rcn_paras["TSRN"], rcn_paras["TSN"], rcn_paras["TPN"])
            else:
                rxuinfo["CPRI_BBP_PORT2"] = None
            rxuinfo["PS"] = str(int(rxuinfo["RXUPOS"]) - 1)

            cellid_list = list(set(rxuinfo["CELLID_LIST"]))
            if len(cellid_list) > 0:
                rxuinfo["SECTOR_NO"] = [btsinfo["CELL_INFO"][cellid]["SECTOR_NO"] for cellid in cellid_list]
                rxuinfo["TRX_NUM"] = len(rxuinfo["TRXID_LIST"])
            else:
                rxuinfo["TRX_NUM"] = 0

            if rxuinfo["RXUTYPE"] in ["DRRU", "DRFU", "GRFU", "GRRU"]:
                work_mode = "G"
            else:
                work_mode_map = {"GSM_AND_UMTS": "GU", "GSM": "G", "GSM_AND_LTE": "GL", "GSM_AND_UMTS_AND_LTE": "GUL",
                                 "GSM_AND_NBIOT": "GM", "GSM_AND_UMTS_AND_NBIOT": "GUM", "GSM_AND_LTE_AND_NBIOT": "GLM",
                                 "GSM_AND_UMTS_AND_LTE_AND_NBIOT": "GULM"}
                work_mode = work_mode_map[rxuinfo["WORKINGSTANDARD"]]
            rxuinfo["WORK_MODE"] = work_mode

            rxuinfo["VSWR_THD_LV1"] = rxuinfo["LVL1VSWR"]
            rxuinfo["VSWR_THD_LV2"] = rxuinfo["LVL2VSWR"]

            # 根据收发模式，获得RXU的发射端口号
            send_rcv_mod = rxuinfo["TxRxMode"] if "TxRxMode" in rxuinfo else None
            port_assign_mode = rxuinfo["PORT_ASSIGN_MODE"] if "PORT_ASSIGN_MODE" in rxuinfo else None

            if send_rcv_mod is None:
                continue
            elif send_rcv_mod == "SGL_ANTENNA":  # SGL_ANTENNA
                rxuinfo["TX_RX_NUM"] = (1, 2)
            elif send_rcv_mod == "SGLDOUBLE_ANTENNA":  # ，双拼
                rxuinfo["TX_RX_NUM"] = (1, 2)
            elif send_rcv_mod == "DOUBLE_ANTENNA":  #
                rxuinfo["TX_RX_NUM"] = (2, 2)
            elif send_rcv_mod == "DOUBLEFOUR_ANTENNA":  # , 双拼
                rxuinfo["TX_RX_NUM"] = (2, 2)
            elif send_rcv_mod == "DOUBLESINGLE_ANTENNA":  #
                rxuinfo["TX_RX_NUM"] = (1, 2)
            elif send_rcv_mod == "DOUBLEDOUBLE_ANTENNA":  #
                rxuinfo["TX_RX_NUM"] = (1, 2)
            elif send_rcv_mod == "FOURDOUBLE_ANTENNA":  #
                rxuinfo["TX_RX_NUM"] = (2, 4)
            elif send_rcv_mod == "FOURDOUBLEFOUR_ANTENNA":  #
                rxuinfo["TX_RX_NUM"] = (2, 4)
            elif send_rcv_mod == "THREEDOUBLEFOUR_ANTENNA":  # , 劈裂场景，一个RRU用于两个扇区
                rxuinfo["TX_RX_NUM"] = (2, 4)
            elif send_rcv_mod == "FOURDOUBLE_ANTENNA_NOTCOMMON":  #
                rxuinfo["TX_RX_NUM"] = (2, 4)
            elif send_rcv_mod == "FOUR_ANTENNA_A_B_C_D":  #
                rxuinfo["TX_RX_NUM"] = (4, 4)
            elif send_rcv_mod == "FOUR_ANTENNA_AB_CD_SEP_INTRA":  #
                rxuinfo["TX_RX_NUM"] = (4, 4)
            elif send_rcv_mod == "FOUR_ANTENNA_AC_BD_SEP_INTRA":  #
                rxuinfo["TX_RX_NUM"] = (4, 4)
            elif send_rcv_mod == "FOUR_ANTENNA_AB_CD_SEP_INTER":  #
                rxuinfo["TX_RX_NUM"] = (4, 4)
            elif send_rcv_mod == "FOUR_ANTENNA_AC_BD_SEP_INTER":  #
                rxuinfo["TX_RX_NUM"] = (4, 4)
            elif send_rcv_mod == "FOUR_ANTENNA_AB_CD":  #
                rxuinfo["TX_RX_NUM"] = (4, 4)
            elif send_rcv_mod == "FOUR_ANTENNA_AC_BD":  #
                rxuinfo["TX_RX_NUM"] = (4, 4)
            elif send_rcv_mod == "BY_ANTGRP":  #
                print("Error: Send_Rcv_Mode=BY_ANTGRP is not support")

            # 对没有绑定TRX的小区，且是双拼场景，尝试寻找另一个RXU，并获得另外一个RXU的扇区和频段
            if "SECTOR_NO" not in rxuinfo:
                print("Warning: no TRX bind to RXU=%d-%d-%d." % (cn, srn, sn))
                # 没有TRX绑定到RXU上，不能获得RXU的频段和扇区信息，如何处理？？？
                if send_rcv_mod in ["SGLDOUBLE_ANTENNA", "DOUBLEFOUR_ANTENNA"]:  # 双拼场景
                    inter_rxu = None
                    if int(srn) >= 60:  # RRU场景
                        if (cn, str(int(srn) - 1), sn) in btsinfo["RXU_INFO"] and \
                                        btsinfo["RXU_INFO"][(cn, str(int(srn) - 1), sn)][
                                            "PORT_ASSIGN_MODE"] == port_assign_mode:
                            inter_rxu = (cn, str(int(srn) - 1), sn)
                    else:
                        if (cn, srn, str(int(sn) - 1)) in btsinfo["RXU_INFO"] and \
                                        btsinfo["RXU_INFO"][(cn, srn, str(int(sn) - 1))][
                                            "PORT_ASSIGN_MODE"] == port_assign_mode:
                            inter_rxu = (cn, srn, str(int(sn) - 1))
                    if inter_rxu:
                        self.print_msg("  ...Try use RXU=%s-%s-%s as Inter-Connect RXU." % inter_rxu)
                        btsinfo["RXU_INFO"][(cn, srn, sn)]["SECTOR_NO"] = btsinfo["RXU_INFO"][inter_rxu]["SECTOR_NO"]
                        btsinfo["RXU_INFO"][(cn, srn, sn)]["BAND"] = btsinfo["RXU_INFO"][inter_rxu]["BAND"]

            if "SECTOR_NO" not in btsinfo["RXU_INFO"][(cn, srn, sn)]:
                self.print_msg( "Fail to Get SECTOR_NO/BAND for RXU=%d-%d-%d." % (cn, srn, sn))
            else:
                sector_list = btsinfo["RXU_INFO"][(cn, srn, sn)]["SECTOR_NO"]
                if len(sector_list) > 1:  # 一个RRU用于两个扇区
                    btsinfo["RXU_INFO"][(cn, srn, sn)]["WORK_MODE"] = work_mode + "&" + work_mode
                    btsinfo["RXU_INFO"][(cn, srn, sn)]["SECTOR_NO"] = "&".join(sector_list)
                    btsinfo["RXU_INFO"][(cn, srn, sn)][
                        "PORT_ASSIGN_MODE"] = port_assign_mode + "(L)&" + port_assign_mode + "(R)"
                else:
                    btsinfo["RXU_INFO"][(cn, srn, sn)]["WORK_MODE"] = work_mode
                    btsinfo["RXU_INFO"][(cn, srn, sn)]["SECTOR_NO"] = sector_list[0]
                    btsinfo["RXU_INFO"][(cn, srn, sn)]["PORT_ASSIGN_MODE"] = port_assign_mode

            # 对2T或者4R，修改端口发射模式
            if "TxRxMode" in btsinfo["RXU_INFO"][(cn, srn, sn)]:
                send_mode, recv_mode = btsinfo["RXU_INFO"][(cn, srn, sn)]["TxRxMode"]
                btsinfo["RXU_INFO"][(cn, srn, sn)]["PORT_ASSIGN_MODE"] += (send_mode + recv_mode)

        return btsinfo["RXU_INFO"]

    # 得到TMA、RET配置信息，并输出到Excel表中
    @API_RECORD
    def get_TMA_Info(self, site_name, ne_tree, ret_excel_row_list, tma_excel_row_list):
        for ret_obj in ne_tree["RET"]:
            row = ExcelRow()
            row["SITENAME"] = site_name
            row["NENAME"] = ne_tree["NE"][0].NENAME
            row["DEVICENO"] = ret_obj.DEVICENO
            row["RETTYPE"] = MODEL.RET.RETTYPE.toString(ret_obj.RETTYPE)
            row["POLARTYPE"] = MODEL.RET.POLARTYPE.toString(ret_obj.POLARTYPE)
            row["SCENARIO"] = MODEL.RET.SCENARIO.toString(ret_obj.SCENARIO)
            row["SUBUNITNUM"] = ret_obj.SUBUNITNUM
            row["DEVICENAME"] = ret_obj.DEVICENAME
            row["VENDORCODE"] = ret_obj.VENDORCODE
            row["SERIALNO"] = ret_obj.SERIALNO
            row["CTRLCN"] = ret_obj.CTRLCN
            row["CTRLSRN"] = ret_obj.CTRLSRN
            row["CTRLSN"] = ret_obj.CTRLSN
            row["TILT"], row["AER"] = \
            self.get_para_list_from_moc(ne_tree["RETSUBUNIT"], ["TILT", "AER"], WHERE(DEVICENO=ret_obj.DEVICENO))[0]
            ret_excel_row_list.append(row)
        for tma_obj in ne_tree["TMA"]:
            row = ExcelRow()
            row["SITENAME"] = site_name
            row["NENAME"] = ne_tree["NE"][0].NENAME
            row["DEVICENO"] = tma_obj.DEVICENO
            row["SUBUNITNUM"] = tma_obj.SUBUNITNUM
            if hasattr(MODEL.TMA, "TMATYPE"):  # R13
                row["TMATYPE"] = MODEL.TMA.TMATYPE.toString(tma_obj.TMATYPE)
            else:
                row["TMATYPE"] = "NORMAL_TMA"
            row["DEVICENAME"] = tma_obj.DEVICENAME
            row["CTRLCN"] = tma_obj.CTRLCN
            row["CTRLSRN"] = tma_obj.CTRLSRN
            row["CTRLSN"] = tma_obj.CTRLSN
            row["VENDORCODE"] = tma_obj.VENDORCODE
            row["SERIALNO"] = tma_obj.SERIALNO
            row["ATTEN"] = self.get_para_list_from_moc(ne_tree["RXBRANCH"], ["ATTEN"],
                                          WHERE(CN=tma_obj.CTRLCN, SRN=tma_obj.CTRLSRN, SN=tma_obj.CTRLSN, RXNO=0))[0]
            PWRSWITCH, THRESHOLDTYPE, row["UOTHD"], row["UCTHD"], row["OOTHD"], row["OCTHD"] = \
                self.get_para_list_from_moc(ne_tree["ANTENNAPORT"],
                               ["PWRSWITCH", "THRESHOLDTYPE", "UOTHD", "UCTHD", "OOTHD", "OCTHD"],
                               WHERE(CN=tma_obj.CTRLCN, SRN=tma_obj.CTRLSRN, SN=tma_obj.CTRLSN))[0]
            row["PWRSWITCH"] = MODEL.ANTENNAPORT.PWRSWITCH.toString(PWRSWITCH)
            row["THRESHOLDTYPE"] = MODEL.ANTENNAPORT.THRESHOLDTYPE.toString(THRESHOLDTYPE)
            tma_excel_row_list.append(row)
        pass

    ###########################################################################
    # Inner function
    @API_RECORD
    def inner_delete_unnecessary_data_during_convert(self, ne_tree):
        # 删除不需要的对象。对于共主控需要的对象，CME会自动按照版本模型重新创建
        no_need_moc_list = ["APPLICATION", "SFP", "CPRIPORT", "FLTCORRENABLECFG", "TBDSPINFO", "TBLANGNO"]
        for moc in no_need_moc_list:
            if hasattr(ne_tree, moc):
                del ne_tree[moc]

        # 把非主控单板槽位号的E1T1全部删除
        if hasattr(ne_tree, "E1T1"):
            mpt_slot = ne_tree.MPT[0].SN
            ne_tree.E1T1 = self.get_moc_list_by_del(ne_tree.E1T1, WHERE(lambda obj: obj.SN != mpt_slot))

        # 删除未被使用的ALMPORT、RETPORT，方便多制式合并。对于缺少的，平台会自动进行补充
        if "ALMPORT" in ne_tree:ne_tree.ALMPORT = self.get_moc_list_by_del(ne_tree.ALMPORT, WHERE(SW=0))
        if "RETPORT" in ne_tree:ne_tree.RETPORT = self.get_moc_list_by_del(ne_tree.RETPORT, WHERE(PWRSWITCH=MODEL.RETPORT.PWRSWITCH.OFF))

        # 删除没有数据的moc
        for moc in ne_tree.IncludedMoc:
            if hasattr(ne_tree, moc) and len(getattr(ne_tree, moc)) == 0:
                del ne_tree[moc]
        pass

    @API_RECORD
    def inner_delete_RXU(self,ne_tree, cn, srn, sn):
        pass

    #############################

    @API_RECORD
    def inner_get_id_list(self,ne_tree, ne_tree2, moc, id_para):
        list1 = self.get_para_list_from_moc(ne_tree[moc], id_para) if moc in ne_tree else []
        list2 = self.get_para_list_from_moc(ne_tree2[moc], id_para) if moc in ne_tree2 else []

        if type(id_para) == list and len(id_para) > 1:  # 当传入的是多个参数，把结果转换为tuple，方便下面set操作
            list1 = [tuple(s) for s in list1]
            list2 = [tuple(s) for s in list2]
        all_id_list = set(list1).union(set(list2))
        same_id_list = set(list1).intersection(set(list2))
        return all_id_list, same_id_list

    ##########################################################################
    # GSM共主控改造的辅助函数
    @API_RECORD
    def inner_GO_To_COMPT_create_GLOCELL(self, egbts_tree, btsinfo, cell_template=None):
        egbts_tree["GLOCELL"] = []
        for (cellid, cell_info) in btsinfo["CELL_INFO"].items():
            obj = MODEL.GLOCELL(GLOCELLID=int(cell_info["GLOCELLID"]))
            egbts_tree["GLOCELL"].append(obj)

        # 为GLOCELL应用默认的本地小区模板
        if cell_template == None:
            cell_template = "GBTS_Cell"
        glocell_template = self.get_data_from_template(cell_template, "GLOCELL", with_child=True)[0]
        egbts_tree["GLOCELL"] = self.save_data_with_template(egbts_tree["GLOCELL"], glocell_template)
        pass

    @API_RECORD
    def create_GTRXGROUP(self,btsinfo):
        GTRXGROUP_obj_list = []
        GTRXGROUPSECTOREQM_obj_list = []

        for (cellid, cellinfo) in btsinfo["CELL_INFO"].items():
            glocellid = int(cellinfo["GLOCELLID"])
            for trxgroupid in cellinfo["GTRXGROUPID_LIST"]:
                trxgroupid = int(trxgroupid)
                obj = MODEL.GTRXGROUP(GTRXGROUPID=trxgroupid, GLOCELLID=glocellid)
                GTRXGROUP_obj_list.append(obj)
                obj = MODEL.GTRXGROUPSECTOREQM(GTRXGROUPID=trxgroupid, SECTOREQMID=trxgroupid)
                GTRXGROUPSECTOREQM_obj_list.append(obj)

        return GTRXGROUP_obj_list, GTRXGROUPSECTOREQM_obj_list

    @API_RECORD
    def inner_GO_To_COMPT_create_CABINET(self, egbts_tree, btsinfo):
        egbts_tree["CABINET"] = []
        egbts_tree["SUBRACK"] = []
        for mml in btsinfo["MML_MAP"]["ADD BTSCABINET"]:
            c, paras = self.split_mml(mml)
            if paras["TYPE"] in ["APM30", "TMC", "BBC", "APM100", "APM200", "PS4890", "OMB", "BTS3900", "BTS3900L",
                                 "BTS3900AL",
                                 "VIRTUAL", "TP48600A", "BTS3012_SRAN", "BTS3012AE_SRAN", "BTS3012II_SRAN"]:
                pass
            elif paras["TYPE"] == "RFC-6":
                paras["TYPE"] = "RFC"
            else:
                paras["TYPE"] = "VIRTUAL"

            obj = MODEL.CABINET(CN=int(paras["CN"]), TYPE=paras["TYPE"], DESC=paras["CABINETDESC"])
            egbts_tree["CABINET"].append(obj)

            if (paras["CN"] == "0" and paras["ISMAINCABINET"] == "DEFAULTRULE") or paras[
                "ISMAINCABINET"] == "YES":  # 增加BBU的subrack
                obj = MODEL.SUBRACK(CN=int(paras["CN"]), SRN=0,
                                    TYPE=MODEL.SUBRACK.TYPE.fromString(paras["BBUSUBRACKTYPE"]))
                egbts_tree["SUBRACK"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_BRD(self, egbts_tree, btsinfo):
        egbts_tree["BRI"] = []
        egbts_tree["UEIU"] = []
        egbts_tree["PSU"] = []
        if "ADD BTSBRD" not in btsinfo["MML_MAP"]: return

        for mml in btsinfo["MML_MAP"]["ADD BTSBRD"]:
            c, paras = self.split_mml(mml)
            if paras["BT"] == "UBRI":
                obj = MODEL.BRI(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]),
                                TYPE=MODEL.BRI.TYPE.UBRI)
                egbts_tree["BRI"].append(obj)
            elif paras["BT"] == "UEIU":
                obj = MODEL.UEIU(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]))
                egbts_tree["UEIU"].append(obj)
            elif paras["BT"] == "PSU":
                obj = MODEL.PSU(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]))
                egbts_tree["PSU"].append(obj)
                pass
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_EMU(self, egbts_tree, btsinfo):
        egbts_tree["EMU"] = []
        if "SET BTSDEMUBP" not in btsinfo["MML_MAP"]: return

        c, paras2 = self.split_mml(btsinfo["MML_MAP"]["SET BTSEXD"][0])
        for mml in btsinfo["MML_MAP"]["SET BTSDEMUBP"]:
            c, paras = self.split_mml(mml)
            saaf = paras["SAAF"][:paras["SAAF"].find("&RES3")]  # 共主控不支持RES3, RES4
            obj = MODEL.EMU(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]),
                            MCN=int(paras["MCN"]), MSRN=int(paras["MSRN"]), MPN=int(paras["MPN"]),
                            ADDR=int(paras["ADDR"]),
                            TLTHD=paras2["TLTHD"], TUTHD=paras2["TUTHD"], HLTHD=paras2["HLTHD"], HUTHD=paras2["HUTHD"],
                            SAAF=saaf, SBAF=paras["SBAF"])
            egbts_tree["EMU"].append(obj)

            obj = MODEL.SUBRACK(CN=int(paras["CN"]), SRN=int(paras["SRN"]), TYPE=MODEL.SUBRACK.TYPE.EMU)
            egbts_tree["SUBRACK"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_CCU(self, egbts_tree, btsinfo):
        egbts_tree["CCU"] = []
        if "SET BTSCCUBP" not in btsinfo["MML_MAP"]: return

        for mml in btsinfo["MML_MAP"]["SET BTSCCUBP"]:
            c, paras = self.split_mml(mml)
            obj = MODEL.CCU(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]),
                            MCN=int(paras["MCN"]), MSRN=int(paras["MSRN"]), MPN=int(paras["MPN"]),
                            DCF=paras["DCF"], CCN=paras["CCN"], CS=paras["CS"], SBAF=paras["SBAF"])
            egbts_tree["CCU"].append(obj)

            obj = MODEL.SUBRACK(CN=int(paras["CN"]), SRN=int(paras["SRN"]), TYPE=MODEL.SUBRACK.TYPE.CCU)
            egbts_tree["SUBRACK"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_TCU(self, egbts_tree, btsinfo):
        egbts_tree["TCU"] = []
        egbts_tree["HTCDPA"] = []
        if "SET BTSDHEUBP" not in btsinfo["MML_MAP"]: return

        for mml in btsinfo["MML_MAP"]["SET BTSDHEUBP"]:
            c, paras = self.split_mml(mml)
            obj = MODEL.TCU(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]),
                            MCN=int(paras["MCN"]), MSRN=int(paras["MSRN"]), MPN=int(paras["MPN"]),
                            ADDR=int(paras["ADDR"]),
                            TLTHD=paras.get("TLTHD", None),
                            TUTHD=paras.get("TUTHD", None),
                            SBAF=paras.get("SBAF", None),
                            TCMODE=paras.get("TCMODE", None))
            egbts_tree["TCU"].append(obj)

            obj = MODEL.HTCDPA(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]),
                               LTCP=paras.get("LTCP", None),
                               HTCP=paras.get("HTCP", None),
                               TLT=paras.get("TLT", None),
                               DBD=paras.get("DBD", None),
                               NTDI=paras.get("NTDI", None),
                               NTDO=paras.get("NTDO", None),
                               HTDO=paras.get("HTDO", None))
            egbts_tree["HTCDPA"].append(obj)

            obj = MODEL.SUBRACK(CN=int(paras["CN"]), SRN=int(paras["SRN"]), TYPE=MODEL.SUBRACK.TYPE.TCU)
            egbts_tree["SUBRACK"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_FMU(self, egbts_tree, btsinfo):
        egbts_tree["FMU"] = []
        if "SET BTSFMUABP" not in btsinfo["MML_MAP"]: return

        for mml in btsinfo["MML_MAP"]["SET BTSFMUABP"]:
            c, paras = self.split_mml(mml)
            sbaf_map = dict([p.split("-") for p in paras["SBAF"].split("&")])
            sbaf = "SS_DISABLE-%s&WS_DISABLE-%s" % (sbaf_map["SS_DISABLE"], sbaf_map["WS_DISABLE"])  # 共主控，只支持这两个参数
            stc = "ENABLE" if paras["STC"] == "ENABLED" else "DISABLE"
            obj = MODEL.FMU(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]),
                            MCN=int(paras["MCN"]), MSRN=int(paras["MSRN"]), MPN=int(paras["MPN"]),
                            ADDR=int(paras["ADDR"]),
                            SBAF=sbaf, STC=stc, TCMODE=paras["TCMODE"])
            egbts_tree["FMU"].append(obj)

            obj = MODEL.SUBRACK(CN=int(paras["CN"]), SRN=int(paras["SRN"]), TYPE=MODEL.SUBRACK.TYPE.FMU)
            egbts_tree["SUBRACK"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_PMU(self, egbts_tree, btsinfo):
        egbts_tree["PMU"] = []
        if "SET BTSAPMUBP" not in btsinfo["MML_MAP"]: return

        for mml in btsinfo["MML_MAP"]["SET BTSAPMUBP"]:
            c, paras = self.split_mml(mml)
            if "SAAF" in paras:
                paras["SAAF"] = paras["SAAF"].replace("AT2_DISABLE-1&", "")
                paras["SAAF"] = paras["SAAF"].replace("AT2_DISABLE-0&", "")
            obj = MODEL.PMU(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]),
                            MCN=int(paras["MCN"]), MSRN=int(paras["MSRN"]), MPN=int(paras["MPN"]),
                            ADDR=int(paras["ADDR"]),
                            PTYPE=paras.get("PTYPE", "APM30"),
                            ACVLTHD=paras.get("ACVLTHD", 180),
                            ACVUTHD=paras.get("ACVUTHD", 280),
                            DCVLTHD=paras.get("DCVLTHD", 450),
                            DCVUTHD=paras.get("DCVUTHD", 580),
                            LSDF=paras.get("LSDF", "DISABLE"),
                            LSDV=paras.get("LSDV", 0),
                            ATLTHD=int(paras.get("TEMPALARMTHRESHOLDL", 0)) / 10,
                            ATUTHD=int(paras.get("TEMPALARMTHRESHOLDH", 500)) / 10,
                            AHLTHD=int(paras.get("HUMALAMRTHRESHOLDL", 100)) / 10,
                            AHUTHD=int(paras.get("HUMALAMRTHRESHOLDH", 800)) / 10,
                            SAAF=paras.get("SAAF", 0),
                            SBAF=paras.get("SBAF", 0))
            egbts_tree["PMU"].append(obj)

            obj = MODEL.SUBRACK(CN=int(paras["CN"]), SRN=int(paras["SRN"]), TYPE=MODEL.SUBRACK.TYPE.PMU)
            egbts_tree["SUBRACK"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_BATTERY(self, egbts_tree, btsinfo):
        egbts_tree["BATTERY"] = []
        egbts_tree["BATCTPA"] = []
        if "SET BTSAPMUBP" not in btsinfo["MML_MAP"]: return

        for mml in btsinfo["MML_MAP"]["SET BTSAPMUBP"]:
            c, paras = self.split_mml(mml)
            if paras["CFGFLAG"] == "NO": continue  # no more config
            if paras["BE"] == "NO": continue  # no battery
            if paras["BTYPE"] == "NO_BAT": continue  # no battery

            if paras["BTYPE"] == "LI_BAT":  # LI_BAT
                install_type = "INNER"  # Inner
                battery_type = "LI_BAT"  # LI_BAT
            else:
                install_type = "OUTER"  # Outer
                battery_type = "VRLA_BAT"  # VRLA_BAT

            obj = MODEL.BATTERY(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]),
                                INSTALLTYPE=install_type, BTYPE=battery_type,
                                BCD=paras.get("BCD", None),
                                BCV=paras.get("BCV", None),
                                BC1=paras.get("BC", None),
                                BCLC=paras.get("BCLC", None),
                                FCV=paras.get("FCV", None),
                                HTSDF=paras.get("HTSDF", None),
                                SDT=paras.get("SDT", None),
                                LVSDF=paras.get("LVSDF", None),
                                SDV=paras.get("SDV", None),
                                TCC=paras.get("TCC", None),
                                TLTHD=paras.get("TLTHD", None),
                                TUTHD=paras.get("TUTHD", None),
                                BN=paras.get("BN", None))
            egbts_tree["BATTERY"].append(obj)
            obj = MODEL.BATCTPA(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]),
                                DSCHGT0=paras.get("DSCHGT0", None),
                                DSCHGT1=paras.get("DSCHGT1", None),
                                DSCHGT2=paras.get("DSCHGT2", None),
                                DSCHGT3=paras.get("DSCHGT3", None),
                                DSCHGT4=paras.get("DSCHGT4", None),
                                DSCHGT5=paras.get("DSCHGT5", None),
                                DSCHGT6=paras.get("DSCHGT6", None),
                                DSCHGT7=paras.get("DSCHGT7", None),
                                DSCHGT8=paras.get("DSCHGT8", None),
                                DSCHGT9=paras.get("DSCHGT9", None),
                                EFF=paras.get("EFF", None),
                                ENDV=paras.get("ENDV", None),
                                BATNUM=paras.get("BATNUM", None),
                                DSTML=paras.get("DSTML", None),
                                SDSTML=paras.get("SDSTML", None),
                                SDSEV=paras.get("SDSEV", None),
                                ATMODE=paras.get("ATMODE", None),
                                TDSTM=paras.get("TDSTM", None),
                                DDSTM=paras.get("DDSTM", None))
            egbts_tree["BATCTPA"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_TMA(self, egbts_tree, btsinfo):
        egbts_tree["TMA"] = []
        egbts_tree["TMASUBUNIT"] = []
        egbts_tree["TMADEVICEDATA"] = []
        if "ADD BTSTMA" not in btsinfo["MML_MAP"]: return

        for mml in btsinfo["MML_MAP"]["ADD BTSTMA"]:
            c, paras = self.split_mml(mml)
            obj = MODEL.TMA(DEVICENO=int(paras["DEVICENO"]),
                            DEVICENAME=paras.get("DEVICENAME", '""')[1:-1],
                            CTRLCN=paras.get("CTRLPORTCN", None),
                            CTRLSRN=paras.get("CTRLPORTSRN", None),
                            CTRLSN=paras.get("CTRLPORTSN", None),
                            VENDORCODE=paras.get("VENDORCODE", '""')[1:-1],
                            SERIALNO=paras.get("SERIALNO", '""')[1:-1],
                            SUBUNITNUM=paras.get("SUBUNITNUM", None))
            egbts_tree["TMA"].append(obj)

        for mml in btsinfo["MML_MAP"]["MOD BTSTMASUBUNIT"]:
            c, paras = self.split_mml(mml)
            if paras["GAIN"] == "0":
                paras["GAIN"] = "255"
            obj = MODEL.TMASUBUNIT(DEVICENO=int(paras["DEVICENO"]),
                                   SUBUNITNO=int(paras["SUBUNITNO"]),
                                   CONNPN=paras.get("CONNPN", None),
                                   CONNCN=paras.get("CONNCN", None),
                                   CONNSN=paras.get("CONNSN", None),
                                   CONNSRN=paras.get("CONNSRN", None),
                                   GAIN=paras.get("GAIN", None),
                                   MODE=paras.get("MODE", None))
            egbts_tree["TMASUBUNIT"].append(obj)

        for mml in btsinfo["MML_MAP"]["MOD BTSTMADEVICEDATA"]:
            c, paras = self.split_mml(mml)
            obj = MODEL.TMADEVICEDATA(DEVICENO=int(paras["DEVICENO"]),
                                      SUBUNITNO=int(paras["SUBUNITNO"]),
                                      BEARING=paras.get("BEARING", None),
                                      BSID=paras.get("BSID", '""')[1:-1],
                                      BEAMWIDTH1=paras.get("BEAMWIDTH1", None),
                                      BEAMWIDTH2=paras.get("BEAMWIDTH2", None),
                                      BEAMWIDTH3=paras.get("BEAMWIDTH3", None),
                                      BEAMWIDTH4=paras.get("BEAMWIDTH4", None),
                                      GAIN1=paras.get("GAIN1", None),
                                      GAIN2=paras.get("GAIN2", None),
                                      GAIN3=paras.get("GAIN3", None),
                                      GAIN4=paras.get("GAIN4", None),
                                      DATE=paras.get("DATE", '""')[1:-1],
                                      TILT=paras.get("TILT", None),
                                      INSTALLERID=paras.get("INSTALLERID", '""')[1:-1],
                                      BAND1=paras.get("BAND1", None),
                                      BAND2=paras.get("BAND2", None),
                                      BAND3=paras.get("BAND3", None),
                                      BAND4=paras.get("BAND4", None),
                                      SECTORID=paras.get("SECTORID", None),
                                      SERIALNO=paras.get("SERIALNO", None),
                                      MODELNO=paras.get("MODELNO", '""')[1:-1])
            egbts_tree["TMADEVICEDATA"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_RET(self, egbts_tree, btsinfo):
        egbts_tree["RET"] = []
        egbts_tree["RETSUBUNIT"] = []
        egbts_tree["RETDEVICEDATA"] = []
        if "ADD BTSRET" not in btsinfo["MML_MAP"]: return

        for mml in btsinfo["MML_MAP"]["ADD BTSRET"]:
            c, paras = self.split_mml(mml)
            obj = MODEL.RET(DEVICENO=int(paras["DEVICENO"]),
                            DEVICENAME=paras.get("DEVICENAME", '""')[1:-1],
                            RETTYPE=paras.get("RETTYPE", None),
                            CTRLCN=paras.get("CTRLPORTCN", None),
                            CTRLSRN=paras.get("CTRLPORTSRN", None),
                            CTRLSN=paras.get("CTRLPORTSN", None),
                            POLARTYPE=paras.get("POLARTYPE", None),
                            SCENARIO=paras.get("SCENARIO", None),
                            SUBUNITNUM=paras.get("SUBUNITNUM", None),
                            VENDORCODE=paras.get("VENDORCODE", '""')[1:-1],
                            SERIALNO=paras.get("SERIALNO", '""')[1:-1])
            egbts_tree["RET"].append(obj)

        for mml in btsinfo["MML_MAP"]["MOD BTSRETSUBUNIT"]:
            c, paras = self.split_mml(mml)
            obj = MODEL.RETSUBUNIT(DEVICENO=int(paras["DEVICENO"]),
                                   SUBUNITNO=int(paras["SUBUNITNO"]),
                                   CONNCN1=paras.get("CONNCN1", None),
                                   CONNSRN1=paras.get("CONNSRN1", None),
                                   CONNSN1=paras.get("CONNSN1", None),
                                   CONNPN1=paras.get("CONNPN1", None),
                                   CONNCN2=paras.get("CONNCN2", None),
                                   CONNSRN2=paras.get("CONNSRN2", None),
                                   CONNSN2=paras.get("CONNSN2", None),
                                   CONNPN2=paras.get("CONNPN2", None),
                                   TILT=paras.get("TILT", None),
                                   AER=paras.get("AER", None))
            egbts_tree["RETSUBUNIT"].append(obj)

        for mml in btsinfo["MML_MAP"]["MOD BTSRETDEVICEDATA"]:
            c, paras = self.split_mml(mml)
            obj = MODEL.RETDEVICEDATA(DEVICENO=int(paras["DEVICENO"]),
                                      SUBUNITNO=int(paras["SUBUNITNO"]),
                                      BEARING=paras.get("BEARING", None),
                                      MODELNO=paras.get("MODELNO", '""')[1:-1],
                                      BSID=paras.get("BSID", '""')[1:-1],
                                      BEAMWIDTH1=paras.get("BEAMWIDTH1", None),
                                      BEAMWIDTH2=paras.get("BEAMWIDTH2", None),
                                      BEAMWIDTH3=paras.get("BEAMWIDTH3", None),
                                      BEAMWIDTH4=paras.get("BEAMWIDTH4", None),
                                      GAIN1=paras.get("GAIN1", None),
                                      GAIN2=paras.get("GAIN2", None),
                                      GAIN3=paras.get("GAIN3", None),
                                      GAIN4=paras.get("GAIN4", None),
                                      DATE=paras.get("DATE", '""')[1:-1],
                                      TILT=paras.get("TILT", None),
                                      INSTALLERID=paras.get("INSTALLERID", '""')[1:-1],
                                      BAND1=paras.get("BAND1", None),
                                      BAND2=paras.get("BAND2", None),
                                      BAND3=paras.get("BAND3", None),
                                      BAND4=paras.get("BAND4", None),
                                      SECTORID=paras.get("SECTORID", None),
                                      SERIALNO=paras.get("SERIALNO", None))
            egbts_tree["RETDEVICEDATA"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_ALMPORT(self, egbts_tree, btsinfo):
        egbts_tree["ALMPORT"] = []
        if "SET BTSENVALMPORT" not in btsinfo["MML_MAP"]: return

        for mml in btsinfo["MML_MAP"]["SET BTSENVALMPORT"]:
            c, paras = self.split_mml(mml)
            if paras["SW"] == "CLOSE": continue
            obj = MODEL.ALMPORT(CN=int(paras["CN"]), SRN=int(paras["SRN"]), SN=int(paras["SN"]), PN=int(paras["PN"]),
                                SW="ON",
                                AID=paras.get("AID", None), PT=paras.get("PT", None), AVOL=paras.get("AVOL", None),
                                UL=paras.get("UL", None), LL=paras.get("LL", None), ST=paras.get("ST", None),
                                SMUL=paras.get("SMUL", None), SMLL=paras.get("SMLL", None),
                                SOUL=paras.get("SOUL", None), SOLL=paras.get("SOLL", None))
            egbts_tree["ALMPORT"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_ALMCURCFG(self, egbts_tree, btsinfo):
        egbts_tree["ALMCURCFG"] = []
        if "ENVALMPARA_MML" not in btsinfo: return

        for mml in btsinfo["ENVALMPARA_MML"]:
            c, paras = self.split_mml(mml)
            aid = int(paras["AID"])
            if aid > 65233 or aid < 65033: continue
            alvl = paras["ALVL"].upper()
            ass = paras["ASS"].upper()
            anm = paras["ANM"][1:-1]
            obj = MODEL.ALMCURCFG(AID=aid, ALVL=alvl, ASS=ass, ANM=anm)
            egbts_tree["ALMCURCFG"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_DEVIP_SRCIPRT(self, egbts_tree, btsinfo):
        port_no = btsinfo["ETHPORT_NO"]
        obj = MODEL.DEVIP(CN=0, SRN=0, SN=7, SBT="BASE_BOARD", PT="ETH", PN=port_no, VRFIDX=0,
                          IP=btsinfo["GSM_IP"], MASK=btsinfo["GSM_MASK"], USERLABEL="2G")
        egbts_tree["DEVIP"] = [obj]

        obj = MODEL.SRCIPRT(SRCRTIDX=0, CN=0, SRN=0, SN=7, SBT="BASE_BOARD", RTTYPE="NEXTHOP",
                            SRCIP=btsinfo["GSM_IP"], NEXTHOP=btsinfo["GSM_GATEWAY"], USERLABEL="2G")
        egbts_tree["SRCIPRT"] = [obj]

        # obj = MODEL.IPRT(RTIDX=0, CN=0, SRN=0, SN=7, SBT="BASE_BOARD", RTTYPE="NEXTHOP", VRFIDX=0,
        #                  DSTIP=btsinfo["BSC_IP"], DSTMASK="255.255.255.255", NEX)
        # egbts_tree["IPRT"] = [obj]
        # IPRT

        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_VLAN(self, egbts_tree, btsinfo):
        egbts_tree["VLANCLASS"] = []
        egbts_tree["VLANMAP"] = []
        if "GSM_VLAN" not in btsinfo: return

        vlan = int(btsinfo["GSM_VLAN"])
        if vlan <= 0 or vlan > 4094:
            self.print_msg( "Error: vlan=%d is invalid" % vlan)
            return

        added_list = []
        if "SET BTSVLAN" in btsinfo["MML_MAP"]:
            traffic_map = {"OTHERDATA": "OTHER", "RSL": "SIG", "ESL": "OM_HIGH", "OML": "OM_LOW",
                           "CSVOICE": "USERDATA", "CSDATA": "USERDATA", "PSHIGHPRI": "USERDATA", "PSLOWPRI": "USERDATA"}
            for mml in btsinfo["MML_MAP"]["SET BTSVLAN"]:
                c, paras = self.split_mml(mml)
                service_type = paras["SERVICETYPE"]
                if service_type not in traffic_map: continue
                traffic = MODEL.VLANCLASS.TRAFFIC.fromString(traffic_map[service_type])
                dscp = int(paras["DSCP"])
                if (traffic, dscp) in added_list: continue

                added_list.append((traffic, dscp))
                vlanpri = "0" if paras["VLANSWITCH"] == "NO" else paras["VLANPRI"]
                obj = MODEL.VLANCLASS(VLANGROUPNO=0, TRAFFIC=traffic, SRVPRIO=dscp, VLANID=vlan, VLANPRIO=vlanpri)
                egbts_tree["VLANCLASS"].append(obj)

        gw = btsinfo["GSM_GATEWAY"]
        mask = btsinfo["GSM_MASK"]

        if len(egbts_tree["VLANCLASS"]) > 0:
            obj = MODEL.VLANMAP(VRFIDX=0, NEXTHOPIP=gw, MASK=mask, VLANMODE="VLANGROUP", VLANID=vlan, VLANGROUPNO=0)
        else:
            obj = MODEL.VLANMAP(VRFIDX=0, NEXTHOPIP=gw, MASK=mask, VLANMODE="SINGLEVLAN", VLANID=vlan,
                                SETPRIO="DISABLE", VLANPRIO=0)
        egbts_tree["VLANMAP"].append(obj)

        if "ADD BTSVLANMAP" in btsinfo["MML_MAP"]:
            egbts_tree["VLANMAP"] = []
            for mml in btsinfo["MML_MAP"]["SET BTSVLAN"]:
                c, paras = self.split_mml(mml)
                if "MODE" not in paras:
                    continue
                elif paras["MODE"] != "VLANCLASS":
                    obj = MODEL.VLANMAP(VRFIDX=0, NEXTHOPIP=gw, MASK=mask, VLANMODE="VLANGROUP", VLANID=vlan,
                                        VLANGROUPNO=0)
                else:
                    obj = MODEL.VLANMAP(VRFIDX=0, NEXTHOPIP=gw, MASK=mask, VLANMODE="SINGLEVLAN", VLANID=vlan,
                                        SETPRIO="DISABLE", VLANPRIO=paras["VLANPRI"])
                egbts_tree["VLANMAP"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_SCTPLNK(self, egbts_tree, btsinfo):
        egbts_tree["SCTPLNK"] = []
        egbts_tree["CPBEARER"] = []
        egbts_tree["GBTSABISCP"] = []
        for (bsc_sctplnkid, bsc_sctplnk_dscp, bts_sctpno, bts_port) in btsinfo["SCTPLNK_INFO"]:
            obj = MODEL.SCTPLNK(SCTPNO=bts_sctpno, CN=0, SRN=0, SN=7, VRFIDX=0, DESCRI="Abis",
                                LOCIP=btsinfo["GSM_IP"], LOCPORT=bts_port, PEERIP=btsinfo["BSC_IP"], PEERPORT=58080)
            egbts_tree["SCTPLNK"].append(obj)

            obj = MODEL.CPBEARER(CPBEARID=bts_sctpno, LINKNO=bts_sctpno, FLAG="MASTER", BEARTYPE="SCTP",
                                 CTRLMODE="MANUAL_MODE")
            egbts_tree["CPBEARER"].append(obj)

            obj = MODEL.GBTSABISCP(ABISCPID=2, CPBEARID=bts_sctpno)
            egbts_tree["GBTSABISCP"].append(obj)
        pass

    @API_RECORD
    def inner_GO_To_COMPT_create_for_UserPlane(self, egbts_tree, btsinfo):
        PHB_2_DSCP_map = {"BE": 0, "CS1": 8, "AF11": 10, "AF12": 12, "AF13": 14, "CS2": 16,
                          "AF21": 18, "AF22": 20, "AF23": 22, "CS3": 24, "AF31": 26, "AF32": 28, "AF33": 30,
                          "CS4": 32, "AF41": 34, "AF42": 36, "AF43": 38, "CS5": 40, "EF": 46, "CS6": 48, "CS7": 56}

        egbts_tree["IPPATH"] = []
        if btsinfo["BSC_TYPE"] == "BSC6900":
            port_no = btsinfo["ETHPORT_NO"]
            if "ADD IPPATH" in btsinfo["MML_MAP"]:  # 之前有IPPATH配置
                for (idx, mml) in enumerate(btsinfo["MML_MAP"]["ADD IPPATH"]):
                    c, paras = self.split_mml(mml)
                    if paras["PATHT"] == "QoS":
                        path_type = "ANY"
                        dscp = None
                    else:
                        path_type = "FIXED"
                        dscp = PHB_2_DSCP_map[paras["PATHT"]]
                    obj = MODEL.IPPATH(PATHID=idx, VRFIDX=0, CN=0, SRN=0, SN=7, SBT="BASE_BOARD", PT="ETH", PN=port_no,
                                       PATHTYPE=path_type,
                                       DSCP=dscp, LOCALIP=btsinfo["GSM_IP"], PEERIP=btsinfo["BSC_IP"], DESCRI="TO BSC")
                    egbts_tree["IPPATH"].append(obj)
            else:  # 改造前，没有IPPATH配置. 只创建一条QoS的Path
                obj = MODEL.IPPATH(PATHID=0, VRFIDX=0, CN=0, SRN=0, SN=7, SBT="BASE_BOARD", PT="ETH", PN=port_no,
                                   PATHTYPE="ANY", LOCALIP=btsinfo["GSM_IP"], PEERIP=btsinfo["BSC_IP"], DESCRI="TO BSC")
                egbts_tree["IPPATH"].append(obj)
        else:  # BSC6910，用户面资源池
            obj = MODEL.USERPLANEHOST(UPHOSTID=2, VRFIDX=0, IPVERSION="IPv4", LOCIPV4=btsinfo["GSM_IP"],
                                      USERLABEL="Abis")
            egbts_tree["USERPLANEHOST"].append(obj)

            sub_obj = MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=2)
            obj = MODEL.EPGROUP(EPGROUPID=2, VRFIDX=0, USERPLANEHOSTREFS=[sub_obj], USERLABEL="Abis")
            egbts_tree["EPGROUP"].append(obj)

            obj = MODEL.ABIS(ABISID=2, UPEPGRPID=2, USERLABEL="Abis UP")
            egbts_tree["ABIS"].append(obj)
        pass

    # Analyze Current config, Get mapping relation between Freq_Band and IDs(SECTORID, SECTOREQMID, RRU Subrack, RCN, etc)
    @API_RECORD
    def analyze_Data(self, ne_tree=None, bts_info=None,band_gtrxgroupid_map=None, lte_sectorid_fun=None, tdd_sectorid_fun=None, nb_sectorid_fun=None, start_sector_id=0):
        if tdd_sectorid_fun is None:
            tdd_sectorid_fun = lte_sectorid_fun
        if nb_sectorid_fun is None:
            nb_sectorid_fun = lte_sectorid_fun

        sectorid_sector_map = {}  # Record the relation between SECTORID and physical sector
        self.Analyze_Cache["RXU_To_Rat"] = {}
        # Analyze UMTS
        band_locellid_map = {}
        umtsfreq_band = []
        for cell_obj in self.inner_Get_Data(ne_tree, "ULOCELL"):
            band_str = self.get_UMTS_Common_Str_From_Dlfreq(cell_obj.DLFREQ)
            umtsfreq_band.append(band_str)
            if band_str not in band_locellid_map:
                band_locellid_map[band_str] = []
            band_locellid_map[band_str].append(cell_obj.ULOCELLID)
        for (band_str, locellid_list) in band_locellid_map.items():
            rat_band_str = "UO" + band_str
            if band_str not in self.Analyze_Cache["Band_Sector_To_ULOCELLID"]:
                self.Analyze_Cache["Band_Sector_To_ULOCELLID"][rat_band_str] = {}
            if rat_band_str not in self.Analyze_Cache["Band_Sector_To_SectorEqmId"]:
                self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str] = {}
            if band_str not in self.Analyze_Cache["Band_Sector_To_SectorId"]:
                self.Analyze_Cache["Band_Sector_To_SectorId"][band_str] = {}
            if band_str not in self.Analyze_Cache["Band_Sector_To_RXU"]:
                self.Analyze_Cache["Band_Sector_To_RXU"][band_str] = {}
            if band_str not in self.Analyze_Cache["Band_Sector_To_RruChain"]:
                self.Analyze_Cache["Band_Sector_To_RruChain"][band_str] = {}
            if band_str not in self.Analyze_Cache["Band_Sector_To_Bbp_Port"]:
                self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str] = {}

            locellid_list.sort()
            sector_idx = 0
            for locellid in locellid_list:
                sectoreqmid_list = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "ULOCELLSECTOREQM"), "SECTOREQMID",
                                                  WHERE(ULOCELLID=locellid))
                if len(sectoreqmid_list) == 0:
                    self.print_msg("Band=%s, ULOCELLID=%d has no ULOCELLSECTOREQM config. skip" % (band_str, locellid))
                    continue
                sectorid = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "SECTOREQM"), "SECTORID",
                                          WHERE(SECTOREQMID=sectoreqmid_list[0]))[0]

                if sectorid in sectorid_sector_map:
                    sector_str = sectorid_sector_map[sectorid]
                else:
                    sector_str = chr(ord('A') + sector_idx)
                    sectorid_sector_map[sectorid] = sector_str
                    sector_idx += 1

                if sector_str not in self.Analyze_Cache["Band_Sector_To_ULOCELLID"][rat_band_str]:
                    self.Analyze_Cache["Band_Sector_To_ULOCELLID"][rat_band_str][sector_str] = []
                if sector_str not in self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str]:
                    self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str][sector_str] = []
                if sector_str not in self.Analyze_Cache["Band_Sector_To_SectorId"][band_str]:
                    self.Analyze_Cache["Band_Sector_To_SectorId"][band_str][sector_str] = []
                if sector_str not in self.Analyze_Cache["Band_Sector_To_RXU"][band_str]:
                    self.Analyze_Cache["Band_Sector_To_RXU"][band_str][sector_str] = []
                if sector_str not in self.Analyze_Cache["Band_Sector_To_RruChain"][band_str]:
                    self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str] = []
                if sector_str not in self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str]:
                    self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str][sector_str] = []

                self.Analyze_Cache["Band_Sector_To_ULOCELLID"][rat_band_str][sector_str].append(locellid)
                self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str][sector_str].extend(sectoreqmid_list)
                self.Analyze_Cache["Band_Sector_To_SectorId"][band_str][sector_str].append(sectorid)

                for sectoreqm_obj in self.inner_Get_Data(ne_tree, "SECTOREQM"):
                    if sectoreqm_obj.SECTOREQMID not in sectoreqmid_list: continue
                    rxu_pos_list = self.get_para_list_from_moc(sectoreqm_obj.SECTOREQMANTENNA, ["CN", "SRN", "SN"])
                    rxu_pos_list = [tuple(s) for s in rxu_pos_list]
                    for rxu_pos in rxu_pos_list:
                        if rxu_pos not in self.Analyze_Cache["RXU_To_Rat"]:
                            self.Analyze_Cache["RXU_To_Rat"][rxu_pos] = []
                        self.Analyze_Cache["RXU_To_Rat"][rxu_pos].append("U")
                        if rxu_pos not in self.Analyze_Cache["Band_Sector_To_RXU"][band_str][sector_str]:
                            self.Analyze_Cache["Band_Sector_To_RXU"][band_str][sector_str].append(rxu_pos)
                        rruchainid = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RRU"), "RCN",
                                                    WHERE(CN=rxu_pos[0], SRN=rxu_pos[1], SN=rxu_pos[2]))
                        if rruchainid is not None and len(rruchainid) != 0 and rruchainid[0] not in \
                                self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str]:
                            self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str].append(rruchainid[0])
                            bbp_pos_list = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RRUCHAIN"),
                                                          ["HCN", "HSRN", "HSN", "HPN"], WHERE(RCN=rruchainid[0]))
                            bbp_pos_list = [tuple(s) for s in bbp_pos_list]
                            self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str][sector_str].append(bbp_pos_list[0])
                        rruchainid = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RFU"), "RCN",
                                                    WHERE(CN=rxu_pos[0], SRN=rxu_pos[1], SN=rxu_pos[2]))
                        if rruchainid is not None and len(rruchainid) != 0 and rruchainid[0] not in \
                                self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str]:
                            self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str].append(rruchainid[0])
                            bbp_pos_list = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RRUCHAIN"),
                                                          ["HCN", "HSRN", "HSN", "HPN"],
                                                          WHERE(RCN=rruchainid[0]))
                            bbp_pos_list = [tuple(s) for s in bbp_pos_list]
                            self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str][sector_str].append(bbp_pos_list[0])
            pass

        # Analyze LTE
        band_locellid_map = {}
        for cell_obj in self.inner_Get_Data(ne_tree, "Cell"):
            if cell_obj.NbCellFlag == MODEL.Cell.NbCellFlag.TRUE:
                prb_obj_list = [obj for obj in self.inner_Get_Data(ne_tree,"Prb") if obj.LocalCellId == cell_obj.LocalCellId]
                cell_band = prb_obj_list[0].FreqBand
            else:
                cell_band = cell_obj.FreqBand
            band_str = self.get_LTE_Common_Str_From_Band(cell_band)
            if band_str not in band_locellid_map:
                band_locellid_map[band_str] = []
            band_locellid_map[band_str].append(cell_obj.LocalCellId)

        for (band_str, locellid_list) in band_locellid_map.items():
            locellid_list.sort()
            sector_idx = 0
            for locellid in locellid_list:
                cell_obj = [obj for obj in self.inner_Get_Data(ne_tree, "Cell") if obj.LocalCellId == locellid][0]
                if cell_obj.NbCellFlag == MODEL.Cell.NbCellFlag.TRUE:
                    cell_rat = "MO"
                elif cell_obj.FddTddInd == MODEL.Cell.FddTddInd.CELL_FDD:
                    cell_rat = "LO"
                else:
                    cell_rat = "TO"

                rat_band_str = cell_rat + band_str
                if rat_band_str not in self.Analyze_Cache["Band_Sector_To_LocalCellId"]:
                    self.Analyze_Cache["Band_Sector_To_LocalCellId"][rat_band_str] = {}
                if rat_band_str not in self.Analyze_Cache["Band_Sector_To_SectorEqmId"]:
                    self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str] = {}
                if band_str not in self.Analyze_Cache["Band_Sector_To_SectorId"]:
                    self.Analyze_Cache["Band_Sector_To_SectorId"][band_str] = {}
                if band_str not in self.Analyze_Cache["Band_Sector_To_RXU"]:
                    self.Analyze_Cache["Band_Sector_To_RXU"][band_str] = {}
                if band_str not in self.Analyze_Cache["Band_Sector_To_RruChain"]:
                    self.Analyze_Cache["Band_Sector_To_RruChain"][band_str] = {}
                if band_str not in self.Analyze_Cache["Band_Sector_To_Bbp_Port"]:
                    self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str] = {}

                if cell_rat == "MO":
                    sectoreqmid_list = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "EuPrbSectorEqm"), "SectorEqmId", WHERE(LocalCellId=locellid))
                else:
                    sectoreqmid_list = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "eUCellSectorEqm"), "SectorEqmId", WHERE(LocalCellId=locellid))
                if len(sectoreqmid_list) == 0:
                    self.print_msg("Band=%s, LTE Cell=%d %s has no eUCellSectorEqm config. skip" % (band_str, locellid, cell_obj.CellName))
                    continue

                sector_str = None
                if cell_rat == "MO":
                    if nb_sectorid_fun is not None:
                        sector_str = chr(ord('A') + nb_sectorid_fun(cell_obj) + start_sector_id)
                elif cell_rat == "LO":
                    if lte_sectorid_fun is not None:
                        sector_str = chr(ord('A') + lte_sectorid_fun(cell_obj) + start_sector_id)
                else:
                    if tdd_sectorid_fun is not None:
                        sector_str = chr(ord('A') + tdd_sectorid_fun(cell_obj) + start_sector_id)

                sectorid = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "SECTOREQM"), "SECTORID",
                                                       WHERE(SECTOREQMID=sectoreqmid_list[0]))[0]
                if sector_str is None:
                    if sectorid not in sectorid_sector_map:
                        sector_str = chr(ord('A') + sector_idx + start_sector_id)
                        sectorid_sector_map[sectorid] = sector_str
                        sector_idx += 1
                    else:
                        sector_str = sectorid_sector_map[sectorid]

                if sector_str not in self.Analyze_Cache["Band_Sector_To_LocalCellId"][rat_band_str]:
                    self.Analyze_Cache["Band_Sector_To_LocalCellId"][rat_band_str][sector_str] = []
                if sector_str not in self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str]:
                    self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str][sector_str] = []
                if sector_str not in self.Analyze_Cache["Band_Sector_To_SectorId"][band_str]:
                    self.Analyze_Cache["Band_Sector_To_SectorId"][band_str][sector_str] = []
                if sector_str not in self.Analyze_Cache["Band_Sector_To_RXU"][band_str]:
                    self.Analyze_Cache["Band_Sector_To_RXU"][band_str][sector_str] = []
                if sector_str not in self.Analyze_Cache["Band_Sector_To_RruChain"][band_str]:
                    self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str] = []
                if sector_str not in self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str]:
                    self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str][sector_str] = []

                self.Analyze_Cache["Band_Sector_To_LocalCellId"][rat_band_str][sector_str].append(locellid)
                self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str][sector_str].extend(sectoreqmid_list)
                self.Analyze_Cache["Band_Sector_To_SectorId"][band_str][sector_str].append(sectorid)

                for sectoreqm_obj in self.inner_Get_Data(ne_tree, "SECTOREQM"):
                    if sectoreqm_obj.SECTOREQMID not in sectoreqmid_list: continue
                    rxu_pos_list = self.get_para_list_from_moc(sectoreqm_obj.SECTOREQMANTENNA, ["CN", "SRN", "SN"])
                    rxu_pos_list = [tuple(s) for s in rxu_pos_list]
                    for rxu_pos in rxu_pos_list:
                        if rxu_pos not in self.Analyze_Cache["RXU_To_Rat"]:
                            self.Analyze_Cache["RXU_To_Rat"][rxu_pos] = []
                        self.Analyze_Cache["RXU_To_Rat"][rxu_pos].append("L")
                        if rxu_pos not in self.Analyze_Cache["Band_Sector_To_RXU"][band_str][sector_str]:
                            self.Analyze_Cache["Band_Sector_To_RXU"][band_str][sector_str].append(rxu_pos)
                        rruchainid = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RRU"), "RCN",
                                                    WHERE(CN=rxu_pos[0], SRN=rxu_pos[1], SN=rxu_pos[2]))
                        if rruchainid is not None and len(rruchainid) != 0 and rruchainid[0] not in \
                                self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str]:
                            self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str].append(rruchainid[0])
                            bbp_pos_list = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RRUCHAIN"),
                                                          ["HCN", "HSRN", "HSN", "HPN"],
                                                          WHERE(RCN=rruchainid[0]))
                            bbp_pos_list = [tuple(s) for s in bbp_pos_list]
                            self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str][sector_str].append(bbp_pos_list[0])
                        rruchainid = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RFU"), "RCN",
                                                    WHERE(CN=rxu_pos[0], SRN=rxu_pos[1], SN=rxu_pos[2]))
                        if rruchainid is not None and len(rruchainid) != 0 and rruchainid[0] not in \
                                self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str]:
                            self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str].append(rruchainid[0])
                            bbp_pos_list = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RRUCHAIN"),
                                                          ["HCN", "HSRN", "HSN", "HPN"],
                                                          WHERE(RCN=rruchainid[0]))
                            bbp_pos_list = [tuple(s) for s in bbp_pos_list]
                            self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str][sector_str].append(bbp_pos_list[0])
                pass

        if bts_info is not None or band_gtrxgroupid_map is not None and len(self.inner_Get_Data(ne_tree, "GTRXGROUP")) > 0:
            # Analyze GSM
            for cellinfo in bts_info['CELL_INFO'].values():
                rat_band_str = cellinfo['TYPE']
                sector_str = cellinfo['CELLNAME']
                locellid = cellinfo['GLOCELLID']
                if rat_band_str not in self.Analyze_Cache["Band_Sector_To_GLOCELLID"]:
                    self.Analyze_Cache["Band_Sector_To_GLOCELLID"][rat_band_str] = {}
                if sector_str not in self.Analyze_Cache["Band_Sector_To_GLOCELLID"][rat_band_str]:
                    self.Analyze_Cache["Band_Sector_To_GLOCELLID"][rat_band_str][sector_str] = []
                self.Analyze_Cache["Band_Sector_To_GLOCELLID"][rat_band_str][sector_str].append(locellid)
            if band_gtrxgroupid_map is None:
                band_gtrxgroupid_map = self.get_Band_GtrxGroupID_Map(bts_info)
            for (band_str, gtrxgroupid_list) in band_gtrxgroupid_map.items():
                rat_band_str = "GO" + band_str
                if rat_band_str not in self.Analyze_Cache["Band_Sector_To_SectorEqmId"]:
                    self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str] = {}
                if rat_band_str not in self.Analyze_Cache["Band_Sector_To_GTRXGROUPID"]:
                    self.Analyze_Cache["Band_Sector_To_GTRXGROUPID"][rat_band_str] = {}
                if band_str not in self.Analyze_Cache["Band_Sector_To_SectorId"]:
                    self.Analyze_Cache["Band_Sector_To_SectorId"][band_str] = {}
                if band_str not in self.Analyze_Cache["Band_Sector_To_RXU"]:
                    self.Analyze_Cache["Band_Sector_To_RXU"][band_str] = {}
                if band_str not in self.Analyze_Cache["Band_Sector_To_RruChain"]:
                    self.Analyze_Cache["Band_Sector_To_RruChain"][band_str] = {}
                if band_str not in self.Analyze_Cache["Band_Sector_To_Bbp_Port"]:
                    self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str] = {}

                gtrxgroupid_list.sort()
                sector_idx = 0
                for gtrxgroupid in gtrxgroupid_list:
                    sectoreqmid_list = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "GTRXGROUPSECTOREQM"), "SECTOREQMID",
                                                      WHERE(GTRXGROUPID=int(gtrxgroupid)))
                    if len(sectoreqmid_list) == 0:
                        self.print_msg("Band=%s, GTRXGROUPID=%d has no GTRXGROUPSECTOREQM config. skip" % (band_str, gtrxgroupid))
                        continue
                    sectorid_list = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "SECTOREQM"), "SECTORID",
                                                                WHERE(SECTOREQMID=sectoreqmid_list[0]))
                    if len(sectorid_list) == 0: continue
                    sectorid = sectorid_list[0]
                    if sectorid not in sectorid_sector_map:
                        sector_str = chr(ord('A') + sector_idx)
                        sectorid_sector_map[sectorid] = sector_str
                        sector_idx += 1
                    else:
                        sector_str = sectorid_sector_map[sectorid]

                    if sector_str not in self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str]:
                        self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str][sector_str] = []
                    if sector_str not in self.Analyze_Cache["Band_Sector_To_GTRXGROUPID"][rat_band_str]:
                        self.Analyze_Cache["Band_Sector_To_GTRXGROUPID"][rat_band_str][sector_str] = []
                    if sector_str not in self.Analyze_Cache["Band_Sector_To_SectorId"][band_str]:
                        self.Analyze_Cache["Band_Sector_To_SectorId"][band_str][sector_str] = []
                    if sector_str not in self.Analyze_Cache["Band_Sector_To_RXU"][band_str]:
                        self.Analyze_Cache["Band_Sector_To_RXU"][band_str][sector_str] = []
                    if sector_str not in self.Analyze_Cache["Band_Sector_To_RruChain"][band_str]:
                        self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str] = []
                    if sector_str not in self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str]:
                        self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str][sector_str] = []

                    self.Analyze_Cache["Band_Sector_To_SectorEqmId"][rat_band_str][sector_str].extend(sectoreqmid_list)
                    self.Analyze_Cache["Band_Sector_To_GTRXGROUPID"][rat_band_str][sector_str].extend([gtrxgroupid])
                    self.Analyze_Cache["Band_Sector_To_SectorId"][band_str][sector_str].append(sectorid)

                    for sectoreqm_obj in self.inner_Get_Data(ne_tree, "SECTOREQM"):
                        if sectoreqm_obj.SECTOREQMID not in sectoreqmid_list: continue
                        rxu_pos_list = self.get_para_list_from_moc(sectoreqm_obj.SECTOREQMANTENNA, ["CN", "SRN", "SN"])
                        rxu_pos_list = list(set([tuple(s) for s in rxu_pos_list]))
                        for rxu_pos in rxu_pos_list:
                            if rxu_pos not in self.Analyze_Cache["RXU_To_Rat"]:
                                self.Analyze_Cache["RXU_To_Rat"][rxu_pos] = []
                            self.Analyze_Cache["RXU_To_Rat"][rxu_pos].append("G")
                            if rxu_pos not in self.Analyze_Cache["Band_Sector_To_RXU"][band_str][sector_str]:
                                self.Analyze_Cache["Band_Sector_To_RXU"][band_str][sector_str].append(rxu_pos)
                            rruchainid = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RRU"), "RCN",
                                                        WHERE(CN=rxu_pos[0], SRN=rxu_pos[1], SN=rxu_pos[2]))
                            if rruchainid is not None and len(rruchainid) != 0 and rruchainid[0] not in \
                                    self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str]:
                                self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str].append(rruchainid[0])
                                bbp_pos_list = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RRUCHAIN"),
                                                              ["HCN", "HSRN", "HSN", "HPN"],
                                                              WHERE(RCN=rruchainid[0]))
                                bbp_pos_list = [tuple(s) for s in bbp_pos_list]
                                self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str][sector_str].append(bbp_pos_list[0])
                            rruchainid = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RFU"), "RCN",
                                                        WHERE(CN=rxu_pos[0], SRN=rxu_pos[1], SN=rxu_pos[2]))
                            if rruchainid is not None and len(rruchainid) != 0 and rruchainid[0] not in \
                                    self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str]:
                                self.Analyze_Cache["Band_Sector_To_RruChain"][band_str][sector_str].append(rruchainid[0])
                                bbp_pos_list = self.get_para_list_from_moc(self.inner_Get_Data(ne_tree, "RRUCHAIN"),
                                                              ["HCN", "HSRN", "HSN", "HPN"],
                                                              WHERE(RCN=rruchainid[0]))
                                bbp_pos_list = [tuple(s) for s in bbp_pos_list]
                                self.Analyze_Cache["Band_Sector_To_Bbp_Port"][band_str][sector_str].append(bbp_pos_list[0])
                    pass

        return self.Analyze_Cache

    @API_RECORD
    def inner_Get_Data(self,ne_tree, moc):
        if ne_tree is None:
            return self.get_moc(moc)
        elif moc in ne_tree:
            return ne_tree[moc]
        else:
            return []

    # Modify ID
    @API_RECORD
    def modify_ID(self, ne_tree, moc_analyze_map, id_plan_map, api_modify_fun, newid_fun=int):
        id_replace_map = {}
        for band_str in moc_analyze_map:
            for (sector_str, id_list) in moc_analyze_map[band_str].items():
                id_list = list(set(id_list))
                id_list.sort()
                plan_id_list = id_plan_map[band_str]["SECTOR_%s" % sector_str]
                num = 0
                for (i, id) in enumerate(id_list):
                    if isinstance(id, tuple) and len(id) == 3 and id[1] < 60:
                        num = num + 1
                        continue
                    if len(plan_id_list) + num <= i:
                        self.exit_Info("No enough ID PLAN for Band=%s, Secotr=%s. Plan ID=%r" % (
                            band_str, sector_str, plan_id_list))
                    id_replace_map[id] = newid_fun(plan_id_list[i])

        id_replace_list = self.get_ID_Replace_List(id_replace_map)
        if id_replace_list is not None:
            for (old_id, new_id) in id_replace_list:
                if old_id == new_id: continue
                api_modify_fun(ne_tree, old_id, new_id)
        pass

    # BSC6900 CFGMML, 输入一条MML命令，返回命令名称、参数和值的map
    def split_mml(self, cmd):
        x = cmd.strip().split(":", 1)  # 只用第一个冒号，分拆为2部分
        if len(x) != 2:
            return (None, None)
        c = x[0].strip()
        plist = x[1].strip(";").split(",")
        paras = {}
        for l in plist:
            p = l.split("=")
            if len(p) == 2:
                para = p[0].strip()
                value = p[1].strip()
                paras[para] = value
        return (c, paras)

    # 对IP和Mask进行&运算，得到IP网段。要求输入和输出均为字符串
    @API_RECORD
    def get_network_by_ip(self, ip, mask):
        network = ".".join([str(int(a) & int(b)) for (a, b) in zip(ip.split("."), mask.split("."))])
        return network

    # 从小区类型和频点，推导出频段
    @API_RECORD
    def get_GSM_Band_By_Freq(self, freq, cell_type):
        if 128 <= freq <= 251:
            return "850"
        elif 512 <= freq <= 885 and cell_type in ["DCS1800", "GSM900_DCS1800", "GSM850_1800"]:
            return "1800"
        elif 512 <= freq <= 810 and cell_type in ["PCS1900", "GSM850_1900"]:
            return "1900"
        else:
            return "900"
        pass

    # 获得指定MML命令的参数值的列表
    # cell_band_list = API_Get_MML_Para_List(nodeb_info, "ADD UCELLSETUP", ["CELLID", "BANDIND"])
    @API_RECORD
    def get_MML_Para_List(self, info_map, cmd, para_list):
        if cmd in info_map:
            mml_list = info_map[cmd]
        elif cmd in info_map["MML_MAP"]:
            mml_list = info_map["MML_MAP"][cmd]
        else:
            return []

        if type(para_list) == type(u"") or type(para_list) == type(""):
            para_list = [para_list]

        all_value_list = []
        for mml in mml_list:
            value_list = []
            c, paras = self.split_mml(mml)
            for p in para_list:
                if p not in paras:
                    value_list.append(None)
                else:
                    value_list.append(paras[p])
            if len(para_list) == 1:
                value_list = value_list[0]
            all_value_list.append(value_list)
        return all_value_list

    # 输入gbts_name, 返回该BTS对应参数信息，包含所有MML
    @API_RECORD
    def get_BTS_Info(self, gbts_name, encoding="GBK"):
        gbts_info_map = load_Object("ALL_BTS_CFGMML_INFO", {})
        if len(gbts_info_map) == 0:
            gbts_info_map, _ = self.inner_Parse_CFGMML_File(encoding)
        if gbts_name not in gbts_info_map:
            self.print_msg("Error: BTS=%s is not found in all CFGMML files" % gbts_name)
            return None
        self.print_msg('Info: get BTS Information')
        btsinfo = gbts_info_map[gbts_name]
        btsid = btsinfo["BTSID"]
        cellid_list = btsinfo["CELLID_LIST"]
        btsinfo["ENVALMPARA_MML"] = []
        btsinfo["IPPOOLIP_MML"] = []

        iprt_mml_list = []
        self.print_msg("Read BSC CFGMML file" + btsinfo["CFGMML_FILE"])
        cmd_lines = load_TXT_File(btsinfo["CFGMML_FILE"], encoding)
        for line in cmd_lines:
            c, paras = self.split_mml(line)
            if c is None:
                continue
            elif c == "ADD IPRT":
                iprt_mml_list.append(line)
            elif c == "ADD GTRX" and paras["CELLID"] in cellid_list:
                btsinfo["TRXID_LIST"].append(paras["TRXID"])
            elif c == "ADD BTSCONNECT":
                if paras["BTSID"] == btsid:  # 本基站的E1
                    if "UPBTSID" in paras:
                        btsinfo["PARENT_BTSID"] = paras["UPBTSID"]
                if "UPBTSID" in paras and paras["UPBTSID"] == btsid:  # 本基站的下级基站的ID
                    btsinfo["CHILD_BTSID_LIST"].append(paras["BTSID"])
            elif c == "SET ENVALMPARA":
                btsinfo["ENVALMPARA_MML"].append(line)
            elif c == "ADD IPPOOLIP":
                btsinfo["IPPOOLIP_MML"].append(line)

            # 判断是否为本基站的命令，如是则保存
            is_bts_mml = False
            if "BTSID" in paras and paras["BTSID"] == btsid:
                is_bts_mml = True
            elif "ANI" in paras and paras["ANI"] == btsinfo["ANI"]:
                is_bts_mml = True
            elif "CELLID" in paras and paras["CELLID"] in cellid_list:
                is_bts_mml = True
            elif "TRXID" in paras and paras["TRXID"] in btsinfo["TRXID_LIST"]:
                is_bts_mml = True
            elif "SCTPLNKID" in paras and paras["SCTPLNKID"] in btsinfo["SCTPLNKID_LIST"]:
                is_bts_mml = True
            elif "SRC2GNCELLID" in paras:
                if (paras["SRC2GNCELLID"] in cellid_list) or (
                    paras["NBR2GNCELLID"] in cellid_list):  # add 2G neighbor data
                    is_bts_mml = True
            elif "SRC3GNCELLID" in paras and paras["SRC3GNCELLID"] in cellid_list:  # add 3G neighbor data
                is_bts_mml = True
            elif "ADD GLTENCELL" in paras and paras["SRCLTENCELLID"] in cellid_list:  # add LTE neighbor data
                is_bts_mml = True
            elif c == "ADD VLANID" and "GSM_IP" in btsinfo and \
                            paras["IPADDR"][1:-1] == btsinfo["GSM_IP"]:  # 二层组网，需要包含BSC侧的VLANID配置
                is_bts_mml = True

            # 判断是否为本基站的MML, 如果是，保存MML
            if is_bts_mml == True:
                if c not in btsinfo["MML_MAP"]:
                    btsinfo["MML_MAP"][c] = []
                btsinfo["MML_MAP"][c].append(line)
                btsinfo["ALL_MML_LIST"].append(line)
            pass

        # 建立小区ID和小区名对应关系
        btsinfo["CELLID_2_CELLNAME"] = {}
        btsinfo["CELL_INFO"] = {}
        for mml in btsinfo["MML_MAP"]["ADD GCELL"]:
            c, paras = self.split_mml(mml)
            cellid = paras["CELLID"]
            paras["CELLNAME"] = paras["CELLNAME"][1:-1]
            paras["TRXID_LIST"] = []
            btsinfo["CELLID_2_CELLNAME"][cellid] = paras["CELLNAME"]
            btsinfo["CELL_INFO"][cellid] = paras

        if btsinfo["BTSTYPE"] == "EGBTS":
            btsinfo["BIND_TRXID_LIST"] = btsinfo["TRXID_LIST"]

        # 建立RXU信息表
        btsinfo["RXU_INFO"] = {}
        if "ADD BTSRXUBRD" in btsinfo["MML_MAP"]:
            for mml in btsinfo["MML_MAP"]["ADD BTSRXUBRD"]:
                c, paras = self.split_mml(mml)
                rxu_pos = (paras["CN"], paras["SRN"], paras["SN"])
                btsinfo["RXU_INFO"][rxu_pos] = paras
                btsinfo["RXU_INFO"][rxu_pos]["BAND"] = None
                btsinfo["RXU_INFO"][rxu_pos]["TRXID_LIST"] = []
                btsinfo["RXU_INFO"][rxu_pos]["CELLID_LIST"] = []
            for mml in btsinfo["MML_MAP"]["SET BTSRXUBP"]:
                c, paras = self.split_mml(mml)
                rxu_pos = (paras["CN"], paras["SRN"], paras["SN"])
                for p in ["", "1", "2", "3"]:
                    send_rcv_para_name = "SNDRCVMODE" + p
                    if send_rcv_para_name in paras:  # 收发模式
                        paras["PORT_ASSIGN_MODE"] = paras[send_rcv_para_name]
                btsinfo["RXU_INFO"][rxu_pos].update(paras)
            pass

        # 建立TRX信息表
        btsinfo["TRX_INFO"] = {}
        for mml in btsinfo["MML_MAP"]["ADD GTRX"]:
            c, paras = self.split_mml(mml)
            trxid = paras["TRXID"]
            freq = paras["FREQ"]
            cellid = paras["CELLID"]
            cell_type = btsinfo["CELL_INFO"][cellid]["TYPE"]
            paras["BAND"] = self.get_GSM_Band_By_Freq(int(freq), cell_type)
            paras["CELLNAME"] = btsinfo["CELL_INFO"][cellid]["CELLNAME"]
            btsinfo["TRX_INFO"][trxid] = paras
            btsinfo["CELL_INFO"][cellid]["TRXID_LIST"].append(trxid)

        if "ADD TRXBIND2PHYBRD" in btsinfo["MML_MAP"]:
            for mml in btsinfo["MML_MAP"]["ADD TRXBIND2PHYBRD"]:
                c, paras = self.split_mml(mml)
                trxid = paras["TRXID"]
                rxu_pos = (paras["CN"], paras["SRN"], paras["SN"])
                paras["RXU_POS"] = rxu_pos
                btsinfo["TRX_INFO"][trxid].update(paras)
                btsinfo["RXU_INFO"][rxu_pos]["TRXID_LIST"].append(trxid)
                cellid = btsinfo["TRX_INFO"][trxid]["CELLID"]
                if cellid not in btsinfo["RXU_INFO"][rxu_pos]["CELLID_LIST"]:
                    btsinfo["RXU_INFO"][rxu_pos]["CELLID_LIST"].append(cellid)
                    btsinfo["RXU_INFO"][rxu_pos]["BAND"] = btsinfo["TRX_INFO"][trxid]["BAND"]

            for mml in btsinfo["MML_MAP"]["SET GTRXDEV"]:
                c, paras = self.split_mml(mml)
                trxid = paras["TRXID"]
                btsinfo["TRX_INFO"][trxid].update(paras)
                rxu_pos = btsinfo["TRX_INFO"][trxid]["RXU_POS"]  # 找到TRXID对应的RXUPOS
                if "TxRxMode" not in btsinfo["RXU_INFO"][rxu_pos]:
                    send_mode = "_2T" if paras["SNDMD"] == "DIVERSITY" else ""  # 发分集
                    recv_mode = "_4R" if paras["RCVMD"] == "FOURDIVERSITY" else ""  # 四接收分集
                    btsinfo["RXU_INFO"][rxu_pos]["TxRxMode"] = (send_mode, recv_mode)
            pass

        # 建立RCN信息表
        btsinfo["RCN_INFO"] = {}
        if "ADD BTSRXUCHAIN" in btsinfo["MML_MAP"]:
            for mml in btsinfo["MML_MAP"]["ADD BTSRXUCHAIN"]:
                c, paras = self.split_mml(mml)
                rcn = paras["RCN"]
                btsinfo["RCN_INFO"][rcn] = paras
            pass

        # 获得IP信息
        if "SET BTSIP" in btsinfo["MML_MAP"]:
            c, paras = self.split_mml(btsinfo["MML_MAP"]["SET BTSIP"][0])
            if paras["BTSMUTIP"] == "NO":
                btsinfo["GSM_IP"] = paras["BTSIP"][1:-1]
                btsinfo["BSC_IP"] = paras["BSCIP"][1:-1]
        if "ADD BTSDEVIP" in btsinfo["MML_MAP"]:
            c, paras = self.split_mml(btsinfo["MML_MAP"]["ADD BTSDEVIP"][0])
            btsinfo["GSM_IP"] = paras["IP"][1:-1]
            btsinfo["GSM_MASK"] = paras["MASK"][1:-1]
        if "ADD BTSIPRT" in btsinfo["MML_MAP"]:
            c, paras = self.split_mml(btsinfo["MML_MAP"]["ADD BTSIPRT"][0])
            if paras["RTTYPE"] == "NEXTHOP":
                btsinfo["GSM_GATEWAY"] = paras["NEXTHOP"][1:-1]
        if "SET BTSVLAN" in btsinfo["MML_MAP"]:
            c, paras = self.split_mml(btsinfo["MML_MAP"]["SET BTSVLAN"][0])
            btsinfo["GSM_VLAN"] = paras["VLANID"]

        # 对EGBTS，获得IP信息
        if btsinfo["BTSTYPE"] == "EGBTS":
            c, paras = self.split_mml(btsinfo["MML_MAP"]["ADD SCTPLNK"][0])
            btsinfo["BSC_IP"] = paras["LOCIP1"][1:-1]
            btsinfo["GSM_IP"] = paras["PEERIP1"][1:-1]

        # 查找BTS的IP地址路由
        if "GSM_IP" in btsinfo:
            itf_board_srn, itf_board_sn = btsinfo["IP_2_SRN_SN"][btsinfo["BSC_IP"]]  # 获得IP地址所在的框槽号
            btsinfo["MML_MAP"]["ADD IPRT"] = []
            for line in iprt_mml_list:
                c, paras = self.split_mml(line)
                dst_ip = paras["DSTIP"][1:-1]
                dst_mask = paras["DSTMASK"][1:-1]
                if dst_ip == self.get_network_by_ip(btsinfo["GSM_IP"], dst_mask):  # 路由匹配
                    if paras["SRN"] == itf_board_srn:  # 且在同一框
                        btsinfo["MML_MAP"]["ADD IPRT"].append(line)

        return btsinfo

    # 输入nodeb_name, 返回该BTS对应参数信息，包含所有MML
    @API_RECORD
    def get_NodeB_Info(self, nodeb_name, encoding="GBK"):
        nodeb_info_map = load_Object("ALL_NODEB_CFGMML_INFO", {})
        if len(nodeb_info_map) == 0:
            _, nodeb_info_map = self.inner_Parse_CFGMML_File(encoding)
        if nodeb_name not in nodeb_info_map:
            self.print_msg("Error: NodeB=%s is not found in all CFGMML files" % nodeb_name)
            return None

        nodeb_info = nodeb_info_map[nodeb_name]
        nodebid = nodeb_info["NODEBID"]
        cellid_list = nodeb_info["UCELLID_LIST"]

        iprt_mml_list = []
        atmlogicport_mml_list = []
        iplogicport_mml_list = []
        self.print_msg("Read RNC CFGMML file "+ nodeb_info["CFGMML_FILE"])
        cmd_lines = load_TXT_File(nodeb_info["CFGMML_FILE"], encoding)
        for line in cmd_lines:
            c, paras = self.split_mml(line)
            if c is None:
                continue
            elif c == "ADD IPRT":  # 保存ADD IPRT命令行，用于后续分析处理
                iprt_mml_list.append(line)
            elif c == "ADD ATMLOGICPORT": # 保存，用于后续通过LPN还原
                atmlogicport_mml_list.append(line)
            elif c == "ADD IPLOGICPORT": # 保存，用于后续通过LPN还原
                iplogicport_mml_list.append(line)

            # 判断是否为本基站的命令，如是则保存
            is_bts_mml = False
            if "NODEBID" in paras and paras["NODEBID"] == nodebid:
                is_bts_mml = True
            elif "NODEB_NAME" in paras and paras["NODEB_NAME"] == nodeb_name:
                is_bts_mml = True
            elif "ANI" in paras and paras["ANI"] == nodeb_info["ANI"]:
                is_bts_mml = True
            elif "SAC" in paras and paras["SAC"] in nodeb_info["SAC_LIST"]:
                is_bts_mml = True
            elif "CELLID" in paras and paras["CELLID"] in cellid_list:
                is_bts_mml = True
            elif "NCELLID" in paras and paras["NCELLID"] in cellid_list:
                is_bts_mml = True
            elif "SCTPLNKID" in paras and paras["SCTPLNKID"] in nodeb_info["SCTPLNKID_LIST"]:
                is_bts_mml = True
            elif "SAALLNKN" in paras and paras["SAALLNKN"] in nodeb_info["SAALLNKN_LIST"]:
                is_bts_mml = True

            # 判断是否为本基站的MML, 如果是，保存MML
            if is_bts_mml == True:
                if c not in nodeb_info["MML_MAP"]:
                    nodeb_info["MML_MAP"][c] = []
                nodeb_info["MML_MAP"][c].append(line)
                nodeb_info["ALL_MML_LIST"].append(line)

        # 获得NodeB IP地址
        if "ADD SCTPLNK" in nodeb_info["MML_MAP"]:
            nodeb_ip_list = []
            rnc_ip_list = []
            for mml in nodeb_info["MML_MAP"]["ADD SCTPLNK"]:
                c, paras = self.split_mml(mml)
                rnc_ip1 = paras["LOCIP1"][1:-1]
                rnc_ip2 = paras["LOCIP2"][1:-1]
                nodeb_ip = paras["PEERIP1"][1:-1]
                if rnc_ip1 != "0.0.0.0" and rnc_ip1 not in rnc_ip_list:
                    rnc_ip_list.append(rnc_ip1)
                if rnc_ip2 != "0.0.0.0" and rnc_ip2 not in rnc_ip_list:
                    rnc_ip_list.append(rnc_ip2)
                if nodeb_ip != "0.0.0.0" and nodeb_ip not in nodeb_ip_list:
                    nodeb_ip_list.append(nodeb_ip)

            nodeb_info["UMTS_IP"] = nodeb_ip_list[0]
            nodeb_info["RNC_IP"] = rnc_ip_list[0]
            if len(rnc_ip_list) > 1:
                nodeb_info["RNC_IP2"] = rnc_ip_list[1]

            # 查找NodeB的IP地址路由
            itf_board_srn, itf_board_sn = nodeb_info["IP_2_SRN_SN"][nodeb_info["RNC_IP"]]
            nodeb_info["MML_MAP"]["ADD IPRT"] = []
            for line in iprt_mml_list:
                c, paras = self.split_mml(line)
                dst_ip = paras["DSTIP"][1:-1]
                dst_mask = paras["DSTMASK"][1:-1]
                if dst_ip == self.get_network_by_ip(nodeb_info["UMTS_IP"], dst_mask):  # 路由匹配
                    if paras["SRN"] == itf_board_srn:  # 且在同一框
                        nodeb_info["MML_MAP"]["ADD IPRT"].append(line)
            pass

        # 通过IPPATH的LPN还原IPLOGICPORT
        if "ADD IPPATH" in nodeb_info["MML_MAP"]:
            try:
                for ippath in nodeb_info["MML_MAP"]["ADD IPPATH"]:
                    c, paras = self.split_mml(ippath)
                    lpn = paras["LPN"]
                    for item in iplogicport_mml_list:
                        tmp_c, tmp_paras = self.split_mml(item)
                        if lpn == tmp_paras["LPN"]:
                            if tmp_c not in nodeb_info["MML_MAP"]:
                                nodeb_info["MML_MAP"][tmp_c] = []
                            if item not in nodeb_info["MML_MAP"][tmp_c]:
                                nodeb_info["MML_MAP"][tmp_c].append(item)
                                nodeb_info["ALL_MML_LIST"].append(item)
            except:
                pass

        # 通过AAL2PATH的CARRYVPN还原ATMLOGICPORT
        if "ADD AAL2PATH" in nodeb_info["MML_MAP"]:
            for ippath in nodeb_info["MML_MAP"]["ADD AAL2PATH"]:
                c, paras = self.split_mml(ippath)
                lpn = paras["CARRYVPN"]
                for item in atmlogicport_mml_list:
                    tmp_c, tmp_paras = self.split_mml(item)
                    if lpn == tmp_paras["LPN"]:
                        if tmp_c not in nodeb_info["MML_MAP"]:
                            nodeb_info["MML_MAP"][tmp_c] = []
                        if item not in nodeb_info["MML_MAP"][tmp_c]:
                            nodeb_info["MML_MAP"][tmp_c].append(item)
                            nodeb_info["ALL_MML_LIST"].append(item)

        return nodeb_info

    # 为GSM小区计算所在物理扇区号
    @API_RECORD
    def calculate_SectorNo_For_GSM_Cell(self, cell_info_map, cellname_format_map):
        for (cellid, cell_info) in cell_info_map.items():
            cellname = cell_info["CELLNAME"]
            cell_type = cell_info["TYPE"]
            cell_id = cell_info['CELLID']
            if cell_type == "DCS1800":
                band_str = "GO1800"
            elif cell_type == "PCS1900":
                band_str = "GO1900"
            elif cell_type in ["GSM900", "GSM900_DCS1800"]:
                band_str = "GO900"
            else:
                band_str = "GO850"
            one_band_format_map = cellname_format_map[band_str]
            sector_no = self.calculate_SectorNo_For_Cell(band_str, cellname, one_band_format_map)
            cell_info["SECTOR_NO"] = sector_no
            cell_info["BAND_STR"] = band_str
            msg = cellname + " " + cell_type + " " + sector_no + " " + band_str
            # if band_str not in self.Analyze_Cache['Band_Sector_To_GLOCELLID']:
            #     self.Analyze_Cache['Band_Sector_To_GLOCELLID'][band_str] = {}
            # if sector_no not in self.Analyze_Cache['Band_Sector_To_GLOCELLID'][band_str]:
            #     self.Analyze_Cache['Band_Sector_To_GLOCELLID'][band_str][sector_no] = []
            # self.Analyze_Cache['Band_Sector_To_GLOCELLID'][band_str][sector_no].append(cell_id)
            self.print_msg(msg)
        pass

    # 输出GBTS共主控改造的MML, 以及回退的MML
    @API_RECORD
    def get_GBTS_Convert_MML_In_BSC(self, btsinfo, ip_reconstruction=False):
        if btsinfo["BTSTYPE"] == "EGBTS":
            self.print_msg("Error: BTS=%s is already EGBTS, cannot convert")
            return None, None

        cmd_lines = []
        cmd_lines.append(
            "//CoMPT Convert for BTS=%s on BSC=%s, %s" % (btsinfo["BTSNAME"], btsinfo["BSC_NAME"], btsinfo["BSC_TYPE"]))

        # 去激活、解绑定和删除基站命令
        self.inner_GBTS_Covert_MML_deactive_unbind_delete(cmd_lines, btsinfo)

        # 增加eGBTS
        self.inner_GBTS_Convert_MML_add_egbts(cmd_lines, btsinfo)

        # 增加ip 配置
        if ip_reconstruction == True:
            self.inner_ip_reconstruction(cmd_lines, btsinfo)

        # 绑定小区和TRX
        self.inner_GBTS_Convert_MML_bind(cmd_lines, btsinfo)

        # 改造时，部分GCELL小区参数会发生变化，下面的MML把小区的参数修改为和之前一致。
        self.innner_GBTS_Convert_MML_set_cell_trx_parameter(cmd_lines, btsinfo)

        #
        cmd_lines.append("SET DATACONVERTSWITCH: TYPE=BTS_SINGLEOM_UPGRADE, SWITCH=OFF;")

        # 激活基站
        cmd_lines.append("//activate BTS")
        cmd_lines.append("ACT BTS: IDTYPE=BYID, BTSID=%s, TRXIDTYPE=BYID;" % btsinfo["BTSID"])
        cmd_lines.append("")

        # 获得回退MML命令
        rollback_mml_list = self.inner_GBTS_Convert_MML_rollback(btsinfo, ip_reconstruction)

        return cmd_lines, rollback_mml_list

    @API_RECORD
    def modify_GLoCellD_GtrxGroupID_For_EGBTS_In_BSC(self, btsinfo):
        mml_list = []
        mml_list.append("//Modify GTRXGROUP config for BTS=%s on BSC=%s, %s" % (
            btsinfo["BTSNAME"], btsinfo["BSC_NAME"], btsinfo["BSC_TYPE"]))
        for trxid in btsinfo["TRXID_LIST"]:
            info = btsinfo["TRX_INFO"][trxid]
            gtrxgroupid = info["GTRXGROUPID"]
            mml_list.append("MOD GTRX: IDTYPE=BYID, TRXID=%s, GTRXGROUPID=%s;" % (trxid, gtrxgroupid))
        mml_list.append("")
        for (cellid, cellinfo) in btsinfo["CELL_INFO"].items():
            if cellinfo["OLD_GLOCELLID"] == cellinfo["GLOCELLID"]: continue
            locellid = cellinfo["GLOCELLID"]
            mml_list.append('MOD GCELL: IDTYPE=BYNAME, CELLNAME="%s", GLOCELLID=%s;' % (cellinfo["CELLNAME"], locellid))
        mml_list.append("")

        rollback_mml_list = []
        rollback_mml_list.append("//Rollback GTRXGROUP config for BTS=%s on BSC=%s, %s" % (
        btsinfo["BTSNAME"], btsinfo["BSC_NAME"], btsinfo["BSC_TYPE"]))
        for line in btsinfo["MML_MAP"]["ADD GTRX"]:
            c, paras = self.split_mml(line)
            rollback_mml_list.append(
                "MOD GTRX: IDTYPE=BYID, TRXID=%s, GTRXGROUPID=%s;" % (paras["TRXID"], paras["GTRXGROUPID"]))
        rollback_mml_list.append("")
        for (cellid, cellinfo) in btsinfo["CELL_INFO"].items():
            if cellinfo["OLD_GLOCELLID"] == cellinfo["GLOCELLID"]: continue
            old_locellid = cellinfo["OLD_GLOCELLID"]
            rollback_mml_list.append(
                'MOD GCELL: IDTYPE=BYNAME, CELLNAME="%s", GLOCELLID=%s;' % (cellinfo["CELLNAME"], old_locellid))
        rollback_mml_list.append("")
        return mml_list, rollback_mml_list

    @API_RECORD
    def _set_sctplnkn_dic(self, sctplnkn_dic, srn, sn, saallnkid):
        tmp_sctplnkn = saallnkid[-4:]
        if tmp_sctplnkn[0] == '0':
            sctplnkn = tmp_sctplnkn[1:4]
        else:
            sctplnkn = tmp_sctplnkn
        if srn == '0' and sn == '0':
            sctplnk_id = sctplnkn
        elif srn == '0' and sn != '0':
            sctplnk_id = sn + tmp_sctplnkn
        else:
            sctplnk_id = srn + '0' + sn + tmp_sctplnkn
        sctplnkn_dic[int(sctplnkn)] = sctplnk_id

    @API_RECORD
    def modify_NodeB_IP_In_RNC(self, nodebinfo, nodeb_ip, om_ip, atm2ip_flag=False, old_mml_flag=True):
        mml_list = []
        if old_mml_flag == True:
            mml_list.append("//old config for %s on RNC=%s, RNC_TYPE=%s" % (
            nodebinfo["NODEBNAME"], nodebinfo["RNC_NAME"], nodebinfo["RNC_TYPE"]))
            # Output old MML config
            for cmd in ["ADD UNODEB", "ADD ADJNODE", "ADD ADJMAP", "ADD IPRT", "ADD SCTPLNK", "ADD IPPATH", "ADD SAALLNK",
                        "ACT IPPM", "ACT IPPOOLPM", "ADD UNCP", "ADD UCCP", "ADD UNODEBIP", "ADD IPMUX", "ACT IPPOOLPM"]:
                if cmd not in nodebinfo["MML_MAP"]: continue
                cmd_lines = nodebinfo["MML_MAP"][cmd]
                cmd_lines = ["//" + l for l in cmd_lines]
                mml_list.extend(cmd_lines)
            mml_list.append("\n")

        # for ip change
        if nodeb_ip != nodebinfo["UMTS_IP"]:
            # Modify IP for SCTPLNK
            for mml in nodebinfo["MML_MAP"]["ADD SCTPLNK"]:
                c, paras = self.split_mml(mml)
                mml_list.append('MOD SCTPLNK:SCTPLNKID=%s, PEERIP1="%s";' % (paras["SCTPLNKID"], nodeb_ip))
            # DEA IPPM
            if "ACT IPPM" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ACT IPPM"]:
                    c, paras = self.split_mml(mml)
                    mml_list.append("DEA IPPM:ANI=%s, PATHID=%s;" % (paras["ANI"], paras["PATHID"]))
            # DEA IPPOOLPM
            if "ACT IPPOOLPM" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ACT IPPOOLPM"]:
                    c, paras = self.split_mml(mml)
                    mml_list.append(
                        "DEA IPPOOLPM: ANI=%s, SIPTYPE=%s, PHB=%s;" % (paras["ANI"], paras["SIPTYPE"], paras["PHB"]))
            # Remove IPMUX
            if "ADD IPMUX" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ADD IPMUX"]:
                    c, paras = self.split_mml(mml)
                    mml_list.append("RMV IPMUX: IPMUXINDEX=%s;" % (paras["IPMUXINDEX"]))
            # Remove IPPATH
            if "ADD IPPATH" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ADD IPPATH"]:
                    c, paras = self.split_mml(mml)
                    mml_list.append("RMV IPPATH: ANI=%s, PATHID=%s;" % (paras["ANI"], paras["PATHID"]))

            # Remove IPRT, then ADD IPRT
            if "ADD IPRT" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ADD IPRT"]:
                    c, paras = self.split_mml(mml)
                    dst_mask = paras["DSTMASK"][1:-1]
                    if dst_mask in ["255.255.255.255", "255.255.255.252"]:
                        mml_list.append(
                            'RMV IPRT:SRN=%s, SN=%s, DSTIP="%s", DSTMASK="%s", NEXTHOPTYPE=Gateway, NEXTHOP="%s";' %
                            (paras["SRN"], paras["SN"], nodeb_ip, dst_mask, paras["NEXTHOP"]))
                        dstip = self.get_network_by_ip(nodeb_ip, dst_mask)
                        mml_list.append(nodebinfo["MML_MAP"]["ADD IPRT"][0].replace(paras["DSTIP"][1:-1], dstip))

            # ADD IPPATH
            if "ADD IPPATH" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ADD IPPATH"]:
                    c, paras = self.split_mml(mml)
                    mml = mml.replace(paras["PEERIPADDR"][1:-1], nodeb_ip)
                    mml_list.append(mml)
            # ADD IPMUX
            if "ADD IPMUX" in nodebinfo["MML_MAP"]:
                mml_list.extend(nodebinfo["MML_MAP"]["ADD IPMUX"])
            # ACT IPPM
            if "ACT IPPM" in nodebinfo["MML_MAP"]:
                mml_list.extend(nodebinfo["MML_MAP"]["ACT IPPM"])
            # ACT IPPOOLPM
            if "ACT IPPOOLPM" in nodebinfo["MML_MAP"]:
                mml_list.extend(nodebinfo["MML_MAP"]["ACT IPPOOLPM"])
            # MOD UNODEBIP
            mml_list.append('MOD UNODEBIP: NODEBID=%s, NBTRANTP=IPTRANS_IP, NBIPOAMIP="%s", NBIPOAMMASK="%s";'
                            % (nodebinfo["NODEBID"], om_ip, nodebinfo["OM_IP_MASK"]))
            pass

        # for ATM siwtch to IP
        if atm2ip_flag == True:
            uccp_pn = ''
            ani = ''
            sctplnkn_dic = {}
            c, paras = self.split_mml(nodebinfo["MML_MAP"]["ADD UNODEB"][0])
            srn,sn = paras["SRN"],paras["SN"]

            # get ani
            if "ADD ADJNODE" in nodebinfo["MML_MAP"]:
                c, paras = self.split_mml(nodebinfo["MML_MAP"]["ADD ADJNODE"][0])
                ani = paras["ANI"]

            # get uccp_pn
            if "ADD UCCP" in nodebinfo["MML_MAP"]:
                c, paras = self.split_mml(nodebinfo["MML_MAP"]["ADD UCCP"][0])
                uccp_pn = paras["PN"]

            for cell_id in nodebinfo["UCELLID_LIST"]:
                mml_list.append("DEA UCELL: CELLID=%s;" % cell_id)
            mml_list.append("")

            # remove UCCP/UNCP/UNODEBIP
            mml_list.append("RMV UCCP: IDTYPE=BYID, NODEBID=%s, PN=%s;" % (nodebinfo["NODEBID"], uccp_pn))
            mml_list.append("RMV UNCP: IDTYPE=BYID, NODEBID=%s;" % nodebinfo["NODEBID"])
            mml_list.append("RMV UNODEBIP: IDTYPE=BYID, NODEBID=%s;\n" % nodebinfo["NODEBID"])

            # remove AAL2PATH
            if "ADD AAL2PATH" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ADD AAL2PATH"]:
                    c, paras = self.split_mml(mml)
                    mml_list.append("RMV AAL2PATH: ANI=%s, PATHID=%s;" % (paras["ANI"], paras["PATHID"]))
            # remove AAL2RT
            if "ADD AAL2RT" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ADD AAL2RT"]:
                    c, paras = self.split_mml(mml)
                    mml_list.append("RMV AAL2RT: RTX=%s, FORCEEXECUTE=YES;" % paras["RTX"])
            mml_list.append("")

            # remove ADJMAP
            mml_list.append("RMV ADJMAP: ANI=%s, ITFT=IUB, CNMNGMODE=SHARE, FORCEEXECUTE=YES;\n" % ani)

            # dea IPPM
            if "ACT IPPM" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ACT IPPM"]:
                    c, paras = self.split_mml(mml)
                    mml_list.append("DEA IPPM: ANI=%s, PATHID=%s;" % (paras["ANI"], paras["PATHID"]))
            mml_list.append("")

            # remove IPPATH
            if "ADD IPPATH" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ADD IPPATH"]:
                    c, paras = self.split_mml(mml)
                    mml_list.append("RMV IPPATH: ANI=%s, PATHID=%s;" % (paras["ANI"], paras["PATHID"]))
            mml_list.append("")

            # remove ADJNODE
            mml_list.append("RMV ADJNODE: ANI=%s;\n" % ani)

            # rmv SAALLNK
            if "ADD ADJNODE" in nodebinfo["MML_MAP"]:
                c, paras = self.split_mml(nodebinfo["MML_MAP"]["ADD ADJNODE"][0])
                third_saallnkid = int(paras["SAALLNKID"])
                str_saallnkid = str(third_saallnkid - 2)
                mml_list.append("RMV SAALLNK: SAALLNKID=%s;" % str_saallnkid)
                self._set_sctplnkn_dic(sctplnkn_dic, srn, sn, str_saallnkid)
                str_saallnkid = str(third_saallnkid - 1)
                mml_list.append("RMV SAALLNK: SAALLNKID=%s;" % str_saallnkid)
                self._set_sctplnkn_dic(sctplnkn_dic, srn, sn, str_saallnkid)
                mml_list.append("RMV SAALLNK: SAALLNKID=%s;" % paras["SAALLNKID"])
            mml_list.append("")

            # remove ATMLOGICPORT and IPLOGICPORT
            if "ADD ATMLOGICPORT" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ADD ATMLOGICPORT"]:
                    c, paras = self.split_mml(mml)
                    mml_list.append("RMV ATMLOGICPORT: SRN=%s, SN=%s, LPN=%s;" % (paras["SRN"], paras["SN"], paras["LPN"]))
            if "ADD IPLOGICPORT" in nodebinfo["MML_MAP"]:
                for mml in nodebinfo["MML_MAP"]["ADD IPLOGICPORT"]:
                    c, paras = self.split_mml(mml)
                    mml_list.append("RMV IPLOGICPORT: SRN=%s, SN=%s, LPN=%s;" % (paras["SRN"], paras["SN"], paras["LPN"]))
            mml_list.append("")

            #add SCTPLNK
            peer_pn = 58081
            sctplnkn_list = sorted(sctplnkn_dic.keys())
            for sctplnkn in sctplnkn_list:
                mml_list.append('ADD SCTPLNK: APP=NBAP, SCTPLNKID=%s, SRN=%s, SN=%s, SCTPLNKN=%d, MODE=SERVER, '
                                'DSCP=48, SPECIFYLOCPNFLAG=NO, LOCIP1="%s", LOCIP2="0.0.0.0", PEERIP1="%s", PEERIP2="0.0.0.0", '
                                'PEERPN=%d, LOGPORTFLAG=NO, RTOMIN=150, RTOMAX=500, RTOINIT=400, RTOALPHA=12, RTOBETA=25, '
                                'TSACK=100, HBINTER=3000, MAXASSOCRETR=10, MAXPATHRETR=9, CHKSUMTX=NO, CHKSUMRX=NO, '
                                'CHKSUMTYPE=CRC32, MTU=1480, VLANFLAG1=DISABLE, VLANFLAG2=DISABLE, CROSSIPFLAG=UNAVAILABLE, '
                                'SWITCHBACKFLAG=NO, BUNDLINGFLAG=YES, REMARK="%s", PEERMULTIFASTRETRANFLAG=YES;' %
                                (sctplnkn_dic[sctplnkn], srn, sn, sctplnkn, nodebinfo["RNC_IBU_IP"], nodeb_ip, peer_pn, nodebinfo["NODEBNAME"] ))
                peer_pn -= 1
            mml_list.append("")

            # add ADJNODE
            mml_list.append('ADD ADJNODE: ANI=%s, NAME="%s", NODET=IUB, NODEBID=%s, TRANST=IP, ISIPPOOL=NO;\n' % (ani, nodebinfo["NODEBNAME"], nodebinfo["NODEBID"]))

            # add IPPATH
            ippath_list = [[0,"BE","Best Effort"], [26,"AF31","-"], [34,"AF41","Video"], [40,"AF42","-"], [48,"EF","-"]]
            for ippath in ippath_list:
                mml_list.append('ADD IPPATH: ANI=%s, PATHID=%d, IPADDR="%s", PEERIPADDR="%s", VLANFLAG=DISABLE, CARRYFLAG=NULL, PATHT=%s, PEERMASK="%s", '
                            'TXBW=3000000, RXBW=3000000, PATHCHK=DISABLED, ITFT=IUB, TRANST=IP, TRMLOADTHINDEX=15, REMARK="%s";'
                            % (ani, ippath[0], nodebinfo["RNC_IBU_IP"], nodeb_ip, ippath[1], nodebinfo["UMTS_IP_MASK"], ippath[2]))

            mml_list.append('ADD IPPATH: ANI=%s, PATHID=46, IPADDR="%s", PEERIPADDR="%s", ECHOIP="%s", VLANFLAG=DISABLE, PERIOD=4, CHECKCOUNT=3, CARRYFLAG=NULL, PATHT=AF43, PEERMASK="%s", '
                            'TXBW=3000000, RXBW=3000000, PATHCHK=ENABLED, ITFT=IUB, TRANST=IP, TRMLOADTHINDEX=15, ICMPPKGLEN=64, CHECKT=ICMP, REMARK="Voice";\n'
                            % (ani, nodebinfo["RNC_IBU_IP"], nodeb_ip, nodeb_ip, nodebinfo["UMTS_IP_MASK"]))

            # ACT IPPM
            ippm_list = [[0, "O1E1_R5E2"], [34, "O5E2_R1E2"], [46, "O1E2_R5E3"]]
            for ippm in ippm_list:
                mml_list.append("ACT IPPM: ANI=%s, PATHID=%d, ISQOSPATH=NO, PMPRD=1, LOSTPKTDETECTSW=ON, LOSTPKTALARMTHD=%s;" % (ani, ippm[0], ippm[1]))
            mml_list.append("")

            #mod UNODEB
            mml_list.append("MOD UNODEB: NODEBID=%d, TNLBEARERTYPE=IP_TRANS;\n" % nodebinfo["NODEBID"])

            # add IPRT, the vdf customer will config it, delete it
            #mml_list.append('ADD IPRT: SRN=%s, SN=%s, DSTIP="%s", DSTMASK="%s", NEXTHOPTYPE=Gateway, NEXTHOP="%s", PRIORITY=HIGH, REMARK="To-NodeB";\n'
            #                % (nodebinfo["RNC_SRN"], nodebinfo["RNC_SN"], nodebinfo["DST_IP"], nodebinfo["UMTS_IP_MASK"], nodebinfo["RNC_NEXTHOP"]))

            # add UNODEBIP/UNCP/UCCP/ADJNODE/ADJMAP
            mml_list.append('ADD UNODEBIP: IDTYPE=BYID, NODEBID=%s, NBTRANTP=IPTRANS_IP, NBIPOAMIP="%s", NBIPOAMMASK="%s", IPSRN=%s, IPSN=%s, '
                            'IPLOGPORTFLAG=NO, VLANFLAG=DISABLE;' % (nodebinfo["NODEBID"], om_ip, nodebinfo["OM_IP_MASK"], nodebinfo["RNC_SRN"], nodebinfo["RNC_SN"]))
            if len(sctplnkn_dic) >= 2:
                mml_list.append("ADD UNCP: IDTYPE=BYID, NODEBID=%d, CARRYLNKT=SCTP, SCTPLNKN=%d, SCTPLNKID=%s;" % (nodebinfo["NODEBID"], sctplnkn_list[0], sctplnkn_dic[sctplnkn_list[0]]))
                mml_list.append("ADD UCCP: IDTYPE=BYID, NODEBID=%d, PN=%s, CARRYLNKT=SCTP, SCTPLNKN=%d, SCTPLNKID=%s;\n" % (nodebinfo["NODEBID"], pn, sctplnkn_list[1], sctplnkn_dic[sctplnkn_list[1]]))
            mml_list.append("ADD ADJMAP: ANI=%s, ITFT=IUB, TRANST=IP, CNMNGMODE=SHARE, TMIGLD=44, TMISLV=44, TMIBRZ=44, FTI=22;\n" % ani)

            for cell_id in nodebinfo["UCELLID_LIST"]:
                mml_list.append("ACT UCELL: CELLID=%s;" % cell_id)

        return mml_list

    # 输出两个NodeB合并的MML
    @API_RECORD
    def merge_NodeB_In_RNC(self, nodebinfo_2, nodebinfo, id_step=10):
        old_name = nodebinfo_2["NODEBNAME"]
        new_name = nodebinfo["NODEBNAME"]

        mml_list = []
        mml_list.append("\n\n//Merge NodeB=%s to NodeB=%s" % (old_name, new_name))
        mml_list.append('DEA UNODEB: IDTYPE=BYNAME, NodeBName="%s";' % old_name)
        for ucellid in nodebinfo_2["UCELLID_LIST"]:
            mml_list.append('RMV UCELL: CellId=%s;' % ucellid)
        mml_list.append("")

        for locellid in nodebinfo_2["LOCELLID_LIST"]:
            mml_list.append('RMV ULOCELL: IDTYPE=BYNAME, NodeBName="%s", LoCell=%s;' % (old_name, locellid))
        mml_list.append("")

        mml_list.append('RMV UNODEB: IDTYPE=BYNAME, NodeBName="%s";' % old_name)
        mml_list.append("")

        for locellid in nodebinfo_2["LOCELLID_LIST"]:
            mml_list.append(
                'ADD ULOCELL: IDTYPE=BYNAME, NodeBName="%s", LoCell=%s;' % (new_name, str(int(locellid) + id_step)))
        mml_list.append("")

        for line in nodebinfo_2["MML_MAP"]["ADD UCELLSETUP"]:
            c, paras = self.split_mml(line)
            locell = int(paras["LOCELL"])
            line = line.replace("LOCELL=%s" % locell, "LOCELL=%s" % str(int(locell) + id_step))
            line = line.replace('NODEBNAME="%s"' % old_name, 'NODEBNAME="%s"' % new_name)
            line = line.replace('CELLNAME="%s"' % paras["CELLNAME"][1:-1],
                                'CELLNAME="%s_%d"' % (new_name, locell + id_step))
            mml_list.append(line)

        # Output other mml
        for mml in nodebinfo_2["ALL_MML_LIST"]:
            c, paras = self.split_mml(mml)
            if c == "ADD UCELLSETUP": continue
            if "CELLID" in paras:
                mml_list.append(mml)
            elif "NCELLID" in paras:
                mml_list.append(mml)

        rollback_mml_list = []
        rollback_mml_list.append("//Rollback Config for NodeB=%s" % (old_name))

        for ucellid in nodebinfo_2["UCELLID_LIST"]:
            rollback_mml_list.append('RMV UCELL: CellId=%s;' % ucellid)
        rollback_mml_list.append("")

        for locellid in nodebinfo_2["LOCELLID_LIST"]:
            rollback_mml_list.append(
                'RMV ULOCELL: IDTYPE=BYNAME, NodeBName="%s", LoCell=%s;' % (new_name, str(int(locellid) + id_step)))
        rollback_mml_list.append("")

        rollback_mml_list.extend(nodebinfo_2["ALL_MML_LIST"])

        return mml_list, rollback_mml_list

    ########################################################################
    ## 内部函数
    # BSC6900 CFGMML, 输入一条MML命令，返回命令名称。
    def get_command_from_cmd_line(self, cmd_line):
        l = cmd_line.strip()
        if len(l) == 0: return None

        p = l.find(":")
        if p == -1: return None

        cmd = l[:p].strip()
        return cmd

    # 首次遍历，获得基站列表
    @API_RECORD
    def inner_Parse_CFGMML_File_aux(self, filename, cmd_lines, bts_info_map, nodeb_info_map):
        bts_id_2_name_map = {}
        nodeb_id_2_name_map = {}

        ip_2_srn_sn = {}
        bsc_ip_map = {}
        rnc_ip_map = {}
        controller_name = ""
        controller_type = "BSC6900"
        for line in cmd_lines:
            cmd = self.get_command_from_cmd_line(line)
            if cmd == "SET SYS":
                c, paras = self.split_mml(line)
                controller_name = paras["SYSOBJECTID"][1:-1] if "SYSOBJECTID" in paras else ""
            elif cmd == "ADD BRD":
                c, paras = self.split_mml(line)
                if paras["BRDCLASS"] == "GPU":
                    controller_type = "BSC6910"
            elif cmd == "ADD BTS":
                c, paras = self.split_mml(line)
                btsname = paras["BTSNAME"][1:-1]
                btsid = paras["BTSID"]
                bts_type = paras["BTSTYPE"]
                bts_info_map[btsname] = {"CFGMML_FILE": filename, "BSC_NAME": controller_name,
                                         "BSC_TYPE": controller_type,
                                         "BTSNAME": btsname, "BTSID": btsid, "BTSTYPE": bts_type, "ANI": "",
                                         "CELLID_LIST": [], "BIND_TRXID_LIST": [], "TRXID_LIST": [],
                                         "SCTPLNKID_LIST": [],
                                         "CHILD_BTSID_LIST": [], "IP_2_SRN_SN": ip_2_srn_sn, "ABIS_BSCIP": bsc_ip_map,
                                         "ALL_MML_LIST": [], "MML_MAP": {}}
                bts_id_2_name_map[btsid] = btsname
            elif cmd == "ADD CELLBIND2BTS":
                c, paras = self.split_mml(line)
                btsid = paras["BTSID"]
                cellid = paras["CELLID"]
                btsname = bts_id_2_name_map[btsid]
                bts_info_map[btsname]["CELLID_LIST"].append(cellid)
            elif cmd == "ADD TRXBIND2PHYBRD":
                c, paras = self.split_mml(line)
                btsid = paras["BTSID"]
                trxid = paras["TRXID"]
                btsname = bts_id_2_name_map[btsid]
                bts_info_map[btsname]["BIND_TRXID_LIST"].append(trxid)
            elif cmd == "ADD ABISCP":
                c, paras = self.split_mml(line)
                btsid = paras["BTSID"]
                btsname = bts_id_2_name_map[btsid]
                sctplnkid = paras["SCTPLNKID"]
                bts_info_map[btsname]["SCTPLNKID_LIST"].append(sctplnkid)
            elif cmd == "SET BTSIP":
                c, paras = self.split_mml(line)
                btsid = paras["BTSID"]
                btsname = bts_id_2_name_map[btsid]
                bts_info_map[btsname]["GSM_IP"] = paras["BTSIP"][1:-1]
                bts_info_map[btsname]["BSC_IP"] = paras["BSCIP"][1:-1]
            elif cmd == "ADD ADJNODE":
                c, paras = self.split_mml(line)
                if "BTSID" in paras:
                    btsid = paras["BTSID"]
                    btsname = bts_id_2_name_map[btsid]
                    bts_info_map[btsname]["ANI"] = paras["ANI"]
                if "NODEBID" in paras:
                    nodeb_id = paras["NODEBID"]
                    if nodeb_id in nodeb_id_2_name_map:
                        nodeb_name = nodeb_id_2_name_map[nodeb_id]
                        nodeb_info_map[nodeb_name]["ANI"] = paras["ANI"]
            elif cmd == "ADD UNODEB":
                c, paras = self.split_mml(line)
                nodeb_name = paras["NODEBNAME"][1:-1]
                nodeb_id = paras["NODEBID"]
                nodeb_info_map[nodeb_name] = {"CFGMML_FILE": filename, "RNC_NAME": controller_name,
                                              "RNC_TYPE": controller_type,
                                              "NODEBNAME": nodeb_name, "NODEBID": nodeb_id,
                                              "UCELLID_LIST": [], "LOCELLID_LIST": [], "SAC_LIST": [],
                                              "SCTPLNKID_LIST": [], "SAALLNKN_LIST": [],
                                              "IP_2_SRN_SN": ip_2_srn_sn, "IUB_RNCIP": rnc_ip_map,
                                              "ALL_MML_LIST": [], "MML_MAP": {}}
                nodeb_id_2_name_map[nodeb_id] = nodeb_name
                nodeb_info_map[nodeb_name]["LOGICRNCID"] = paras["LOGICRNCID"] if "LOGICRNCID" in paras else ""
            elif cmd == "ADD UCELLSETUP":
                c, paras = self.split_mml(line)
                nodeb_name = paras["NODEBNAME"][1:-1]
                cellid = paras["CELLID"]
                locellid = paras["LOCELL"]
                sac = paras["SAC"]
                nodeb_info_map[nodeb_name]["UCELLID_LIST"].append(cellid)
                nodeb_info_map[nodeb_name]["LOCELLID_LIST"].append(locellid)
                nodeb_info_map[nodeb_name]["SAC_LIST"].append(sac)
            elif cmd in ["ADD UNCP", "ADD UCCP"]:
                c, paras = self.split_mml(line)
                nodeb_id = paras["NODEBID"]
                nodeb_name = nodeb_id_2_name_map[nodeb_id]
                if "SCTPLNKID" in paras:
                    sctplnkid = paras["SCTPLNKID"]
                    nodeb_info_map[nodeb_name]["SCTPLNKID_LIST"].append(sctplnkid)
                if "SAALLNKN" in paras:
                    saallnkn = paras["SAALLNKN"]
                    nodeb_info_map[nodeb_name]["SAALLNKN_LIST"].append(saallnkn)
            elif cmd in ["ADD ETHIP", "ADD DEVIP", "ADD ETHTRKIP"]:
                c, paras = self.split_mml(line)
                ip = paras["IPADDR"][1:-1]
                ip_2_srn_sn[ip] = (paras["SRN"], paras["SN"])
            elif cmd == "ADD SCTPLNK":
                c, paras = self.split_mml(line)
                ip = paras["LOCIP1"][1:-1]
                if paras["APP"] == "ABISCP":
                    if ip not in bsc_ip_map:
                        bsc_ip_map[ip] = 0
                    bsc_ip_map[ip] += 1
                elif paras["APP"] == "NBAP":
                    if ip not in rnc_ip_map:
                        rnc_ip_map[ip] = 0
                    rnc_ip_map[ip] += 1
            else:
                pass
        return None

    # 搜索所有CFGMML zip文件, 返回BTS、NodeB列表
    @API_RECORD
    def inner_Parse_CFGMML_File(self, encoding="GBK"):
        bts_info_map = {}
        nodeb_info_map = {}
        filename_list = search_Files("*CFGMML*", "zip/ZIP")
        if len(filename_list) == 0:
            self.print_msg("Error: Not found any CFGMML file")
        for filename in filename_list:
            cmd_lines = load_TXT_File(filename, encoding)
            self.inner_Parse_CFGMML_File_aux(filename, cmd_lines, bts_info_map, nodeb_info_map)

        dump_Object("ALL_BTS_CFGMML_INFO", bts_info_map)
        dump_Object("ALL_NODEB_CFGMML_INFO", nodeb_info_map)
        return bts_info_map, nodeb_info_map

    #
    @API_RECORD
    def inner_GBTS_Covert_MML_deactive_unbind_delete(self, cmd_lines, btsinfo):
        if "CHILD_BTSID_LIST" in btsinfo and len(btsinfo["CHILD_BTSID_LIST"]) > 0:
            cmd_lines.append("//!!!Please Move Child BTS to other port first: %r." % btsinfo["CHILD_BTSID_LIST"])
            for (idx, name) in btsinfo["CHILD_BTSID_LIST"]:
                cmd_lines.append('DEA BTS: IDTYPE=BYNAME, BTSNAME="%s";' % name)
                cmd_lines.append('MOD BTSCONNECT: IDTYPE=BYNAME, BTSNAME="%s", ;' % name)
            cmd_lines.append("")
        if "PARENT_BTSID" in btsinfo:
            cmd_lines.append("//Parent BTS for reference: %r." % btsinfo["PARENT_BTSID"])
            cmd_lines.append("")

        cmd_lines.append('LST BTS: LSTTYPE=BYBTSNAME, BTSNAME="%s";\n' % btsinfo["BTSNAME"])
        cmd_lines.append("SET DATACONVERTSWITCH: TYPE=BTS_SINGLEOM_UPGRADE, SWITCH=ON;")

        # 去激活BTS
        cmd_lines.append("//Remove BTS")
        cmd_lines.append('DEA BTS: IDTYPE=BYNAME, BTSNAME="%s";' % btsinfo["BTSNAME"])
        cmd_lines.append("")

        # 修改三个eGBTS不支持的参数
        for cellid in btsinfo["CELLID_LIST"]:
            cmd_lines.append('SET GCELLSOFT: IDTYPE=BYID, CELLID=%s, RPTDLVQIALLOWED=DISABLE;' % cellid)
            cmd_lines.append('SET GCELLBASICPARA: IDTYPE=BYID, CELLID=%s, ICBALLOW=NO;' % cellid)
            cmd_lines.append('SET GCELLGPRS: IDTYPE=BYID, CELLID=%s, GPRS=SupportAsInnPcu, EGPRS2A=NO;' % cellid)
        cmd_lines.append("")

        # 解绑定TRX
        for trxid in btsinfo["TRXID_LIST"]:
            if trxid not in btsinfo["BIND_TRXID_LIST"]:
                cmd_lines.append("//TRXID=%s not bind to any RxU board. Skip it." % trxid)
            else:
                cmd_lines.append("RMV TRXBIND2PHYBRD: IDTYPE=BYID, TRXID=%s;" % trxid)
        cmd_lines.append("")

        # 解绑定小区
        for cellid in btsinfo["CELLID_LIST"]:
            cmd_lines.append("RMV CELLBIND2BTS: IDTYPE=BYID, CELLID=%s;" % cellid)
        cmd_lines.append("")

        # 删除传输对象
        self.inner_GBTS_Convert_MML_delete_tx(cmd_lines, btsinfo)

        # 删除基站
        cmd_lines.append("RMV BTS: IDTYPE=BYID, BTSID=%s;" % btsinfo["BTSID"])
        cmd_lines.append("\n")
        return cmd_lines

    @API_RECORD
    def inner_GBTS_Convert_MML_delete_tx(self, cmd_lines, btsinfo):
        # 删除IPMUX
        ipmuxidx_list = self.get_MML_Para_List(btsinfo, "ADD IPMUX", "IPMUXINDEX")
        for idx in ipmuxidx_list:
            cmd_lines.append("RMV IPMUX: IPMUXINDEX=%s;" % idx)

        # 删除IPPOOLMUX
        ippoolidx_list = self.get_MML_Para_List(btsinfo, "ADD IPPOOLMUX", "IPPOOLMUXINDEX")
        for idx in ippoolidx_list:
            cmd_lines.append("RMV IPPOOLMUX: IPPOOLMUXINDEX=%s;" % idx)

        # 删除IPPM
        ani_pathid_list = self.get_MML_Para_List(btsinfo, "ACT IPPM", ["ANI", "PATHID"])
        for (ani, pathid) in ani_pathid_list:
            cmd_lines.append("DEA IPPM: ANI=%s, PATHID=%s;" % (ani, pathid))

        # 删除IPPATH
        ani_pathid_list = self.get_MML_Para_List(btsinfo, "ADD IPPATH", ["ANI", "PATHID"])
        for (ani, pathid) in ani_pathid_list:
            cmd_lines.append("RMV IPPATH: ANI=%s, PATHID=%s;" % (ani, pathid))

        # 删除ADJAMP
        if "ADD ADJMAP" in btsinfo["MML_MAP"]:
            cmd_lines.append("RMV ADJMAP: ANI=%s, ITFT=ABIS,FORCEEXECUTE=YES;" % btsinfo["ANI"])

        # 删除ANI
        if "ADD ADJNODE" in btsinfo["MML_MAP"]:
            cmd_lines.append("RMV ADJNODE: ANI=%s,FORCEEXECUTE=YES;" % btsinfo["ANI"])
        pass

    @API_RECORD
    def inner_ip_reconstruction(self, cmd_lines, btsinfo):
        ani = int(btsinfo["ANI"])
        bts_id = int(btsinfo["BTSID"])
        bts_name = btsinfo["BTSNAME"]
        cmd_lines.append('ADD ADJNODE: ANI=%d, NAME="%s", NODET=ABIS, BTSID=%d;' % (ani, bts_name, bts_id))
        cmd_lines.append("")
        cmd_lines.append('ADD IPPATH: ANI=%d, PATHID=1, ITFT=ABIS, ISEGBTS=Yes, PATHT=QoS, IPADDR="%s", PEERIPADDR="%s", TXBW=3000000, RXBW=3000000, '
                         'CARRYFLAG=NULL, VLANFLAG=DISABLE, PATHCHK=DISABLED, ABISLNKBKFLAG=OFF, REMARK="Abis";' % (ani, btsinfo["BSC_IP"], btsinfo["GSM_IP"]))
        cmd_lines.append("")
        cmd_lines.append("ACT IPPM: ANI=%d, PATHID=1, ISQOSPATH=YES, PHB=BE-1&AF31-1&AF41-1&EF-1, LOSTPKTDETECTSW=OFF;" % (ani))
        cmd_lines.append("")
        cmd_lines.append("ADD ADJMAP: ANI=%d, TMIGLD=10, FTI=2, ITFT=ABIS;" % ani)
        pass

    @API_RECORD
    def inner_GBTS_Convert_MML_add_egbts(self, cmd_lines, btsinfo):
        btsid = btsinfo["BTSID"]
        if "NEW_BTSNAME" not in btsinfo:
            btsinfo["NEW_BTSNAME"] = btsinfo["BTSNAME"]
        cmd_lines.append(
            'ADD BTS: BTSID=%s, BTSNAME="%s", BTSTYPE=EGBTS, INNBBULICSHAEN=NO;' % (btsid, btsinfo["NEW_BTSNAME"]))

        # 基站传输模式
        cmd_lines.extend(btsinfo["MML_MAP"]["SET BTSTRANS"])
        cmd_lines.append("")

        for (sctpid, dscp, bts_sctpno, bts_port) in btsinfo["SCTPLNK_INFO"]:
            if btsinfo["BSC_TYPE"] == "BSC6910":
                cmd_lines.append(
                    'ADD SCTPLNK: SCTPLNKID=%d, APP=ABISCP, MODE=SERVER, DSCP=%d, SpecifyLOCPNFlag=NO, LOCIP1="%s", '
                    'PEERIP1="%s", PEERPN=%d, LOGPORTFLAG=NO, SWITCHBACKFLAG=YES;' %
                    (sctpid, dscp, btsinfo["BSC_IP"], btsinfo["GSM_IP"], bts_port))
            else:
                cmd_lines.append(
                    'ADD SCTPLNK: APP=ABISCP, SCTPLNKID=%d, MODE=SERVER, DSCP=%d, SpecifyLOCPNFlag=NO, LOCIP1="%s", '
                    'PEERIP1="%s", PEERPN=%d, LOGPORTFLAG=NO, VLANFLAG1=DISABLE, VLANFLAG2=DISABLE, SWITCHBACKFLAG=YES;' %
                    (sctpid, dscp, btsinfo["BSC_IP"], btsinfo["GSM_IP"], bts_port))
        cmd_lines.append("")

        for (sctpid, dscp, bts_sctpno, bts_port) in btsinfo["SCTPLNK_INFO"]:
            cmd_lines.append('ADD ABISCP: IDTYPE=BYID, BTSID=%s, SCTPLNKID=%d;' % (btsid, sctpid))
        cmd_lines.append("")

        if "ADD ADJNODE" in btsinfo["MML_MAP"]:
            mml = btsinfo["MML_MAP"]["ADD ADJNODE"][0].replace(btsinfo["BTSNAME"], btsinfo["NEW_BTSNAME"])
            cmd_lines.append(mml)

        if "ADD ADJMAP" in btsinfo["MML_MAP"]:
            cmd_lines.append(btsinfo["MML_MAP"]["ADD ADJMAP"][0])
        else:
            pass
            # if btsinfo["BSC_TYPE"] == "BSC6900":
            #     cmd_lines.append('ADD ADJNODE: ANI=%s, NAME="%s", NODET=ABIS, IDTYPE=BYNAME, BTSNAME="%s";\n' % (ani, btsname, btsname))
            #     if len(tmigld) > 0:
            #     ani=btsinfo["MML_MAP"]["ADD ADJNODE"][0].split(",")[0].split("=")[1]
            #     cmd_lines.append('ADD ADJMAP: ANI=%s, ITFT=ABIS, CNMNGMODE=SHARE, TMIGLD=%s, FTI=%s;\n' % (ani, 10, 0))
            # else:
            #     cmd_lines.append('ADD ADJNODE: ANI=%s, NAME="%s", NODET=ABIS, IDTYPE=BYNAME, BTSNAME="%s", IPPOOLINDEX=%s, CNMNGMODE=SHARE, TxBw=%s, RxBw=%s, PINGSWITCH=ENABLE;\n' %
            #                      (ani, btsname, btsname, ippoolindex, abis_bandwidth, abis_bandwidth))
            #     if len(tmigld) > 0:
            #         cmd_lines.append('ADD ADJMAP: ANI=%s, ITFT=ABIS, TMIGLD=%s, FTI=%s;\n' % (ani, tmigld, fti))
            pass

        if "ADD IPPATH" in btsinfo["MML_MAP"]:
            for line in btsinfo["MML_MAP"]["ADD IPPATH"]:
                t_str = 'ISEGBTS=Yes, IPADDR="%s", PEERIPADDR="%s"' % (btsinfo["BSC_IP"], btsinfo["GSM_IP"])
                line = line.replace('ISEGBTS=No', t_str)
                line = line.replace('CNMNGMODE=SHARE,', "")
                cmd_lines.append(line)
            cmd_lines.append("")

        for cmd in ["ADD IPMUX", "ADD IPPOOLMUX", "ACT IPPM", "ACT IPPOOLPM"]:
            if cmd in btsinfo["MML_MAP"]:
                cmd_lines.extend(btsinfo["MML_MAP"][cmd])
                cmd_lines.append("")

        # OM_IP和OM_MASK
        om_ip = btsinfo["OM_IP"]
        om_ip2 = btsinfo["OM_IP2"] if "OM_IP2" in btsinfo else "0.0.0.0"
        cmd_lines.append(
            'ADD BTSOAMIP: IDTYPE=BYID, BTSID=%s, OAMIP="%s", BACKUPOAMIP="%s";\n' % (btsid, om_ip, om_ip2))
        return cmd_lines

    @API_RECORD
    def inner_GBTS_Convert_MML_bind(self, cmd_lines, btsinfo):
        # 修改小区名称
        for cellid in btsinfo["CELLID_LIST"]:
            info = btsinfo["CELL_INFO"][cellid]
            if "NEW_CELLNAME" in info and info["NEW_CELLNAME"] != info["CELLNAME"]:
                cmd_lines.append(
                    'MOD GCELL: IDTYPE=BYID, CELLID=%s, NEWCELLNAME="%s";' % (cellid, info["NEW_CELLNAME"]))
        cmd_lines.append("")

        # 绑定小区
        for cellid in btsinfo["CELLID_LIST"]:
            cmd_lines.append('ADD CELLBIND2BTS: IDTYPE=BYID, CELLID=%s, BTSID=%s;' % (cellid, btsinfo["BTSID"]))
        cmd_lines.append("")

        # 修改本地小区
        for cellid in btsinfo["CELLID_LIST"]:
            info = btsinfo["CELL_INFO"][cellid]
            cmd_lines.append('MOD GCELL: IDTYPE=BYID, CELLID=%s, GLOCELLID=%s;' % (cellid, info["GLOCELLID"]))
        cmd_lines.append("")

        # 绑定TRX
        unbind_trxid_list = []
        for trxid in btsinfo["TRXID_LIST"]:
            info = btsinfo["TRX_INFO"][trxid]
            if trxid in btsinfo["BIND_TRXID_LIST"]:
                gtrxgroupid = info["GTRXGROUPID"]
                cmd_lines.append("MOD GTRX: IDTYPE=BYID, TRXID=%s, GTRXGROUPID=%s;" % (trxid, gtrxgroupid))
            else:
                unbind_trxid_list.append(trxid)
        cmd_lines.append("")

        # 删除未绑定的TRX
        if len(unbind_trxid_list) > 0:
            cmd_lines.append("//Below TRX was not bind to any RxU board before. delete.")
            for trxid in unbind_trxid_list:
                cmd_lines.append("RMV GTRX: IDTYPE=BYID, TRXID=%s;" % trxid)
            cmd_lines.append("")
        return cmd_lines

    @API_RECORD
    def innner_GBTS_Convert_MML_set_cell_trx_parameter(self, cmd_lines, btsinfo):
        c, paras = self.split_mml(btsinfo["MML_MAP"]["SET BTSOTHPARA"][0])
        cmd_lines.append('SET BTSOTHPARA: IDTYPE=BYID, BTSID=%s, PDCHGBR=%s;' % (btsinfo["BTSID"], paras["PDCHGBR"]))

        cell_para_list = self.get_MML_Para_List(btsinfo, "SET GCELLBASICPARA", ["CELLID", "IMMASSCBB"])
        for (cellid, cbb) in cell_para_list:
            cmd_lines.append('SET GCELLBASICPARA: IDTYPE=BYID, CELLID=%s, IMMASSCBB=%s;' % (cellid, cbb))

        cmd_lines.extend(btsinfo["MML_MAP"]["SET GCELLCCAMR"])
        cmd_lines.extend(btsinfo["MML_MAP"]["SET GCELLCCBASIC"])

        cell_para_list = self.get_MML_Para_List(btsinfo, "SET GCELLPSBASE", ["CELLID", "T3168", "T3192", "BSCVMAX"])
        for (cellid, t3168, t3192, vmax) in cell_para_list:
            cmd_lines.append('SET GCELLPSBASE: IDTYPE=BYID, CELLID=%s, T3168=%s, T3192=%s, BSCVMAX=%s;' % (
            cellid, t3168, t3192, vmax))

        cell_para_list = self.get_MML_Para_List(btsinfo, "SET GCELLBTSSOFTPARA",
                                               ["BTSID", "CELLID", "PAGINGOVERRPTTHRD"])
        for (btsid, cellid, thd) in cell_para_list:
            cmd_lines.append(
                'SET GCELLBTSSOFTPARA: IDTYPE=BYID, BTSID=%s, CELLID=%s, PAGINGOVERRPTTHRD=%s;' % (btsid, cellid, thd))

        cell_para_list = self.get_MML_Para_List(btsinfo, "SET GCELLOTHPARA",
                                               ["CELLID", "SDCONGESTBTSFLOWCTRLSW", "AMRULCMRSENDMODE", "RPTRLTSW"])
        for (cellid, sdlsw, mode, sw) in cell_para_list:
            cmd_lines.append(
                'SET GCELLOTHPARA:CELLID=%s, IDTYPE=BYID, SDCONGESTBTSFLOWCTRLSW=%s, AMRULCMRSENDMODE=%s, RPTRLTSW=%s;' % (
                    cellid, sdlsw, mode, sw))

        for trxid in btsinfo["TRXID_LIST"]:
            paras = btsinfo["TRX_INFO"][trxid]
            power = 1000 * float(paras["POWT"][:-1].replace("_", "."))
            paras["EGBTSPOWT"] = str(int(math.log10(power) * 100))  # 换算成dbm

            if "OUTHOPWROVERLOADTHRESHOLD" in paras and paras["OUTHOPWROVERLOADTHRESHOLD"] != "0":
                paras["A1"] = str(int(math.log10(int(paras["OUTHOPWROVERLOADTHRESHOLD"]) * 1000) * 100 + 0.5))  # 换算成dbm
            else:
                paras["A1"] = "0"

            if "INHOPWROVERLOADTHRESHOLD" in paras and paras["INHOPWROVERLOADTHRESHOLD"] != "0":
                paras["B1"] = str(int(math.log10(int(paras["INHOPWROVERLOADTHRESHOLD"]) * 1000) * 100 + 0.5))  # 换算成dbm
            else:
                paras["B1"] = "0"

            if "TSPWRRESERVE" in paras and paras["TSPWRRESERVE"] != "0":
                paras["C1"] = str(int(math.log10(int(paras["TSPWRRESERVE"]) * 1000) * 100 + 0.5))  # 换算成dbm
            else:
                paras["C1"] = "0"

            new_mml = 'SET GTRXDEV:IDTYPE=BYID, TRXID={TRXID}, EGBTSPOWT={EGBTSPOWT}, POWTUNIT=0_1DBM, PAOPTILEVEL={PAOPTILEVEL}, ' \
                      'TSPWRRESERVE1={C1}, OUTHOPWROVERLOADTHRESHOLD1={A1}, INHOPWROVERLOADTHRESHOLD1={B1};'.format(
                **paras)
            cmd_lines.append(new_mml)
            pass

        if "SET BTSRSV" in btsinfo["MML_MAP"]:
            cmd_lines.extend(btsinfo["MML_MAP"]["SET BTSRSV"])
        pass

    # 搜索回滚时bts_name这个基站的所有相关的MML命令
    @API_RECORD
    def inner_GBTS_Convert_MML_rollback(self, btsinfo, ip_reconstruction):
        btsid = btsinfo["BTSID"]
        cmd_lines = []

        cmd_lines.append("//BSC Name: %s" % btsinfo["BSC_NAME"])
        cmd_lines.append('LST BTS: LSTTYPE=BYBTSNAME, BTSNAME="%s";\n' % btsinfo["NEW_BTSNAME"])

        cmd_lines.append("SET DATACONVERTSWITCH: TYPE=BTS_SINGLEOM_ROLLBACK, SWITCH=ON;")
        # 去激活BTS
        cmd_lines.append("//Remove BTS")
        cmd_lines.append('DEA BTS: IDTYPE=BYNAME, BTSNAME="%s";' % btsinfo["NEW_BTSNAME"])

        # 解绑定小区
        for cellid in btsinfo["CELLID_LIST"]:
            cmd_lines.append("RMV CELLBIND2BTS: IDTYPE=BYID, CELLID=%s;" % cellid)
        cmd_lines.append("")

        # 删除传输对象
        self.inner_GBTS_Convert_MML_delete_tx(cmd_lines, btsinfo)

        # 删除ABISCP
        for (sctpid, bsc_sctplnk_dscp, bts_sctpno, bts_port) in btsinfo["SCTPLNK_INFO"]:
            cmd_lines.append('RMV ABISCP: IDTYPE=BYID, BTSID=%s, SCTPLNKID=%s;' % (btsid, sctpid))

        # 删除SCTPLNK
        for (sctpid, bsc_sctplnk_dscp, bts_sctpno, bts_port) in btsinfo["SCTPLNK_INFO"]:
            cmd_lines.append("RMV SCTPLNK: SCTPLNKID=%s;" % (sctpid))

        if ip_reconstruction == True:
            ani = int(btsinfo["ANI"])
            cmd_lines.append("RMV ADJNODE: ANI=%d;" % ani)
            cmd_lines.append("RMV IPPATH: ANI=%d, PATHID=1;" % ani)
            cmd_lines.append("DEA IPPM: ANI=%d, PATHID=1;" % ani)
            cmd_lines.append("")

        # 删除基站
        cmd_lines.append("RMV BTS: IDTYPE=BYID, BTSID=%s;\n" % btsinfo["BTSID"])

        cell_id_list = btsinfo["CELLID_LIST"]
        trx_id_list = btsinfo["TRXID_LIST"]
        for l in btsinfo["ALL_MML_LIST"]:
            c = self.get_command_from_cmd_line(l)
            if c is None: continue
            if c in ["ACT BTS", "SET BTSMNTMODE", "SET BTSDSCPMAP"]: continue  # skip these commands

            if c[4:7] == "BTS" or (
                        c in ["ADD CELLBIND2BTS", "ADD TRXBIND2PHYBRD", "ADD ADJNODE", "ADD ADJMAP", "ADD IPPATH",
                              "ADD IPPOOLMUX",
                              "ADD IPMUX",
                              "ACT IPPM", "ACT IPPOOLPM", "SET BSCABISPRIMAP", "SET GDSSPARA", "SET GCELLCCBASIC",
                              "SET GCELLBTSSOFTPARA", "SET BTSCELLPATCHPARA", "SET GCELLNONSTANDARDBW",
                              "SET GCELLCHMGAD", "SET GCELLCHMGBASIC", "SET GCELLGSMR", "SET GCELLBASICPARA",
                              "SET GCELLCCAMR",
                              "SET GCELLOTHBASIC",
                              "SET GCELLOTHEXT", "SET GCELLCCCH", "SET GCELLPSBASE", "SET GCELLSOFT",
                              "SET GCELLUNDPARA",
                              "SET GCELLOTHPARA",
                              "SET GCELLTRANPARA", "SET GTRXDEV"]):  # 回退的命令，BTS命令+上面这些命令
                c, paras = self.split_mml(l)
                if paras is None: continue

                if "BTSID" in paras:
                    if paras["BTSID"] == btsid:
                        cmd_lines.append(l)
                elif "CELLID" in paras:
                    if paras["CELLID"] in cell_id_list:
                        cmd_lines.append(l)
                elif "ANI" in paras:
                    if paras["ANI"] == btsinfo["ANI"]:
                        cmd_lines.append(l)
                elif "TRXID" in paras:
                    if paras["TRXID"] in trx_id_list:
                        cmd_lines.append(l)
                pass
            else:
                pass
        cmd_lines.append("\n")

        for cellid in btsinfo["CELLID_LIST"]:
            cmd_lines.append("MOD GCELL: IDTYPE=BYID, CELLID=%s, GLOCELLID=4294967295;" % cellid)
        cmd_lines.append("")

        for trxid in btsinfo["TRXID_LIST"]:
            cmd_lines.append("MOD GTRX: IDTYPE=BYID, TRXID=%s, GTRXGROUPID=4294967295;" % trxid)
        cmd_lines.append("")

        cmd_lines.append("SET DATACONVERTSWITCH: TYPE=BTS_SINGLEOM_ROLLBACK, SWITCH=OFF;")
        cmd_lines.append("//activate BTS")
        cmd_lines.append("ACT BTS: IDTYPE=BYID, BTSID=%s, TRXIDTYPE=BYID;\n\n" % btsinfo["BTSID"])
        return cmd_lines

    @API_RECORD
    def get_Band_GtrxGroupID_Map(self,bts_info):
        if "TRX_INFO" not in bts_info: return None
        result_dict = {}
        for x in bts_info["TRX_INFO"].values():
            if x["BAND"] not in result_dict:
                result_dict[x["BAND"]] = []
            elif int(x["GTRXGROUPID"]) not in result_dict[x["BAND"]]:
                result_dict[x["BAND"]].append(int(x["GTRXGROUPID"]))
            else:
                pass
        return result_dict

    @API_RECORD
    def create_BFANT(self,subrack_no,band,tilt):
        band = int(band)
        deviceno=self.get_free_id_list("BfAnt", 'DEVICENO').pop(0)
        bfant_obj = MODEL.BfAnt(DEVICENO=deviceno, MANUFACTORY="OtherManufacturer1", CrsSplitBeamIndicator=255,
                                VERTICALBEAMWIDTH=60, CONNCN=0, CONNSRN=subrack_no, CONNSN=0, TILT=tilt,MODELNO="MassiveAntenna",
                                BEAMWIDTH=30, Band=band, TYPE="INTELLIGENT", BFANTBEARING=0,CoverageScenario="SCENARIO_2")
        COMMIT_DATA('BfAnt', [bfant_obj], APPEND_MODE, with_child=True)

    @API_RECORD
    def modify_ProductType(self, product_type, old_ne_name= None):
        if old_ne_name == None:
            old_ne_name = self.NEName
        ne_tree = self.get_all_moc_from_ref(old_ne_name)
        ne_tree["SUBRACK"] = self.get_moc_list_by_mod(ne_tree["SUBRACK"],
                                                      MOD(TYPE=MODEL.SUBRACK.TYPE.fromString("BBU" + product_type[3:7])).WHERE(
                                             lambda o: "BBU" in MODEL.SUBRACK.TYPE.toString(o.TYPE)))
        self.convert_product_type(ne_tree, product_type)
        self.NEVERSION = self.get_moc("NE")[0].PRODUCTVERSION

    @API_RECORD
    def trans_convert(self, opt_switch=3, doc=None):
        '''
        Indicates the opt_switch
        1: Only the transmission configuration model is optimized (excluding the cabinet number, subrack number, and slot number).
        2: Only VLAN optimization is required. (The prerequisite is that the new transmission model has been used.)
        3: The transmission configuration model is optimized (excluding the cabinet number, subrack number, and slot number) and VLAN optimization is required.
        4: The transmission configuration model is optimized (excluding the cabinet number, subrack number, and slot number), VLAN optimization is required, and IPv4 IPsec policy group binding related reconstruction is required.
        5: VLAN optimization is required, and IPv4 IPsec policy group binding related reconstruction is required. (The prerequisite is that the new transmission model has been used. The scenario is the same as that in mode 4.)
        '''
        return TRANS_OPTIMIZE(opt_switch, doc)

    @API_RECORD
    def ne_site_type_convert(self,ne_tree, product_type_new, para_list=[]):
        def get_local_debug_parameter():
            '''
            三合一场景在线及离线调测参数构造函数
            '''
            para_list = []
            para_list.append(True)  # 三合一场景设置为True, 一般场景为False
            try:
                para_list.append(MidLibPath)  # 三合一场景本地调测所需参数
                para_list.append(ToolPath)  # 三合一场景本地调测所需参数
            except:
                pass
            return para_list
        if para_list == []:
            para_list = get_local_debug_parameter()
        is_success, ne_tree = NE_SITETYPE_CONVERT(ne_tree, product_type_new, para_list)
        return is_success, ne_tree

    @API_RECORD
    def get_dict_from_excel_file(self, excel_filename, sheet_name, title_row, group_title, target_title_list, **kwargs):
        """读取Excel文件，返回一个字典"""
        para_setting_map = load_Excel_File(excel_filename, sheet_name, title_row=title_row, group_title=group_title, **kwargs)
        rf_para_setting_dict = {}
        for (mo, row_list) in para_setting_map.items():
            rf_para_setting_dict[mo] = []
            for excel_row in row_list:
                tmp_list = []
                for target_title in target_title_list:
                    tmp_list.append(excel_row[target_title])
                rf_para_setting_dict[mo].append(tmp_list)
        return rf_para_setting_dict

    @API_RECORD
    def modify_LTE_RF_Para(self, result_row, rf_para_setting_dict, report_value_invalid=True):
        if "Result" not in result_row:
            result_row["Result"] = "Success"
        locellid = int(result_row["LocalCellId"])
        cell_obj_list = self.get_moc("Cell", WHERE(LocalCellId=locellid))
        if len(cell_obj_list) == 0:
            result_row["Detail"] = "Error: LocalCellId=%s is not exist" % (locellid)
            result_row["Result"] = "Fail"
            return False

        result_row["CellName"] = cell_obj_list[0].CellName
        result_row["Detail"] = ""

        for (MO, para_list) in rf_para_setting_dict.items():
            mo_class = CVT_CLASS(MO)  # 获得mo对应的类
            if mo_class is None:
                msg = "Error: MO=%s is not exist. Please check\n" % (MO)
                result_row["Detail"] += msg
                print(msg)
                result_row["Result"] = "Fail"
                continue
            mo = CVT_CLASS_NAME(MO)  # 转为标准名称
            big_para_name_list = [s.upper() for s in copy.deepcopy(mo_class._field_names_)]
            for (parameter, target_value, default_value, key_para_name) in para_list:
                key_para_dict = {}
                # 输出Excel的Title
                if key_para_name:
                    output_excel_title = "%s\n%s\n(%s)" % (MO, parameter, key_para_name)
                    if "=" not in key_para_name:
                        result_row[output_excel_title] += "KeyPara Invalid"
                        result_row["Result"] = "Partial Fail"
                        continue
                    else:
                        invalid_key_para = False
                        tmp_list = key_para_name.split(",")
                        for tmp_name in tmp_list:
                            key_para_name, key_para_value = tmp_name.split("=")
                            key_para_name = key_para_name.upper().strip()
                            if key_para_name not in big_para_name_list:
                                result_row[output_excel_title] = "KeyPara Invalid"
                                print("Error: MO=%s, KeyPara=%s is invalid" % (mo, key_para_name))
                                result_row["Result"] = "Partial Fail"
                                invalid_key_para = True
                                break
                            else:
                                key_para_name = mo_class._field_names_[big_para_name_list.index(key_para_name)]
                                key_para_value = int(key_para_value)  # !!! KeyPara只支持整数类型
                                key_para_dict[key_para_name] = key_para_value
                        if invalid_key_para is True:  # 存在参数错误
                            continue
                    pass
                else:
                    output_excel_title = "%s\n%s" % (MO, parameter)
                    pass
                # 获取满足条件的mo
                if hasattr(mo_class, "LocalCellId"): # 小区级别的参数
                    key_para_dict["LocalCellId"] = locellid
                mo_obj_list = self.get_moc(mo, WHERE(**key_para_dict))

                if len(mo_obj_list) == 0:
                    if key_para_name: # 如果输入了KeyPara，且原先不存在，则创建
                        obj = mo_class(**key_para_dict)
                        mo_obj_list = [obj]
                    else:
                        result_row["Detail"] += "Warning: LocalCellId=%s has no MO=%s data. Please check\n" % (locellid, mo)
                        result_row["Result"] = "Partial Fail"
                        continue

                if target_value is None:
                    target_value = default_value
                if ":" in parameter:  # 修改bit参数
                    para_name, switch_name = parameter.split(":")
                else:
                    para_name, switch_name = parameter, None
                para_name = para_name.upper().strip()
                if para_name not in big_para_name_list:
                    result_row[output_excel_title] = "Para Invalid"
                    print("Error: MO=%s, Para=%s is invalid" % (mo, para_name))
                    result_row["Result"] = "Partial Fail"
                    continue
                para_name = mo_class._field_names_[big_para_name_list.index(para_name)]
                para_class = getattr(mo_class, para_name)
                para_value = getattr(mo_obj_list[0], para_name)  # 得到当前参数的值

                if para_class.typeName == "BitDomain":  #Bit类型
                    if switch_name is None:
                        result_row[output_excel_title] = "Switch Invalid"
                        print("Error: MO=%s, Para=%s, Switch=None is invalid" % (mo, para_name))
                        result_row["Result"] = "Partial Fail"
                        continue
                    switch_name = switch_name.upper().strip()
                    big_switch_name_list = [s.upper() for s in copy.deepcopy(para_class._field_keys_)]
                    if switch_name not in big_switch_name_list:
                        result_row[output_excel_title] = "Switch Invalid"
                        print("Error: MO=%s, Para=%s, Switch=%s is invalid" % (mo, para_name, switch_name))
                        result_row["Result"] = "Partial Fail"
                        continue
                    switch_name = para_class._field_keys_[big_switch_name_list.index(switch_name)]
                    # 得到 当前开关的值
                    switch_bit = getattr(para_class, switch_name)
                    if para_value is None:
                        para_value = 0
                    elif type(para_value) is str:  # 把字符串
                        para_value = para_class.fromString(para_value)
                    switch_value = para_value & (1 << switch_bit)
                    switch_value = "OFF" if switch_value == 0 else "ON"
                    target_switch_value = target_value.upper().strip()
                    if switch_value == target_switch_value:
                        result_row[output_excel_title] = "%s" % (switch_value)
                        continue
                    else:
                        if target_switch_value not in ["ON", "OFF", "PERMIT", "NOT_PERMIT", "CFG", "NOT_CFG"]:
                            result_row[output_excel_title] = "Value Invalid(%s)" % (target_switch_value)
                            result_row["Result"] = "Partial Fail"
                            continue
                        result_row[output_excel_title] = "%s->%s" % (switch_value, target_switch_value)

                        if target_switch_value in ["ON", "PERMIT", "CFG"]:
                            new_para_value = para_value | (1 << switch_bit)
                        else:
                            new_para_value = para_value & (~(1 << switch_bit))
                    pass
                else:  # 非比特类型
                    if para_class.typeName == "Enum" and len(target_value) > 0:  # 枚举类型
                        para_value = para_class.toString(para_value)  # 把整数值转换为枚举类型
                        tmp_big_list = [s.upper() for s in para_class._field_names_]
                        if target_value.upper() not in tmp_big_list:  # 判断输入的是否是有效的值。对无效值报错
                            if report_value_invalid is True:
                                result_row[output_excel_title] = "Value Invalid(%s)" % (target_value)
                                result_row["Result"] = "Partial Fail"
                            else:
                                result_row[output_excel_title] = "skip"
                            continue
                        else:
                            target_value = para_class._field_names_[tmp_big_list.index(target_value.upper())]
                    elif para_class.typeName == "List":  # 如果是列表，不设置
                        if report_value_invalid is True:
                            result_row[output_excel_title] = "Para Type Invalid(List)"
                            result_row["Result"] = "Partial Fail"
                        else:
                            result_row[output_excel_title] = "skip"
                        continue
                    elif para_class.typeName == "IpV4":  # IPV4类型，不设置
                        para_value = para_class.toString(para_value)
                    elif para_class.typeName in ["UnsignedLong", "Long"]:
                        try:
                            target_value = int(target_value)
                        except:
                            result_row[output_excel_title] = "Value Invalid(%s)" % (target_value)
                            result_row["Result"] = "Partial Fail"
                            continue
                        target_value = int(target_value)
                    elif para_class.typeName in ["String", "DateTime", "Time"]:
                        pass
                    else:
                        if report_value_invalid is True:
                            result_row[output_excel_title] = "Para Type Invalid(%s)" % (para_class.typeName)
                            result_row["Result"] = "Partial Fail"
                        else:
                            result_row[output_excel_title] = "skip"
                        continue

                    if para_value == target_value:
                        result_row[output_excel_title] = "%s" % para_value
                        continue
                    else:
                        result_row[output_excel_title] = "%s->%s" % (para_value, target_value)
                        new_para_value = target_value
                    pass
                # 修改值
                mo_obj_list = UPDATE_DATA(mo_obj_list, MOD(lambda o: setattr(o, para_name, new_para_value)))
                mo_obj_list = CVT_OBJ(mo, mo_obj_list)
                self.save_moc(mo, mo_obj_list, APPEND_MODE, with_merge=True)
                pass
            pass
        pass

    @API_RECORD
    def set_PnpInfo(self,version=None ,connectiontype="Common",opscenario=14,authtype="AnonymousAuthentication"):
        # PnP Information
        if self.NEVERSION:
            version = self.NEVERSION
        pnp_obj = MODEL.PnPINFO(NENAME=self.NEName, SoftwareVersion=version, SubNetwork=None, SubArea=None, ESN=None,
                                ConnectionType=connectiontype,  # Common, SSL
                                OpScenario=opscenario,  # 0: New Build, 1: Expand RAT, 14: Change BTS Type,
                                AuthType=authtype)  # AnonymousAuthentication, OSSAuthenticatesNE
        self.save_moc("PnPINFO", [pnp_obj], OVERWRITE_MODE)

    @API_RECORD
    def get_RRU_Band_Sector(self, srn, rru_subrack_plan_map):
        for band_str in rru_subrack_plan_map:
            for (sector_str, id_list) in rru_subrack_plan_map[band_str].items():
                if str(srn) in id_list:
                    return band_str, sector_str
        self.print_msg( "Error: RRU Subrack=%r is not in the ID plan. Fail to get Band/Sector for it" % srn)
        return (None, None)

    @API_RECORD
    def get_RFU_Band_Sector(self, cn, srn, sn, rfu_subrack_plan_map):
        for band_str in rfu_subrack_plan_map:
            for (sector_str, id_list) in rfu_subrack_plan_map[band_str].items():
                if str(cn) + "-" + str(srn) + "-" + str(sn) in id_list:
                    return band_str, sector_str
        self.print_msg( "Error: RRU Subrack=%r is not in the ID plan. Fail to get Band/Sector for it" % srn)
        return (None, None)

    @API_RECORD
    def clear_Redundance_SectorEqm(self, ne_tree,bts_info=None):
        busy_sectoreqm_id_list = []
        if bts_info is not None and "GTRXGROUP" in ne_tree:
            band_gtrxgroupid_map = self.get_Band_GtrxGroupID_Map(bts_info)
            busy_gtrxgroup_id_list = []
            for (band_str, gtrxgroupid_list) in band_gtrxgroupid_map.items():
                busy_gtrxgroup_id_list.extend(gtrxgroupid_list)
            ne_tree["GTRXGROUP"] = self.get_moc_list_by_del(ne_tree["GTRXGROUP"], WHERE(lambda o: o.GTRXGROUPID not in busy_gtrxgroup_id_list))
            ne_tree["GTRXGROUPSECTOREQM"] = self.get_moc_list_by_del(ne_tree["GTRXGROUPSECTOREQM"],
                                                                     WHERE(lambda o: o.GTRXGROUPID not in busy_gtrxgroup_id_list))
            busy_glocell_id_list = [x.GLOCELLID for x in ne_tree["GTRXGROUP"]]
            delete_moc_list = ["GLOCELL","GLOCELLOTHPARA","GLOCELLALGPARA","GLOCELLRSVDPARA","GLOCELLRLALMPARA","GLOCELLENERGYMGTPARA"]
            for moc in delete_moc_list:
                ne_tree[moc] = self.get_moc_list_by_del(ne_tree[moc],
                                                        WHERE(lambda o: o.GLOCELLID not in busy_glocell_id_list))
            sectoreqm_id_list_2g = [x.SECTOREQMID for x in ne_tree["GTRXGROUPSECTOREQM"]]
            busy_sectoreqm_id_list.extend(sectoreqm_id_list_2g)

        if "ULOCELL" in ne_tree:
            sectoreqm_id_list_3g = [x.SECTOREQMID for x in ne_tree["ULOCELLSECTOREQM"]]
            busy_sectoreqm_id_list.extend(sectoreqm_id_list_3g)

        if "Cell" in ne_tree:
            sectoreqm_id_list_4g = [x.SectorEqmId for x in ne_tree["eUCellSectorEqm"]]
            busy_sectoreqm_id_list.extend(sectoreqm_id_list_4g)

        busy_sectoreqm_id_list = list(set(busy_sectoreqm_id_list))

        ne_tree["SECTOREQM"] = self.get_moc_list_by_del(ne_tree["SECTOREQM"],
                                                        WHERE(lambda o: o.SECTOREQMID not in busy_sectoreqm_id_list))
        pass

    @API_RECORD
    def get_Wsd_Data(self, filename=None, addition_rat="", offlineFlag=False):
        if filename is None:
            filename = self.NEName
        if offlineFlag is False:
            jsondata = load_WSD_File(ne_name=filename, with_raw=True)
        else:
            jsondata = load_Json_File(filename)
        # self.print_msg(vars(jsondata))
        for logicSiteInfo in jsondata["logicSiteList"]:
            self.print_msg(self.ratStr)
            self.print_msg(logicSiteInfo["workMode"])
            workmode = logicSiteInfo["workMode"].replace("O", "")
            if "L" in workmode:
                workmode = workmode.replace("T", "")
            else:
                workmode = workmode.replace("T", "L")
            if set(list(workmode)) != set(list(self.ratStr+addition_rat)): continue
            self.WSD_Info_Cache["logicSiteId"] = logicSiteInfo["logicSiteId"]
            self.WSD_Info_Cache["workMode"] = workmode
            self.WSD_Info_Cache["bbuType"] = logicSiteInfo["bbuBoard"]["bbuType"]
            self.WSD_Info_Cache["CN"] = logicSiteInfo["bbuBoard"]["CN-SRN"].split("-")[0]
            self.WSD_Info_Cache["SRN"] = logicSiteInfo["bbuBoard"]["CN-SRN"].split("-")[1]
            self.WSD_Info_Cache["bbpToCell"] = logicSiteInfo["bbpToCell"]
            self.WSD_Info_Cache["bbuBoard"] = logicSiteInfo["bbuBoard"]
            self.WSD_Info_Cache["rxu"] = logicSiteInfo["rxu"]
            self.WSD_Info_Cache["cellList"] = logicSiteInfo["cellList"]
            self.print_msg("NE=%s Get WSD Data and Save to Cache!" % self.NEName)
            break
        if set(list(workmode)) != set(list(self.ratStr+addition_rat)):
            self.exit_Info("NE=%s No Data in WSD Info " % self.NEName)
        self.print_msg(self.WSD_Info_Cache)
        pass

    @API_RECORD
    def get_Ep_Data(self,ne_name, ep_type="Design", with_raw=False):
        return LOAD_EP_FILE(ne_name, ep_type, with_raw)

    @API_RECORD
    def create_BBUBoard_By_WSD(self):
        if "bbuBoard" not in self.WSD_Info_Cache:
            self.exit_Info("NE=%s No bbuBoard in WSD cache, Please get it using get_Wsd_Data function first" % self.NEName)
        bbp_info = self.WSD_Info_Cache["bbuBoard"]
        cn, srn = bbp_info["CN-SRN"].split("-")
        cn, srn = int(cn), int(srn)
        for sn in [0, 1, 2, 3, 4, 5, 6, 7, 16, 18, 19]:
            slot_str = "slot%d" % sn
            if slot_str not in bbp_info: continue
            if bbp_info[slot_str] is None: continue
            bbp_str = bbp_info[slot_str]
            if bbp_str is None: continue
            if "_" in bbp_str:
                brd, rat = bbp_str.rsplit("_", 1)
            else:
                brd, rat = bbp_str, ""

            if brd[1:4] == "MPT":  # Create MPT Board  UMPT/LMPT/WMPT
                self.add_moc("MPT", CN=cn, SRN=srn, SN=sn, TYPE=brd[:4])
            elif brd[1:4] == "BBP":
                for r_str in rat:
                    if r_str in ["O"]: continue
                    self.Rat_BBP_Cache[r_str].append((brd[:4], int(cn), int(srn), int(sn)))
                self.create_One_BBP(cn, srn, sn, brd, rat)
            elif brd[:3] == "FAN":
                self.add_moc("BBUFAN", CN=cn, SRN=srn, SN=sn)
            elif brd[:4] == "UPEU":
                self.add_moc("PEU", CN=cn, SRN=srn, SN=sn)
            elif brd[:4] == "UEIU":
                self.add_moc("UEIU", CN=cn, SRN=srn, SN=sn)
            self.print_msg("Info: Create %s: %d-%d-%d, %s" % (brd, cn, srn, sn, rat))
        # 创建机柜
        subrack_type = bbp_info["bbuType"]
        self.add_moc("SUBRACK", CN=cn, SRN=srn, TYPE=MODEL.SUBRACK.TYPE.fromString(subrack_type), DESC="by WSD")
        return self.Rat_BBP_Cache

    @API_RECORD
    def create_RXUBoard_By_WSD(self, band_filter=None, workmode_filter=None):
        if "rxu" not in self.WSD_Info_Cache or len(self.WSD_Info_Cache["rxu"]) == 0:
            self.exit_Info("NE=%s No rxu in WSD cache, Please get it using get_Wsd_Data function first" % self.NEName)
        rxu_info_map = self.WSD_Info_Cache["rxu"]
        cell_List = self.WSD_Info_Cache["cellList"]
        hcn = int(self.WSD_Info_Cache["CN"])
        hsrn = int(self.WSD_Info_Cache["SRN"])
        # 读取并获得SECTOREQMID的规划表
        sectoreqmid_plan_map = self.ID_Plan_Cache["SECTOREQMID"]
        # 获得扇区ID
        sectorid_plan_map = self.ID_Plan_Cache["SECTORID"]
        rcn_plan_map = self.ID_Plan_Cache["RRUCHAINNO"]
        # 创建RXU
        rruObjList = []
        rfuObjList = []
        # 创建RRUCHAIN
        rruChainObjList = []
        rxuspecList = []
        assignStr_list = []
        for pos, rxu_info in rxu_info_map.items():
            work_mode = rxu_info["workMode"]
            work_mode_value = []
            # check which work mode, if single, check from list , if more than one, use API
            if work_mode in ["GO", "UO", "LO", "MO"]:
                work_mode_value.append(self.rat_map[work_mode])
            else:
                work_mode_value = self.get_RXU_WorkMode_List_From_String(work_mode)
            if band_filter is not None and band_filter != rxu_info["band"]: continue
            if workmode_filter is not None and workmode_filter != work_mode: continue
            rxu_type = rxu_info["type"]
            sectorNo_list = [int(x) for x in rxu_info["sector"].split("&")]
            sectorNo_list.sort()
            sectorNo = sectorNo_list.pop(0)
            Band_list = [int(x[:-1]) for x in rxu_info["band"].split("&")]
            # contacenate workmode_band_rxu and add to a list for all rrus
            if len(Band_list) == 1:
                for each_work_mode in work_mode_value:
                    workmode_band_rxu = each_work_mode + str(Band_list[0]) + "_" + rxu_info["rxuSpec"]
                    rxuspecList.append(workmode_band_rxu)
            else:
                for each_band in Band_list:
                    for each_work_mode in work_mode_value:
                        workmode_band_rxu = each_work_mode + str(each_band) + "_" + rxu_info["rxuSpec"]
                        rxuspecList.append(workmode_band_rxu)
            Band_list.sort()
            Band = Band_list.pop(0)
            hsn, hpn = [int(x) for x in rxu_info["cpri0"].split("-")]
            if str(Band) in rcn_plan_map:
                lst = rcn_plan_map[str(Band)]["SECTOR_%s" % chr(ord("A") + sectorNo - 1)]
                rcn = rcn_plan_map[str(Band)]["SECTOR_%s" % chr(ord("A") + sectorNo - 1)][0]
            else:
                tmp_band = "TDD" + str(Band) if "T" in rxu_info["workMode"] else "LTE" + str(Band)
                lst = rcn_plan_map[tmp_band]["SECTOR_%s" % chr(ord("A") + sectorNo - 1)]
                rcn = rcn_plan_map[tmp_band]["SECTOR_%s" % chr(ord("A") + sectorNo - 1)][0]
            if (len(lst) == 0):
                print("band %s setcor %d" % (str(Band), sectorNo))
            rruChainObj = MODEL.RRUCHAIN(RCN=rcn, HCN=hcn, HSRN=hsrn, HSN=hsn, HPN=hpn)
            if rxu_info["cpri1"] in [None, ""]:  # 一根光纤
                rruChainObj.TT = MODEL.RRUCHAIN.TT.CHAIN
                rruChainObj.BM = MODEL.RRUCHAIN.BM.COLD
                rruChainObj.AT = MODEL.RRUCHAIN.AT.LOCALPORT
            else:  # 两根光纤
                rruChainObj.TT = MODEL.RRUCHAIN.TT.LOADBALANCE
                tsn, tpn = [int(x) for x in rxu_info["cpri0"].split("-")]
                rruChainObj.TCN, rruChainObj.TSRN, rruChainObj.TSN, rruChainObj.TPN = hcn, hsrn, tsn, tpn
            rruChainObjList.append(rruChainObj)
            # 计算RRU工作制式的值
            work_mode_value = self.get_RXU_WorkMode_From_String(work_mode)
            cn, srn, sn = self.inner_get_cn_srn_sn_from_rxu_info(rxu_info)
            if rxu_type[1:4] in ["RRU", "IRU"]:
                rxuObj = MODEL.RRU(CN=cn, SRN=srn, SN=sn, RCN=rcn, PS=rxu_info["ps"], TXNUM=rxu_info["txNum"],
                                   RXNUM=rxu_info["rxNum"],
                                   RS=work_mode_value, RT=MODEL.RRU.RT.field(rxu_type),
                                   RUSPEC=rxu_info["rxuSpec"],
                                   TP=MODEL.RRU.TP.TRUNK,
                                   ADMSTATE=MODEL.RRU.ADMSTATE.UNBLOCKED)
                rruObjList.append(rxuObj)
            else:
                rxuObj = MODEL.RFU(CN=cn, SRN=srn, SN=sn, RCN=rcn, PS=rxu_info[u"ps"], TXNUM=rxu_info["txNum"],
                                   RXNUM=rxu_info["rxNum"],
                                   RS=work_mode_value, RT=MODEL.RFU.RT.field(rxu_type),
                                   RUSPEC=rxu_info["rxuSpec"],
                                   TP=MODEL.RFU.TP.TRUNK,
                                   ADMSTATE=MODEL.RFU.ADMSTATE.UNBLOCKED)
                rfuObjList.append(rxuObj)
            # 配置射频互连
            if "InterCon_RXU" in rxu_info and rxu_info["InterCon_RXU"] != "":
                cn, srn, sn = [int(x) for x in rxu_info["InterCon_RXU"].split("-")]
                rxuObj.RFCONNTYPE = MODEL.RRU.RFCONNTYPE.INTRA_SYS_INTERCONN
                rxuObj.RFCONNCN2 = cn
                rxuObj.RFCONNSRN2 = srn
                rxuObj.RFCONNSN2 = sn
            # RXU用于UMTS且频段为850/900时，设置RXU带宽为4.2M
            if "U" in work_mode:
                if "900" in rxu_info["band"]:
                    rxuObj.FMBWH = MODEL.RFU.FMBWH.field("4200")
                elif "850" in rxu_info["band"]:
                    rxuObj.FMBWH = MODEL.RFU.FMBWH.field("4200")
                else:
                    pass
        rxuspecList = set(rxuspecList)
        rxuspecList = list(rxuspecList)
        sectorEqmObjList = []
        complan_freqband = ''
        for cell_info in cell_List:
            if band_filter is not None and band_filter != cell_info['band']: continue
            if workmode_filter is not None and cell_info["cellMode"][0] not in workmode_filter: continue
            cell_mode = cell_info["cellMode"]
            sectorEqmNoStr = cell_info["physicalSector"]
            sectorEqmNoList = [int(x) for x in sectorEqmNoStr.split("&")]
            for i in sectorEqmNoList:
                sectorEqmStr = "sectorEqm%d" % (sectorEqmNoList.index(i) + 1)
                if sectorEqmStr not in cell_info: continue
                sectorEqmRxulist_Dict = cell_info[sectorEqmStr]
                for bandStr, sectorEqmRxu_list in sectorEqmRxulist_Dict.items():
                    sectorStr = "SECTOR_%s" % chr(ord("A") + i)
                    if cell_mode in ["GO", "UO", "LO", "MO", "TO", "NO"]:
                        bandStr_GO = cell_info["band"].split('&')
                        for band_go in bandStr_GO:
                            rat_go = self.rat_map[cell_info["cellMode"]] + band_go[:-1]
                            if band_go[:-1] in sectorid_plan_map:
                                sectorId = int(sectorid_plan_map[band_go[:-1]][sectorStr][0])
                            else:
                                tmp_band = "TDD" + band_go[:-1] if "T" in cell_info["cellMode"] else "LTE" + band_go[:-1]
                                sectorId = int(sectorid_plan_map[tmp_band][sectorStr][0])
                            cell_complete_field = rat_go  # + '_' + str(sectorId)
                            for excel_row in rxuspecList:
                                if cell_complete_field in excel_row:
                                    complan_freqband = excel_row
                            if complan_freqband not in self.Com_Plan_Cache["ASSIGN"]:
                                complan_freqband = rat_go
                            assignList = [chr(ord("A") + int(x[-1])) for x in sectorEqmRxu_list]
                            assignStr_list = self.get_AssignStr(complan_freqband, assignList)
                            for assignStr in assignStr_list:
                                sectorEmqId = int(sectoreqmid_plan_map[rat_go][sectorStr][assignStr_list.index(assignStr)])
                                rruList = list(set([x[:-2] for x in sectorEqmRxu_list]))
                                if len(sectorEqmRxulist_Dict) == 1:
                                    rruList = rruList
                                elif len(sectorEqmRxulist_Dict) == 2:
                                    temp_lst = []
                                    if rat_go[3:] + "M" in [[x for x in sectorEqmRxulist_Dict][1]][0].split("&"):
                                        temp = sectorEqmRxulist_Dict[[x for x in sectorEqmRxulist_Dict][1]][0][:-2]
                                    elif rat_go[3:] + "M" in [[x for x in sectorEqmRxulist_Dict][0]][0].split("&"):
                                        temp = sectorEqmRxulist_Dict[[x for x in sectorEqmRxulist_Dict][0]][0][:-2]
                                    temp_lst.append(temp)
                                    rruList = temp_lst

                                sectorEqmAntennaList = []
                                sectorEqmObj = self.inner_create_one_sectoreqm(sectorEmqId, sectorId, assignStr,rruList)
                                if "BEAM" in "".join(assignStr):
                                    sectorEqmObj.RRUCN = (rruList[0]).split("-")[0]
                                    sectorEqmObj.RRUSRN = (rruList[0]).split("-")[1]
                                    sectorEqmObj.RRUSN = (rruList[0]).split("-")[2]
                                    sectorEqmObj.BEAMSHAPE = "SEC_120DEG"
                                    sectorEqmObj.BEAMLAYERSPLIT = "None"
                                    sectorEqmObj.BEAMAZIMUTHOFFSET = MODEL.SECTOREQM.BEAMAZIMUTHOFFSET.NONE
                                    sectorEqmObjList.append(sectorEqmObj)
                                    self.save_moc("SECTOREQM", [sectorEqmObj], APPEND_MODE, with_merge=True,with_child=True)
                                    pass
                                else:
                                    if sectorEqmObj != None:
                                        sectorEqmObj.ANTCFGMODE = MODEL.SECTOREQM.ANTCFGMODE.ANTENNAPORT
                                        sectorEqmObjList.append(sectorEqmObj)
                                        self.save_moc("SECTOREQM", [sectorEqmObj], APPEND_MODE, with_merge=True,
                                                      with_child=True)
                        pass
                    else:
                        bandStr = bandStr[:-1]
                        convert_rat = self.rat_map[cell_info["cellMode"]]
                        ratBandStr = "".join([convert_rat, bandStr])
                        sectorStr = "SECTOR_%s" % chr(ord("A") + i)
                        sectorEmqId = int(sectoreqmid_plan_map[ratBandStr][sectorStr][sectorEqmNoList.index(i)])
                        sectorId = int(sectorid_plan_map[bandStr][sectorStr][0])
                        assignList = [chr(ord("A") + int(x[-1])) for x in sectorEqmRxu_list]
                        assignStr = self.get_AssignStr(ratBandStr, assignList)
                        rruList = list(set([x[:-2] for x in sectorEqmRxu_list]))
                        sectorEqmAntennaList = []
                        for sectorEqmRxuItem in sectorEqmRxu_list:
                            rxuCN, rxuSRN, rxuSN, rxuANTN = [int(x) for x in sectorEqmRxuItem.split("-")]
                            sectorEqmAntennaObj = MODEL.SECTOREQM.SECTOREQMANTENNA(CN=rxuCN, SRN=rxuSRN, SN=rxuSN,
                                                                                   ANTN=rxuANTN)
                            sectorEqmAntennaObj.ANTTYPE = self.get_AntennaType(assignStr, rxuANTN,
                                                                               rruList.index(sectorEqmRxuItem[:-2]))
                            sectorEqmAntennaObj.TXBKPMODE = "MASTER"
                            sectorEqmAntennaList.append(sectorEqmAntennaObj)
                        sectorEqmObj = MODEL.SECTOREQM(SECTOREQMID=sectorEmqId, SECTORID=sectorId,
                                                       SECTOREQMANTENNA=sectorEqmAntennaList)
                        if "BEAM" in "".join(sectorEqmRxu_list):
                            sectorEqmObj.RRUCN = "1"
                            sectorEqmObj.RRUSRN = "1"
                            sectorEqmObj.RRUSN = "1"
                            sectorEqmObj.BEAMSHAPE = "SEC_120DEG"
                            sectorEqmObj.BEAMLAYERSPLIT = "None"
                            sectorEqmObj.BEAMAZIMUTHOFFSET = MODEL.SECTOREQM.BEAMAZIMUTHOFFSET.NONE
                            pass
                        else:
                            sectorEqmObj.ANTCFGMODE = MODEL.SECTOREQM.ANTCFGMODE.ANTENNAPORT
                        sectorEqmObjList.append(sectorEqmObj)
                        self.save_moc("SECTOREQM", [sectorEqmObj], APPEND_MODE, with_merge=True, with_child=True)

        # 根据扇区设备对象，创建扇区对象
        sectorObjList = self.inner_create_sector_by_sectoreqm(sectorEqmObjList)
        self.save_moc("RRUCHAIN", rruChainObjList, APPEND_MODE, with_merge=True, with_child=True)
        self.save_moc("RRU", rruObjList, APPEND_MODE, with_merge=True, with_child=True)
        self.save_moc("RFU", rfuObjList, APPEND_MODE, with_merge=True, with_child=True)
        self.save_moc("SECTOREQM", sectorEqmObjList, APPEND_MODE, with_merge=True, with_child=True)
        self.save_moc("SECTOR", sectorObjList, APPEND_MODE, with_merge=True, with_child=True)

        return rruChainObjList, rruObjList, rfuObjList, sectorEqmObjList, sectorObjList

    @API_RECORD
    def remove_duplicate(self, sectorEqmObjList):
    # 去重 sectoreqmid 可能会填成重复ID，导致CME规则检查不通过
        id_list = []
        uniq_eqmObjlist = []
        for se_eqm in sectorEqmObjList:
            id_list.append(se_eqm.SECTOREQMID)
            id_list = list(set(id_list))
        for se_eqm in sectorEqmObjList:
            if se_eqm.SECTOREQMID in id_list:
                uniq_eqmObjlist.append(se_eqm)
                id_list.remove(se_eqm.SECTOREQMID)
        return uniq_eqmObjlist

    @API_RECORD
    def get_Com_Plan_Ex(self, excel_file):
        id_plan_map = load_Excel_File(excel_file, "Com Plan", 1, "ID_TYPE")
        if len(id_plan_map) == 0:
            raise Exception("Error: No Com Plan was found in Com Plan sheet")
        for id_type, plan_list in id_plan_map.items():
            result_map = {}
            for plan_info in plan_list:
                band = plan_info.attr(u"FREQ_BAND")
                if band not in result_map:
                    result_map[band] = {}

                for i in range(6):  # 最大支持6个优先级
                    pri_name = "PRI_%d" % i
                    if not hasattr(plan_info, pri_name): continue
                    if plan_info.attr(pri_name):
                        string_list = plan_info.attr(pri_name).split(";")   # BEAM(SEC_120DEG, None)
                        result_map[band][pri_name] = [s.strip() for s in string_list if len(s.strip()) > 0]
                    else:
                        result_map[band][pri_name] = []
            self.Com_Plan_Cache[id_type] = result_map
        self.print_msg("NE=%s Get Com Plan and Save to Cache!" % self.NEName)
        return self.Com_Plan_Cache

    @API_RECORD
    def set_HardwareFromWSD(self, plan_file, physical_site_name=None, addition_rat=""):
        self.get_Wsd_Data(filename=physical_site_name, addition_rat=addition_rat)
        self.get_ID_Plan_Ex(plan_file)
        self.get_Com_Plan_Ex(plan_file)
        self.create_BBUBoard_By_WSD()
        self.create_RXUBoard_By_WSD()
        pass

    @API_RECORD
    def set_HardwareFromNodeTemplate(self,TemplateName,excluding_list=[],including_list=[]):
        moc_list = ["BBP","BBUFAN","MPT","PEU","TRP","USCU","UEIU","BRI","GTMU","UCIU","RFC","RFU","RRU","AAS","AARU","AAMU","RHUB"]
        moc_list.extend(including_list)
        moc_list = list(set(moc_list))
        moc_list = list(set(moc_list)-set(excluding_list))
        for item in moc_list:
            template_list = self.get_data_from_template(TemplateName, item, with_raw=True)
            self.save_moc(item, template_list, APPEND_MODE, with_merge=True)

    @API_RECORD
    def get_antenna_port_assign_mode(self, freq_band_str, port):
        for i in range(6):
            priStr = "PRI_%d" % i
            assignStr = self.Com_Plan_Cache["ASSIGN"][freq_band_str][priStr][0]
            if assignStr in [None, ""]: continue
            txStr = assignStr.split("T")[0]
            rxStr = assignStr.split("T")[1].split("R")[0]
            txList = [ord(i)-ord("A") for i in txStr]
            rxList = [ord(i)-ord("A") for i in rxStr]
            resultStr = ""
            if port in txList:
                resultStr = "".join([resultStr, "TX"])
            if port in rxList:
                resultStr = "".join([resultStr, "RX"])
            if resultStr != "":
                break
        resultStr = "".join([resultStr, "_MODE"])
        return resultStr

    @API_RECORD
    def get_AssignStr(self, ratBandStr, assignList):
        if ratBandStr in self.Com_Plan_Cache["ASSIGN"].keys():
            for i in range(6):
                priStr = "PRI_%d" % i

                assignStr = self.Com_Plan_Cache["ASSIGN"][ratBandStr][priStr]
                if not assignStr: continue
                # 对AAU 大于8T8R的情况下，模式为BEAM（在EXCEL填入BEAM，而不是XTXR）
                if "BEAM" in assignStr[0]:
                    return assignStr
                List = []
                for each_antennae in assignStr: #For JSON to CME Decoding
                    txStr = each_antennae.split("T")[0]
                    rxStr = each_antennae.split("T")[1].split("R")[0]
                    Listtemp = [i for i in "".join([txStr, rxStr])]
                    Listtemp = [x.upper() for x in Listtemp]
                    List.extend(Listtemp)
                List = list(set(List))
                List.sort()
                assignList.sort()
                if List == assignList:
                    return assignStr
        else:
            raise Exception(ratBandStr + " with antennae " + "".join(assignList) + " is not present in CoMPT_GUL.xlsx")
        return ""

    @API_RECORD
    def get_AntennaType(self, assignStr, antNo, index):
        if "BEAM" in assignStr:
            return "RXTX_MODE"
        iAntNo = antNo + index * 32
        txStr = assignStr.split("T")[0]
        rxStr = assignStr.split("T")[1].split("R")[0]
        txList = [ord(s)-ord("A") for s in txStr]
        rxList = [ord(s)-ord("A") for s in rxStr]
        resultStr  = ""
        if iAntNo in rxList:
            resultStr += "RX"
        if iAntNo in txList:
            resultStr += "TX"
        return resultStr + "_MODE"

    @API_RECORD
    def delete_GRat(self, ne_tree):
        if hasattr(ne_tree, "GBTSFUNCTION") == False: return
        print("Info(delete_GRat): Delete GSM Rat Data:")
        # delete SCTPLNK
        cpbearid_list = self.get_para_list_from_moc(ne_tree["GBTSABISCP"], "CPBEARID")
        sctplnkid_list = self.get_para_list_from_moc(ne_tree["CPBEARER"], "LINKNO", WHERE(lambda o: o.CPBEARID in cpbearid_list))
        print("Info(delete_GRat): Delete GSM SCTPLNK:", sctplnkid_list)
        ne_tree["GBTSABISCP"] = []
        ne_tree["CPBEARER"] = self.get_moc_list_by_del(ne_tree["CPBEARER"], WHERE(lambda o: o.CPBEARID in cpbearid_list))
        ne_tree["SCTPLNK"] = self.get_moc_list_by_del(ne_tree["SCTPLNK"], WHERE(lambda o: o.SCTPNO in sctplnkid_list))

        if hasattr(MODEL, "GBTSFUNCTION"):
            moc_name_list = MODEL.GBTSFUNCTION.get_child_names(True) + MODEL.GLOCELL.get_child_names(True)
            print(moc_name_list)
            for moc in moc_name_list:
                if hasattr(ne_tree, moc) == False: continue
                del ne_tree[moc]
            del ne_tree["GBTSFUNCTION"]
        ne_tree["APPLICATION"] = self.get_moc_list_by_del(ne_tree["APPLICATION"], WHERE(AT=MODEL.APPLICATION.AT.GBTS))
        pass

    @API_RECORD
    def delete_URat(self, ne_tree):
        if hasattr(ne_tree, "NODEBFUNCTION") == False: return
        print("Info(delete_URat): Delete UMTS Rat Data:")
        # delete SCTPLNK
        cpbearid_list = self.get_para_list_from_moc(ne_tree["IUBCP"], "CPBEARID")
        sctplnkid_list = self.get_para_list_from_moc(ne_tree["CPBEARER"], "LINKNO", WHERE(lambda o: o.CPBEARID in cpbearid_list))
        print("Info(delete_URat): Delete UMTS SCTPLNK:", sctplnkid_list)
        ne_tree["IUBCP"] = []
        ne_tree["CPBEARER"] = self.get_moc_list_by_del(ne_tree["CPBEARER"], WHERE(lambda o: o.CPBEARID in cpbearid_list))
        ne_tree["SCTPLNK"] = self.get_moc_list_by_del(ne_tree["SCTPLNK"], WHERE(lambda o: o.SCTPNO in sctplnkid_list))

        # delete UMTS RAT
        if hasattr(MODEL, "NODEBFUNCTION"):
            moc_name_list = MODEL.NODEBFUNCTION.get_child_names(True) + MODEL.ULOCELL.get_child_names(True)
            print(moc_name_list)
            for moc in moc_name_list:
                if hasattr(ne_tree, moc) == False: continue
                del ne_tree[moc]
            del ne_tree["NODEBFUNCTION"]
        ne_tree["APPLICATION"] = self.get_moc_list_by_del(ne_tree["APPLICATION"], WHERE(AT=MODEL.APPLICATION.AT.NodeB))
        pass

    @API_RECORD
    def delete_NRat(self, ne_tree):
        if hasattr(ne_tree, "gNodeBFunction")==False: return
        print("Info(delete_NRat): Delete NR Rat Data:")
        if hasattr(MODEL, "gNodeBFunction"):
            moc_name_list = MODEL.gNodeBFunction.get_child_names(True) + MODEL.NRDUCell.get_child_names(True) + MODEL.NRCell.get_child_names(True)
            print(moc_name_list)
            for moc in moc_name_list:
                if hasattr(ne_tree, moc) == False: continue
                del ne_tree[moc]
            del ne_tree["gNodeBFunction"]
        ne_tree["APPLICATION"] = self.get_moc_list_by_del(ne_tree["APPLICATION"], WHERE(AT=MODEL.APPLICATION.AT.gNodeB))
        pass

    @API_RECORD
    def delete_LRat(self, ne_tree):
        if hasattr(ne_tree, "eNodeBFunction")==False: return
        print("Info(delete_LRat): Delete LTE Rat Data:")
        if hasattr(MODEL, "eNodeBFunction"):
            moc_name_list = MODEL.eNodeBFunction.get_child_names(True) + MODEL.Cell.get_child_names(True)
            print(moc_name_list)
            for moc in moc_name_list:
                if hasattr(ne_tree, moc) == False: continue
                del ne_tree[moc]
            del ne_tree["eNodeBFunction"]
        ne_tree["APPLICATION"] = self.get_moc_list_by_del(ne_tree["APPLICATION"], WHERE(AT=MODEL.APPLICATION.AT.eNodeB))
        pass

    @API_RECORD
    def create_NEFromOldNE(self, product_type, old_ne_name=None, new_gnodeb_name=None, new_enodeb_name=None, new_nodeb_name=None, new_gbts_name=None):
        if old_ne_name is None:
            old_ne_name = self.NEName
        if not (new_enodeb_name or new_gbts_name or new_nodeb_name or new_gnodeb_name):
            msg = 'Info(create_NEFromOldNE): No new Rat Fill'
            self.print_msg(msg)
            return
        ne_tree = self.get_all_moc_from_ref(old_ne_name, with_clone=True)

        if new_gnodeb_name == None:  # delete NR RAT
            self.delete_NRat(ne_tree)

        if new_enodeb_name == None:  # delete LTE RAT
            self.delete_LRat(ne_tree)

        if new_nodeb_name == None:  # Delete UMTS RAT
            self.delete_URat(ne_tree)

        if new_gbts_name == None:  # Delete GSM RAT
            self.delete_GRat(ne_tree)

        # Check if from CoMPT to Single mode. If so, need Create NODE
        if "WCDMA" in product_type or "LTE" in product_type or "NR" in product_type or "5G" in product_type:  # Single Mode
            node_obj = MODEL.NODE(PRODUCTTYPE=product_type, WM="NON-CONCURRENT", NODENAME=self.NEName, NODEID=1)
            ne_tree.NODE = [node_obj]
            single_mode = True
        else:
            ne_tree.NODE[0].NENAME = self.NEName  # SET NE Name
            single_mode = False

        # Set RAT Name
        if new_gnodeb_name != None:
            ne_tree["gNodeBFunction"][0].gNodeBFunctionName = new_gnodeb_name  # Set NR RAT Name
            if single_mode:
                ne_tree["gNodeBFunction"][0].gNodeBFunctionName = self.NEName

        if new_enodeb_name != None:
            ne_tree["eNodeBFunction"][0].eNodeBFunctionName = new_enodeb_name  # Set LTE RAT Name
            if single_mode:
                ne_tree["eNodeBFunction"][0].eNodeBFunctionName = self.NEName

        if new_nodeb_name != None:
            ne_tree["NODEBFUNCTION"][0].NODEBFUNCTIONNAME = new_nodeb_name  # Set UMTS RAT Name
            if single_mode:
                ne_tree["NODEBFUNCTION"][0].NODEBFUNCTIONNAME = self.NEName  # Set UMTS RAT Name

        if new_gbts_name != None:
            ne_tree["GBTSFUNCTION"][0].GBTSFUNCTIONNAME = new_gbts_name  # Set GSM RAT Name

        # Delete Inventory Data
        for moc in ["EQMTOINVENTORYUNITHW", "INVENTORYUNITHW", "TOINVENTORYUNITHW"]:
            if hasattr(ne_tree, moc):
                del ne_tree[moc]

        # COMMIT_DATA
        self.save_all_mocs(ne_tree, APPEND_MODE, with_merge=True, include_mocs=None, exclude_mocs=None)

        # Must Create NE, set NE Name
        self.set_moc("NE", NENAME=self.NEName, LOCATION=ne_tree.NE[0].LOCATION, SITENAME=ne_tree.NE[0].SITENAME)


    @API_RECORD
    def adjust_Cabinet(self, old, new):
        #Get current cabinet no
        cabinet_cn_list = self.get_para_list_from_moc("CABINET", "CN")
        # convert string to integer
        old_cn = int(old)
        new_cn = int(new)
        # check if input Cabinet_No exist
        if old_cn not in cabinet_cn_list:
            self.print_msg("Error: CABINET CN=%d is not exist. Cannot modify" % old_cn)
            return False
        if new_cn in cabinet_cn_list:
            self.print_msg("Error: CABINET CN=%d is already exist. Cannot modify" % new_cn)
            return False
        # Adjust cabinet no
        self.print_msg("Adjust CABINET CN from %d to %d" % (old_cn, new_cn))
        self.mod_moc("CABINET", MOD(CN=new_cn).WHERE(CN=old_cn))
        return True

    # Adjust Subrack NO
    @API_RECORD
    def adjust_Subrack(self, old, new):
        #Get current subrack no
        subrack_cn_srn_list = self.get_para_list_from_moc("SUBRACK", ["CN", "SRN"])
        old_cn, old_srn = old.split("-")
        new_cn, new_srn = new.split("-")
        # Convert input subrack no to integer
        old_cn, old_srn = int(old_cn), int(old_srn)
        new_cn, new_srn = int(new_cn), int(new_srn)
        #Check
        if [old_cn, old_srn] not in subrack_cn_srn_list:
            self.print_msg("Error: SUBRACK %s is not exist. Cannot modify" % old)
            return False
        if [new_cn, new_srn] in subrack_cn_srn_list:
            self.print_msg("Error: SUBRACK %s is already exist. Cannot modify" % new)
            return False
        #Adjust
        self.print_msg("Adjust SUBRACK from %s to %s" % (old, new))
        self.mod_moc("SUBRACK", MOD(CN=new_cn, SRN=new_srn).WHERE(CN=old_cn, SRN=old_srn))
        return True

    # Adjust BBP slot
    @API_RECORD
    def adjust_BBP(self, old, new):
        bbp_cn_srn_sn_list = self.get_para_list_from_moc("BBP", ["CN", "SRN", "SN"])
        if "-" in old:
            old_cn, old_srn, old_sn = old.split("-")
            new_cn, new_srn, new_sn = new.split("-")
            # Convert input data to integer
            old_cn, old_srn, old_sn = int(old_cn), int(old_srn), int(old_sn)
            new_cn, new_srn, new_sn = int(new_cn), int(new_srn), int(new_sn)
        else:
            old_cn, old_srn, old_sn = 0, 0, int(old)
            new_cn, new_srn, new_sn = 0, 0, int(new)
        #Check
        if [old_cn, old_srn, old_sn] not in bbp_cn_srn_sn_list:
            self.print_msg("Error: BBP %s is not exist. Cannot modify" % old)
            return False
        if [new_cn, new_srn, new_sn] in bbp_cn_srn_sn_list:
            self.print_msg("Error: BBP %s is already exist. Cannot modify" % new)
            return False
        #Adjust
        self.print_msg("Adjust BBP from %s to %s" % (old, new))
        self.mod_moc("BBP", MOD(CN=new_cn, SRN=new_srn, SN=new_sn).WHERE(CN=old_cn, SRN=old_srn, SN=old_sn))
        return True

    # Adjust RRU subrack
    @API_RECORD
    def adjust_RRU(self, old, new):
        cn_srn_sn_list = self.get_para_list_from_moc("RRU", ["CN", "SRN", "SN"])
        if "-" in old:
            old_cn, old_srn, old_sn = old.split("-")
            new_cn, new_srn, new_sn = new.split("-")
            old_cn, old_srn, old_sn = int(old_cn), int(old_srn), int(old_sn)
            new_cn, new_srn, new_sn = int(new_cn), int(new_srn), int(new_sn)
        else:
            old_cn, old_srn, old_sn = 0, int(old), 0
            new_cn, new_srn, new_sn = 0, int(new), 0
        # Check
        if [old_cn, old_srn, old_sn] not in cn_srn_sn_list:
            self.print_msg("Error: RRU %s is not exist. Cannot modify" % old)
            return False
        if [new_cn, new_srn, new_sn] in cn_srn_sn_list:
            self.print_msg("Error: RRU %s is already exist. Cannot modify" % new)
            return False
        # Adjust
        self.print_msg("Adjust RRU from %s to %s" % (old, new))
        self.mod_moc("RRU", MOD(CN=new_cn, SRN=new_srn, SN=new_sn).WHERE(CN=old_cn, SRN=old_srn, SN=old_sn))
        return True

    #Adjust RFU Pos
    @API_RECORD
    def adjust_RFU(self, old, new):
        cn_srn_sn_list = self.get_para_list_from_moc("RFU", ["CN", "SRN", "SN"])
        if "-" in old:
            old_cn, old_srn, old_sn = old.split("-")
            new_cn, new_srn, new_sn = new.split("-")
            #
            old_cn, old_srn, old_sn = int(old_cn), int(old_srn), int(old_sn)
            new_cn, new_srn, new_sn = int(new_cn), int(new_srn), int(new_sn)
        else:
            old_cn, old_srn, old_sn = 0, int(old), 0
            new_cn, new_srn, new_sn = 0, int(new), 0
        # Check
        if [old_cn, old_srn, old_sn] not in cn_srn_sn_list:
            self.print_msg("Error: RFU %s is not exist. Cannot modify" % old)
            return False
        if [new_cn, new_srn, new_sn] in cn_srn_sn_list:
            self.print_msg("Error: RFU %s is already exist. Cannot modify" % new)
            return False
        # Adjust
        self.print_msg("Adjust RFU from %s to %s" % (old, new))
        self.mod_moc("RFU", MOD(CN=new_cn, SRN=new_srn, SN=new_sn).WHERE(CN=old_cn, SRN=old_srn, SN=old_sn))
        return True

    # Adjust MPT Slot
    @API_RECORD
    def adjust_MPT(self, old, new):
        #获得当前主控板的柜框槽号列表，机柜号是整数
        cn_srn_sn_list = self.get_para_list_from_moc("MPT", ["CN", "SRN", "SN"])
        if "-" in old:
            old_cn, old_srn, old_sn = old.split("-")
            new_cn, new_srn, new_sn = new.split("-")
            #
            old_cn, old_srn, old_sn = int(old_cn), int(old_srn), int(old_sn)
            new_cn, new_srn, new_sn = int(new_cn), int(new_srn), int(new_sn)
        else:
            old_cn, old_srn, old_sn = 0, 0, int(old)
            new_cn, new_srn, new_sn = 0, 0, int(new)
        # Check
        if [old_cn, old_srn, old_sn] not in cn_srn_sn_list:
            self.print_msg("Error: MPT %s is not exist. Cannot modify" % old)
            return False
        if [new_cn, new_srn, new_sn] in cn_srn_sn_list:
            self.print_msg("Error: MPT %s is already exist. Cannot modify" % new)
            return False
        # Adjust
        self.print_msg("Adjust MPT from %s to %s" % (old, new))
        self.mod_moc("MPT", MOD(CN=new_cn, SRN=new_srn, SN=new_sn).WHERE(CN=old_cn, SRN=old_srn, SN=old_sn))
        return True

    # Adjust TX Ethport
    @API_RECORD
    def adjust_Ethport(self, old, new):
        old_pn = int(old)
        new_pn = int(new)
        # Check current Port
        obj_list = self.get_moc("DEVIP", WHERE(PT=MODEL.DEVIP.PT.ETH, PN=old_pn))
        if len(obj_list) > 0:
            self.print_msg("Info: Modify TX port from %d to %d" % (old_pn, new_pn))
            self.mod_moc("DEVIP", MOD(PN=new_pn).WHERE(PT=MODEL.DEVIP.PT.ETH, PN=old_pn))
            self.mod_moc("IPPATH", MOD(PN=new_pn).WHERE(PT=MODEL.DEVIP.PT.ETH, PN=old_pn))
            return True
        return False

    # Found LTE IP(Control Panel)
    @API_RECORD
    def get_LteS1CpIpList(self):
        lte_ip_list = []
        S1 = self.get_moc('S1')
        EPGROUP = self.get_moc('EPGROUP')
        SCTPHOST = self.get_moc('SCTPHOST')
        if len(S1) > 0:
            epgroupid_list = []
            for s1_obj in S1:
                if s1_obj.EpGroupCfgFlag == MODEL.S1.EpGroupCfgFlag.UP_CFG: continue  # Only up, skip
                if s1_obj.CpEpGroupId not in epgroupid_list:
                    epgroupid_list.append(s1_obj.CpEpGroupId)
            sctphostid_list = []
            for ep_obj in EPGROUP:
                if ep_obj.EPGROUPID not in epgroupid_list: continue
                for sctphostref in ep_obj.SCTPHOSTREFS:
                    if sctphostref.SCTPHOSTID not in sctphostid_list:
                        sctphostid_list.append(sctphostref.SCTPHOSTID)
            for sctphost_obj in SCTPHOST:
                if sctphost_obj.SCTPHOSTID not in sctphostid_list:  continue
                lte_ip_list.append(sctphost_obj.SIGIP1V4)
                lte_ip_list.append(sctphost_obj.SIGIP2V4)
        S1Interface = self.get_moc('S1Interface')
        CPBEARER = self.get_moc('CPBEARER')
        SCTPLNK = self.get_moc('SCTPLNK')
        if len(S1Interface) > 0:
            cpbearerid_list = []
            for s1_itf_obj in S1Interface:
                if s1_itf_obj.AutoCfgFlag == MODEL.S1Interface.CtrlMode.AUTO_MODE: continue
                if s1_itf_obj.S1CpBearerId not in cpbearerid_list:
                    cpbearerid_list.append(s1_itf_obj.S1CpBearerId)
            sctplnkid_list = []
            for cpbearer_obj in CPBEARER:
                if cpbearer_obj.AUTOCFGFLAG == MODEL.CPBEARER.AUTOCFGFLAG.AUTO_CREATED: continue
                if cpbearer_obj.CPBEARID not in cpbearerid_list: continue
                if cpbearer_obj.LINKNO not in sctplnkid_list:
                    sctplnkid_list.append(cpbearer_obj.LINKNO)

            for sctplnk_obj in SCTPLNK:
                if sctplnk_obj.SCTPNO not in sctplnkid_list: continue
                lte_ip_list.append(sctplnk_obj.LOCIP)
                lte_ip_list.append(sctplnk_obj.SECLOCIP)

        lte_ip_list = list(set(lte_ip_list))  # Remove Duplicate
        for abnormal in [0, None]:  # Remove 0, None
            if abnormal in lte_ip_list:
                lte_ip_list.remove(abnormal)
        return lte_ip_list

    # From DEVIP to Get MASK/GATEWAY/VLAN
    @API_RECORD
    def get_MaskGatewayVlanByDevip(self, devip):
        mask_list = self.get_para_list_from_moc("DEVIP", "MASK", WHERE(IP=devip))
        mask = mask_list[0] if len(mask_list) > 0 else None
        network = devip & mask
        gateway_list = self.get_para_list_from_moc("IPRT", "NEXTHOP", WHERE(lambda o: o.NEXTHOP & mask == network))
        gateway = gateway_list[0] if len(gateway_list) > 0 else None
        vlan_list = self.get_para_list_from_moc("VLANMAP", "VLANID", WHERE(NEXTHOPIP=gateway))
        vlan = vlan_list[0] if len(vlan_list) > 0 else None
        return (mask, gateway, vlan)

    @API_RECORD
    def create_BaseBandEqm(self, bbp_pri_list, bbp_list_dict=None):
        if bbp_list_dict is None:
            bbp_list_dict = self.Rat_BBP_Cache
        basebandeqm_obj_list = []
        basebandeqm_id_dict = {"F": [], "T": [], "U": {"DL": [],"UL": []}}
        if bbp_list_dict["F"] not in  [None,[]]:
            bb_brd_list = [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=cn, SRN=srn, SN=sn) for (cn,srn,sn) in bbp_list_dict["F"]]
            obj = MODEL.BASEBANDEQM(BASEBANDEQMID=0, BASEBANDEQMTYPE="ULDL", UMTSDEMMODE="NULL", BASEBANDEQMBOARD=bb_brd_list)
            basebandeqm_obj_list.append(obj)
            basebandeqm_id_dict["F"].append(0)
        if bbp_list_dict["T"] not in [None,[]]:
            bb_brd_list = [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=cn, SRN=srn, SN=sn) for (cn,srn,sn) in bbp_list_dict["T"]]
            obj = MODEL.BASEBANDEQM(BASEBANDEQMID=1, BASEBANDEQMTYPE="ULDL", UMTSDEMMODE="NULL", BASEBANDEQMBOARD=bb_brd_list)
            basebandeqm_obj_list.append(obj)
            basebandeqm_id_dict["T"].append(1)
        if bbp_list_dict["U"] not in [None, []]:
            bb_brd_list = [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=cn, SRN=srn, SN=sn) for (cn,srn,sn) in bbp_list_dict["U"]]
            obj = MODEL.BASEBANDEQM(BASEBANDEQMID=1, BASEBANDEQMTYPE="DL", UMTSDEMMODE="NULL",
                                    BASEBANDEQMBOARD=bb_brd_list)
            basebandeqm_obj_list.append(obj)
            basebandeqm_id_dict["U"]["DL"].append(2)
            for (cn,srn,sn) in bbp_list_dict["U"]:
                bbid = bbp_pri_list.index(sn) + 2
                obj = MODEL.BASEBANDEQM(BASEBANDEQMID=bbid, BASEBANDEQMTYPE="UL", UMTSDEMMODE="DEM_2_CHAN",
                                        BASEBANDEQMBOARD=[MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=cn, SRN=srn, SN=sn)])
                basebandeqm_obj_list.append(obj)
                basebandeqm_id_dict["U"]["UL"].append(bbid)
        self.save_moc("BASEBANDEQM", basebandeqm_obj_list, OVERWRITE_MODE)
        return basebandeqm_id_dict

    @API_RECORD
    def delete_UselessRXU(self):
        busy_rxupos_list = []
        sectoreqm_obj_list = self.get_moc("SECTOREQM")
        for sectoreqm_obj in sectoreqm_obj_list:
            ant_obj_list = sectoreqm_obj.SECTOREQMANTENNA
            for ant_obj in ant_obj_list:
                rxupos_str = "%s-%s-%s" % (ant_obj.CN, ant_obj.SRN, ant_obj.SN)
                if rxupos_str not in busy_rxupos_list:
                    busy_rxupos_list.append(rxupos_str)
        self.del_moc("RRU", WHERE(lambda o: "%s-%s-%s" % (o.CN, o.SRN, o.SN) not in busy_rxupos_list))
        self.del_moc("RFU", WHERE(lambda o: "%s-%s-%s" % (o.CN, o.SRN, o.SN) not in busy_rxupos_list))
        busy_rruchain_list = []
        rru_rruchain_list = self.get_para_list_from_moc("RRU", "RCN")
        busy_rruchain_list.extend(rru_rruchain_list)
        rfu_rruchain_list = self.get_para_list_from_moc("RFU", "RCN")
        busy_rruchain_list.extend(rfu_rruchain_list)
        busy_rruchain_list = list(set(busy_rruchain_list))
        self.del_moc("RRUCHAIN", WHERE(lambda o: o.RCN not in busy_rruchain_list))
        return

    @API_RECORD
    def delete_UselessSECTOREQM(self):
        busy_sectoreqm_id_list = []
        sectoreqm_id_list_2g = self.get_para_list_from_moc("GTRXGROUPSECTOREQM", "SECTOREQMID")
        busy_sectoreqm_id_list.extend(sectoreqm_id_list_2g)
        sectoreqm_id_list_3g = self.get_para_list_from_moc("ULOCELLSECTOREQM", "SECTOREQMID")
        busy_sectoreqm_id_list.extend(sectoreqm_id_list_3g)
        sectoreqm_id_list_4g = self.get_para_list_from_moc("eUCellSectorEqm", "SectorEqmId")
        busy_sectoreqm_id_list.extend(sectoreqm_id_list_4g)
        sectoreqm_id_list_5g = self.get_para_list_from_moc("NRDUCellCoverage", "SectorEqmId")
        busy_sectoreqm_id_list.extend(sectoreqm_id_list_5g)
        busy_sectoreqm_id_list = list(set(busy_sectoreqm_id_list))
        self.del_moc("SECTOREQM", WHERE(lambda o: o.SECTOREQMID not in busy_sectoreqm_id_list))
        return busy_sectoreqm_id_list

    @API_RECORD
    def create_BaseBandEqm_Ex(self, lte_bbp_list=None, umts_bbp_list=None,nr_bbp_list=None, with_clear=True, umts_cell_count=0, umtsdemmode="DEM_2_CHAN"):
        if with_clear is True:
            self.del_moc("BASEBANDEQM")
        if lte_bbp_list is None and umts_bbp_list is None and nr_bbp_list is None:
            nr_bbp_list = self.Rat_BBP_Cache["N"]
            lte_bbp_list = self.Rat_BBP_Cache["F"]
            umts_bbp_list = self.Rat_BBP_Cache["U"]
        if umts_cell_count == 0:
            umts_cell_count = self.UMTS_Cell_Count
        if nr_bbp_list not in [None, []]:
            bbid = self.get_free_id_list("BASEBANDEQM", "BASEBANDEQMID" , 0,10)[0]
            bb_brd_list = [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=item[1], SRN=item[2], SN=item[3]) for item in nr_bbp_list]
            snList = [x[3] for x in nr_bbp_list]
            self.add_moc("BASEBANDEQM", BASEBANDEQMID=bbid, BASEBANDEQMTYPE="ULDL", UMTSDEMMODE="NULL", BASEBANDEQMBOARD=bb_brd_list)
            self.BaseBandEqm_Cache["N"].append((bbid, "NR", snList))
        if lte_bbp_list not in [None, []]:
            bbid = self.get_free_id_list("BASEBANDEQM", "BASEBANDEQMID" , 10,20)[0]
            bb_brd_list = [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=item[1], SRN=item[2], SN=item[3]) for item in lte_bbp_list]
            snList = [x[3] for x in lte_bbp_list]
            self.add_moc("BASEBANDEQM", BASEBANDEQMID=bbid, BASEBANDEQMTYPE="ULDL", UMTSDEMMODE="NULL", BASEBANDEQMBOARD=bb_brd_list)
            self.BaseBandEqm_Cache["F"].append((bbid, "FDD", snList, len(snList)*6))
        if umts_bbp_list not in [None, []]:
            bbid = self.get_free_id_list("BASEBANDEQM", "BASEBANDEQMID", 0, 100, WHERE(lambda o: o.BASEBANDEQMTYPE in ["DL", MODEL.BASEBANDEQM.BASEBANDEQMTYPE.DL]))[0]
            bb_brd_list = [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=item[1], SRN=item[2], SN=item[3]) for item in umts_bbp_list]
            snList = [x[3] for x in umts_bbp_list]
            self.add_moc("BASEBANDEQM", BASEBANDEQMID=bbid, BASEBANDEQMTYPE="DL", UMTSDEMMODE="NULL", BASEBANDEQMBOARD=bb_brd_list)
            self.BaseBandEqm_Cache["U"]["DL"].append((bbid, "UMTS_DL", snList, len(snList)*6))
            if umts_cell_count <= 6:
                bb_brd_list = [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=item[1], SRN=item[2], SN=item[3]) for item in umts_bbp_list]
                snList = [x[3] for x in umts_bbp_list]
                bbid = self.get_free_id_list("BASEBANDEQM", "BASEBANDEQMID", 0, 100, WHERE(lambda o: o.BASEBANDEQMTYPE in ["UL", MODEL.BASEBANDEQM.BASEBANDEQMTYPE.UL]))[0]
                self.add_moc("BASEBANDEQM", BASEBANDEQMID=bbid, BASEBANDEQMTYPE="UL", UMTSDEMMODE=umtsdemmode,
                             BASEBANDEQMBOARD=bb_brd_list)
                self.BaseBandEqm_Cache["U"]["UL"].append((bbid, "UMTS_UL_ALL", snList))
            else:
                bb_brd_list = [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=item[1], SRN=item[2], SN=item[3]) for item in
                               umts_bbp_list if "WBBP" in item[0]]
                snList = [x[3] for x in umts_bbp_list if "WBBP" in x[0]]
                if bb_brd_list not in [None, []]:
                    bbid = self.get_free_id_list("BASEBANDEQM", "BASEBANDEQMID",0, 100, WHERE(lambda o: o.BASEBANDEQMTYPE in ["UL", MODEL.BASEBANDEQM.BASEBANDEQMTYPE.UL]))[0]
                    self.add_moc("BASEBANDEQM", BASEBANDEQMID=bbid, BASEBANDEQMTYPE="UL", UMTSDEMMODE=umtsdemmode,
                                 BASEBANDEQMBOARD=bb_brd_list)
                    self.BaseBandEqm_Cache["U"]["UL"].append((bbid, "UMTS_UL_WBBP", snList, len(snList)*6))

                bb_brd_list = [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=item[1], SRN=item[2], SN=item[3]) for item in
                               umts_bbp_list if "UBBP" in item[0]]
                snList = [x[3] for x in umts_bbp_list if "UBBP" in x[0]]
                if bb_brd_list not in [None, []]:
                    bbid = self.get_free_id_list("BASEBANDEQM", "BASEBANDEQMID", 0, 100, WHERE(lambda o: o.BASEBANDEQMTYPE in ["UL", MODEL.BASEBANDEQM.BASEBANDEQMTYPE.UL]))[0]
                    self.add_moc("BASEBANDEQM", BASEBANDEQMID=bbid, BASEBANDEQMTYPE="UL", UMTSDEMMODE=umtsdemmode,
                                 BASEBANDEQMBOARD=bb_brd_list)
                    self.BaseBandEqm_Cache["U"]["UL"].append((bbid, "UMTS_UL_UBBP", snList, len(snList)*6))
        return self.BaseBandEqm_Cache

    @API_RECORD
    def clear_NeTreePre(self, ne_tree):
        for key in ne_tree:
            for moi in ne_tree[key]:
                if getattr(moi, '__prev', None) is not None:
                    setattr(moi, '__prev', None)

    @API_RECORD
    def get_UMTSCellCount_By_WSD(self):
        if "bbpToCell" not in self.WSD_Info_Cache:
            self.exit_Info("NE=%s No bbpToCell in WSD cache, Please get it using get_Wsd_Data function first" % self.NEName)
        bbpToCell_Dict = self.WSD_Info_Cache["bbpToCell"]
        count = 0
        for slot, bbp_ToCell_Info in bbpToCell_Dict.items():
            if "UO" not in bbp_ToCell_Info["bbp"]: continue
            count += len(bbp_ToCell_Info["cellList"])
        self.UMTS_Cell_Count = count
        return count

    @API_RECORD
    def update_UMTSCellBaseBandEqm(self):
        ulocell_map_list = self.get_para_list_from_moc("ULOCELL", ["ULOCELLID", "DLFREQ", "TTW", "VAM"])
        for ulocell_map_item in ulocell_map_list:
            ulocell_map_item[1] = ulocell_map_item[1]
        if "bbpToCell" not in self.WSD_Info_Cache:
            self.exit_Info(
                "NE=%s No bbpToCell in WSD cache, Please get it using get_Wsd_Data function first" % self.NEName)
        bbpToCell_Dict = self.WSD_Info_Cache["bbpToCell"]
        for slot, bbp_ToCell_Info in bbpToCell_Dict.items():
            if "UO" not in bbp_ToCell_Info["bbp"]: continue
            for getCellItem in bbp_ToCell_Info["cellList"]:
                rat, band, txmode = getCellItem.split("(")[1].split(")")[0].split(",")
                self.set_RatBandTxmodeToULOCELL(slot=int(slot[-1]), band=band, txmode=txmode)
        pass

    @API_RECORD
    def get_TxModeFromTtwAndVam(self, ttw, vam):
        if ttw == MODEL.ULOCELL.TTW.FALSE:
            return "1T2R"
        else:
            return "2T2R"

    @API_RECORD
    def set_RatBandTxmodeToULOCELL(self, slot, band, txmode):
        cellList = self.get_moc("ULOCELL")
        for cellInfo in cellList:
            if self.get_UMTS_Common_Str_From_Dlfreq(cellInfo["DLFREQ"]) in band \
                    and self.get_TxModeFromTtwAndVam(cellInfo["TTW"], cellInfo["VAM"]) == txmode \
                    and "fixDLULBaseBandFlag" not in cellInfo:
                dlbasebandeqmid, ulbasebandeqmid = self.get_BaseBandEqmId_By_Slot_From_BaseBandEqm_Cache(slot)
                if dlbasebandeqmid == 255 or ulbasebandeqmid == 255:
                    self.exit_Info("set_RatBandTxmodeToULOCELL: get dl, ul basebandeqmid error")
                cellInfo["DLBASEBANDEQMID"] = dlbasebandeqmid
                cellInfo["ULBASEBANDEQMID"] = ulbasebandeqmid
                cellInfo["fixDLULBaseBandFlag"] = True
                break
            else:
                pass
        self.save_moc("ULOCELL", cellList, OVERWRITE_MODE)

    @API_RECORD
    def get_BaseBandEqmId_By_Slot_From_BaseBandEqm_Cache(self, slot):
        dl = 255
        ul = 255
        for temp in self.BaseBandEqm_Cache.values():
            if len(temp) == 0: continue
            for key, value in temp.items():
                if key == "DL":
                    for item in value:
                        if slot in item[2]:
                            dl = item[0]
                elif key == "UL":
                    for item in value:
                        if slot in item[2]:
                            ul = item[0]
        return dl, ul


    @API_RECORD
    def get_GSM_SectorEqms(self):
        # 获取GSM扇区设备
        result = []
        sectoreqms = self.get_moc("SECTOREQM")
        for obj in sectoreqms:
            for key in self.ID_Plan_Cache["SECTOREQMID"].keys():
                if "GO" in key:
                    for sector, eqmids in self.ID_Plan_Cache["SECTOREQMID"][key].items():
                        if str(obj.SECTOREQMID) in eqmids:
                            result.append(obj)
                else:
                    continue

        return result

    @API_RECORD
    def adapt_GSM_DCS_Scenes(self):
        # 适配 GSM 开闭小区场景， 开闭场景GTRXGROUP数量与sectoreqm数量一致，不能与EXCEL中的GTXGROUPID一致
        gsm_sectoreqms = self.get_GSM_SectorEqms()
        gtxgroup_obj_list = []
        gtxgroupsectoreqm_list = []
        for seq in gsm_sectoreqms:
            id = seq.SECTOREQMID
            # cell_id = get_glocell_id(seq.SECTOREQMID)
            cell_id = self.get_GLOCELL_id(seq.SECTOREQMID)
            gtxgroup_obj = MODEL.GTRXGROUP(GTRXGROUPID=seq.SECTOREQMID, GLOCELLID=cell_id)
            gtxgroupsectoreqm = MODEL.GTRXGROUPSECTOREQM(GTRXGROUPID=gtxgroup_obj.GTRXGROUPID,
                                                         SECTOREQMID=seq.SECTOREQMID)

            gtxgroup_obj_list.append(gtxgroup_obj)
            gtxgroupsectoreqm_list.append(gtxgroupsectoreqm)
        self.save_moc("GTRXGROUP", gtxgroup_obj_list, OVERWRITE_MODE, with_merge=True, with_child=True)
        self.save_moc("GTRXGROUPSECTOREQM", gtxgroupsectoreqm_list, OVERWRITE_MODE, with_merge=True, with_child=True)
        # bbgrouplist = self.get_moc("GTRXGROUP")

    @API_RECORD
    def get_sector(self,cell_id):
    # 获取小区在缓存中对应的扇区
        for key in self.ID_Plan_Cache["SECTOREQMID"].keys():
            if "GO" in key:
                for sector, eqmids in self.ID_Plan_Cache["SECTOREQMID"][key].items():
                    if cell_id in eqmids:
                        return sector
                else:
                    continue
        return None

    @API_RECORD
    def get_GLOCELL_id(self,sectoreqm_id):
        # 获取与输入参数的扇区设备 同一扇区的小区ID
        cells = self.get_moc("GLOCELL")
        for cell in cells:
            cell_sector = self.get_sector(cell.SECTOREQMID)
            sector = self.get_sector(str(sectoreqm_id))
            if cell_sector == sector:
                return cell.GLOCELLID
            else:
                continue
        return None


class ControllerObject(BaseObject):
    rat_list = []
    short_rat_list = []
    WSD_Info_Cache = {}
    BOM_dict = {}
    CONFIG_dict = {}
    Rat_BBP_Cache = {"G": [], "U": [], "L": [], "F": [], "T": [], "N": []}
    ID_Plan_Cache = {}
    Com_Plan_Cache = {}
    UMTS_Cell_Count = 0
    BaseBandEqm_Cache = {"G": [], "U": {"DL": [], "UL": []}, "L": [], "F": [], "T": [], "N": []}

    @API_RECORD
    def __init__(self):
        self.ControllerName = None
        self.BTSName = None
        self.NodeBName = None
        self.eNodeBName = None
        self.NEVERSION = None
        self.ProductType = None
        self.RRULIST = None
        self.RFULIST = None
        self.BBPLIST = None
        self.MPTLIST = None
        self.controllerType = None
        self.ratStr = ""
        self.start()

    @API_RECORD
    def start(self):
        self.ControllerName = NENAME
        self.controllerType = "BSC6910" if hasattr(MODEL.BRD.BRDCLASS, "GPU") else "BSC6900"
        self.print_msg("Process NE=" + self.ControllerName)
        pass

    @API_RECORD
    def load_Summary_file(self, summary_file_name, variable_dict):
        doc_tree = BaseObject.inner_load_Summary_file(self, summary_file_name, variable_dict, is_controller=True)
        return doc_tree

    @API_RECORD
    def get_data_from_excel(self, excel_name, sheet_name, title_row, group_title, filter_name=None, **kwargs):
        if filter_name is None:
            filter_name = self.ControllerName
        data_map = load_Excel_File(excel_name, sheet_name, title_row, group_title, **kwargs)
        if filter_name not in data_map:
            self.print_msg('%s is not in the %s file %s sheet' % (filter_name, excel_name, sheet_name))
            return []
        return data_map[filter_name]

    @API_RECORD
    def get_parameter_name_value(self, Common_Parameter_map, parameter_name):
        for k, v in Common_Parameter_map.items():
            if parameter_name == k:
                count = 1
                for excel_row in v:
                    if count > 1:
                        msg = "Error: {} map multi row".format(k)
                        self.exit_Info(msg)
                        break
                    count += 1
                    return excel_row.Values

    @API_RECORD
    def get_Ep_Data(self,ne_name, ep_type="Design", with_raw=False):
        return LOAD_EP_FILE(ne_name, ep_type, with_raw)

    @API_RECORD
    def get_SiteInfo(self, site_info_excel_name, site_name_title="*Name",
                     site_info_sheet_name="Base Station Transport Data", ne_name=None, title_row=2, **kwargs):
        site_info_list = self.get_data_from_excel(excel_name=site_info_excel_name, sheet_name=site_info_sheet_name,
                                                  group_title=site_name_title, title_row=title_row, filter_name=ne_name,
                                                  **kwargs)
        if len(site_info_list) != 1:
            msg = "NE=%s No or More than one Site info in file %s sheet %s" % (
            ne_name, site_info_excel_name, site_info_sheet_name)
            self.exit_Info(msg)
        if "*DO" in site_info_list[0]:
            do = site_info_list[0].attr("*DO")
            if do == None or do.upper() != "YES":
                msg = "Skip NE=%s Col DO is not YES or None" % ne_name
                self.exit_Info(msg)
        return site_info_list[0]

    @API_RECORD
    def inner_check_para(self, kwargs, para_list):
        error_count = 0
        for para in para_list:
            if para not in kwargs:
                print("Error: para=%s must provide" % para)
            elif kwargs[para] in [None, "", u""]:
                print("Error: para=%s is None" % para)
                error_count += 1
            else:
                continue
        return error_count

    @API_RECORD
    def get_SiteInfoListGroupByBSC(self, bsc_info_excel_name, bsc_name_title="BSC Name", bsc_info_sheet_name="Base Station Transport Data", bsc_name=None, title_row=2, **kwargs):
        bsc_info_list = self.get_data_from_excel(excel_name=bsc_info_excel_name, sheet_name=bsc_info_sheet_name, group_title=bsc_name_title, title_row=title_row, filter_name=bsc_name, **kwargs)
        bsc_list = []
        for bsc_info in bsc_info_list:
            if "*DO" in bsc_info:
                do = bsc_info.attr("*DO")
                if do is None or do.upper() != "YES": continue
                bsc_list.append(bsc_info)
        if len(bsc_info_list) == 0:
            msg = "No Site in BSC=%s" % bsc_name
            self.print_msg(msg)
        return bsc_list

    @API_RECORD
    def get_SiteInfoListGroupByRNC(self, rnc_info_excel_name, rnc_name_title="RNC Name", rnc_info_sheet_name="Base Station Transport Data", rnc_name=None, title_row=2, **kwargs):
        rnc_info_list = self.get_data_from_excel(excel_name=rnc_info_excel_name, sheet_name=rnc_info_sheet_name, group_title=rnc_name_title, title_row=title_row, filter_name=rnc_name, **kwargs)
        rnc_list = []
        for rnc_info in rnc_info_list:
            if "*DO" in rnc_info:
                do = rnc_info.attr("*DO")
                if do is None or do.upper() != "YES": continue
                rnc_list.append(rnc_info)
        return rnc_list

    @API_RECORD
    def get_CellInfoList(self, cell_info_excel_name, cell_info_sheet_name, site_name_title, ne_name=None, title_row=2,  **kwargs):
        cell_info_list = self.get_data_from_excel(excel_name=cell_info_excel_name, sheet_name=cell_info_sheet_name, group_title=site_name_title, title_row=title_row, filter_name=ne_name, **kwargs)
        if len(cell_info_list) == 0:
            msg = "Error: NE=%s No Cell info in file %s sheet %s" % (ne_name, cell_info_excel_name, cell_info_sheet_name)
            self.exit_Info(msg)
        return cell_info_list

    @API_RECORD
    def get_IPInfo(self, ip_info_excel_name, ip_info_sheet_name="IP Data", site_name_title="*NE Name", ne_name=None, title_row=2, **kwargs):
        ip_info_list = self.get_data_from_excel(excel_name=ip_info_excel_name, sheet_name=ip_info_sheet_name, group_title=site_name_title, title_row=title_row, filter_name=ne_name, **kwargs)
        if len(ip_info_list) != 1:
            msg = "Error: NE=%s No or More than one IP info in file %s sheet %s" % (ne_name, ip_info_excel_name, ip_info_sheet_name)
            self.exit_Info(msg)
        return ip_info_list[0]

    @API_RECORD
    def get_UNODEB_by_name(self, nodeb_name):
        tmp_name = nodeb_name.upper().strip()
        unodeb_obj_list = self.get_moc("UNODEB")
        for unodeb_obj in unodeb_obj_list:
            if unodeb_obj.NODEBNAME.upper() == tmp_name:
                return unodeb_obj
        return None

    @API_RECORD
    def create_UNODEB_Node(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["NODEBID", "NODEBNAME", "ANI"])
        if "LOGICRNCID" not in kwargs:
            kwargs["LOGICRNCID"] = 0
        if "SN" not in kwargs:
            kwargs["SN"] = 0
        if "SRN" not in kwargs:
            kwargs["SRN"] = 0
        if "SSN" not in kwargs:
            kwargs["SSN"] = 0
        if "CNOPINDEX" not in kwargs:
            kwargs["CNOPINDEX"] = 0
        #此处需要判断BSC6900 还是6910 ,6900不需要配置IPPOOL,6910保持原来的逻辑
        bsc_type = "BSC6910" if hasattr(MODEL.BRD.BRDCLASS, "GPU") else "BSC6900"
        if bsc_type == "BSC6900":
            if "ISIPPOOL" not in kwargs:
                kwargs["ISIPPOOL"] = 0
        else:
            if "IPPOOLINDEX" not in kwargs:
                kwargs["IPPOOLINDEX"] = 0

        if "TNLBEARERTYPE" not in kwargs:
            kwargs["TNLBEARERTYPE"] = MODEL.UNODEB.TNLBEARERTYPE.IP_TRANS

        if "IPTRANSAPARTIND" not in kwargs:
            kwargs["IPTRANSAPARTIND"] = 0

        if "SHARINGTYPE" not in kwargs:
            kwargs["SHARINGTYPE"] = MODEL.UNODEB.SHARINGTYPE.DEDICATED
        self.add_moc("UNODEB", **kwargs)
        if "NODET" not in kwargs:
            kwargs["NODET"] = MODEL.ADJNODE.NODET.IUB
        if "TRANST" not in kwargs:
            kwargs["TRANST"] = MODEL.ADJNODE.TRANST.IP
        if "TXBW" not in kwargs:
            kwargs["TXBW"] = 100000
        if "RXBW" not in kwargs:
            kwargs["RXBW"] = 100000
        kwargs["NAME"] = kwargs["NODEBNAME"]
        self.add_moc("ADJNODE", **kwargs)
        if "ITFT" not in kwargs:
            kwargs["ITFT"] = MODEL.ADJMAP.ITFT.IUB
        if "TRANST" not in kwargs:
            kwargs["TRANST"] = MODEL.ADJMAP.TRANST.IP
        if "CNMNGMODE" not in kwargs:
            kwargs["CNMNGMODE"] = MODEL.ADJMAP.CNMNGMODE.SHARE

        trmmaps = self.get_moc("TRMMAP",WHERE(ITFT=kwargs["NODET"],TRANST=kwargs["TRANST"]))
        if(len(trmmaps)>0):
            if "TMIGLD" not in kwargs:
                kwargs["TMIGLD"] = trmmaps[-1].TMI  #取最后一个，比较新
            if "TMISLV" not in kwargs:
                kwargs["TMISLV"] = trmmaps[-1].TMI
            if "TMIBRZ" not in kwargs:
                kwargs["TMIBRZ"] = trmmaps[-1].TMI
        if "FTI" not in kwargs:
            kwargs["FTI"] = 0


        self.add_moc("ADJMAP", **kwargs)
        self.add_moc("UNODEBOLC", **kwargs)
        self.add_moc("UNODEBLDR", **kwargs)
        self.add_moc("UNODEBALGOPARA", **kwargs)
        if "MNTMODE" not in kwargs:
            kwargs["MNTMODE"] = MODEL.UNODEBMNTMODE.MNTMODE.NORMAL
        self.add_moc("UNODEBMNTMODE", **kwargs)

        return error_count

    @API_RECORD
    def create_UNODEB_UNCP(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["LOCIP1", "PEERIP1", "PEERPN", "NODEBID"])
        if "LOGICRNCID" not in kwargs:
            kwargs["LOGICRNCID"] = 0
        if "SCTPSN" not in kwargs:
            kwargs["SCTPSN"] = 0
        if "SCTPSRN" not in kwargs:
            kwargs["SCTPSRN"] = 0
        if "SCTPSSN" not in kwargs:
            kwargs["SCTPSSN"] = 0
        if "SCTPLNKID" not in kwargs:
            if "SCTPLNKN" in kwargs:
                kwargs["SCTPLNKID"] = int(kwargs["SRN"]) * 1000000 + int(kwargs["SN"]) * 10000 + int(kwargs["SCTPLNKN"])
            else:
                kwargs["SCTPLNKID"] = self.get_free_id_list("SCTPLNK", "SCTPLNKID").pop(0)
        if "REMARK" not in kwargs:
            kwargs["REMARK"] = "NCP For " + kwargs["NODEBID"]
        if "LOGPORTFLAG" not in kwargs:
            kwargs["LOGPORTFLAG"] = MODEL.SCTPLNK.LOGPORTFLAG.NO
        if "APP" not in kwargs:
            kwargs["APP"] = MODEL.SCTPLNK.APP.NBAP
        if "MODE" not in kwargs:
            kwargs["MODE"] = MODEL.SCTPLNK.MODE.SERVER
        if "SPECIFYLOCPNFLAG" not in kwargs:
            kwargs["SPECIFYLOCPNFLAG"] = MODEL.SCTPLNK.SPECIFYLOCPNFLAG.NO
        if "MTU" not in kwargs:
            kwargs["MTU"] = 1500
        self.add_moc("SCTPLNK", **kwargs)
        if "CARRYLNKT" not in kwargs:
            kwargs["CARRYLNKT"] = MODEL.UNCP.CARRYLNKT.SCTP
        self.add_moc("UNCP", **kwargs)

        return  error_count

    @API_RECORD
    def create_UNODEB_UCCP(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["LOCIP1", "PEERIP1", "PEERPN", "NODEBID"])
        if "LOGICRNCID" not in kwargs:
            kwargs["LOGICRNCID"] = 0
        if "SCTPSN" not in kwargs:
            kwargs["SCTPSN"] = 0
        if "SCTPSRN" not in kwargs:
            kwargs["SCTPSRN"] = 0
        if "SCTPSSN" not in kwargs:
            kwargs["SCTPSSN"] = 0
        if "SCTPLNKID" not in kwargs:
            if "SCTPLNKN" in kwargs:
                kwargs["SCTPLNKID"] = int(kwargs["SRN"]) * 1000000 + int(kwargs["SN"]) * 10000 + int(kwargs["SCTPLNKN"])
            else:
                kwargs["SCTPLNKID"] = self.get_free_id_list("SCTPLNK", "SCTPLNKID").pop(0)
        if "REMARK" not in kwargs:
            kwargs["REMARK"] = "NCP For " + kwargs["NODEBID"]
        if "LOGPORTFLAG" not in kwargs:
            kwargs["LOGPORTFLAG"] = MODEL.SCTPLNK.LOGPORTFLAG.NO
        if "APP" not in kwargs:
            kwargs["APP"] = MODEL.SCTPLNK.APP.NBAP
        if "MODE" not in kwargs:
            kwargs["MODE"] = MODEL.SCTPLNK.MODE.SERVER
        if "SPECIFYLOCPNFLAG" not in kwargs:
            kwargs["SPECIFYLOCPNFLAG"] = MODEL.SCTPLNK.SPECIFYLOCPNFLAG.NO
        if "MTU" not in kwargs:
            kwargs["MTU"] = 1500
        self.add_moc("SCTPLNK", **kwargs)
        if "CARRYLNKT" not in kwargs:
            kwargs["CARRYLNKT"] = MODEL.UCCP.CARRYLNKT.SCTP
        if "PN" not in kwargs:
            kwargs["PN"] = 0
        self.add_moc("UCCP", **kwargs)

        return  error_count

    @API_RECORD
    def create_UNODEB_OAM(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["NODEBID", "NODEBNAME", "NBIPOAMIP", "NBIPOAMMASK", "IPSRN", "IPSN"])
        if "LOGICRNCID" not in kwargs:
            kwargs["LOGICRNCID"] = 0

        if "NBTRANTP" not in kwargs:
            kwargs["NBTRANTP"] = MODEL.UNODEBIP.NBTRANTP.IPTRANS_IP
        if "VLANFLAG" not in kwargs:
            kwargs["VLANFLAG"] = MODEL.UNODEBIP.VLANFLAG.DISABLE
        if "IPLOGPORTFLAG" not in kwargs:
            kwargs["IPLOGPORTFLAG"] = "NO"
        self.add_moc("UNODEBIP", **kwargs)
        # obj = MODEL.IPRT(SRN=ipsrn, SN=ipsn, DSTIP=API_IP_GET_NETWORK_SEGMENT(nodeb_ip1,nodeb_mask), DSTMASK=nodeb_mask,
        #                 NEXTHOPTYPE=MODEL.IPRT.NEXTHOPTYPE.Gateway, NEXTHOP=RNC_IP_TO_IPRT(rnc_ip1), PRIORITY=MODEL.IPRT.PRIORITY.HIGH,
        #                 REMARK="IUB")
        # COMMIT_DATA("IPRT", [obj], APPEND_MODE, with_child=True)
        return error_count

    @API_RECORD
    def create_UNODEB_IPPATH(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["ANI", "IPADDR", "PEERIPADDR", "PATHT"])
        if "LOGICRNCID" not in kwargs:
            kwargs["LOGICRNCID"] = 0

        if "ITFT" not in kwargs:
            kwargs["ITFT"] = MODEL.IPPATH.ITFT.IUB
        if "TRANST" not in kwargs:
            kwargs["TRANST"] = MODEL.IPPATH.TRANST.IP
        if "TXBW" not in kwargs:
            kwargs["TXBW"] = 100000
        if "RXBW" not in kwargs:
            kwargs["RXBW"] = 100000
        if "PATHID" not in kwargs:
            kwargs["PATHID"] = self.get_free_id_list("IPPATH","PATHID").pop(0)

        self.add_moc("IPPATH", **kwargs)
        # obj = MODEL.IPRT(SRN=ipsrn, SN=ipsn, DSTIP=API_IP_GET_NETWORK_SEGMENT(nodeb_ip1,nodeb_mask), DSTMASK=nodeb_mask,
        #                 NEXTHOPTYPE=MODEL.IPRT.NEXTHOPTYPE.Gateway, NEXTHOP=RNC_IP_TO_IPRT(rnc_ip1), PRIORITY=MODEL.IPRT.PRIORITY.HIGH,
        #                 REMARK="IUB")
        # COMMIT_DATA("IPRT", [obj], APPEND_MODE, with_child=True)
        return error_count

    @API_RECORD
    def common_data_from_template(self, moc_names, **kwargs):
        if not isinstance(moc_names, list):
            moc_names = [moc_names]
        TemplateName = kwargs["TemplateName"]
        for moc_name in moc_names:
            data_from_template = self.get_data_from_template(TemplateName, moc_name, **kwargs)[0]
            for field_name in data_from_template.get_field_names():
                if field_name not in kwargs:
                    kwargs[field_name] = data_from_template.get(field_name)
        return kwargs

    @API_RECORD
    def create_UCELL(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["NODEBID", "NODEBNAME", "CELLID", "CELLNAME",
                                                     "LOCELL", "BANDIND", "UARFCNDOWNLINK", "LAC", "PSCRAMBCODE", "TCELL",
                                                      "URAID", "SPGID", "RAC", "SAC"])
        if "TemplateName" not in kwargs:
            kwargs["TemplateName"] = "Default 3G Cell Template"
        ucell_template = self.get_data_from_template(kwargs["TemplateName"], "UCELL", with_child=True)[0]
        for field_name in ucell_template.get_field_names():
            if field_name not in kwargs:
                kwargs[field_name] = ucell_template.get(field_name)

        if "LOGICRNCID" not in kwargs:
            kwargs["LOGICRNCID"] = 0
        self.add_moc("ULOCELL",**kwargs)
        if "CNOPINDEX" not in kwargs:
            kwargs["CNOPINDEX"] = 0
        if "CNOPINDEXLIST" in kwargs and kwargs["CNOPINDEXLIST"] is not None:
            for kwargs["CNOPINDEX"] in kwargs["CNOPINDEXLIST"]:
                self.add_moc("USAC", **kwargs)
        else:
            self.add_moc("USAC", **kwargs)
        # URA ID already configured?
        ura_list = self.get_para_list_from_moc("UURA", "URAID", WHERE(CNOPINDEX=kwargs["CNOPINDEX"]))
        if ura_list and int(kwargs["URAID"]) not in ura_list:
            self.add_moc("UURA", **kwargs)
        if "CNOPGRPINDEX" not in kwargs:
            kwargs["CNOPGRPINDEX"] = 0
        if "UARFCNUPLINKIND" not in kwargs:
            kwargs["UARFCNUPLINKIND"] = MODEL.UCELL.UARFCNUPLINKIND.FALSE
        if "CFGRACIND" not in kwargs:
            kwargs["CFGRACIND"] = MODEL.UCELL.CFGRACIND.REQUIRE
        if "EAGCHCODENUM" not in kwargs:
            kwargs["EAGCHCODENUM"] = 3
        if "ERGCHEHICHCODENUM" not in kwargs:
            kwargs["ERGCHEHICHCODENUM"] = 3
        if "MAXTARGETULLOADFACTOR" not in kwargs:
            kwargs["MAXTARGETULLOADFACTOR"] = 70
        if "NONSERVTOTOTALEDCHPWRRATIO" not in kwargs:
            kwargs["NONSERVTOTOTALEDCHPWRRATIO"] = 0
        if "DYNTGTROTCTRLSWITCH" not in kwargs:
            kwargs["DYNTGTROTCTRLSWITCH"] = MODEL.CELLHSUPA.DYNTGTROTCTRLSWITCH.OFF
        if "TGTROTADJPERIOD" not in kwargs:
            kwargs["TGTROTADJPERIOD"] = 5
        if "TGTROTUPADJSTEP" not in kwargs:
            kwargs["TGTROTUPADJSTEP"] = 10
        if "TGTROTDOWNADJSTEP" not in kwargs:
            kwargs["TGTROTDOWNADJSTEP"] = 20
        if "UPLIMITFORMAXULTGTLDFACTOR" not in kwargs:
            kwargs["UPLIMITFORMAXULTGTLDFACTOR"] = 90
        if "ALLOCCODEMODE" not in kwargs:
            kwargs["ALLOCCODEMODE"] = MODEL.CELLHSDPA.ALLOCCODEMODE.Manual
        if "HSPDSCHCODENUM" not in kwargs:
            kwargs["HSPDSCHCODENUM"] = 5
        if "HSSCCHCODENUM" not in kwargs:
            kwargs["HSSCCHCODENUM"] = 3
        if "HSPAPOWER" not in kwargs:
            kwargs["HSPAPOWER"] = 0
        if "HSPDSCHMPOCONSTENUM" not in kwargs:
            kwargs["HSPDSCHMPOCONSTENUM"] = MODEL.CELLHSDPA.HSPDSCHMPOCONSTENUM.field("2.5DB")
        if "HSDPCCHPREAMBLESWITCH" not in kwargs:
            kwargs["HSDPCCHPREAMBLESWITCH"] = MODEL.CELLHSDPA.HSDPCCHPREAMBLESWITCH.field("Mode0")
        if "CODEADJFORHSDPASWITCH" not in kwargs:
            kwargs["CODEADJFORHSDPASWITCH"] = MODEL.CELLHSDPA.CODEADJFORHSDPASWITCH.ON
        if "CODEADJFORHSDPAUSERNUMTHD" not in kwargs:
            kwargs["CODEADJFORHSDPAUSERNUMTHD"] = 3
        if "HCODEADJPUNSHTIMERLENGTH" not in kwargs:
            kwargs["HCODEADJPUNSHTIMERLENGTH"] = 5
        if "MIMOMPOCONSTANT" not in kwargs:
            kwargs["MIMOMPOCONSTANT"] = MODEL.CELLHSDPA.MIMOMPOCONSTANT.field("2.5DB")
        if "DYNHSSCCHALLOCSWITCH" not in kwargs:
            kwargs["DYNHSSCCHALLOCSWITCH"] = MODEL.CELLHSDPA.DYNHSSCCHALLOCSWITCH.OFF
        if "PCPICHPOWER" not in kwargs:
            kwargs["PCPICHPOWER"] = 330
        if "MAXPCPICHPOWER" not in kwargs:
            kwargs["MAXPCPICHPOWER"] = 346
        if "MINPCPICHPOWER" not in kwargs:
            kwargs["MINPCPICHPOWER"] = 313

        # UCELL start
        # 先造个UCELL对象，再把template和UCELL相关的配置都读出来，然后合并到一起

        ucell_obj = MODEL.UCELL(**kwargs)

        new_ucell_obj = self.save_data_with_template([ucell_obj], ucell_template)[0]

        # 处理UCELL相关的子对象，找到子对象，如果子对象的子参数在kwargs里面存在就赋值过去
        ucell_obj_dict = vars(new_ucell_obj)
        for sub_name, sub_obj_list in ucell_obj_dict.items():
            if type(sub_obj_list) is list and len(sub_obj_list) > 0:
                sub_obj = sub_obj_list[0]
                sub_obj_dict = vars(sub_obj)
                for key, value in sub_obj_dict.items():
                    if key in kwargs and kwargs[key] != None:
                        setattr(sub_obj, key, kwargs[key])

        # 保存UCELL和其相关的子对象
        self.save_moc("UCELL", [new_ucell_obj], APPEND_MODE, with_child=True, with_merge=True)
        # UCELL end

        return error_count

    @API_RECORD
    def create_USMLCCELL(self, **kwargs):
        error_count = self.inner_check_para(kwargs,  ["RNCID", "CELLID", "ANTENNALATITUDEDEGREE",
                                                      "ANTENNALONGITUDEDEGREE", "ANTENNAALTITUDEMETER",
                                                      "ANTENNAORIENTATION", "MAXANTENNARANGE",
                                                      "ANTENNAOPENING", "CELLAVERAGEHEIGHT", "CELLHEIGHTSTD"])

        if "GCDF" not in kwargs:
            kwargs["GCDF"] = "DEG"
        if "MTRLGY" not in kwargs:
            kwargs["MTRLGY"] = "MET"
        if "CELLLOCCFGTYPE" not in kwargs:
            kwargs["CELLLOCCFGTYPE"] = "CELL_ANTENNA"
        self.add_moc("USMLCCELL", **kwargs)
        return error_count

    @API_RECORD
    def create_IPPOOLPM(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["ANI", "ITFT", "PHB"])
        if "PMPRD" not in kwargs:
            kwargs["PMPRD"] = 1
        if "LOSTPKTDETECTSW" not in kwargs:
            kwargs["LOSTPKTDETECTSW"] = 0
        if "DR" not in kwargs:
            if kwargs["ITFT"] == "IUB":
                kwargs["DR"] = "BOTH"
            else:
                kwargs["DR"] = "SOURCE"
        if "SIPTYPE" not in kwargs:
            kwargs["SIPTYPE"] = "ADJNODE_BIND_SIP"
        self.add_moc("IPPOOLPM", **kwargs)
        return error_count

    @API_RECORD
    def create_BSCIPPATH(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["ANI","PATHID","PATHT","IPADDR","PEERIPADDR"])
        if "ISEGBTS" not in kwargs:
            kwargs["ISEGBTS"] = MODEL.IPPATH.ISEGBTS.YES
        if "ISEGBTS" == "No":
            kwargs["CNMNGMODE"] =MODEL.IPPATH.CNMNGMODE.SHARE
        if "ITFT" not in kwargs:
            kwargs["ITFT"] = MODEL.IPPATH.ITFT.ABIS
        if "TXBW" not in kwargs:
            kwargs["TXBW"] = 100000
        if "RXBW" not in kwargs:
            kwargs["RXBW"] = 100000
        if "REMARK" not in kwargs:
            kwargs["REMARK"] = "-"
        if "CARRYFLAG" not in kwargs:
            kwargs["CARRYFLAG"] = MODEL.IPPATH.CARRYFLAG.NULL
        if "TRMLOADTHINDEX" not in kwargs:
            kwargs["TRMLOADTHINDEX"] = 2
        if "VLANFLAG" not in kwargs:
            kwargs["VLANFLAG"] = MODEL.IPPATH.VLANFLAG.DISABLE
        if "PATHCHK" not in kwargs:
            kwargs["PATHCHK"] = MODEL.IPPATH.PATHCHK.DISABLED
        if "ABISLNKBKFLAG" not in kwargs:
            kwargs["ABISLNKBKFLAG"] = MODEL.IPPATH.ABISLNKBKFLAG.OFF
        if "BLKSTATUS" not in kwargs:
            kwargs["BLKSTATUS"] =MODEL.IPPATH.BLKSTATUS.UNBLOCKED
        self.add_moc("IPPATH", **kwargs)
        return error_count

    @API_RECORD
    def create_eGBTS_Node(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["BTSID", "BTSNAME", "ANI"])
        if "LOGICRNCID" not in kwargs:
            kwargs["LOGICRNCID"] = 0
        if "BTSTYPE" not in kwargs:
            kwargs["BTSTYPE"] = MODEL.BTS.BTSTYPE.EGBTS
        self.add_moc("BTS", **kwargs)
        if "TRANSMODE" not in kwargs:
            kwargs["TRANSMODE"] = MODEL.BTSTRANS.TRANSMODE.TER_TRANS
        self.add_moc("BTSTRANS",**kwargs)
        if "NODET" not in kwargs:
            kwargs["NODET"] = MODEL.ADJNODE.NODET.ABIS
        if "IPPOOLINDEX" not in kwargs:
            kwargs["IPPOOLINDEX"] = 0
        if "TXBW" not in kwargs:
            kwargs["TXBW"] = 100000
        if "RXBW" not in kwargs:
            kwargs["RXBW"] = 100000
        kwargs["NAME"] = kwargs["BTSNAME"]
        self.add_moc("ADJNODE", **kwargs)
        if "FTI" not in kwargs:
            kwargs["FTI"] = 0
        if "TMIGLD" not in kwargs:
            kwargs["TMIGLD"] = 10
        if "ITFT" not in kwargs:
            kwargs["ITFT"] = MODEL.ADJMAP.ITFT.ABIS
        self.add_moc("ADJMAP", **kwargs)
        return error_count

    @API_RECORD
    def create_eGBTS_OAM(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["BTSID", "BTSNAME", "OAMIP"])
        self.add_moc("BTSOAMIP", **kwargs)
        return error_count

    @API_RECORD
    def create_eGBTS_ABISCP(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["BTSID", "LOCIP1", "PEERIP1", "PEERPN"])
        if "LOGICRNCID" not in kwargs:
            kwargs["LOGICRNCID"] = 0
        if "SCTPLNKID" not in kwargs:
            kwargs["SCTPLNKID"] = self.get_free_id_list("SCTPLNK","SCTPLNKID").pop(0)
        if "REMARK" not in kwargs:
            kwargs["REMARK"] = "For " + kwargs["BTSID"]
        if "LOGPORTFLAG" not in kwargs:
            kwargs["LOGPORTFLAG"] = MODEL.SCTPLNK.LOGPORTFLAG.NO
        if "APP" not in kwargs:
            kwargs["APP"] = MODEL.SCTPLNK.APP.ABISCP
        if "MODE" not in kwargs:
            kwargs["MODE"] = MODEL.SCTPLNK.MODE.SERVER
        if "SPECIFYLOCPNFLAG" not in kwargs:
            kwargs["SPECIFYLOCPNFLAG"] = MODEL.SCTPLNK.SPECIFYLOCPNFLAG.NO
        if "MTU" not in kwargs:
            kwargs["MTU"] = 1500
        peerport_list = kwargs["PEERPN"].split(";")
        i = 0
        for kwargs["PEERPN"] in peerport_list:
            if "SCTPLNKID" not in kwargs:
                kwargs["SCTPLNKID"] = self.get_free_id_list("SCTPLNK", "SCTPLNKID").pop(0)
            if i != 0:
                kwargs["SCTPLNKID"] = int(kwargs["SCTPLNKID"]) + 1
            kwargs["PEERPN"] = int(kwargs["PEERPN"])
            self.add_moc("SCTPLNK", **kwargs)
            self.add_moc("ABISCP", **kwargs)
            i += 1
        return error_count

    @API_RECORD
    def create_GCELL(self, with_trx=True,**kwargs):
        # Mandatory parameters must be included
        error_count = self.inner_check_para(kwargs, ["BTSID", "CELLID", "CELLNAME", "MCC", "MNC", "LAC","BCC", "NCC"])
        if "TemplateName" not in kwargs:
            kwargs["TemplateName"] = "Default 2G Cell Template"
        gcell_template = self.get_data_from_template(kwargs["TemplateName"], "GCELL", with_child=True)[0]
        for field_name in gcell_template.get_field_names():
            if field_name not in kwargs:
                kwargs[field_name] = gcell_template.get(field_name)
        if "LOGICRNCID" not in kwargs:
            kwargs["LOGICRNCID"] = 0
        # Add some option parameters if not included
        if "EGBTSPOWT" not in kwargs:
            kwargs["EGBTSPOWT"] = 430
        if "POWL" not in kwargs:
            kwargs["POWL"] = 0
        if "RA" not in kwargs:
            kwargs["RA"] = 0
        if "BCCHTYPE" not in kwargs:
            kwargs["BCCHTYPE"] = MODEL.TRXINFO.BCCHTYPE.field("MBCCH")
        if "CBCHTYPE" not in kwargs:
            kwargs["CBCHTYPE"] = MODEL.TRXINFO.CBCHTYPE.field("Not Support")
        if "TSC" not in kwargs:
            kwargs["TSC"] = kwargs["BCC"]
        if "BCHNUM" not in kwargs:
            kwargs["BCHNUM"] = 0
        # GCELL start
        # 先造个GCELL对象，再把template和GCELL相关的配置都读出来，然后合并到一起

        gcell_obj = MODEL.GCELL(**kwargs)
        new_gcell_obj = self.save_data_with_template([gcell_obj], gcell_template)[0]
        # 处理GCELL相关的子对象，找到子对象，如果子对象的子参数在kwargs里面存在就赋值过去
        gcell_obj_dict = vars(new_gcell_obj)
        for sub_name, sub_obj_list in gcell_obj_dict.items():
            if type(sub_obj_list) is list and len(sub_obj_list) > 0:
                sub_obj = sub_obj_list[0]
                sub_obj_dict = vars(sub_obj)
                for key, value in sub_obj_dict.items():
                    if key in kwargs and kwargs[key] != None:
                        setattr(sub_obj, key, kwargs[key])

        # 保存GCELL和其相关的子对象
        self.save_moc("GCELL", [new_gcell_obj], APPEND_MODE, with_child=True, with_merge=True)
        # GCELL end

        # TRX
        if with_trx:
            if "NONBCCHFREQLIST" not in kwargs or kwargs["NONBCCHFREQLIST"] is None or len(kwargs["NONBCCHFREQLIST"]) == 0:  # BCCH
                kwargs["NONBCCHFREQLIST"] = ""
                kwargs["HOPMODE"] = "NO_FH"  # Not FREQ HOPPING
                kwargs["TXNUM"] = 1
            else:
                kwargs["NONBCCHFREQLIST"] = kwargs["NONBCCHFREQLIST"].replace(";",",")
            self.add_moc("TRXINFO", **kwargs)
            self.add_moc("GTRXDEV", **kwargs)
            if kwargs["HOPMODE"] != "NO_FH":
                self.add_moc("GCELLMAGRP", **kwargs)
        # GCELLOSPMAP
        self.add_moc("GCELLOSPMAP", **kwargs)
        # PTPBVC
        bvci_list = kwargs["BVCI"].replace(",",";").split(";")
        nsei_list = kwargs["NSEI"].replace(",",";").split(";")
        if len(bvci_list) != len(nsei_list):
            if len(bvci_list) == 1:
                bvci_list = bvci_list * len(nsei_list)
            elif len(nsei_list) == 1:
                nsei_list = nsei_list * len(bvci_list)
            else:
                error_count += 1
            pass
        else: pass

        while bvci_list:
            kwargs["BVCI"] = int(bvci_list.pop(0))
            kwargs["NSEI"] = int(nsei_list.pop(0))
            self.add_moc("PTPBVC", **kwargs)

        return  error_count

    @API_RECORD
    def create_GCELLLCS(self, **kwargs):
        error_count = self.inner_check_para(kwargs, ["CELLID", "INPUTMD", "NSLATI", "LATIINT", "LATIDECI",
                                                     "WELONGI", "LONGIINT", "LONGIDECI"])
        if "INPUTMD" not in kwargs:
            kwargs["INPUTMD"] = MODEL.GCELLLCS.INPUTMD.Degree
        if "NSLATI" not in kwargs:
            kwargs["NSLATI"] = MODEL.GCELLLCS.NSLATI.South_latitude
        if "WELONGI" not in kwargs:
            kwargs["WELONGI"] = MODEL.GCELLLCS.WELONGI.East_Longitude
        self.add_moc("GCELLLCS", **kwargs)
        return error_count

    @API_RECORD
    def modify_RNC_RF_Para(self, result_row, rf_para_setting_dict, report_value_invalid=True):
        if "Result" not in result_row:
            result_row["Result"] = "Success"
        logicrncid = result_row["LOGICRNCID"]
        ucellid = int(result_row["CELLID"])
        cell_obj_list = self.get_moc("UCELL", WHERE(LOGICRNCID=logicrncid, CELLID=ucellid))
        if len(cell_obj_list) == 0:
            result_row["Detail"] = "Error: CELLID=%s is not exist" % (ucellid)
            result_row["Result"] = "Fail"
            return False

        result_row["CellName"] = cell_obj_list[0].CELLNAME
        result_row["Detail"] = ""

        for (MO, para_list) in rf_para_setting_dict.items():
            mo_class = CVT_CLASS(MO)  # 获得mo对应的类
            if mo_class is None:
                msg = "Error: MO=%s is not exist. Please check\n" % (MO)
                result_row["Detail"] += msg
                print(msg)
                result_row["Result"] = "Fail"
                continue
            mo = CVT_CLASS_NAME(MO)  # 转为标准名称
            big_para_name_list = [s.upper() for s in copy.deepcopy(mo_class._field_names_)]
            for (parameter, target_value, default_value, key_para_name) in para_list:
                # 输出Excel的Title
                key_para_dict = {}
                if key_para_name:
                    output_excel_title = "%s\n%s\n(%s)" % (MO, parameter, key_para_name)
                    if "=" not in key_para_name:
                        result_row[output_excel_title] += "KeyPara Invalid"
                        result_row["Result"] = "Partial Fail"
                        continue
                    else:
                        invalid_key_para = False
                        tmp_list = key_para_name.split(",")
                        for tmp_name in tmp_list:
                            key_para_name, key_para_value = tmp_name.split("=")
                            key_para_name = key_para_name.upper().strip()
                            if key_para_name not in big_para_name_list:
                                result_row[output_excel_title] = "KeyPara Invalid"
                                print("Error: MO=%s, KeyPara=%s is invalid" % (mo, key_para_name))
                                result_row["Result"] = "Partial Fail"
                                invalid_key_para = True
                                break
                            else:
                                key_para_name = mo_class._field_names_[big_para_name_list.index(key_para_name)]
                                key_para_value = int(key_para_value)  # !!! KeyPara只支持整数类型
                                key_para_dict[key_para_name] = key_para_value
                        if invalid_key_para is True:  # 存在参数错误
                            continue
                    pass
                else:
                    output_excel_title = "%s\n%s" % (MO, parameter)
                    pass
                # 获取满足条件的mo
                if hasattr(mo_class, "LOGICRNCID"):
                    key_para_dict["LOGICRNCID"] = logicrncid
                if hasattr(mo_class, "CELLID"):
                    key_para_dict["CELLID"] = ucellid
                if hasattr(mo_class, "NODEBID"):
                    key_para_dict["NODEBID"] = result_row["NODEBID"]
                if hasattr(mo_class, "NODEBNAME"):
                    key_para_dict["NODEBNAME"] = result_row["NodeBName"]
                mo_obj_list = self.get_moc(mo, WHERE(**key_para_dict))

                if len(mo_obj_list) == 0:
                    if key_para_name: # 如果输入了KeyPara，且原先不存在，则创建
                        obj = mo_class(**key_para_dict)
                        mo_obj_list = [obj]
                    else:
                        result_row["Detail"] += "Warning: CELLID=%s has no MO=%s data. Please check\n" % (ucellid, mo)
                        result_row["Result"] = "Partial Fail"
                        continue

                if target_value is None:
                    target_value = default_value
                if ":" in parameter:  # 修改bit参数
                    para_name, switch_name = parameter.split(":", 1)
                else:
                    para_name, switch_name = parameter, None
                para_name = para_name.upper().strip()
                if para_name not in big_para_name_list:
                    result_row[output_excel_title] = "Para Invalid"
                    print("Error: MO=%s, Para=%s is invalid" % (mo, para_name))
                    result_row["Result"] = "Partial Fail"
                    continue
                para_name = mo_class._field_names_[big_para_name_list.index(para_name)]
                para_class = getattr(mo_class, para_name)
                para_value = getattr(mo_obj_list[0], para_name)  # 得到当前参数的值

                if para_class.typeName == "BitDomain":  #Bit类型
                    if switch_name is None:
                        result_row[output_excel_title] = "Switch Invalid"
                        print("Error: MO=%s, Para=%s, Switch=None is invalid" % (mo, para_name))
                        result_row["Result"] = "Partial Fail"
                        continue
                    switch_name = switch_name.upper().strip()
                    big_switch_name_list = [s.upper() for s in copy.deepcopy(para_class._field_keys_)]
                    if switch_name not in big_switch_name_list:
                        result_row[output_excel_title] = "Switch Invalid"
                        print("Error: MO=%s, Para=%s, Switch=%s is invalid" % (mo, para_name, switch_name))
                        result_row["Result"] = "Partial Fail"
                        continue
                    switch_name = para_class._field_keys_[big_switch_name_list.index(switch_name)]
                    # 得到 当前开关的值
                    switch_bit = getattr(para_class, switch_name)
                    if para_value is None:
                        para_value = 0
                    elif type(para_value) is str:  # 把字符串
                        para_value = para_class.fromString(para_value)
                    switch_value = para_value & (1 << switch_bit)
                    switch_value = "OFF" if switch_value == 0 else "ON"
                    target_switch_value = target_value.upper().strip()
                    if switch_value == target_switch_value:
                        result_row[output_excel_title] = "%s" % (switch_value)
                        continue
                    else:
                        if target_switch_value not in ["ON", "OFF", "PERMIT", "NOT_PERMIT", "CFG", "NOT_CFG", "1", "0"]:
                            result_row[output_excel_title] = "Value Invalid(%s)" % (target_switch_value)
                            result_row["Result"] = "Partial Fail"
                            continue
                        result_row[output_excel_title] = "%s->%s" % (switch_value, target_switch_value)

                        if target_switch_value in ["ON", "PERMIT", "CFG", "1"]:
                            new_para_value = para_value | (1 << switch_bit)
                        else:
                            new_para_value = para_value & (~(1 << switch_bit))
                    pass
                else:  # 非比特类型
                    if para_class.typeName == "Enum" and len(target_value) > 0:  # 枚举类型
                        para_value = para_class.toString(para_value)  # 把整数值转换为枚举类型
                        tmp_big_list = [s.upper() for s in para_class._field_names_]
                        if target_value.upper() not in tmp_big_list:  # 判断输入的是否是有效的值。对无效值报错
                            if report_value_invalid is True:
                                result_row[output_excel_title] = "Value Invalid(%s)" % (target_value)
                                result_row["Result"] = "Partial Fail"
                            else:
                                result_row[output_excel_title] = "skip"
                            continue
                        else:
                            target_value = para_class._field_names_[tmp_big_list.index(target_value.upper())]
                    elif para_class.typeName == "List":  # 如果是列表，不设置
                        if report_value_invalid is True:
                            result_row[output_excel_title] = "Para Type Invalid(List)"
                            result_row["Result"] = "Partial Fail"
                        else:
                            result_row[output_excel_title] = "skip"
                        continue
                    elif para_class.typeName == "IpV4":  # IPV4类型，不设置
                        para_value = para_class.toString(para_value)
                    elif para_class.typeName in ["UnsignedLong", "Long"]:
                        try:
                            target_value = int(target_value)
                        except:
                            result_row[output_excel_title] = "Value Invalid(%s)" % (target_value)
                            result_row["Result"] = "Partial Fail"
                            continue
                        target_value = int(target_value)
                    elif para_class.typeName in ["String", "DateTime", "Time"]:
                        pass
                    else:
                        if report_value_invalid is True:
                            result_row[output_excel_title] = "Para Type Invalid(%s)" % (para_class.typeName)
                            result_row["Result"] = "Partial Fail"
                        else:
                            result_row[output_excel_title] = "skip"
                        continue

                    if para_value == target_value:
                        result_row[output_excel_title] = "%s" % para_value
                        continue
                    else:
                        result_row[output_excel_title] = "%s->%s" % (para_value, target_value)
                        new_para_value = target_value
                    pass
                # 修改值
                mo_obj_list = UPDATE_DATA(mo_obj_list, MOD(lambda o: setattr(o, para_name, new_para_value)))
                mo_obj_list = CVT_OBJ(mo, mo_obj_list)
                self.save_moc(mo, mo_obj_list, APPEND_MODE, with_merge=True)
                pass
            pass
        pass

    @API_RECORD
    def clear_ATM_Transformation_by_site(self,ne_name):
        nodeb_id = self.get_para_list_from_moc("NODEB", "NODEBID", WHERE(NODEBNAME=ne_name))[0]
        nodeb_ani = int(self.get_moc("ADJNODE", WHERE(NODEBID=nodeb_id))[0].ANI)
        nodeb_srn = self.get_moc("AAL2PATH", WHERE(ANI=nodeb_ani))[0].CARRYF
        nodeb_sn = self.get_moc("AAL2PATH", WHERE(ANI=nodeb_ani))[0].CARRYSN
        nodeb_imagrpn = self.get_moc("AAL2PATH", WHERE(ANI=nodeb_ani))[0].CARRYIMAGRPN
        rnc_ip = self.get_moc("IPPATH", WHERE(ANI=nodeb_ani))[0].IPADDR
        nodeb_ip = self.get_moc("IPPATH", WHERE(ANI=nodeb_ani))[0].PEERIPADDR

        # del moc
        self.del_moc("SAALLNK", WHERE(CARRYSRN=nodeb_srn, CARRYSN=nodeb_sn, CARRYIMAGRPN=nodeb_imagrpn))
        self.del_moc("AAL2PATH", WHERE(ANI=nodeb_ani))
        self.del_moc("AAL2RT", WHERE(ANI=nodeb_ani))
        self.del_moc("IPPM", WHERE(ANI=nodeb_ani))
        self.del_moc("IMAGRP", WHERE(SRN=nodeb_srn, SN=nodeb_sn, IMAGRPN=nodeb_imagrpn))
        self.del_moc("IMALNK", WHERE(SRN=nodeb_srn, SN=nodeb_sn, IMAGRPN=nodeb_imagrpn))

        ipoapvc_peeripaddr_para_list = self.get_para_list_from_moc("IPOAPVC", ["PEERIPADDR"],WHERE(CARRYSN=nodeb_sn,CARRYIMAGRPN=nodeb_imagrpn))
        self.del_moc("IPOAPVC", WHERE(CARRYSN=nodeb_sn, CARRYIMAGRPN=nodeb_imagrpn))
        for ip in ipoapvc_peeripaddr_para_list:
            self.del_moc("IPRT", WHERE(NEXTHOP=ip))

        return nodeb_id, nodeb_ani, rnc_ip, nodeb_ip

    @API_RECORD
    def modify_GCELL_CELLID(self, ne_tree, old_id, new_id):
        self.print_msg("Info: Modify GCELL CELLID from %d to %d" % (old_id, new_id))
        moc_list = MODEL.GCELL.get_child_names(True)
        for moc in moc_list:
            if hasattr(ne_tree, moc) == False: continue
            if len(ne_tree[moc]) == 0: continue
            moc_class = getattr(MODEL, moc)
            if hasattr(moc_class, "GCELL"):
                ne_tree[moc] = self.get_moc_list_by_mod(ne_tree[moc], MOD(CELLID=new_id).WHERE(CELLID=old_id), is_new=True)

    @API_RECORD
    def switch_and_or(self, switch, on_list=None, off_list=None, bit_num=None):
        bit_off = (1 << bit_num) - 1
        if off_list != None:
            for num in off_list:
                tmp_num = 1 << num
                bit_off = bit_off ^ tmp_num

        bit_on = 0
        if on_list != None:
            for num in on_list:
                tmp_num = 1 << num
                bit_on += tmp_num

        return (int(switch) & bit_off) | bit_on

    pass

