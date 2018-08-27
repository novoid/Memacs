# -*- coding: utf-8 -*-
# Time-stamp: <2016-01-23 18:07:46 vk>

import unittest
import os
from memacs.ical import CalendarMemacs


class TestCalendar(unittest.TestCase):

    def test_all(self):
        test_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data', 'austrian_holidays_from_google.ics'
        )
        argv = "-s -cf " + test_file
        memacs = CalendarMemacs(argv=argv.split())
        data = memacs.test_get_entries()

        self.assertEqual(
            data[0],
             "** <2012-05-28 Mon>--<2012-05-28 Mon> Whit Monday")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :ID:         b6972cddd864a2fba79ed8ff95e0f2f8948f2410")
        self.assertEqual(
            data[3],
             "   :END:")
        self.assertEqual(
            data[4],
             "** <2011-02-14 Mon>--<2011-02-14 Mon> Valentine's day")
        self.assertEqual(
            data[5],
             "   :PROPERTIES:")
        self.assertEqual(
            data[6],
             "   :ID:         66186caf3409e2086a9c199a03cb6ff440ab738b")
        self.assertEqual(
            data[7],
             "   :END:")
        self.assertEqual(
            data[8],
             "** <2010-02-14 Sun>--<2010-02-14 Sun> Valentine's day")
        self.assertEqual(
            data[9],
             "   :PROPERTIES:")
        self.assertEqual(
            data[10],
             "   :ID:         bee25809ac0695d567664decb61592ada965f858")
        self.assertEqual(
            data[11],
             "   :END:")
        self.assertEqual(
            data[12],
             "** <2012-02-14 Tue>--<2012-02-14 Tue> Valentine's day")
        self.assertEqual(
            data[13],
             "   :PROPERTIES:")
        self.assertEqual(
            data[14],
             "   :ID:         d74b79979f616f13715439a1ef7e0b2f0c69f220")
        self.assertEqual(
            data[15],
             "   :END:")
        self.assertEqual(
            data[16],
             "** <2012-12-26 Wed>--<2012-12-26 Wed> St. Stephan's Day")
        self.assertEqual(
            data[17],
             "   :PROPERTIES:")
        self.assertEqual(
            data[18],
             "   :ID:         c2559692c5465c6dad0f014f936eef320b516b9f")
        self.assertEqual(
            data[19],
             "   :END:")
        self.assertEqual(
            data[20],
             "** <2010-12-26 Sun>--<2010-12-26 Sun> St. Stephan's Day")
        self.assertEqual(
            data[21],
             "   :PROPERTIES:")
        self.assertEqual(
            data[22],
             "   :ID:         c145ba3f76fab2f9eca5a9b09695c47b1f65554a")
        self.assertEqual(
            data[23],
             "   :END:")
        self.assertEqual(
            data[24],
             "** <2011-12-26 Mon>--<2011-12-26 Mon> St. Stephan's Day")
        self.assertEqual(
            data[25],
             "   :PROPERTIES:")
        self.assertEqual(
            data[26],
             "   :ID:         0c663e887265d372cf40d3c7f1d7fd595a0114a0")
        self.assertEqual(
            data[27],
             "   :END:")
        self.assertEqual(
            data[28],
             "** <2011-12-06 Tue>--<2011-12-06 Tue> St. Nicholas")
        self.assertEqual(
            data[29],
             "   :PROPERTIES:")
        self.assertEqual(
            data[30],
             "   :ID:         821d4ce5231db9f037cf64f8b3cfeeeb65c84bee")
        self.assertEqual(
            data[31],
             "   :END:")
        self.assertEqual(
            data[32],
             "** <2010-12-06 Mon>--<2010-12-06 Mon> St. Nicholas")
        self.assertEqual(
            data[33],
             "   :PROPERTIES:")
        self.assertEqual(
            data[34],
             "   :ID:         4b1f7183ef085af82ec9b7be7845d35d9504b0b6")
        self.assertEqual(
            data[35],
             "   :END:")
        self.assertEqual(
            data[36],
             "** <2012-12-06 Thu>--<2012-12-06 Thu> St. Nicholas")
        self.assertEqual(
            data[37],
             "   :PROPERTIES:")
        self.assertEqual(
            data[38],
             "   :ID:         34c1c44697bedbe3228842204e84f45ec45b0923")
        self.assertEqual(
            data[39],
             "   :END:")
        self.assertEqual(
            data[40],
             "** <2011-12-31 Sat>--<2011-12-31 Sat> New Year's Eve")
        self.assertEqual(
            data[41],
             "   :PROPERTIES:")
        self.assertEqual(
            data[42],
             "   :ID:         ea722a9d474e8bbda41f48460ad3681e10097044")
        self.assertEqual(
            data[43],
             "   :END:")
        self.assertEqual(
            data[44],
             "** <2010-12-31 Fri>--<2010-12-31 Fri> New Year's Eve")
        self.assertEqual(
            data[45],
             "   :PROPERTIES:")
        self.assertEqual(
            data[46],
             "   :ID:         afcbb4912aaede6e31b0c4bdb9221b90f10c1b62")
        self.assertEqual(
            data[47],
             "   :END:")
        self.assertEqual(
            data[48],
             "** <2012-01-01 Sun>--<2012-01-01 Sun> New Year")
        self.assertEqual(
            data[49],
             "   :PROPERTIES:")
        self.assertEqual(
            data[50],
             "   :ID:         9a533328738c914dcc4abd5bb571e63cccae0fa2")
        self.assertEqual(
            data[51],
             "   :END:")
        self.assertEqual(
            data[52],
             "** <2010-01-01 Fri>--<2010-01-01 Fri> New Year")
        self.assertEqual(
            data[53],
             "   :PROPERTIES:")
        self.assertEqual(
            data[54],
             "   :ID:         1239f768e303f38b312d4fa84ad295f44a12ea99")
        self.assertEqual(
            data[55],
             "   :END:")
        self.assertEqual(
            data[56],
             "** <2011-01-01 Sat>--<2011-01-01 Sat> New Year")
        self.assertEqual(
            data[57],
             "   :PROPERTIES:")
        self.assertEqual(
            data[58],
             "   :ID:         c578509791f5865707d0018ad79c2eaf37210481")
        self.assertEqual(
            data[59],
             "   :END:")
        self.assertEqual(
            data[60],
             "** <2010-10-26 Tue>--<2010-10-26 Tue> National Holiday")
        self.assertEqual(
            data[61],
             "   :PROPERTIES:")
        self.assertEqual(
            data[62],
             "   :ID:         dffe086b45549c333b308892bf7b4b83485ea216")
        self.assertEqual(
            data[63],
             "   :END:")
        self.assertEqual(
            data[64],
             "** <2012-10-26 Fri>--<2012-10-26 Fri> National Holiday")
        self.assertEqual(
            data[65],
             "   :PROPERTIES:")
        self.assertEqual(
            data[66],
             "   :ID:         5d74bcc91609435775c774cf4b2c373e3b6b9a9e")
        self.assertEqual(
            data[67],
             "   :END:")
        self.assertEqual(
            data[68],
             "** <2011-10-26 Wed>--<2011-10-26 Wed> National Holiday")
        self.assertEqual(
            data[69],
             "   :PROPERTIES:")
        self.assertEqual(
            data[70],
             "   :ID:         5c99d7709dfe1e81b18e3c3343e06edd0854015f")
        self.assertEqual(
            data[71],
             "   :END:")
        self.assertEqual(
            data[72],
             "** <2011-05-01 Sun>--<2011-05-01 Sun> Labour Day")
        self.assertEqual(
            data[73],
             "   :PROPERTIES:")
        self.assertEqual(
            data[74],
             "   :ID:         5f18bf2bffdedf1fd50bca2b5ccfb8bd7554b52f")
        self.assertEqual(
            data[75],
             "   :END:")
        self.assertEqual(
            data[76],
             "** <2010-05-01 Sat>--<2010-05-01 Sat> Labour Day")
        self.assertEqual(
            data[77],
             "   :PROPERTIES:")
        self.assertEqual(
            data[78],
             "   :ID:         248bbd02f36ba32fbe36c5fdf65ab66a400307c5")
        self.assertEqual(
            data[79],
             "   :END:")
        self.assertEqual(
            data[80],
             "** <2012-05-01 Tue>--<2012-05-01 Tue> Labour Day")
        self.assertEqual(
            data[81],
             "   :PROPERTIES:")
        self.assertEqual(
            data[82],
             "   :ID:         709d57b34901a8dab5277cdec884acb989579451")
        self.assertEqual(
            data[83],
             "   :END:")
        self.assertEqual(
            data[84],
             "** <2012-12-08 Sat>--<2012-12-08 Sat> Immaculate Conception")
        self.assertEqual(
            data[85],
             "   :PROPERTIES:")
        self.assertEqual(
            data[86],
             "   :ID:         9718f2c669addc152c80d478beaeb81ab7dc2757")
        self.assertEqual(
            data[87],
             "   :END:")
        self.assertEqual(
            data[88],
             "** <2010-12-08 Wed>--<2010-12-08 Wed> Immaculate Conception")
        self.assertEqual(
            data[89],
             "   :PROPERTIES:")
        self.assertEqual(
            data[90],
             "   :ID:         7d02e0af4e44664e5a474376dd97ba838bcdb725")
        self.assertEqual(
            data[91],
             "   :END:")
        self.assertEqual(
            data[92],
             "** <2011-12-08 Thu>--<2011-12-08 Thu> Immaculate Conception")
        self.assertEqual(
            data[93],
             "   :PROPERTIES:")
        self.assertEqual(
            data[94],
             "   :ID:         20e022ce71904efac1f90d45b24b4164623a919b")
        self.assertEqual(
            data[95],
             "   :END:")
        self.assertEqual(
            data[96],
             "** <2012-04-06 Fri>--<2012-04-06 Fri> Good Friday")
        self.assertEqual(
            data[97],
             "   :PROPERTIES:")
        self.assertEqual(
            data[98],
             "   :ID:         6a9a405cdba496987ca9ab66aef623fe0ed70e26")
        self.assertEqual(
            data[99],
             "   :END:")
        self.assertEqual(
            data[100],
             "** <2010-01-06 Wed>--<2010-01-06 Wed> Epiphany")
        self.assertEqual(
            data[101],
             "   :PROPERTIES:")
        self.assertEqual(
            data[102],
             "   :ID:         6640ef7807da042944392601c4e9b046174bce8e")
        self.assertEqual(
            data[103],
             "   :END:")
        self.assertEqual(
            data[104],
             "** <2012-01-06 Fri>--<2012-01-06 Fri> Epiphany")
        self.assertEqual(
            data[105],
             "   :PROPERTIES:")
        self.assertEqual(
            data[106],
             "   :ID:         0aa9ab88fb1bfcb9b0fb430e673ec23eb42a4f38")
        self.assertEqual(
            data[107],
             "   :END:")
        self.assertEqual(
            data[108],
             "** <2011-01-06 Thu>--<2011-01-06 Thu> Epiphany")
        self.assertEqual(
            data[109],
             "   :PROPERTIES:")
        self.assertEqual(
            data[110],
             "   :ID:         36897fcbb92a331ebebb86f4cef7b0e988c020c6")
        self.assertEqual(
            data[111],
             "   :END:")
        self.assertEqual(
            data[112],
             "** <2012-04-09 Mon>--<2012-04-09 Mon> Easter Monday")
        self.assertEqual(
            data[113],
             "   :PROPERTIES:")
        self.assertEqual(
            data[114],
             "   :ID:         a71164883dcb44825f7de50f68b7ea881b1a5d23")
        self.assertEqual(
            data[115],
             "   :END:")
        self.assertEqual(
            data[116],
             "** <2012-04-08 Sun>--<2012-04-08 Sun> Easter")
        self.assertEqual(
            data[117],
             "   :PROPERTIES:")
        self.assertEqual(
            data[118],
             "   :ID:         7dcfbb563cd9300bf18f3c05965a1b0c7c6442b8")
        self.assertEqual(
            data[119],
             "   :END:")
        self.assertEqual(
            data[120],
             "** <2012-06-07 Thu>--<2012-06-07 Thu> Corpus Christi")
        self.assertEqual(
            data[121],
             "   :PROPERTIES:")
        self.assertEqual(
            data[122],
             "   :ID:         01cd602579e0774b020c3d13a760e8fa828c6aec")
        self.assertEqual(
            data[123],
             "   :END:")
        self.assertEqual(
            data[124],
             "** <2011-12-24 Sat>--<2011-12-24 Sat> Christmas Eve")
        self.assertEqual(
            data[125],
             "   :PROPERTIES:")
        self.assertEqual(
            data[126],
             "   :ID:         4b91f8eefc9723bb3022b2bedb4c4d098f7f9d39")
        self.assertEqual(
            data[127],
             "   :END:")
        self.assertEqual(
            data[128],
             "** <2010-12-24 Fri>--<2010-12-24 Fri> Christmas Eve")
        self.assertEqual(
            data[129],
             "   :PROPERTIES:")
        self.assertEqual(
            data[130],
             "   :ID:         b3b00147203e50aa69fdae2f6745b78d13a39231")
        self.assertEqual(
            data[131],
             "   :END:")
        self.assertEqual(
            data[132],
             "** <2012-12-24 Mon>--<2012-12-24 Mon> Christmas Eve")
        self.assertEqual(
            data[133],
             "   :PROPERTIES:")
        self.assertEqual(
            data[134],
             "   :ID:         23506451af37175457bfff7b113aff5ff75881e7")
        self.assertEqual(
            data[135],
             "   :END:")
        self.assertEqual(
            data[136],
             "** <2010-12-25 Sat>--<2010-12-25 Sat> Christmas")
        self.assertEqual(
            data[137],
             "   :PROPERTIES:")
        self.assertEqual(
            data[138],
             "   :ID:         ae52748d82d25b1ada9ef73e6c608519c0cecca5")
        self.assertEqual(
            data[139],
             "   :END:")
        self.assertEqual(
            data[140],
             "** <2011-12-25 Sun>--<2011-12-25 Sun> Christmas")
        self.assertEqual(
            data[141],
             "   :PROPERTIES:")
        self.assertEqual(
            data[142],
             "   :ID:         802fb8acb3618909a6d7aaf605bf732a97a84d39")
        self.assertEqual(
            data[143],
             "   :END:")
        self.assertEqual(
            data[144],
             "** <2012-12-25 Tue>--<2012-12-25 Tue> Christmas")
        self.assertEqual(
            data[145],
             "   :PROPERTIES:")
        self.assertEqual(
            data[146],
             "   :ID:         1dc9ebe2f8ff2c91ca155c30ae65a67db11cf8aa")
        self.assertEqual(
            data[147],
             "   :END:")
        self.assertEqual(
            data[148],
             "** <2010-08-15 Sun>--<2010-08-15 Sun> Assumption")
        self.assertEqual(
            data[149],
             "   :PROPERTIES:")
        self.assertEqual(
            data[150],
             "   :ID:         c3e85e7c44c5cca95efa0751c7c52375640b43c2")
        self.assertEqual(
            data[151],
             "   :END:")
        self.assertEqual(
            data[152],
             "** <2012-08-15 Wed>--<2012-08-15 Wed> Assumption")
        self.assertEqual(
            data[153],
             "   :PROPERTIES:")
        self.assertEqual(
            data[154],
             "   :ID:         52c49d4ca2a196e6409ac362183cedcd656975ef")
        self.assertEqual(
            data[155],
             "   :END:")
        self.assertEqual(
            data[156],
             "** <2011-08-15 Mon>--<2011-08-15 Mon> Assumption")
        self.assertEqual(
            data[157],
             "   :PROPERTIES:")
        self.assertEqual(
            data[158],
             "   :ID:         be957e5083131794b874b06597cd1cc935d35408")
        self.assertEqual(
            data[159],
             "   :END:")
        self.assertEqual(
            data[160],
             "** <2012-05-17 Thu>--<2012-05-17 Thu> Ascension Day")
        self.assertEqual(
            data[161],
             "   :PROPERTIES:")
        self.assertEqual(
            data[162],
             "   :ID:         f718e41128812a9864df1a1aa649c23c82f453f9")
        self.assertEqual(
            data[163],
             "   :END:")
        self.assertEqual(
            data[164],
             "** <2011-11-02 Wed>--<2011-11-02 Wed> All Souls' Day")
        self.assertEqual(
            data[165],
             "   :PROPERTIES:")
        self.assertEqual(
            data[166],
             "   :ID:         f55d246b411fd4fe3d47205041538d04f56cac53")
        self.assertEqual(
            data[167],
             "   :END:")
        self.assertEqual(
            data[168],
             "** <2010-11-02 Tue>--<2010-11-02 Tue> All Souls' Day")
        self.assertEqual(
            data[169],
             "   :PROPERTIES:")
        self.assertEqual(
            data[170],
             "   :ID:         62e1a6c16ce2c40e33d67961b6cec5c0a099b14d")
        self.assertEqual(
            data[171],
             "   :END:")
        self.assertEqual(
            data[172],
             "** <2012-11-02 Fri>--<2012-11-02 Fri> All Souls' Day")
        self.assertEqual(
            data[173],
             "   :PROPERTIES:")
        self.assertEqual(
            data[174],
             "   :ID:         c9eae72e34489720698a1054cd03bb4cc8859e71")
        self.assertEqual(
            data[175],
             "   :END:")
        self.assertEqual(
            data[176],
             "** <2010-11-01 Mon>--<2010-11-01 Mon> All Saints' Day")
        self.assertEqual(
            data[177],
             "   :PROPERTIES:")
        self.assertEqual(
            data[178],
             "   :ID:         b87bcffe87fda005047d738c07a31cd8c25f609c")
        self.assertEqual(
            data[179],
             "   :END:")
        self.assertEqual(
            data[180],
             "** <2012-11-01 Thu>--<2012-11-01 Thu> All Saints' Day")
        self.assertEqual(
            data[181],
             "   :PROPERTIES:")
        self.assertEqual(
            data[182],
             "   :ID:         37b17e9da936c61a627101afd0cc87d28aafbe70")
        self.assertEqual(
            data[183],
             "   :END:")
        self.assertEqual(
            data[184],
             "** <2011-11-01 Tue>--<2011-11-01 Tue> All Saints' Day")
        self.assertEqual(
            data[185],
             "   :PROPERTIES:")
        self.assertEqual(
            data[186],
             "   :ID:         fe605142ace6ab6268fc672fccece05219c17148")
        self.assertEqual(
            data[187],
             "   :END:")
        self.assertEqual(
            data[188:194], ['** <2011-08-22 Mon>-<9999-12-31 Fri> No end time/date',
                            '   :PROPERTIES:',
                            '   :DESCRIPTION: No end time/date',
                            '   :ID:          62bf353bf19c0379faf4910741635dfd6a804b11',
                            '   :END:'])
