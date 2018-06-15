# -*- coding: utf-8 -*-
import re


if __name__ == '__main__':
    from django.conf import settings
    if not settings.configured:
        settings.configure()


from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

country_data = (
    (998, 'UZ / UZB ', _('Uzbekistan')),
    (996, 'KG / KGZ ', _('Kyrgyzstan')),
    (995, 'GE / GEO ', _('Georgia')),
    (994, 'AZ / AZE ', _('Azerbaijan')),
    (993, 'TM / TKM ', _('Turkmenistan')),
    (992, 'TJ / TJK ', _('Tajikistan')),
    (977, 'NP / NPL ', _('Nepal')),
    (976, 'MN / MNG ', _('Mongolia')),
    (975, 'BT / BTN ', _('Bhutan')),
    (974, 'QA / QAT ', _('Qatar')),
    (973, 'BH / BHR ', _('Bahrain')),
    (972, 'IL / ISR ', _('Israel')),
    (971, 'AE / ARE ', _('United Arab Emirates')),
    (970, ' /  ', _('Gaza Strip')),
    (970, ' /  ', _('West Bank')),
    (968, 'OM / OMN ', _('Oman')),
    (967, 'YE / YEM ', _('Yemen')),
    (966, 'SA / SAU ', _('Saudi Arabia')),
    (965, 'KW / KWT ', _('Kuwait')),
    (964, 'IQ / IRQ ', _('Iraq')),
    (963, 'SY / SYR ', _('Syria')),
    (962, 'JO / JOR ', _('Jordan')),
    (961, 'LB / LBN ', _('Lebanon')),
    (960, 'MV / MDV ', _('Maldives')),
    (886, 'TW / TWN ', _('Taiwan')),
    (880, 'BD / BGD ', _('Bangladesh')),
    (870, 'PN / PCN ', _('Pitcairn Islands')),
    (856, 'LA / LAO ', _('Laos')),
    (855, 'KH / KHM ', _('Cambodia')),
    (853, 'MO / MAC ', _('Macau')),
    (852, 'HK / HKG ', _('Hong Kong')),
    (850, 'KP / PRK ', _('North Korea')),
    (692, 'MH / MHL ', _('Marshall Islands')),
    (691, 'FM / FSM ', _('Micronesia')),
    (690, 'TK / TKL ', _('Tokelau')),
    (689, 'PF / PYF ', _('French Polynesia')),
    (688, 'TV / TUV ', _('Tuvalu')),
    (687, 'NC / NCL ', _('New Caledonia')),
    (686, 'KI / KIR ', _('Kiribati')),
    (685, 'WS / WSM ', _('Samoa')),
    (683, 'NU / NIU ', _('Niue')),
    (682, 'CK / COK ', _('Cook Islands')),
    (681, 'WF / WLF ', _('Wallis and Futuna')),
    (680, 'PW / PLW ', _('Palau')),
    (679, 'FJ / FJI ', _('Fiji')),
    (678, 'VU / VUT ', _('Vanuatu')),
    (677, 'SB / SLB ', _('Solomon Islands')),
    (676, 'TO / TON ', _('Tonga')),
    (675, 'PG / PNG ', _('Papua New Guinea')),
    (674, 'NR / NRU ', _('Nauru')),
    (673, 'BN / BRN ', _('Brunei')),
    (672, 'AQ / ATA ', _('Antarctica')),
    (672, ' / NFK ', _('Norfolk Island')),
    (670, 'TL / TLS ', _('Timor-Leste')),
    (599, 'AN / ANT ', _('Netherlands Antilles')),
    (598, 'UY / URY ', _('Uruguay')),
    (597, 'SR / SUR ', _('Suriname')),
    (595, 'PY / PRY ', _('Paraguay')),
    (593, 'EC / ECU ', _('Ecuador')),
    (592, 'GY / GUY ', _('Guyana')),
    (591, 'BO / BOL ', _('Bolivia')),
    (590, 'BL / BLM ', _('Saint Barthelemy')),
    (509, 'HT / HTI ', _('Haiti')),
    (508, 'PM / SPM ', _('Saint Pierre and Miquelon')),
    (507, 'PA / PAN ', _('Panama')),
    (506, 'CR / CRC ', _('Costa Rica')),
    (505, 'NI / NIC ', _('Nicaragua')),
    (504, 'HN / HND ', _('Honduras')),
    (503, 'SV / SLV ', _('El Salvador')),
    (502, 'GT / GTM ', _('Guatemala')),
    (501, 'BZ / BLZ ', _('Belize')),
    (500, 'FK / FLK ', _('Falkland Islands')),
    (423, 'LI / LIE ', _('Liechtenstein')),
    (421, 'SK / SVK ', _('Slovakia')),
    (420, 'CZ / CZE ', _('Czech Republic')),
    (389, 'MK / MKD ', _('Macedonia')),
    (387, 'BA / BIH ', _('Bosnia and Herzegovina')),
    (386, 'SI / SVN ', _('Slovenia')),
    (385, 'HR / HRV ', _('Croatia')),
    (382, 'ME / MNE ', _('Montenegro')),
    (381, ' /  ', _('Kosovo')),
    (381, 'RS / SRB ', _('Serbia')),
    (380, 'UA / UKR ', _('Ukraine')),
    (378, 'SM / SMR ', _('San Marino')),
    (377, 'MC / MCO ', _('Monaco')),
    (376, 'AD / AND ', _('Andorra')),
    (375, 'BY / BLR ', _('Belarus')),
    (374, 'AM / ARM ', _('Armenia')),
    (373, 'MD / MDA ', _('Moldova')),
    (372, 'EE / EST ', _('Estonia')),
    (371, 'LV / LVA ', _('Latvia')),
    (370, 'LT / LTU ', _('Lithuania')),
    (359, 'BG / BGR ', _('Bulgaria')),
    (358, 'FI / FIN ', _('Finland')),
    (357, 'CY / CYP ', _('Cyprus')),
    (356, 'MT / MLT ', _('Malta')),
    (355, 'AL / ALB ', _('Albania')),
    (354, 'IS / IS ', _('Iceland')),
    (353, 'IE / IRL ', _('Ireland')),
    (352, 'LU / LUX ', _('Luxembourg')),
    (351, 'PT / PRT ', _('Portugal')),
    (350, 'GI / GIB ', _('Gibraltar')),
    (299, 'GL / GRL ', _('Greenland')),
    (298, 'FO / FRO ', _('Faroe Islands')),
    (297, 'AW / ABW ', _('Aruba')),
    (291, 'ER / ERI ', _('Eritrea')),
    (290, 'SH / SHN ', _('Saint Helena')),
    (269, 'KM / COM ', _('Comoros')),
    (268, 'SZ / SWZ ', _('Swaziland')),
    (267, 'BW / BWA ', _('Botswana')),
    (266, 'LS / LSO ', _('Lesotho')),
    (265, 'MW / MWI ', _('Malawi')),
    (264, 'NA / NAM ', _('Namibia')),
    (263, 'ZW / ZWE ', _('Zimbabwe')),
    (262, 'YT / MYT ', _('Mayotte')),
    (261, 'MG / MDG ', _('Madagascar')),
    (260, 'ZM / ZMB ', _('Zambia')),
    (258, 'MZ / MOZ ', _('Mozambique')),
    (257, 'BI / BDI ', _('Burundi')),
    (256, 'UG / UGA ', _('Uganda')),
    (255, 'TZ / TZA ', _('Tanzania')),
    (254, 'KE / KEN ', _('Kenya')),
    (253, 'DJ / DJI ', _('Djibouti')),
    (252, 'SO / SOM ', _('Somalia')),
    (251, 'ET / ETH ', _('Ethiopia')),
    (250, 'RW / RWA ', _('Rwanda')),
    (249, 'SD / SDN ', _('Sudan')),
    (248, 'SC / SYC ', _('Seychelles')),
    (245, 'GW / GNB ', _('Guinea-Bissau')),
    (244, 'AO / AGO ', _('Angola')),
    (243, 'CD / COD ', _('Democratic Republic of the Congo')),
    (242, 'CG / COG ', _('Republic of the Congo')),
    (241, 'GA / GAB ', _('Gabon')),
    (240, 'GQ / GNQ ', _('Equatorial Guinea')),
    (239, 'ST / STP ', _('Sao Tome and Principe')),
    (238, 'CV / CPV ', _('Cape Verde')),
    (237, 'CM / CMR ', _('Cameroon')),
    (236, 'CF / CAF ', _('Central African Republic')),
    (235, 'TD / TCD ', _('Chad')),
    (234, 'NG / NGA ', _('Nigeria')),
    (233, 'GH / GHA ', _('Ghana')),
    (232, 'SL / SLE ', _('Sierra Leone')),
    (231, 'LR / LBR ', _('Liberia')),
    (230, 'MU / MUS ', _('Mauritius')),
    (229, 'BJ / BEN ', _('Benin')),
    (228, 'TG / TGO ', _('Togo')),
    (227, 'NE / NER ', _('Niger')),
    (226, 'BF / BFA ', _('Burkina Faso')),
    (225, 'CI / CIV ', _('Ivory Coast')),
    (224, 'GN / GIN ', _('Guinea')),
    (223, 'ML / MLI ', _('Mali')),
    (222, 'MR / MRT ', _('Mauritania')),
    (221, 'SN / SEN ', _('Senegal')),
    (220, 'GM / GMB ', _('Gambia')),
    (218, 'LY / LBY ', _('Libya')),
    (216, 'TN / TUN ', _('Tunisia')),
    (213, 'DZ / DZA ', _('Algeria')),
    (212, 'MA / MAR ', _('Morocco')),
    (98, 'IR / IRN ', _('Iran')),
    (95, 'MM / MMR ', _('Burma (Myanmar)')),
    (94, 'LK / LKA ', _('Sri Lanka')),
    (93, 'AF / AFG ', _('Afghanistan')),
    (92, 'PK / PAK ', _('Pakistan')),
    (91, 'IN / IND ', _('India')),
    (90, 'TR / TUR ', _('Turkey')),
    (86, 'CN / CHN ', _('China')),
    (84, 'VN / VNM ', _('Vietnam')),
    (82, 'KR / KOR ', _('South Korea')),
    (81, 'JP / JPN ', _('Japan')),
    (66, 'TH / THA ', _('Thailand')),
    (65, 'SG / SGP ', _('Singapore')),
    (64, 'NZ / NZL ', _('New Zealand')),
    (63, 'PH / PHL ', _('Philippines')),
    (62, 'ID / IDN ', _('Indonesia')),
    (61, 'AU / AUS ', _('Australia')),
    (61, 'CX / CXR ', _('Christmas Island')),
    (61, 'CC / CCK ', _('Cocos (Keeling) Islands')),
    (60, 'MY / MYS ', _('Malaysia')),
    (58, 'VE / VEN ', _('Venezuela')),
    (57, 'CO / COL ', _('Colombia')),
    (56, 'CL / CHL ', _('Chile')),
    (55, 'BR / BRA ', _('Brazil')),
    (54, 'AR / ARG ', _('Argentina')),
    (53, 'CU / CUB ', _('Cuba')),
    (52, 'MX / MEX ', _('Mexico')),
    (51, 'PE / PER ', _('Peru')),
    (49, 'DE / DEU ', _('Germany')),
    (48, 'PL / POL ', _('Poland')),
    (47, 'NO / NOR ', _('Norway')),
    (46, 'SE / SWE ', _('Sweden')),
    (45, 'DK / DNK ', _('Denmark')),
    (44, 'IM / IMN ', _('Isle of Man')),
    (44, 'GB / GBR ', _('United Kingdom')),
    (43, 'AT / AUT ', _('Austria')),
    (41, 'CH / CHE ', _('Switzerland')),
    (40, 'RO / ROU ', _('Romania')),
    (39, 'IT / ITA ', _('Italy')),
    (39, 'VA / VAT ', _('Holy See (Vatican City)')),
    (36, 'HU / HUN ', _('Hungary')),
    (34, 'ES / ESP ', _('Spain')),
    (33, 'FR / FRA ', _('France')),
    (32, 'BE / BEL ', _('Belgium')),
    (31, 'NL / NLD ', _('Netherlands')),
    (30, 'GR / GRC ', _('Greece')),
    (27, 'ZA / ZAF ', _('South Africa')),
    (20, 'EG / EGY ', _('Egypt')),
    (7, 'KZ / KAZ ', _('Kazakhstan')),
    (7, 'RU / RUS ', _('Russia')),
    (1, 'PR / PRI ', _('Puerto Rico')),
    (1, 'US / USA ', _('United States')),
    (1, 'CA / CAN ', _('Canada')),
    (1684, 'AS / ASM ', _('American Samoa')),
    (1264, 'AI / AIA ', _('Anguilla')),
    (1268, 'AG / ATG ', _('Antigua and Barbuda')),
    (1242, 'BS / BHS ', _('Bahamas')),
    (1246, 'BB / BRB ', _('Barbados')),
    (1441, 'BM / BMU ', _('Bermuda')),
    (1284, 'VG / VGB ', _('British Virgin Islands')),
    (1345, 'KY / CYM ', _('Cayman Islands')),
    (1767, 'DM / DMA ', _('Dominica')),
    (1809, 'DO / DOM ', _('Dominican Republic')),
    (1473, 'GD / GRD ', _('Grenada')),
    (1671, 'GU / GUM ', _('Guam')),
    (1876, 'JM / JAM ', _('Jamaica')),
    (1664, 'MS / MSR ', _('Montserrat')),
    (1670, 'MP / MNP ', _('Northern Mariana Islands')),
    (1869, 'KN / KNA ', _('Saint Kitts and Nevis')),
    (1758, 'LC / LCA ', _('Saint Lucia')),
    (1599, 'MF / MAF ', _('Saint Martin')),
    (1784, 'VC / VCT ', _('Saint Vincent and the Grenadines')),
    (1868, 'TT / TTO ', _('Trinidad and Tobago')),
    (1649, 'TC / TCA ', _('Turks and Caicos Islands')),
    (1340, 'VI / VIR ', _('US Virgin Islands')),
    (None, 'EH / ESH ', _('Western Sahara')),
    (None, 'IO / IOT ', _('British Indian Ocean Territory')),
    (None, 'JE / JEY ', _('Jersey')),
    (None, 'SJ / SJM ', _('Svalbard')),
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
    max_full_phone_length = 15

    def clean(self, value):
        """
        >>> str(FullPhoneFormField().clean(u'79254525702'))
        '+79254525702'
        >>> str(FullPhoneFormField().clean('9161234567'))
        '+79161234567'
        >>> str(FullPhoneFormField().clean('89161234567'))
        '+79161234567'
        >>> str(FullPhoneFormField().clean('+7(916)1234567'))
        '+79161234567'
        >>> str(FullPhoneFormField().clean('(916)1234567'))
        '+79161234567'
        >>> str(FullPhoneFormField().clean(u' 8(916)-123-45-67 '))
        '+79161234567'
        >>> str(FullPhoneFormField().clean(u'+37412345678'))
        '+37412345678'
        """
        if value:
            value = value.strip()

            phone = None
            code = None

            has_country_code = value.startswith('+')
            value = value.lstrip('+')
            value = re.sub('[^\d]', '', value)

            if not value or len(value) > self.max_full_phone_length:
                raise ValidationError(ugettext('Incorrect phone'))

            if value.startswith(self.default_code):
                phone = value[len(self.default_code):]
                code = self.default_code
            elif not has_country_code and (value.startswith('8') or value.startswith('9')):
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
