# coding=utf-8
try:
    from CommonClass.AAA_BTSObject import *
except:
    pass

def change_switch(switch,parameter_class,config_value,Target_Value):
    if str(config_value).isdigit():
        config_string = parameter_class.toString(int(config_value))
        configure_string = "0"
        if switch not in config_string:
            config_value = "switch not exist"
            Target_Value = "switch not exist"
        elif Target_Value not in config_string:
            if Target_Value[-1] == "0":
                configure_string = config_string.replace(
                    Target_Value[:-1] + "1", Target_Value)
                config_value = Target_Value[:-1] + "1"

            else:
                configure_string = config_string.replace(
                    Target_Value[:-1] + "0", Target_Value)
                config_value = Target_Value[:-1] + "0"
        else:
            configure_string = Target_Value
            config_value = Target_Value
    else:
        configure_string = config_value
        if switch not in config_value:
            config_value = "switch not exist"
            Target_Value = "switch not exist"
        elif Target_Value not in configure_string:
            if Target_Value[-1] == "0":
                configure_string = configure_string.replace(
                    Target_Value[:-1] + "1", Target_Value)
                config_value = Target_Value[:-1] + "1"
            else:
                configure_string = configure_string.replace(
                    Target_Value[:-1] + "0", Target_Value)
                config_value = Target_Value[:-1] + "0"
        else:
            config_value = Target_Value
    return configure_string, config_value,Target_Value
def change_parameter(parameter_class,config_value,Target_Value):
    if Target_Value.isdigit():
        current_config_value = config_value
        if str(config_value)[0] == "-":
            pass
        elif not str(config_value).isdigit() and ":" not in str(config_value):
            current_config_value = str(parameter_class.fromString(config_value))
    elif ":" in Target_Value or "TELCEL" in Target_Value or "-" in Target_Value:
        current_config_value = config_value
    else:
        current_config_value = config_value
        if str(config_value).isdigit():
            current_config_value = parameter_class.toString(int(config_value))
    return current_config_value

def change_parameters(switch,MO,Parameter,id,config_value,Target_Value,parameter_modify,Technology,id_parameter,
                      parameter_filter):
    if switch:
        mo_class = getattr(MODEL, MO)
        parameter_class = getattr(mo_class, Parameter)
        configure_string, config_value,Target_Value = change_switch(switch,parameter_class, config_value, Target_Value)
        parameter_modify[Parameter] = configure_string
    else:
        mo_class = getattr(MODEL, MO)
        parameter_class = getattr(mo_class, Parameter)
        config_value = change_parameter(parameter_class, config_value,Target_Value)
        parameter_modify[Parameter] = Target_Value

    if str(config_value) != Target_Value and config_value != "switch not exist":
        x = parameter_modify
        y = copy.deepcopy(parameter_filter)
        bts_obj.mod_moc(MO, MOD(**x).WHERE(**y), is_new=True)

def cidr_to_netmask(cidr):
    """
    将 CIDR 位数转换为点分十进制子网掩码。
    """
    if not (0 <= cidr <= 32):
        raise ValueError("CIDR 值必须在 0 到 32 之间")

    # 构造 32 位的二进制字符串（包含 1 和 0）
    binary_mask = '1' * cidr + '0' * (32 - cidr)

    # 将 32 位二进制字符串分成 8 位一组
    octets = [binary_mask[i:i+8] for i in range(0, 32, 8)]

    # 将每组 8 位二进制转换为十进制
    netmask_octets = [str(int(octet, 2)) for octet in octets]

    # 组合成点分十进制格式
    return ".".join(netmask_octets)
