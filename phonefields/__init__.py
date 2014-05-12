# -*- coding: utf-8 -*-
import re

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy


country_data = (
    (998, 'UZ / UZB ', ugettext_lazy('Uzbekistan')),
    (996, 'KG / KGZ ', ugettext_lazy('Kyrgyzstan')),
    (995, 'GE / GEO ', ugettext_lazy('Georgia')),
    (994, 'AZ / AZE ', ugettext_lazy('Azerbaijan')),
    (993, 'TM / TKM ', ugettext_lazy('Turkmenistan')),
    (992, 'TJ / TJK ', ugettext_lazy('Tajikistan')),
    (977, 'NP / NPL ', ugettext_lazy('Nepal')),
    (976, 'MN / MNG ', ugettext_lazy('Mongolia')),
    (975, 'BT / BTN ', ugettext_lazy('Bhutan')),
    (974, 'QA / QAT ', ugettext_lazy('Qatar')),
    (973, 'BH / BHR ', ugettext_lazy('Bahrain')),
    (972, 'IL / ISR ', ugettext_lazy('Israel')),
    (971, 'AE / ARE ', ugettext_lazy('United Arab Emirates')),
    (970, ' /  ', ugettext_lazy('Gaza Strip')),
    (970, ' /  ', ugettext_lazy('West Bank')),
    (968, 'OM / OMN ', ugettext_lazy('Oman')),
    (967, 'YE / YEM ', ugettext_lazy('Yemen')),
    (966, 'SA / SAU ', ugettext_lazy('Saudi Arabia')),
    (965, 'KW / KWT ', ugettext_lazy('Kuwait')),
    (964, 'IQ / IRQ ', ugettext_lazy('Iraq')),
    (963, 'SY / SYR ', ugettext_lazy('Syria')),
    (962, 'JO / JOR ', ugettext_lazy('Jordan')),
    (961, 'LB / LBN ', ugettext_lazy('Lebanon')),
    (960, 'MV / MDV ', ugettext_lazy('Maldives')),
    (886, 'TW / TWN ', ugettext_lazy('Taiwan')),
    (880, 'BD / BGD ', ugettext_lazy('Bangladesh')),
    (870, 'PN / PCN ', ugettext_lazy('Pitcairn Islands')),
    (856, 'LA / LAO ', ugettext_lazy('Laos')),
    (855, 'KH / KHM ', ugettext_lazy('Cambodia')),
    (853, 'MO / MAC ', ugettext_lazy('Macau')),
    (852, 'HK / HKG ', ugettext_lazy('Hong Kong')),
    (850, 'KP / PRK ', ugettext_lazy('North Korea')),
    (692, 'MH / MHL ', ugettext_lazy('Marshall Islands')),
    (691, 'FM / FSM ', ugettext_lazy('Micronesia')),
    (690, 'TK / TKL ', ugettext_lazy('Tokelau')),
    (689, 'PF / PYF ', ugettext_lazy('French Polynesia')),
    (688, 'TV / TUV ', ugettext_lazy('Tuvalu')),
    (687, 'NC / NCL ', ugettext_lazy('New Caledonia')),
    (686, 'KI / KIR ', ugettext_lazy('Kiribati')),
    (685, 'WS / WSM ', ugettext_lazy('Samoa')),
    (683, 'NU / NIU ', ugettext_lazy('Niue')),
    (682, 'CK / COK ', ugettext_lazy('Cook Islands')),
    (681, 'WF / WLF ', ugettext_lazy('Wallis and Futuna')),
    (680, 'PW / PLW ', ugettext_lazy('Palau')),
    (679, 'FJ / FJI ', ugettext_lazy('Fiji')),
    (678, 'VU / VUT ', ugettext_lazy('Vanuatu')),
    (677, 'SB / SLB ', ugettext_lazy('Solomon Islands')),
    (676, 'TO / TON ', ugettext_lazy('Tonga')),
    (675, 'PG / PNG ', ugettext_lazy('Papua New Guinea')),
    (674, 'NR / NRU ', ugettext_lazy('Nauru')),
    (673, 'BN / BRN ', ugettext_lazy('Brunei')),
    (672, 'AQ / ATA ', ugettext_lazy('Antarctica')),
    (672, ' / NFK ', ugettext_lazy('Norfolk Island')),
    (670, 'TL / TLS ', ugettext_lazy('Timor-Leste')),
    (599, 'AN / ANT ', ugettext_lazy('Netherlands Antilles')),
    (598, 'UY / URY ', ugettext_lazy('Uruguay')),
    (597, 'SR / SUR ', ugettext_lazy('Suriname')),
    (595, 'PY / PRY ', ugettext_lazy('Paraguay')),
    (593, 'EC / ECU ', ugettext_lazy('Ecuador')),
    (592, 'GY / GUY ', ugettext_lazy('Guyana')),
    (591, 'BO / BOL ', ugettext_lazy('Bolivia')),
    (590, 'BL / BLM ', ugettext_lazy('Saint Barthelemy')),
    (509, 'HT / HTI ', ugettext_lazy('Haiti')),
    (508, 'PM / SPM ', ugettext_lazy('Saint Pierre and Miquelon')),
    (507, 'PA / PAN ', ugettext_lazy('Panama')),
    (506, 'CR / CRC ', ugettext_lazy('Costa Rica')),
    (505, 'NI / NIC ', ugettext_lazy('Nicaragua')),
    (504, 'HN / HND ', ugettext_lazy('Honduras')),
    (503, 'SV / SLV ', ugettext_lazy('El Salvador')),
    (502, 'GT / GTM ', ugettext_lazy('Guatemala')),
    (501, 'BZ / BLZ ', ugettext_lazy('Belize')),
    (500, 'FK / FLK ', ugettext_lazy('Falkland Islands')),
    (423, 'LI / LIE ', ugettext_lazy('Liechtenstein')),
    (421, 'SK / SVK ', ugettext_lazy('Slovakia')),
    (420, 'CZ / CZE ', ugettext_lazy('Czech Republic')),
    (389, 'MK / MKD ', ugettext_lazy('Macedonia')),
    (387, 'BA / BIH ', ugettext_lazy('Bosnia and Herzegovina')),
    (386, 'SI / SVN ', ugettext_lazy('Slovenia')),
    (385, 'HR / HRV ', ugettext_lazy('Croatia')),
    (382, 'ME / MNE ', ugettext_lazy('Montenegro')),
    (381, ' /  ', ugettext_lazy('Kosovo')),
    (381, 'RS / SRB ', ugettext_lazy('Serbia')),
    (380, 'UA / UKR ', ugettext_lazy('Ukraine')),
    (378, 'SM / SMR ', ugettext_lazy('San Marino')),
    (377, 'MC / MCO ', ugettext_lazy('Monaco')),
    (376, 'AD / AND ', ugettext_lazy('Andorra')),
    (375, 'BY / BLR ', ugettext_lazy('Belarus')),
    (374, 'AM / ARM ', ugettext_lazy('Armenia')),
    (373, 'MD / MDA ', ugettext_lazy('Moldova')),
    (372, 'EE / EST ', ugettext_lazy('Estonia')),
    (371, 'LV / LVA ', ugettext_lazy('Latvia')),
    (370, 'LT / LTU ', ugettext_lazy('Lithuania')),
    (359, 'BG / BGR ', ugettext_lazy('Bulgaria')),
    (358, 'FI / FIN ', ugettext_lazy('Finland')),
    (357, 'CY / CYP ', ugettext_lazy('Cyprus')),
    (356, 'MT / MLT ', ugettext_lazy('Malta')),
    (355, 'AL / ALB ', ugettext_lazy('Albania')),
    (354, 'IS / IS ', ugettext_lazy('Iceland')),
    (353, 'IE / IRL ', ugettext_lazy('Ireland')),
    (352, 'LU / LUX ', ugettext_lazy('Luxembourg')),
    (351, 'PT / PRT ', ugettext_lazy('Portugal')),
    (350, 'GI / GIB ', ugettext_lazy('Gibraltar')),
    (299, 'GL / GRL ', ugettext_lazy('Greenland')),
    (298, 'FO / FRO ', ugettext_lazy('Faroe Islands')),
    (297, 'AW / ABW ', ugettext_lazy('Aruba')),
    (291, 'ER / ERI ', ugettext_lazy('Eritrea')),
    (290, 'SH / SHN ', ugettext_lazy('Saint Helena')),
    (269, 'KM / COM ', ugettext_lazy('Comoros')),
    (268, 'SZ / SWZ ', ugettext_lazy('Swaziland')),
    (267, 'BW / BWA ', ugettext_lazy('Botswana')),
    (266, 'LS / LSO ', ugettext_lazy('Lesotho')),
    (265, 'MW / MWI ', ugettext_lazy('Malawi')),
    (264, 'NA / NAM ', ugettext_lazy('Namibia')),
    (263, 'ZW / ZWE ', ugettext_lazy('Zimbabwe')),
    (262, 'YT / MYT ', ugettext_lazy('Mayotte')),
    (261, 'MG / MDG ', ugettext_lazy('Madagascar')),
    (260, 'ZM / ZMB ', ugettext_lazy('Zambia')),
    (258, 'MZ / MOZ ', ugettext_lazy('Mozambique')),
    (257, 'BI / BDI ', ugettext_lazy('Burundi')),
    (256, 'UG / UGA ', ugettext_lazy('Uganda')),
    (255, 'TZ / TZA ', ugettext_lazy('Tanzania')),
    (254, 'KE / KEN ', ugettext_lazy('Kenya')),
    (253, 'DJ / DJI ', ugettext_lazy('Djibouti')),
    (252, 'SO / SOM ', ugettext_lazy('Somalia')),
    (251, 'ET / ETH ', ugettext_lazy('Ethiopia')),
    (250, 'RW / RWA ', ugettext_lazy('Rwanda')),
    (249, 'SD / SDN ', ugettext_lazy('Sudan')),
    (248, 'SC / SYC ', ugettext_lazy('Seychelles')),
    (245, 'GW / GNB ', ugettext_lazy('Guinea-Bissau')),
    (244, 'AO / AGO ', ugettext_lazy('Angola')),
    (243, 'CD / COD ', ugettext_lazy('Democratic Republic of the Congo')),
    (242, 'CG / COG ', ugettext_lazy('Republic of the Congo')),
    (241, 'GA / GAB ', ugettext_lazy('Gabon')),
    (240, 'GQ / GNQ ', ugettext_lazy('Equatorial Guinea')),
    (239, 'ST / STP ', ugettext_lazy('Sao Tome and Principe')),
    (238, 'CV / CPV ', ugettext_lazy('Cape Verde')),
    (237, 'CM / CMR ', ugettext_lazy('Cameroon')),
    (236, 'CF / CAF ', ugettext_lazy('Central African Republic')),
    (235, 'TD / TCD ', ugettext_lazy('Chad')),
    (234, 'NG / NGA ', ugettext_lazy('Nigeria')),
    (233, 'GH / GHA ', ugettext_lazy('Ghana')),
    (232, 'SL / SLE ', ugettext_lazy('Sierra Leone')),
    (231, 'LR / LBR ', ugettext_lazy('Liberia')),
    (230, 'MU / MUS ', ugettext_lazy('Mauritius')),
    (229, 'BJ / BEN ', ugettext_lazy('Benin')),
    (228, 'TG / TGO ', ugettext_lazy('Togo')),
    (227, 'NE / NER ', ugettext_lazy('Niger')),
    (226, 'BF / BFA ', ugettext_lazy('Burkina Faso')),
    (225, 'CI / CIV ', ugettext_lazy('Ivory Coast')),
    (224, 'GN / GIN ', ugettext_lazy('Guinea')),
    (223, 'ML / MLI ', ugettext_lazy('Mali')),
    (222, 'MR / MRT ', ugettext_lazy('Mauritania')),
    (221, 'SN / SEN ', ugettext_lazy('Senegal')),
    (220, 'GM / GMB ', ugettext_lazy('Gambia')),
    (218, 'LY / LBY ', ugettext_lazy('Libya')),
    (216, 'TN / TUN ', ugettext_lazy('Tunisia')),
    (213, 'DZ / DZA ', ugettext_lazy('Algeria')),
    (212, 'MA / MAR ', ugettext_lazy('Morocco')),
    (98, 'IR / IRN ', ugettext_lazy('Iran')),
    (95, 'MM / MMR ', ugettext_lazy('Burma (Myanmar)')),
    (94, 'LK / LKA ', ugettext_lazy('Sri Lanka')),
    (93, 'AF / AFG ', ugettext_lazy('Afghanistan')),
    (92, 'PK / PAK ', ugettext_lazy('Pakistan')),
    (91, 'IN / IND ', ugettext_lazy('India')),
    (90, 'TR / TUR ', ugettext_lazy('Turkey')),
    (86, 'CN / CHN ', ugettext_lazy('China')),
    (84, 'VN / VNM ', ugettext_lazy('Vietnam')),
    (82, 'KR / KOR ', ugettext_lazy('South Korea')),
    (81, 'JP / JPN ', ugettext_lazy('Japan')),
    (66, 'TH / THA ', ugettext_lazy('Thailand')),
    (65, 'SG / SGP ', ugettext_lazy('Singapore')),
    (64, 'NZ / NZL ', ugettext_lazy('New Zealand')),
    (63, 'PH / PHL ', ugettext_lazy('Philippines')),
    (62, 'ID / IDN ', ugettext_lazy('Indonesia')),
    (61, 'AU / AUS ', ugettext_lazy('Australia')),
    (61, 'CX / CXR ', ugettext_lazy('Christmas Island')),
    (61, 'CC / CCK ', ugettext_lazy('Cocos (Keeling) Islands')),
    (60, 'MY / MYS ', ugettext_lazy('Malaysia')),
    (58, 'VE / VEN ', ugettext_lazy('Venezuela')),
    (57, 'CO / COL ', ugettext_lazy('Colombia')),
    (56, 'CL / CHL ', ugettext_lazy('Chile')),
    (55, 'BR / BRA ', ugettext_lazy('Brazil')),
    (54, 'AR / ARG ', ugettext_lazy('Argentina')),
    (53, 'CU / CUB ', ugettext_lazy('Cuba')),
    (52, 'MX / MEX ', ugettext_lazy('Mexico')),
    (51, 'PE / PER ', ugettext_lazy('Peru')),
    (49, 'DE / DEU ', ugettext_lazy('Germany')),
    (48, 'PL / POL ', ugettext_lazy('Poland')),
    (47, 'NO / NOR ', ugettext_lazy('Norway')),
    (46, 'SE / SWE ', ugettext_lazy('Sweden')),
    (45, 'DK / DNK ', ugettext_lazy('Denmark')),
    (44, 'IM / IMN ', ugettext_lazy('Isle of Man')),
    (44, 'GB / GBR ', ugettext_lazy('United Kingdom')),
    (43, 'AT / AUT ', ugettext_lazy('Austria')),
    (41, 'CH / CHE ', ugettext_lazy('Switzerland')),
    (40, 'RO / ROU ', ugettext_lazy('Romania')),
    (39, 'IT / ITA ', ugettext_lazy('Italy')),
    (39, 'VA / VAT ', ugettext_lazy('Holy See (Vatican City)')),
    (36, 'HU / HUN ', ugettext_lazy('Hungary')),
    (34, 'ES / ESP ', ugettext_lazy('Spain')),
    (33, 'FR / FRA ', ugettext_lazy('France')),
    (32, 'BE / BEL ', ugettext_lazy('Belgium')),
    (31, 'NL / NLD ', ugettext_lazy('Netherlands')),
    (30, 'GR / GRC ', ugettext_lazy('Greece')),
    (27, 'ZA / ZAF ', ugettext_lazy('South Africa')),
    (20, 'EG / EGY ', ugettext_lazy('Egypt')),
    (7, 'KZ / KAZ ', ugettext_lazy('Kazakhstan')),
    (7, 'RU / RUS ', ugettext_lazy('Russia')),
    (1, 'PR / PRI ', ugettext_lazy('Puerto Rico')),
    (1, 'US / USA ', ugettext_lazy('United States')),
    (1, 'CA / CAN ', ugettext_lazy('Canada')),
    (1684, 'AS / ASM ', ugettext_lazy('American Samoa')),
    (1264, 'AI / AIA ', ugettext_lazy('Anguilla')),
    (1268, 'AG / ATG ', ugettext_lazy('Antigua and Barbuda')),
    (1242, 'BS / BHS ', ugettext_lazy('Bahamas')),
    (1246, 'BB / BRB ', ugettext_lazy('Barbados')),
    (1441, 'BM / BMU ', ugettext_lazy('Bermuda')),
    (1284, 'VG / VGB ', ugettext_lazy('British Virgin Islands')),
    (1345, 'KY / CYM ', ugettext_lazy('Cayman Islands')),
    (1767, 'DM / DMA ', ugettext_lazy('Dominica')),
    (1809, 'DO / DOM ', ugettext_lazy('Dominican Republic')),
    (1473, 'GD / GRD ', ugettext_lazy('Grenada')),
    (1671, 'GU / GUM ', ugettext_lazy('Guam')),
    (1876, 'JM / JAM ', ugettext_lazy('Jamaica')),
    (1664, 'MS / MSR ', ugettext_lazy('Montserrat')),
    (1670, 'MP / MNP ', ugettext_lazy('Northern Mariana Islands')),
    (1869, 'KN / KNA ', ugettext_lazy('Saint Kitts and Nevis')),
    (1758, 'LC / LCA ', ugettext_lazy('Saint Lucia')),
    (1599, 'MF / MAF ', ugettext_lazy('Saint Martin')),
    (1784, 'VC / VCT ', ugettext_lazy('Saint Vincent and the Grenadines')),
    (1868, 'TT / TTO ', ugettext_lazy('Trinidad and Tobago')),
    (1649, 'TC / TCA ', ugettext_lazy('Turks and Caicos Islands')),
    (1340, 'VI / VIR ', ugettext_lazy('US Virgin Islands')),
    (None, 'EH / ESH ', ugettext_lazy('Western Sahara')),
    (None, 'IO / IOT ', ugettext_lazy('British Indian Ocean Territory')),
    (None, 'JE / JEY ', ugettext_lazy('Jersey')),
    (None, 'SJ / SJM ', ugettext_lazy('Svalbard')),
)


