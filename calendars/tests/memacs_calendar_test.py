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
             "   :CREATED: <2012-05-28 Mon>--<2012-05-28 Mon>")
        self.assertEqual(
            data[3],
             "   :ID:      872442b280e6d62d507c69e791b9313b4327c56c")
        self.assertEqual(
            data[4],
             "   :END:")
        self.assertEqual(
            data[5],
             "** Valentine's day")
        self.assertEqual(
            data[6],
             "   :PROPERTIES:")
        self.assertEqual(
            data[7],
             "   :CREATED: <2011-02-14 Mon>--<2011-02-14 Mon>")
        self.assertEqual(
            data[8],
             "   :ID:      2f022437f3ad7f0db77482fcda3d180852ab0f0e")
        self.assertEqual(
            data[9],
             "   :END:")
        self.assertEqual(
            data[10],
             "** Valentine's day")
        self.assertEqual(
            data[11],
             "   :PROPERTIES:")
        self.assertEqual(
            data[12],
             "   :CREATED: <2010-02-14 Sun>--<2010-02-14 Sun>")
        self.assertEqual(
            data[13],
             "   :ID:      8ea1c95bd556508acfb143dee49432418fe8a9d3")
        self.assertEqual(
            data[14],
             "   :END:")
        self.assertEqual(
            data[15],
             "** Valentine's day")
        self.assertEqual(
            data[16],
             "   :PROPERTIES:")
        self.assertEqual(
            data[17],
             "   :CREATED: <2012-02-14 Tue>--<2012-02-14 Tue>")
        self.assertEqual(
            data[18],
             "   :ID:      615bc80bd9f34a80b0bdc19b0d5eb79450e6dd18")
        self.assertEqual(
            data[19],
             "   :END:")
        self.assertEqual(
            data[20],
             "** St. Stephan's Day")
        self.assertEqual(
            data[21],
             "   :PROPERTIES:")
        self.assertEqual(
            data[22],
             "   :CREATED: <2012-12-26 Wed>--<2012-12-26 Wed>")
        self.assertEqual(
            data[23],
             "   :ID:      187c8a8294076477890005f735f75bd828bb0072")
        self.assertEqual(
            data[24],
             "   :END:")
        self.assertEqual(
            data[25],
             "** St. Stephan's Day")
        self.assertEqual(
            data[26],
             "   :PROPERTIES:")
        self.assertEqual(
            data[27],
             "   :CREATED: <2010-12-26 Sun>--<2010-12-26 Sun>")
        self.assertEqual(
            data[28],
             "   :ID:      6c17dfb70e84e690749f4918d060f764819744a6")
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
             "   :CREATED: <2011-12-26 Mon>--<2011-12-26 Mon>")
        self.assertEqual(
            data[33],
             "   :ID:      00745e09a0ddaa1c3766cbcf28901c2e30ed9981")
        self.assertEqual(
            data[34],
             "   :END:")
        self.assertEqual(
            data[35],
             "** St. Nicholas")
        self.assertEqual(
            data[36],
             "   :PROPERTIES:")
        self.assertEqual(
            data[37],
             "   :CREATED: <2011-12-06 Tue>--<2011-12-06 Tue>")
        self.assertEqual(
            data[38],
             "   :ID:      49816302825b07ece0bda6f51e02bcfcc7ccacdd")
        self.assertEqual(
            data[39],
             "   :END:")
        self.assertEqual(
            data[40],
             "** St. Nicholas")
        self.assertEqual(
            data[41],
             "   :PROPERTIES:")
        self.assertEqual(
            data[42],
             "   :CREATED: <2010-12-06 Mon>--<2010-12-06 Mon>")
        self.assertEqual(
            data[43],
             "   :ID:      f2c11cb8dc8d295fb2a6cc6ef07b2bd4eea1c39f")
        self.assertEqual(
            data[44],
             "   :END:")
        self.assertEqual(
            data[45],
             "** St. Nicholas")
        self.assertEqual(
            data[46],
             "   :PROPERTIES:")
        self.assertEqual(
            data[47],
             "   :CREATED: <2012-12-06 Thu>--<2012-12-06 Thu>")
        self.assertEqual(
            data[48],
             "   :ID:      7b70de09bd52eb81740422a9ad14e7e6bf19a9de")
        self.assertEqual(
            data[49],
             "   :END:")
        self.assertEqual(
            data[50],
             "** New Year's Eve")
        self.assertEqual(
            data[51],
             "   :PROPERTIES:")
        self.assertEqual(
            data[52],
             "   :CREATED: <2011-12-31 Sat>--<2011-12-31 Sat>")
        self.assertEqual(
            data[53],
             "   :ID:      fa0ded653c08dc837773471241d8278480830158")
        self.assertEqual(
            data[54],
             "   :END:")
        self.assertEqual(
            data[55],
             "** New Year's Eve")
        self.assertEqual(
            data[56],
             "   :PROPERTIES:")
        self.assertEqual(
            data[57],
             "   :CREATED: <2010-12-31 Fri>--<2010-12-31 Fri>")
        self.assertEqual(
            data[58],
             "   :ID:      653483b0b15935affbe8a07dacb34429ed003fd6")
        self.assertEqual(
            data[59],
             "   :END:")
        self.assertEqual(
            data[60],
             "** New Year")
        self.assertEqual(
            data[61],
             "   :PROPERTIES:")
        self.assertEqual(
            data[62],
             "   :CREATED: <2012-01-01 Sun>--<2012-01-01 Sun>")
        self.assertEqual(
            data[63],
             "   :ID:      28c6eff4b61dfe6cdb6d3eb8b5817928c380502b")
        self.assertEqual(
            data[64],
             "   :END:")
        self.assertEqual(
            data[65],
             "** New Year")
        self.assertEqual(
            data[66],
             "   :PROPERTIES:")
        self.assertEqual(
            data[67],
             "   :CREATED: <2010-01-01 Fri>--<2010-01-01 Fri>")
        self.assertEqual(
            data[68],
             "   :ID:      5fcdfaf0ded5b10c6673ef42fa56e69e39ffc6d7")
        self.assertEqual(
            data[69],
             "   :END:")
        self.assertEqual(
            data[70],
             "** New Year")
        self.assertEqual(
            data[71],
             "   :PROPERTIES:")
        self.assertEqual(
            data[72],
             "   :CREATED: <2011-01-01 Sat>--<2011-01-01 Sat>")
        self.assertEqual(
            data[73],
             "   :ID:      40949f3ed7af7e953325ea04331a5fd7a34d1297")
        self.assertEqual(
            data[74],
             "   :END:")
        self.assertEqual(
            data[75],
             "** National Holiday")
        self.assertEqual(
            data[76],
             "   :PROPERTIES:")
        self.assertEqual(
            data[77],
             "   :CREATED: <2010-10-26 Tue>--<2010-10-26 Tue>")
        self.assertEqual(
            data[78],
             "   :ID:      3f20cc2822c74a4a26f43e8bdb40e20f07d7f9c4")
        self.assertEqual(
            data[79],
             "   :END:")
        self.assertEqual(
            data[80],
             "** National Holiday")
        self.assertEqual(
            data[81],
             "   :PROPERTIES:")
        self.assertEqual(
            data[82],
             "   :CREATED: <2012-10-26 Fri>--<2012-10-26 Fri>")
        self.assertEqual(
            data[83],
             "   :ID:      71ae09d742e630007e8dc84c63c29c2956aeede6")
        self.assertEqual(
            data[84],
             "   :END:")
        self.assertEqual(
            data[85],
             "** National Holiday")
        self.assertEqual(
            data[86],
             "   :PROPERTIES:")
        self.assertEqual(
            data[87],
             "   :CREATED: <2011-10-26 Wed>--<2011-10-26 Wed>")
        self.assertEqual(
            data[88],
             "   :ID:      d95adbf6d79cb37f66f29d65eb350e97b69c4b48")
        self.assertEqual(
            data[89],
             "   :END:")
        self.assertEqual(
            data[90],
             "** Labour Day")
        self.assertEqual(
            data[91],
             "   :PROPERTIES:")
        self.assertEqual(
            data[92],
             "   :CREATED: <2011-05-01 Sun>--<2011-05-01 Sun>")
        self.assertEqual(
            data[93],
             "   :ID:      ac35f3e6758aa14f0858d2a4016c0476cdfbb606")
        self.assertEqual(
            data[94],
             "   :END:")
        self.assertEqual(
            data[95],
             "** Labour Day")
        self.assertEqual(
            data[96],
             "   :PROPERTIES:")
        self.assertEqual(
            data[97],
             "   :CREATED: <2010-05-01 Sat>--<2010-05-01 Sat>")
        self.assertEqual(
            data[98],
             "   :ID:      c5da43da196542b510333289dfea6f0f04216b01")
        self.assertEqual(
            data[99],
             "   :END:")
        self.assertEqual(
            data[100],
             "** Labour Day")
        self.assertEqual(
            data[101],
             "   :PROPERTIES:")
        self.assertEqual(
            data[102],
             "   :CREATED: <2012-05-01 Tue>--<2012-05-01 Tue>")
        self.assertEqual(
            data[103],
             "   :ID:      44f950d8a2dfa852954794d790139dcfeaa0cba0")
        self.assertEqual(
            data[104],
             "   :END:")
        self.assertEqual(
            data[105],
             "** Immaculate Conception")
        self.assertEqual(
            data[106],
             "   :PROPERTIES:")
        self.assertEqual(
            data[107],
             "   :CREATED: <2012-12-08 Sat>--<2012-12-08 Sat>")
        self.assertEqual(
            data[108],
             "   :ID:      d46c7dd63895283ccade96be4263d8fca1c249a8")
        self.assertEqual(
            data[109],
             "   :END:")
        self.assertEqual(
            data[110],
             "** Immaculate Conception")
        self.assertEqual(
            data[111],
             "   :PROPERTIES:")
        self.assertEqual(
            data[112],
             "   :CREATED: <2010-12-08 Wed>--<2010-12-08 Wed>")
        self.assertEqual(
            data[113],
             "   :ID:      8c50510ec4cd89a32cbfc329952c20d6463b538a")
        self.assertEqual(
            data[114],
             "   :END:")
        self.assertEqual(
            data[115],
             "** Immaculate Conception")
        self.assertEqual(
            data[116],
             "   :PROPERTIES:")
        self.assertEqual(
            data[117],
             "   :CREATED: <2011-12-08 Thu>--<2011-12-08 Thu>")
        self.assertEqual(
            data[118],
             "   :ID:      254a9fc69183d8b178c14fb1a00dba17f694c7cf")
        self.assertEqual(
            data[119],
             "   :END:")
        self.assertEqual(
            data[120],
             "** Good Friday")
        self.assertEqual(
            data[121],
             "   :PROPERTIES:")
        self.assertEqual(
            data[122],
             "   :CREATED: <2012-04-06 Fri>--<2012-04-06 Fri>")
        self.assertEqual(
            data[123],
             "   :ID:      4886d9ecb353653c2e7fd5bf17ca1c1a31246945")
        self.assertEqual(
            data[124],
             "   :END:")
        self.assertEqual(
            data[125],
             "** Epiphany")
        self.assertEqual(
            data[126],
             "   :PROPERTIES:")
        self.assertEqual(
            data[127],
             "   :CREATED: <2010-01-06 Wed>--<2010-01-06 Wed>")
        self.assertEqual(
            data[128],
             "   :ID:      14d1bf3af1ebcf0c8b49cc25ebc65765839d1af2")
        self.assertEqual(
            data[129],
             "   :END:")
        self.assertEqual(
            data[130],
             "** Epiphany")
        self.assertEqual(
            data[131],
             "   :PROPERTIES:")
        self.assertEqual(
            data[132],
             "   :CREATED: <2012-01-06 Fri>--<2012-01-06 Fri>")
        self.assertEqual(
            data[133],
             "   :ID:      09427b134dcc0666b82891d9886e2de18a271909")
        self.assertEqual(
            data[134],
             "   :END:")
        self.assertEqual(
            data[135],
             "** Epiphany")
        self.assertEqual(
            data[136],
             "   :PROPERTIES:")
        self.assertEqual(
            data[137],
             "   :CREATED: <2011-01-06 Thu>--<2011-01-06 Thu>")
        self.assertEqual(
            data[138],
             "   :ID:      90235b6e88ba3518491ca5d94bd21c2ee3892f28")
        self.assertEqual(
            data[139],
             "   :END:")
        self.assertEqual(
            data[140],
             "** Easter Monday")
        self.assertEqual(
            data[141],
             "   :PROPERTIES:")
        self.assertEqual(
            data[142],
             "   :CREATED: <2012-04-09 Mon>--<2012-04-09 Mon>")
        self.assertEqual(
            data[143],
             "   :ID:      007fda5c8ff4c819f4e3a0b0923bab2db57d4617")
        self.assertEqual(
            data[144],
             "   :END:")
        self.assertEqual(
            data[145],
             "** Easter")
        self.assertEqual(
            data[146],
             "   :PROPERTIES:")
        self.assertEqual(
            data[147],
             "   :CREATED: <2012-04-08 Sun>--<2012-04-08 Sun>")
        self.assertEqual(
            data[148],
             "   :ID:      982f0e91aa1220844bbb9d9cf319a1ccf99e2db5")
        self.assertEqual(
            data[149],
             "   :END:")
        self.assertEqual(
            data[150],
             "** Corpus Christi")
        self.assertEqual(
            data[151],
             "   :PROPERTIES:")
        self.assertEqual(
            data[152],
             "   :CREATED: <2012-06-07 Thu>--<2012-06-07 Thu>")
        self.assertEqual(
            data[153],
             "   :ID:      b9bd048d63ced2df00ba4099925f109268675ec6")
        self.assertEqual(
            data[154],
             "   :END:")
        self.assertEqual(
            data[155],
             "** Christmas Eve")
        self.assertEqual(
            data[156],
             "   :PROPERTIES:")
        self.assertEqual(
            data[157],
             "   :CREATED: <2011-12-24 Sat>--<2011-12-24 Sat>")
        self.assertEqual(
            data[158],
             "   :ID:      0a019be0ae53e259e71668392192b739985cf8bb")
        self.assertEqual(
            data[159],
             "   :END:")
        self.assertEqual(
            data[160],
             "** Christmas Eve")
        self.assertEqual(
            data[161],
             "   :PROPERTIES:")
        self.assertEqual(
            data[162],
             "   :CREATED: <2010-12-24 Fri>--<2010-12-24 Fri>")
        self.assertEqual(
            data[163],
             "   :ID:      e574bb8ce796af957223e1053f13ea8234458bcc")
        self.assertEqual(
            data[164],
             "   :END:")
        self.assertEqual(
            data[165],
             "** Christmas Eve")
        self.assertEqual(
            data[166],
             "   :PROPERTIES:")
        self.assertEqual(
            data[167],
             "   :CREATED: <2012-12-24 Mon>--<2012-12-24 Mon>")
        self.assertEqual(
            data[168],
             "   :ID:      0f8ae11bd0730ba5cd506a316d2e9b6538f750b9")
        self.assertEqual(
            data[169],
             "   :END:")
        self.assertEqual(
            data[170],
             "** Christmas")
        self.assertEqual(
            data[171],
             "   :PROPERTIES:")
        self.assertEqual(
            data[172],
             "   :CREATED: <2010-12-25 Sat>--<2010-12-25 Sat>")
        self.assertEqual(
            data[173],
             "   :ID:      00c5b0f53007843ad38616b51a583d2317c26e6a")
        self.assertEqual(
            data[174],
             "   :END:")
        self.assertEqual(
            data[175],
             "** Christmas")
        self.assertEqual(
            data[176],
             "   :PROPERTIES:")
        self.assertEqual(
            data[177],
             "   :CREATED: <2011-12-25 Sun>--<2011-12-25 Sun>")
        self.assertEqual(
            data[178],
             "   :ID:      6c7dca1a1315b45a17f9b9e30cc47fe04394c400")
        self.assertEqual(
            data[179],
             "   :END:")
        self.assertEqual(
            data[180],
             "** Christmas")
        self.assertEqual(
            data[181],
             "   :PROPERTIES:")
        self.assertEqual(
            data[182],
             "   :CREATED: <2012-12-25 Tue>--<2012-12-25 Tue>")
        self.assertEqual(
            data[183],
             "   :ID:      f9d538a52add8000c5812b1053a0c6e037c8fa10")
        self.assertEqual(
            data[184],
             "   :END:")
        self.assertEqual(
            data[185],
             "** Assumption")
        self.assertEqual(
            data[186],
             "   :PROPERTIES:")
        self.assertEqual(
            data[187],
             "   :CREATED: <2010-08-15 Sun>--<2010-08-15 Sun>")
        self.assertEqual(
            data[188],
             "   :ID:      fa99c634fbbc371408f5be66899b7b37f9d717df")
        self.assertEqual(
            data[189],
             "   :END:")
        self.assertEqual(
            data[190],
             "** Assumption")
        self.assertEqual(
            data[191],
             "   :PROPERTIES:")
        self.assertEqual(
            data[192],
             "   :CREATED: <2012-08-15 Wed>--<2012-08-15 Wed>")
        self.assertEqual(
            data[193],
             "   :ID:      1d7ace1e96bbee6c0922bfde7f3d353e11df6a5d")
        self.assertEqual(
            data[194],
             "   :END:")
        self.assertEqual(
            data[195],
             "** Assumption")
        self.assertEqual(
            data[196],
             "   :PROPERTIES:")
        self.assertEqual(
            data[197],
             "   :CREATED: <2011-08-15 Mon>--<2011-08-15 Mon>")
        self.assertEqual(
            data[198],
             "   :ID:      1f3a2a6e858573e6b7ad8587e4487831514e1a03")
        self.assertEqual(
            data[199],
             "   :END:")
        self.assertEqual(
            data[200],
             "** Ascension Day")
        self.assertEqual(
            data[201],
             "   :PROPERTIES:")
        self.assertEqual(
            data[202],
             "   :CREATED: <2012-05-17 Thu>--<2012-05-17 Thu>")
        self.assertEqual(
            data[203],
             "   :ID:      c1e26de8ea10797ab719163cef85761f7f03dafc")
        self.assertEqual(
            data[204],
             "   :END:")
        self.assertEqual(
            data[205],
             "** All Souls' Day")
        self.assertEqual(
            data[206],
             "   :PROPERTIES:")
        self.assertEqual(
            data[207],
             "   :CREATED: <2011-11-02 Wed>--<2011-11-02 Wed>")
        self.assertEqual(
            data[208],
             "   :ID:      77baeab9fb6dec117affa2172b1024ea1b5dd9d8")
        self.assertEqual(
            data[209],
             "   :END:")
        self.assertEqual(
            data[210],
             "** All Souls' Day")
        self.assertEqual(
            data[211],
             "   :PROPERTIES:")
        self.assertEqual(
            data[212],
             "   :CREATED: <2010-11-02 Tue>--<2010-11-02 Tue>")
        self.assertEqual(
            data[213],
             "   :ID:      8e5563c2985dbde1b23370738273f8f06a493ca3")
        self.assertEqual(
            data[214],
             "   :END:")
        self.assertEqual(
            data[215],
             "** All Souls' Day")
        self.assertEqual(
            data[216],
             "   :PROPERTIES:")
        self.assertEqual(
            data[217],
             "   :CREATED: <2012-11-02 Fri>--<2012-11-02 Fri>")
        self.assertEqual(
            data[218],
             "   :ID:      509b615485eac996dc4a95267dc5685cb6f56738")
        self.assertEqual(
            data[219],
             "   :END:")
        self.assertEqual(
            data[220],
             "** All Saints' Day")
        self.assertEqual(
            data[221],
             "   :PROPERTIES:")
        self.assertEqual(
            data[222],
             "   :CREATED: <2010-11-01 Mon>--<2010-11-01 Mon>")
        self.assertEqual(
            data[223],
             "   :ID:      a84ec1d7424ef46c9eefa49fb9a46e867bb40c48")
        self.assertEqual(
            data[224],
             "   :END:")
        self.assertEqual(
            data[225],
             "** All Saints' Day")
        self.assertEqual(
            data[226],
             "   :PROPERTIES:")
        self.assertEqual(
            data[227],
             "   :CREATED: <2012-11-01 Thu>--<2012-11-01 Thu>")
        self.assertEqual(
            data[228],
             "   :ID:      025e9387e2f52f7e94aad2266acec6ba348eb9a8")
        self.assertEqual(
            data[229],
             "   :END:")
        self.assertEqual(
            data[230],
             "** All Saints' Day")
        self.assertEqual(
            data[231],
             "   :PROPERTIES:")
        self.assertEqual(
            data[232],
             "   :CREATED: <2011-11-01 Tue>--<2011-11-01 Tue>")
        self.assertEqual(
            data[233],
             "   :ID:      e44f87f68c0b5d3b73e532ba210cbf6737d9fd12")
        self.assertEqual(
            data[234],
             "   :END:")
