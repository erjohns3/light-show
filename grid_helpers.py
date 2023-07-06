import PIL
from PIL import Image, ImageSequence
import numpy as np
import serial

from helpers import *


try:
    profile
except NameError:
    profile = lambda x: x


grid_serial = None


GRID_WIDTH = 20
GRID_HEIGHT = 32
GRID_SIZE = GRID_HEIGHT * GRID_WIDTH * 3

GRID_ROW = np.arange(GRID_WIDTH)
GRID_COL = np.arange(GRID_HEIGHT)

grid = np.array(np.zeros((GRID_WIDTH, GRID_HEIGHT, 3)), np.double)

grid_index = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 183, 184, 185, 180, 181, 182, 177, 178, 179, 174, 175, 176, 171, 172, 173, 168, 169, 170, 165, 166, 167, 162, 163, 164, 159, 160, 161, 156, 157, 158, 153, 154, 155, 150, 151, 152, 147, 148, 149, 144, 145, 146, 141, 142, 143, 141, 142, 143, 138, 139, 140, 135, 136, 137, 132, 133, 134, 129, 130, 131, 126, 127, 128, 123, 124, 125, 123, 124, 125, 120, 121, 122, 117, 118, 119, 114, 115, 116, 111, 112, 113, 108, 109, 110, 105, 106, 107, 102, 103, 104, 99, 100, 101, 96, 97, 98, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 378, 379, 380, 375, 376, 377, 372, 373, 374, 369, 370, 371, 366, 367, 368, 363, 364, 365, 360, 361, 362, 357, 358, 359, 354, 355, 356, 351, 352, 353, 348, 349, 350, 345, 346, 347, 342, 343, 344, 339, 340, 341, 336, 337, 338, 333, 334, 335, 330, 331, 332, 327, 328, 329, 324, 325, 326, 321, 322, 323, 318, 319, 320, 315, 316, 317, 312, 313, 314, 309, 310, 311, 306, 307, 308, 303, 304, 305, 300, 301, 302, 297, 298, 299, 294, 295, 296, 291, 292, 293, 288, 289, 290, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 573, 574, 575, 570, 571, 572, 567, 568, 569, 564, 565, 566, 561, 562, 563, 558, 559, 560, 555, 556, 557, 552, 553, 554, 549, 550, 551, 546, 547, 548, 543, 544, 545, 540, 541, 542, 537, 538, 539, 534, 535, 536, 531, 532, 533, 528, 529, 530, 525, 526, 527, 522, 523, 524, 519, 520, 521, 516, 517, 518, 513, 514, 515, 510, 511, 512, 507, 508, 509, 504, 505, 506, 501, 502, 503, 498, 499, 500, 495, 496, 497, 492, 493, 494, 489, 490, 491, 486, 487, 488, 483, 484, 485, 480, 481, 482, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 765, 766, 767, 762, 763, 764, 759, 760, 761, 756, 757, 758, 753, 754, 755, 750, 751, 752, 747, 748, 749, 744, 745, 746, 741, 742, 743, 738, 739, 740, 735, 736, 737, 732, 733, 734, 729, 730, 731, 726, 727, 728, 723, 724, 725, 720, 721, 722, 717, 718, 719, 714, 715, 716, 711, 712, 713, 708, 709, 710, 705, 706, 707, 702, 703, 704, 699, 700, 701, 696, 697, 698, 693, 694, 695, 690, 691, 692, 687, 688, 689, 684, 685, 686, 681, 682, 683, 678, 679, 680, 675, 676, 677, 672, 673, 674, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 957, 958, 959, 954, 955, 956, 951, 952, 953, 948, 949, 950, 945, 946, 947, 942, 943, 944, 939, 940, 941, 936, 937, 938, 933, 934, 935, 930, 931, 932, 927, 928, 929, 924, 925, 926, 921, 922, 923, 918, 919, 920, 915, 916, 917, 912, 913, 914, 909, 910, 911, 906, 907, 908, 903, 904, 905, 900, 901, 902, 897, 898, 899, 894, 895, 896, 891, 892, 893, 888, 889, 890, 885, 886, 887, 882, 883, 884, 879, 880, 881, 876, 877, 878, 873, 874, 875, 870, 871, 872, 867, 868, 869, 864, 865, 866, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1149, 1150, 1151, 1146, 1147, 1148, 1143, 1144, 1145, 1140, 1141, 1142, 1137, 1138, 1139, 1134, 1135, 1136, 1131, 1132, 1133, 1128, 1129, 1130, 1125, 1126, 1127, 1122, 1123, 1124, 1119, 1120, 1121, 1116, 1117, 1118, 1113, 1114, 1115, 1110, 1111, 1112, 1107, 1108, 1109, 1104, 1105, 1106, 1101, 1102, 1103, 1098, 1099, 1100, 1095, 1096, 1097, 1092, 1093, 1094, 1089, 1090, 1091, 1086, 1087, 1088, 1083, 1084, 1085, 1080, 1081, 1082, 1077, 1078, 1079, 1074, 1075, 1076, 1071, 1072, 1073, 1068, 1069, 1070, 1065, 1066, 1067, 1062, 1063, 1064, 1059, 1060, 1061, 1056, 1057, 1058, 1152, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1193, 1194, 1195, 1196, 1197, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246, 1247, 1341, 1342, 1343, 1338, 1339, 1340, 1335, 1336, 1337, 1332, 1333, 1334, 1329, 1330, 1331, 1326, 1327, 1328, 1323, 1324, 1325, 1320, 1321, 1322, 1317, 1318, 1319, 1314, 1315, 1316, 1311, 1312, 1313, 1308, 1309, 1310, 1305, 1306, 1307, 1302, 1303, 1304, 1299, 1300, 1301, 1296, 1297, 1298, 1293, 1294, 1295, 1290, 1291, 1292, 1287, 1288, 1289, 1284, 1285, 1286, 1281, 1282, 1283, 1278, 1279, 1280, 1275, 1276, 1277, 1272, 1273, 1274, 1269, 1270, 1271, 1266, 1267, 1268, 1263, 1264, 1265, 1260, 1261, 1262, 1257, 1258, 1259, 1254, 1255, 1256, 1251, 1252, 1253, 1248, 1249, 1250, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1360, 1361, 1362, 1363, 1364, 1365, 1366, 1367, 1368, 1369, 1370, 1371, 1372, 1373, 1374, 1375, 1376, 1377, 1378, 1379, 1380, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1392, 1393, 1394, 1395, 1396, 1397, 1398, 1399, 1400, 1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1410, 1411, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1420, 1421, 1422, 1423, 1424, 1425, 1426, 1427, 1428, 1429, 1430, 1431, 1432, 1433, 1434, 1435, 1436, 1437, 1438, 1439, 1533, 1534, 1535, 1530, 1531, 1532, 1527, 1528, 1529, 1524, 1525, 1526, 1521, 1522, 1523, 1518, 1519, 1520, 1515, 1516, 1517, 1512, 1513, 1514, 1509, 1510, 1511, 1506, 1507, 1508, 1503, 1504, 1505, 1500, 1501, 1502, 1497, 1498, 1499, 1494, 1495, 1496, 1491, 1492, 1493, 1488, 1489, 1490, 1485, 1486, 1487, 1482, 1483, 1484, 1479, 1480, 1481, 1476, 1477, 1478, 1473, 1474, 1475, 1470, 1471, 1472, 1467, 1468, 1469, 1464, 1465, 1466, 1461, 1462, 1463, 1458, 1459, 1460, 1455, 1456, 1457, 1452, 1453, 1454, 1449, 1450, 1451, 1446, 1447, 1448, 1443, 1444, 1445, 1440, 1441, 1442, 1536, 1537, 1538, 1539, 1540, 1541, 1542, 1543, 1544, 1545, 1546, 1547, 1548, 1549, 1550, 1551, 1552, 1553, 1554, 1555, 1556, 1557, 1558, 1559, 1560, 1561, 1562, 1563, 1564, 1565, 1566, 1567, 1568, 1569, 1570, 1571, 1572, 1573, 1574, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583, 1584, 1585, 1586, 1587, 1588, 1589, 1590, 1591, 1592, 1593, 1594, 1595, 1596, 1597, 1598, 1599, 1600, 1601, 1602, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612, 1613, 1614, 1615, 1616, 1617, 1618, 1619, 1620, 1621, 1622, 1623, 1624, 1625, 1626, 1627, 1628, 1629, 1630, 1631, 1725, 1726, 1727, 1722, 1723, 1724, 1719, 1720, 1721, 1716, 1717, 1718, 1713, 1714, 1715, 1710, 1711, 1712, 1707, 1708, 1709, 1704, 1705, 1706, 1701, 1702, 1703, 1698, 1699, 1700, 1695, 1696, 1697, 1692, 1693, 1694, 1689, 1690, 1691, 1686, 1687, 1688, 1683, 1684, 1685, 1680, 1681, 1682, 1677, 1678, 1679, 1674, 1675, 1676, 1671, 1672, 1673, 1668, 1669, 1670, 1665, 1666, 1667, 1662, 1663, 1664, 1659, 1660, 1661, 1656, 1657, 1658, 1653, 1654, 1655, 1650, 1651, 1652, 1647, 1648, 1649, 1644, 1645, 1646, 1641, 1642, 1643, 1638, 1639, 1640, 1635, 1636, 1637, 1632, 1633, 1634, 1728, 1729, 1730, 1731, 1732, 1733, 1734, 1735, 1736, 1737, 1738, 1739, 1740, 1741, 1742, 1743, 1744, 1745, 1746, 1747, 1748, 1749, 1750, 1751, 1752, 1753, 1754, 1755, 1756, 1757, 1758, 1759, 1760, 1761, 1762, 1763, 1764, 1765, 1766, 1767, 1768, 1769, 1770, 1771, 1772, 1773, 1774, 1775, 1776, 1777, 1778, 1779, 1780, 1781, 1782, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 1790, 1791, 1792, 1793, 1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803, 1804, 1805, 1806, 1807, 1808, 1809, 1810, 1811, 1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1917, 1918, 1919, 1914, 1915, 1916, 1911, 1912, 1913, 1908, 1909, 1910, 1905, 1906, 1907, 1902, 1903, 1904, 1899, 1900, 1901, 1896, 1897, 1898, 1893, 1894, 1895, 1890, 1891, 1892, 1887, 1888, 1889, 1884, 1885, 1886, 1881, 1882, 1883, 1878, 1879, 1880, 1875, 1876, 1877, 1872, 1873, 1874, 1869, 1870, 1871, 1866, 1867, 1868, 1863, 1864, 1865, 1860, 1861, 1862, 1857, 1858, 1859, 1854, 1855, 1856, 1851, 1852, 1853, 1848, 1849, 1850, 1845, 1846, 1847, 1842, 1843, 1844, 1839, 1840, 1841, 1836, 1837, 1838, 1833, 1834, 1835, 1830, 1831, 1832, 1827, 1828, 1829, 1824, 1825, 1826])

