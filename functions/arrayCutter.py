# !/usr/bin/python3
# -*- coding: utf-8 -*-

from functions.array2string import array2string, linear_array2string


def arrayCutter(arr, good_values=1, in_row=3, summ=3, offset=0, debug=False):
    cutter = {
        'data': [],
        'index_begin': -1,
        'index_end': -1
    }

    flag_begin = flag_end = False

    temp = ''
    for i in range(in_row):
        temp += str(good_values)

    rowIndex = 0
    data = []
    index_begin = -1
    index_end = -1
    old_summ = 0
    for i in range(offset, len(arr)):
        flag_Append = False
        row = arr[i]
        col_summ = sum(row)

        tinr = linear_array2string(row, '')
        if tinr.find(temp) > -1:
            flag_Append = True

        if not flag_begin:
            if flag_Append and col_summ >= summ:
                # if old_summ > summ:
                flag_begin = True
                index_begin = i
                data.append(row)
        else:
            if not flag_end:
                if col_summ <= summ:
                    flag_end = False
                    index_end = i - 1
                    break
                else:
                    data.append(row)

        if (debug):
            print(
                f"[{rowIndex}] col_summ={col_summ}, flag_Append={flag_Append}, begin={flag_begin}, end={flag_end}, ib={index_begin}, ie={index_end}, old_summ={old_summ}, temp={temp}")
            print(row)
            print('')

        rowIndex += 1
        old_summ = col_summ

    cutter['data'] = data
    cutter['index_begin'] = index_begin
    cutter['index_end'] = index_end

    return cutter
