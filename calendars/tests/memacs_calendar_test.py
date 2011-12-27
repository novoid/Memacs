# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import unittest
import sys
import os
sys.path.append(
      os.path.dirname(
            os.path.dirname(
                  os.path.dirname(
                        os.path.abspath(__file__)))))
from calendars.memacs_calendar import CalendarMemacs


class TestCalendar(unittest.TestCase):

    def test_all(self):
        test_file = os.path.dirname(os.path.abspath(__file__)) + \
        os.sep + "austrian_holidays_from_google.ics"
        argv = "-s -cf " + test_file
        memacs = CalendarMemacs(argv=argv.split(), append=True)
        data = memacs.test_get_entries()
        #for d in range(len(data)):
        #      print "self.assertEqual(\n\tdata[%d],\n\t \"%s\")" % \
        #            (d, data[d])
        self.assertEqual(
             data[0],
             "** Whit Monday")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :SUMMARY: Whit Monday")
        self.assertEqual(
            data[3],
             "   :CREATED: <2012-05-28 Mon>--<2012-05-28 Mon>")
        self.assertEqual(
            data[4],
             "   :ID:      6af338d85769b094123b935301adff56bc1a6ae7")
        self.assertEqual(
            data[5],
             "   :END:")
        self.assertEqual(
            data[6],
             "** Valentine's day")
        self.assertEqual(
            data[7],
             "   :PROPERTIES:")
        self.assertEqual(
            data[8],
             "   :SUMMARY: Valentine's day")
        self.assertEqual(
            data[9],
             "   :CREATED: <2011-02-14 Mon>--<2011-02-14 Mon>")
        self.assertEqual(
            data[10],
             "   :ID:      7aa936d548f447b800aedd9b45c7613d6490d6f1")
        self.assertEqual(
            data[11],
             "   :END:")
        self.assertEqual(
            data[12],
             "** Valentine's day")
        self.assertEqual(
            data[13],
             "   :PROPERTIES:")
        self.assertEqual(
            data[14],
             "   :SUMMARY: Valentine's day")
        self.assertEqual(
            data[15],
             "   :CREATED: <2010-02-14 Sun>--<2010-02-14 Sun>")
        self.assertEqual(
            data[16],
             "   :ID:      4843bb393609c2052a523454d076eea24cf29b12")
        self.assertEqual(
            data[17],
             "   :END:")
        self.assertEqual(
            data[18],
             "** Valentine's day")
        self.assertEqual(
            data[19],
             "   :PROPERTIES:")
        self.assertEqual(
            data[20],
             "   :SUMMARY: Valentine's day")
        self.assertEqual(
            data[21],
             "   :CREATED: <2012-02-14 Tue>--<2012-02-14 Tue>")
        self.assertEqual(
            data[22],
             "   :ID:      73d45ec59c126a09ecaddc4a633eac70788fe55e")
        self.assertEqual(
            data[23],
             "   :END:")
        self.assertEqual(
            data[24],
             "** St. Stephan's Day")
        self.assertEqual(
            data[25],
             "   :PROPERTIES:")
        self.assertEqual(
            data[26],
             "   :SUMMARY: St. Stephan's Day")
        self.assertEqual(
            data[27],
             "   :CREATED: <2012-12-26 Wed>--<2012-12-26 Wed>")
        self.assertEqual(
            data[28],
             "   :ID:      0093d67f0626c773bc4e7752ddd8215c69d85b78")
        self.assertEqual(
            data[29],
             "   :END:")
        self.assertEqual(
            data[30],
             "** St. Stephan's Day")
        self.assertEqual(
            data[31],
             "   :PROPERTIES:")
        self.assertEqual(
            data[32],
             "   :SUMMARY: St. Stephan's Day")
        self.assertEqual(
            data[33],
             "   :CREATED: <2010-12-26 Sun>--<2010-12-26 Sun>")
        self.assertEqual(
            data[34],
             "   :ID:      e4acad60429fc6931e8b07b6435f9e880e712f4c")
        self.assertEqual(
            data[35],
             "   :END:")
        self.assertEqual(
            data[36],
             "** St. Stephan's Day")
        self.assertEqual(
            data[37],
             "   :PROPERTIES:")
        self.assertEqual(
            data[38],
             "   :SUMMARY: St. Stephan's Day")
        self.assertEqual(
            data[39],
             "   :CREATED: <2011-12-26 Mon>--<2011-12-26 Mon>")
        self.assertEqual(
            data[40],
             "   :ID:      8561d085065fe7761734e4045695d5303ce638db")
        self.assertEqual(
            data[41],
             "   :END:")
        self.assertEqual(
            data[42],
             "** St. Nicholas")
        self.assertEqual(
            data[43],
             "   :PROPERTIES:")
        self.assertEqual(
            data[44],
             "   :SUMMARY: St. Nicholas")
        self.assertEqual(
            data[45],
             "   :CREATED: <2011-12-06 Tue>--<2011-12-06 Tue>")
        self.assertEqual(
            data[46],
             "   :ID:      20ecf62b7060eb4ca67f5fbef88f7bfbbfccec98")
        self.assertEqual(
            data[47],
             "   :END:")
        self.assertEqual(
            data[48],
             "** St. Nicholas")
        self.assertEqual(
            data[49],
             "   :PROPERTIES:")
        self.assertEqual(
            data[50],
             "   :SUMMARY: St. Nicholas")
        self.assertEqual(
            data[51],
             "   :CREATED: <2010-12-06 Mon>--<2010-12-06 Mon>")
        self.assertEqual(
            data[52],
             "   :ID:      f416e41d1c8861a5c63c04018fdf96c81585a648")
        self.assertEqual(
            data[53],
             "   :END:")
        self.assertEqual(
            data[54],
             "** St. Nicholas")
        self.assertEqual(
            data[55],
             "   :PROPERTIES:")
        self.assertEqual(
            data[56],
             "   :SUMMARY: St. Nicholas")
        self.assertEqual(
            data[57],
             "   :CREATED: <2012-12-06 Thu>--<2012-12-06 Thu>")
        self.assertEqual(
            data[58],
             "   :ID:      755c68435e857fd16d05fe5ae0ed59ff30bf741a")
        self.assertEqual(
            data[59],
             "   :END:")
        self.assertEqual(
            data[60],
             "** New Year's Eve")
        self.assertEqual(
            data[61],
             "   :PROPERTIES:")
        self.assertEqual(
            data[62],
             "   :SUMMARY: New Year's Eve")
        self.assertEqual(
            data[63],
             "   :CREATED: <2011-12-31 Sat>--<2011-12-31 Sat>")
        self.assertEqual(
            data[64],
             "   :ID:      fa7e41df6cb647201cbdf92cb8877cf420feb6b2")
        self.assertEqual(
            data[65],
             "   :END:")
        self.assertEqual(
            data[66],
             "** New Year's Eve")
        self.assertEqual(
            data[67],
             "   :PROPERTIES:")
        self.assertEqual(
            data[68],
             "   :SUMMARY: New Year's Eve")
        self.assertEqual(
            data[69],
             "   :CREATED: <2010-12-31 Fri>--<2010-12-31 Fri>")
        self.assertEqual(
            data[70],
             "   :ID:      8c3023300f8f40f99269c48bd01e6105fdf2704b")
        self.assertEqual(
            data[71],
             "   :END:")
        self.assertEqual(
            data[72],
             "** New Year")
        self.assertEqual(
            data[73],
             "   :PROPERTIES:")
        self.assertEqual(
            data[74],
             "   :SUMMARY: New Year")
        self.assertEqual(
            data[75],
             "   :CREATED: <2012-01-01 Sun>--<2012-01-01 Sun>")
        self.assertEqual(
            data[76],
             "   :ID:      968c728cea249df38089224672959b6afe7b5bff")
        self.assertEqual(
            data[77],
             "   :END:")
        self.assertEqual(
            data[78],
             "** New Year")
        self.assertEqual(
            data[79],
             "   :PROPERTIES:")
        self.assertEqual(
            data[80],
             "   :SUMMARY: New Year")
        self.assertEqual(
            data[81],
             "   :CREATED: <2010-01-01 Fri>--<2010-01-01 Fri>")
        self.assertEqual(
            data[82],
             "   :ID:      48f54539a3bd2370c8537e24f45026ef9787697d")
        self.assertEqual(
            data[83],
             "   :END:")
        self.assertEqual(
            data[84],
             "** New Year")
        self.assertEqual(
            data[85],
             "   :PROPERTIES:")
        self.assertEqual(
            data[86],
             "   :SUMMARY: New Year")
        self.assertEqual(
            data[87],
             "   :CREATED: <2011-01-01 Sat>--<2011-01-01 Sat>")
        self.assertEqual(
            data[88],
             "   :ID:      4685f2c7176a0be2ed79310624f30ba59e5abe37")
        self.assertEqual(
            data[89],
             "   :END:")
        self.assertEqual(
            data[90],
             "** National Holiday")
        self.assertEqual(
            data[91],
             "   :PROPERTIES:")
        self.assertEqual(
            data[92],
             "   :SUMMARY: National Holiday")
        self.assertEqual(
            data[93],
             "   :CREATED: <2010-10-26 Tue>--<2010-10-26 Tue>")
        self.assertEqual(
            data[94],
             "   :ID:      461062af066b57f70fa7f80d2d94a12669ab1299")
        self.assertEqual(
            data[95],
             "   :END:")
        self.assertEqual(
            data[96],
             "** National Holiday")
        self.assertEqual(
            data[97],
             "   :PROPERTIES:")
        self.assertEqual(
            data[98],
             "   :SUMMARY: National Holiday")
        self.assertEqual(
            data[99],
             "   :CREATED: <2012-10-26 Fri>--<2012-10-26 Fri>")
        self.assertEqual(
            data[100],
             "   :ID:      ae66a7e7b3fb5284ac6a95b93aa3cb89a4a28fe6")
        self.assertEqual(
            data[101],
             "   :END:")
        self.assertEqual(
            data[102],
             "** National Holiday")
        self.assertEqual(
            data[103],
             "   :PROPERTIES:")
        self.assertEqual(
            data[104],
             "   :SUMMARY: National Holiday")
        self.assertEqual(
            data[105],
             "   :CREATED: <2011-10-26 Wed>--<2011-10-26 Wed>")
        self.assertEqual(
            data[106],
             "   :ID:      aee60ae61038ecd5232a80e752cd41d097157daf")
        self.assertEqual(
            data[107],
             "   :END:")
        self.assertEqual(
            data[108],
             "** Labour Day")
        self.assertEqual(
            data[109],
             "   :PROPERTIES:")
        self.assertEqual(
            data[110],
             "   :SUMMARY: Labour Day")
        self.assertEqual(
            data[111],
             "   :CREATED: <2011-05-01 Sun>--<2011-05-01 Sun>")
        self.assertEqual(
            data[112],
             "   :ID:      951763429457df8da1244af40b91da368c2041c3")
        self.assertEqual(
            data[113],
             "   :END:")
        self.assertEqual(
            data[114],
             "** Labour Day")
        self.assertEqual(
            data[115],
             "   :PROPERTIES:")
        self.assertEqual(
            data[116],
             "   :SUMMARY: Labour Day")
        self.assertEqual(
            data[117],
             "   :CREATED: <2010-05-01 Sat>--<2010-05-01 Sat>")
        self.assertEqual(
            data[118],
             "   :ID:      6aff3ac374d4930dd339714dec95372e2e050ebf")
        self.assertEqual(
            data[119],
             "   :END:")
        self.assertEqual(
            data[120],
             "** Labour Day")
        self.assertEqual(
            data[121],
             "   :PROPERTIES:")
        self.assertEqual(
            data[122],
             "   :SUMMARY: Labour Day")
        self.assertEqual(
            data[123],
             "   :CREATED: <2012-05-01 Tue>--<2012-05-01 Tue>")
        self.assertEqual(
            data[124],
             "   :ID:      a3c13b7c8a6a1fcef43a00d1d203b6442b3a8dbd")
        self.assertEqual(
            data[125],
             "   :END:")
        self.assertEqual(
            data[126],
             "** Immaculate Conception")
        self.assertEqual(
            data[127],
             "   :PROPERTIES:")
        self.assertEqual(
            data[128],
             "   :SUMMARY: Immaculate Conception")
        self.assertEqual(
            data[129],
             "   :CREATED: <2012-12-08 Sat>--<2012-12-08 Sat>")
        self.assertEqual(
            data[130],
             "   :ID:      2ef0b570c0c2dd3c293fffd111f6f90bd4972e26")
        self.assertEqual(
            data[131],
             "   :END:")
        self.assertEqual(
            data[132],
             "** Immaculate Conception")
        self.assertEqual(
            data[133],
             "   :PROPERTIES:")
        self.assertEqual(
            data[134],
             "   :SUMMARY: Immaculate Conception")
        self.assertEqual(
            data[135],
             "   :CREATED: <2010-12-08 Wed>--<2010-12-08 Wed>")
        self.assertEqual(
            data[136],
             "   :ID:      bd0f3b4bcf60d2afcacc9940a0c2ed6b7a11c2d0")
        self.assertEqual(
            data[137],
             "   :END:")
        self.assertEqual(
            data[138],
             "** Immaculate Conception")
        self.assertEqual(
            data[139],
             "   :PROPERTIES:")
        self.assertEqual(
            data[140],
             "   :SUMMARY: Immaculate Conception")
        self.assertEqual(
            data[141],
             "   :CREATED: <2011-12-08 Thu>--<2011-12-08 Thu>")
        self.assertEqual(
            data[142],
             "   :ID:      fb8c0af3c35c5d28419e0a6d6d5b4c7df45a9c95")
        self.assertEqual(
            data[143],
             "   :END:")
        self.assertEqual(
            data[144],
             "** Good Friday")
        self.assertEqual(
            data[145],
             "   :PROPERTIES:")
        self.assertEqual(
            data[146],
             "   :SUMMARY: Good Friday")
        self.assertEqual(
            data[147],
             "   :CREATED: <2012-04-06 Fri>--<2012-04-06 Fri>")
        self.assertEqual(
            data[148],
             "   :ID:      caf7269a74354304102fa9b76046567279a0bd23")
        self.assertEqual(
            data[149],
             "   :END:")
        self.assertEqual(
            data[150],
             "** Epiphany")
        self.assertEqual(
            data[151],
             "   :PROPERTIES:")
        self.assertEqual(
            data[152],
             "   :SUMMARY: Epiphany")
        self.assertEqual(
            data[153],
             "   :CREATED: <2010-01-06 Wed>--<2010-01-06 Wed>")
        self.assertEqual(
            data[154],
             "   :ID:      d7de6d17564f0b2856d96469853694adc33a640c")
        self.assertEqual(
            data[155],
             "   :END:")
        self.assertEqual(
            data[156],
             "** Epiphany")
        self.assertEqual(
            data[157],
             "   :PROPERTIES:")
        self.assertEqual(
            data[158],
             "   :SUMMARY: Epiphany")
        self.assertEqual(
            data[159],
             "   :CREATED: <2012-01-06 Fri>--<2012-01-06 Fri>")
        self.assertEqual(
            data[160],
             "   :ID:      a96bf370fd121df1d6d02631bbd7f0a5b2c53654")
        self.assertEqual(
            data[161],
             "   :END:")
        self.assertEqual(
            data[162],
             "** Epiphany")
        self.assertEqual(
            data[163],
             "   :PROPERTIES:")
        self.assertEqual(
            data[164],
             "   :SUMMARY: Epiphany")
        self.assertEqual(
            data[165],
             "   :CREATED: <2011-01-06 Thu>--<2011-01-06 Thu>")
        self.assertEqual(
            data[166],
             "   :ID:      230403cb069237eabaac46b24798878057f886bb")
        self.assertEqual(
            data[167],
             "   :END:")
        self.assertEqual(
            data[168],
             "** Easter Monday")
        self.assertEqual(
            data[169],
             "   :PROPERTIES:")
        self.assertEqual(
            data[170],
             "   :SUMMARY: Easter Monday")
        self.assertEqual(
            data[171],
             "   :CREATED: <2012-04-09 Mon>--<2012-04-09 Mon>")
        self.assertEqual(
            data[172],
             "   :ID:      a5d720ec1a1f5ec3bbf7c465027111769a94772a")
        self.assertEqual(
            data[173],
             "   :END:")
        self.assertEqual(
            data[174],
             "** Easter")
        self.assertEqual(
            data[175],
             "   :PROPERTIES:")
        self.assertEqual(
            data[176],
             "   :SUMMARY: Easter")
        self.assertEqual(
            data[177],
             "   :CREATED: <2012-04-08 Sun>--<2012-04-08 Sun>")
        self.assertEqual(
            data[178],
             "   :ID:      00ac559d0904b9f140a6b22de7e4ba72e3d47976")
        self.assertEqual(
            data[179],
             "   :END:")
        self.assertEqual(
            data[180],
             "** Corpus Christi")
        self.assertEqual(
            data[181],
             "   :PROPERTIES:")
        self.assertEqual(
            data[182],
             "   :SUMMARY: Corpus Christi")
        self.assertEqual(
            data[183],
             "   :CREATED: <2012-06-07 Thu>--<2012-06-07 Thu>")
        self.assertEqual(
            data[184],
             "   :ID:      bbacc85310a00ed64457218a4acbfd87ea82ec30")
        self.assertEqual(
            data[185],
             "   :END:")
        self.assertEqual(
            data[186],
             "** Christmas Eve")
        self.assertEqual(
            data[187],
             "   :PROPERTIES:")
        self.assertEqual(
            data[188],
             "   :SUMMARY: Christmas Eve")
        self.assertEqual(
            data[189],
             "   :CREATED: <2011-12-24 Sat>--<2011-12-24 Sat>")
        self.assertEqual(
            data[190],
             "   :ID:      3cf4978116e2fc672a1d687d10f25fd23738b2f6")
        self.assertEqual(
            data[191],
             "   :END:")
        self.assertEqual(
            data[192],
             "** Christmas Eve")
        self.assertEqual(
            data[193],
             "   :PROPERTIES:")
        self.assertEqual(
            data[194],
             "   :SUMMARY: Christmas Eve")
        self.assertEqual(
            data[195],
             "   :CREATED: <2010-12-24 Fri>--<2010-12-24 Fri>")
        self.assertEqual(
            data[196],
             "   :ID:      9b8b270b84a0b5e204b5bb4700f41aa78f932765")
        self.assertEqual(
            data[197],
             "   :END:")
        self.assertEqual(
            data[198],
             "** Christmas Eve")
        self.assertEqual(
            data[199],
             "   :PROPERTIES:")
        self.assertEqual(
            data[200],
             "   :SUMMARY: Christmas Eve")
        self.assertEqual(
            data[201],
             "   :CREATED: <2012-12-24 Mon>--<2012-12-24 Mon>")
        self.assertEqual(
            data[202],
             "   :ID:      8b7ec333f63a31f4a2b327180159465e0560038f")
        self.assertEqual(
            data[203],
             "   :END:")
        self.assertEqual(
            data[204],
             "** Christmas")
        self.assertEqual(
            data[205],
             "   :PROPERTIES:")
        self.assertEqual(
            data[206],
             "   :SUMMARY: Christmas")
        self.assertEqual(
            data[207],
             "   :CREATED: <2010-12-25 Sat>--<2010-12-25 Sat>")
        self.assertEqual(
            data[208],
             "   :ID:      b258cdeab83a30031bc2a7720912df12f983b8b2")
        self.assertEqual(
            data[209],
             "   :END:")
        self.assertEqual(
            data[210],
             "** Christmas")
        self.assertEqual(
            data[211],
             "   :PROPERTIES:")
        self.assertEqual(
            data[212],
             "   :SUMMARY: Christmas")
        self.assertEqual(
            data[213],
             "   :CREATED: <2011-12-25 Sun>--<2011-12-25 Sun>")
        self.assertEqual(
            data[214],
             "   :ID:      3e70e67dd40d21721e011dc786dc41cdb045e701")
        self.assertEqual(
            data[215],
             "   :END:")
        self.assertEqual(
            data[216],
             "** Christmas")
        self.assertEqual(
            data[217],
             "   :PROPERTIES:")
        self.assertEqual(
            data[218],
             "   :SUMMARY: Christmas")
        self.assertEqual(
            data[219],
             "   :CREATED: <2012-12-25 Tue>--<2012-12-25 Tue>")
        self.assertEqual(
            data[220],
             "   :ID:      b48c8b4c64c8ac3207a86fd95195de8334b0bbe9")
        self.assertEqual(
            data[221],
             "   :END:")
        self.assertEqual(
            data[222],
             "** Assumption")
        self.assertEqual(
            data[223],
             "   :PROPERTIES:")
        self.assertEqual(
            data[224],
             "   :SUMMARY: Assumption")
        self.assertEqual(
            data[225],
             "   :CREATED: <2010-08-15 Sun>--<2010-08-15 Sun>")
        self.assertEqual(
            data[226],
             "   :ID:      8051ac5ec0edd576b8f0978951001808e1531145")
        self.assertEqual(
            data[227],
             "   :END:")
        self.assertEqual(
            data[228],
             "** Assumption")
        self.assertEqual(
            data[229],
             "   :PROPERTIES:")
        self.assertEqual(
            data[230],
             "   :SUMMARY: Assumption")
        self.assertEqual(
            data[231],
             "   :CREATED: <2012-08-15 Wed>--<2012-08-15 Wed>")
        self.assertEqual(
            data[232],
             "   :ID:      6bf03edfea5d318a7395d4d72b9e3b8fe9b55a4a")
        self.assertEqual(
            data[233],
             "   :END:")
        self.assertEqual(
            data[234],
             "** Assumption")
        self.assertEqual(
            data[235],
             "   :PROPERTIES:")
        self.assertEqual(
            data[236],
             "   :SUMMARY: Assumption")
        self.assertEqual(
            data[237],
             "   :CREATED: <2011-08-15 Mon>--<2011-08-15 Mon>")
        self.assertEqual(
            data[238],
             "   :ID:      551d7a91571e961343f5e4125254c2e56e382229")
        self.assertEqual(
            data[239],
             "   :END:")
        self.assertEqual(
            data[240],
             "** Ascension Day")
        self.assertEqual(
            data[241],
             "   :PROPERTIES:")
        self.assertEqual(
            data[242],
             "   :SUMMARY: Ascension Day")
        self.assertEqual(
            data[243],
             "   :CREATED: <2012-05-17 Thu>--<2012-05-17 Thu>")
        self.assertEqual(
            data[244],
             "   :ID:      da3fa1158af56ce0ad54a9d2c7c6d63b7af2ed0a")
        self.assertEqual(
            data[245],
             "   :END:")
        self.assertEqual(
            data[246],
             "** All Souls' Day")
        self.assertEqual(
            data[247],
             "   :PROPERTIES:")
        self.assertEqual(
            data[248],
             "   :SUMMARY: All Souls' Day")
        self.assertEqual(
            data[249],
             "   :CREATED: <2011-11-02 Wed>--<2011-11-02 Wed>")
        self.assertEqual(
            data[250],
             "   :ID:      a6d8a9d2dc6101af0b4adf5ac1bbb4e1c8928854")
        self.assertEqual(
            data[251],
             "   :END:")
        self.assertEqual(
            data[252],
             "** All Souls' Day")
        self.assertEqual(
            data[253],
             "   :PROPERTIES:")
        self.assertEqual(
            data[254],
             "   :SUMMARY: All Souls' Day")
        self.assertEqual(
            data[255],
             "   :CREATED: <2010-11-02 Tue>--<2010-11-02 Tue>")
        self.assertEqual(
            data[256],
             "   :ID:      3c53c96cb9b37c98bcf6ca2e74a7fa5f5785e6b5")
        self.assertEqual(
            data[257],
             "   :END:")
        self.assertEqual(
            data[258],
             "** All Souls' Day")
        self.assertEqual(
            data[259],
             "   :PROPERTIES:")
        self.assertEqual(
            data[260],
             "   :SUMMARY: All Souls' Day")
        self.assertEqual(
            data[261],
             "   :CREATED: <2012-11-02 Fri>--<2012-11-02 Fri>")
        self.assertEqual(
            data[262],
             "   :ID:      fd5481e7f3809123dd5b06c8aadf068dbb4cf273")
        self.assertEqual(
            data[263],
             "   :END:")
        self.assertEqual(
            data[264],
             "** All Saints' Day")
        self.assertEqual(
            data[265],
             "   :PROPERTIES:")
        self.assertEqual(
            data[266],
             "   :SUMMARY: All Saints' Day")
        self.assertEqual(
            data[267],
             "   :CREATED: <2010-11-01 Mon>--<2010-11-01 Mon>")
        self.assertEqual(
            data[268],
             "   :ID:      80a8e64f9a50e62e7d2856d66c3c53fb333ba376")
        self.assertEqual(
            data[269],
             "   :END:")
        self.assertEqual(
            data[270],
             "** All Saints' Day")
        self.assertEqual(
            data[271],
             "   :PROPERTIES:")
        self.assertEqual(
            data[272],
             "   :SUMMARY: All Saints' Day")
        self.assertEqual(
            data[273],
             "   :CREATED: <2012-11-01 Thu>--<2012-11-01 Thu>")
        self.assertEqual(
            data[274],
             "   :ID:      7da43cca5b25e84d42c5bb3dee50b55fa9b5ef13")
        self.assertEqual(
            data[275],
             "   :END:")
        self.assertEqual(
            data[276],
             "** All Saints' Day")
        self.assertEqual(
            data[277],
             "   :PROPERTIES:")
        self.assertEqual(
            data[278],
             "   :SUMMARY: All Saints' Day")
        self.assertEqual(
            data[279],
             "   :CREATED: <2011-11-01 Tue>--<2011-11-01 Tue>")
        self.assertEqual(
            data[280],
             "   :ID:      926326081187309c0ac6444ed406a980686271da")
        self.assertEqual(
            data[281],
             "   :END:")