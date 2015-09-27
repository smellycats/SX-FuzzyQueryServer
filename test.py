# -*- coding: utf-8 -*-

#车牌号码分解
def decompose_hphm(hphm):
    if hphm == '' or hphm == '-':
        return None
    p_list = []
    fix_hphm = '%s_' % hphm
    for i in range(len(hphm)):
        p_list.append(fix_hphm[i:i+2])
    return p_list

def built_hphm(hphm):
    hphm += '_'
    area = 1
    flag = ''  
    count = 0
    _count = 0
    wordflag = True
    plate_l = []

    for i in hphm:
        if i == '%':
            if flag == '':
                area += 1
                count +=1
            elif flag == '%':
                pass
            elif flag == '_':
                count -= _count
                _count = 0
                area += 1
                if len(plate_l) == 0:
                    count +=1
            else:
                if area == 1:
                    if count != 1:
                        plate_l.append({'num': 1, 'area': area, 'position': count,
                                        'section': flag+'_', 'weight': 10+count})
                else:
                    plate_l.append({'num': 1, 'area': area, 'position': count,
                                    'section': flag+'_', 'weight': count})
                area +=1
            wordflag = False
        elif i == '_':
            if flag == '':
                count += 1
                _count += 1
            elif flag == '%':
                pass
            elif flag == '_':
                if wordflag:
                    count += 1
                    _count += 1
            else:
                if area == 1:
                    if count != 1:
                        plate_l.append({'num': 1, 'area': area, 'position': count,
                                        'section': flag+'_', 'weight': 10+count})
                else:
                    plate_l.append({'num': 1, 'area': area, 'position': count,
                                    'section': flag+'_', 'weight': count})
                count +=1
                _count +=1

        else:
            if flag == '':
                count += 1
            elif flag=='%':
                count += 1
            elif flag=='_':
                if wordflag == False:
                    count -= _count
                count += 1
            else:
                if area == 1:
                    if count != 1:
                        plate_l.append({'num': 2, 'area': area, 'position': count,
                                        'section': flag+i, 'weight': count+30})
                else:
                    plate_l.append({'num': 2, 'area': area, 'position': count,
                                    'section': flag+i, 'weight': count+20})
                count +=1
            wordflag = True
            _count = 0
        flag = i

    return sorted(plate_l, key=lambda x:x['weight'], reverse=True)

def test():
    plate_list = [{'num':2, 'area': 1, 'count': 3, 'section': u'L2', 'weight': 12}, {'num':2, 'area': 1, 'count': 3, 'section': u'L1', 'weight': 22}]
    return sorted(plate_list,key=lambda x:x['weight'],reverse=True)

def bulit_hphm2(hphm):
    hphm_list = hphm.split('%')
    hphm_segment_list = []
    hphm_len = 0
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
                    return {'h': seg['segment'], 'f': False, 'l': hphm_len,
                            'p': p+seg['pos'] + i}
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
            
    
if __name__ == '__main__':
    #print decompose_hphm(u'粤L12345')
    #print built_hphm(u'粤L%234_%')
    #print test()
    #print find_hphm_segment(u'L23_')
    print bulit_hphm2(u'粤%L_21%2_')