def get_grid_width():
    return GRID_WIDTH

def get_grid_height():
    return GRID_HEIGHT

def grid_coords():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            yield (x, y)

def get_grid():
    return grid


@profile
def render_grid(terminal=False, skip_if_terminal=False, reset_terminal=True):
    if terminal:
        if skip_if_terminal:
            return
        for y in range(GRID_HEIGHT):
            row_parts = []
            for x in range(GRID_WIDTH):
                rgb = tuple(map(lambda x: int(x * 2.55), grid[x][y]))
                row_parts.append(rgb_ansi('▆', rgb))
            print(''.join(row_parts))
        if reset_terminal:
            print('\033[F' * GRID_HEIGHT, end='')
    else:
        grid_out = get_grid_serial().out_waiting
        grid_in = get_grid_serial().in_waiting

        if grid_out == 0 and grid_in > 0:
            get_grid_serial().read(grid_in)
            get_grid_serial().write(grid_pack())

def get_grid_index():
    return grid_index


def grid_in_bounds(pos):
    # !TODO it seems like for now grid_pack sends all 640 (1920 RGB) over, even thought there are 3 spots that are empty, ask eric later
    # print(len(grid_index), GRID_HEIGHT * GRID_WIDTH * 3)
    x, y = pos
    if x < 0 or y < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
        return False
    return True
    index = grid_index[x][y] * 3
    return index >= 0