def nr_tx_expansion(nr_ip):
    if region=="AMBA":
        tp_5gcp_ip = MODEL.IPV4.fromString(nr_ip.attr("TA_S1CP_5G"))
        tp_5gcp_mask = nr_ip.attr("TA_S1CP_5G_MASK")
        if tp_5gcp_mask.isdigit():
            tp_5gcp_mask = cidr_to_netmask(int(tp_5gcp_mask))
        tp_5gcp_gw = MODEL.IPV4.fromString(nr_ip.attr("TA_S1CP_5G_GW"))
        tp_5gcp_vlan = nr_ip.attr("TA_S1CP_5G_VLAN")
        tp_5gup_ip = MODEL.IPV4.fromString(nr_ip.attr("TA_S1UP_5G"))
        tp_5gup_mask = nr_ip.attr("TA_S1UP_5G_MASK")
        if tp_5gup_mask.isdigit():
            tp_5gup_mask = cidr_to_netmask(int(tp_5gup_mask))
        tp_5gup_gw = MODEL.IPV4.fromString(nr_ip.attr("TA_S1UP_5G_GW"))
        tp_5gup_vlan = nr_ip.attr("TA_S1UP_5G_VLAN")

        if tp_5gcp_ip and tp_5gcp_ip not in ip_configure_list:
            bts_obj.add_moc("DEVIP", CN=0, SRN=0, SN=7, SBT=0, PT=devip_type, PN=devip_port, IP=tp_5gcp_ip,
                            MASK=tp_5gcp_mask,
                            USERLABEL="S1CP_5G", VRFIDX=0)
            if tp_5gcp_gw not in vlan_confiure_list:
                bts_obj.add_moc("VLANMAP", VRFIDX=0, NEXTHOPIP=tp_5gcp_gw, MASK=tp_5gcp_mask, VLANMODE=0,
                                VLANID=tp_5gcp_vlan, SETPRIO=0)
            ta_5gcp_srciprtid = 5
            if 5 in bts_obj.get_para_list_from_moc("SRCIPRT", "SRCRTIDX"):
                ta_5gcp_srciprtid = bts_obj.get_free_id_list("SRCIPRT", "SRCRTIDX")[0]
            if tp_5gcp_ip not in srciprt_configure_list:
                bts_obj.add_moc("SRCIPRT", SRCRTIDX=ta_5gcp_srciprtid, CN=0, SRN=0, SN=7, SBT=0, SRCIP=tp_5gcp_ip,
                            RTTYPE=0,
                            NEXTHOP=tp_5gcp_gw, PREF=60, USERLABEL="S1CP_5G")
            bts_obj.add_moc("DEVIP", CN=0, SRN=0, SN=7, SBT=0, PT=devip_type, PN=devip_port, IP=tp_5gup_ip,
                            MASK=tp_5gup_mask,
                            USERLABEL="S1UP_5G", VRFIDX=0)
            if tp_5gup_gw not in vlan_confiure_list:
                bts_obj.add_moc("VLANMAP", VRFIDX=0, NEXTHOPIP=tp_5gup_gw, MASK=tp_5gup_mask, VLANMODE=1,
                                VLANGROUPNO=2)
                if not bts_obj.get_para_list_from_moc("VLANCLASS", "VLANGROUPNO", WHERE(VLANGROUPNO=2)):
                    bts_obj.add_moc("VLANCLASS", VLANGROUPNO=2, TRAFFIC=3, VLANID=tp_5gup_vlan, SRVPRIO="", VLANPRIO=5)
                    bts_obj.add_moc("VLANCLASS", VLANGROUPNO=2, TRAFFIC=0, VLANID=tp_5gup_vlan, SRVPRIO="0",
                                    VLANPRIO=0)
                    bts_obj.add_moc("VLANCLASS", VLANGROUPNO=2, TRAFFIC=0, VLANID=tp_5gup_vlan, SRVPRIO="18",
                                    VLANPRIO=2)
                    bts_obj.add_moc("VLANCLASS", VLANGROUPNO=2, TRAFFIC=0, VLANID=tp_5gup_vlan, SRVPRIO="46",
                                    VLANPRIO=5)
                ta_5gup_srciprtid = 6
                if 6 in bts_obj.get_para_list_from_moc("SRCIPRT", "SRCRTIDX"):
                    ta_5gup_srciprtid = bts_obj.get_free_id_list("SRCIPRT", "SRCRTIDX")[0]
                if tp_5gup_ip not in srciprt_configure_list:
                    bts_obj.add_moc("SRCIPRT", SRCRTIDX=ta_5gup_srciprtid, CN=0, SRN=0, SN=7, SBT=0, SRCIP=tp_5gup_ip,
                                RTTYPE=0,
                                NEXTHOP=tp_5gup_gw, PREF=60, USERLABEL="S1UP_5G")
        if tp_5gcp_ip and 200 not in bts_obj.get_para_list_from_moc("EPGROUP","EPGROUPID") and 201 not in bts_obj.get_para_list_from_moc("EPGROUP","EPGROUPID"):
            sctphost_id = 101
            if 101 in bts_obj.get_para_list_from_moc("SCTPHOST", "SCTPHOSTID"):
                sctphost_id = bts_obj.get_free_id_list("SCTPHOST", "SCTPHOSTID")[0]
            bts_obj.add_moc("SCTPHOST", SCTPHOSTID=sctphost_id, VRFIDX=0, IPVERSION="IPv4", SIGIP1V4=tp_5gcp_ip,
                            SIGIP1SECSWITCH=0,
                            SIGIP2V4="0.0.0.0", SIGIP2SECSWITCH=0, PN="36422", SCTPTEMPLATEID=1,
                            DTLSPOLICYID="NULL",
                            USERLABEL="5G_X2", SIMPLEMODESWITCH="SIMPLE_MODE_OFF")
            tp_5gup_id = 1
            if bts_obj.get_para_list_from_moc("USERPLANEHOST", "UPHOSTID", WHERE(LOCIPV4=tp_5gup_ip)):
                tp_5gup_id = bts_obj.get_para_list_from_moc("USERPLANEHOST", "UPHOSTID", WHERE(LOCIPV4=tp_5gup_ip))[
                    0]
            else:
                if 1 not in bts_obj.get_para_list_from_moc("USERPLANEHOST", "UPHOSTID"):
                    tp_5gup_id = bts_obj.get_free_id_list("USERPLANEHOST", "UPHOSTID")[0]
                bts_obj.add_moc("USERPLANEHOST", UPHOSTID=tp_5gup_id, VRFIDX=0, IPVERSION="IPv4",
                                LOCIPV4=tp_5gup_ip, IPSECSWITCH="DISABLE",
                                USERLABEL="5G_X2", FLAG="MASTER")
            bts_obj.add_moc("EPGROUP", EPGROUPID=200, VRFIDX=0, IPV6VRFIDX=0, PACKETFILTERSWITCH="DISABLE",
                            PACKETFILTERSWITCH6="DISABLE", USERLABEL="TMA_5G_X2", TYPEFLAG="COMMON",
                            LNKPFMSW="DISABLE",
                            STATICCHK="DISABLE", IPPMSWITCH="DISABLE", APPTYPE="NULL", IPVERPREFERENCE="IPv6",
                            SCTPHOSTREFS=[MODEL.EPGROUP.SCTPHOSTREFS(SCTPHOSTID=101)], SCTPPEERREFS=[],
                            USERPLANEHOSTREFS=[MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=tp_5gup_id)])
            bts_obj.add_moc("EPGROUP", EPGROUPID=20, VRFIDX=0, IPV6VRFIDX=0, PACKETFILTERSWITCH="DISABLE",
                            PACKETFILTERSWITCH6="DISABLE", USERLABEL="5G_S1", TYPEFLAG="COMMON", LNKPFMSW="DISABLE",
                            STATICCHK="DISABLE", IPPMSWITCH="DISABLE", APPTYPE="NULL", IPVERPREFERENCE="IPv6",
                            SCTPHOSTREFS=[], SCTPPEERREFS=[],
                            USERPLANEHOSTREFS=[MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=tp_5gup_id)])

        rsh_5gcp_ip = MODEL.IPV4.fromString(nr_ip.attr("TLF_S1CP_5G"))
        rsh_5gup_ip = MODEL.IPV4.fromString(nr_ip.attr("TLF_S1UP_5G"))
        rsh_5gup_mask = nr_ip.attr("TLF_S1UP_5G_MASK")
        if rsh_5gup_mask.isdigit():
            rsh_5gup_mask=cidr_to_netmask(int(rsh_5gup_mask))
        rsh_5gup_gw = MODEL.IPV4.fromString(nr_ip.attr("TLF_S1UP_5G_GW"))
        rsh_5gup_vlan = nr_ip.attr("TLF_S1UP_5G_VLAN")
        if rsh_5gcp_ip and rsh_5gcp_ip not in ip_configure_list:
            bts_obj.add_moc("DEVIP", CN=0, SRN=0, SN=7, SBT=0, PT=devip_type, PN=devip_port, IP=rsh_5gcp_ip, MASK=rsh_5gup_mask,
                            USERLABEL="RSH_5GCP", VRFIDX=0)
            tlf_5gcp_srciprtid = 12
            if 12 in bts_obj.get_para_list_from_moc("SRCIPRT", "SRCRTIDX"):
                tlf_5gcp_srciprtid = bts_obj.get_free_id_list("SRCIPRT", "SRCRTIDX")[0]
            if rsh_5gcp_ip not in srciprt_configure_list:
                bts_obj.add_moc("SRCIPRT", SRCRTIDX=tlf_5gcp_srciprtid, CN=0, SRN=0, SN=7, SBT=0, SRCIP=rsh_5gcp_ip, RTTYPE=0,
                            NEXTHOP=rsh_5gup_gw, PREF=60, USERLABEL="RSH_5GCP_TMA")

            bts_obj.add_moc("DEVIP", CN=0, SRN=0, SN=7, SBT=0, PT=devip_type, PN=devip_port, IP=rsh_5gup_ip, MASK=rsh_5gup_mask,
                            USERLABEL="RSH_5GUP_TMA", VRFIDX=0)
            if rsh_5gup_gw not in vlan_confiure_list:
                bts_obj.add_moc("VLANMAP", VRFIDX=0, NEXTHOPIP=rsh_5gup_gw, MASK=rsh_5gup_mask, VLANMODE=0, VLANID=rsh_5gup_vlan, SETPRIO=0)
            tlf_5gup_srciprtid = 13
            if 13 in bts_obj.get_para_list_from_moc("SRCIPRT", "SRCRTIDX"):
                tlf_5gup_srciprtid = bts_obj.get_free_id_list("SRCIPRT", "SRCRTIDX")[0]
            if rsh_5gup_ip not in srciprt_configure_list:
                bts_obj.add_moc("SRCIPRT", SRCRTIDX=tlf_5gup_srciprtid, CN=0, SRN=0, SN=7, SBT=0, SRCIP=rsh_5gup_ip, RTTYPE=0,NEXTHOP=rsh_5gup_gw, PREF=60, USERLABEL="RSH_5GUP")

        if rsh_5gcp_ip:
            rsh_sctphost_id = 103
            if rsh_sctphost_id in bts_obj.get_para_list_from_moc("SCTPHOST", "SCTPHOSTID"):
                rsh_sctphost_id = bts_obj.get_free_id_list("SCTPHOST", "SCTPHOSTID")[0]
            bts_obj.add_moc("SCTPHOST", SCTPHOSTID=rsh_sctphost_id, VRFIDX=0, IPVERSION="IPv4", SIGIP1V4=rsh_5gcp_ip,
                            SIGIP1SECSWITCH=0,
                            SIGIP2V4="0.0.0.0", SIGIP2SECSWITCH=0, PN="36422", SCTPTEMPLATEID=1,
                            DTLSPOLICYID="NULL",
                            USERLABEL="TMA_5G_X2", SIMPLEMODESWITCH="SIMPLE_MODE_OFF")

            if bts_obj.get_para_list_from_moc("USERPLANEHOST", "UPHOSTID", WHERE(LOCIPV4=rsh_5gup_ip)):
                rsh_5gup_id = \
                    bts_obj.get_para_list_from_moc("USERPLANEHOST", "UPHOSTID", WHERE(LOCIPV4=rsh_5gup_ip))[0]
            else:
                bts_obj.add_moc("USERPLANEHOST", UPHOSTID=9, VRFIDX=0, IPVERSION="IPv4",
                                LOCIPV4=rsh_5gup_ip, IPSECSWITCH="DISABLE",
                                USERLABEL="TMA_5G_X2", FLAG="MASTER")
                rsh_5gup_id = 9
            bts_obj.add_moc("EPGROUP", EPGROUPID=103, VRFIDX=0, IPV6VRFIDX=0, PACKETFILTERSWITCH="DISABLE",
                            PACKETFILTERSWITCH6="DISABLE", USERLABEL="TMA_5G_X2", TYPEFLAG="COMMON",
                            LNKPFMSW="DISABLE",
                            STATICCHK="DISABLE", IPPMSWITCH="DISABLE", APPTYPE="NULL", IPVERPREFERENCE="IPv6",
                            SCTPHOSTREFS=[MODEL.EPGROUP.SCTPHOSTREFS(SCTPHOSTID=rsh_sctphost_id)], SCTPPEERREFS=[],
                            USERPLANEHOSTREFS=[MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=rsh_5gup_id)])
            bts_obj.add_moc("EPGROUP", EPGROUPID=81, VRFIDX=0, IPV6VRFIDX=0, PACKETFILTERSWITCH="DISABLE",
                            PACKETFILTERSWITCH6="DISABLE", USERLABEL="TMA_5G_S1", TYPEFLAG="COMMON",
                            LNKPFMSW="DISABLE",
                            STATICCHK="DISABLE", IPPMSWITCH="DISABLE", APPTYPE="NULL", IPVERPREFERENCE="IPv6",
                            SCTPHOSTREFS=[], SCTPPEERREFS=[],
                            USERPLANEHOSTREFS=[MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=rsh_5gup_id)])
    elif region=="SUR":
        mvs_5gcp_ip = MODEL.IPV4.fromString(nr_ip.attr("TLF_S1CP_5G"))
        mvs_5gup_ip = MODEL.IPV4.fromString(nr_ip.attr("TLF_S1UP_5G"))
        mvs_5gup_mask = nr_ip.attr("TLF_S1UP_5G_MASK")
        if mvs_5gup_mask.isdigit():
            mvs_5gup_mask=cidr_to_netmask(int(mvs_5gup_mask))
        mvs_5gup_gw = MODEL.IPV4.fromString(nr_ip.attr("TLF_S1UP_5G_GW"))
        mvs_5gup_vlan = nr_ip.attr("TLF_S1UP_5G_VLAN")
        if mvs_5gcp_ip not in ip_configure_list:
            bts_obj.add_moc("DEVIP", CN=0, SRN=0, SN=7, SBT=0, PT=devip_type, PN=devip_port, IP=mvs_5gcp_ip, MASK=mvs_5gup_mask,
                            USERLABEL="5G_CP", VRFIDX=0)
            tlf_5gcp_srciprtid = 6
            if 6 in bts_obj.get_para_list_from_moc("SRCIPRT", "SRCRTIDX"):
                tlf_5gcp_srciprtid = bts_obj.get_free_id_list("SRCIPRT", "SRCRTIDX")[0]
            if mvs_5gcp_ip not in srciprt_configure_list:
                bts_obj.add_moc("SRCIPRT", SRCRTIDX=tlf_5gcp_srciprtid, CN=0, SRN=0, SN=7, SBT=0, SRCIP=mvs_5gcp_ip, RTTYPE=0,
                            NEXTHOP=mvs_5gup_gw, PREF=60, USERLABEL="5G_CP")

            bts_obj.add_moc("DEVIP", CN=0, SRN=0, SN=7, SBT=0, PT=devip_type, PN=devip_port, IP=mvs_5gup_ip, MASK=mvs_5gup_mask,
                            USERLABEL="5G_UP", VRFIDX=0)
            if mvs_5gup_gw not in vlan_confiure_list:
                bts_obj.add_moc("VLANMAP", VRFIDX=0, NEXTHOPIP=mvs_5gup_gw, MASK=mvs_5gup_mask, VLANMODE=0, VLANID=mvs_5gup_vlan, SETPRIO=0)
            tlf_5gup_srciprtid = 7
            if 7 in bts_obj.get_para_list_from_moc("SRCIPRT", "SRCRTIDX"):
                tlf_5gup_srciprtid = bts_obj.get_free_id_list("SRCIPRT", "SRCRTIDX")[0]
            if mvs_5gup_ip not in srciprt_configure_list:
                bts_obj.add_moc("SRCIPRT", SRCRTIDX=tlf_5gup_srciprtid, CN=0, SRN=0, SN=7, SBT=0, SRCIP=mvs_5gup_ip, RTTYPE=0,NEXTHOP=mvs_5gup_gw, PREF=60, USERLABEL="5G_UP")
        if 12 not in bts_obj.get_para_list_from_moc("SCTPHOST","SCTPHOSTID"):
            bts_obj.add_moc("SCTPHOST", SCTPHOSTID=12, VRFIDX=0, IPVERSION="IPv4", SIGIP1V4=mvs_5gcp_ip,
                            SIGIP1SECSWITCH=0,
                            SIGIP2V4="0.0.0.0", SIGIP2SECSWITCH=0, PN="36422", SCTPTEMPLATEID=1, DTLSPOLICYID="NULL",
                            USERLABEL="5G_X2", SIMPLEMODESWITCH="SIMPLE_MODE_OFF")
            if bts_obj.get_para_list_from_moc("USERPLANEHOST","UPHOSTID",WHERE(LOCIPV4=mvs_5gup_ip)):
                mvs_5gup_id=bts_obj.get_para_list_from_moc("USERPLANEHOST","UPHOSTID",WHERE(LOCIPV4=mvs_5gup_ip))[0]
            else:
                bts_obj.add_moc("USERPLANEHOST", UPHOSTID=1, VRFIDX=0, IPVERSION="IPv4",
                                LOCIPV4=mvs_5gup_ip, IPSECSWITCH="DISABLE",
                                USERLABEL="5G_X2", FLAG="MASTER")
                mvs_5gup_id=1
            bts_obj.add_moc("EPGROUP", EPGROUPID=12, VRFIDX=0, IPV6VRFIDX=0, PACKETFILTERSWITCH="DISABLE",
                            PACKETFILTERSWITCH6="DISABLE", USERLABEL="5G_X2", TYPEFLAG="COMMON", LNKPFMSW="DISABLE",
                            STATICCHK="DISABLE", IPPMSWITCH="DISABLE", APPTYPE="NULL", IPVERPREFERENCE="IPv6",
                            SCTPHOSTREFS=[MODEL.EPGROUP.SCTPHOSTREFS(SCTPHOSTID=12)],SCTPPEERREFS=[],
                            USERPLANEHOSTREFS=[MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=mvs_5gup_id)])
            bts_obj.add_moc("EPGROUP", EPGROUPID=11, VRFIDX=0, IPV6VRFIDX=0, PACKETFILTERSWITCH="DISABLE",
                            PACKETFILTERSWITCH6="DISABLE", USERLABEL="5G_S1", TYPEFLAG="COMMON", LNKPFMSW="DISABLE",
                            STATICCHK="DISABLE", IPPMSWITCH="DISABLE", APPTYPE="NULL", IPVERPREFERENCE="IPv6",
                            SCTPHOSTREFS=[],SCTPPEERREFS=[],
                            USERPLANEHOSTREFS=[MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=mvs_5gup_id)])

        rsh_5gcp_ip = MODEL.IPV4.fromString(nr_ip.attr("TA_S1CP_5G"))
        rsh_5gcp_mask = nr_ip.attr("TA_S1CP_5G_MASK")
        if rsh_5gcp_mask.isdigit():
            rsh_5gcp_mask=cidr_to_netmask(int(rsh_5gcp_mask))
        rsh_5gcp_gw = MODEL.IPV4.fromString(nr_ip.attr("TA_S1CP_5G_GW"))
        rsh_5gcp_vlan = nr_ip.attr("TA_S1CP_5G_VLAN")
        rsh_5gup_ip = MODEL.IPV4.fromString(nr_ip.attr("TA_S1UP_5G"))
        rsh_5gup_mask = nr_ip.attr("TA_S1UP_5G_MASK")
        if rsh_5gup_mask.isdigit():
            rsh_5gup_mask=cidr_to_netmask(int(rsh_5gup_mask))
        rsh_5gup_gw = MODEL.IPV4.fromString(nr_ip.attr("TA_S1UP_5G_GW"))
        rsh_5gup_vlan = nr_ip.attr("TA_S1UP_5G_VLAN")

        if rsh_5gcp_ip not in ip_configure_list:
            bts_obj.add_moc("DEVIP", CN=0, SRN=0, SN=7, SBT=0, PT=devip_type, PN=devip_port, IP=rsh_5gcp_ip,MASK=rsh_5gcp_mask,
                            USERLABEL="RSH_5GCP_TP", VRFIDX=0)
            if rsh_5gcp_gw not in vlan_confiure_list:
                bts_obj.add_moc("VLANMAP", VRFIDX=0, NEXTHOPIP=rsh_5gcp_gw, MASK=rsh_5gcp_mask, VLANMODE=0,VLANID=rsh_5gcp_vlan, SETPRIO=0)
            ta_5gcp_srciprtid=12
            if 12 in bts_obj.get_para_list_from_moc("SRCIPRT","SRCRTIDX"):
                ta_5gcp_srciprtid=bts_obj.get_free_id_list("SRCIPRT","SRCRTIDX")[0]
            if rsh_5gcp_ip not in srciprt_configure_list:
                bts_obj.add_moc("SRCIPRT", SRCRTIDX=ta_5gcp_srciprtid, CN=0, SRN=0, SN=7, SBT=0, SRCIP=rsh_5gcp_ip, RTTYPE=0,
                            NEXTHOP=rsh_5gcp_gw, PREF=60, USERLABEL="RSH_5GCP_TP")
            bts_obj.add_moc("DEVIP", CN=0, SRN=0, SN=7, SBT=0, PT=devip_type, PN=devip_port, IP=rsh_5gup_ip,MASK=rsh_5gup_mask,
                            USERLABEL="RSH_5GUP_TP", VRFIDX=0)
            if rsh_5gup_gw not in vlan_confiure_list:
                bts_obj.add_moc("VLANMAP", VRFIDX=0, NEXTHOPIP=rsh_5gup_gw, MASK=rsh_5gup_mask, VLANMODE=1, VLANGROUPNO=2)
                if not bts_obj.get_para_list_from_moc("VLANCLASS","VLANGROUPNO",WHERE(VLANGROUPNO=2)):
                    bts_obj.add_moc("VLANCLASS", VLANGROUPNO=2, TRAFFIC=3, VLANID=rsh_5gup_vlan,SRVPRIO="", VLANPRIO=5)
                    bts_obj.add_moc("VLANCLASS", VLANGROUPNO=2, TRAFFIC=0, VLANID=rsh_5gup_vlan, SRVPRIO="0", VLANPRIO=0)
                    bts_obj.add_moc("VLANCLASS", VLANGROUPNO=2, TRAFFIC=0, VLANID=rsh_5gup_vlan, SRVPRIO="18", VLANPRIO=2)
                    bts_obj.add_moc("VLANCLASS", VLANGROUPNO=2, TRAFFIC=0, VLANID=rsh_5gup_vlan, SRVPRIO="46", VLANPRIO=5)

            ta_5gup_srciprtid = 13
            if 13 in bts_obj.get_para_list_from_moc("SRCIPRT", "SRCRTIDX"):
                ta_5gup_srciprtid = bts_obj.get_free_id_list("SRCIPRT", "SRCRTIDX")[0]
            if rsh_5gup_ip not in srciprt_configure_list:
                bts_obj.add_moc("SRCIPRT", SRCRTIDX=ta_5gup_srciprtid, CN=0, SRN=0, SN=7, SBT=0, SRCIP=rsh_5gup_ip, RTTYPE=0,
                            NEXTHOP=rsh_5gup_gw, PREF=60, USERLABEL="RSH_5GUP_TP")
        if 13 not in bts_obj.get_para_list_from_moc("SCTPHOST", "SCTPHOSTID"):
            bts_obj.add_moc("SCTPHOST", SCTPHOSTID=81, VRFIDX=0, IPVERSION="IPv4", SIGIP1V4=rsh_5gcp_ip,
                            SIGIP1SECSWITCH=0,
                            SIGIP2V4="0.0.0.0", SIGIP2SECSWITCH=0, PN="36422", SCTPTEMPLATEID=1, DTLSPOLICYID="NULL",
                            USERLABEL="5G_X2_TP", SIMPLEMODESWITCH="SIMPLE_MODE_OFF")
            if bts_obj.get_para_list_from_moc("USERPLANEHOST", "UPHOSTID", WHERE(LOCIPV4=rsh_5gup_ip)):
                rsh_5gup_id = bts_obj.get_para_list_from_moc("USERPLANEHOST", "UPHOSTID", WHERE(LOCIPV4=rsh_5gup_ip))[0]
            else:
                bts_obj.add_moc("USERPLANEHOST", UPHOSTID=9, VRFIDX=0, IPVERSION="IPv4",
                                LOCIPV4=rsh_5gup_ip, IPSECSWITCH="DISABLE",
                                USERLABEL="5G_X2", FLAG="MASTER")
                rsh_5gup_id = 9
            bts_obj.add_moc("EPGROUP", EPGROUPID=81, VRFIDX=0, IPV6VRFIDX=0, PACKETFILTERSWITCH="DISABLE",
                            PACKETFILTERSWITCH6="DISABLE", USERLABEL="5G_X2_TP", TYPEFLAG="COMMON", LNKPFMSW="DISABLE",
                            STATICCHK="DISABLE", IPPMSWITCH="DISABLE", APPTYPE="NULL", IPVERPREFERENCE="IPv6",
                            SCTPHOSTREFS=[MODEL.EPGROUP.SCTPHOSTREFS(SCTPHOSTID=81)], SCTPPEERREFS=[],
                            USERPLANEHOSTREFS=[MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=rsh_5gup_id)])
            bts_obj.add_moc("EPGROUP", EPGROUPID=9, VRFIDX=0, IPV6VRFIDX=0, PACKETFILTERSWITCH="DISABLE",
                            PACKETFILTERSWITCH6="DISABLE", USERLABEL="5G_S1_TP", TYPEFLAG="COMMON", LNKPFMSW="DISABLE",
                            STATICCHK="DISABLE", IPPMSWITCH="DISABLE", APPTYPE="NULL", IPVERPREFERENCE="IPv6",
                            SCTPHOSTREFS=[], SCTPPEERREFS=[],
                            USERPLANEHOSTREFS=[MODEL.EPGROUP.USERPLANEHOSTREFS(UPHOSTID=rsh_5gup_id)])
