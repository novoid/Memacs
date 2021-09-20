# -*- coding: utf-8 -*-
# Time-stamp: <2016-01-23 18:07:46 vk>

import os
import re
import tempfile
import time
import unittest

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
             "** <2012-05-28 Mon> Whit Monday")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :ID:         8ba5a253410baff870da60487d97976bae948e6d")
        self.assertEqual(
            data[3],
             "   :END:")
        self.assertEqual(
            data[4],
             "** <2011-02-14 Mon> Valentine's day")
        self.assertEqual(
            data[5],
             "   :PROPERTIES:")
        self.assertEqual(
            data[6],
             "   :ID:         e5d97f07e8df141cddb101943449afddbc2c4366")
        self.assertEqual(
            data[7],
             "   :END:")
        self.assertEqual(
            data[8],
             "** <2010-02-14 Sun> Valentine's day")
        self.assertEqual(
            data[9],
             "   :PROPERTIES:")
        self.assertEqual(
            data[10],
             "   :ID:         7816a7cfdeebd359c435e5da53dbbe15e0902115")
        self.assertEqual(
            data[11],
             "   :END:")
        self.assertEqual(
            data[12],
             "** <2012-02-14 Tue> Valentine's day")
        self.assertEqual(
            data[13],
             "   :PROPERTIES:")
        self.assertEqual(
            data[14],
             "   :ID:         e3e1dfc836f4ddb91be7e396001993dc42dac33d")
        self.assertEqual(
            data[15],
             "   :END:")
        self.assertEqual(
            data[16],
             "** <2012-12-26 Wed> St. Stephan's Day")
        self.assertEqual(
            data[17],
             "   :PROPERTIES:")
        self.assertEqual(
            data[18],
             "   :ID:         5f2df9848d632c475e3cf509251f31359828cd19")
        self.assertEqual(
            data[19],
             "   :END:")
        self.assertEqual(
            data[20],
             "** <2010-12-26 Sun> St. Stephan's Day")
        self.assertEqual(
            data[21],
             "   :PROPERTIES:")
        self.assertEqual(
            data[22],
             "   :ID:         e74c056dfdb5ebcbfd8d725eacf5fe2180204705")
        self.assertEqual(
            data[23],
             "   :END:")
        self.assertEqual(
            data[24],
             "** <2011-12-26 Mon> St. Stephan's Day")
        self.assertEqual(
            data[25],
             "   :PROPERTIES:")
        self.assertEqual(
            data[26],
             "   :ID:         646b8200bd6186fc7c75bac6050486544edf9208")
        self.assertEqual(
            data[27],
             "   :END:")
        self.assertEqual(
            data[28],
             "** <2011-12-06 Tue> St. Nicholas")
        self.assertEqual(
            data[29],
             "   :PROPERTIES:")
        self.assertEqual(
            data[30],
             "   :ID:         3beb4ee6504aea9042b8a760a4cfdb82b24cb271")
        self.assertEqual(
            data[31],
             "   :END:")
        self.assertEqual(
            data[32],
             "** <2010-12-06 Mon> St. Nicholas")
        self.assertEqual(
            data[33],
             "   :PROPERTIES:")
        self.assertEqual(
            data[34],
             "   :ID:         ee05ddc226cfd7cbde339d25d9983a2e528040a9")
        self.assertEqual(
            data[35],
             "   :END:")
        self.assertEqual(
            data[36],
             "** <2012-12-06 Thu> St. Nicholas")
        self.assertEqual(
            data[37],
             "   :PROPERTIES:")
        self.assertEqual(
            data[38],
             "   :ID:         110237aee7b949c84e1c5614f1f7fb631c9ff942")
        self.assertEqual(
            data[39],
             "   :END:")
        self.assertEqual(
            data[40],
             "** <2011-12-31 Sat> New Year's Eve")
        self.assertEqual(
            data[41],
             "   :PROPERTIES:")
        self.assertEqual(
            data[42],
             "   :ID:         1a571159635d3d651b6af68d20620eade7f8a984")
        self.assertEqual(
            data[43],
             "   :END:")
        self.assertEqual(
            data[44],
             "** <2010-12-31 Fri> New Year's Eve")
        self.assertEqual(
            data[45],
             "   :PROPERTIES:")
        self.assertEqual(
            data[46],
             "   :ID:         cc2b9683716ac8d32c381ae9380d0a25f57ae0f5")
        self.assertEqual(
            data[47],
             "   :END:")
        self.assertEqual(
            data[48],
             "** <2012-01-01 Sun> New Year")
        self.assertEqual(
            data[49],
             "   :PROPERTIES:")
        self.assertEqual(
            data[50],
             "   :ID:         0b5b288f6b0322e0fae4beed157989d319b82814")
        self.assertEqual(
            data[51],
             "   :END:")
        self.assertEqual(
            data[52],
             "** <2010-01-01 Fri> New Year")
        self.assertEqual(
            data[53],
             "   :PROPERTIES:")
        self.assertEqual(
            data[54],
             "   :ID:         ab434dc5112a7a5c2237131c71ca254f5f99dc05")
        self.assertEqual(
            data[55],
             "   :END:")
        self.assertEqual(
            data[56],
             "** <2011-01-01 Sat> New Year")
        self.assertEqual(
            data[57],
             "   :PROPERTIES:")
        self.assertEqual(
            data[58],
             "   :ID:         869198e6dcfa0bc49fc171f17d50ba49d3fe62a7")
        self.assertEqual(
            data[59],
             "   :END:")
        self.assertEqual(
            data[60],
             "** <2010-10-26 Tue> National Holiday")
        self.assertEqual(
            data[61],
             "   :PROPERTIES:")
        self.assertEqual(
            data[62],
             "   :ID:         3c6042aba5db24b2ed09eedc1b3da56e7e0b601f")
        self.assertEqual(
            data[63],
             "   :END:")
        self.assertEqual(
            data[64],
             "** <2012-10-26 Fri> National Holiday")
        self.assertEqual(
            data[65],
             "   :PROPERTIES:")
        self.assertEqual(
            data[66],
             "   :ID:         601c8de3cea5d678e9919c9d64b1d7655f7843e5")
        self.assertEqual(
            data[67],
             "   :END:")
        self.assertEqual(
            data[68],
             "** <2011-10-26 Wed> National Holiday")
        self.assertEqual(
            data[69],
             "   :PROPERTIES:")
        self.assertEqual(
            data[70],
             "   :ID:         2f61fd1f446d4f384f3caf65a404d50b86f696a4")
        self.assertEqual(
            data[71],
             "   :END:")
        self.assertEqual(
            data[72],
             "** <2011-05-01 Sun> Labour Day")
        self.assertEqual(
            data[73],
             "   :PROPERTIES:")
        self.assertEqual(
            data[74],
             "   :ID:         781eb260ac25af31e97c26890f105ef7fdf03635")
        self.assertEqual(
            data[75],
             "   :END:")
        self.assertEqual(
            data[76],
             "** <2010-05-01 Sat> Labour Day")
        self.assertEqual(
            data[77],
             "   :PROPERTIES:")
        self.assertEqual(
            data[78],
             "   :ID:         70c5b304f299beac1474dd8bef716d47e1cf15a7")
        self.assertEqual(
            data[79],
             "   :END:")
        self.assertEqual(
            data[80],
             "** <2012-05-01 Tue> Labour Day")
        self.assertEqual(
            data[81],
             "   :PROPERTIES:")
        self.assertEqual(
            data[82],
             "   :ID:         c3b5e3ed1905b6a8c63847ad5ea12a87108f951f")
        self.assertEqual(
            data[83],
             "   :END:")
        self.assertEqual(
            data[84],
             "** <2012-12-08 Sat> Immaculate Conception")
        self.assertEqual(
            data[85],
             "   :PROPERTIES:")
        self.assertEqual(
            data[86],
             "   :ID:         9b716e3e1d58220b301621c6f027e73667ab7b52")
        self.assertEqual(
            data[87],
             "   :END:")
        self.assertEqual(
            data[88],
             "** <2010-12-08 Wed> Immaculate Conception")
        self.assertEqual(
            data[89],
             "   :PROPERTIES:")
        self.assertEqual(
            data[90],
             "   :ID:         b9a77981c516f27a9985223d5af3e578f1d11c3d")
        self.assertEqual(
            data[91],
             "   :END:")
        self.assertEqual(
            data[92],
             "** <2011-12-08 Thu> Immaculate Conception")
        self.assertEqual(
            data[93],
             "   :PROPERTIES:")
        self.assertEqual(
            data[94],
             "   :ID:         4043adda1b297521c55cd06b912de52e1373a999")
        self.assertEqual(
            data[95],
             "   :END:")
        self.assertEqual(
            data[96],
             "** <2012-04-06 Fri> Good Friday")
        self.assertEqual(
            data[97],
             "   :PROPERTIES:")
        self.assertEqual(
            data[98],
             "   :ID:         344c7600e82efb9445e871b931877d051b94b6c9")
        self.assertEqual(
            data[99],
             "   :END:")
        self.assertEqual(
            data[100],
             "** <2010-01-06 Wed> Epiphany")
        self.assertEqual(
            data[101],
             "   :PROPERTIES:")
        self.assertEqual(
            data[102],
             "   :ID:         93ba1d459c22550601fffa38c9204067296a51e1")
        self.assertEqual(
            data[103],
             "   :END:")
        self.assertEqual(
            data[104],
             "** <2012-01-06 Fri> Epiphany")
        self.assertEqual(
            data[105],
             "   :PROPERTIES:")
        self.assertEqual(
            data[106],
             "   :ID:         699f5d8d424735f5593e1d1d44604f529c4fdbb3")
        self.assertEqual(
            data[107],
             "   :END:")
        self.assertEqual(
            data[108],
             "** <2011-01-06 Thu> Epiphany")
        self.assertEqual(
            data[109],
             "   :PROPERTIES:")
        self.assertEqual(
            data[110],
             "   :ID:         d48ee26b995cb0c2033077c99788ec6cca5afb66")
        self.assertEqual(
            data[111],
             "   :END:")
        self.assertEqual(
            data[112],
             "** <2012-04-09 Mon> Easter Monday")
        self.assertEqual(
            data[113],
             "   :PROPERTIES:")
        self.assertEqual(
            data[114],
             "   :ID:         c69c15ca890a76c6c982f7a998ae4c9ce79ddd45")
        self.assertEqual(
            data[115],
             "   :END:")
        self.assertEqual(
            data[116],
             "** <2012-04-08 Sun> Easter")
        self.assertEqual(
            data[117],
             "   :PROPERTIES:")
        self.assertEqual(
            data[118],
             "   :ID:         f0d2b4a8dbcca5208b2aab6755e8cd7c1efe18e5")
        self.assertEqual(
            data[119],
             "   :END:")
        self.assertEqual(
            data[120],
             "** <2012-06-07 Thu> Corpus Christi")
        self.assertEqual(
            data[121],
             "   :PROPERTIES:")
        self.assertEqual(
            data[122],
             "   :ID:         32e659d60f167f7386c8269644c9c920614ce55d")
        self.assertEqual(
            data[123],
             "   :END:")
        self.assertEqual(
            data[124],
             "** <2011-12-24 Sat> Christmas Eve")
        self.assertEqual(
            data[125],
             "   :PROPERTIES:")
        self.assertEqual(
            data[126],
             "   :ID:         949f24fdaa8122916bad02b3548e402b2d2391e7")
        self.assertEqual(
            data[127],
             "   :END:")
        self.assertEqual(
            data[128],
             "** <2010-12-24 Fri> Christmas Eve")
        self.assertEqual(
            data[129],
             "   :PROPERTIES:")
        self.assertEqual(
            data[130],
             "   :ID:         96dfd09ae391c0a4e1ecd00ffbc875e714dcf9c6")
        self.assertEqual(
            data[131],
             "   :END:")
        self.assertEqual(
            data[132],
             "** <2012-12-24 Mon> Christmas Eve")
        self.assertEqual(
            data[133],
             "   :PROPERTIES:")
        self.assertEqual(
            data[134],
             "   :ID:         554ab6eebf09552bccc3264f46000f98a3812ab0")
        self.assertEqual(
            data[135],
             "   :END:")
        self.assertEqual(
            data[136],
             "** <2010-12-25 Sat> Christmas")
        self.assertEqual(
            data[137],
             "   :PROPERTIES:")
        self.assertEqual(
            data[138],
             "   :ID:         9047b4007e15ff0250613e25650aadb1be5ff8a7")
        self.assertEqual(
            data[139],
             "   :END:")
        self.assertEqual(
            data[140],
             "** <2011-12-25 Sun> Christmas")
        self.assertEqual(
            data[141],
             "   :PROPERTIES:")
        self.assertEqual(
            data[142],
             "   :ID:         a4e7890b6ce1602706a74fff5a0fc067492dc586")
        self.assertEqual(
            data[143],
             "   :END:")
        self.assertEqual(
            data[144],
             "** <2012-12-25 Tue> Christmas")
        self.assertEqual(
            data[145],
             "   :PROPERTIES:")
        self.assertEqual(
            data[146],
             "   :ID:         6eee35b32d3d3e172e14528e32c02e7bae48e3fc")
        self.assertEqual(
            data[147],
             "   :END:")
        self.assertEqual(
            data[148],
             "** <2010-08-15 Sun> Assumption")
        self.assertEqual(
            data[149],
             "   :PROPERTIES:")
        self.assertEqual(
            data[150],
             "   :ID:         be5c5c89e8e8f98ada9548422b3707fff9d41512")
        self.assertEqual(
            data[151],
             "   :END:")
        self.assertEqual(
            data[152],
             "** <2012-08-15 Wed> Assumption")
        self.assertEqual(
            data[153],
             "   :PROPERTIES:")
        self.assertEqual(
            data[154],
             "   :ID:         71156b8c067eabdea667f8696395011414ab967c")
        self.assertEqual(
            data[155],
             "   :END:")
        self.assertEqual(
            data[156],
             "** <2011-08-15 Mon> Assumption")
        self.assertEqual(
            data[157],
             "   :PROPERTIES:")
        self.assertEqual(
            data[158],
             "   :ID:         aaf4f5c9ff6a712b701539baa69d3afede23012c")
        self.assertEqual(
            data[159],
             "   :END:")
        self.assertEqual(
            data[160],
             "** <2012-05-17 Thu> Ascension Day")
        self.assertEqual(
            data[161],
             "   :PROPERTIES:")
        self.assertEqual(
            data[162],
             "   :ID:         e219abf88617f8796c9fba500e3bb9b829dac14a")
        self.assertEqual(
            data[163],
             "   :END:")
        self.assertEqual(
            data[164],
             "** <2011-11-02 Wed> All Souls' Day")
        self.assertEqual(
            data[165],
             "   :PROPERTIES:")
        self.assertEqual(
            data[166],
             "   :ID:         1dd09748419fc6f7eee66184febf879f6323a2d5")
        self.assertEqual(
            data[167],
             "   :END:")
        self.assertEqual(
            data[168],
             "** <2010-11-02 Tue> All Souls' Day")
        self.assertEqual(
            data[169],
             "   :PROPERTIES:")
        self.assertEqual(
            data[170],
             "   :ID:         c7559b4e0501b55eecce604b3939e34683a60fb8")
        self.assertEqual(
            data[171],
             "   :END:")
        self.assertEqual(
            data[172],
             "** <2012-11-02 Fri> All Souls' Day")
        self.assertEqual(
            data[173],
             "   :PROPERTIES:")
        self.assertEqual(
            data[174],
             "   :ID:         581e71732c88e6225a282be86e284002ddd23b97")
        self.assertEqual(
            data[175],
             "   :END:")
        self.assertEqual(
            data[176],
             "** <2010-11-01 Mon> All Saints' Day")
        self.assertEqual(
            data[177],
             "   :PROPERTIES:")
        self.assertEqual(
            data[178],
             "   :ID:         69e6dffd28ba8b5f396fb9ceecf115d0f08a6369")
        self.assertEqual(
            data[179],
             "   :END:")
        self.assertEqual(
            data[180],
             "** <2012-11-01 Thu> All Saints' Day")
        self.assertEqual(
            data[181],
             "   :PROPERTIES:")
        self.assertEqual(
            data[182],
             "   :ID:         554ed843558464e3867d3154d88541a953f23708")
        self.assertEqual(
            data[183],
             "   :END:")
        self.assertEqual(
            data[184],
             "** <2011-11-01 Tue> All Saints' Day")
        self.assertEqual(
            data[185],
             "   :PROPERTIES:")
        self.assertEqual(
            data[186],
             "   :ID:         aa06dce749fe46fabe338df8bee04ecdfa0b120a")
        self.assertEqual(
            data[187],
             "   :END:")
        self.assertEqual(
            data[188:194], ['** <2011-08-22 Mon 16:10>--<9999-12-31 Fri> No end time/date',
                            '   :PROPERTIES:',
                            '   :DESCRIPTION: No end time/date',
                            '   :ID:          23c8b62cf2043b91627ffb832fa565fc125f95a3',
                            '   :END:'])

    def __build_ical_str(self, dtstart, dtend, extra):
        if dtend:
            dtend = "DTEND" + dtend + "\n"

        return ("BEGIN:VCALENDAR\n"
                "VERSION:2.0\n"
                "PRODID:manual\n"
                + (extra or "") +
                "BEGIN:VEVENT\n"
                "CLASS:PUBLIC\n"
                "DTSTART" + dtstart + "\n"
                + (dtend or "") +
                "UID:whatever.ics\n"
                "DTSTAMP:20190127T140400\n"
                "DESCRIPTION:whatever\n"
                "SUMMARY:whatever\n"
                "END:VEVENT\n"
                "END:VCALENDAR\n")

    # Several variations need to be tested here:
    #
    # - DATE-TIME:
    #   - [1] UTC
    #   - [2] VTIMEZONE-specifed
    #   - [3] Inline (IANA-style, w/o VTIMEZONE)*
    #   - Floating:
    #     - [4] Basic case (truly floating)
    #     - [5] w/ X-WR-TIMEZONE*
    #   - [6] No end DATE-TIME
    # - DATE:
    #   - [7] Basic case (differing dates)
    #   - [8] One-day, all-day event (collapsed to single org timestamp)
    #   - [9] No end DATE
    #
    # * = not included in RFC5545, but commonly in use.
    def test_date_handling(self):
        os.environ['TZ'] = "America/Chicago"
        time.tzset()

        VTIMEZONE_COMPONENT = ("BEGIN:VTIMEZONE\n"
                               "TZID:My/Berlin\n"
                               "TZURL:http://tzurl.org/zoneinfo-outlook/Europe/Berlin\n"
                               "X-LIC-LOCATION:Europe/Berlin\n"
                               "BEGIN:DAYLIGHT\n"
                               "TZOFFSETFROM:+0100\n"
                               "TZOFFSETTO:+0200\n"
                               "TZNAME:CEST\n"
                               "DTSTART:19700329T020000\n"
                               "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU\n"
                               "END:DAYLIGHT\n"
                               "BEGIN:STANDARD\n"
                               "TZOFFSETFROM:+0200\n"
                               "TZOFFSETTO:+0100\n"
                               "TZNAME:CET\n"
                               "DTSTART:19701025T030000\n"
                               "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU\n"
                               "END:STANDARD\n"
                               "END:VTIMEZONE\n")

        cases = [(':20181103T201500Z',                     ':20181103T211500Z',                    None,                             '<2018-11-03 Sat 15:15>--<2018-11-03 Sat 16:15>'), # [1]
                 (':20181103T201500Z',                     ':20181103T201500Z',                    None,                             '<2018-11-03 Sat 15:15>--<2018-11-03 Sat 15:15>'), # [1] (no collapse)
                 (';TZID=My/Berlin:20181103T201500',       ';TZID=My/Berlin:20181103T211500',      VTIMEZONE_COMPONENT,              '<2018-11-03 Sat 14:15>--<2018-11-03 Sat 15:15>'), # [2]
                 (';TZID=Europe/Berlin:20181103T201500:',  ';TZID=Europe/Berlin:20181103T211500',  None,                             '<2018-11-03 Sat 14:15>--<2018-11-03 Sat 15:15>'), # [3]
                 (';TZID=Europe/Berlin:20181103T201500',   ';TZID=Europe/Berlin:20181103T211500',  'X-WR-TIMEZONE:America/Denver\n', '<2018-11-03 Sat 14:15>--<2018-11-03 Sat 15:15>'), # [3] (X-WR-TIMEZONE ignored)
                 (':20181103T201500',                      ':20181103T211500',                     None,                             '<2018-11-03 Sat 20:15>--<2018-11-03 Sat 21:15>'), # [4]
                 (':20181103T201500',                      ':20181103T211500',                     'X-WR-TIMEZONE:Europe/Berlin\n',  '<2018-11-03 Sat 14:15>--<2018-11-03 Sat 15:15>'), # [5]
                 (':20181103T201500',                      None,                                   'X-WR-TIMEZONE:Europe/Berlin\n',  '<2018-11-03 Sat 14:15>--<9999-12-31 Fri>'),       # [6]
                 (':20210201',                             ':20210204',                            None,                             '<2021-02-01 Mon>--<2021-02-03 Wed>'),             # [7]
                 (':20210201',                             ':20210204',                            'X-WR-TIMEZONE:Europe/Berlin\n',  '<2021-02-01 Mon>--<2021-02-03 Wed>'),             # [7] (X-WR-TIMEZONE ignored)
                 (':20210201',                             ':20210202',                            'X-WR-TIMEZONE:Europe/Berlin\n',  '<2021-02-01 Mon>'),                               # [8]
                 (':20210201',                             None,                                   'X-WR-TIMEZONE:Europe/Berlin\n',  '<2021-02-01 Mon>--<9999-12-31 Fri>')]             # [9]

        for (dtstart, dtend, extra, output) in cases:
            with tempfile.NamedTemporaryFile("wt") as tmp:
                tmp.write(self.__build_ical_str(dtstart, dtend, extra))
                tmp.seek(0)

                print("+++ Testing: " + dtstart + " / " + str(dtend) + " / " + str(extra)[:10] + " +++")

                argv = "-s -cf " + tmp.name
                memacs = CalendarMemacs(argv=argv.split())
                data = memacs.test_get_entries()

                m = re.search("<.*>", data[0]).group(0)
                self.assertEqual(output, m)