def grid_pack():
    return (np.round(grid.reshape(GRID_SIZE)[grid_index] * 127 / 100) * 2).astype(np.byte).tobytes()

def grid_fill(to_fill):
    if type(to_fill) in [float, int]:
        return grid.fill(0)
    for x, y in grid_coords():
        for rgb_index, value in enumerate(to_fill):
            grid[x][y][rgb_index] = value

def grid_fill_and_write(to_fill):
    grid_fill(to_fill)
    render_grid()

def grid_reset():
    grid.fill(0)

def grid_reset_and_write():
    grid_reset()
    render_grid()

def get_grid_serial():
    global grid_serial
    if grid_serial is None: 
        grid_serial = serial.Serial(
            port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
            baudrate = 2000000,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0,
            write_timeout=0
        )
    return grid_serial



# ====== image stuff ======

@profile
def resize_PIL_image(pil_image, rotate_90=False):
    desired_width = GRID_WIDTH
    desired_height = GRID_HEIGHT
    if rotate_90:
        desired_width = GRID_HEIGHT
        desired_height = GRID_WIDTH
    
    # rely on cache here
    if pil_image.size[0] != desired_width or pil_image.size[1] != desired_height:
        print_yellow(f'resizeing image, this should only happen once, if you see it multiple runs theres something wrong')
        pil_image = pil_image.resize((desired_width, desired_height), Image.LANCZOS)
    
    return pil_image