def modify_lte_tx(lte_ip):
    lte_cp_old_ip = siteinfo.attr("old LTE CP IP")
    lte_up_old_ip = siteinfo.attr("old LTE UP IP")
    lte_cp_old_gw = siteinfo.attr("old LTE CP GW")
    lte_up_old_gw = siteinfo.attr("old LTE UP GW")
    if lte_cp_old_ip:
        lte_cp_old_ip = MODEL.IPV4.fromString(lte_cp_old_ip)
        lte_cp_old_gw = MODEL.IPV4.fromString(lte_cp_old_gw)
    if lte_up_old_ip:
        lte_up_old_ip = MODEL.IPV4.fromString(lte_up_old_ip)
        lte_up_old_gw = MODEL.IPV4.fromString(lte_up_old_gw)

    tp_5gcp_gw = MODEL.IPV4.fromString(lte_ip.attr("TA_S1CP_5G_GW"))
    tp_5gcp_vlan = lte_ip.attr("TA_S1CP_5G_VLAN")
    tp_5gup_gw = MODEL.IPV4.fromString(lte_ip.attr("TA_S1UP_5G_GW"))
    tp_5gup_vlan = lte_ip.attr("TA_S1UP_5G_VLAN")
    lte_cp_new_ip = MODEL.IPV4.fromString(lte_ip.attr("TA S1CP_LTE"))
    lte_up_new_ip = MODEL.IPV4.fromString(lte_ip.attr("TA S1UP_LTE"))

    bts_obj.mod_moc("IPRT", MOD(NEXTHOP=tp_5gcp_gw).WHERE(NEXTHOP=lte_cp_old_gw), is_new=True)
    bts_obj.mod_moc("IPRT", MOD(NEXTHOP=tp_5gup_gw).WHERE(NEXTHOP=lte_up_old_gw), is_new=True)
    bts_obj.mod_moc("IPCLKLNK",MOD(CIP=lte_cp_new_ip).WHERE(CIP=lte_cp_old_ip), is_new=True)
    bts_obj.mod_moc("IPCLKLNK", MOD(CIP=lte_up_new_ip).WHERE(CIP=lte_up_old_ip), is_new=True)

    bts_obj.mod_moc("SCTPHOST", MOD(SIGIP1V4=lte_cp_new_ip).WHERE(SIGIP1V4=lte_cp_old_ip), is_new=True)
    bts_obj.mod_moc("USERPLANEHOST", MOD(LOCIPV4=lte_up_new_ip).WHERE(LOCIPV4=lte_up_old_ip), is_new=True)
    bts_obj.mod_moc("TWAMPRESPONDER", MOD(LOCALIP=lte_cp_new_ip).WHERE(LOCALIP=lte_cp_old_ip), is_new=True)
    bts_obj.mod_moc("TWAMPRESPONDER", MOD(LOCALIP=lte_up_new_ip).WHERE(LOCALIP=lte_up_old_ip), is_new=True)
    srciprt_id_up=10
    srciprt_id_cp=11
    srciprt_des_up="RSH_4GUP_TP"
    srciprt_des_cp = "RSH_4GCP_TP"
    if region=="AMBA":
        srciprt_id_up = 1
        srciprt_id_cp = 2
        srciprt_des_up = "S1UP_LTE"
        srciprt_des_cp = "S1CP_LTE"
    if lte_up_old_ip in bts_obj.get_para_list_from_moc("SRCIPRT", "SRCIP"):
        bts_obj.mod_moc("SRCIPRT", MOD(SRCIP=lte_up_new_ip, NEXTHOP=tp_5gup_gw).WHERE(SRCIP=lte_up_old_ip),is_new=True)
    elif srciprt_id_up not in bts_obj.get_para_list_from_moc("SRCIPRT", "SRCRTIDX"):
        bts_obj.add_moc("SRCIPRT", SRCRTIDX=srciprt_id_up, CN=0, SRN=0, SN=7, SBT=0, SRCIP=lte_up_new_ip, RTTYPE=0,
                        NEXTHOP=tp_5gup_gw, PREF=60, USERLABEL=srciprt_des_up)
    else:
        bts_obj.add_moc("SRCIPRT", SRCRTIDX=bts_obj.get_free_id_list("SRCIPRT", "SRCRTIDX")[0], CN=0, SRN=0, SN=7,
                        SBT=0, SRCIP=lte_up_new_ip, RTTYPE=0,
                        NEXTHOP=tp_5gup_gw, PREF=60, USERLABEL=srciprt_des_up)
    if lte_cp_old_ip in bts_obj.get_para_list_from_moc("SRCIPRT", "SRCIP"):
        bts_obj.mod_moc("SRCIPRT", MOD(SRCIP=lte_cp_new_ip, NEXTHOP=tp_5gcp_gw).WHERE(SRCIP=lte_cp_old_ip),is_new=True)
    elif srciprt_id_cp not in bts_obj.get_para_list_from_moc("SRCIPRT", "SRCRTIDX"):
        bts_obj.add_moc("SRCIPRT", SRCRTIDX=srciprt_id_cp, CN=0, SRN=0, SN=7, SBT=0, SRCIP=lte_cp_new_ip, RTTYPE=0,
                        NEXTHOP=tp_5gcp_gw, PREF=60, USERLABEL=srciprt_des_cp)
    else:
        bts_obj.add_moc("SRCIPRT", SRCRTIDX=bts_obj.get_free_id_list("SRCIPRT", "SRCRTIDX")[0], CN=0, SRN=0, SN=7,
                        SBT=0, SRCIP=lte_cp_new_ip, RTTYPE=0,
                        NEXTHOP=tp_5gcp_gw, PREF=60, USERLABEL=srciprt_des_cp)

    bts_obj.mod_moc("DEVIP",
                    MOD(IP=lte_cp_new_ip, MASK="255.255.255.248", USERLABEL=srciprt_des_cp).WHERE(IP=lte_cp_old_ip),
                    is_new=True)
    bts_obj.mod_moc("DEVIP",
                    MOD(IP=lte_up_new_ip, MASK="255.255.255.248", USERLABEL=srciprt_des_up).WHERE(IP=lte_up_old_ip),
                    is_new=True)
    if tp_5gcp_vlan:
        bts_obj.mod_moc("VLANMAP", MOD(NEXTHOPIP=tp_5gcp_gw, MASK="255.255.255.248", VLANID=tp_5gcp_vlan).WHERE(
            NEXTHOPIP=lte_cp_old_gw),is_new=True)
    else:
        bts_obj.mod_moc("VLANMAP", MOD(NEXTHOPIP=tp_5gcp_gw, MASK="255.255.255.248").WHERE(NEXTHOPIP=lte_cp_old_gw),is_new=True)
    bts_obj.mod_moc("VLANMAP", MOD(NEXTHOPIP=tp_5gup_gw, MASK="255.255.255.248").WHERE(NEXTHOPIP=lte_up_old_gw),is_new=True)

    # mvs_lte_cpip= siteinfo.attr("old MVS LTE CP IP")
    # mvs_lte_cpgw = siteinfo.attr("old MVS LTE CP GW")
    # if mvs_lte_cpip:
    #     mvs_lte_cpip = MODEL.IPV4.fromString(mvs_lte_cpip)
    #     mvs_lte_cpgw = MODEL.IPV4.fromString(mvs_lte_cpgw)
    # mvs_new_cp_ip = MODEL.IPV4.fromString(lte_ip.attr("TA S1CP_LTE"))
    # lte_up_new_ip = MODEL.IPV4.fromString(lte_ip.attr("TA S1UP_LTE"))



def create_gnodeb_op():
    if region=="AMBA":
        bts_obj.set_moc("gNBOperator", OperatorId=0, OperatorName="PERSONAL_5G", Mcc="722", Mnc="34",
                        NrNetworkingOption="NSA", OperatorType="PRIMARY_OPERATOR", ReLicPercentage="255",
                        RrcConnUserLicPercentage="255", gNBIdLength="255", gNBId=gnodebid, CmasBroadcastSwitch="ON",
                        OperatorInterRatPolicySw="NSA_SA_DL_SEL_OPT_SW-0&NSA_SA_UL_SEL_OPT_SW-0",
                        RoamingPlmnFlag="FALSE", HplmnAlgoSwitch="VOICE_CAPB_MOB_TO_HPLMN_SW-0")
        bts_obj.add_moc("gNBOperator", OperatorId=2, OperatorName="Movistar_5G", Mcc="722", Mnc="07",
                        NrNetworkingOption="NSA", OperatorType="SECONDARY_OPERATOR", ReLicPercentage="255",
                        RrcConnUserLicPercentage="255", gNBIdLength="255", gNBId=gnodebid, CmasBroadcastSwitch="ON",
                        OperatorInterRatPolicySw="NSA_SA_DL_SEL_OPT_SW-0&NSA_SA_UL_SEL_OPT_SW-0",
                        RoamingPlmnFlag="FALSE", HplmnAlgoSwitch="VOICE_CAPB_MOB_TO_HPLMN_SW-0")

        bts_obj.set_moc("gNBTrackingArea",TrackingAreaId=0, Tac=tp_tacnr)
        if mvs_tacnr:
            bts_obj.add_moc("gNBTrackingArea", TrackingAreaId=3, Tac=mvs_tacnr)

        if 200 not in bts_obj.get_para_list_from_moc("EPGROUP","EPGROUPID") and 201 not in bts_obj.get_para_list_from_moc("EPGROUP","EPGROUPID"):
            bts_obj.set_moc("gNBCUS1", gNBCuS1Id=0, UpEpGroupId=20, UserLabel="5G_S1")
            bts_obj.set_moc("gNBCUX2", gNBCuX2Id=0, CpEpGroupId=200, UpEpGroupId=200)
        else:
            bts_obj.set_moc("gNBCUS1", gNBCuS1Id=0, UpEpGroupId=10, UserLabel="5G_S1")
            bts_obj.set_moc("gNBCUX2", gNBCuX2Id=0, CpEpGroupId=201, UpEpGroupId=201)
        bts_obj.add_moc("gNBCUS1", gNBCuS1Id=2, UpEpGroupId=81, UserLabel="TMA_5G_S1")
        bts_obj.add_moc("gNBCUX2", gNBCuX2Id=2, CpEpGroupId=103, UpEpGroupId=103)
        bts_obj.set_moc("gNBCUS1Op", gNBCuS1Id=0, OperatorId=0)
        bts_obj.add_moc("gNBCUS1Op", gNBCuS1Id=2, OperatorId=2)
        bts_obj.set_moc("gNBCUX2Op", gNBCuX2Id=0, OperatorId=0)
        bts_obj.add_moc("gNBCUX2Op", gNBCuX2Id=2, OperatorId=2)
    elif region=="SUR":
        bts_obj.set_moc("gNBOperator", OperatorId=0, OperatorName="Movistar_5G", Mcc="722", Mnc="07",
                        NrNetworkingOption="NSA", OperatorType="PRIMARY_OPERATOR", ReLicPercentage="255",
                        RrcConnUserLicPercentage="255", gNBIdLength="255", gNBId=gnodebid, CmasBroadcastSwitch="ON",
                        OperatorInterRatPolicySw="NSA_SA_DL_SEL_OPT_SW-0&NSA_SA_UL_SEL_OPT_SW-0",
                        RoamingPlmnFlag="FALSE", HplmnAlgoSwitch="VOICE_CAPB_MOB_TO_HPLMN_SW-0")
        bts_obj.add_moc("gNBOperator", OperatorId=2, OperatorName="PERSONAL_5G", Mcc="722", Mnc="34",
                        NrNetworkingOption="NSA", OperatorType="SECONDARY_OPERATOR", ReLicPercentage="255",
                        RrcConnUserLicPercentage="255", gNBIdLength="255", gNBId=gnodebid, CmasBroadcastSwitch="ON",
                        OperatorInterRatPolicySw="NSA_SA_DL_SEL_OPT_SW-0&NSA_SA_UL_SEL_OPT_SW-0",
                        RoamingPlmnFlag="FALSE", HplmnAlgoSwitch="VOICE_CAPB_MOB_TO_HPLMN_SW-0")
        bts_obj.set_moc("gNBTrackingArea", TrackingAreaId=3, Tac=tp_tacnr)
        if mvs_tacnr:
            bts_obj.add_moc("gNBTrackingArea", TrackingAreaId=0, Tac=mvs_tacnr)
        bts_obj.set_moc("gNBCUS1", gNBCuS1Id=0, UpEpGroupId=11, UserLabel="5G_S1")
        bts_obj.set_moc("gNBCUX2", gNBCuX2Id=0, CpEpGroupId=12, UpEpGroupId=12)
        bts_obj.add_moc("gNBCUS1", gNBCuS1Id=2, UpEpGroupId=9, UserLabel="5G_S1_TP")
        bts_obj.add_moc("gNBCUX2", gNBCuX2Id=2, CpEpGroupId=81, UpEpGroupId=81)
        bts_obj.set_moc("gNBCUS1Op", gNBCuS1Id=0, OperatorId=0)
        bts_obj.add_moc("gNBCUS1Op", gNBCuS1Id=2, OperatorId=2)
        bts_obj.add_moc("gNBCUX2Op", gNBCuX2Id=0, OperatorId=0)
        bts_obj.add_moc("gNBCUX2Op", gNBCuX2Id=2, OperatorId=2)
    bts_obj.mod_moc("gNBSharingMode", MOD(gNBMultiOpSharingMode=2))
