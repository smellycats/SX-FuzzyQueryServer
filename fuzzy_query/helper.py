# -*- coding: utf-8 -*-

#车牌号码分解
def decompose_hphm(hphm):
    if hphm == '' or hphm == '-':
        return None
    hphm_segment_list = []
    fix_hphm = '%s_' % hphm
    for i in range(len(hphm)):
        hphm_segment_list.append(fix_hphm[i:i+2])
    return hphm_segment_list

def bulit_hphm(hphm):
    hphm_list = hphm.split('%')
    hphm_segment_list = []
    hphm_len = 0
    print hphm_list
    if len(hphm_list) == 1:
        seg = find_hphm_segment(hphm_list[0])
        if seg:
            return {'h': seg['segment'], 'f': False, 'p': seg['pos'],
                    'l': len(hphm_list[0])}
    else:
        # 删除每节的多余的'_'
        hphm_list[0] = hphm_list[0].rstrip('_')
        hphm_list[-1] = hphm_list[-1].lstrip('_')
        for i in range(1, len(hphm_list)-1):
            hphm_list[i] = hphm_list[i].strip('_')
        # 计算车牌号码长度
        for i in hphm_list:
            hphm_len += len(i)
        # 权重
        w_flag = 0
        if hphm_list[0] != '':
            head = find_hphm_segment(hphm_list[0])
            if head:
                if head['pos'] == 0:
                    w_flag = 1
                elif head['pos'] == 1:
                    w_flag = 20
                else:
                    return {'h': head['segment'], 'f': False, 'p': head['pos'],
                            'l': hphm_len}
        if hphm_list[-1] != '':
            tail = find_hphm_segment(hphm_list[-1])
            if tail:
                return {'h': tail['segment'], 'f': False, 'l': hphm_len,
                        'p': 5 - (len(hphm_list[-1]) - tail['pos'] - 2)}
        if w_flag == 20:
            return {'h': head['segment'], 'f': False, 'p': head['pos'],
                    'l': hphm_len}
        for i in range(1, len(hphm_list) - 1):
            if hphm_list[i] != '':
                seg = find_hphm_segment(hphm_list[i])
                if seg:
                    p = 0
                    for j in range(0, i):
                        p += len(hphm_list[j])
                    return {'h': seg['segment'], 'f': True, 'l': hphm_len,
                            'p': p + seg['pos']}
    return None
            
            
def find_hphm_segment(hphm_section):
    # 上一位车牌字符 char
    pre_h = ''
    # 字符位置 int
    pos = 0
    # 车牌号码片段 list
    hphm_segment_list = []
    for i in hphm_section:
        if pre_h == '' or pre_h == '_' or i == '_':
            pass
        else:
            hphm_segment_list.append({'segment': pre_h + i, 'pos': pos - 1})
        pre_h = i
        pos += 1
    
    if len(hphm_segment_list) >= 1:
        return hphm_segment_list[-1]
    else:
        return None