@profile
def recolor_PIL_image(pil_image):
    if pil_image.mode != 'RGB':
        print_yellow(f'was {pil_image.mode=}, but recoloring image to RGB, this should only happen once, if you see it multiple runs theres something wrong')
        pil_image = pil_image.convert('RGB')
    return pil_image


@profile
def resize_and_color_PIL_image(pil_image, rotate_90=False):
    pil_image = resize_PIL_image(pil_image, rotate_90=rotate_90)
    pil_image = recolor_PIL_image(pil_image)
    return pil_image


@profile
def PIL_image_to_numpy_arr(pil_image, rotate_90=False):
    pil_image = resize_and_color_PIL_image(pil_image, rotate_90=rotate_90)
    
    # this is because we are working with 0-100 in the grid, not 0-255
    np_arr = np.array(pil_image) / 2.55

    # https://www.desmos.com/calculator
    # iterate through numpy array and run ln(x) * 22
    np_arr = np.power(np_arr, 2.2) * .004
    # np_arr = np.log(np_arr) * 22

    np_arr = np_arr.astype(np.uint8)

    if rotate_90:
        return np_arr
    return np.transpose(np_arr, (1, 0, 2))


resize_cache_dir = get_temp_dir().joinpath('image_resize_cache')
make_if_not_exist(resize_cache_dir)

static_image_cache = {}
def load_image_to_grid(image_filepath, rotate_90=False):
    if image_filepath not in static_image_cache:
        with Image.open(image_filepath) as image_file:
            static_image_cache[image_filepath] = PIL_image_to_numpy_arr(image_file, rotate_90=rotate_90)
    grid[:] = static_image_cache[image_filepath]