def create_5g_hw():
    physicalconfig = bts_obj.get_data_from_excel(excel_name=site_list_filename, sheet_name="Fisico", title_row=1,
                                                 group_title="Name", ne_name=nename)
    for physic in physicalconfig:
        srn = physic.attr("Subrack")
        if int(srn) in bts_obj.get_para_list_from_moc("RRU", "SRN"):continue
        rruchain = physic.attr("RRUChain")
        rruname = physic.attr("RRUName")
        slot = physic.attr("Slot Connection")
        cpri = physic.attr("CPRI Connection")
        rrumode = physic.attr("MRRU AIRU")
        wm = physic.attr("Working Mode")
        prot = physic.attr("PROTOCOL CPRI")
        ruspe = physic.attr("RUSPEC")
        fbw = physic.attr("FMBWH")
        slot2=physic.attr("Slot Connection2")
        cpri2 = physic.attr("CPRI Connection2")
        if ruspe == "RRU5512" or ruspe == "RRU5517t" or ruspe == "RRU5502":
            vsswitch = "ON"
        else:
            vsswitch = "OFF"
        if ruspe == "RRU5512":
            txrxn = "4"
        elif ruspe == "RRU5517t":
            txrxn = "4"
        elif ruspe == "RRU5502":
            txrxn = "4"
        elif ruspe == "AAU5636w":
            txrxn = "64"
        elif ruspe == "AAU5636m":
            txrxn = "64"
        elif ruspe == "AAU5733":
            txrxn = "32"
        elif ruspe == "AAU5336w":
            txrxn = "32"
        elif ruspe == "RRU5866":
            txrxn = "8"
        else:
            txrxn = "error"
        if int(srn) not in bts_obj.get_para_list_from_moc("RRU", "SRN"):
            bts_obj.add_moc("RRU", CN=0, SRN=int(srn), SN=0, TP="TRUNK", RCN=srn, PS=0, RT=rrumode, RN=rruname,
                            ADMSTATE="UNBLOCKED", ALMPROCSW=vsswitch, ALMPROCTHRHLD=30, ALMTHRHLD=20, RS=wm,
                            RXNUM=txrxn, TXNUM=txrxn, IFFREQ=0, RFDS=0, FMBWH=fbw, LCPSW="Enable", FLAG=0,
                            RUSPEC=ruspe,
                            RFCONNTYPE="NULL", DORMANCYSW="OFF", PSGID="0", PIM3CFGSW="OFF", PAEFFSWITCH="OFF",
                            SCR="AUTO", RXFREQBANDMUTUALSW="OFF", REMOTEFLAG="UNDEFINED",
                            RFDCPWROFFALMDETECTSW="OFF",
                            LEDSW="ON", RFTXSIGNDETECTSW="OFF",
                            CUSTOMEDRFSPECSW="SPEC_1900M_45M_IBW_LTE-0&SPEC_2600M_EXPAND_LTE_TDD-0&SPEC_SUPPORT_TWO_LTE_CARRIERS-0&SPEC_1900M_60M_IBW_LTE-0&SPEC_1800M_45M_IBW_LTE-0&SPEC_1800M_55M_IBW_LTE-0&SPEC_2100M_60M_IBW_LTE-0&SPEC_2100M_45M_IBW_LTE-0&SPEC_1.8G_55M_2.1G_60M_IBW_LTE-0&SPEC_NONSTANDARD_BW_ENHANCE-0&SPEC_LOOSE_PSD_LIMIT-0&SPEC_SUB6G_CR_NUM_ENH_NR_TDD-0&SPEC_SUB6G_PFM_ENH_NR_TDD-0&SPEC_2.1G_55M_IBW_LTE-0&SPEC_100M_AND_60M_NR-0&SPEC_AWS_70M_PCS_60M_IBW_LTE-0&SPEC_1.8G_45M_2.1G_45M_IBW_LTE-0&SPEC_2.1G_55M_IBW_NR-0&SPEC_ENH_LOOSE_PSD_LIMIT-0&SPEC_ENHANCED_RF_CARRIER_NR-0&SPEC_ENHANCED_RF_CARRIER_LTE-0&SPEC_ENH_LNR_MODE1_FDD-0&SPEC_2.1G_60M_IBW_NR-0&SPEC_1.8G_ONLY-0&SPEC_AWS_45M_IBW_LTE-0&SPEC_1800M_50M_IBW_LTE-0",
                            CIRCUITBREAKERVALUE="default", DCUVADSW="OFF", MECHANICALTILT="65535",
                            LOCALRS="LTE_TDD-0&LTE_FDD-0&NBIOT-0&NR-0", TEMPERATUREALMDETENHSW="OFF",
                            HIGHTEMPPRETHLD="255", CALPORTCONSTATUS="CONNECTED", RXHWALMDETECTSW="OFF",
                            MNTMODE="NORMAL")
            bts_obj.add_moc("RRUCHAIN", RCN=rruchain, TT="LOADBALANCE", BM="COLD", AT="LOCALPORT", HCN=0, HSRN=0,
                            HSN=slot, HPN=cpri, TCN=0, TSRN=0, TSN=slot2, TPN=cpri2,
                            BRKPOS1=255, BRKPOS2=255, CR=255, USERDEFRATENEGOSW=0, PROTOCOL="eCPRI", SBT="1E-6",
                            RESVBW=255)
        if srn == "100":
            bts_obj.add_moc("SECTOR", SECTORID=100, SECNAME="NR_A", ANTAZIMUTH=65535, SECTORANTENNA=[])
            bts_obj.add_moc("SECTOREQM", SECTOREQMID=100, SECTORID=100, ANTCFGMODE="BEAM", RRUCN="0", RRUSRN="100",
                            RRUSN="0", BEAMSHAPE="SEC_120DEG", BEAMLAYERSPLIT="None", BEAMAZIMUTHOFFSET="None",
                            RRUNUM="1")
        elif srn == "101":
            bts_obj.add_moc("SECTOR", SECTORID=101, SECNAME="NR_B", ANTAZIMUTH=65535, SECTORANTENNA=[])
            bts_obj.add_moc("SECTOREQM", SECTOREQMID=101, SECTORID=101, ANTCFGMODE="BEAM", RRUCN="0", RRUSRN="101",
                            RRUSN="0", BEAMSHAPE="SEC_120DEG", BEAMLAYERSPLIT="None", BEAMAZIMUTHOFFSET="None",
                            RRUNUM="1")
        elif srn == "102":
            bts_obj.add_moc("SECTOR", SECTORID=102, SECNAME="NR_C", ANTAZIMUTH=65535, SECTORANTENNA=[])
            bts_obj.add_moc("SECTOREQM", SECTOREQMID=102, SECTORID=102, ANTCFGMODE="BEAM", RRUCN="0", RRUSRN="102",
                            RRUSN="0", BEAMSHAPE="SEC_120DEG", BEAMLAYERSPLIT="None", BEAMAZIMUTHOFFSET="None",
                            RRUNUM="1")
        elif int(srn) not in bts_obj.get_para_list_from_moc("SECTOR", "SECTORID"):
            bts_obj.add_moc("SECTOR", SECTORID=int(srn), SECNAME=rruname, ANTAZIMUTH=65535, SECTORANTENNA=[])
            bts_obj.add_moc("SECTOREQM", SECTOREQMID=int(srn), SECTORID=int(srn), ANTCFGMODE="BEAM", RRUCN="0", RRUSRN=int(srn),
                            RRUSN="0", BEAMSHAPE="SEC_120DEG", BEAMLAYERSPLIT="None", BEAMAZIMUTHOFFSET="None",
                            RRUNUM="1")
    if not physicalconfig:
        bts_obj.add_moc("RRU", CN=0, SRN=100, SN=0, TP="TRUNK", RCN=100, PS=0, RT="AIRU",
                        RN="F" + nename[1:len(nename)] + "A",
                        ADMSTATE="UNBLOCKED", ALMPROCSW="OFF", ALMPROCTHRHLD=30, ALMTHRHLD=20, RS="NO",
                        RXNUM=64, TXNUM=64, IFFREQ=0, RFDS=0, FMBWH=5000, LCPSW="Enable", FLAG=0,
                        RUSPEC="AAU5636m",
                        RFCONNTYPE="NULL", DORMANCYSW="OFF", PSGID="0", PIM3CFGSW="OFF", PAEFFSWITCH="OFF",
                        SCR="AUTO", RXFREQBANDMUTUALSW="OFF", REMOTEFLAG="UNDEFINED",
                        RFDCPWROFFALMDETECTSW="OFF",
                        LEDSW="ON", RFTXSIGNDETECTSW="OFF",
                        CUSTOMEDRFSPECSW="SPEC_1900M_45M_IBW_LTE-0&SPEC_2600M_EXPAND_LTE_TDD-0&SPEC_SUPPORT_TWO_LTE_CARRIERS-0&SPEC_1900M_60M_IBW_LTE-0&SPEC_1800M_45M_IBW_LTE-0&SPEC_1800M_55M_IBW_LTE-0&SPEC_2100M_60M_IBW_LTE-0&SPEC_2100M_45M_IBW_LTE-0&SPEC_1.8G_55M_2.1G_60M_IBW_LTE-0&SPEC_NONSTANDARD_BW_ENHANCE-0&SPEC_LOOSE_PSD_LIMIT-0&SPEC_SUB6G_CR_NUM_ENH_NR_TDD-0&SPEC_SUB6G_PFM_ENH_NR_TDD-0&SPEC_2.1G_55M_IBW_LTE-0&SPEC_100M_AND_60M_NR-0&SPEC_AWS_70M_PCS_60M_IBW_LTE-0&SPEC_1.8G_45M_2.1G_45M_IBW_LTE-0&SPEC_2.1G_55M_IBW_NR-0&SPEC_ENH_LOOSE_PSD_LIMIT-0&SPEC_ENHANCED_RF_CARRIER_NR-0&SPEC_ENHANCED_RF_CARRIER_LTE-0&SPEC_ENH_LNR_MODE1_FDD-0&SPEC_2.1G_60M_IBW_NR-0&SPEC_1.8G_ONLY-0&SPEC_AWS_45M_IBW_LTE-0&SPEC_1800M_50M_IBW_LTE-0",
                        CIRCUITBREAKERVALUE="default", DCUVADSW="OFF", MECHANICALTILT="65535",
                        LOCALRS="LTE_TDD-0&LTE_FDD-0&NBIOT-0&NR-0", TEMPERATUREALMDETENHSW="OFF",
                        HIGHTEMPPRETHLD="255", CALPORTCONSTATUS="CONNECTED", RXHWALMDETECTSW="OFF",
                        MNTMODE="NORMAL")
        bts_obj.add_moc("RRU", CN=0, SRN=101, SN=0, TP="TRUNK", RCN=101, PS=0, RT="AIRU",
                        RN="F" + nename[1:len(nename)] + "B",
                        ADMSTATE="UNBLOCKED", ALMPROCSW="OFF", ALMPROCTHRHLD=30, ALMTHRHLD=20, RS="NO",
                        RXNUM=64, TXNUM=64, IFFREQ=0, RFDS=0, FMBWH=5000, LCPSW="Enable", FLAG=0,
                        RUSPEC="AAU5636m",
                        RFCONNTYPE="NULL", DORMANCYSW="OFF", PSGID="0", PIM3CFGSW="OFF", PAEFFSWITCH="OFF",
                        SCR="AUTO", RXFREQBANDMUTUALSW="OFF", REMOTEFLAG="UNDEFINED",
                        RFDCPWROFFALMDETECTSW="OFF",
                        LEDSW="ON", RFTXSIGNDETECTSW="OFF",
                        CUSTOMEDRFSPECSW="SPEC_1900M_45M_IBW_LTE-0&SPEC_2600M_EXPAND_LTE_TDD-0&SPEC_SUPPORT_TWO_LTE_CARRIERS-0&SPEC_1900M_60M_IBW_LTE-0&SPEC_1800M_45M_IBW_LTE-0&SPEC_1800M_55M_IBW_LTE-0&SPEC_2100M_60M_IBW_LTE-0&SPEC_2100M_45M_IBW_LTE-0&SPEC_1.8G_55M_2.1G_60M_IBW_LTE-0&SPEC_NONSTANDARD_BW_ENHANCE-0&SPEC_LOOSE_PSD_LIMIT-0&SPEC_SUB6G_CR_NUM_ENH_NR_TDD-0&SPEC_SUB6G_PFM_ENH_NR_TDD-0&SPEC_2.1G_55M_IBW_LTE-0&SPEC_100M_AND_60M_NR-0&SPEC_AWS_70M_PCS_60M_IBW_LTE-0&SPEC_1.8G_45M_2.1G_45M_IBW_LTE-0&SPEC_2.1G_55M_IBW_NR-0&SPEC_ENH_LOOSE_PSD_LIMIT-0&SPEC_ENHANCED_RF_CARRIER_NR-0&SPEC_ENHANCED_RF_CARRIER_LTE-0&SPEC_ENH_LNR_MODE1_FDD-0&SPEC_2.1G_60M_IBW_NR-0&SPEC_1.8G_ONLY-0&SPEC_AWS_45M_IBW_LTE-0&SPEC_1800M_50M_IBW_LTE-0",
                        CIRCUITBREAKERVALUE="default", DCUVADSW="OFF", MECHANICALTILT="65535",
                        LOCALRS="LTE_TDD-0&LTE_FDD-0&NBIOT-0&NR-0", TEMPERATUREALMDETENHSW="OFF",
                        HIGHTEMPPRETHLD="255", CALPORTCONSTATUS="CONNECTED", RXHWALMDETECTSW="OFF",
                        MNTMODE="NORMAL")
        bts_obj.add_moc("RRU", CN=0, SRN=102, SN=0, TP="TRUNK", RCN=102, PS=0, RT="AIRU",
                        RN="F" + nename[1:len(nename)] + "C",
                        ADMSTATE="UNBLOCKED", ALMPROCSW="OFF", ALMPROCTHRHLD=30, ALMTHRHLD=20, RS="NO",
                        RXNUM=64, TXNUM=64, IFFREQ=0, RFDS=0, FMBWH=5000, LCPSW="Enable", FLAG=0,
                        RUSPEC="AAU5636m",
                        RFCONNTYPE="NULL", DORMANCYSW="OFF", PSGID="0", PIM3CFGSW="OFF", PAEFFSWITCH="OFF",
                        SCR="AUTO", RXFREQBANDMUTUALSW="OFF", REMOTEFLAG="UNDEFINED",
                        RFDCPWROFFALMDETECTSW="OFF",
                        LEDSW="ON", RFTXSIGNDETECTSW="OFF",
                        CUSTOMEDRFSPECSW="SPEC_1900M_45M_IBW_LTE-0&SPEC_2600M_EXPAND_LTE_TDD-0&SPEC_SUPPORT_TWO_LTE_CARRIERS-0&SPEC_1900M_60M_IBW_LTE-0&SPEC_1800M_45M_IBW_LTE-0&SPEC_1800M_55M_IBW_LTE-0&SPEC_2100M_60M_IBW_LTE-0&SPEC_2100M_45M_IBW_LTE-0&SPEC_1.8G_55M_2.1G_60M_IBW_LTE-0&SPEC_NONSTANDARD_BW_ENHANCE-0&SPEC_LOOSE_PSD_LIMIT-0&SPEC_SUB6G_CR_NUM_ENH_NR_TDD-0&SPEC_SUB6G_PFM_ENH_NR_TDD-0&SPEC_2.1G_55M_IBW_LTE-0&SPEC_100M_AND_60M_NR-0&SPEC_AWS_70M_PCS_60M_IBW_LTE-0&SPEC_1.8G_45M_2.1G_45M_IBW_LTE-0&SPEC_2.1G_55M_IBW_NR-0&SPEC_ENH_LOOSE_PSD_LIMIT-0&SPEC_ENHANCED_RF_CARRIER_NR-0&SPEC_ENHANCED_RF_CARRIER_LTE-0&SPEC_ENH_LNR_MODE1_FDD-0&SPEC_2.1G_60M_IBW_NR-0&SPEC_1.8G_ONLY-0&SPEC_AWS_45M_IBW_LTE-0&SPEC_1800M_50M_IBW_LTE-0",
                        CIRCUITBREAKERVALUE="default", DCUVADSW="OFF", MECHANICALTILT="65535",
                        LOCALRS="LTE_TDD-0&LTE_FDD-0&NBIOT-0&NR-0", TEMPERATUREALMDETENHSW="OFF",
                        HIGHTEMPPRETHLD="255", CALPORTCONSTATUS="CONNECTED", RXHWALMDETECTSW="OFF",
                        MNTMODE="NORMAL")

        bts_obj.add_moc("RRUCHAIN", RCN=100, TT="LOADBALANCE", BM="COLD", AT="LOCALPORT", HCN=0, HSRN=0,
                        HSN=3, HPN=0, TCN=0, TSRN=0, TSN=1, TPN=0,
                        BRKPOS1=255, BRKPOS2=255, CR=255, USERDEFRATENEGOSW=0, PROTOCOL="eCPRI", SBT="1E-6",
                        RESVBW=255)
        bts_obj.add_moc("RRUCHAIN", RCN=101, TT="LOADBALANCE", BM="COLD", AT="LOCALPORT", HCN=0, HSRN=0,
                        HSN=3, HPN=1, TCN=0, TSRN=0, TSN=1, TPN=1,
                        BRKPOS1=255, BRKPOS2=255, CR=255, USERDEFRATENEGOSW=0, PROTOCOL="eCPRI", SBT="1E-6",
                        RESVBW=255)
        bts_obj.add_moc("RRUCHAIN", RCN=102, TT="LOADBALANCE", BM="COLD", AT="LOCALPORT", HCN=0, HSRN=0,
                        HSN=3, HPN=2, TCN=0, TSRN=0, TSN=1, TPN=2,
                        BRKPOS1=255, BRKPOS2=255, CR=255, USERDEFRATENEGOSW=0, PROTOCOL="eCPRI", SBT="1E-6",
                        RESVBW=255)
        bts_obj.add_moc("SECTOR", SECTORID=100, SECNAME="NR_A", ANTAZIMUTH=65535, SECTORANTENNA=[])
        bts_obj.add_moc("SECTOREQM", SECTOREQMID=100, SECTORID=100, ANTCFGMODE="BEAM", RRUCN="0",
                        RRUSRN="100",
                        RRUSN="0", BEAMSHAPE="SEC_120DEG", BEAMLAYERSPLIT="None", BEAMAZIMUTHOFFSET="None",
                        RRUNUM="1")
        bts_obj.add_moc("SECTOR", SECTORID=101, SECNAME="NR_B", ANTAZIMUTH=65535, SECTORANTENNA=[])
        bts_obj.add_moc("SECTOREQM", SECTOREQMID=101, SECTORID=101, ANTCFGMODE="BEAM", RRUCN="0",
                        RRUSRN="101",
                        RRUSN="0", BEAMSHAPE="SEC_120DEG", BEAMLAYERSPLIT="None", BEAMAZIMUTHOFFSET="None",
                        RRUNUM="1")
        bts_obj.add_moc("SECTOR", SECTORID=102, SECNAME="NR_C", ANTAZIMUTH=65535, SECTORANTENNA=[])
        bts_obj.add_moc("SECTOREQM", SECTOREQMID=102, SECTORID=102, ANTCFGMODE="BEAM", RRUCN="0",
                        RRUSRN="102",
                        RRUSN="0", BEAMSHAPE="SEC_120DEG", BEAMLAYERSPLIT="None", BEAMAZIMUTHOFFSET="None",
                        RRUNUM="1")
    brdspec = "UBBPg2a"
    if "5900A" in product_type:
        bts_obj.add_moc("BBP", CN=0, SRN=0, SN=0, TYPE="UBBP", ADMSTATE="UNBLOCKED", HCE="FULL", CCNE="ON",
                        BBWS=MODEL.BBP.BBWS.fromString(BIT(NR=1)), SRT="DEFAULT", CPRIITFTYPE="CPRI_SFP",
                        LTEFLEXSPECSW="OFF")
    else:
        if 1 not in bts_obj.get_para_list_from_moc("BPP", "SN"):
            bts_obj.add_moc("BBP", CN=0, SRN=0, SN=1, TYPE="UBBP", OVERLOADALMRPTTHLD=90,
                            OVERLOADALMCLRTHLD=85,
                            ADMSTATE="UNBLOCKED", HCE="FULL", BBWS="GSM-0&UMTS-0&LTE_FDD-0&LTE_TDD-0&NBIOT-0&NR-1", WM=14,
                            SRT="DEFAULT",
                            CPRIITFTYPE="CPRI_SFP", LTEFLEXSPECSW="OFF", BRDSPEC=brdspec)
        else:
            mo_class = getattr(MODEL, "BBP")
            parameter_class = getattr(mo_class, "BBWS")
            config_string=parameter_class.toString(bts_obj.get_para_list_from_moc("BBP","BBWS",WHERE(SN=1))[0])
            config_string = config_string.replace("NR-0", "NR-1")
            bts_obj.mod_moc("BBP", MOD(BBWS=config_string).WHERE(SN=1))
        if 3 not in bts_obj.get_para_list_from_moc("BPP", "SN"):
            bts_obj.add_moc("BBP", CN=0, SRN=0, SN=3, TYPE="UBBP", OVERLOADALMRPTTHLD=90,
                            OVERLOADALMCLRTHLD=85,
                            ADMSTATE="UNBLOCKED", HCE="FULL", BBWS="GSM-0&UMTS-0&LTE_FDD-0&LTE_TDD-0&NBIOT-0&NR-1", WM=14,
                            SRT="DEFAULT",
                            CPRIITFTYPE="CPRI_SFP", LTEFLEXSPECSW="OFF", BRDSPEC=brdspec)
        else:
            mo_class = getattr(MODEL, "BBP")
            parameter_class = getattr(mo_class, "BBWS")
            config_string=parameter_class.toString(bts_obj.get_para_list_from_moc("BBP","BBWS",WHERE(SN=3))[0])
            config_string = config_string.replace("NR-0", "NR-1")
            bts_obj.mod_moc("BBP", MOD(BBWS=config_string).WHERE(SN=3))

    if 10 not in bts_obj.get_para_list_from_moc("BASEBANDEQM", "BASEBANDEQMID"):
        bts_obj.add_moc("BASEBANDEQM", BASEBANDEQMID=10, BASEBANDEQMTYPE="ULDL", UMTSDEMMODE=0,
                        BASEBANDEQMBOARD=[MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=0, SRN=0, SN=1)])
    if 12 not in bts_obj.get_para_list_from_moc("BASEBANDEQM", "BASEBANDEQMID"):
        bts_obj.add_moc("BASEBANDEQM", BASEBANDEQMID=12, BASEBANDEQMTYPE="ULDL", UMTSDEMMODE=0,
                        BASEBANDEQMBOARD=[MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=0, SRN=0, SN=3)])
    # bts_obj.set_moc("GNSS", GN="0", CN="0", SRN="0", SN="7", WPOS="AUTOSEARCH", AGL="5", CABLE_LEN="50",
    #                 MODE="GPS",
    #                 PRI="1", POSCHECKSW="ON", ANTMODE="AUTO")
    # bts_obj.mod_moc("TASM", MOD(MODE="AUTO", CLKSYNCMODE="TIME"), is_new=True)