all_codes = sorted(set(str(code) for code, _, __ in country_data if code),
                   key=lambda v: (-len(v), int(v)))


class FullPhoneFormField(forms.CharField):
    u"""
    >>> class Form(forms.Form):
    ...     phone = FullPhoneFormField()
    >>> Form({'phone': '            '}).is_valid()
    False
    >>> Form({'phone': ' 8 923  987 22 11  '}).is_valid()
    True
    """
    available_codes = getattr(settings, 'AVAILABLE_PHONE_COUNTRY_CODES', None) or all_codes
    default_code = getattr(settings, 'DEFAULT_PHONE_COUNTRY_CODE', '7')
    min_phone_length = 8
    max_phone_length = 10

    def clean(self, value):
        u"""
        >>> FullPhoneFormField().clean('9161234567')
        u'+79161234567'
        >>> FullPhoneFormField().clean('89161234567')
        u'+79161234567'
        >>> FullPhoneFormField().clean('+7(916)1234567')
        u'+79161234567'
        >>> FullPhoneFormField().clean('(916)1234567')
        u'+79161234567'
        >>> FullPhoneFormField().clean(u' 8(916)-123-45-67 ')
        u'+79161234567'
        """
        if value:
            value = value.strip()

            phone = None
            code = None

            has_country_code = value.startswith('+')
            value = value.lstrip('+')
            value = re.sub('[^\d]', '', value)

            if not has_country_code:
                phone = value[1:] if value.startswith('8') else value
                code = self.default_code
            else:
                for c in self.available_codes:
                    if value.startswith(c):
                        phone = value[len(c):]
                        code = c
                        break
                if not phone:
                    raise ValidationError(ugettext('Unsupported country code'))

            length = len(phone)
            if not (self.min_phone_length <= length <= self.max_phone_length):
                raise ValidationError(ugettext('Incorrect phone'))

            value = '+' + code + phone
        return super(FullPhoneFormField, self).clean(value)


class FullPhoneDbField(models.CharField):
    _max_length = 20
    _options = None

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = self._max_length
        self._options = (args, kwargs)
        super(FullPhoneDbField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = FullPhoneFormField
        return super(FullPhoneDbField, self).formfield(**kwargs)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = 'django.db.models.fields.CharField'
        args, kwargs = introspector(models.CharField(*self._options[0], **self._options[1]))
        kwargs['max_length'] = self._max_length
        return field_class, args, kwargs