animation_cache = {}
@profile
def try_load_into_animation_cache(filepath, rotate_90=False):
    with Image.open(filepath) as animation_file:
        print(f'loading animation {filepath.name}, {animation_file.info=}')
        if not animation_file.is_animated:
            raise Exception(f'file {filepath} is not animated, and yet was called load_into_animation, not loading')

        total_duration = 0
        all_frames = []
        for frame in ImageSequence.Iterator(animation_file):
            frame.load() # for webps you need to call load for it to calculate the duration

            duration = frame.info["duration"] / 1000
            total_duration += duration

            all_frames.append([PIL_image_to_numpy_arr(frame, rotate_90=rotate_90), duration])
        animation_cache[filepath] = [0, all_frames, total_duration]
        print(f'loaded animation {filepath.name}, {total_duration=}, {len(all_frames)=}, shape {all_frames[0][0].shape}')
        # exit()


def load_animation_to_grid(filepath, rotate_90=False):
    if filepath not in animation_cache:
        try_load_into_animation_cache(filepath, rotate_90=rotate_90)
    index = animation_cache[filepath][0]
    frames = animation_cache[filepath][1]
    grid[:] = frames[index][0]


def increment_animation_frame(filepath):
    if filepath not in animation_cache:
        print(f'filepath {filepath} not in animation cache')
        return
    index = animation_cache[filepath][0]
    frames = animation_cache[filepath][1]
    animation_cache[filepath][0] = (index + 1) % len(frames)


def get_png_path(filepath):
    filepath = filepath.with_suffix('.png')
    if not filepath.exists():
        with Image.open(filepath) as pil_image:
            pil_image.save(filepath, format='png')
        print(f'new png file created {filepath}')
    return filepath


def save_resize_and_color_image(source_path, destination_path, rotate_90=False):
    with Image.open(source_path) as pil_image:
        if getattr(pil_image, 'is_animated', None):
            converted_frames = []
            for frame in ImageSequence.Iterator(pil_image):
                frame.load()
                converted_frames.append(resize_and_color_PIL_image(frame, rotate_90=rotate_90))
                # !TODO i have a hunch that the webp (nyan.webp) at least is getting lost compresesion if i recolor it because RGB might by lossy, only RGBA is lossless
                # converted_frames.append(resize_PIL_image(frame, rotate_90=rotate_90))
            return converted_frames[0].save(destination_path, save_all=True, append_images=converted_frames[1:], quality=100)

    with Image.open(source_path) as static_pil_image:
        resize_and_color_PIL_image(static_pil_image, rotate_90=rotate_90).save(destination_path, format=destination_path.suffix[1:].lower(), quality=100)


# !TODO this is linear, could make log(n) if someone writes a BST 
def seek_to_animation_time(filepath, time_to_seek):
    if filepath not in animation_cache:
        print(f'filepath {filepath} not in animation cache')
        return
    total_duration = animation_cache[filepath][2]
    time_to_seek = time_to_seek % total_duration
    frames = animation_cache[filepath][1]
    time_so_far = 0
    for index, (_frame, duration) in enumerate(frames):
        time_so_far += duration
        if time_so_far > time_to_seek:
            animation_cache[filepath][0] = index
            # print(f'seeking to {time_to_seek} in {filepath}, {index=}, {time_so_far=}, {duration=}')
            return


def is_animated(filepath):
    if filepath not in animation_cache:
        return False
    return True


def fill_grid_from_image_filepath(filepath, rotate_90=False):
    if filepath.suffix.lower() in ['.webp', '.gif']:
        load_animation_to_grid(filepath, rotate_90=rotate_90)
    elif filepath.suffix.lower() in ['.jpg', '.jpeg', '.png']:
        load_image_to_grid(filepath, rotate_90=rotate_90)
    else:
        print_red(f'file suffix {filepath.suffix} not supported')