def nr_cell_expansion(nr_plan_cell):
    banda = nr_plan_cell.attr("Frequency Band")
    if banda == "78":
        bandaok = "N78"
    else:
        bandaok = "error"
    bw = nr_plan_cell.attr("Bandwidth [kHz]")
    if bw == "50000":
        bwok = "CELL_BW_50M"
    elif bw == "100000":
        bwok = "CELL_BW_100M"
    elif bw == "20000":
        bwok = "CELL_BW_20M"
    else:
        bwok = "error"
    se = ""
    if nr_plan_cell.attr("Sector")=="A" or nr_plan_cell.attr("Sector")=="1":
        se=100
    elif nr_plan_cell.attr("Sector")=="B" or nr_plan_cell.attr("Sector")=="2":
        se=101
    elif nr_plan_cell.attr("Sector")=="C" or nr_plan_cell.attr("Sector")=="3":
        se=102
    if 100 not in bts_obj.get_para_list_from_moc("SECTOREQM","SECTOREQMID"):
        if nr_plan_cell.attr("Sector") == "A" or nr_plan_cell.attr("Sector") == "1":
            se = 120
        elif nr_plan_cell.attr("Sector") == "B" or nr_plan_cell.attr("Sector") == "2":
            se = 121
        elif nr_plan_cell.attr("Sector") == "C" or nr_plan_cell.attr("Sector") == "3":
            se = 122

    nrcellid = int(nr_plan_cell.attr("Cell ID / Cell Index"))
    nr_tilt = nr_plan_cell.attr("Electrical Downtilt")
    if nr_tilt:
        nr_tilt = int(float(nr_tilt))
    else:
        nr_tilt=0

    sub = nr_plan_cell.attr("Subcarrier Spacing [KHz]")
    if sub == "30":
        subok = "30KHZ"
    else:
        subok = "error"
    power = nr_plan_cell.attr("Pilot Power(dBm)")
    if power.isdigit():
        powerok = int(float(power) * 10)
    else:
        powerok = 369
    nrcell_active_state = 1
    nr_trackingarea_id=3
    nr_operator=2
    customer = "TELECOM"
    if region=="AMBA" and nr_plan_cell.attr("MNC")=="07":
        customer = "TELEFONICA"
        basen = 12
        nr_trackingarea_id = 3
        nr_operator = 2
    elif region=="SUR" and nr_plan_cell.attr("MNC")=="34":
        basen = 12
        nr_trackingarea_id = 3
        nr_operator = 2
    elif region=="AMBA" and nr_plan_cell.attr("MNC")=="34":
        basen = 10
        nr_trackingarea_id = 0
        nr_operator = 0
    elif region=="SUR" and nr_plan_cell.attr("MNC")=="07":
        customer = "TELEFONICA"
        nr_trackingarea_id = 0
        nr_operator = 0
        basen = 10
    else:
        basen = 10

    SsbDescMethod = "SSB_DESC_TYPE_GSCN"
    SsbFreqPos = nr_plan_cell.attr("SSB Frequency Position")
    trx = nr_plan_cell.attr("TXRX MODE")
    template_type = "NRCELL"
    template_type_ducell = "NRDUCELL"
    combine = template_type + "_" + bandaok + "_" + trx + "_" + customer + "_YES" + "_" + region
    nrcell_template = ""
    nrducell_template = ""
    for cell_template in template_list:
        if cell_template.attr("Scenario") == combine:
            nrcell_template = cell_template.attr("TEMPLATE NAME")
            break
    combine = template_type_ducell + "_" + bandaok + "_" + trx + "_" + customer + "_YES" +  "_" + region
    for cell_template in template_list:
        if cell_template.attr("Scenario") == combine:
            nrducell_template = cell_template.attr("TEMPLATE NAME")
            break
    if nrcellid == 350:
        ducelltrpid = 4
    elif nrcellid == 351:
        ducelltrpid = 5
    elif nrcellid == 352:
        ducelltrpid = 6
    else:
        ducelltrpid = nrcellid
    print(nrcell_template)
    print(nrducell_template)
    bts_obj.create_5G_NrCell(TemplateName=nrcell_template,
                             NrCellId=nrcellid,
                             CellName=nr_plan_cell.attr("Cell Name"),
                             CellId=nrcellid,
                             # MaxTransmitPower=cell_excel_row.attr("Max Transmit Power(0.1dBm)"),
                             FrequencyBand=bandaok,
                             DlNarfcn=nr_plan_cell.attr("ARFCN DL"),
                             CpriCompression="3DOT2_COMPRESSION",
                             TrackingAreaId=nr_trackingarea_id,
                             Tac=nr_plan_cell.attr("LAC/TAC"),
                             CellActiveState=nrcell_active_state)
    bts_obj.create_5G_NrDuCell(TemplateName=nrducell_template,
                               NrDuCellId=nrcellid,
                               NrDuCellName=nr_plan_cell.attr("Cell Name"),
                               CellId=nrcellid,
                               PhysicalCellId=nr_plan_cell.attr("PCI/PSC"),
                               FrequencyBand=bandaok,
                               UlNarfcn=nr_plan_cell.attr("ARFCN DL"),
                               DlNarfcn=nr_plan_cell.attr("ARFCN DL"),
                               UlBandwidth=bwok,
                               DlBandwidth=bwok,
                               MaxTransmitPower="65535",
                               SectorEqmId=se,
                               NrDuCellActiveState="NRDU_CELL_ACTIVE",  # temporal para test
                               BasebandEqmId=basen,
                               SlotAssignment=nr_plan_cell.attr("Frame Configuration (Slot Assignment)"),
                               SlotStructure=nr_plan_cell.attr("Slot Structure"),
                               SsbDescMethod=SsbDescMethod,
                               SsbFreqPos=SsbFreqPos,
                               SubcarrierSpacing=subok,
                               CellRadius=nr_plan_cell.attr("Cell Radius [m]"),
                               LogicalRootSequenceIndex=nr_plan_cell.attr("PRACH (Root Sequence Idx) 5G"),
                               TxRxMode=nr_plan_cell.attr("TXRX MODE"),
                               PowerConfigMode="TRANSMIT_POWER",
                               CpriCompression="3DOT2_COMPRESSION",
                               BranchCpriCompression="3DOT2_COMPRESSION",
                               TrackingAreaId=nr_trackingarea_id,
                               FrAndDuplexMode="FR1_TDD",
                               OperatorId=nr_operator,
                               NrDuCellTrpId=ducelltrpid)
    bts_obj.mod_moc("NRDUCellTrp", MOD(MaxTransmitPower=powerok).WHERE(NrDuCellId=nrcellid))
    bts_obj.mod_moc("NRDUCell", MOD(TrackingAreaId=nr_trackingarea_id).WHERE(NrDuCellId=nrcellid), is_new=True)
    bts_obj.add_moc("NRDUCellTrpBeam", NrDuCellTrpId=ducelltrpid, CoverageScenario="DEFAULT", Tilt=nr_tilt,
                    Azimuth=0, MaxSsbPwrOffset=0, ScenarioBeamAlgoSw=0, ConnModeCoverageScenario="DEFAULT",
                    TrpAntType="DEFAULT")
    bts_obj.mod_moc("NRDUCellTrpBeam", MOD(Tilt=nr_tilt).WHERE(NrDuCellTrpId=ducelltrpid))
    if not bts_obj.get_para_list_from_moc("NRDUCellOp", "NrDuCellId", WHERE(NrDuCellId=nrcellid)):
        bts_obj.add_moc("NRDUCellOp", CellId=nrcellid, CellPrimaryOpFlag=0, CellReservedForOp=0, CellResId=255,
                        NrDuCellId=nrcellid, NrNetworkingOption=3, OperatorId=nr_operator, TrackingAreaId=4294967295)
    else:
        bts_obj.mod_moc("NRDUCellOp", MOD(OperatorId=nr_operator, CellId=nrcellid).WHERE(NrDuCellId=nrcellid),is_new=True)

bts_obj = BTSObject()

site_list_filename = u'*Argentina_TA_5G*'
siteinfo = bts_obj.get_SiteInfo(site_info_excel_name=site_list_filename, site_info_sheet_name= "Base Station Transport Data",  title_row=2,  site_name_title="*Name")
nename = siteinfo.attr("*Name")
metainfo = siteinfo.attr("META")
scenarioespecial = siteinfo.attr("Escenario con IPs correctas pero sin 5G")

nr_ip_plan = bts_obj.get_data_from_excel(excel_name=site_list_filename, sheet_name="AMBA", title_row=2,
                                                     group_title="Site OSS Name (BBU)", ne_name=nename)
if not nr_ip_plan:
    nr_ip_plan = bts_obj.get_data_from_excel(excel_name=site_list_filename, sheet_name="SUR", title_row=2,
                                             group_title="Site OSS me (BBU)", ne_name=nename)
if nr_ip_plan:
    ipplaninfo=nr_ip_plan[0]
gnodebid = siteinfo.attr("*gNodeB ID")
product_type = siteinfo.attr("*Product Type")
nr_radio_template = siteinfo.attr("gRadio Template")
BBU_change = siteinfo.attr("BBU Change")
tacnr = siteinfo.attr("TAC")
compt_tree = None
compt_name = siteinfo.attr("Old BTS Name")
region=siteinfo.attr("Region")
if compt_name:
    compt_tree = bts_obj.get_all_moc_from_ref(compt_name)
    pass
compt_extend_list = []
no_need_moc_list = []
if compt_tree:
    bts_obj.clear_NeTreePre(compt_tree)
    bts_obj.save_all_mocs(compt_tree, APPEND_MODE, with_merge=True, with_child=True, include_mocs=None, exclude_mocs=no_need_moc_list + compt_extend_list)

def clear_pre(ne_tree):
    for key in ne_tree:
        for moi in ne_tree[key]:
            if getattr(moi, '__prev', None) is not None:
                setattr(moi, '__prev', None)
########################################################################################################################

techology_list = bts_obj.get_para_list_from_moc("APPLICATION","AT")
ip_configure_list=bts_obj.get_para_list_from_moc("DEVIP","IP")
vlan_confiure_list=bts_obj.get_para_list_from_moc("VLANMAP","NEXTHOPIP")
sctphost_configure_list= bts_obj.get_para_list_from_moc("SCTPHOST",["SCTPHOSTID","SIGIP1V4"])
userplanehost_configure_list = bts_obj.get_para_list_from_moc("SCTPHOST",["SCTPHOSTID","SIGIP1V4"])
devip_type,devip_port=bts_obj.get_para_list_from_moc("DEVIP",["PT","PN"])[2]
srciprt_configure_list=bts_obj.get_para_list_from_moc("SRCIPRT","SRCIP")

cell_plan_info_list = bts_obj.get_data_from_excel(excel_name=site_list_filename, sheet_name="RND_MVS",title_row=1,
                                                         group_title="Site OSS Name (BBU)", ne_name=nename)
tp_cell_plan_info_list = bts_obj.get_data_from_excel(excel_name=site_list_filename, sheet_name="RND_TP",title_row=1,
                                                     group_title="Site OSS Name (EMG)", ne_name=nename)
for cell_plan in tp_cell_plan_info_list:
    cell_plan_info_list.append(cell_plan)
template_list=bts_obj.get_data_from_excel(excel_name=site_list_filename, sheet_name="Template",title_row=1,group_title="NE Name", ne_name="standard")

mvs_tacnr=""
tp_tacnr=""
tp_tac=""
tlf_tac=""
mvs_tac_nb=""
tp_tac_nb=""

if cell_plan_info_list:
    for cell_plan in cell_plan_info_list:
        if cell_plan.attr("RAT")=="4G" and cell_plan.attr("MNC")=="07" and cell_plan.attr("Cell Type")=="FDD":
            tlf_tac=int(cell_plan.attr("LAC/TAC"))
        if cell_plan.attr("RAT") == "4G" and cell_plan.attr("MNC") == "34" and cell_plan.attr("Cell Type")=="FDD":
            tp_tac = int(cell_plan.attr("LAC/TAC"))
        if  cell_plan.attr("RAT")=="5G" and cell_plan.attr("MNC")=="07" and cell_plan.attr("Cell Type")=="TDD":
            mvs_tacnr=int(cell_plan.attr("LAC/TAC"))
        if cell_plan.attr("RAT") == "5G" and cell_plan.attr("MNC") == "34" and cell_plan.attr("Cell Type")=="TDD":
            tp_tacnr = int(cell_plan.attr("LAC/TAC"))

exist_nr_cell = bts_obj.get_para_list_from_moc("NRDUCell","NrDuCellId")
for cell in exist_nr_cell:
    bts_obj.add_moc("NRDUCellOp", CellId=cell, CellPrimaryOpFlag=0, CellReservedForOp=0, CellResId=255,
                        NrDuCellId=cell, NrNetworkingOption=3, OperatorId=0, TrackingAreaId=4294967295)
if not exist_nr_cell:
    if scenarioespecial == "YES":
        if metainfo == "YES":
            nr_radio_template_filename = "AR_TA_NR_Radio_con_META"
        elif metainfo == "NO":
            nr_radio_template_filename = "AR_TA_NR_Radio_sin_META"
        else:
            nr_radio_template_filename = "Missing Fill Meta Info"
        bts_obj.create_5G_Radio_Ex(TemplateName=nr_radio_template_filename, gNodeBFunctionName=siteinfo.attr("*gNodeB Name"), gNBId=siteinfo.attr("*gNodeB ID"), gNBIdLength=22, OperatorName="PERSONAL 5G", Mcc="722", Mnc="34")

        if not bts_obj.get_para_list_from_moc("GPS","GN"):
            bts_obj.set_moc("GNSS", GN=0, CN=0, SRN=0, SN=7, WPOS="AUTO_SEARCH", AGL=5, CABLE_LEN=10, MODE="GPS", PRI=1,
                        POSCHECKSW="ON")
        bts_obj.mod_moc("TASM", MOD(SRCNO=0, CLKSRC=0, CLKSYNCMODE=1))
    else:
        if metainfo == "YES":
            nr_radio_template_filename = "AR_TA_NR_Radio_con_META"
        elif metainfo == "NO":
            nr_radio_template_filename = "AR_TA_NR_Radio_sin_META"
        else:
            nr_radio_template_filename = "Missing Fill Meta Info"
        bts_obj.create_5G_Radio_Ex(TemplateName=nr_radio_template_filename, gNodeBFunctionName=siteinfo.attr("*gNodeB Name"), gNBId=siteinfo.attr("*gNodeB ID"), gNBIdLength=22, OperatorName="PERSONAL 5G", Mcc="722", Mnc="34")

if not bts_obj.get_para_list_from_moc("GNSS","GN"):
    bts_obj.add_moc("GNSS", GN=0, CN=0, SRN=0, SN=7, WPOS="AUTO_SEARCH", AGL=5, CABLE_LEN=10, MODE="GPS", PRI=1,
                POSCHECKSW="ON")
bts_obj.mod_moc("TASM", MOD(SRCNO=0, CLKSRC=0, CLKSYNCMODE=1))
create_gnodeb_op()

#BBU change
if BBU_change =="YES":
    bts_obj.mod_moc("SUBRACK", MOD(TYPE=166).WHERE(SRN=0))
    bts_obj.mod_moc("CABINET", MOD(TYPE="BTS5900").WHERE(CN=0))

