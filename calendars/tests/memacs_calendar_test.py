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
        memacs = CalendarMemacs(argv=argv.split())
        data = memacs.test_get_entries()
        #for d in range(len(data)):
        #      print "self.assertEqual(\n\tdata[%d],\n\t \"%s\")" % \
        #            (d, data[d])
        self.assertEqual(
            data[0],
             "** <2012-05-28 Mon>--<2012-05-28 Mon> Whit Monday")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :ID:             0c83f0a3ca8ff5354117f8f38ae862578168ae05")
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
             "   :ID:             e21842b27601508e5b3b53fc3baaab6a1ca96be7")
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
             "   :ID:             e21842b27601508e5b3b53fc3baaab6a1ca96be7")
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
             "   :ID:             e21842b27601508e5b3b53fc3baaab6a1ca96be7")
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
             "   :ID:             5a7c8c5342c367d20d7f81d86d2dfab3863cba94")
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
             "   :ID:             5a7c8c5342c367d20d7f81d86d2dfab3863cba94")
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
             "   :ID:             5a7c8c5342c367d20d7f81d86d2dfab3863cba94")
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
             "   :ID:             4cb0942069580b4af7099c104006fd69eb071729")
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
             "   :ID:             4cb0942069580b4af7099c104006fd69eb071729")
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
             "   :ID:             4cb0942069580b4af7099c104006fd69eb071729")
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
             "   :ID:             12ad58c0ae8928d38a1ed0526046120b8070a4ae")
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
             "   :ID:             12ad58c0ae8928d38a1ed0526046120b8070a4ae")
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
             "   :ID:             70270756c18c1afbfc131f7f238f1d14f2a555a0")
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
             "   :ID:             70270756c18c1afbfc131f7f238f1d14f2a555a0")
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
             "   :ID:             70270756c18c1afbfc131f7f238f1d14f2a555a0")
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
             "   :ID:             4748118d7fe930bbc850c5f9e0ddfd29af261359")
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
             "   :ID:             4748118d7fe930bbc850c5f9e0ddfd29af261359")
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
             "   :ID:             4748118d7fe930bbc850c5f9e0ddfd29af261359")
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
             "   :ID:             fea4063a6b411d536c6c8984e069246a60b3e33b")
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
             "   :ID:             fea4063a6b411d536c6c8984e069246a60b3e33b")
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
             "   :ID:             fea4063a6b411d536c6c8984e069246a60b3e33b")
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
             "   :ID:             5b5bf1bb44aa437924bbaeeb27af96879fe04772")
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
             "   :ID:             5b5bf1bb44aa437924bbaeeb27af96879fe04772")
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
             "   :ID:             5b5bf1bb44aa437924bbaeeb27af96879fe04772")
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
             "   :ID:             f0e5acae3e49404548844496dc99554e17492f67")
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
             "   :ID:             290444975d821c61d536c4dfab56d06bd2ab17af")
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
             "   :ID:             290444975d821c61d536c4dfab56d06bd2ab17af")
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
             "   :ID:             290444975d821c61d536c4dfab56d06bd2ab17af")
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
             "   :ID:             bba3224b1a56b7f5a6f17f8ced66819a748b1483")
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
             "   :ID:             2606285359704adc2fe251511f5adeb24d53898b")
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
             "   :ID:             d02d05010206893071a49491e5214c54843abfbd")
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
             "   :ID:             bc0a33b502b5758cdc7d30f67149f32809c05057")
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
             "   :ID:             bc0a33b502b5758cdc7d30f67149f32809c05057")
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
             "   :ID:             bc0a33b502b5758cdc7d30f67149f32809c05057")
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
             "   :ID:             051e56681a6282bb0ad3cd11837891397cde76b3")
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
             "   :ID:             051e56681a6282bb0ad3cd11837891397cde76b3")
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
             "   :ID:             051e56681a6282bb0ad3cd11837891397cde76b3")
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
             "   :ID:             1f17bd7220b2119c51733823566a45b8b00fd044")
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
             "   :ID:             1f17bd7220b2119c51733823566a45b8b00fd044")
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
             "   :ID:             1f17bd7220b2119c51733823566a45b8b00fd044")
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
             "   :ID:             d9afce0359fd03875146c0c7ba19ff79ac9c52fb")
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
             "   :ID:             b3f5a0572af51f26beaef4f7d7eddf7f9421448a")
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
             "   :ID:             b3f5a0572af51f26beaef4f7d7eddf7f9421448a")
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
             "   :ID:             b3f5a0572af51f26beaef4f7d7eddf7f9421448a")
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
             "   :ID:             71bca54e376ac4a9dfcb1eeef38a330fdc366817")
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
             "   :ID:             71bca54e376ac4a9dfcb1eeef38a330fdc366817")
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
             "   :ID:             71bca54e376ac4a9dfcb1eeef38a330fdc366817")
        self.assertEqual(
            data[187],
             "   :END:")