this_file_directory = pathlib.Path(__file__).parent.resolve()
run_once = set()
def get_cached_converted_filepath(filename, rotate_90=False):
    filepath = this_file_directory.joinpath('images', filename)
    cache_filepath = resize_cache_dir.joinpath(f'{rotate_90}_' + filepath.name)

    # jpgs have horrible artifacts, so we convert them to pngs, note we will have to do this for mpegs too, and maybe webps
    if cache_filepath.suffix.lower() in ['.jpg', '.jpeg']:
        cache_filepath = cache_filepath.with_suffix('.png')

    if (False and filepath not in run_once) or not cache_filepath.exists():
        save_resize_and_color_image(source_path=filepath, destination_path=cache_filepath, rotate_90=rotate_90)
        print(f'cached {filepath} to {cache_filepath}')
        run_once.add(filepath)
    return cache_filepath


from PIL import Image, ImageDraw, ImageFont
def random_pilmoji_havent_worked():
    from pilmoji import Pilmoji

    im = Image.new('RGB', (1024, 768))

    drawer = Pilmoji(im)

    FONT_PATH = './NotoSansSC-Regular.otf'
    font_size = 30
    font = ImageFont.truetype(FONT_PATH, size=font_size)

    text = "Hello, world! 👋 Here are some emojis: 🎨 🌊 😎"
    drawer((10, 10), text, font=font)

    im.show()

def create_image_from_text_pilmoji(text, font_size=12, rotate_90=False):
    hash_filename = hash(text)
    output_filepath = get_temp_dir().joinpath(f'{hash_filename}.png')
    if output_filepath.exists():
        return output_filepath

    from pilmoji import Pilmoji
    if not rotate_90:
        width, height = 32, 20
    else:
        width, height = 20, 32
    image = Image.new('RGB', (width, height), 'black')
    
    # C:\Windows\Fonts
    # font_name = 'NotoEmoji-Medium.ttf'
    # font_name = 'Noto-Medium.ttf'
    # font_name = 'arial.ttf'
    # font_name = 'ariblk.ttf'
    font_name = 'sitka-small.ttf'
    filepath_font = get_ray_directory().joinpath('random', 'fonts', font_name)
    font = ImageFont.truetype(str(filepath_font), font_size)

    with Pilmoji(image) as pilmoji:
        # !TODO get a better method for this
        # text_width, text_height = pilmoji_drawer.textsize(text, font)
        draw = ImageDraw.Draw(image)
        text_width, text_height = draw.textsize(text, font)

        x = (width - text_width) // 2
        y = (height - text_height) // 2
        pilmoji.text((x, y), text, (255, 255, 255), font)


    if not rotate_90:
        image = image.rotate(90, expand=True)

    image.save(output_filepath)
    return output_filepath


def create_image_from_text(text, rotate_90=False):
    if not rotate_90:
        width, height = 32, 20
    else:
        width, height = 20, 32
    image = Image.new('RGB', (width, height), 'black')

    draw = ImageDraw.Draw(image)
    
    # font_name = 'NotoEmoji-Medium.ttf'
    font_name = 'NotoColorEmoji-Regular.ttf'
    filepath_font = get_ray_directory().joinpath('random', 'fonts', font_name)
    font = ImageFont.truetype(str(filepath_font), 20)

    # text_width, text_height = draw.textsize(text, font)
    # text_width, text_height = draw.textsize(text, font, 'white')
    text_width, text_height = draw.textsize(text, font)

    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # draw.text((x, y), text, font=font)
    draw.text((x, y), text, font=font, embedded_color=True) 


    if not rotate_90:
        image = image.rotate(90, expand=True)

    hash_filename = hash(text)
    filepath = get_temp_dir().joinpath(f'{hash_filename}.png')
    image.save(filepath)
    return filepath