#change BBP
bbp_config_list = bts_obj.get_data_from_excel(excel_name=site_list_filename, sheet_name="BBP", title_row=1,
                                              group_title="Site Name", ne_name=nename)
if bbp_config_list:
    bts_obj.del_moc("BBP")
    bts_obj.del_moc("BASEBANDEQM")
    all_baseband = []
    ul_list = {}
    dl_list = {}
    full_list = {}
    ul_exist_list = []
    dl_exist_list = []
    full_exist_list = []
    for bbp_config in bbp_config_list:
        if not bbp_config.attr("new BBP slot"):continue
        bbp_slot=int(bbp_config.attr("new BBP slot"))
        bts_obj.add_moc("BBP", CN=0, SRN=0, SN=bbp_slot, TYPE="UBBP", OVERLOADALMRPTTHLD=90,
                        OVERLOADALMCLRTHLD=85,
                        ADMSTATE="UNBLOCKED", HCE="FULL", BBWS=bbp_config.attr("BBP work mode"), WM=14, SRT="DEFAULT",
                        CPRIITFTYPE="CPRI_SFP", LTEFLEXSPECSW="OFF", BRDSPEC=bbp_config.attr("BRDSPEC"))
        if not bbp_config.attr("*Baseband Equipment Type"):continue
        baseband_list = bbp_config.attr("*Baseband Equipment Type").split(";")
        basebandid_list = bbp_config.attr("Baseband equipment ID").split(";")
        basebandid_list=[int(x) for x in basebandid_list]
        for i in range(len(baseband_list)):
            if baseband_list[i] == "UL":
                if basebandid_list[i] not in ul_exist_list:
                    ul_list[basebandid_list[i]]=[MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=0, SRN=0, SN=bbp_slot)]
                    ul_exist_list.append(basebandid_list[i])
                else:
                    if len(ul_list)>1:
                        ul_list[basebandid_list[i]] = ul_list[basebandid_list[i]].append([MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=0, SRN=0, SN=bbp_slot)])
                    else:
                        ul_list[basebandid_list[i]] = list(ul_list[basebandid_list[i]]).append(
                            [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=0, SRN=0, SN=bbp_slot)])

            elif baseband_list[i] == "DL":
                if basebandid_list[i] not in dl_exist_list:
                    dl_list[basebandid_list[i]] = [
                        MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=0, SRN=0, SN=bbp_slot)]
                    dl_exist_list.append(basebandid_list[i])
                else:
                    if len(dl_list)>1:
                        dl_list[basebandid_list[i]] = dl_list[basebandid_list[i]].append(
                        [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=0, SRN=0, SN=bbp_slot)])
                    else:
                        dl_list[basebandid_list[i]] = list(dl_list[basebandid_list[i]]).append(
                            [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=0, SRN=0, SN=bbp_slot)])

            elif baseband_list[i] == "FULL":
                if basebandid_list[i] not in full_exist_list:
                    full_list[basebandid_list[i]] = [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=0, SRN=0, SN=bbp_slot)]
                    full_exist_list.append(basebandid_list[i])
                else:
                    if len(full_list[basebandid_list[i]]) >1:
                        full_list[basebandid_list[i]] = full_list[basebandid_list[i]].append(
                        [MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=0, SRN=0, SN=bbp_slot)])
                    else:
                        full_list[basebandid_list[i]]=list(full_list[basebandid_list[i]]).append([MODEL.BASEBANDEQM.BASEBANDEQMBOARD(CN=0, SRN=0, SN=bbp_slot)])
                if bbp_config.attr("LTE cell ID"):
                    cellid_list = bbp_config.attr("LTE cell ID").split(";")
                    for cellid in cellid_list:
                        bts_obj.mod_moc("eUCellSectorEqm",MOD(BaseBandEqmId=basebandid_list[i]).WHERE(LocalCellId=int(cellid)),is_new=True)
                        bts_obj.mod_moc("EuPrbSectorEqm",MOD(BasebandEqmId=basebandid_list[i]).WHERE(LocalCellId=int(cellid)),is_new=True)
                    pass
                if bbp_config.attr("NR cell ID"):
                    nrcellid_list = bbp_config.attr("NR cell ID").split(";")
                    for nrcell in nrcellid_list:
                        bts_obj.mod_moc("NRDUCellTrp",MOD(BasebandEqmId=basebandid_list[i]).WHERE(NrDuCellId=nrcell),is_new=True)
                        bts_obj.mod_moc("NRDUCellTrp", MOD(BasebandEqmId=basebandid_list[i]).WHERE(NrDuCellId=int(nrcell)),
                                        is_new=True)
            else:
                exit("basebandeqm error")
    if ul_list:
        for key in ul_list:
            bts_obj.add_moc("BASEBANDEQM", BASEBANDEQMID=key, BASEBANDEQMTYPE=0, UMTSDEMMODE=4,
                            BASEBANDEQMBOARD=ul_list[key])
    if dl_list:
        for key in dl_list:
            bts_obj.add_moc("BASEBANDEQM", BASEBANDEQMID=key, BASEBANDEQMTYPE=1, BASEBANDEQMBOARD=dl_list[key])
    if full_list:
        for key in full_list:
            bts_obj.add_moc("BASEBANDEQM", BASEBANDEQMID=key, BASEBANDEQMTYPE=2, UMTSDEMMODE=0, BASEBANDEQMBOARD=full_list[key])

#change RRU chain
swap_config_list = bts_obj.get_data_from_excel(excel_name=site_list_filename, sheet_name="BBU", title_row=1,
                                               group_title="Site Name", ne_name=nename)
if swap_config_list:
    for swap_config in swap_config_list:
        old_rruchain = int(swap_config.attr("old RRUCHAIN"))
        new_bbp_slot = int(swap_config.attr("new BBP slot"))
        new_port_no = int(swap_config.attr("new port number"))
        bts_obj.mod_moc("RRUCHAIN", MOD(HSN=new_bbp_slot, HPN=new_port_no).WHERE(RCN=old_rruchain),is_new=True)

create_5g_hw()
if siteinfo.attr("old LTE CP IP"):
    modify_lte_tx(ipplaninfo)

nr_tx_expansion(ipplaninfo)


tp_newnr_celllist=[]
mvs_newnr_celllist=[]
for nr_plan_cell in cell_plan_info_list:
    if nr_plan_cell.attr("RAT")!="5G":continue
    banda = nr_plan_cell.attr("Frequency Band")
    if banda == "78":
        bandaok = "N78"
    else:
        bandaok = "error"
    bw = nr_plan_cell.attr("Bandwidth [kHz]")
    if bw == "50000":
        bwok = "CELL_BW_50M"
    elif bw == "100000":
        bwok = "CELL_BW_100M"
    elif bw == "20000":
        bwok = "CELL_BW_20M"
    else:
        bwok = "error"
    se = ""
    if nr_plan_cell.attr("Sector") == "A" or nr_plan_cell.attr("Sector") == "1":
        se = 100
    elif nr_plan_cell.attr("Sector") == "B" or nr_plan_cell.attr("Sector") == "2":
        se = 101
    elif nr_plan_cell.attr("Sector") == "C" or nr_plan_cell.attr("Sector") == "3":
        se = 102
    if 100 not in bts_obj.get_para_list_from_moc("SECTOREQM","SECTOREQMID"):
        if nr_plan_cell.attr("Sector") == "A" or nr_plan_cell.attr("Sector") == "1":
            se = 120
        elif nr_plan_cell.attr("Sector") == "B" or nr_plan_cell.attr("Sector") == "2":
            se = 121
        elif nr_plan_cell.attr("Sector") == "C" or nr_plan_cell.attr("Sector") == "3":
            se = 122

    nrcellid = int(nr_plan_cell.attr("Cell ID / Cell Index"))
    nr_tilt = nr_plan_cell.attr("Electrical Downtilt")
    if nr_tilt:
        nr_tilt = int(float(nr_tilt))
    else:
        nr_tilt = 0

    sub = nr_plan_cell.attr("Subcarrier Spacing [KHz]")
    if sub == "30":
        subok = "30KHZ"
    else:
        subok = "error"
    power = nr_plan_cell.attr("Pilot Power(dBm)")
    if power.isdigit():
        powerok = int(power)
    else:
        powerok = int(power.split("m")[0])
    # power = nr_plan_cell.attr("Pilot Power(dBm)")
    # if power.isdigit():
    #     powerok = int(float(power) * 10)
    # else:
    #     powerok = 369
    SsbDescMethod = "SSB_DESC_TYPE_GSCN"
    SsbFreqPos = nr_plan_cell.attr("SSB Frequency Position")
    SsbNarFcn = nr_plan_cell.attr("SsbNarFcn")
    trx = nr_plan_cell.attr("TXRX MODE")
    pci=nr_plan_cell.attr("PCI/PSC")
    nrcell_active_state = 1
    nr_trackingarea_id = 3
    nr_operator = 2
    customer = "TELECOM"
    if nr_plan_cell.attr("MNC") == "07":
        customer = "TELEFONICA"
        basen = 12
        nr_trackingarea_id = 3
        nr_operator = 2
        mvs_newnr_celllist.append([nrcellid,int(pci),int(SsbNarFcn)])
    elif nr_plan_cell.attr("MNC") == "34":
        basen = 10
        nr_trackingarea_id = 0
        nr_operator = 0
        tp_newnr_celllist.append([nrcellid,pci,SsbNarFcn])


    template_type = "NRCELL"
    template_type_ducell = "NRDUCELL"
    combine = template_type + "_" + bandaok + "_" + trx + "_" + customer + "_YES" + "_" + region
    print(combine)
    nrcell_template = ""
    nrducell_template = ""
    for cell_template in template_list:
        if cell_template.attr("Scenario") == combine:
            nrcell_template = cell_template.attr("TEMPLATE NAME")
            break
    combine = template_type_ducell + "_" + bandaok + "_" + trx + "_" + customer + "_YES" + "_" + region
    print(combine)
    for cell_template in template_list:
        if cell_template.attr("Scenario") == combine:
            nrducell_template = cell_template.attr("TEMPLATE NAME")
            break
    if nrcellid < 255:
        ducelltrpid = nrcellid
    elif nrcellid == 350:
        ducelltrpid = 4
    elif nrcellid == 351:
        ducelltrpid = 5
    elif nrcellid == 352:
        ducelltrpid = 6
    else:
        ducelltrpid="error"
    bts_obj.create_5G_NrCell(TemplateName=nrcell_template,
                             NrCellId=nrcellid,
                             CellName=nr_plan_cell.attr("Cell Name"),
                             CellId=nrcellid,
                             # MaxTransmitPower=cell_excel_row.attr("Max Transmit Power(0.1dBm)"),
                             FrequencyBand=bandaok,
                             DlNarfcn=nr_plan_cell.attr("ARFCN DL"),
                             CpriCompression="3DOT2_COMPRESSION",
                             TrackingAreaId=nr_trackingarea_id,
                             Tac=nr_plan_cell.attr("LAC/TAC"),
                             CellActiveState=nrcell_active_state)
    bts_obj.create_5G_NrDuCell(TemplateName=nrducell_template,
                               NrDuCellId=nrcellid,
                               NrDuCellName=nr_plan_cell.attr("Cell Name"),
                               CellId=nrcellid,
                               PhysicalCellId=nr_plan_cell.attr("PCI/PSC"),
                               FrequencyBand=bandaok,
                               UlNarfcn=nr_plan_cell.attr("ARFCN DL"),
                               DlNarfcn=nr_plan_cell.attr("ARFCN DL"),
                               UlBandwidth=bwok,
                               DlBandwidth=bwok,
                               MaxTransmitPower="65535",
                               SectorEqmId=se,
                               NrDuCellActiveState="NRDU_CELL_ACTIVE",  # temporal para test
                               BasebandEqmId=basen,
                               SlotAssignment=nr_plan_cell.attr("Frame Configuration (Slot Assignment)"),
                               SlotStructure=nr_plan_cell.attr("Slot Structure"),
                               SsbDescMethod=SsbDescMethod,
                               SsbFreqPos=SsbFreqPos,
                               SubcarrierSpacing=subok,
                               CellRadius=nr_plan_cell.attr("Cell Radius [m]"),
                               LogicalRootSequenceIndex=nr_plan_cell.attr("PRACH (Root Sequence Idx) 5G"),
                               TxRxMode=nr_plan_cell.attr("TXRX MODE"),
                               PowerConfigMode="TRANSMIT_POWER",
                               CpriCompression="3DOT2_COMPRESSION",
                               BranchCpriCompression="3DOT2_COMPRESSION",
                               TrackingAreaId=nr_trackingarea_id,
                               FrAndDuplexMode="FR1_TDD",
                               OperatorId=nr_operator,
                               NrDuCellTrpId=ducelltrpid)
    tacnr = nr_plan_cell.attr("LAC/TAC")
    bts_obj.mod_moc("NRDUCellTrp", MOD(PowerConfigMode=2, MaxTransmitPowerMw=powerok).WHERE(NrDuCellId=nrcellid),
                    is_new=True)

    # bts_obj.mod_moc("NRDUCellTrp", MOD(MaxTransmitPower=powerok).WHERE(NrDuCellId=nrcellid))
    bts_obj.mod_moc("NRDUCell", MOD(TrackingAreaId=nr_trackingarea_id).WHERE(NrDuCellId=nrcellid), is_new=True)
    bts_obj.add_moc("NRDUCellTrpBeam", NrDuCellTrpId=ducelltrpid, CoverageScenario="DEFAULT", Tilt=nr_tilt,
                    Azimuth=0, MaxSsbPwrOffset=0, ScenarioBeamAlgoSw=0, ConnModeCoverageScenario="DEFAULT",
                    TrpAntType="DEFAULT")
    bts_obj.mod_moc("NRDUCellTrpBeam", MOD(Tilt=nr_tilt).WHERE(NrDuCellTrpId=ducelltrpid))
    if not bts_obj.get_para_list_from_moc("NRDUCellOp", "NrDuCellId", WHERE(NrDuCellId=nrcellid)):
        bts_obj.add_moc("NRDUCellOp", CellId=nrcellid, CellPrimaryOpFlag=0, CellReservedForOp=0, CellResId=255,
                        NrDuCellId=nrcellid, NrNetworkingOption=3, OperatorId=nr_operator, TrackingAreaId=4294967295)
    else:
        bts_obj.mod_moc("NRDUCellOp", MOD(OperatorId=nr_operator, CellId=nrcellid).WHERE(NrDuCellId=nrcellid),
                        is_new=True)

#neighboring
nrcell_list = bts_obj.get_para_list_from_moc("NRDUCell",["NrDuCellId","PhysicalCellId","SsbFreqPos"],WHERE(DlNarfcn="630000"))
ltecell_list = bts_obj.get_para_list_from_moc("Cell", "LocalCellId",WHERE(NbCellFlag=0))
configure_nrnfreq_list=bts_obj.get_para_list_from_moc("NrNFreq",["LocalCellId","DlArfcn"])
configure_nrnrelationship_list = bts_obj.get_para_list_from_moc("NrNRelationship",["LocalCellId","GnodebId","CellId"])
nrcellrelation_list = bts_obj.get_para_list_from_moc("NRCellRelation",["NrCellId","gNBId","CellId"])
nb_cell_list=bts_obj.get_para_list_from_moc("Cell","LocalCellId",WHERE(NbCellFlag=1))
tp_lte_cell_list=[]
mvs_lte_cell_list=[]
if region=="AMBA":
    tem_lte_cell_list=bts_obj.get_para_list_from_moc("CellOp","LocalCellId",WHERE(TrackingAreaId=0))
    for cell in tem_lte_cell_list:
        if cell not in nb_cell_list:
            tp_lte_cell_list.append(cell)
    tem_lte_cell_list = bts_obj.get_para_list_from_moc("CellOp", "LocalCellId", WHERE(TrackingAreaId=3))
    for cell in tem_lte_cell_list:
        if cell not in nb_cell_list:
            mvs_lte_cell_list.append(cell)
elif region == "SUR":
    tem_lte_cell_list = bts_obj.get_para_list_from_moc("CellOp", "LocalCellId", WHERE(TrackingAreaId=3))
    for cell in tem_lte_cell_list:
        if cell not in nb_cell_list:
            tp_lte_cell_list.append(cell)
    tem_lte_cell_list = bts_obj.get_para_list_from_moc("CellOp", "LocalCellId", WHERE(TrackingAreaId=0))
    for cell in tem_lte_cell_list:
        if cell not in nb_cell_list:
            mvs_lte_cell_list.append(cell)

if region=="AMBA":
    for nrducellid,physicalcellid,ssbfreqpos in tp_newnr_celllist:
        bts_obj.add_moc("NrExternalCell", Mcc="722", Mnc="34", GnodebId=gnodebid, CellId=nrducellid, DlArfcn="629280", UlArfcnConfigInd="NOT_CFG", PhyCellId=physicalcellid, Tac=tacnr, AggregationAttribute=1, MasterPlmnReservedFlag="FALSE", NrNetworkingOption="NSA",FrequencyBand=78,AdditionalFrequencyBand="NULL")
        for ltecellid in tp_lte_cell_list:
            if [ltecellid,gnodebid,nrducellid] not in configure_nrnrelationship_list:
                bts_obj.add_moc("NrNRelationship", LocalCellId=ltecellid, Mcc="722", Mnc="34", GnodebId=gnodebid,
                                CellId=nrducellid, BlindConfigIndicator="FALSE",
                                AggregationAttribute="CONTROL_MODE_FLAG-1&NO_REMOVE_FLAG-1&NO_HO_FLAG-0&CO_DEPLOYMENT_NSA_FLAG-0",
                                NCellAdditionTime="2024-01-01")
                configure_nrnrelationship_list.append([ltecellid,gnodebid,nrducellid])
            if [ltecellid,int(ssbfreqpos)] not in configure_nrnfreq_list:
                bts_obj.add_moc("NrNFreq", LocalCellId=ltecellid, DlArfcn=int(ssbfreqpos), UlArfcnConfigInd="NOT_CFG",
                                ConnFreqPriority="0", FreqSpecificOffset="0", MinRxLevel="-68", NrFreqHighPriReselThld="6",
                                NrFreqLowPriReselThld="6", NrFreqReselPriority="1", SsbOffset="0",
                                SsbMeasurementDuration="5MS",
                                SsbPeriod="20MS", SubcarrierSpacing="30KHZ",
                                AggregationAttribute=11,
                                MaxAllowedTxPower="23", RsQltyThldForCellQltyCalc="-86", MaxRsQtyForCellQltyCalc="16",
                                NrFreqHighPriReselThldRsrq="255", NrFreqLowPriReselThldRsrq="255",
                                NrFreqReselSubPriority="ZERO", VonrPriority="1")
                configure_nrnfreq_list.append([ltecellid,int(ssbfreqpos)])

        # NRCELLRELATION
        for nrducellid2,physicalcellid2,ssbfreqpos2 in tp_newnr_celllist:
            if nrducellid == nrducellid2: continue
            if [nrducellid,gnodebid, nrducellid2] in nrcellrelation_list:continue
            bts_obj.add_moc("NRCellRelation",NrCellId=nrducellid,Mcc="722",Mnc="34",gNBId=gnodebid,CellId=nrducellid2,CellIndividualOffset=15,BlindScellConfigFlag=0,
                            NoHoFlag=0,NoRmvFlag=1,NCellReselOffset=15,NCellClassLabel=0,BlindHoFlag=0,PowerSavingCellFlag=0,MlbHoFlag=0,InterGnodebFlag=0,
                            InterGnodebSulFlag=0,HighSpeedIntrfAvoidFlag=0)
            nrcellrelation_list.append([nrducellid,gnodebid, nrducellid2])
    for nrducellid, physicalcellid, ssbfreqpos in mvs_newnr_celllist:
        bts_obj.add_moc("NrExternalCell", Mcc="722", Mnc="34", GnodebId=gnodebid, CellId=nrducellid, DlArfcn="637440",
                        UlArfcnConfigInd="NOT_CFG", PhyCellId=physicalcellid, Tac=tacnr, AggregationAttribute=1,
                        MasterPlmnReservedFlag="FALSE", NrNetworkingOption="NSA", FrequencyBand=78,
                        AdditionalFrequencyBand="NULL")
        bts_obj.add_moc("NrExternalCellPlmn", Mcc="722", Mnc="34", GnodebId=gnodebid, CellId=nrducellid, SharedMcc="722",SharedMnc="07",NrNetworkingOption=2,Tac=4294967295,SharedPlmnGnodebId=gnodebid,SharedPlmnCellId=nrducellid)
        for ltecellid in mvs_lte_cell_list:
            if [ltecellid, gnodebid, nrducellid] not in configure_nrnrelationship_list:
                bts_obj.add_moc("NrNRelationship", LocalCellId=ltecellid, Mcc="722", Mnc="34", GnodebId=gnodebid,
                                CellId=nrducellid, BlindConfigIndicator="FALSE",
                                AggregationAttribute="CONTROL_MODE_FLAG-1&NO_REMOVE_FLAG-1&NO_HO_FLAG-0&CO_DEPLOYMENT_NSA_FLAG-0",
                                NCellAdditionTime="2024-01-01")
                configure_nrnrelationship_list.append([ltecellid, gnodebid, nrducellid])
            if [ltecellid, int(ssbfreqpos)] not in configure_nrnfreq_list:
                bts_obj.add_moc("NrNFreq", LocalCellId=ltecellid, DlArfcn=int(ssbfreqpos), UlArfcnConfigInd="NOT_CFG",
                                ConnFreqPriority="0", FreqSpecificOffset="0", MinRxLevel="-68",
                                NrFreqHighPriReselThld="6",
                                NrFreqLowPriReselThld="6", NrFreqReselPriority="1", SsbOffset="0",
                                SsbMeasurementDuration="5MS",
                                SsbPeriod="20MS", SubcarrierSpacing="30KHZ",
                                AggregationAttribute=11,
                                MaxAllowedTxPower="23", RsQltyThldForCellQltyCalc="-86", MaxRsQtyForCellQltyCalc="16",
                                NrFreqHighPriReselThldRsrq="255", NrFreqLowPriReselThldRsrq="255",
                                NrFreqReselSubPriority="ZERO", VonrPriority="1")
                configure_nrnfreq_list.append([ltecellid, int(ssbfreqpos)])

        # NRCELLRELATION
        for nrducellid2, physicalcellid2, ssbfreqpos2 in mvs_newnr_celllist:
            if nrducellid == nrducellid2: continue
            if [nrducellid, gnodebid, nrducellid2] in nrcellrelation_list: continue
            bts_obj.add_moc("NRCellRelation", NrCellId=nrducellid, Mcc="722", Mnc="07", gNBId=gnodebid, CellId=nrducellid2,
                            CellIndividualOffset=15, BlindScellConfigFlag=0,
                            NoHoFlag=0, NoRmvFlag=1, NCellReselOffset=15, NCellClassLabel=0, BlindHoFlag=0,
                            PowerSavingCellFlag=0, MlbHoFlag=0, InterGnodebFlag=0,
                            InterGnodebSulFlag=0, HighSpeedIntrfAvoidFlag=0)
            nrcellrelation_list.append([nrducellid, gnodebid, nrducellid2])
elif region=="SUR":
    for nrducellid,physicalcellid,ssbfreqpos in tp_newnr_celllist:
        bts_obj.add_moc("NrExternalCell", Mcc="722", Mnc="07", GnodebId=gnodebid, CellId=nrducellid, DlArfcn="629280", UlArfcnConfigInd="NOT_CFG", PhyCellId=physicalcellid, Tac=tacnr, AggregationAttribute=1, MasterPlmnReservedFlag="FALSE", NrNetworkingOption="NSA",FrequencyBand=78,AdditionalFrequencyBand="NULL")
        bts_obj.add_moc("NrExternalCellPlmn", Mcc="722", Mnc="07", GnodebId=gnodebid, CellId=nrducellid,
                        SharedMcc="722", SharedMnc="34", NrNetworkingOption=2, Tac=4294967295,
                        SharedPlmnGnodebId=gnodebid, SharedPlmnCellId=nrducellid)
        for ltecellid in tp_lte_cell_list:
            if [ltecellid,gnodebid,nrducellid] not in configure_nrnrelationship_list:
                bts_obj.add_moc("NrNRelationship", LocalCellId=ltecellid, Mcc="722", Mnc="07", GnodebId=gnodebid,
                                CellId=nrducellid, BlindConfigIndicator="FALSE",
                                AggregationAttribute="CONTROL_MODE_FLAG-1&NO_REMOVE_FLAG-1&NO_HO_FLAG-0&CO_DEPLOYMENT_NSA_FLAG-0",
                                NCellAdditionTime="2024-01-01")
                configure_nrnrelationship_list.append([ltecellid,gnodebid,nrducellid])
            if [ltecellid,int(ssbfreqpos)] not in configure_nrnfreq_list:
                bts_obj.add_moc("NrNFreq", LocalCellId=ltecellid, DlArfcn=int(ssbfreqpos), UlArfcnConfigInd="NOT_CFG",
                                ConnFreqPriority="0", FreqSpecificOffset="0", MinRxLevel="-68", NrFreqHighPriReselThld="6",
                                NrFreqLowPriReselThld="6", NrFreqReselPriority="1", SsbOffset="0",
                                SsbMeasurementDuration="5MS",
                                SsbPeriod="20MS", SubcarrierSpacing="30KHZ",
                                AggregationAttribute=11,
                                MaxAllowedTxPower="23", RsQltyThldForCellQltyCalc="-86", MaxRsQtyForCellQltyCalc="16",
                                NrFreqHighPriReselThldRsrq="255", NrFreqLowPriReselThldRsrq="255",
                                NrFreqReselSubPriority="ZERO", VonrPriority="1")
                configure_nrnfreq_list.append([ltecellid,int(ssbfreqpos)])

        # NRCELLRELATION
        for nrducellid2,physicalcellid2,ssbfreqpos2 in tp_newnr_celllist:
            if nrducellid == nrducellid2: continue
            if [nrducellid,gnodebid, nrducellid2] in nrcellrelation_list:continue
            bts_obj.add_moc("NRCellRelation",NrCellId=nrducellid,Mcc="722",Mnc="34",gNBId=gnodebid,CellId=nrducellid2,CellIndividualOffset=15,BlindScellConfigFlag=0,
                            NoHoFlag=0,NoRmvFlag=1,NCellReselOffset=15,NCellClassLabel=0,BlindHoFlag=0,PowerSavingCellFlag=0,MlbHoFlag=0,InterGnodebFlag=0,
                            InterGnodebSulFlag=0,HighSpeedIntrfAvoidFlag=0)
            nrcellrelation_list.append([nrducellid,gnodebid, nrducellid2])
    for nrducellid, physicalcellid, ssbfreqpos in mvs_newnr_celllist:
        bts_obj.add_moc("NrExternalCell", Mcc="722", Mnc="07", GnodebId=gnodebid, CellId=nrducellid, DlArfcn="637440",
                        UlArfcnConfigInd="NOT_CFG", PhyCellId=physicalcellid, Tac=tacnr, AggregationAttribute=1,
                        MasterPlmnReservedFlag="FALSE", NrNetworkingOption="NSA", FrequencyBand=78,
                        AdditionalFrequencyBand="NULL")
        for ltecellid in mvs_lte_cell_list:
            if [ltecellid, gnodebid, nrducellid] not in configure_nrnrelationship_list:
                bts_obj.add_moc("NrNRelationship", LocalCellId=ltecellid, Mcc="722", Mnc="07", GnodebId=gnodebid,
                                CellId=nrducellid, BlindConfigIndicator="FALSE",
                                AggregationAttribute="CONTROL_MODE_FLAG-1&NO_REMOVE_FLAG-1&NO_HO_FLAG-0&CO_DEPLOYMENT_NSA_FLAG-0",
                                NCellAdditionTime="2024-01-01")
                configure_nrnrelationship_list.append([ltecellid, gnodebid, nrducellid])
            if [ltecellid, int(ssbfreqpos)] not in configure_nrnfreq_list:
                bts_obj.add_moc("NrNFreq", LocalCellId=ltecellid, DlArfcn=int(ssbfreqpos), UlArfcnConfigInd="NOT_CFG",
                                ConnFreqPriority="0", FreqSpecificOffset="0", MinRxLevel="-68",
                                NrFreqHighPriReselThld="6",
                                NrFreqLowPriReselThld="6", NrFreqReselPriority="1", SsbOffset="0",
                                SsbMeasurementDuration="5MS",
                                SsbPeriod="20MS", SubcarrierSpacing="30KHZ",
                                AggregationAttribute=11,
                                MaxAllowedTxPower="23", RsQltyThldForCellQltyCalc="-86", MaxRsQtyForCellQltyCalc="16",
                                NrFreqHighPriReselThldRsrq="255", NrFreqLowPriReselThldRsrq="255",
                                NrFreqReselSubPriority="ZERO", VonrPriority="1")
                configure_nrnfreq_list.append([ltecellid, int(ssbfreqpos)])

        # NRCELLRELATION
        for nrducellid2, physicalcellid2, ssbfreqpos2 in mvs_newnr_celllist:
            if nrducellid == nrducellid2: continue
            if [nrducellid, gnodebid, nrducellid2] in nrcellrelation_list: continue
            bts_obj.add_moc("NRCellRelation", NrCellId=nrducellid, Mcc="722", Mnc="07", gNBId=gnodebid, CellId=nrducellid2,
                            CellIndividualOffset=15, BlindScellConfigFlag=0,
                            NoHoFlag=0, NoRmvFlag=1, NCellReselOffset=15, NCellClassLabel=0, BlindHoFlag=0,
                            PowerSavingCellFlag=0, MlbHoFlag=0, InterGnodebFlag=0,
                            InterGnodebSulFlag=0, HighSpeedIntrfAvoidFlag=0)
            nrcellrelation_list.append([nrducellid, gnodebid, nrducellid2])
mfbifreq_list = bts_obj.get_para_list_from_moc("NrMfbiFreq","DlArfcn")
if "629280" not in mfbifreq_list and 629280 not in mfbifreq_list:
    bts_obj.add_moc("NrMfbiFreq",DlArfcn="629280",FrequencyBand=78,AdditionalFrequencyBand=0,objId=0)
if "637440" not in mfbifreq_list and 637440 not in mfbifreq_list:
    bts_obj.add_moc("NrMfbiFreq",DlArfcn="637440",FrequencyBand=78,AdditionalFrequencyBand=0,objId=0)

PccFreqCfg_PccDlEarfcn_list = bts_obj.get_para_list_from_moc("PccFreqCfg", "PccDlEarfcn")
SccFreqCfg_config_list = bts_obj.get_para_list_from_moc("SccFreqCfg", ["PccDlEarfcn", "SccDlEarfcn"])
CA_list = bts_obj.get_data_from_excel(excel_name=site_list_filename, sheet_name="CA",
                                      title_row=1, group_title="Site Name",
                                      ne_name="standard")
cell_freq_list  = bts_obj.get_para_list_from_moc("Cell","DlEarfcn",WHERE(WHERE(NbCellFlag=0)))

for CA in CA_list:
    pcc_freq = int(CA.attr("PccDlEarfcn"))
    scc_freq = CA.attr("SccDlEarfcn")
    if pcc_freq not in PccFreqCfg_PccDlEarfcn_list and pcc_freq in cell_freq_list :
        bts_obj.add_moc("PccFreqCfg", PccDlEarfcn=pcc_freq,
                        PreferredPccPriority=CA.attr("PreferredPccPriority"), PccA4RsrpThd=CA.attr("PccA4RsrpThd"),
                        PccA4RsrqThd=CA.attr("PccA4RsrqThd"),
                        NsaPccAnchoringPriority=CA.attr("NsaPccAnchoringPriority"))
        PccFreqCfg_PccDlEarfcn_list.append(pcc_freq)
    elif pcc_freq not in PccFreqCfg_PccDlEarfcn_list and pcc_freq == 66711:
        bts_obj.add_moc("PccFreqCfg", PccDlEarfcn=pcc_freq,
                        PreferredPccPriority=CA.attr("PreferredPccPriority"), PccA4RsrpThd=CA.attr("PccA4RsrpThd"),
                        PccA4RsrqThd=CA.attr("PccA4RsrqThd"),
                        NsaPccAnchoringPriority=CA.attr("NsaPccAnchoringPriority"))
        PccFreqCfg_PccDlEarfcn_list.append(pcc_freq)

    if scc_freq and [pcc_freq, scc_freq] not in SccFreqCfg_config_list and pcc_freq in cell_freq_list and scc_freq in cell_freq_list:
        bts_obj.add_moc("SccFreqCfg", PccDlEarfcn=pcc_freq, SccDlEarfcn=scc_freq,
                        SccPriority=int(CA.attr("SccPriority")), SccA2Offset="0",
                        SccA4Offset="0", BlindScellAddThd=75, BlindScellDelThd=50)
        SccFreqCfg_config_list.append([pcc_freq,scc_freq])
    elif scc_freq and [pcc_freq, scc_freq] not in SccFreqCfg_config_list and pcc_freq == 66711 and scc_freq in cell_freq_list:
        bts_obj.add_moc("SccFreqCfg", PccDlEarfcn=pcc_freq, SccDlEarfcn=scc_freq,
                        SccPriority=int(CA.attr("SccPriority")), SccA2Offset="0",
                        SccA4Offset="0", BlindScellAddThd=75, BlindScellDelThd=50)
        SccFreqCfg_config_list.append([pcc_freq, scc_freq])
    elif scc_freq and [pcc_freq, scc_freq] not in SccFreqCfg_config_list and pcc_freq in cell_freq_list and scc_freq == 77711:
        bts_obj.add_moc("SccFreqCfg", PccDlEarfcn=pcc_freq, SccDlEarfcn=scc_freq,
                        SccPriority=int(CA.attr("SccPriority")), SccA2Offset="0",
                        SccA4Offset="0", BlindScellAddThd=75, BlindScellDelThd=50)
        SccFreqCfg_config_list.append([pcc_freq, scc_freq])
nrscgfreqconfig_list = bts_obj.get_para_list_from_moc("NrScgFreqConfig", ["PccDlEarfcn", "ScgDlArfcn"])
for cell in tp_lte_cell_list:
    lte_freq=bts_obj.get_para_list_from_moc("Cell","DlEarfcn",WHERE(LocalCellId=cell))[0]
    if [lte_freq,"629280"] in nrscgfreqconfig_list:continue
    bts_obj.add_moc("NrScgFreqConfig", PccDlEarfcn=lte_freq, ScgDlArfcn=629280,
                    ScgDlArfcnPriority=5, NsaDcB1ThldRsrp="-112", NrB1TimeToTrigger="40MS",
                    NsaDcSulB1ThldRsrp="-112", AggregationAttribute=0, ForbiddenSpidGrpId=65535,
                    NsaDcLteNrSimulHoThld=0, NrB1ReportWaitingTimer=3, NsaDcB1ThldRsrq="-127")
    nrscgfreqconfig_list.append([lte_freq, "629280"])
for cell in mvs_lte_cell_list:
    lte_freq=bts_obj.get_para_list_from_moc("Cell","DlEarfcn",WHERE(LocalCellId=cell))[0]
    if [lte_freq,"637440"] in nrscgfreqconfig_list:continue
    bts_obj.add_moc("NrScgFreqConfig", PccDlEarfcn=lte_freq, ScgDlArfcn=637440,
                    ScgDlArfcnPriority=5, NsaDcB1ThldRsrp="-105", NrB1TimeToTrigger="40MS",
                    NsaDcSulB1ThldRsrp="-105", AggregationAttribute=0, ForbiddenSpidGrpId=65535,
                    NsaDcLteNrSimulHoThld=0, NrB1ReportWaitingTimer=3, NsaDcB1ThldRsrq="-127")
    nrscgfreqconfig_list.append([lte_freq, "637440"])

for ltecellid in tp_lte_cell_list:
    bts_obj.add_moc("EutranInterNFreq", LocalCellId=ltecellid, DlEarfcn=66711,
                    UlEarfcnCfgInd="NOT_CFG",
                    CellReselPriorityCfgInd="CFG", CellReselPriority=6,
                    EutranReselTime="1",
                    SpeedDependSPCfgInd="NOT_CFG", MeasBandWidth="MBW75",
                    QoffsetFreq="dB0",
                    ThreshXhigh=4,
                    ThreshXlow=4, QRxLevMin="-62", PmaxCfgInd="NOT_CFG",
                    NeighCellConfig="BitString01",
                    PresenceAntennaPort1="BOOLEAN_FALSE", InterFreqHoEventType="EventA4",
                    ThreshXhighQ="0",
                    ThreshXlowQ="0", QqualMinCfgInd="NOT_CFG", ConnFreqPriority="0",
                    MlbTargetInd="ALLOWED",
                    FreqPriBasedHoMeasFlag="DISABLE", IdleMlbUEReleaseRatio="0",
                    MlbFreqPriority="7",
                    DlFreqOffset="NEG_0DOT5", QoffsetFreqConn="dB0", MeasFreqPriority="0",
                    IfHoThdRsrpOffset="6", IfMlbThdRsrpOffset="0", MasterBandFlag="FALSE",
                    InterFreqRanSharingInd="BOOLEAN_TRUE",
                    InterFreqHighSpeedFlag="LOW_SPEED",
                    AnrInd="ALLOWED",
                    VoipPriority="1", PsPriority="1", VolteHoTargetInd="ALLOWED",
                    FreqPriorityForAnr="0",
                    BackoffTargetInd="NOT_ALLOWED", MlbInterFreqHoEventType="EventA4",
                    MobilityTargetInd="SpeedMobilityTargetInd-0&LcsMobilityTargetInd-0",
                    MlbInterFreqEffiRatio="100", SnrBasedUeSelectionMode="Random",
                    UlTrafficMlbTargetInd="NOT_ALLOWED", UlTrafficMlbPriority="7",
                    MlbInterFreqHoA3Offset="-2",
                    IfSrvHoThdRsrpOffset="0", IfSrvHoThdRsrqOffset="0",
                    MlbFreqUlPriority="7",
                    InterFreqMlbDlPrbOffset="0", InterFreqMlbUlPrbOffset="0",
                    NcellNumForAnr="0",
                    MeasPerformanceDemand="NORMAL", IfBackoffThdRsrpOffset="0",
                    IfBackoffThdRsrqOffset="0",
                    VoLTEQualityIfHoTargetInd="ALLOWED", IdleMlbeMtcUEReleaseRatio="0",
                    InterFreqCioAdjLimitCfgInd="NOT_CFG", InterFreq4TInd="FREQ2T",
                    CtrlMode="AUTO_MODE",
                    MeasPriorityForFreqPriHo="0", EmtcInterFreqCellReselPri="255",QRxLevMinForCeModeA="-70")

userplanepeer_used_list = bts_obj.get_para_list_from_moc("EPGROUP",["USERPLANEPEERREFS","SCTPPEERREFS"])
uppeer_list = []
cppeer_list = []
userplanepeer_list = bts_obj.get_para_list_from_moc("USERPLANEPEER", "UPPEERID")
sctppeer_list = bts_obj.get_para_list_from_moc("SCTPPEER", "SCTPPEERID")
for uplist,cplist in userplanepeer_used_list:
    if uplist:
        for upid in uplist:
            uppeer_list.append(upid.UPPEERID)
    if cplist:
        for cpid in cplist:
            cppeer_list.append(cpid.SCTPPEERID)

for peer_id in userplanepeer_list:
    if peer_id not in uppeer_list:
        bts_obj.del_moc("USERPLANEPEER",WHERE(UPPEERID=peer_id))
for peer_id in sctppeer_list:
    if peer_id not in cppeer_list:
        bts_obj.del_moc("SCTPPEER",WHERE(SCTPPEERID=peer_id))

new_nr_name = siteinfo.attr("*gNodeB Name")
if new_nr_name:
    bts_obj.mod_moc("gNodeBFunction", MOD(gNodeBFunctionName=new_nr_name, ApplicationRef=4))
bts_obj.mod_moc("TASM", MOD(SRCNO=0, CLKSRC=0, CLKSYNCMODE=1),is_new=True)
if not bts_obj.get_para_list_from_moc("NCellPlmnList","Mcc",WHERE(Mnc="34")):
    bts_obj.add_moc("NCellPlmnList",Mcc="722",Mnc="34",RatType=3,PlmnListType=2,gNBIdLength=22)
else:
    bts_obj.mod_moc("NCellPlmnList", MOD(Mcc=722, Mnc="34", RatType=3, PlmnListType=2, gNBIdLength=22).WHERE(Mnc="34"),is_new=True)
if not bts_obj.get_para_list_from_moc("NCellPlmnList","Mcc",WHERE(Mnc="07")):
    bts_obj.add_moc("NCellPlmnList",Mcc="722",Mnc="07",RatType=3,PlmnListType=2,gNBIdLength=22)
else:
    bts_obj.mod_moc("NCellPlmnList", MOD(Mcc=722, Mnc="07", RatType=3, PlmnListType=2, gNBIdLength=22).WHERE(Mnc="07"),is_new=True)

if not bts_obj.get_para_list_from_moc("RlcPdcpParaGroup","RlcPdcpParaGroupId",WHERE(RlcPdcpParaGroupId=208)):
    bts_obj.add_moc("RlcPdcpParaGroup",RlcPdcpParaGroupId=208,RlcMode=1,RlcParaAdaptSwitch=1,UlDlDiscardtimerSwitch=0,AmPdcpSnSize="AmPdcpSnsize_18bits")
else:
    bts_obj.mod_moc("RlcPdcpParaGroup", MOD(RlcMode=1, RlcParaAdaptSwitch=1, UlDlDiscardtimerSwitch=0,AmPdcpSnSize="AmPdcpSnsize_18bits").WHERE(RlcPdcpParaGroupId=208),is_new=True)

#if regreg == "AMBA":

bts_obj.set_moc("gNBUeInfo", UeInfoIndex="3", UeInfoType="UE_FEATUREVALUE", UeFeatureValueContent="ec7fee769ff7e0fff0",UeFeatureValueMask="FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", UeTypeDesc="Redmi Note 10 pro")

###########################################################################################
# Check and Correct Part
# bts_obj.check_and_correct_Data()

# Create NE and NODE
bts_obj.mod_moc("NE", MOD(NENAME=bts_obj.NEName))

bts_obj.mod_moc('NODE', MOD(NODENAME=bts_obj.NEName, PRODUCTTYPE=siteinfo.attr("*Product Type"), NODEID=1, WM="CONCURRENT"))

bts_obj.mod_moc("EQUIPMENT", MOD(EQUIPMENTTY=siteinfo.attr("*Product Type")))

#baseline
audit_parameter_list = bts_obj.get_data_from_excel(excel_name=site_list_filename, sheet_name="Baseline",
                                                       title_row=1, group_title="Site Name", ne_name="Standard")
for audit_parameter in audit_parameter_list:
    if audit_parameter.attr("Audit") == "NO":continue
    MO = audit_parameter.attr("MO")
    Parameter = audit_parameter.attr("Parameter")
    Filter1 = audit_parameter.attr("Filter1")
    Target_Value = str(audit_parameter.attr("Target Value"))
    switch = audit_parameter.attr("Switch")
    if switch:
        Target_Value = switch + "-" + Target_Value
    if Target_Value == "False":
        Target_Value = "FALSE"
    if Target_Value == "True":
        Target_Value = "TRUE"
    if Target_Value == "None":
        Target_Value = "NONE"
    parameter_filter = {}
    parameter_modify = {Parameter: Target_Value}
    Technology = audit_parameter.attr("Technology")
    Related_mo = audit_parameter.attr("Related filter MO")
    Related_filter = audit_parameter.attr("Related filter parameter")
    Related_filter_value = audit_parameter.attr("Related filter value")
    id_parameter = audit_parameter.attr("id parameter")
    id_filter_parameter = audit_parameter.attr("id filter parameter")
    Related_filter_combine = {}
    filter_id_list = []
    if Related_mo:
        Related_filter_split = Related_filter.split(";")
        Related_filter_value_split = Related_filter_value.split(";")
        for i in range(len(Related_filter_split)):
            Related_filter_combine[Related_filter_split[i]] = int(Related_filter_value_split[i])
        filter_id_list = bts_obj.get_para_list_from_moc(Related_mo, id_filter_parameter,
                                                        WHERE(**Related_filter_combine))
        Related_filter_combine = {}
        for i in range(len(Related_filter_split)):
            Related_filter_combine[Related_filter_split[i]] = Related_filter_value_split[i]
        filter_id_list2 = bts_obj.get_para_list_from_moc(Related_mo, id_filter_parameter,
                                                         WHERE(**Related_filter_combine))
        filter_id_list = filter_id_list + filter_id_list2

    if id_parameter:
        id_parameter_value = audit_parameter.attr("id value")
        if id_parameter_value:
            id_parameter_Value_list = id_parameter_value.split(";")
        else:
            id_parameter_Value_list=[]
        for id_value in id_parameter_Value_list:
            if not id_value: continue
            id_value = int(id_value)
            parameter_filter[id_parameter] = id_value
            if Filter1:
                Filter1_Value_total = audit_parameter.attr("Filter1 Value")
                Filter1_Value_list = Filter1_Value_total.split(";")
                for Filter1_Value in Filter1_Value_list:
                    Filter1_Value = int(Filter1_Value)
                    parameter_filter[Filter1] = Filter1_Value
                    if Related_mo and filter_id_list:
                        for filterid in filter_id_list:
                            if filterid != id_value: continue
                            parameter_filter[id_parameter] = filterid
                            config_value_list = bts_obj.get_para_list_from_moc(MO, [id_parameter, Parameter],
                                                                               WHERE(**parameter_filter))
                            if config_value_list:
                                for id, config_value in config_value_list:
                                    if config_value == None: continue
                                    change_parameters(switch, MO, Parameter, id, config_value, Target_Value,
                                                          parameter_modify, Technology, id_parameter,
                                                          parameter_filter)
                    elif not Related_mo:
                        config_value_list = bts_obj.get_para_list_from_moc(MO, [id_parameter, Parameter],
                                                                           WHERE(**parameter_filter))

                        if config_value_list:
                            for id, config_value in config_value_list:

                                if config_value == None: continue
                                change_parameters(switch, MO, Parameter, id, config_value, Target_Value,
                                                      parameter_modify, Technology, id_parameter,
                                                      parameter_filter)
                    else:
                        pass

            else:
                if Related_mo and filter_id_list:
                    for filterid in filter_id_list:
                        if filterid != id_value: continue
                        parameter_filter[id_parameter] = filterid
                        config_value_list = bts_obj.get_para_list_from_moc(MO, [id_parameter, Parameter],
                                                                           WHERE(**parameter_filter))
                        if config_value_list:
                            for id, config_value in config_value_list:
                                if config_value == None: continue
                                change_parameters(switch, MO, Parameter, id, config_value, Target_Value,
                                                      parameter_modify, Technology, id_parameter,
                                                      parameter_filter)
                elif not Related_mo:
                    config_value_list = bts_obj.get_para_list_from_moc(MO, [id_parameter, Parameter],
                                                                       WHERE(**parameter_filter))

                    if config_value_list:
                        for id, config_value in config_value_list:
                            if config_value == None: continue
                            change_parameters(switch, MO, Parameter, id, config_value, Target_Value,
                                                  parameter_modify, Technology, id_parameter,
                                                  parameter_filter)


    else:
        config_value_list = bts_obj.get_para_list_from_moc(MO, Parameter, WHERE(**parameter_filter))
        if MO == "NrNfreq":
            print(config_value_list)
        if config_value_list:
            for config_value in config_value_list:
                if config_value == None:
                    config_value = 0
                id = ""
                change_parameters(switch, MO, Parameter, id, config_value, Target_Value,
                                                    parameter_modify, Technology, id_parameter,
                                                  parameter_filter)
for cell in nb_cell_list:
    bts_obj.mod_moc("NsaDcMgmtConfig",MOD(NsaDcAlgoSwitch="NSA_DC_CAPABILITY_SWITCH-0").WHERE(LocalCellId=cell))
if 1 not in bts_obj.get_para_list_from_moc("SCTPTEMPLATE", "SCTPTEMPLATEID"):
    bts_obj.add_moc("SCTPTEMPLATE", SCTPTEMPLATEID=1)
if gnodebid:
    bts_obj.mod_moc("IPCLKLNK", MOD(PROFILETYPE="1588V2"))

bts_obj.mod_moc("NRDUCellTrp", MOD(PowerConfigMode="TRANSMIT_POWER_MW").WHERE(NrDuCellId=350))
bts_obj.mod_moc("NRDUCellTrp", MOD(PowerConfigMode="TRANSMIT_POWER_MW").WHERE(NrDuCellId=351))
bts_obj.mod_moc("NRDUCellTrp", MOD(PowerConfigMode="TRANSMIT_POWER_MW").WHERE(NrDuCellId=352))

bts_obj.finish()